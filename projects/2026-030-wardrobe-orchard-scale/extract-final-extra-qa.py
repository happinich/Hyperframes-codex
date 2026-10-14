"""Extract final short caption cues, bridges, and ending frames without approving them."""
from pathlib import Path
import json, subprocess, hashlib
P=Path(__file__).resolve().parent; O=P/'05_review/frames/final-extra';O.mkdir(parents=True,exist_ok=True)
items=[]
def grab(kind,video,t,label,text=''):
 q=O/f'{label}.png'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(q)],check=True)
 items.append(dict(kind=kind,output_seconds=round(t,4),label=label,caption_text=text,path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),review='pending'))
plans=json.loads((P/'01_script/shorts-caption-plan.json').read_text())
for n,plan in enumerate(plans,1):
 v=P/f'06_delivery/shorts/{P.name}-shorts-{n:02}.mp4'
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(v)]));dur=float(probe['format']['duration'])
 grab(f'SH{n:02}',v,0,f'sh{n:02}-first')
 for i,c in enumerate(plan['cues']):grab(f'SH{n:02}',v,(c['start']+c['end'])/2,f'sh{n:02}-cue-{i:02}',c['text'])
 grab(f'SH{n:02}',v,dur-.06,f'sh{n:02}-last')
v=P/f'06_delivery/youtube/{P.name}-youtube.mp4'
for t in [0,472.5,1005.5,1539,1545,1557.9]:grab('long',v,t,f'long-{t}')
(P/'05_review/final-extra-frames.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print('Extracted',len(items),'actual final MP4 frames; pending individual review.')
