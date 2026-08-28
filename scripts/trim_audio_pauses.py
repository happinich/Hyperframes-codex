#!/usr/bin/env python3
"""Trim excessive pauses in normalized narration audio."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


SILENCE_RE = re.compile(r"silence_(start|end): ([0-9.]+)(?: \\| silence_duration: ([0-9.]+))?")


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def detect_silences(path: Path, threshold: str, min_pause: float) -> list[tuple[float, float]]:
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(path),
            "-af",
            f"silencedetect=n={threshold}:d={min_pause}",
            "-f",
            "null",
            "-",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    silences: list[tuple[float, float]] = []
    pending_start: float | None = None
    for line in result.stderr.splitlines():
        match = SILENCE_RE.search(line)
        if not match:
            continue
        event, value = match.group(1), float(match.group(2))
        if event == "start":
            pending_start = value
        elif pending_start is not None and value > pending_start:
            silences.append((pending_start, value))
            pending_start = None
    return silences


def retained_intervals(
    duration: float,
    silences: list[tuple[float, float]],
    keep_pause: float,
) -> tuple[list[tuple[float, float]], float]:
    intervals: list[tuple[float, float]] = []
    cursor = 0.0
    removed = 0.0
    half_keep = keep_pause / 2.0
    for silence_start, silence_end in silences:
        cut_start = max(cursor, silence_start + half_keep)
        cut_end = min(duration, silence_end - half_keep)
        if cut_end <= cut_start:
            continue
        if cut_start > cursor:
            intervals.append((cursor, cut_start))
        removed += cut_end - cut_start
        cursor = cut_end
    if cursor < duration:
        intervals.append((cursor, duration))
    return intervals, removed


def trim_detected_pauses(source: Path, target: Path, threshold: str, min_pause: float, keep_pause: float) -> None:
    duration = audio_duration(source)
    silences = detect_silences(source, threshold, min_pause)
    intervals, removed = retained_intervals(duration, silences, keep_pause)
    if not intervals or removed <= 0:
        shutil.copy2(source, target)
        print("No qualifying internal pauses found; copied source unchanged.")
        return

    filters = []
    labels = []
    for index, (start, end) in enumerate(intervals):
        label = f"a{index}"
        filters.append(f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS[{label}]")
        labels.append(f"[{label}]")
    filters.append(f"{''.join(labels)}concat=n={len(labels)}:v=0:a=1[out]")
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[out]",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-c:a",
        "pcm_s16le",
        str(target),
    ]
    subprocess.run(command, check=True)
    print(f"Detected pauses: {len(silences)} | removed excess silence: {removed:.3f}s")


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
    if args.min_pause <= 0:
        parser.error("--min-pause must be positive")
    if args.keep_pause < 0 or args.keep_pause >= args.min_pause:
        parser.error("--keep-pause must satisfy 0 <= keep-pause < min-pause")

    trim_detected_pauses(source, out, args.threshold, args.min_pause, args.keep_pause)
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
