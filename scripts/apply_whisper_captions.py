#!/usr/bin/env python3
"""Rewrite external subtitle files from validated Whisper-aligned cues."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from align_captions import update_compositions, write_captions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    sync = project / "03_sync"
    report = json.loads((sync / "sync_report.json").read_text(encoding="utf-8"))
    if report.get("status") != "ready_for_review":
        parser.error("Whisper alignment has not passed review threshold")
    payload = json.loads((sync / "captions.words.json").read_text(encoding="utf-8"))
    cues = payload["cues"]
    write_captions(cues, sync)
    update_compositions(project, cues, float(payload["duration"]), payload)
    print(f"Rewrote {len(cues)} Whisper-aligned external subtitle cues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
