#!/usr/bin/env python3
"""Analyze narration pacing after Whisper alignment."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


SILENCE_RE = re.compile(r"silence_(start|end): ([0-9.]+)(?: \\| silence_duration: ([0-9.]+))?")


def run_silencedetect(audio: Path, threshold: str, min_duration: float) -> list[dict]:
    command = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        str(audio),
        "-af",
        f"silencedetect=n={threshold}:d={min_duration}",
        "-f",
        "null",
        "-",
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    events: list[dict] = []
    pending_start: float | None = None
    for line in result.stderr.splitlines():
        match = SILENCE_RE.search(line)
        if not match:
            continue
        kind, value, duration = match.groups()
        if kind == "start":
            pending_start = float(value)
        elif kind == "end" and pending_start is not None:
            end = float(value)
            events.append(
                {
                    "start": round(pending_start, 3),
                    "end": round(end, 3),
                    "duration": round(float(duration or (end - pending_start)), 3),
                }
            )
            pending_start = None
    return events


def analyze_windows(words: list[dict], duration: float, window: float, step: float) -> list[dict]:
    windows = []
    t = 0.0
    while t < duration:
        count = sum(1 for word in words if t <= float(word["start"]) < t + window)
        windows.append(
            {
                "start": round(t, 3),
                "end": round(min(duration, t + window), 3),
                "word_count": count,
                "wpm": round(count * 60 / window, 1),
            }
        )
        t += step
    return windows


def word_gaps(words: list[dict], threshold: float) -> list[dict]:
    gaps = []
    previous = None
    for word in words:
        if previous is not None:
            gap = float(word["start"]) - float(previous["end"])
            if gap >= threshold:
                gaps.append(
                    {
                        "start": round(float(previous["end"]), 3),
                        "end": round(float(word["start"]), 3),
                        "duration": round(gap, 3),
                        "before": previous["text"],
                        "after": word["text"],
                    }
                )
        previous = word
    return gaps


def status_for(report: dict, max_long_silences: int, max_gap_count: int, max_slow_windows: int) -> str:
    if report["long_silence_count"] > max_long_silences:
        return "pacing_review_required"
    if report["long_word_gap_count"] > max_gap_count:
        return "pacing_review_required"
    if report["slow_window_count"] > max_slow_windows:
        return "pacing_review_required"
    return "ready_for_review"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--language", default="ko")
    parser.add_argument("--silence-threshold", default="-42dB")
    parser.add_argument("--silence-duration", type=float, default=0.8)
    parser.add_argument("--gap-threshold", type=float, default=0.8)
    parser.add_argument("--window", type=float, default=15.0)
    parser.add_argument("--step", type=float, default=5.0)
    parser.add_argument("--slow-wpm", type=float, default=58.0)
    parser.add_argument("--fast-wpm", type=float, default=135.0)
    parser.add_argument("--max-long-silences", type=int, default=3)
    parser.add_argument("--max-gap-count", type=int, default=6)
    parser.add_argument("--max-slow-windows", type=int, default=4)
    args = parser.parse_args()

    project = args.project.resolve()
    words_path = project / "03_sync" / "captions.words.json"
    audio = project / "04_composition" / "assets" / "audio" / "voice.wav"
    if not words_path.exists():
        parser.error("missing captions.words.json; run align_captions.py first")
    if not audio.exists():
        parser.error("missing render audio; run ingest_audio.py first")

    payload = json.loads(words_path.read_text(encoding="utf-8"))
    words = payload.get("words", [])
    duration = float(payload.get("duration", 0))
    windows = analyze_windows(words, duration, args.window, args.step)
    slow_windows = [item for item in windows if item["wpm"] < args.slow_wpm and item["word_count"] > 1]
    fast_windows = [item for item in windows if item["wpm"] > args.fast_wpm]
    gaps = word_gaps(words, args.gap_threshold)
    silences = run_silencedetect(audio, args.silence_threshold, args.silence_duration)

    report = {
        "status": "ready_for_review",
        "duration": round(duration, 3),
        "word_count": len(words),
        "average_wpm": round(len(words) * 60 / duration, 1) if duration else 0,
        "window_seconds": args.window,
        "step_seconds": args.step,
        "slow_wpm_threshold": args.slow_wpm,
        "fast_wpm_threshold": args.fast_wpm,
        "long_silence_threshold_seconds": args.silence_duration,
        "long_silence_count": len(silences),
        "long_silences": silences,
        "long_word_gap_threshold_seconds": args.gap_threshold,
        "long_word_gap_count": len(gaps),
        "long_word_gaps": gaps,
        "slow_window_count": len(slow_windows),
        "slow_windows": slow_windows,
        "fast_window_count": len(fast_windows),
        "fast_windows": fast_windows,
        "recommendations": [],
    }
    if silences:
        report["recommendations"].append("Regenerate affected sections or trim long silences before rendering.")
    if slow_windows:
        report["recommendations"].append("Use eleven_v3 with 1,000-1,300 character sentence chunks and review voice settings before rendering.")
    if fast_windows:
        report["recommendations"].append("Review fast windows for rushed pronunciation before accepting.")
    report["status"] = status_for(report, args.max_long_silences, args.max_gap_count, args.max_slow_windows)

    out = project / "03_sync" / "pacing_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Pacing report: {out}")
    print(
        f"Status: {report['status']} | avg {report['average_wpm']} wpm | "
        f"long silences {report['long_silence_count']} | long gaps {report['long_word_gap_count']} | "
        f"slow windows {report['slow_window_count']}"
    )
    return 0 if report["status"] == "ready_for_review" else 2


if __name__ == "__main__":
    raise SystemExit(main())
