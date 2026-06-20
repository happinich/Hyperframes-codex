#!/usr/bin/env python3
"""Store an original narration file and create a normalized editing WAV."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SUPPORTED = {".mp3", ".m4a", ".mp4", ".wav"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("recording", type=Path)
    parser.add_argument("--replace", action="store_true", help="Replace an already ingested recording")
    args = parser.parse_args()

    project = args.project.resolve()
    recording = args.recording.expanduser().resolve()
    inbox = project / "02_audio" / "inbox"
    working = project / "02_audio" / "working"
    if not (project / "01_script" / "narration.txt").exists():
        parser.error(f"not a valid project directory: {project}")
    if not recording.exists() or recording.suffix.lower() not in SUPPORTED:
        parser.error("recording must be an existing mp3, m4a, mp4 or wav file")

    stored = inbox / f"{project.name}-narration{recording.suffix.lower()}"
    existing = [path for path in inbox.glob("*-narration.*") if path.resolve() != recording]
    if existing and not args.replace:
        parser.error("an audio source already exists; pass --replace to replace it")
    if args.replace:
        for old in existing:
            old.unlink()

    inbox.mkdir(parents=True, exist_ok=True)
    working.mkdir(parents=True, exist_ok=True)
    if recording != stored:
        shutil.copy2(recording, stored)
    normalized = working / "voice.wav"
    command = [
        "ffmpeg", "-y", "-i", str(stored), "-vn",
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(normalized),
    ]
    subprocess.run(command, check=True)
    render_audio = project / "04_composition" / "assets" / "audio" / "voice.wav"
    render_audio.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(normalized, render_audio)
    print(f"Original:   {stored}")
    print(f"Normalized: {normalized}")
    print(f"Render asset: {render_audio}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
