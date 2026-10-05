"""Create original low-level cafe ambience and timed tactile foley; preserve voice and BGM stems."""
from pathlib import Path
import json,subprocess,wave,numpy as np,shutil
P=Path(__file__).resolve().parent;A=P/'02_audio/working';SR=48000
probe=lambda p:float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
total=probe(A/'voice-bgm.wav');voice=probe(A/'voice.wav');assert abs(total-voice-4)<.01
words=json.loads((P/'03_sync/captions.words.json').read_text())['words'];plan=json.loads((P/'01_script/scene-plan.json').read_text());by={x['id']:x for x in plan['scenes']}
def phrase(sid,text):
 s=by[sid];candidates=[x['start'] for x in words if s['spoken_start_seconds']-.01<=x['start']<=s['spoken_end_seconds']+.01 and text in x['text']];return candidates[0] if candidates else s['spoken_start_seconds']
foley=np.zeros(round(total*SR),dtype=np.float32);rng=np.random.default_rng(2026025);events=[]
def put(t,signal,name):
 at=round(t*SR);end=min(len(foley),at+len(signal));foley[at:end]+=signal[:end-at];events.append({'start':round(t,3),'duration':len(signal)/SR,'kind':name})
def bounce(t,amp=.025):
 x=np.arange(int(.17*SR))/SR;sig=amp*(np.sin(2*np.pi*(190*x-50*x*x))+.35*np.sin(2*np.pi*430*x))*np.exp(-x*34);put(t,sig,'hollow_plastic_ball')
def scrape(t,length=.55,amp=.008):
 x=np.arange(int(length*SR))/SR;n=rng.standard_normal(len(x)).astype(np.float32);n=np.convolve(n,np.ones(24)/24,mode='same');sig=amp*n*np.sin(np.pi*x/length)**2;put(t,sig,'short_surface_scrape')
for sid,word in [('s05','뒤꿈치에'),('s06','떨어졌어요'),('s10','날아오는'),('s22','공을'),('s30','떨어졌어요')]:bounce(phrase(sid,word))
for sid,word in [('s13','마찰음'),('s17','밀려왔어요'),('s18','떼어'),('s21','들렸어요'),('s24','굴러')]:scrape(phrase(sid,word),.55)
for t in [phrase('s31','번,'),phrase('s31','또')]:bounce(t,.02)
# The quiet vibration comes only after the phone is set into the ball bin.
t=phrase('s23','진동');x=np.arange(int(.7*SR))/SR;put(t,.006*np.sin(2*np.pi*145*x)*np.sin(np.pi*x/.7)**2,'phone_pocket_vibration')
start=phrase('s23','넣었습니다.')+.3
for t in np.arange(start,by['s24']['spoken_end_seconds'],2.3):
 x=np.arange(int(.75*SR))/SR;put(float(t),.006*np.sin(2*np.pi*145*x)*np.sin(np.pi*x/.75)**2,'phone_bin_vibration')
with wave.open(str(A/'event-foley.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(foley,-1,1)*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'anoisesrc=d={total}:c=brown:a=0.008:s={SR}', '-af',f'highpass=f=80,lowpass=f=600,afade=t=in:st=0:d=0.5,afade=t=out:st={total-3}:d=3','-ac','2',str(A/'room-ambience.wav')],check=True)
street_start=by['s25']['start_seconds'];street_end=by['s27']['start_seconds'];street_len=street_end-street_start
subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'anoisesrc=d={street_len}:c=pink:a=0.0025:s={SR}','-af',f'highpass=f=100,lowpass=f=1800,afade=t=in:st=0:d=0.8,afade=t=out:st={street_len-1}:d=1,adelay={round(street_start*1000)}:all=1,apad,atrim=duration={total}','-ac','2',str(A/'street-ambience.wav')],check=True)
final=A/'voice-bgm-soundscape.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'voice-bgm.wav'),'-i',str(A/'room-ambience.wav'),'-i',str(A/'event-foley.wav'),'-i',str(A/'street-ambience.wav'),'-filter_complex',f"[1:a]volume=0.15:enable='between(t,{street_start},{street_end})'[r];[0:a][r][2:a][3:a]amix=inputs=4:duration=first:normalize=0,alimiter=limit=0.96:level=false:latency=true[m]",'-map','[m]','-ar',str(SR),'-ac','2',str(final)],check=True)
shutil.copy2(final,P/'04_composition/assets/audio/voice.wav')
# Independently spoken Short, no excerpt or added outro.
shortdur=probe(A/'shorts-voice.wav');bgm=P/'02_audio/bgm/candidates/cand-03.mp3'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'shorts-voice.wav'),'-stream_loop','-1','-i',str(bgm),'-filter_complex',f'[1:a]volume=-22dB,afade=t=out:st={shortdur-1}:d=1[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.96:level=false:latency=true[m]','-map','[m]','-ar',str(SR),'-ac','2','-t',str(shortdur),str(P/'04_composition/assets/audio/shorts-mix.wav')],check=True)
(P/'02_audio/sound-design.json').write_text(json.dumps({'original_generated_stems':True,'events':events,'narration_unchanged':True,'duration':total,'shorts_duration':shortdur,'ambience':'room-ambience.wav','street_ambience':'street-ambience.wav','street_interval':[street_start,street_end],'foley':'event-foley.wav','mix':'voice-bgm-soundscape.wav'},ensure_ascii=False,indent=2)+'\n')
print(f'Main soundscape {total:.3f}s; Short {shortdur:.3f}s; {len(events)} foley events.')
