"""Original restrained ambience/foley, separate from approved spoken takes and BGM."""
from pathlib import Path
import json, subprocess, wave, shutil
import numpy as np
P=Path(__file__).resolve().parent
A=P/'02_audio/working'; C=P/'04_composition/assets/audio'; SR=48000
probe=lambda p:float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
total=probe(A/'voice-bgm.wav'); voice=probe(A/'voice.wav')
assert abs(total-voice-4)<.01
plan=json.loads((P/'01_script/scene-plan.json').read_text())
words=json.loads((P/'03_sync/captions.words.json').read_text())['words']
scenes={s['id']:s for s in plan['scenes']}
def phrase(sid,part):
 s=scenes[sid]
 matches=[w['start'] for w in words if s.get('spoken_start_seconds',s['start_seconds'])-.01<=w['start']<=s.get('spoken_end_seconds',s['end_seconds'])+.01 and part in w['text']]
 if not matches: raise ValueError((sid,part))
 return matches[0]
rng=np.random.default_rng(2026027)
foley=np.zeros(round(total*SR),dtype=np.float32); events=[]
def add(t,length,kind,amp=.016):
 x=np.arange(round(length*SR),dtype=np.float32)/SR
 noise=rng.normal(0,1,len(x)).astype(np.float32)
 noise=np.convolve(noise,np.ones(16,dtype=np.float32)/16,mode='same')
 if kind=='water_drop': sig=(np.sin(2*np.pi*(760*x-900*x*x))+.3*np.sin(2*np.pi*1100*x))*np.exp(-x*40)
 elif kind=='telephone_vibration': sig=np.sin(2*np.pi*145*x)*np.sin(np.pi*x/length)**2
 elif kind=='countdown_tone': sig=np.sin(2*np.pi*420*x)*np.sin(np.pi*x/length)**2
 elif kind=='train_pass': sig=noise*np.sin(np.pi*x/length)**2+0.05*np.sin(2*np.pi*70*x)*np.sin(np.pi*x/length)**2
 else: sig=noise*np.sin(np.pi*x/length)**2
 sig=(sig*amp).astype(np.float32); start=round(max(0,t)*SR); end=min(len(foley),start+len(sig))
 foley[start:end]+=sig[:end-start]
 events.append({'start':round(t,3),'duration':length,'kind':kind,'peak_amplitude':float(np.max(np.abs(sig))),'source':'original_procedural_synthesis_no_external_recordings'})
for sid,part,kind,length in [
 ('C01-S04','물장구','water_swish',1.2),('C01-S06','떨어지고','water_drop',.18),('C01-S08','진동이','telephone_vibration',.5),('C01-S12','긁혔어요.','metal_scrape',.65),('C01-S15','부딪쳤어요.','metal_hit',.3),('C01-S16','닫히고,','door_thud',.3),
 ('C02-S04','눌리는','grass_rustle',.7),('C02-S05','손뼉을','soft_clap',.16),('C02-S05','축축한','soft_clap',.18),('C02-S09','경보음이','countdown_tone',.18),('C02-S10','철망이','fence_rattle',.5),('C02-S12','꺾이고','tent_creak',.7),('C02-S14','찌그러지는','metal_scrape',.65),
 ('C03-S04','돌리는','latch_click',.12),('C03-S05','잠금쇠가','latch_click',.15),('C03-S08','의자가','chair_drag',.75),('C03-S09','삐걱거렸습니다.','wood_creak',.6),('C03-S13','찌그러졌어요.','cardboard_crush',.45),('C03-S14','상자가','cardboard_drag',.5),('C03-S17','소리가','door_thud',.35),('C03-S21','상자를','cardboard_drag',.7)]:
 add(phrase(sid,part),length,kind,.013)
with wave.open(str(A/'event-foley.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(foley,-1,1)*32767).astype('<i2').tobytes())
ambience=[]
for i,ch in enumerate(plan['chapters']):
 start=ch['start_seconds']; length=ch['duration_seconds']; fn=A/f'ambience-story-{i+1:02}.wav'
 color=['brown','pink','brown'][i]; filters=['highpass=f=90,lowpass=f=650','highpass=f=80,lowpass=f=900','highpass=f=60,lowpass=f=500'][i]
 subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'anoisesrc=d={length}:c={color}:a=0.004:s={SR}', '-af',f'{filters},afade=t=in:st=0:d=0.5,afade=t=out:st={length-1}:d=1,adelay={round(start*1000)}:all=1,apad,atrim=duration={total}','-ac','2',str(fn)],check=True)
 ambience.append(fn)
cmd=['ffmpeg','-v','error','-y','-i',str(A/'voice-bgm.wav'),'-i',str(A/'event-foley.wav')]
for p in ambience:cmd+=['-i',str(p)]
final=A/'voice-bgm-soundscape.wav'
cmd+=['-filter_complex','[0:a][1:a][2:a][3:a][4:a]amix=inputs=5:duration=first:normalize=0,alimiter=limit=0.96:level=false:latency=true[m]','-map','[m]','-ar',str(SR),'-ac','2',str(final)]
subprocess.run(cmd,check=True);shutil.copy2(final,C/'voice.wav')
shortdur=[]
for i in range(1,4):
 src=C/f'shorts-{i:02}-voice.wav'; d=probe(src);shortdur.append(d)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-stream_loop','-1','-i',str(P/'02_audio/bgm/candidates/cand-03.mp3'),'-filter_complex',f'[1:a]volume=-22dB,afade=t=in:st=0:d=0.25,afade=t=out:st={d-1}:d=1[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.96:level=false:latency=true[m]','-map','[m]','-ar',str(SR),'-ac','2','-t',str(d),str(C/f'shorts-{i:02}-mix.wav')],check=True)
(P/'02_audio/sound-design.json').write_text(json.dumps({'original_generated_stems':True,'events':events,'narration_stem_unchanged':True,'duration_seconds':total,'voice_duration_seconds':voice,'shorts_duration_seconds':shortdur,'ambience_stems':[str(p.relative_to(P)) for p in ambience],'foley':'02_audio/working/event-foley.wav','mix':'02_audio/working/voice-bgm-soundscape.wav','subjective_listening':'Unavailable. Signal levels, speech verification and exact event timing are reviewed; ear-based sound quality is not claimed.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'duration':total,'shorts':shortdur,'events':len(events)}))
