#!/usr/bin/env python3
"""Create estimated SRT/VTT captions from the approved script and scene plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from align_captions import make_cues, timecode


def seconds_from_clock(value: str) -> float:
    value = value.strip()
    if ":" not in value:
        return float(value)
    parts = value.split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    hours, minutes, seconds = parts
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def scene_range(scene: dict) -> tuple[float, float]:
    if "start_seconds" in scene and "end_seconds" in scene:
        return float(scene["start_seconds"]), float(scene["end_seconds"])
    if "estimated_time" in scene:
        start, end = re.split(r"\s*-\s*", scene["estimated_time"], maxsplit=1)
        return seconds_from_clock(start), seconds_from_clock(end)
    raise ValueError(f"scene {scene.get('id', '<unknown>')} is missing timing")


def distribute_tokens(text: str, start: float, end: float) -> list:
    words = re.findall(r"\S+", text.strip())
    duration = max(0.1, end - start)
    total_chars = sum(max(1, len(word)) for word in words)
    cursor = start
    tokens = []
    for index, word in enumerate(words):
        share = max(1, len(word)) / max(1, total_chars)
        token_duration = duration * share
        token_start = cursor
        token_end = end if index == len(words) - 1 else min(end, cursor + token_duration)
        tokens.append(type("Token", (), {
            "text": word,
            "start": token_start,
            "end": max(token_start + 0.08, token_end),
        })())
        cursor = token_end
    return tokens


def write_outputs(cues: list[dict], sync_dir: Path) -> None:
    srt = []
    vtt = ["WEBVTT", ""]
    for number, cue in enumerate(cues, 1):
        srt.extend([
            str(number),
            f"{timecode(cue['start'])} --> {timecode(cue['end'])}",
            cue["text"],
            "",
        ])
        vtt.extend([
            f"{timecode(cue['start'], True)} --> {timecode(cue['end'], True)}",
            cue["text"],
            "",
        ])
    sync_dir.mkdir(parents=True, exist_ok=True)
    (sync_dir / "planned-captions.srt").write_text("\n".join(srt), encoding="utf-8")
    (sync_dir / "planned-captions.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (sync_dir / "planned-captions.json").write_text(
        json.dumps({"source": "scene-plan.json", "cues": cues}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--max-caption-chars", type=int, default=26)
    parser.add_argument("--max-caption-seconds", type=float, default=3.6)
    args = parser.parse_args()

    project = args.project.resolve()
    plan_path = project / "01_script" / "scene-plan.json"
    if not plan_path.exists():
        parser.error(f"missing scene plan: {plan_path}")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    cues = []
    for scene in plan.get("scenes", []):
        text = scene.get("caption_text") or scene.get("narration_text") or ""
        if not text.strip():
            continue
        start, end = scene_range(scene)
        tokens = distribute_tokens(text, start, end)
        cues.extend(make_cues(tokens, args.max_caption_chars, args.max_caption_seconds))

    if not cues:
        parser.error("scene plan produced no captions")
    write_outputs(cues, project / "03_sync")
    print(f"Planned captions: {project / '03_sync' / 'planned-captions.srt'}")
    print("After final audio is generated, run align_captions.py to create captions.srt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
