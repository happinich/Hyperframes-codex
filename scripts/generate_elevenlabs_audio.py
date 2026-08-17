#!/usr/bin/env python3
"""Generate narration audio from a project script using ElevenLabs TTS."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

from audio_mixing import (
    DEFAULT_BGM_FADE_OUT_SECONDS,
    DEFAULT_BGM_GAIN_DB,
    DEFAULT_BGM_OUTRO_GAIN_DB,
    DEFAULT_BGM_OUTRO_SECONDS,
    audio_duration_seconds,
    mix_bgm_with_voice,
)

DEFAULT_MODEL_ID = "eleven_v3"
DEFAULT_VOICE_SETTINGS = {
    "stability": 0.50,
    "similarity_boost": 0.75,
    "style": 0.15,
    "use_speaker_boost": True,
}
DEFAULT_MIN_CHARS = 1000
DEFAULT_MAX_CHARS = 1300


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sentence_units(text: str) -> list[str]:
    compact = re.sub(r"[ \t]+", " ", text.strip())
    if not compact:
        return []
    units = re.findall(r".+?(?:[.!?。！？]+[\"')\]]*|\n+|$)", compact, flags=re.S)
    return [unit.strip() for unit in units if unit.strip()]


def split_oversized_unit(unit: str, max_chars: int) -> list[str]:
    parts: list[str] = []
    remaining = unit.strip()
    while len(remaining) > max_chars:
        split_at = remaining.rfind("\n", 0, max_chars + 1)
        if split_at < max_chars // 2:
            split_at = remaining.rfind(" ", 0, max_chars + 1)
        if split_at < max_chars // 2:
            split_at = max_chars
        parts.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    if remaining:
        parts.append(remaining)
    return parts


def split_text_chunks(text: str, min_chars: int = DEFAULT_MIN_CHARS, max_chars: int = DEFAULT_MAX_CHARS) -> list[str]:
    if min_chars < 1 or max_chars < min_chars:
        raise ValueError("chunk character limits must satisfy 1 <= min_chars <= max_chars")

    chunks: list[str] = []
    current = ""
    for unit in sentence_units(text):
        candidates = split_oversized_unit(unit, max_chars) if len(unit) > max_chars else [unit]
        for candidate in candidates:
            # Sentence units should remain natural prose inside a chunk. Sending
            # every sentence on a new line makes V3 add an exaggerated pause.
            separator = " " if current else ""
            proposed = f"{current}{separator}{candidate}" if current else candidate
            if current and len(proposed) > max_chars:
                chunks.append(current.strip())
                current = candidate
            else:
                current = proposed
    if current.strip():
        chunks.append(current.strip())

    if len(chunks) <= 1:
        return chunks

    balanced: list[str] = []
    for chunk in chunks:
        if balanced and len(balanced[-1]) < min_chars and len(balanced[-1]) + 1 + len(chunk) <= max_chars:
            balanced[-1] = f"{balanced[-1]} {chunk}"
        else:
            balanced.append(chunk)
    return balanced


def request_audio_bytes(
    *,
    url: str,
    api_key: str,
    text: str,
    request_config: dict,
    chunk_number: int,
    chunk_count: int,
) -> bytes:
    payload: dict[str, object] = {
        "text": text,
        "model_id": request_config.get("model_id", DEFAULT_MODEL_ID),
        "voice_settings": request_config.get("voice_settings", DEFAULT_VOICE_SETTINGS),
    }
    if request_config.get("language_code"):
        payload["language_code"] = request_config["language_code"]

    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
            "xi-api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(f"ElevenLabs request failed on chunk {chunk_number}/{chunk_count}: HTTP {error.code}", file=sys.stderr)
        print(body, file=sys.stderr)
        raise


def concat_list_entry(path: Path) -> str:
    return "file '" + str(path).replace("'", "'\\''") + "'"


def merge_audio_parts(part_paths: list[Path], target_audio: Path) -> None:
    if len(part_paths) == 1:
        target_audio.write_bytes(part_paths[0].read_bytes())
        return

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        list_path = Path(handle.name)
        handle.write("\n".join(concat_list_entry(path.resolve()) for path in part_paths))
        handle.write("\n")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_path),
                "-c",
                "copy",
                str(target_audio),
            ],
            check=True,
        )
    finally:
        list_path.unlink(missing_ok=True)


def configured_bgm(config_path: Path, config: dict, args: argparse.Namespace) -> tuple[Path | None, float, float, float, float]:
    bgm_config = config.get("bgm") or {}
    bgm_source = args.bgm or bgm_config.get("source")
    gain_db = args.bgm_gain_db if args.bgm_gain_db is not None else bgm_config.get("gain_db", DEFAULT_BGM_GAIN_DB)
    outro_seconds = (
        args.bgm_outro_seconds
        if args.bgm_outro_seconds is not None
        else bgm_config.get("outro_seconds", DEFAULT_BGM_OUTRO_SECONDS)
    )
    outro_gain_db = (
        args.bgm_outro_gain_db
        if args.bgm_outro_gain_db is not None
        else bgm_config.get("outro_gain_db", DEFAULT_BGM_OUTRO_GAIN_DB)
    )
    fade_out = (
        args.bgm_fade_out_seconds
        if args.bgm_fade_out_seconds is not None
        else bgm_config.get("fade_out_seconds", DEFAULT_BGM_FADE_OUT_SECONDS)
    )
    if not bgm_source:
        return None, float(gain_db), float(outro_seconds), float(outro_gain_db), float(fade_out)

    bgm_audio = Path(bgm_source).expanduser()
    if not bgm_audio.is_absolute():
        base_path = Path.cwd() if args.bgm else config_path.parent
        bgm_audio = (base_path / bgm_audio).resolve()
    if not bgm_audio.exists():
        raise FileNotFoundError(f"missing BGM audio: {bgm_audio}")
    return bgm_audio, float(gain_db), float(outro_seconds), float(outro_gain_db), float(fade_out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path, help="Project directory, e.g. projects/2026-001-topic")
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional ElevenLabs request config. Defaults to project/02_audio/elevenlabs-request.json",
    )
    parser.add_argument("--replace", action="store_true", help="Replace an existing generated target audio file")
    parser.add_argument(
        "--postprocess",
        action="store_true",
        help="Run ingest_audio.py, align_captions.py, and analyze_audio_pacing.py after generation",
    )
    parser.add_argument("--language", default="ko", help="Language passed to align_captions.py when --postprocess is set")
    parser.add_argument("--chunk-min-chars", type=int, default=DEFAULT_MIN_CHARS, help="Preferred minimum text chunk size")
    parser.add_argument("--chunk-max-chars", type=int, default=DEFAULT_MAX_CHARS, help="Maximum text chunk size sent to ElevenLabs")
    parser.add_argument("--bgm", type=Path, help="Optional background music file mixed under the generated voice")
    parser.add_argument("--bgm-gain-db", type=float, help="BGM gain in dB. Defaults to -18dB when BGM is enabled")
    parser.add_argument("--bgm-outro-seconds", type=float, help="BGM-only outro tail after the voice ends. Defaults to 4 seconds")
    parser.add_argument(
        "--bgm-outro-gain-db",
        type=float,
        help="BGM gain in dB during the outro tail. Defaults to -14dB",
    )
    parser.add_argument(
        "--bgm-fade-out-seconds",
        type=float,
        help="BGM fade-out duration at the end of the outro. Defaults to 3 seconds",
    )
    args = parser.parse_args()

    project = args.project.resolve()
    repo = Path(__file__).resolve().parent.parent
    load_dotenv(repo / ".env", override=False)
    config_path = (args.config or project / "02_audio" / "elevenlabs-request.json").resolve()
    if not config_path.exists():
        parser.error(f"missing config: {config_path}")

    config = load_json(config_path)
    request_config = config.get("request", {})
    auth_config = config.get("auth", {})
    try:
        bgm_audio, bgm_gain_db, bgm_outro_seconds, bgm_outro_gain_db, bgm_fade_out_seconds = configured_bgm(
            config_path,
            config,
            args,
        )
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))
    voice_id = request_config.get("voice_id")
    if not voice_id:
        parser.error("missing request.voice_id in ElevenLabs config")

    env_var = auth_config.get("env_var", "ELEVENLABS_API_KEY")
    api_key = os.environ.get(env_var)
    if not api_key:
        parser.error(f"missing API key. Set {env_var} in your shell environment")

    script_source = (config_path.parent / config.get("script_source", "../01_script/narration.txt")).resolve()
    if not script_source.exists():
        parser.error(f"missing narration script: {script_source}")
    text = script_source.read_text(encoding="utf-8").strip()
    if not text:
        parser.error("narration script is empty")

    target_audio = (config_path.parent / config.get("target_audio", f"inbox/{project.name}-narration.mp3")).resolve()
    if target_audio.exists() and not args.replace:
        parser.error(f"target audio already exists: {target_audio}. Pass --replace to overwrite")
    target_audio.parent.mkdir(parents=True, exist_ok=True)

    output_format = request_config.get("output_format", "mp3_44100_128")
    query = urllib.parse.urlencode({"output_format": output_format})
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{urllib.parse.quote(voice_id)}?{query}"

    chunks = split_text_chunks(text, min_chars=args.chunk_min_chars, max_chars=args.chunk_max_chars)
    print(
        f"Generating with {request_config.get('model_id', DEFAULT_MODEL_ID)} "
        f"in {len(chunks)} chunk(s): {', '.join(str(len(chunk)) for chunk in chunks)} chars"
    )
    try:
        with tempfile.TemporaryDirectory(prefix="elevenlabs-parts-") as temp_dir:
            part_paths: list[Path] = []
            voice_only_audio = Path(temp_dir) / f"{target_audio.stem}-voice-only{target_audio.suffix}"
            for index, chunk in enumerate(chunks, start=1):
                print(f"  chunk {index}/{len(chunks)}: {len(chunk)} chars")
                audio = request_audio_bytes(
                    url=url,
                    api_key=api_key,
                    text=chunk,
                    request_config=request_config,
                    chunk_number=index,
                    chunk_count=len(chunks),
                )
                part_path = Path(temp_dir) / f"part-{index:03d}.mp3"
                part_path.write_bytes(audio)
                part_paths.append(part_path)
            merge_audio_parts(part_paths, voice_only_audio)
            if bgm_audio:
                preserved_voice = target_audio.with_name(f"{target_audio.stem}-voice-only{target_audio.suffix}")
                preserved_voice.write_bytes(voice_only_audio.read_bytes())
                mix_bgm_with_voice(
                    voice_audio=voice_only_audio,
                    bgm_audio=bgm_audio,
                    target_audio=target_audio,
                    gain_db=bgm_gain_db,
                    outro_seconds=bgm_outro_seconds,
                    outro_gain_db=bgm_outro_gain_db,
                    fade_out_seconds=bgm_fade_out_seconds,
                )
                print(
                    f"Mixed BGM: {bgm_audio} ({bgm_gain_db:.1f}dB under voice, "
                    f"{bgm_outro_seconds:.1f}s outro at {bgm_outro_gain_db:.1f}dB, "
                    f"{bgm_fade_out_seconds:.1f}s fade out)"
                )
                print(f"Preserved voice-only: {preserved_voice}")
            else:
                target_audio.write_bytes(voice_only_audio.read_bytes())
    except (subprocess.CalledProcessError, urllib.error.HTTPError, ValueError) as error:
        print(f"ElevenLabs generation failed: {error}", file=sys.stderr)
        return 1

    print(f"Generated: {target_audio}")
    if args.postprocess:
        subprocess.run(
            [sys.executable, str(repo / "scripts" / "ingest_audio.py"), str(project), str(target_audio), "--replace"],
            check=True,
        )
        subprocess.run(
            [sys.executable, str(repo / "scripts" / "align_captions.py"), str(project), "--language", args.language],
            check=True,
        )
        pacing = subprocess.run(
            [sys.executable, str(repo / "scripts" / "analyze_audio_pacing.py"), str(project), "--language", args.language],
            check=False,
        )
        if pacing.returncode:
            print("Pacing review is required before rendering.", file=sys.stderr)
            return pacing.returncode
    else:
        print("Next:")
        print(f"  python3 scripts/ingest_audio.py {project} {target_audio} --replace")
        print(f"  python3 scripts/align_captions.py {project} --language {args.language}")
        print(f"  python3 scripts/analyze_audio_pacing.py {project} --language {args.language}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
