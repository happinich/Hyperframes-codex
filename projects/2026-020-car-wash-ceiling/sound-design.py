"""Keep the approved voice intact while adding quiet, timed car-wash foley."""
import json
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parents[1] / 'scripts'))
from audio_mixing import mix_bgm_with_voice, WAV_CODEC_ARGS

plan = json.loads((P/'01_script/scene-plan.json').read_text())
duration = plan['duration_seconds']
sr = 24000
rng = np.random.default_rng(20)
count = round(duration * sr)
t = np.arange(count, dtype=np.float32) / sr
room = (.00045*np.sin(2*np.pi*60*t) + .0002*np.sin(2*np.pi*120*t) + rng.normal(0,.00025,count)).astype(np.float32)
room *= np.minimum(t/2,1)*np.clip((duration-t)/3,0,1)
foley = np.zeros(count,dtype=np.float32)
events = []

def event(at, kind, seconds=.5, gain=.008):
    n=round(sr*seconds); x=np.arange(n)/sr
    env=np.minimum(x/.02,1)*np.minimum((seconds-x)/.08,1)
    if kind=='drop':
        sig=np.sin(2*np.pi*(650*x+180*x*x))*np.exp(-16*x)
    elif kind=='metal':
        sig=(np.sin(2*np.pi*62*x)+.25*np.sin(2*np.pi*119*x))*np.exp(-3*x)
    elif kind=='scratch':
        sig=np.convolve(rng.normal(0,1,n),np.ones(7)/7,'same')*(.6+.4*np.sin(2*np.pi*9*x))
    else:
        sig=np.sin(2*np.pi*90*x)*np.exp(-9*x)
    start=round(at*sr); end=min(count,start+n)
    foley[start:end]+=(sig*env*gain)[:end-start]
    events.append({'start':round(at,3),'kind':kind,'duration':seconds,'gain':gain})

shots=json.loads((P/'04_composition/scene-data.json').read_text())['shots']
seen=set()
for shot in shots:
    n=int(shot['visual'].split('-')[-1])
    if n in seen: continue
    seen.add(n); at=shot['start']
    if n in [6,8,20]:
        for i in range(3):event(at+.2+i*1.3,'drop',.4,.005)
    if n in [21,24,36,48]:event(at+.4,'metal',.9,.01)
    if n in [10,26,35,38]:event(at+.3,'scratch',.65,.008)

def save(name, data):
    target=P/'02_audio/working'/name
    with wave.open(str(target),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
    return target

amb=save('room-ambience.wav',room); fx=save('event-foley.wav',foley)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'02_audio/working/voice-bgm.wav'),'-i',str(amb),'-i',str(fx),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95:level=false:latency=true','-ar','48000','-ac','2',str(P/'04_composition/assets/audio/voice.wav')],check=True)
short=P/'04_composition/assets/audio/shorts-voice.wav'
if short.exists():
    mix_bgm_with_voice(voice_audio=short,bgm_audio=P/'02_audio/bgm/candidates/cand-02.mp3',target_audio=P/'04_composition/assets/audio/shorts-mix.wav',gain_db=-18,outro_seconds=4,outro_gain_db=-14,fade_out_seconds=3,output_codec_args=WAV_CODEC_ARGS)
(P/'02_audio/sound-design.json').write_text(json.dumps({'voice_unchanged_during_mixing':True,'bgm_candidate':'cand-02','selection_basis':'Delegated selection; cand-02 has a lower measured peak (-3.1 dB) and less peak-to-mean spread than cand-01 (-0.5 dB peak), to avoid sudden accents. Automated signal assessment, not a claim of human listening.','ambience':'quiet procedural fluorescent hum and air','events':events,'bgm_gain_db':-18,'outro_seconds':4,'fade_out_seconds':3},ensure_ascii=False,indent=2)+'\n')
print('Main ambience/foley mix ready; Short mix added only if its new voice exists.')
