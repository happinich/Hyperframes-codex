#!/usr/bin/env python3
"""Create an independent narration video project from the repository template."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "project"
PROJECTS = ROOT / "projects"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".html", ".js"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id", help="Lowercase project identifier, e.g. 2026-001-topic")
    parser.add_argument("--title", required=True, help="Display title of the video")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", args.project_id):
        parser.error("project_id must contain only lowercase letters, digits, '-' or '_'")

    destination = PROJECTS / args.project_id
    if destination.exists():
        parser.error(f"project already exists: {destination}")

    shutil.copytree(TEMPLATE, destination)
    values = {
        "{{PROJECT_ID}}": args.project_id,
        "{{TITLE}}": args.title,
        "{{CREATED_DATE}}": dt.date.today().isoformat(),
    }
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            content = path.read_text(encoding="utf-8")
            for marker, replacement in values.items():
                content = content.replace(marker, replacement)
            path.write_text(content, encoding="utf-8")

    print(f"Created project: {destination}")
    print(f"Write narration: {destination / '01_script' / 'narration.txt'}")
    print(f"Plan scenes:     {destination / '01_script' / 'scene-plan.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
