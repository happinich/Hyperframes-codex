"""Extract one encoded midpoint per finished scene group, without assigning review decisions."""
from pathlib import Path
import json
import subprocess
P=Path(__file__).resolve().parent
segments=json.loads((P/'04_composition/render-segments.json').read_text())
directory=P/'05_review/frames/main-scene-pass2'
directory.mkdir(parents=True,exist_ok=True)
rows=[]
for i,segment in enumerate(segments,1):
    video=P/f'06_delivery/youtube/parts/part-{i:02}.mp4'
    if not video.with_suffix('.json').exists():break
    output=directory/f'{i:02}-{segment["scene"]}.png'
    midpoint=segment['duration']/2
    if not output.exists():
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(midpoint),'-i',str(video),'-frames:v','1',str(output)],check=True)
    rows.append({'part':i,'scene':segment['scene'],'absolute_seconds':segment['startFrame']/60+midpoint,'frame':str(output.relative_to(P))})
(directory/'frame-index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Encoded scene frames available:',len(rows))
