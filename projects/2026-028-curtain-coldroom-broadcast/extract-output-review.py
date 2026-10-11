"""Extract real render frames for coverage; this does not approve outputs."""
from pathlib import Path
import json, subprocess, concurrent.futures, sys
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
shots=json.loads((P/'04_composition/scene-data.json').read_text())['shots']
segments=json.loads((P/'04_composition/render-segments.json').read_text())
root=P/'05_review/frames/main';root.mkdir(parents=True,exist_ok=True)
round_id=sys.argv[1] if len(sys.argv)>1 else '1'
records=[]
for shot in shots:
    t=min(shot['start']+1.5,(shot['start']+shot['end'])/2) if round_id=='1' else max(shot['start']+.1,shot['end']-1.5)
    ix=next(i for i,s in enumerate(segments,1) if s['startFrame']/60<=t<s['endFrame']/60)
    src=P/f'06_delivery/youtube/parts/part-{ix:02}.mp4'
    if not src.exists() or not src.with_suffix('.json').exists():continue
    out=root/f'r{round_id}-{shot["id"]}.png'
    records.append({**shot,'time':t,'part':ix,'source':str(src),'file':str(out),'local_time':t-segments[ix-1]['startFrame']/60})
def extract(r):
    if not Path(r['file']).exists():
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(r['local_time']),'-i',r['source'],'-frames:v','1',r['file']],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(extract,records))
(root/f'round-{round_id}-index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
for n in range(0,len(records),12):
    page=Image.new('RGB',(1280,816),'#131923');draw=ImageDraw.Draw(page)
    for k,r in enumerate(records[n:n+12]):
        im=Image.open(r['file']).convert('RGB');im.thumbnail((426,240))
        x=(k%3)*426;y=(k//3)*204
        # 16:9 tile, 180px tall, leaves labels separately visible.
        im=im.resize((320,180));page.paste(im,(x+53,y))
        draw.text((x+8,y+182),f'{r["id"]} {r["scene_id"]} {r["time"]:.2f}s',fill='white')
    page.save(root/f'r{round_id}-page-{n//12+1:02}.png')
print(json.dumps({'round':round_id,'frames':len(records),'pages':(len(records)+11)//12}))
