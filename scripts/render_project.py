#!/usr/bin/env python3
"""Render an approved HyperFrames composition for a delivery format."""

from __future__ import annotations

import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path


DEFAULT_FPS = 60
MANUAL_PACING_APPROVAL_STATUS = "approved_after_manual_review"


def has_manual_pacing_approval(project: Path) -> bool:
    """Allow a flagged pacing report only after an explicit project review."""
    approval = project / "05_review" / "audio-review.json"
    if not approval.exists():
        return False
    try:
        data = json.loads(approval.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return data.get("status") == MANUAL_PACING_APPROVAL_STATUS


def project_fps(project: Path, delivery_format: str) -> int:
    """Use the project's recorded fps so completed projects keep their format."""
    plan = project / "01_script" / "scene-plan.json"
    if plan.exists():
        try:
            data = json.loads(plan.read_text(encoding="utf-8"))
            format_key = "master_format" if delivery_format == "youtube" else "shorts_format"
            recorded_fps = data.get(format_key, {}).get("fps")
            if recorded_fps is not None:
                fps = int(recorded_fps)
                if 1 <= fps <= 120:
                    return fps
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    existing = (
        project
        / "06_delivery"
        / delivery_format
        / f"{project.name}-{delivery_format}.mp4"
    )
    if existing.exists():
        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=avg_frame_rate",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(existing),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            fps = round(float(Fraction(probe.stdout.strip())))
            if probe.returncode == 0 and 1 <= fps <= 120:
                return fps
        except (ValueError, ZeroDivisionError):
            pass

    return DEFAULT_FPS


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--format", choices=("youtube", "shorts"), default="youtube")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    html_name = "index.html" if args.format == "youtube" else "variants/shorts.html"
    composition_dir = project / "04_composition"
    composition = composition_dir / html_name
    audio = project / "04_composition" / "assets" / "audio" / "voice.wav"
    report = project / "03_sync" / "sync_report.json"
    pacing_report = project / "03_sync" / "pacing_report.json"
    if not composition.exists():
        parser.error(f"missing composition: {composition}")
    if not audio.exists() and not args.dry_run:
        parser.error("missing normalized narration; run ingest_audio.py first")
    if not report.exists() and not args.dry_run:
        parser.error("missing sync report; run align_captions.py and review it first")
    if report.exists() and not args.dry_run:
        status = json.loads(report.read_text(encoding="utf-8")).get("status")
        if status == "alignment_review_required":
            parser.error("caption alignment requires review before rendering")
    if not pacing_report.exists() and not args.dry_run:
        parser.error("missing pacing report; run analyze_audio_pacing.py before rendering")
    if pacing_report.exists() and not args.dry_run:
        pacing_status = json.loads(pacing_report.read_text(encoding="utf-8")).get("status")
        if pacing_status == "pacing_review_required" and not has_manual_pacing_approval(project):
            parser.error("audio pacing requires review before rendering")

    delivery = project / "06_delivery" / args.format
    delivery.mkdir(parents=True, exist_ok=True)
    output = delivery / f"{project.name}-{args.format}.mp4"
    fps = project_fps(project, args.format)
    command = ["npx", "--no-install", "hyperframes", "render", str(composition_dir)]
    if args.format == "shorts":
        command.extend(["--composition", html_name])
    command.extend(["--output", str(output), "--fps", str(fps), "--strict"])
    if args.dry_run:
        print(" ".join(command))
        return 0
    subprocess.run(command, check=True)
    print(f"Rendered: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
