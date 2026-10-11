"""Record only a performed individual visual review; no automatic approvals."""
from pathlib import Path
import json, sys, fcntl
p=Path(__file__).resolve().parent
asset,stage,decision,note=sys.argv[1:]
assert stage in ('pass_1','pass_2') and decision in ('passed','rejected')
with (p/'05_review/generated-assets.lock').open('a+') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 f=p/'05_review/generated-assets.json';j=json.loads(f.read_text())
 a=next(a for a in j['assets'] if a['asset_id']==asset)
 a[stage]=decision;a[stage+'_note']=note
 a['render_approved']=a.get('pass_1')=='passed' and a.get('pass_2')=='passed'
 f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 print(asset,stage,decision)
