#!/usr/bin/env python3
"""Trim excessive pauses in normalized narration audio."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--threshold", default="-42dB")
    parser.add_argument("--min-pause", type=float, default=0.7, help="Only pauses longer than this are shortened")
    parser.add_argument("--keep-pause", type=float, default=0.45, help="Silence left in place after trimming")
    parser.add_argument("--replace", action="store_true", help="Replace working/render voice.wav with trimmed audio")
    args = parser.parse_args()

    project = args.project.resolve()
    source = project / "02_audio" / "working" / "voice.wav"
    if not source.exists():
        parser.error("missing normalized audio; run ingest_audio.py first")

    out = project / "02_audio" / "working" / "voice-paced.wav"
    backup = project / "02_audio" / "working" / "voice-before-pacing-trim.wav"
    filter_expr = (
        "silenceremove="
        "start_periods=0:"
        "stop_periods=-1:"
        f"stop_duration={args.min_pause}:"
        f"stop_threshold={args.threshold}:"
        f"stop_silence={args.keep_pause}:"
        "detection=rms"
    )
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-af",
        filter_expr,
        "-ar",
        "48000",
        "-ac",
        "2",
        "-c:a",
        "pcm_s16le",
        str(out),
    ]
    subprocess.run(command, check=True)
    print(f"Trimmed: {out}")

    if args.replace:
        if not backup.exists():
            shutil.copy2(source, backup)
        shutil.copy2(out, source)
        render_audio = project / "04_composition" / "assets" / "audio" / "voice.wav"
        render_audio.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, render_audio)
        print(f"Backup: {backup}")
        print(f"Replaced: {source}")
        print(f"Render asset: {render_audio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
