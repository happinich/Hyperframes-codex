#!/usr/bin/env python3
"""Render an approved HyperFrames composition for a delivery format."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


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
        if pacing_status == "pacing_review_required":
            parser.error("audio pacing requires review before rendering")

    delivery = project / "06_delivery" / args.format
    delivery.mkdir(parents=True, exist_ok=True)
    output = delivery / f"{project.name}-{args.format}.mp4"
    command = ["npx", "--no-install", "hyperframes", "render", str(composition_dir)]
    if args.format == "shorts":
        command.extend(["--composition", html_name])
    command.extend(["--output", str(output), "--fps", "30", "--strict"])
    if args.dry_run:
        print(" ".join(command))
        return 0
    subprocess.run(command, check=True)
    print(f"Rendered: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
