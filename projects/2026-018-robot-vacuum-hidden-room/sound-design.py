"""Render independent, restrained procedural room tone and foley layers."""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'scripts'))
from audio_mixing import mix_bgm_with_voice, WAV_CODEC_ARGS

plan=json.loads((P/'01_script/scene-plan.json').read_text())
duration=plan['duration_seconds']
sr=24000
rng=np.random.default_rng(18)
count=round(duration*sr)
t=np.arange(count,dtype=np.float32)/sr
room=(.00065*np.sin(2*np.pi*60*t)+.00028*np.sin(2*np.pi*121*t)+rng.normal(0,.00035,count)).astype(np.float32)
room*=np.minimum(t/2,1)*np.clip((duration-t)/3,0,1)
foley=np.zeros(count,dtype=np.float32)
events=[]
def event(at,kind,seconds=.8,gain=.014):
    n=round(sr*seconds);x=np.arange(n)/sr
    env=np.minimum(x/.025,1)*np.minimum((seconds-x)/.09,1)
    if kind=='notification':
        sig=(np.sin(2*np.pi*660*x)+.25*np.sin(2*np.pi*880*x))*np.exp(-6*x)
    elif kind=='motor':
        sig=(np.sin(2*np.pi*(95*x+14*x*x))+.3*np.sin(2*np.pi*193*x))*(.6+.4*np.sin(2*np.pi*4*x))
    elif kind=='scratch':
        raw=rng.normal(0,1,n);sig=np.convolve(raw,np.ones(8)/8,'same')*(.5+.5*np.sin(2*np.pi*11*x))
    else:
        sig=np.sin(2*np.pi*52*x)*np.exp(-8*x)
    start=round(at*sr);end=min(start+n,count)
    foley[start:end]+=(sig*env*gain)[:end-start]
    events.append({'start':round(at,3),'kind':kind,'duration':seconds,'peak_gain':gain})
for s in plan['scenes']:
    if s['id'] in ['S03','S04','S16']:event(s['start_seconds']+.3,'notification',.55,.008)
    if s['id'] in ['S05','S08','S17']:event(s['start_seconds']+.6,'motor',2.0,.007)
    if s['id']=='S11':event(s['start_seconds']+.25,'scratch',.8,.014)
    if s['id']=='S12':event(s['start_seconds']+.4,'scratch',1.1,.012)
    if s['id']=='S13':
        for i in range(6):event(s['start_seconds']+.3+i*.44,'step',.22,.017)
def save(name,data):
    target=P/'02_audio/working'/name
    with wave.open(str(target),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
    return target
amb=save('room-ambience.wav',room);fx=save('event-foley.wav',foley)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'02_audio/working/voice-bgm.wav'),'-i',str(amb),'-i',str(fx),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:level=false:latency=true','-ar','48000','-ac','2',str(P/'04_composition/assets/audio/voice.wav')],check=True)
mix_bgm_with_voice(voice_audio=P/'04_composition/assets/audio/shorts-voice.wav',bgm_audio=P/'02_audio/bgm/candidates/cand-01.mp3',target_audio=P/'04_composition/assets/audio/shorts-mix.wav',gain_db=-18,outro_seconds=4,outro_gain_db=-14,fade_out_seconds=3,output_codec_args=WAV_CODEC_ARGS)
(P/'02_audio/sound-design.json').write_text(json.dumps({'seed':18,'voice_unchanged':True,'bgm_candidate':'cand-01','selection_basis':'Lower measured mean and peak than cand-02, supporting restrained mechanical tension. User delegated choice.','ambience':'procedural 60Hz room tone and soft air','events':events,'bgm_gain_db':-18,'outro_seconds':4,'fade_out_seconds':3},ensure_ascii=False,indent=2)+'\n')
print('Independent ambience, foley and main/Shorts mixes complete.')
