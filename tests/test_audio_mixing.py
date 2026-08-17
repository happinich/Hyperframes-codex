from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from audio_mixing import (
    DEFAULT_BGM_FADE_OUT_SECONDS,
    DEFAULT_BGM_GAIN_DB,
    DEFAULT_BGM_OUTRO_SECONDS,
    audio_duration_seconds,
    mix_bgm_with_voice,
)


def make_tone(path: Path, seconds: float, frequency: int) -> Path:
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", f"sine=frequency={frequency}:duration={seconds}",
            str(path),
        ],
        check=True,
    )
    return path


@pytest.fixture
def voice(tmp_path: Path) -> Path:
    return make_tone(tmp_path / "voice.wav", 5.0, 220)


@pytest.fixture
def bgm(tmp_path: Path) -> Path:
    return make_tone(tmp_path / "bgm.mp3", 2.0, 440)


def test_defaults_match_success_rules():
    assert DEFAULT_BGM_GAIN_DB == -18.0
    assert DEFAULT_BGM_OUTRO_SECONDS == 4.0
    assert DEFAULT_BGM_FADE_OUT_SECONDS == 3.0


def test_audio_duration_seconds_reads_actual_length(voice: Path):
    assert audio_duration_seconds(voice) == pytest.approx(5.0, abs=0.05)


def test_mix_appends_outro_tail(voice: Path, bgm: Path, tmp_path: Path):
    target = tmp_path / "mixed.mp3"
    mix_bgm_with_voice(
        voice_audio=voice, bgm_audio=bgm, target_audio=target, outro_seconds=4.0
    )
    assert audio_duration_seconds(target) == pytest.approx(9.0, abs=0.15)


def test_mix_loops_bgm_shorter_than_voice(voice: Path, bgm: Path, tmp_path: Path):
    target = tmp_path / "looped.mp3"
    mix_bgm_with_voice(voice_audio=voice, bgm_audio=bgm, target_audio=target)
    assert audio_duration_seconds(target) > audio_duration_seconds(bgm)


def test_mix_does_not_modify_voice(voice: Path, bgm: Path, tmp_path: Path):
    before = voice.read_bytes()
    mix_bgm_with_voice(
        voice_audio=voice, bgm_audio=bgm, target_audio=tmp_path / "out.mp3"
    )
    assert voice.read_bytes() == before
