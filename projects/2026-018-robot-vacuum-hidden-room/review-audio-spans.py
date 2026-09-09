"""Independently re-transcribe recognition weak spots without editing the voice."""
import json
import subprocess
from pathlib import Path
import mlx_whisper

P=Path(__file__).resolve().parent
spans=[(19,12),(149,16),(204,15),(318,12),(434,12)]
results=[]
for start,duration in spans:
    target=P/f'02_audio/working/review-{start}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-t',str(duration),'-i',str(P/'02_audio/working/voice.wav'),str(target)],check=True)
    r=mlx_whisper.transcribe(str(target),path_or_hf_repo='mlx-community/whisper-large-v3-turbo',language='ko',condition_on_previous_text=False)
    results.append({'start':start,'duration':duration,'recognition':r['text']})
    print(start,r['text'],flush=True)
(P/'05_review/audio-span-review.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
