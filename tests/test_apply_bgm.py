from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from apply_bgm import resolve_candidate, update_composition_duration
from audio_mixing import WAV_CODEC_ARGS, audio_duration_seconds, mix_bgm_with_voice


def make_tone(path: Path, seconds: float, frequency: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
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
def project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    make_tone(root / "02_audio" / "bgm" / "candidates" / "cand-01.mp3", 2.0, 440)
    make_tone(root / "02_audio" / "bgm" / "candidates" / "cand-02.mp3", 2.0, 330)
    return root


def test_resolve_candidate_by_id(project: Path):
    assert resolve_candidate(project, "cand-02").name == "cand-02.mp3"


def test_resolve_candidate_by_filename(project: Path):
    assert resolve_candidate(project, "cand-01.mp3").name == "cand-01.mp3"


def test_resolve_candidate_lists_available_on_miss(project: Path):
    with pytest.raises(SystemExit) as excinfo:
        resolve_candidate(project, "cand-99")
    assert "cand-01.mp3" in str(excinfo.value)


def test_update_composition_duration_rewrites_attribute(tmp_path: Path):
    index_html = tmp_path / "index.html"
    index_html.write_text(
        '<audio id="voice" data-start="0" data-duration="1153.031" '
        'src="assets/audio/voice.wav"></audio>',
        encoding="utf-8",
    )
    assert update_composition_duration(index_html, 1157.031) is True
    assert 'data-duration="1157.031"' in index_html.read_text(encoding="utf-8")


def test_update_composition_duration_reports_no_match(tmp_path: Path):
    index_html = tmp_path / "index.html"
    index_html.write_text("<div>no audio element</div>", encoding="utf-8")
    assert update_composition_duration(index_html, 10.0) is False


def test_wav_output_is_pcm(tmp_path: Path):
    voice = make_tone(tmp_path / "voice.wav", 3.0, 220)
    bgm = make_tone(tmp_path / "bgm.mp3", 1.0, 440)
    target = tmp_path / "voice-bgm.wav"
    mix_bgm_with_voice(
        voice_audio=voice,
        bgm_audio=bgm,
        target_audio=target,
        output_codec_args=WAV_CODEC_ARGS,
    )
    codec = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_name",
            "-of", "default=noprint_wrappers=1:nokey=1", str(target),
        ],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert codec == "pcm_s16le"
    assert audio_duration_seconds(target) == pytest.approx(7.0, abs=0.15)
