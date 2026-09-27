"""Add quiet reservoir ambience and event foley without regenerating narration."""
import json
import subprocess
import wave
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent
plan = json.loads((P/'01_script/scene-plan.json').read_text())
duration = plan['duration_seconds']
sr = 24000
rng = np.random.default_rng(22)
count = round(duration*sr)
t = np.arange(count, dtype=np.float32)/sr
noise = rng.normal(0, 1, count).astype(np.float32)
water = np.convolve(noise, np.ones(31)/31, 'same').astype(np.float32)
room = water*.0015*(.7+.3*np.sin(2*np.pi*.19*t))
room *= np.minimum(t/2, 1)*np.clip((duration-t)/3, 0, 1)
foley = np.zeros(count, dtype=np.float32)
events = []

def event(at, kind, seconds=.5, gain=.007):
    n = round(sr*seconds)
    x = np.arange(n)/sr
    env = np.minimum(x/.025, 1)*np.minimum((seconds-x)/.09, 1)
    if kind == 'water':
        sig = np.convolve(rng.normal(0, 1, n), np.ones(11)/11, 'same')*np.exp(-2*x)
    elif kind == 'rubber':
        sig = (np.sin(2*np.pi*95*x)+.15*np.sin(2*np.pi*211*x))*np.exp(-11*x)
    elif kind == 'cloth':
        sig = np.convolve(rng.normal(0, 1, n), np.ones(5)/5, 'same')*np.exp(-3*x)
    else:
        sig = (np.sin(2*np.pi*170*x)+.25*np.sin(2*np.pi*317*x))*np.exp(-18*x)
    start = round(at*sr)
    end = min(count, start+n)
    foley[start:end] += (sig*env*gain)[:end-start]
    events.append({'start':round(at, 3), 'kind':kind, 'duration':seconds, 'gain':gain})

shots = json.loads((P/'04_composition/scene-data.json').read_text())['shots']
for shot in shots:
    n = int(shot['visual'].split('-')[-1])
    at = shot['start']+.25
    if n in [9, 13, 15, 24, 27, 43]: event(at, 'water', .8, .008)
    if n in [10, 20, 21, 30, 34]:
        event(at, 'rubber', .4)
        event(at+.8, 'rubber', .4, .005)
    if n in [25, 32, 33, 41]: event(at, 'wood', .4, .008)
    if n in [31, 35, 36]: event(at, 'cloth', .6, .006)

def save(name, data):
    target = P/'02_audio/working'/name
    with wave.open(str(target), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(data, -1, 1)*32767).astype('<i2').tobytes())
    return target

amb = save('reservoir-ambience.wav', room)
fx = save('event-foley.wav', foley)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'02_audio/working/voice-bgm.wav'),'-i',str(amb),'-i',str(fx),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:level=false:latency=true','-ar','48000','-ac','2',str(P/'04_composition/assets/audio/voice.wav')], check=True)
(P/'02_audio/sound-design.json').write_text(json.dumps({'voice_unchanged_during_mixing':True,'bgm_candidate':'cand-03','selection_basis':'User approved recommended cand-03','ambience':'quiet procedural reservoir water and wind; no indoor mechanical hum','events':events,'bgm_gain_db':-18,'outro_seconds':4,'fade_out_seconds':3},ensure_ascii=False,indent=2)+'\n')
print('Approved voice preserved; separate reservoir ambience and foley mixed.')
