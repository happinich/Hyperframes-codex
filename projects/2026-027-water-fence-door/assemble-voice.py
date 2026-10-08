"""Assemble separately reviewed chapter voices; use actual Whisper timestamps."""
from pathlib import Path
import json, sys, subprocess, shutil, difflib, hashlib, re
P=Path(__file__).resolve().parent
R=P.parents[1]
sys.path.insert(0,str(R/'scripts'))
from align_captions import write_captions
read=lambda p:json.loads(p.read_text())
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def duration(p):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],text=True))
def norm(s):return ''.join(c for c in s if c.isalnum())
plan=read(P/'01_script/scene-plan.json')
GAP=float(plan.get('revision',{}).get('chapter_pause_seconds',1.2))
reports=[];words=[];cues=[];offset=0.;paths=[]
work=P/'02_audio/working';work.mkdir(exist_ok=True)
gap=work/'chapter-transition.wav'
subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',str(GAP),str(gap)],check=True)
for kind in ['story','short']:
 for i in range(1,4):
  job=P/(f'02_audio/chapters/story-{i:02}' if kind=='story' else f'02_audio/shorts/shorts-{i:02}')
  authored=(job/'01_script/narration.txt').read_text()
  final=job/'02_audio/working/voice.wav';sync=read(job/'03_sync/sync_report.json');timing=read(job/'03_sync/captions.words.json')
  assert ' '.join(authored.split())==' '.join(w['text'] for w in timing['words'])
  assert sync['matched_character_ratio']>=.92
  scribe=read(P/f'05_review/scribe-{"story" if kind=="story" else "shorts"}{i:02}-final.json')
  a,b=norm(authored),norm(scribe['text']);m=difflib.SequenceMatcher(None,a,b,autojunk=False);matched=sum(x.size for x in m.get_matching_blocks())
  coverage,precision=matched/len(a),matched/len(b)
  extras=[b[b0:b1] for tag,a0,a1,b0,b1 in m.get_opcodes() if tag=='insert' and b1-b0>12]
  assert coverage>=.96 and precision>=.96 and not extras,(kind,i,coverage,precision,extras)
  events=[w for w in scribe.get('words',[]) if w.get('type')=='audio_event']
  assert not events,(kind,i,events)
  metrics=subprocess.run(['ffmpeg','-hide_banner','-i',str(final),'-af','volumedetect','-f','null','-'],text=True,capture_output=True,check=True).stderr
  peak=float(re.search(r'max_volume: ([\-\d.]+)',metrics)[1]);assert peak<-.1
  actual=duration(final)
  if kind=='short':assert 15<=actual<=40
  reports.append({'id':f'{kind}-{i:02}','duration_seconds':actual,'whisper':sync,'independent_scribe_coverage':coverage,'independent_scribe_precision':precision,'unapproved_insertions':extras,'audio_events':events,'peak_db':peak,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'review_pass_1':'Approved words compared with original V4 takes via Whisper and independent Scribe; sentence-boundary gaps checked; Short 03 first hook take preserved and regenerated for recognition discrepancy.','review_pass_2':'Final processed take independently re-aligned by canonical Whisper; Scribe v2 independently confirms no repeated/unapproved phrases. Exact caption surface, first/last words, clipping and event tags checked.','subjective_listening':'Not performed: tools provide no auditory perception. No ear-based pronunciation/emotion or background-music judgment claimed.'})
  if kind=='short':
   for ext in ['srt','vtt','words.json']:
    shutil.copy2(job/f'03_sync/captions.{ext}',P/f'03_sync/shorts-{i:02}-captions.{ext}')
   shutil.copy2(final,P/f'04_composition/assets/audio/shorts-{i:02}-voice.wav')
   continue
  chapter=plan['chapters'][i-1];chapter.update(start_seconds=offset,end_seconds=offset+actual,duration_seconds=actual)
  local=[s for s in plan['scenes'] if s.get('chapter_id')==f'C{i:02}'];cursor=0
  for index,s in enumerate(local):
   count=len(s['narration_text'].split());part=timing['words'][cursor:cursor+count];assert ' '.join(s['narration_text'].split())==' '.join(w['text'] for w in part)
   s['spoken_start_seconds']=part[0]['start']+offset;s['spoken_end_seconds']=part[-1]['end']+offset
   s['start_seconds']=offset if index==0 else max(offset,part[0]['start']+offset-.35)
   s['timing_source']='actual_final_eleven_v4_audio_mlx_whisper_large_v3_turbo'
   cursor+=count
  assert cursor==len(timing['words'])
  for j,s in enumerate(local):s['end_seconds']=local[j+1]['start_seconds'] if j+1<len(local) else offset+actual;s['duration_seconds']=s['end_seconds']-s['start_seconds']
  words.extend([{**w,'start':round(w['start']+offset,4),'end':round(w['end']+offset,4)} for w in timing['words']])
  cues.extend([{**c,'start':round(c['start']+offset,3),'end':round(c['end']+offset,3)} for c in timing['cues']])
  paths.append(final);offset+=actual
  if i<3:
   trans=next(s for s in plan['scenes'] if s['id']==f'T{i:02}')
   trans.update(start_seconds=offset,end_seconds=offset+GAP,duration_seconds=GAP)
   trans['audio']['intentional_silence']={'duration_seconds':GAP,'reason':'chapter transition; narration rests while low ambience and BGM continue'}
   paths.append(gap);offset+=GAP
assert ' '.join((P/'01_script/narration.txt').read_text().split())==' '.join(w['text'] for w in words)
manifest=work/'voice-concat.txt';manifest.write_text(''.join("file '"+str(f)+"'\n" for f in paths))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c:a','pcm_s16le',str(work/'voice.wav')],check=True)
shutil.copy2(work/'voice.wav',P/'04_composition/assets/audio/voice.wav')
write(P/'03_sync/captions.words.json',{'duration':offset,'cues':cues,'words':words})
write_captions(cues,P/'03_sync')
write(P/'03_sync/sync_report.json',{'status':'ready_for_review','whisper_model':'mlx-community/whisper-large-v3-turbo','matched_character_ratio':min(r['whisper']['matched_character_ratio'] for r in reports if r['id'].startswith('story')),'required_ratio':.92,'source':'separately aligned reviewed chapter takes with exact PCM offsets','caption_text_source':'01_script/narration.txt'})
plan.update(voice_duration_seconds=offset,duration_seconds=offset+4,outro_seconds=4,timing_source='actual_final_eleven_v4_audio_mlx_whisper_large_v3_turbo',status='voice_review_passed_objective_two_pass_checks',voice_speed_multiplier=1.00)
plan['end_screen'].update(start_seconds=offset+4-20,end_seconds=offset+4)
write(P/'01_script/scene-plan.json',plan)
write(P/'05_review/audio-review.json',{'status':'approved_objective_two_pass_review','tracks':reports,'voice_duration_seconds':offset,'subjective_listening':'Unavailable; not claimed. Independent speech recognition and signal analysis used.'})
shorts=read(P/'01_script/shorts-scene-plans.json')
for i,s in enumerate(shorts['shorts'],1):
 t=read(P/f'03_sync/shorts-{i:02}-captions.words.json');s['status']='approved_timed_voice_review_passed';s['duration_seconds']=next(r['duration_seconds'] for r in reports if r['id']==f'short-{i:02}');cursor=0
 for j,scene in enumerate(s['scenes']):
  n=len(scene['narration_text'].split());part=t['words'][cursor:cursor+n];assert ' '.join(scene['narration_text'].split())==' '.join(w['text'] for w in part)
  scene['start_seconds']=0 if j==0 else max(0,part[0]['start']-.15);scene['spoken_start_seconds']=part[0]['start'];scene['spoken_end_seconds']=part[-1]['end'];cursor+=n
 for j,scene in enumerate(s['scenes']):scene['end_seconds']=s['scenes'][j+1]['start_seconds'] if j+1<len(s['scenes']) else s['duration_seconds'];scene['duration_seconds']=scene['end_seconds']-scene['start_seconds']
write(P/'01_script/shorts-scene-plans.json',shorts)
print(json.dumps({'voice_seconds':offset,'total_with_outro':offset+4,'chapter_seconds':[c['duration_seconds'] for c in plan['chapters']],'short_seconds':[r['duration_seconds'] for r in reports if r['id'].startswith('short')]},indent=2))
