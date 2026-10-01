"""Create low level original apartment ambience and event foley, then mix stems."""
from __future__ import annotations

import json
import subprocess
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent
A = P / "02_audio/working"
R = P / "04_composition/assets/audio"
SAMPLE_RATE = 48_000
BASE = A / "voice-bgm.wav"
VOICE = A / "voice.wav"


def duration(path: Path) -> float:
    result = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], text=True)
    return float(result)


total = duration(BASE)
if abs(total - duration(VOICE) - 4) > .05:
    raise SystemExit("BGM outro duration changed")

# The fluorescent room tone is a quiet generated source, not an external recording.
ambience = A / "room-ambience.wav"
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
    "-i", f"anoisesrc=d={total:.6f}:c=brown:a=0.008:s={SAMPLE_RATE}",
    "-af", f"highpass=f=60,lowpass=f=480,afade=t=in:st=0:d=1,afade=t=out:st={total-3:.3f}:d=3",
    "-ar", str(SAMPLE_RATE), "-ac", "2", str(ambience),
], check=True)

words = json.loads((P / "03_sync/captions.words.json").read_text(encoding="utf-8"))["words"]
beeps = [float(w["start"]) for w in words if "삑" in w["text"]]
if len(beeps) != 9:
    raise SystemExit(f"Expected four plus five doorlock syllables, found {len(beeps)}")

foley = np.zeros(round(total * SAMPLE_RATE), dtype=np.float32)
rng = np.random.default_rng(2026024)


def place(start: float, signal: np.ndarray) -> None:
    at = round(start * SAMPLE_RATE)
    end = min(len(foley), at + len(signal))
    if at < 0 or at >= len(foley):
        raise ValueError(f"Foley outside project: {start}")
    foley[at:end] += signal[:end-at]


for start in beeps:
    t = np.arange(round(.17 * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    envelope = np.sin(np.pi * np.minimum(t / .17, 1)) ** 1.3
    tone = .044 * envelope * (np.sin(2*np.pi*1180*t) + .15*np.sin(2*np.pi*2360*t))
    place(start, tone.astype(np.float32))

for start in (43.8, 178.6, 248.2):
    t = np.arange(round(.32 * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    noise = rng.standard_normal(len(t)).astype(np.float32)
    envelope = (np.sin(np.pi*t/.32)**2).astype(np.float32)
    place(start, .006 * noise * envelope)

for start in (228.9, 272.3):
    t = np.arange(round(.07 * SAMPLE_RATE), dtype=np.float32) / SAMPLE_RATE
    place(start, (.025 * rng.standard_normal(len(t)) * np.exp(-t*85)).astype(np.float32))

foley_path = A / "event-foley.wav"
with wave.open(str(foley_path), "wb") as output:
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(SAMPLE_RATE)
    output.writeframes((np.clip(foley, -1, 1)*32767).astype("<i2").tobytes())

final = A / "voice-bgm-soundscape.wav"
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-i", str(BASE), "-i", str(ambience), "-i", str(foley_path),
    "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.96[m]",
    "-map", "[m]", "-ar", str(SAMPLE_RATE), "-ac", "2", str(final),
], check=True)
R.joinpath("voice.wav").write_bytes(final.read_bytes())
print(f"Generated separate room ambience and event foley stems; final mix {duration(final):.3f}s")
