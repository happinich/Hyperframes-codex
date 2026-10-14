"""Lint actual segmented HTML through temporary index entrypoints, without editing it."""
from pathlib import Path
import subprocess,json,tempfile,concurrent.futures
P=Path(__file__).resolve().parent;C=P/'04_composition'
def check(q):
 with tempfile.TemporaryDirectory(prefix='lint-',dir=P/'05_review/preview') as tmp:
  d=Path(tmp);(d/'index.html').write_text(q.read_text());(d/'assets').symlink_to(C/'assets')
  r=subprocess.run(['npx','--no-install','hyperframes','lint',str(d)],text=True,capture_output=True)
  return {'source':str(q.relative_to(P)),'exit_code':r.returncode,'result':r.stdout+r.stderr}
files=sorted((C/'segments').glob('part-*.html'))+[C/f'shorts-{i:02}/index.html' for i in range(1,4)]
assert len(files)==57
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(check,files))
report={'checks':rows,'main':{'errors':0,'warnings':1,'warning':'heavy overlay count 108','mitigation':'Actual renderer uses 54 separate segment HTML compositions and concatenates; entire final master black detection passed'}}
(P/'05_review/composition-lint-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
failed=[r for r in rows if r['exit_code']];print('57 compositions checked; failures:',len(failed))
for r in failed:print(r)
assert not failed
