"""Save a built-in image artifact and provenance; do not auto-approve it."""
from pathlib import Path
import sys,json,hashlib,shutil,re,fcntl
P=Path(__file__).resolve().parent
asset,source=sys.argv[1:3]
assert re.fullmatch(r'(?:C0[123]-S\d{2}-[AB]|SH[123]-0[1-5]|TH-[AB])',asset)
source=Path(source).resolve()
assert source.is_relative_to(Path('/Users/happinich/.codex/generated_images').resolve())
target=P/'04_composition/assets/visuals'/f'{asset}.png'
if target.exists():
    raise SystemExit(f'Asset already exists; use a versioned regeneration instead: {asset}')
shutil.copy2(source,target)
path=P/'05_review/generated-assets.json'
with path.with_suffix('.lock').open('w') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    data=json.loads(path.read_text()) if path.exists() else {'project_id':P.name,'assets':[]}
    data['assets'].append({'asset_id':asset,'source':str(source),'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'generation_mode':'built_in_imagegen','pass_1':'pending_individual_visual_inspection','pass_2':'pending_narration_and_adjacent_shots','render_approved':False})
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Saved {asset}; individual two-pass review remains required.')
