"""Generate six new V4 takes sequentially and preserve original Shorts before 1.07x."""
from pathlib import Path
import subprocess,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];PYTHON=R/'.venv/bin/python';L=P/'05_review/logs';L.mkdir(exist_ok=True)
for category in ['chapters','shorts']:
 for i in range(1,4):
  stem=f'story-{i:02}' if category=='chapters' else f'shorts-{i:02}';d=P/f'02_audio/{category}/{stem}'
  print('starting',category,stem,flush=True)
  with (L/f'voice-{category}-{i:02}.log').open('w') as log:
   subprocess.run([str(PYTHON),str(R/'scripts/prepare_tts_script.py'),str(d),'--replace'],stdout=log,stderr=subprocess.STDOUT,check=True)
   cmd=[str(PYTHON),str(R/'scripts/generate_elevenlabs_audio.py'),str(d),'--replace']
   if category=='chapters':cmd+=['--postprocess']
   subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
   if category=='shorts':
    src=d/f'02_audio/inbox/{stem}-narration.mp3'
    subprocess.run([str(PYTHON),str(R/'scripts/ingest_audio.py'),str(d),str(src),'--replace'],stdout=log,stderr=subprocess.STDOUT,check=True)
    v=d/'02_audio/working/voice.wav';original=d/'02_audio/working/voice-original-1x.wav';shutil.copy2(v,original);speed=d/'02_audio/working/voice-speed-1_07.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(original),'-af','atempo=1.07','-ar','48000','-ac','2','-c:a','pcm_s16le',str(speed)],stdout=log,stderr=subprocess.STDOUT,check=True)
    shutil.copy2(speed,v);shutil.copy2(v,d/'04_composition/assets/audio/voice.wav')
    subprocess.run([str(PYTHON),str(R/'scripts/align_captions.py'),str(d),'--language','ko'],stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run([str(PYTHON),str(R/'scripts/analyze_audio_pacing.py'),str(d),'--language','ko'],stdout=log,stderr=subprocess.STDOUT,check=True)
  ratio=json.loads((d/'03_sync/sync_report.json').read_text())['matched_character_ratio'];print('finished',stem,'ratio',ratio,flush=True)
print('All six voice generations and timing finished.',flush=True)
