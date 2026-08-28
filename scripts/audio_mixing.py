#!/usr/bin/env python3
"""Shared ffmpeg helpers for measuring audio length and mixing BGM under narration."""

from __future__ import annotations

import subprocess
from pathlib import Path

DEFAULT_BGM_GAIN_DB = -18.0
DEFAULT_BGM_OUTRO_SECONDS = 4.0
DEFAULT_BGM_OUTRO_GAIN_DB = -14.0
DEFAULT_BGM_FADE_OUT_SECONDS = 3.0

MP3_CODEC_ARGS = ["-c:a", "libmp3lame", "-b:a", "192k"]
WAV_CODEC_ARGS = ["-c:a", "pcm_s16le"]

# The pipeline standard is 48 kHz stereo. BGM sources are often 44.1 kHz, and
# without pinning this, amix silently downsamples the 48 kHz voice master.
OUTPUT_SAMPLE_RATE = 48000


def audio_duration_seconds(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def mix_bgm_with_voice(
    *,
    voice_audio: Path,
    bgm_audio: Path,
    target_audio: Path,
    gain_db: float = DEFAULT_BGM_GAIN_DB,
    outro_seconds: float = DEFAULT_BGM_OUTRO_SECONDS,
    outro_gain_db: float = DEFAULT_BGM_OUTRO_GAIN_DB,
    fade_out_seconds: float = DEFAULT_BGM_FADE_OUT_SECONDS,
    output_codec_args: list = None,
) -> None:
    codec_args = list(output_codec_args) if output_codec_args else list(MP3_CODEC_ARGS)
    voice_duration = audio_duration_seconds(voice_audio)
    outro_duration = max(outro_seconds, 0.0)
    total_duration = voice_duration + outro_duration
    fade_duration = min(max(fade_out_seconds, 0.0), max(total_duration, 0.0))
    fade_start = max(total_duration - fade_duration, 0.0)
    bgm_main_volume = 10 ** (gain_db / 20)
    bgm_outro_volume = 10 ** (outro_gain_db / 20)
    filter_complex = (
        f"[0:a]atrim=0:{voice_duration:.3f},asetpts=PTS-STARTPTS,"
        f"apad=pad_dur={outro_duration:.3f},atrim=0:{total_duration:.3f}[voice];"
        f"[1:a]atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS,"
        f"volume='if(lt(t,{voice_duration:.3f}),{bgm_main_volume:.8f},{bgm_outro_volume:.8f})':eval=frame,"
        f"atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={fade_start:.3f}:d={fade_duration:.3f}[bgm];"
        "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        f"atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS[mixed]"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(voice_audio),
            "-stream_loop",
            "-1",
            "-i",
            str(bgm_audio),
            "-filter_complex",
            filter_complex,
            "-map",
            "[mixed]",
            "-t",
            f"{total_duration:.3f}",
            "-ar",
            str(OUTPUT_SAMPLE_RATE),
            "-ac",
            "2",
            *codec_args,
            str(target_audio),
        ],
        check=True,
    )
