#!/usr/bin/env python3
"""Mix an approved BGM candidate under an existing narration voice track.

This never calls the ElevenLabs TTS API, so an approved voice take and its
caption timings stay intact.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

from audio_mixing import WAV_CODEC_ARGS, audio_duration_seconds, mix_bgm_with_voice
from bgm_config import load_bgm_settings

REPO_ROOT = Path(__file__).resolve().parents[1]
SUCCESS_RULES_PATH = REPO_ROOT / "config" / "success-rules.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_candidate(project: Path, candidate: str) -> Path:
    candidates_dir = project / "02_audio" / "bgm" / "candidates"
    direct = Path(candidate)
    if direct.is_file():
        return direct
    for suffix in ("", ".mp3"):
        guess = candidates_dir / f"{candidate}{suffix}"
        if guess.is_file():
            return guess
    available = (
        sorted(p.name for p in candidates_dir.glob("*.mp3"))
        if candidates_dir.is_dir()
        else []
    )
    raise SystemExit(
        f"candidate not found: {candidate}. "
        f"Available: {', '.join(available) or '(none)'}"
    )


def update_composition_duration(index_html: Path, total_seconds: float) -> bool:
    text = index_html.read_text(encoding="utf-8")
    pattern = re.compile(r'(<audio[^>]*id="voice"[^>]*data-duration=")([0-9.]+)(")')
    updated, count = pattern.subn(rf"\g<1>{total_seconds:.3f}\g<3>", text)
    if count:
        index_html.write_text(updated, encoding="utf-8")
    return bool(count)


def update_request_config(project: Path, bgm_path: Path) -> None:
    config_path = project / "02_audio" / "elevenlabs-request.json"
    if not config_path.is_file():
        return
    config = load_json(config_path)
    bgm_block = config.get("bgm") or {}
    bgm_block["source"] = os.path.relpath(bgm_path, config_path.parent)
    config["bgm"] = bgm_block
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mix an approved BGM candidate under an existing voice track"
    )
    parser.add_argument("project", type=Path, help="Project directory")
    parser.add_argument(
        "--candidate", required=True, help="Candidate id (cand-02) or path"
    )
    parser.add_argument("--outro-seconds", type=float)
    parser.add_argument("--gain-db", type=float)
    parser.add_argument(
        "--dry-run", action="store_true", help="Report the plan without writing files"
    )
    args = parser.parse_args()

    project = args.project.resolve()
    voice = project / "02_audio" / "working" / "voice.wav"
    if not voice.is_file():
        parser.error(
            f"missing voice track: {voice}. "
            "Run generate_elevenlabs_audio.py and ingest_audio.py first"
        )

    settings = load_bgm_settings(load_json(SUCCESS_RULES_PATH))
    gain_db = args.gain_db if args.gain_db is not None else settings.gain_db
    outro_seconds = (
        args.outro_seconds if args.outro_seconds is not None else settings.outro_seconds
    )

    bgm_path = resolve_candidate(project, args.candidate)
    voice_seconds = audio_duration_seconds(voice)
    total_seconds = voice_seconds + outro_seconds

    print(f"Voice      : {voice} ({voice_seconds:.3f}s)")
    print(f"BGM        : {bgm_path}")
    print(f"Gain       : {gain_db:.1f}dB under voice")
    print(f"Outro      : {outro_seconds:.1f}s at {settings.outro_gain_db:.1f}dB")
    print(f"Fade out   : {settings.fade_out_seconds:.1f}s")
    print(f"New length : {total_seconds:.3f}s")

    if args.dry_run:
        print("Dry run. No files written.")
        return 0

    mixed = project / "02_audio" / "working" / "voice-bgm.wav"
    mix_bgm_with_voice(
        voice_audio=voice,
        bgm_audio=bgm_path,
        target_audio=mixed,
        gain_db=gain_db,
        outro_seconds=outro_seconds,
        outro_gain_db=settings.outro_gain_db,
        fade_out_seconds=settings.fade_out_seconds,
        output_codec_args=WAV_CODEC_ARGS,
    )
    print(f"Wrote      : {mixed}")

    render_audio = project / "04_composition" / "assets" / "audio" / "voice.wav"
    render_audio.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mixed, render_audio)
    print(f"Replaced   : {render_audio}")
    print(f"Preserved  : {voice} (voice-only master, untouched)")

    update_request_config(project, bgm_path)

    index_html = project / "04_composition" / "index.html"
    if index_html.is_file():
        if update_composition_duration(index_html, total_seconds):
            print(f"Updated    : {index_html} data-duration={total_seconds:.3f}")
        else:
            print(f"WARNING    : no voice audio element found in {index_html}")

    print()
    print(
        f"NEXT: extend the composition outro by {outro_seconds:.1f}s "
        "and re-render. Captions end before the voice, so they are unaffected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
