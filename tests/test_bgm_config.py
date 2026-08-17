from __future__ import annotations

import pytest

from bgm_config import (
    MAX_MUSIC_LENGTH_MS,
    MIN_MUSIC_LENGTH_MS,
    build_prompt,
    load_bgm_settings,
    preview_window,
    resolve_style_preset,
    validate_music_length_ms,
)

SUCCESS_RULES = {
    "audio_rules": {
        "bgm": {
            "enabled": True,
            "voice_ducking_gain_db": -18,
            "outro_delay_seconds": 4,
            "fade_out_seconds": 3,
        }
    }
}

PRESETS = {
    "styles": {
        "dark_cinematic": {
            "base_prompt": "낮은 드론.",
            "variation_hints": ["현악 중심", "드론 중심"],
        }
    }
}


def test_load_bgm_settings_reads_success_rules():
    settings = load_bgm_settings(SUCCESS_RULES)
    assert settings.gain_db == -18.0
    assert settings.outro_seconds == 4.0
    assert settings.fade_out_seconds == 3.0


def test_load_bgm_settings_defaults_outro_gain_absent_from_rules():
    assert load_bgm_settings(SUCCESS_RULES).outro_gain_db == -14.0


def test_load_bgm_settings_handles_empty_config():
    settings = load_bgm_settings({})
    assert settings.outro_seconds == 4.0


def test_resolve_style_preset_returns_preset():
    assert resolve_style_preset(PRESETS, "dark_cinematic")["base_prompt"] == "낮은 드론."


def test_resolve_style_preset_lists_available_on_miss():
    with pytest.raises(KeyError) as excinfo:
        resolve_style_preset(PRESETS, "neon_tech")
    assert "dark_cinematic" in str(excinfo.value)


def test_build_prompt_joins_parts():
    assert build_prompt("기본.", "변주.", "내용.") == "기본. 변주. 내용."


def test_build_prompt_skips_empty_parts():
    assert build_prompt("기본.", "", "  ") == "기본."


def test_validate_music_length_ms_accepts_bounds():
    assert validate_music_length_ms(MIN_MUSIC_LENGTH_MS) == MIN_MUSIC_LENGTH_MS
    assert validate_music_length_ms(MAX_MUSIC_LENGTH_MS) == MAX_MUSIC_LENGTH_MS


def test_validate_music_length_ms_rejects_out_of_range():
    with pytest.raises(ValueError):
        validate_music_length_ms(MAX_MUSIC_LENGTH_MS + 1)
    with pytest.raises(ValueError):
        validate_music_length_ms(MIN_MUSIC_LENGTH_MS - 1)


def test_preview_window_uses_ratio():
    start, duration = preview_window(1000.0, 0.6, 30.0)
    assert start == pytest.approx(600.0)
    assert duration == pytest.approx(30.0)


def test_preview_window_clamps_to_end():
    start, duration = preview_window(100.0, 0.99, 30.0)
    assert start == pytest.approx(70.0)
    assert duration == pytest.approx(30.0)


def test_preview_window_handles_short_audio():
    start, duration = preview_window(10.0, 0.6, 30.0)
    assert start == 0.0
    assert duration == pytest.approx(10.0)
