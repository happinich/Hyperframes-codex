#!/usr/bin/env python3
"""Create an independent narration video project from the repository template."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "project"
PROJECTS = ROOT / "projects"
VISUAL_STYLES = ROOT / "config" / "visual-styles.json"
PRODUCTION_PROFILES = ROOT / "config" / "production-profiles.json"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".html", ".js"}


def load_visual_styles() -> dict:
    return json.loads(VISUAL_STYLES.read_text(encoding="utf-8"))["styles"]


def print_visual_styles(styles: dict) -> None:
    for style_id, style in styles.items():
        uses = ", ".join(style["best_for"])
        print(f"{style_id:20} {style['label_ko']} — {style['mood']} ({uses})")


def load_production_profiles() -> tuple[str, dict]:
    data = json.loads(PRODUCTION_PROFILES.read_text(encoding="utf-8"))
    return data["default_profile_id"], data["profiles"]


def print_production_profiles(default_profile_id: str, profiles: dict) -> None:
    for profile_id, profile in profiles.items():
        marker = " (기본)" if profile_id == default_profile_id else ""
        print(f"{profile_id:28} {profile['label_ko']}{marker} — {profile['description']}")


def main() -> int:
    styles = load_visual_styles()
    default_profile_id, profiles = load_production_profiles()
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id", nargs="?", help="Lowercase project identifier, e.g. 2026-001-topic")
    parser.add_argument("--title", help="Display title of the video")
    parser.add_argument("--visual-style", choices=styles, help="Approved visual style for the composition")
    parser.add_argument("--production-profile", choices=profiles, help="Production grammar/version for the project")
    parser.add_argument("--list-visual-styles", action="store_true", help="Show available visual styles and exit")
    parser.add_argument("--list-production-profiles", action="store_true", help="Show available production profiles and exit")
    args = parser.parse_args()

    if args.list_visual_styles:
        print_visual_styles(styles)
        return 0
    if args.list_production_profiles:
        print_production_profiles(default_profile_id, profiles)
        return 0
    if not args.project_id or not args.title:
        parser.error("project_id and --title are required")
    if not args.visual_style:
        parser.error("visual style approval is required; run --list-visual-styles, then pass --visual-style")

    profile_id = args.production_profile
    if not profile_id:
        compatible_profiles = [
            candidate_id
            for candidate_id, candidate in profiles.items()
            if args.visual_style in candidate["compatible_visual_styles"]
        ]
        profile_id = compatible_profiles[0] if len(compatible_profiles) == 1 else default_profile_id
    selected_profile = profiles[profile_id]
    if args.visual_style not in selected_profile["compatible_visual_styles"]:
        compatible = ", ".join(selected_profile["compatible_visual_styles"])
        parser.error(
            f"visual style '{args.visual_style}' is not compatible with production profile "
            f"'{profile_id}'; choose one of: {compatible}"
        )

    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", args.project_id):
        parser.error("project_id must contain only lowercase letters, digits, '-' or '_'")

    destination = PROJECTS / args.project_id
    if destination.exists():
        parser.error(f"project already exists: {destination}")

    shutil.copytree(TEMPLATE, destination)
    selected_style = styles[args.visual_style]
    profile_template = ROOT / selected_profile["composition_template"]
    default_template = TEMPLATE / "04_composition" / "index.html"
    if profile_template.resolve() != default_template.resolve():
        shutil.copyfile(profile_template, destination / "04_composition" / "index.html")
    values = {
        "{{PROJECT_ID}}": args.project_id,
        "{{TITLE}}": args.title,
        "{{CREATED_DATE}}": dt.date.today().isoformat(),
        "{{VISUAL_STYLE_ID}}": args.visual_style,
        "{{VISUAL_STYLE_LABEL}}": selected_style["label_ko"],
        "{{VISUAL_STYLE_MOOD}}": selected_style["mood"],
        "{{VISUAL_STYLE_BACKGROUND}}": selected_style["background"],
        "{{VISUAL_STYLE_PALETTE}}": ", ".join(selected_style["palette"]),
        "{{VISUAL_STYLE_MOTION}}": selected_style["motion"],
        "{{PRODUCTION_PROFILE_ID}}": profile_id,
        "{{PRODUCTION_PROFILE_LABEL}}": selected_profile["label_ko"],
        "{{PRODUCTION_PROFILE_DESCRIPTION}}": selected_profile["description"],
        "{{PRODUCTION_PROFILE_LAYOUT}}": selected_profile["layout_language"],
        "{{PRODUCTION_PROFILE_MOTION}}": selected_profile["motion_density"],
        "{{PRODUCTION_PROFILE_SCRIPT_MODE}}": selected_profile["script_mode"],
        "{{PRODUCTION_PROFILE_OPENING_RULE}}": selected_profile["opening_rule"],
        "{{PRODUCTION_PROFILE_NARRATION_RULE}}": selected_profile["narration_rule"],
        "{{PRODUCTION_PROFILE_SOUND_RULE}}": selected_profile["sound_rule"],
        "{{PRODUCTION_PROFILE_CAPTION_RENDERER}}": selected_profile["captioned_output"]["renderer"],
        "{{PRODUCTION_PROFILE_CAPTION_SUFFIX}}": selected_profile["captioned_output"]["suffix"],
        "{{PRODUCTION_PROFILE_CAPTION_DEFAULT_ENABLED}}": str(
            selected_profile["captioned_output"].get("default_enabled", True)
        ).lower(),
        "{{PRODUCTION_PROFILE_TARGET_WPM}}": str(
            round(sum(selected_profile["target_wpm_range"]) / len(selected_profile["target_wpm_range"]))
        ),
        "{{PRODUCTION_PROFILE_TARGET_WPM_RANGE}}": "–".join(
            str(value) for value in selected_profile["target_wpm_range"]
        ),
    }
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            content = path.read_text(encoding="utf-8")
            for marker, replacement in values.items():
                content = content.replace(marker, replacement)
            path.write_text(content, encoding="utf-8")

    print(f"Created project: {destination}")
    print(f"Profile:        {selected_profile['label_ko']} ({profile_id})")
    print(f"Visual style:   {selected_style['label_ko']} ({args.visual_style})")
    print(f"Write narration: {destination / '01_script' / 'narration.txt'}")
    print(f"Plan scenes:     {destination / '01_script' / 'scene-plan.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
