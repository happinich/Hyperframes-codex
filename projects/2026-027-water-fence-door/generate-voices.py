from pathlib import Path
import subprocess,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1]
for kind in ['story','shorts']:
 for i in range(1,4):
  job=P/('02_audio/chapters' if kind=='story' else '02_audio/shorts')/f'{kind}-{i:02}'
  log=P/f'05_review/logs/voice-{kind}-{i:02}.log'
  if not (job/'03_sync/captions.words.json').exists():
   with log.open('w') as out:
    result=subprocess.run([str(R/'.venv/bin/python'),str(R/'scripts/generate_elevenlabs_audio.py'),str(job),'--postprocess'],stdout=out,stderr=subprocess.STDOUT)
   if not (job/'03_sync/captions.words.json').exists():raise SystemExit(f'Voice or alignment failed: {log}')
  audio=job/'02_audio/working/voice.wav'
  if kind=='shorts' and not (job/'02_audio/working/voice-original-speed.wav').exists():
   shutil.copy2(audio,job/'02_audio/working/voice-original-speed.wav')
   subprocess.run(['ffmpeg','-v','error','-y','-i',str(job/'02_audio/working/voice-original-speed.wav'),'-af','atempo=1.07','-ar','48000','-ac','2',str(audio)],check=True)
   shutil.copy2(audio,job/'04_composition/assets/audio/voice.wav')
   with log.open('a') as out:
    subprocess.run([str(R/'.venv/bin/python'),str(R/'scripts/align_captions.py'),str(job),'--language','ko'],check=True,stdout=out,stderr=subprocess.STDOUT)
  scribe=P/f'05_review/scribe-{kind}{i:02}-final.json'
  if not scribe.exists():subprocess.run([str(R/'.venv/bin/python'),str(P/'check-scribe.py'),str(audio),str(scribe)],check=True)
  print('GENERATED_AND_ALIGNED',kind,i,flush=True)
print('All voice jobs generated; objective review still required.',flush=True)
