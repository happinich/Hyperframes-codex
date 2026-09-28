"""Layer quiet procedural library ambience and causal foley over preserved voice+BGM."""
import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent
short = "--shorts" in sys.argv
name = "shorts" if short else "youtube"
total = json.loads((P / "01_script" / ("shorts-scene-plan.json" if short else "scene-plan.json")).read_text())["duration_seconds"]
src = P / "02_audio/working" / ("shorts-bgm.wav" if short else "voice-bgm.wav")
dst = P / "04_composition/assets/audio" / ("shorts-mix.wav" if short else "voice.wav")
if short and not src.exists():
    shutil.copyfile(dst, src)
sr = 24000
count = round(total * sr)
rng = np.random.default_rng(2301 if short else 2300)
noise = rng.normal(0, 1, count).astype(np.float32)
ambience = np.convolve(noise, np.ones(41, dtype=np.float32) / 41, "same").astype(np.float32) * 0.0016
ambience *= np.minimum(1, np.arange(count, dtype=np.float32) / (2 * sr))
ambience *= np.minimum(1, (count - np.arange(count, dtype=np.float32)) / (2.5 * sr))
foley = np.zeros(count, dtype=np.float32)
events = []

def event(at, kind, seconds=0.5, gain=0.006):
    n = round(sr * seconds)
    x = np.arange(n, dtype=np.float32) / sr
    envelope = np.minimum(x / 0.02, 1) * np.minimum((seconds - x) / 0.09, 1)
    raw = rng.normal(0, 1, n).astype(np.float32)
    if kind == "paper":
        signal = np.convolve(raw, np.ones(5) / 5, "same") * (0.45 + 0.55 * np.sin(2 * np.pi * 18 * x) ** 2)
    elif kind == "metal":
        signal = (np.sin(2 * np.pi * 520 * x) + 0.3 * np.sin(2 * np.pi * 930 * x) + 0.2 * raw) * np.exp(-11 * x)
    elif kind == "step":
        signal = (np.sin(2 * np.pi * 78 * x) + 0.14 * raw) * np.exp(-13 * x)
    else:
        raise ValueError(kind)
    start = round(at * sr)
    end = min(count, start + n)
    if start >= count:
        return
    foley[start:end] += (signal * envelope * gain)[:end - start]
    events.append({"at_seconds": round(at, 3), "kind": kind, "gain": gain})

if short:
    shots = json.loads((P / "01_script/shorts-scene-plan.json").read_text())["shots"]
    for index, kind in [(0, "metal"), (1, "paper"), (2, "paper"), (3, "paper"), (4, "metal"), (5, "paper")]:
        event(shots[index]["start"] + 0.25, kind, gain=0.004)
else:
    shots = json.loads((P / "04_composition/scene-data.json").read_text())["shots"]
    cues = {7: "metal", 9: "paper", 13: "paper", 17: "paper", 21: "paper",
            23: "step", 29: "metal", 31: "paper", 33: "step", 37: "step", 43: "paper"}
    for shot in shots:
        number = int(shot["visual"].split("-")[-1])
        if number in cues:
            event(shot["start"] + 0.35, cues[number])

def save(filename, data):
    target = P / "02_audio/working" / filename
    with wave.open(str(target), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(sr)
        stream.writeframes((np.clip(data, -1, 1) * 32767).astype("<i2").tobytes())
    return target

amb = save(name + "-library-ambience.wav", ambience)
fx = save(name + "-event-foley.wav", foley)
tmp_audio = dst.with_name(dst.stem + "-sound-design.wav")
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(amb), "-i", str(fx),
    "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:level=false:latency=true",
    "-ar", "48000", "-ac", "2", str(tmp_audio),
], check=True)
tmp_audio.replace(dst)
video = P / "06_delivery" / name / f"{P.name}-{name}.mp4"
tmp_video = video.with_name(video.stem + "-sound-design.mp4")
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(dst),
    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
    "-b:a", "192k", "-ar", "48000", "-t", f"{total:.6f}", "-movflags", "+faststart", str(tmp_video),
], check=True)
tmp_video.replace(video)
data = {
    "format": name,
    "voice_source_preserved": "02_audio/working/voice.wav" if not short else "04_composition/assets/audio/shorts-voice.wav",
    "bgm_source_preserved": str(src.relative_to(P)),
    "ambience": str(amb.relative_to(P)),
    "foley": str(fx.relative_to(P)),
    "events": events,
    "note": "Procedural foley deliberately quiet beneath narration; no TTS regenerated.",
}
(P / "02_audio" / (name + "-sound-design.json")).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print(f"{name}: {len(events)} quiet foley cues; original voice and BGM preserved")
