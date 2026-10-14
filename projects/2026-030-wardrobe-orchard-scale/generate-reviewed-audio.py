"""Use existing TTS helpers with prior-request context only, then inspect text recall AND precision."""
from pathlib import Path
import sys,json,subprocess,shutil,urllib.parse,difflib,re
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(R/'scripts'))
from dotenv import load_dotenv
from generate_elevenlabs_audio import request_audio_bytes,split_text_chunks,merge_audio_parts
from korean_tts_normalization import normalize_korean_tts_text
import os
load_dotenv(R/'.env',override=False)
PYTHON=R/'.venv/bin/python';L=P/'05_review/logs';L.mkdir(exist_ok=True)
requested=sys.argv[1:] or ['story-01']
for stem in requested:
 category='chapters' if stem.startswith('story') else 'shorts';d=P/f'02_audio/{category}/{stem}'
 with (L/f'voice-reviewed-{stem}.log').open('w') as log:
  subprocess.run([str(PYTHON),str(R/'scripts/prepare_tts_script.py'),str(d),'--replace'],stdout=log,stderr=subprocess.STDOUT,check=True)
  cfg=d/'02_audio/elevenlabs-request.json';c=json.loads(cfg.read_text());c['request']['performance_direction']='calm, conversational';c['context_stitching_strategy']='prior_request_ids_only; avoid whole neighboring chunks after detected repetition in first take';cfg.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
  original=d/f'02_audio/inbox/{stem}-narration.mp3'
  if original.exists():
   rejected=d/'02_audio/rejected';rejected.mkdir(exist_ok=True)
   version=1
   while (rejected/f'{stem}-take-{version:02}.mp3').exists():version+=1
   shutil.copy2(original,rejected/f'{stem}-take-{version:02}.mp3')
   if (d/'03_sync/whisper_raw.json').exists():shutil.copy2(d/'03_sync/whisper_raw.json',rejected/f'{stem}-take-{version:02}-whisper.json')
  parts=d/'02_audio/parts-reviewed';parts.mkdir(exist_ok=True)
  text=(d/'01_script/tts-narration.txt').read_text().strip();chunks=split_text_chunks(text);history=[];paths=[]
  for i,chunk in enumerate(chunks,1):
   print(stem,'generate',i,'/',len(chunks),len(chunk),flush=True)
   url=f'https://api.elevenlabs.io/v1/text-to-speech/{urllib.parse.quote(c["request"]["voice_id"])}?output_format=mp3_44100_128'
   audio=request_audio_bytes(url=url,api_key=os.environ['ELEVENLABS_API_KEY'],text=chunk,request_config=c['request'],chunk_number=i,chunk_count=len(chunks),request_history=history,previous_text=None,next_text=None)
   path=parts/f'part-{i:02}.mp3';path.write_bytes(audio);paths.append(path)
   (parts/f'part-{i:02}.txt').write_text(chunk+'\n')
  merge_audio_parts(paths,original)
  (parts/'requests.json').write_text(json.dumps({'request_ids':history,'model':'eleven_v4','voice_speed':1.0,'context':'sequential_prior_request_ids_only'})+'\n')
  subprocess.run([str(PYTHON),str(R/'scripts/ingest_audio.py'),str(d),str(original),'--replace'],stdout=log,stderr=subprocess.STDOUT,check=True)
  if category=='shorts':
   v=d/'02_audio/working/voice.wav';src=d/'02_audio/working/voice-original-1x.wav';shutil.copy2(v,src);tmp=d/'02_audio/working/voice-speed-1_07.wav'
   subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-af','atempo=1.07','-ar','48000','-ac','2','-c:a','pcm_s16le',str(tmp)],check=True)
   shutil.copy2(tmp,v);shutil.copy2(v,d/'04_composition/assets/audio/voice.wav')
  subprocess.run([str(PYTHON),str(R/'scripts/align_captions.py'),str(d),'--language','ko'],stdout=log,stderr=subprocess.STDOUT,check=True)
  pacing=subprocess.run([str(PYTHON),str(R/'scripts/analyze_audio_pacing.py'),str(d),'--language','ko'],stdout=log,stderr=subprocess.STDOUT)
 raw=json.loads((d/'03_sync/whisper_raw.json').read_text());heard=' '.join(s['text'] for s in raw['segments'])
 clean=lambda t:re.sub(r'[^가-힣A-Za-z0-9]','',normalize_korean_tts_text(t))
 a,b=clean(text),clean(heard);matcher=difflib.SequenceMatcher(None,a,b,autojunk=False);match=sum(x.size for x in matcher.get_matching_blocks());quality={'reference_recall':match/len(a),'heard_precision':match/len(b),'insertions':[],'omissions':[]}
 for tag,i,j,k,l in matcher.get_opcodes():
  if tag=='insert' and l-k>8:quality['insertions'].append({'heard_text':b[k:l],'char_start':k,'char_end':l})
  if tag=='delete' and j-i>8:quality['omissions'].append({'reference_text':a[i:j],'char_start':i,'char_end':j})
 quality['status']='text_review_required' if min(quality['reference_recall'],quality['heard_precision'])<.92 or quality['insertions'] or quality['omissions'] else 'objective_text_review_passed'
 (d/'03_sync/strict-text-review.json').write_text(json.dumps(quality,ensure_ascii=False,indent=2)+'\n');print(stem,quality['status'],quality['reference_recall'],quality['heard_precision'],'pacing_exit',pacing.returncode,flush=True)
