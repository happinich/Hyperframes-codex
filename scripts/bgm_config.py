#!/usr/bin/env python3
"""Pure configuration helpers for BGM candidate generation and mixing."""

from __future__ import annotations

from dataclasses import dataclass

MIN_MUSIC_LENGTH_MS = 3000
MAX_MUSIC_LENGTH_MS = 600000

DEFAULT_GAIN_DB = -18.0
DEFAULT_OUTRO_SECONDS = 4.0
DEFAULT_OUTRO_GAIN_DB = -14.0
DEFAULT_FADE_OUT_SECONDS = 3.0


@dataclass(frozen=True)
class BgmSettings:
    gain_db: float
    outro_seconds: float
    outro_gain_db: float
    fade_out_seconds: float


def load_bgm_settings(success_rules: dict) -> BgmSettings:
    """Read audio_rules.bgm from success-rules.json content.

    outro_gain_db has no key in success-rules.json, so it falls back to the
    code default that generate_elevenlabs_audio.py has always used.
    """
    audio_rules = success_rules.get("audio_rules") or {}
    bgm = audio_rules.get("bgm") or {}
    return BgmSettings(
        gain_db=float(bgm.get("voice_ducking_gain_db", DEFAULT_GAIN_DB)),
        outro_seconds=float(bgm.get("outro_delay_seconds", DEFAULT_OUTRO_SECONDS)),
        outro_gain_db=float(bgm.get("outro_gain_db", DEFAULT_OUTRO_GAIN_DB)),
        fade_out_seconds=float(bgm.get("fade_out_seconds", DEFAULT_FADE_OUT_SECONDS)),
    )


def resolve_style_preset(presets: dict, style_id: str) -> dict:
    styles = presets.get("styles") or {}
    if style_id not in styles:
        available = ", ".join(sorted(styles)) or "(none)"
        raise KeyError(
            f"no BGM preset for visual style '{style_id}'. Available: {available}"
        )
    return styles[style_id]


def build_prompt(base_prompt: str, variation_hint: str, content_hint: str) -> str:
    parts = [base_prompt.strip(), variation_hint.strip(), content_hint.strip()]
    return " ".join(part for part in parts if part)


def validate_music_length_ms(value: int) -> int:
    if not MIN_MUSIC_LENGTH_MS <= value <= MAX_MUSIC_LENGTH_MS:
        raise ValueError(
            f"music_length_ms must be between {MIN_MUSIC_LENGTH_MS} and "
            f"{MAX_MUSIC_LENGTH_MS}, got {value}"
        )
    return value


def preview_window(
    total_seconds: float, start_ratio: float, preview_seconds: float
) -> tuple:
    """Return (start_seconds, duration_seconds) for the narration preview slice."""
    if total_seconds <= preview_seconds:
        return 0.0, total_seconds
    start = total_seconds * start_ratio
    if start + preview_seconds > total_seconds:
        start = total_seconds - preview_seconds
    return max(start, 0.0), preview_seconds
