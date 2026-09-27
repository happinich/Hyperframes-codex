"""Add independently timed quiet water and rubber foley to the Short mix."""
import json
import subprocess
import wave
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent
plan = json.loads((P/'01_script/shorts-scene-plan.json').read_text())
sr = 24000
duration = plan['duration']
rng = np.random.default_rng(2206)
t = np.arange(round(duration*sr))/sr
room = np.convolve(rng.normal(0,1,len(t)),np.ones(31)/31,'same')*.0015
room *= np.minimum(t/.3,1)*np.clip((duration-t)/3,0,1)
fx = np.zeros(len(t))
events = []
for at in [13.6,14.2,16.1,16.7,20.1]:
    x = np.arange(round(.35*sr))/sr
    signal = np.sin(2*np.pi*95*x)*np.exp(-11*x)*np.minimum(x/.02,1)*np.minimum((.35-x)/.08,1)*.007
    start = round(at*sr)
    fx[start:start+len(signal)] += signal
    events.append({'at':at,'kind':'rubber','gain':.007,'seconds':.35})
paths=[]
for name,data in [('shorts-water.wav',room),('shorts-foley.wav',fx)]:
    p=P/'02_audio/working'/name
    with wave.open(str(p),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
    paths.append(p)
target=P/'04_composition/assets/audio/shorts-mix.wav'
base=target.with_name('shorts-bgm-only-mix.wav')
if not base.exists():target.rename(base)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(base),'-i',str(paths[0]),'-i',str(paths[1]),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:level=false:latency=true','-ar','48000','-ac','2',str(target)],check=True)
(P/'02_audio/shorts-sound-design.json').write_text(json.dumps({'narration_source':'separate Bin V3 generation','voice_multiplier':1.07,'bgm':'cand-03','bgm_gain_db':-18,'outro_seconds':4,'fade_out_seconds':3,'ambience':'new procedural water','events':events},indent=2)+'\n')
