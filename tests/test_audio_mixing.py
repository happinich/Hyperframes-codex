from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from audio_mixing import (
    WAV_CODEC_ARGS,
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


def stream_sample_rate(path: Path) -> int:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        check=True, capture_output=True, text=True,
    )
    return int(result.stdout.strip())


def test_mix_pins_output_to_48k_when_bgm_is_44k(tmp_path: Path):
    """A 44.1 kHz BGM must not drag the 48 kHz voice master down with it."""
    voice = tmp_path / "voice48.wav"
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", "sine=frequency=220:duration=4",
            "-ar", "48000", str(voice),
        ],
        check=True,
    )
    bgm = tmp_path / "bgm44.mp3"
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
            "-ar", "44100", str(bgm),
        ],
        check=True,
    )
    assert stream_sample_rate(voice) == 48000
    assert stream_sample_rate(bgm) == 44100

    target = tmp_path / "mixed.wav"
    mix_bgm_with_voice(
        voice_audio=voice, bgm_audio=bgm, target_audio=target,
        output_codec_args=WAV_CODEC_ARGS,
    )
    assert stream_sample_rate(target) == 48000
