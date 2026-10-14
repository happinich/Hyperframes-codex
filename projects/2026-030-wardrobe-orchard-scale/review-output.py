"""Extract each shot from actual rendered segments; never approve automatically."""
from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageChops,ImageStat
P=Path(__file__).resolve().parent;C=P/'04_composition';R=P/'05_review';O=R/'frames';O.mkdir(exist_ok=True)
shots=json.loads((C/'scene-data.json').read_text())['shots'];segments=json.loads((C/'render-segments.json').read_text());manifest=[]
prior_path=R/'rendered-shot-review.json';prior={s['shot_id']:s for s in json.loads(prior_path.read_text())['shots']} if prior_path.exists() else {}
def extract(source,t,target):
 if not target.exists() or target.stat().st_mtime<source.stat().st_mtime:subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.6f}','-i',str(source),'-frames:v','1',str(target)],check=True)
for shot in shots:
 t=(shot['startFrame']+shot['endFrame'])/120;seg=next((s for s in segments if s['startFrame']<=t*60<s['endFrame']),None)
 if seg is None:raise ValueError(shot)
 n=segments.index(seg)+1;source=P/f'06_delivery/youtube/parts/part-{n:02}.mp4'
 if not source.exists():continue
 target=O/f"{shot['id']}-{shot['scene']}.png";extract(source,t-seg['startFrame']/60,target)
 # Two separated instants measure actual captured activity, independent of authored GSAP IDs.
 a=max(shot['startFrame']/60,seg['startFrame']/60)+.08;b=min(shot['endFrame']/60,seg['endFrame']/60)-.08
 left=O/f"{shot['id']}-motion-start.png";right=O/f"{shot['id']}-motion-end.png";extract(source,a-seg['startFrame']/60,left);extract(source,b-seg['startFrame']/60,right)
 with Image.open(left) as x,Image.open(right) as y:diff=sum(ImageStat.Stat(ImageChops.difference(x.resize((480,270)).convert('RGB'),y.resize((480,270)).convert('RGB'))).mean)/3
 digest=hashlib.sha256(target.read_bytes()).hexdigest();review=prior.get(shot['id'],{})
 keep={k:review[k] for k in ['manual_frame_review','review_note','reviewed_at'] if k in review} if review.get('frame_sha256')==digest else {'manual_frame_review':'pending'}
 manifest.append({'shot_id':shot['id'],'scene_id':shot['scene'],'asset':shot['asset'],'output_seconds':round(t,3),'frame_path':str(target),'frame_sha256':digest,'motion_start_seconds':round(a,3),'motion_end_seconds':round(b,3),'mean_rgb_capture_difference':round(diff,4),**keep})
(R/'rendered-shot-review.json').write_text(json.dumps({'project_id':P.name,'shot_count':len(shots),'extracted':len(manifest),'shots':manifest},ensure_ascii=False,indent=2)+'\n');print('Extracted individual output frames and motion pairs:',len(manifest),'of',len(shots))
