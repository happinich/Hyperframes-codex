#!/usr/bin/env python3
"""Align authored narration text to Whisper timing and write upload caption files."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

from korean_tts_normalization import normalize_korean_tts_text


@dataclass
class TimedToken:
    text: str
    start: float
    end: float
    matched: bool


def normalized(text: str) -> str:
    return "".join(char.lower() for char in text if char.isalnum())


def character_coverage(script: str, raw_words: list[dict]) -> float:
    script_norm = normalized(normalize_korean_tts_text(script))
    heard_text = " ".join(word["text"] for word in raw_words)
    heard_norm = normalized(normalize_korean_tts_text(heard_text))
    if not script_norm or not heard_norm:
        return 0.0
    matcher = difflib.SequenceMatcher(None, script_norm, heard_norm, autojunk=False)
    return sum(block.size for block in matcher.get_matching_blocks()) / len(script_norm)


def timecode(seconds: float, vtt: bool = False) -> str:
    milliseconds = round(max(0, seconds) * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    separator = "." if vtt else ","
    return f"{hours:02}:{minutes:02}:{secs:02}{separator}{milliseconds:03}"


def align_tokens(script: str, raw_words: list[dict], duration: float) -> tuple[list[TimedToken], float]:
    pieces = re.findall(r"\S+", script)
    script_norm = normalized(script)
    heard_norm = ""
    heard_char_to_word: list[int] = []
    for index, word in enumerate(raw_words):
        chars = normalized(word["text"])
        heard_norm += chars
        heard_char_to_word.extend([index] * len(chars))
    if not script_norm:
        raise ValueError("narration.txt contains no spoken text")
    if not heard_norm:
        raise ValueError("Whisper found no spoken words in the audio")

    char_matches: dict[int, int] = {}
    matcher = difflib.SequenceMatcher(None, script_norm, heard_norm, autojunk=False)
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            char_matches[block.a + offset] = block.b + offset
    coverage = len(char_matches) / len(script_norm)

    cursor = 0
    timed: list[TimedToken] = []
    for piece in pieces:
        clean = normalized(piece)
        start_pos = cursor
        end_pos = cursor + len(clean)
        cursor = end_pos
        heard_positions = [char_matches[pos] for pos in range(start_pos, end_pos) if pos in char_matches]
        if heard_positions:
            word_indexes = [heard_char_to_word[pos] for pos in heard_positions]
            first = raw_words[min(word_indexes)]
            last = raw_words[max(word_indexes)]
            timed.append(TimedToken(piece, first["start"], last["end"], True))
        else:
            center = ((start_pos + end_pos) / 2) / max(len(script_norm), 1)
            estimated = min(duration, max(0.0, duration * center))
            timed.append(TimedToken(piece, estimated, min(duration, estimated + 0.22), False))

    # Missing punctuation or poorly recognized words inherit a readable local window.
    for index, token in enumerate(timed):
        if token.matched:
            continue
        previous = next((item for item in reversed(timed[:index]) if item.matched), None)
        following = next((item for item in timed[index + 1:] if item.matched), None)
        if previous and following:
            token.start = previous.end
            token.end = max(token.start + 0.12, following.start)
        elif previous:
            token.start = previous.end
            token.end = min(duration, token.start + 0.3)
        elif following:
            token.end = following.start
            token.start = max(0.0, token.end - 0.3)
    return timed, coverage


def make_cues(tokens: list[TimedToken], max_chars: int, max_seconds: float) -> list[dict]:
    cues: list[dict] = []
    current: list[TimedToken] = []
    for token in tokens:
        proposed = " ".join(item.text for item in current + [token])
        too_long = current and len(proposed) > max_chars
        too_slow = current and token.end - current[0].start > max_seconds
        if too_long or too_slow:
            cues.append(cue_from_tokens(current))
            current = []
        current.append(token)
    if current:
        cues.append(cue_from_tokens(current))
    return cues


def cue_from_tokens(tokens: list[TimedToken]) -> dict:
    return {
        "start": round(tokens[0].start, 3),
        "end": round(max(tokens[-1].end, tokens[0].start + 0.15), 3),
        "text": " ".join(token.text for token in tokens),
    }


def write_captions(cues: list[dict], sync_dir: Path) -> None:
    srt: list[str] = []
    vtt: list[str] = ["WEBVTT", ""]
    for number, cue in enumerate(cues, 1):
        srt.extend([
            str(number),
            f"{timecode(cue['start'])} --> {timecode(cue['end'])}",
            cue["text"],
            "",
        ])
        vtt.extend([
            f"{timecode(cue['start'], True)} --> {timecode(cue['end'], True)}",
            cue["text"],
            "",
        ])
    (sync_dir / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    (sync_dir / "captions.vtt").write_text("\n".join(vtt), encoding="utf-8")


def update_compositions(project: Path, cues: list[dict], duration: float, payload: dict) -> None:
    composition_dir = project / "04_composition"
    js = "window.HF_CAPTIONS = " + json.dumps(payload, ensure_ascii=False) + ";\n"
    (composition_dir / "transcript-data.js").write_text(js, encoding="utf-8")
    for name in ("index.html", "variants/shorts.html"):
        path = composition_dir / name
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        content = re.sub(
            r'(<audio id="voice"[^>]*data-start="0" data-duration=")[^"]+',
            rf"\g<1>{duration:.3f}",
            content,
        )
        content = re.sub(
            r"(<!-- GENERATED_CAPTIONS_BEGIN -->).*?(<!-- GENERATED_CAPTIONS_END -->)",
            lambda match: f"{match.group(1)}\n      {match.group(2)}",
            content,
            flags=re.DOTALL,
        )
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--model",
        default="mlx-community/whisper-large-v3-turbo",
        help="MLX Whisper model; defaults to mlx-community/whisper-large-v3-turbo",
    )
    parser.add_argument("--language", default="ko")
    parser.add_argument("--threshold", type=float, default=0.92)
    parser.add_argument("--max-caption-chars", type=int, default=26)
    args = parser.parse_args()

    project = args.project.resolve()
    script_path = project / "01_script" / "narration.txt"
    spoken_script_path = project / "01_script" / "tts-narration.txt"
    audio_path = project / "02_audio" / "working" / "voice.wav"
    if not script_path.exists() or not audio_path.exists():
        parser.error("project must contain narration.txt and normalized voice.wav")
    script = script_path.read_text(encoding="utf-8").strip()
    spoken_script = spoken_script_path.read_text(encoding="utf-8").strip() if spoken_script_path.exists() else script

    try:
        import mlx_whisper
    except ImportError:
        parser.error("install dependencies first: pip install -r requirements.txt")

    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=args.model,
        language=args.language,
        word_timestamps=True,
        condition_on_previous_text=False,
        hallucination_silence_threshold=1.0,
        verbose=False,
    )
    raw_segments: list[dict] = []
    raw_words: list[dict] = []
    for segment in result.get("segments", []):
        words = []
        for word in segment.get("words", []) or []:
            text = str(word.get("word") or word.get("text") or "").strip()
            if not text:
                continue
            item = {
                "text": text,
                "start": round(float(word["start"]), 3),
                "end": round(float(word["end"]), 3),
            }
            if item["text"]:
                words.append(item)
                raw_words.append(item)
        raw_segments.append({
            "start": round(float(segment.get("start", 0)), 3),
            "end": round(float(segment.get("end", 0)), 3),
            "text": str(segment.get("text", "")).strip(),
            "words": words,
        })
    duration = float(result.get("duration") or (raw_words[-1]["end"] if raw_words else 0))
    timed, caption_coverage = align_tokens(script, raw_words, duration)
    spoken_coverage = character_coverage(spoken_script, raw_words)
    cues = make_cues(timed, args.max_caption_chars, 3.6)
    sync_dir = project / "03_sync"
    sync_dir.mkdir(parents=True, exist_ok=True)
    raw_payload = {
        "backend": "mlx-whisper",
        "model": args.model,
        "language": args.language,
        "duration": duration,
        "segments": raw_segments,
    }
    (sync_dir / "whisper_raw.json").write_text(
        json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    payload = {"duration": round(duration, 3), "cues": cues, "words": [asdict(token) for token in timed]}
    (sync_dir / "captions.words.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_captions(cues, sync_dir)
    coverage = spoken_coverage if spoken_script_path.exists() else caption_coverage
    status = "ready_for_review" if coverage >= args.threshold else "alignment_review_required"
    report = {
        "status": status,
        "whisper_backend": "mlx-whisper",
        "whisper_model": args.model,
        "subtitle_delivery_mode": "external_srt_upload",
        "subtitle_text_source": "01_script/narration.txt",
        "spoken_text_source": "01_script/tts-narration.txt" if spoken_script_path.exists() else "01_script/narration.txt",
        "matched_character_ratio": round(coverage, 4),
        "caption_surface_match_ratio": round(caption_coverage, 4),
        "spoken_match_ratio": round(spoken_coverage, 4),
        "required_ratio": args.threshold,
        "note": "Captions are delivered as external SRT/VTT files. The rendered MP4 does not burn captions into the image.",
    }
    (sync_dir / "sync_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    update_compositions(project, cues, duration, payload)
    print(f"Captions: {sync_dir / 'captions.srt'}")
    print(f"Alignment: {coverage:.1%} ({status})")
    return 0 if status == "ready_for_review" else 2


if __name__ == "__main__":
    raise SystemExit(main())
