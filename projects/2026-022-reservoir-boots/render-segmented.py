"""Bound temporary storage by rendering approved scene groups one at a time."""
import json
import hashlib
import subprocess
import re
import sys
from pathlib import Path

P=Path(__file__).resolve().parent
C=P/'04_composition'
O=P/'06_delivery/youtube'
parts=O/'parts'
parts.mkdir(exist_ok=True)
segments=json.loads((C/'render-segments.json').read_text())
max_parts=int(sys.argv[1]) if len(sys.argv)>1 else len(segments)
for i,s in enumerate(segments,1):
    if i>max_parts:break
    target=parts/f'part-{i:02d}.mp4'
    cache=target.with_suffix('.json')
    html=(C/s['filename']).read_text()
    asset_hash=hashlib.sha256((C/'assets/gsap.min.js').read_bytes())
    for name in sorted(set(re.findall(r'assets/visuals/([^"<>]+\.png)',html))):
        asset_hash.update(name.encode());asset_hash.update((C/'assets/visuals'/name).read_bytes())
    fingerprint=hashlib.sha256(html.encode()+asset_hash.digest()+b'60fps-crf20-v1').hexdigest()
    if target.exists() and cache.exists() and json.loads(cache.read_text()).get('fingerprint')==fingerprint:
        probe=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=nb_frames','-of','default=nw=1:nk=1',str(target)],capture_output=True,text=True)
        if probe.returncode==0 and probe.stdout.strip()==str(s['endFrame']-s['startFrame']):
            print(f'{i}/{len(segments)} verified cached segment',flush=True)
            continue
    log=P/f'05_review/logs/render-part-{i:02d}.log'
    with log.open('w') as out:
        cmd=['npx','--no-install','hyperframes','render',str(C),'--composition',s['filename'],'--output',str(target),'--fps','60','--workers','2','--strict','--crf','20']
        result=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
    if result.returncode:
        raise SystemExit(f'Segment {i} failed; inspect {log}')
    cache.write_text(json.dumps({'fingerprint':fingerprint,'frames':s['endFrame']-s['startFrame']})+'\n')
    print(f'{i}/{len(segments)} rendered ({s["duration"]:.2f}s)',flush=True)
if max_parts<len(segments):
    print(f'Partial review render complete: {max_parts} parts',flush=True)
    raise SystemExit(0)
manifest=parts/'concat.txt'
manifest.write_text(''.join(f"file 'part-{i:02d}.mp4'\n" for i in range(1,len(segments)+1)))
duration=json.loads((P/'01_script/scene-plan.json').read_text())['duration_seconds']
target=O/f'{P.name}-youtube.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-i',str(C/'assets/audio/voice.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',f'{duration:.6f}','-movflags','+faststart',str(target)],check=True)
print(f'Final master: {target}',flush=True)
