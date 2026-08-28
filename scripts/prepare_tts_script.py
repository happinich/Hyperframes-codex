#!/usr/bin/env python3
"""Create a spoken-form TTS script while keeping narration.txt unchanged."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from korean_tts_normalization import normalize_korean_tts_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    project = args.project.resolve()
    source = project / "01_script" / "narration.txt"
    target = project / "01_script" / "tts-narration.txt"
    report_path = project / "01_script" / "tts-normalization-report.json"
    if not source.exists():
        parser.error(f"missing approved narration: {source}")
    if target.exists() and not args.replace:
        parser.error(f"TTS script already exists: {target}. Pass --replace to overwrite")

    approved = source.read_text(encoding="utf-8")
    spoken = normalize_korean_tts_text(approved)
    remaining_digits = re.findall(r"\d", spoken)
    if remaining_digits:
        parser.error("digit normalization was incomplete")

    source_lines = approved.splitlines()
    spoken_lines = spoken.splitlines()
    changes = [
        {"line": index + 1, "display": display, "spoken": voice}
        for index, (display, voice) in enumerate(zip(source_lines, spoken_lines))
        if display != voice
    ]
    target.write_text(spoken, encoding="utf-8")
    report_path.write_text(
        json.dumps(
            {
                "display_source": "01_script/narration.txt",
                "tts_source": "01_script/tts-narration.txt",
                "changed_line_count": len(changes),
                "remaining_digit_count": 0,
                "changes": changes,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"TTS script: {target}")
    print(f"Changed lines: {len(changes)} | Remaining digits: 0")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
