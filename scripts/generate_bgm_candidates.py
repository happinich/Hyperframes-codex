#!/usr/bin/env python3
"""Generate BGM candidates for a project and build the comparison page."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

from audio_mixing import audio_duration_seconds, mix_bgm_with_voice
from bgm_config import (
    build_prompt,
    load_bgm_settings,
    preview_window,
    resolve_style_preset,
    validate_music_length_ms,
)
from bgm_review_page import render_selection_page

REPO_ROOT = Path(__file__).resolve().parents[1]
SUCCESS_RULES_PATH = REPO_ROOT / "config" / "success-rules.json"
PRESETS_PATH = REPO_ROOT / "config" / "bgm-presets.json"
MUSIC_URL = "https://api.elevenlabs.io/v1/music"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def default_content_hint(brief_path: Path) -> str:
    if not brief_path.is_file():
        return ""
    for block in brief_path.read_text(encoding="utf-8").split("\n\n"):
        text = " ".join(
            line.strip()
            for line in block.strip().splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
        if text:
            return text
    return ""


def build_candidate_specs(preset: dict, count: int, content_hint: str) -> list:
    hints = preset.get("variation_hints") or []
    if count > len(hints):
        raise ValueError(
            f"requested {count} candidates but the preset has only {len(hints)} "
            "variation_hints"
        )
    specs = []
    for index in range(count):
        specs.append(
            {
                "id": f"cand-{index + 1:02d}",
                "prompt": build_prompt(
                    preset.get("base_prompt", ""), hints[index], content_hint
                ),
            }
        )
    return specs


def request_music_bytes(
    *, api_key: str, prompt: str, length_ms: int, output_format: str
) -> bytes:
    query = urllib.parse.urlencode({"output_format": output_format})
    payload = json.dumps(
        {"prompt": prompt, "music_length_ms": length_ms}, ensure_ascii=False
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{MUSIC_URL}?{query}",
        data=payload,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return response.read()


def slice_narration(voice: Path, target: Path, start: float, duration: float) -> None:
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{start:.3f}", "-t", f"{duration:.3f}", "-i", str(voice),
            str(target),
        ],
        check=True,
    )


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    parser = argparse.ArgumentParser(
        description="Generate BGM candidates and a comparison page for a project"
    )
    parser.add_argument("project", type=Path, help="Project directory")
    parser.add_argument("--count", type=int)
    parser.add_argument("--length-ms", type=int)
    parser.add_argument("--content-hint", default=None)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        parser.error("missing API key. Set ELEVENLABS_API_KEY in your shell environment")

    project = args.project.resolve()
    profile_path = project / "04_composition" / "profile.json"
    if not profile_path.is_file():
        parser.error(f"missing composition profile: {profile_path}")
    style_id = load_json(profile_path).get("visual_style_id")

    presets = load_json(PRESETS_PATH)
    try:
        preset = resolve_style_preset(presets, style_id)
    except KeyError as error:
        parser.error(str(error))

    defaults = presets.get("defaults") or {}
    count = args.count or defaults.get("candidate_count", 4)
    length_ms = validate_music_length_ms(
        args.length_ms or defaults.get("candidate_length_ms", 40000)
    )
    output_format = defaults.get("output_format", "mp3_44100_128")

    content_hint = args.content_hint
    if content_hint is None:
        content_hint = default_content_hint(project / "00_brief" / "brief.md")

    try:
        specs = build_candidate_specs(preset, count, content_hint)
    except ValueError as error:
        parser.error(str(error))

    bgm_dir = project / "02_audio" / "bgm"
    candidates_dir = bgm_dir / "candidates"
    previews_dir = bgm_dir / "previews"
    if candidates_dir.exists() and any(candidates_dir.glob("*.mp3")) and not args.replace:
        parser.error(f"candidates already exist: {candidates_dir}. Pass --replace")
    candidates_dir.mkdir(parents=True, exist_ok=True)
    previews_dir.mkdir(parents=True, exist_ok=True)

    voice = project / "02_audio" / "working" / "voice.wav"
    settings = load_bgm_settings(load_json(SUCCESS_RULES_PATH))
    narration_slice = None
    if voice.is_file():
        start, duration = preview_window(
            audio_duration_seconds(voice),
            defaults.get("preview_start_ratio", 0.6),
            defaults.get("preview_seconds", 30),
        )
        narration_slice = previews_dir / "narration-slice.wav"
        slice_narration(voice, narration_slice, start, duration)
    else:
        print(f"WARNING: no voice track at {voice}. Skipping narration mix previews.")

    print(f"Style      : {style_id}")
    print(f"Candidates : {count} x {length_ms}ms")

    rendered = []
    failures = 0
    for index, spec in enumerate(specs, start=1):
        print(f"  {spec['id']}: generating...")
        try:
            audio = request_music_bytes(
                api_key=api_key,
                prompt=spec["prompt"],
                length_ms=length_ms,
                output_format=output_format,
            )
        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            failures += 1
            print(f"  {spec['id']}: FAILED ({error})")
            continue

        candidate_path = candidates_dir / f"{spec['id']}.mp3"
        candidate_path.write_bytes(audio)

        preview_href = ""
        if narration_slice is not None:
            preview_path = previews_dir / f"mix-{index:02d}.mp3"
            mix_bgm_with_voice(
                voice_audio=narration_slice,
                bgm_audio=candidate_path,
                target_audio=preview_path,
                gain_db=settings.gain_db,
                outro_seconds=0.0,
                outro_gain_db=settings.outro_gain_db,
                fade_out_seconds=settings.fade_out_seconds,
            )
            preview_href = f"../02_audio/bgm/previews/{preview_path.name}"

        rendered.append(
            {
                "id": spec["id"],
                "prompt": spec["prompt"],
                "bgm_href": f"../02_audio/bgm/candidates/{candidate_path.name}",
                "preview_href": preview_href,
            }
        )

    if not rendered:
        print(f"All {failures} candidate(s) failed.")
        return 1

    (bgm_dir / "candidates.json").write_text(
        json.dumps(
            {
                "style_id": style_id,
                "length_ms": length_ms,
                "output_format": output_format,
                "content_hint": content_hint,
                "candidates": rendered,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    review_page = project / "05_review" / "bgm-selection.html"
    review_page.parent.mkdir(parents=True, exist_ok=True)
    review_page.write_text(
        render_selection_page(project.name, rendered), encoding="utf-8"
    )

    print()
    print(f"Generated  : {len(rendered)} candidate(s), {failures} failed")
    print(f"Review page: {review_page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
