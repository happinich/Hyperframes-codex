"""Original restrained ambience and foley, preserving all approved TTS masters."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt

P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'scripts'))
from audio_mixing import mix_bgm_with_voice
SR=48000
plan=json.loads((P/'01_script/scene-plan.json').read_text())
words=json.loads((P/'03_sync/captions.words.json').read_text())['words']
D=P/'02_audio/sound-design';D.mkdir(exist_ok=True)
def save(path,data):
 with wave.open(str(path),'wb') as out:
  out.setparams((2,2,SR,0,'NONE','not compressed'))
  if data.ndim==1:data=np.column_stack((data,data))
  out.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
def normal(s):return re.sub(r'[^가-힣0-9a-zA-Z]','',s)
def cue(scene,phrase):
 ws=[w for w in words if scene['spoken_start_seconds']-.01<=w['start']<scene['spoken_end_seconds']+.01]
 target=normal(phrase)
 for i in range(len(ws)):
  line=''
  for j in range(i,min(len(ws),i+8)):
   line+=normal(ws[j]['text'])
   if target in line:return ws[i]['start']
 raise ValueError(f'Missing sound cue {scene["id"]}: {phrase}')
rng=np.random.default_rng(28)
sources={}
for n,(freq,cut) in enumerate([(52,750),(86,1050),(120,550)],1):
 t=np.arange(30*SR)/SR
 noise=sosfilt(butter(2,cut,fs=SR,output='sos'),rng.normal(0,1,len(t)))
 noise=noise/max(np.max(np.abs(noise)),1e-9)
 data=(.0017*np.sin(2*np.pi*freq*t)+.0012*noise)*(.8+.2*np.sin(2*np.pi*t/13))
 # Steady room tone; loop endpoints are crossfaded in the final ambience bus.
 save(D/f'room-{n:02}.wav',data)
 sources[n]=data
foley={}
for kind,length in [('scrape',1.25),('paper',.6),('metal',.75),('relay',.14),('buzz',.7),('thud',.3),('pvc',.65)]:
 t=np.arange(round(length*SR))/SR
 noise=sosfilt(butter(2,[90,2600],btype='bandpass',fs=SR,output='sos'),rng.normal(0,1,len(t)))
 if kind=='metal':x=np.sin(2*np.pi*860*t)*np.exp(-7*t)+.5*np.sin(2*np.pi*1310*t)*np.exp(-10*t)
 elif kind=='buzz':x=np.sin(2*np.pi*145*t)*(.4+.6*(np.sin(2*np.pi*9*t)>0))
 elif kind=='thud':x=np.sin(2*np.pi*(95*t-45*t*t))*np.exp(-14*t)+.12*noise
 elif kind=='relay':x=noise*np.exp(-45*t)
 else:x=noise*(.65+.35*np.sin(2*np.pi*(8 if kind=='scrape' else 17)*t))
 envelope=np.minimum(1,t/.035)*np.minimum(1,(length-t)/.11)
 x=x*envelope;x=x/max(np.max(np.abs(x)),1e-9)*(.014 if kind in ['metal','thud'] else .009)
 foley[kind]=x;save(D/f'foley-{kind}.wav',x)
specs=[
 ('C01-S10','바닥 긁는 소리가','scrape'),('C01-S14','금속 고리가','metal'),
 ('C01-S16','넘어져','thud'),('C01-S18','눌렀어요','relay'),('C01-S20','금속 고리가','metal'),
 ('C02-S04','상자가 미끄러져','paper'),('C02-S07','가운데 두 장만','pvc'),
 ('C02-S08','바닥을 문지르는','scrape'),('C02-S10','그때 상자 안쪽에서','scrape'),
 ('C02-S12','상자가 하나 더','paper'),('C02-S16','큰 문이 움직이는','metal'),
 ('C02-S17','걷어찼습니다','thud'),('C02-S18','골판지가 찢어졌습니다','paper'),
 ('C02-S19','금속이 부딪쳤습니다','metal'),('C02-S22','밑창이 종이를','paper'),
 ('C03-S04','스피커에서 안내','relay'),('C03-S06','처음 껐던 교실에서','scrape'),
 ('C03-S07','그때 복도','relay'),('C03-S11','방송이 시작됐어요','relay'),
 ('C03-S12','의자를 끄는','scrape'),('C03-S14','전화가 울렸습니다','buzz'),
 ('C03-S17','의자 다리를','scrape'),('C03-S18','다시 울렸습니다','buzz'),
 ('C03-S19','의자가 문에','thud'),('C03-S21','학교 쪽으로','scrape'),
 ('C03-S23','음성 메시지가','relay')]
events=[]
for sid,phrase,kind in specs:
 s=next(s for s in plan['scenes'] if s['id']==sid)
 at=cue(s,phrase)
 e={'scene_id':sid,'spoken_cue':phrase,'start_seconds':at,'kind':kind,'duration_seconds':len(foley[kind])/SR,'peak_dbfs':float(20*np.log10(np.max(np.abs(foley[kind]))))}
 events.append(e);s['audio']['foley'].append(e)
for s in plan['scenes']:
 s['audio']['narration']='approved_esther_eleven_v4_1.00x'
 s['audio']['bgm']='approved_by_user_selection_delegation_cand-04'
 s['audio']['ambience']='original_generated_room_bus' if not s['id'].startswith('T') else 'room_tone_crossfade_with_bgm'
def bus(path,duration,ambient=False,selected_events=None,chapter_number=None):
 with wave.open(str(path),'wb') as out:
  out.setparams((2,2,SR,0,'NONE','not compressed'))
  for start in range(0,round(duration*SR),SR):
   n=min(SR,round(duration*SR)-start);indices=np.arange(start,start+n);t=indices/SR;x=np.zeros(n)
   if ambient:
    for c in plan['chapters'] if chapter_number is None else [plan['chapters'][chapter_number-1]]:
     num=int(c['id'][-1]);cs=c['start_seconds'] if chapter_number is None else 0;ce=c['end_seconds'] if chapter_number is None else duration
     gain=np.clip((t-cs)/.65,0,1)*np.clip((ce-t)/1.2,0,1)
     x+=sources[num][indices%len(sources[num])]*gain
   else:
    for e in selected_events or events:
     pos=round(e['start_seconds']*SR);signal=foley[e['kind']];lo=max(start,pos);hi=min(start+n,pos+len(signal))
     if hi>lo:x[lo-start:hi-start]+=signal[lo-pos:hi-pos]
   out.writeframes((np.column_stack((x,x))*32767).astype('<i2').tobytes())
total=plan['duration_seconds'];bus(D/'ambience-bus.wav',total,True);bus(D/'foley-bus.wav',total)
voice=P/'02_audio/working/voice.wav';before=hashlib.sha256(voice.read_bytes()).hexdigest()
target=P/'02_audio/working/voice-final.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'02_audio/working/voice-bgm.wav'),'-i',str(D/'ambience-bus.wav'),'-i',str(D/'foley-bus.wav'),'-filter_complex','[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first:dropout_transition=0[a]','-map','[a]','-c:a','pcm_s16le','-ar','48000','-ac','2',str(target)],check=True)
shutil.copy2(target,P/'04_composition/assets/audio/voice.wav')
shorts=json.loads((P/'01_script/shorts-scene-plans.json').read_text())
for num,short in enumerate(shorts['shorts'],1):
 voice_short=P/f'04_composition/assets/audio/shorts-{num:02}-voice.wav';music=D/f'shorts-{num:02}-bgm.wav'
 mix_bgm_with_voice(voice_audio=voice_short,bgm_audio=P/'02_audio/bgm/candidates/cand-04.mp3',target_audio=music,gain_db=-18,outro_seconds=0,fade_out_seconds=.45,output_codec_args=['-c:a','pcm_s16le'])
 ambience=D/f'shorts-{num:02}-ambience.wav';bus(ambience,short['duration_seconds'],True,chapter_number=num)
 out=P/f'04_composition/assets/audio/shorts-{num:02}-mix.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(music),'-i',str(ambience),'-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0:duration=first:dropout_transition=0[a]','-map','[a]','-c:a','pcm_s16le','-ar','48000','-ac','2',str(out)],check=True)
assert before==hashlib.sha256(voice.read_bytes()).hexdigest()
(P/'01_script/scene-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
(P/'05_review/sound-design-review.json').write_text(json.dumps({'status':'signal_and_synchronization_review_required','provenance':'Original deterministic numpy/scipy synthesis in this project; no sampled external recordings.','voice_only_sha256':before,'voice_master_preserved':True,'bgm_candidate':'cand-04','events':events,'ambience_max_peak_dbfs':-46,'subjective_listening_performed':False,'listening_limitation':'Tools do not provide auditory perception; do not claim review by ear.','shorts_no_outro_extension':True},ensure_ascii=False,indent=2)+'\n')
print(f'Mixed separate narration, original ambience, {len(events)} restrained foley events and approved cand-04; three Shorts mixed separately.')
