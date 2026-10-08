from pathlib import Path
import json,sys,hashlib,shutil,re
P=Path(__file__).resolve().parent;asset,source,state=sys.argv[1:4]
assert re.fullmatch(r'[A-Za-z0-9-]+',asset)
src=Path(source);assert src.is_file() and src.suffix=='.png'
f=P/'05_review/image-review-working.json';d=json.loads(f.read_text());items=json.loads((P/'01_script/image-generation-plan.json').read_text())['items'];spec=next(x for x in items if x['asset_id']==asset)
old=[a for a in d['assets'] if a.get('requested_asset_id',a['asset_id'])==asset];version=len(old)+1
label=asset if state=='passed' else asset+f'-rejected-v{version}'
dst=P/'04_composition/assets/visuals'/f'{label}.png';shutil.copy2(src,dst)
d['assets'].append({'asset_id':label,'requested_asset_id':asset,'relative_path':str(dst.relative_to(P)),'source_path':str(src),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'generation_prompt':spec['prompt'],'reference_paths':spec['references'],'kind':spec['kind'],'pass_1_result':'passed_full_resolution_tool_image_observation' if state=='passed' else 'rejected','pass_1_notes':sys.argv[4] if len(sys.argv)>4 else 'Full resolution tool image inspected; concrete review notes added by reviewer.','pass_2_result':'pending' if state=='passed' else 'not_applicable_rejected','decision':'pending_second_review' if state=='passed' else 'excluded'})
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(label,state)
