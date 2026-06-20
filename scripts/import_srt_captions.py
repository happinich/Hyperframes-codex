#!/usr/bin/env python3
"""Import supplied external SRT captions only when their spoken text matches the narration."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import wave
from pathlib import Path

from align_captions import normalized, update_compositions


TIME_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(?P<end>\d{2}:\d{2}:\d{2},\d{3})"
)


def seconds(value: str) -> float:
    hours, minutes, remainder = value.split(":")
    secs, millis = remainder.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(secs) + int(millis) / 1000


def parse_srt(path: Path) -> list[dict]:
    cues = []
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing_index = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            continue
        match = TIME_RE.fullmatch(lines[timing_index])
        if not match:
            raise ValueError(f"unsupported SRT timing line: {lines[timing_index]}")
        cues.append({
            "start": seconds(match.group("start")),
            "end": seconds(match.group("end")),
            "text": " ".join(lines[timing_index + 1:]),
        })
    if not cues:
        raise ValueError("SRT contains no captions")
    return cues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("srt", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    source = args.srt.expanduser().resolve()
    narration = (project / "01_script" / "narration.txt").read_text(encoding="utf-8").strip()
    cues = parse_srt(source)
    provided_text = " ".join(cue["text"] for cue in cues)
    if normalized(provided_text) != normalized(narration):
        raise SystemExit("provided SRT text does not match narration.txt; review before importing")

    sync = project / "03_sync"
    sync.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, sync / "captions.srt")
    vtt_lines = ["WEBVTT", ""]
    for cue in cues:
        start = format_vtt(cue["start"])
        end = format_vtt(cue["end"])
        vtt_lines.extend([f"{start} --> {end}", cue["text"], ""])
    (sync / "captions.vtt").write_text("\n".join(vtt_lines), encoding="utf-8")
    caption_duration = cues[-1]["end"]
    audio_path = project / "02_audio" / "working" / "voice.wav"
    with wave.open(str(audio_path), "rb") as audio:
        media_duration = audio.getnframes() / audio.getframerate()
    payload = {"duration": media_duration, "cues": cues, "words": [], "source": "provided_srt_verified_by_whisper"}
    (sync / "provided_captions.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    update_compositions(project, cues, media_duration, payload)
    print(f"Imported {len(cues)} cues through {caption_duration:.3f}s; exact text match confirmed.")
    return 0


def format_vtt(value: float) -> str:
    total_ms = round(value * 1000)
    hours, total_ms = divmod(total_ms, 3_600_000)
    minutes, total_ms = divmod(total_ms, 60_000)
    secs, millis = divmod(total_ms, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{millis:03}"


if __name__ == "__main__":
    raise SystemExit(main())
