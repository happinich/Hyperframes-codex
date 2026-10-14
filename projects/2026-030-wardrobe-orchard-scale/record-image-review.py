"""Record a human/model visual inspection only after each original has been viewed."""
from pathlib import Path
import sys,json,hashlib,datetime
P=Path(__file__).resolve().parent;stage=sys.argv[1];ids=sys.argv[2].split(',');note=sys.argv[3]
plans=[]
for f in ['image-generation-plan.json','shorts-image-generation-plan.json','thumbnail-image-generation-plan.json']:
 if (P/'01_script'/f).exists():plans+=json.loads((P/'01_script'/f).read_text())['assets']
lookup={a['asset_id']:a for a in plans}
f=P/'05_review/image-review.json';d=json.loads(f.read_text()) if f.exists() else {'project_id':P.name,'status':'in_progress','required_passes':2,'assets':[]}
for aid in ids:
 a=lookup[aid];path=Path(a['output_path']);hash=hashlib.sha256(path.read_bytes()).hexdigest();entry=next((x for x in d['assets'] if x['asset_id']==aid),None)
 if entry is None:
  entry={'asset_id':aid,'scene_id':a.get('scene_id'),'relative_path':str(path.relative_to(P)),'sha256':hash,'first_full_resolution_review':'pending','second_full_resolution_and_adjacent_review':'pending','decision':'pending','rejected_versions':a.get('rejected_versions',[]),'reviews':[]};d['assets'].append(entry)
 if entry['sha256']!=hash and stage!='pass1':raise SystemExit('Asset changed since first review: '+aid)
 if entry['sha256']!=hash:
  entry['first_full_resolution_review']='pending';entry['second_full_resolution_and_adjacent_review']='pending'
 entry['sha256']=hash;entry['rejected_versions']=a.get('rejected_versions',[])
 field='first_full_resolution_review' if stage=='pass1' else 'second_full_resolution_and_adjacent_review';entry[field]='approved';entry['reviews'].append({'pass':stage,'note':note,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'resolution':'original_individually_viewed'})
 entry['decision']='approved' if entry['first_full_resolution_review']==entry['second_full_resolution_and_adjacent_review']=='approved' else 'pending_second_pass'
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(stage,len(ids),'recorded')
