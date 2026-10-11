"""Generate the approved chapter and standalone Shorts voices sequentially."""
from pathlib import Path
import json
import shutil
import subprocess

P=Path(__file__).resolve().parent
R=P.parents[1]
PY=R/'.venv/bin/python'
for kind in ('story','shorts'):
    for i in range(1,4):
        job=P/'02_audio'/('chapters' if kind=='story' else 'shorts')/f'{kind}-{i:02d}'
        log=P/f'05_review/logs/voice-{kind}-{i:02d}.log'
        timing=job/'03_sync/captions.words.json'
        config=json.loads((job/'02_audio/elevenlabs-request.json').read_text())
        if timing.is_file():
            print('ALREADY_ALIGNED',kind,i,flush=True)
            continue
        subprocess.run([str(PY),str(R/'scripts/prepare_tts_script.py'),str(job)],check=True)
        target=job/'02_audio'/config['target_audio']
        with log.open('a') as stream:
            if target.is_file():
                subprocess.run([str(PY),str(R/'scripts/ingest_audio.py'),str(job),str(target)],check=True,stdout=stream,stderr=subprocess.STDOUT)
                subprocess.run([str(PY),str(R/'scripts/align_captions.py'),str(job),'--language','ko'],check=True,stdout=stream,stderr=subprocess.STDOUT)
            else:
                subprocess.run([str(PY),'-u',str(R/'scripts/generate_elevenlabs_audio.py'),str(job),'--postprocess'],check=True,stdout=stream,stderr=subprocess.STDOUT)
        voice=job/'02_audio/working/voice.wav'
        if kind=='shorts':
            original=voice.with_name('voice-original-speed.wav')
            if not original.is_file():
                shutil.copy2(voice,original)
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(original),'-af','atempo=1.07','-ar','48000','-ac','2',str(voice)],check=True)
                shutil.copy2(voice,job/'04_composition/assets/audio/voice.wav')
                with log.open('a') as stream:
                    subprocess.run([str(PY),str(R/'scripts/align_captions.py'),str(job),'--language','ko'],check=True,stdout=stream,stderr=subprocess.STDOUT)
        with log.open('a') as stream:
            subprocess.run([str(PY),str(R/'scripts/analyze_audio_pacing.py'),str(job),'--language','ko'],check=True,stdout=stream,stderr=subprocess.STDOUT)
        print('GENERATED_ALIGNED_NOT_YET_REVIEWED',kind,i,flush=True)
