"""Preserve a current-request rejected image before a replacement generation."""
from pathlib import Path
import json,sys,fcntl
p=Path(__file__).resolve().parent;ident,note=sys.argv[1:]
with (p/'05_review/generated-assets.lock').open('a+') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX);f=p/'05_review/generated-assets.json';j=json.loads(f.read_text());a=next(x for x in j['assets'] if x['asset_id']==ident)
 old=Path(a['path']);n=1
 while old.with_name(ident+f'-rejected-v{n}.png').exists():n+=1
 new=old.with_name(ident+f'-rejected-v{n}.png');old.rename(new)
 a.update(asset_id=ident+f'-rejected-v{n}',path=str(new),pass_1='rejected',pass_1_note=note,render_approved=False,replaced_by=ident)
 f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');print(new)
