from pathlib import Path
import json
P=Path(__file__).resolve().parent;f=P/'01_script/image-generation-plan.json';d=json.loads(f.read_text());rows={a['asset_id']:a for a in d['assets']}
chairs=['C03-S01-A2','C03-S06-A1','C03-S07-A1','C03-S08-A1','C03-S09-A1']
ids=chairs+['C03-S13-A2','C03-S14-A1','C03-S14-A2']
for aid in ids:
 a=rows[aid];path=Path(a['output_path']);n=len(a.get('rejected_versions',[]))+1;old=path.with_name(path.stem+f'-rejected-v{n}.png');path.rename(old)
 if aid in chairs:
  reason='Adjacent continuity: empty chair looks flat before pressure releases in S14'
  prompt='Change ONLY the EMPTY wooden chair seat: give it a CLEAR shallow concave downward bow at its CENTER under invisible pressure. Match the SECOND landscape reference for the seat depression only. Keep chair legs/backrest intact and entire original camera, objects, worker, dust clues, lighting, coarse low-poly style unchanged. No body on chair, extra controller, text, numbers or new objects.'
  a['support_reference_paths']=[rows['C03-S05-A2']['output_path']]
 elif aid=='C03-S13-A2':
  reason='Raised full protective lid is opaque instead of transparent acrylic'
  prompt='Change ONLY the raised rectangular full VISOR above the controller into TRANSPARENT clear acrylic, warehouse background clearly visible THROUGH it. Keep thin rim and hinges. Preserve single controller, dark BLANK display, natural grey-sleeved hand pressing RED center query button, yellow and green untouched. No extra finger or lettering.'
 else:
  reason='Exit lower corrugated panels recover though narration explicitly leaves the door bent'
  prompt='Change ONLY the rear-LEFT corrugated metal EXIT DOOR: its LOWER HALF must have a clearly visible inward BUCKLE and crumpled metal fold, matching deformation in SECOND landscape reference. Keep the present open/closed position, woman exit path if present, normal recovered chair and cart wheels, empty scale, single office and SAME camera/pixel style unchanged. No text, numbers, extra people or objects.'
  a['support_reference_paths']=[rows['C03-S08-A2']['output_path']]
 a.setdefault('rejected_versions',[]).append({'path':str(old),'reason':reason});a.update(prompt=prompt,edit_target_path=str(old),status='planned')
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
review=P/'05_review/image-review.json';r=json.loads(review.read_text())
for a in r['assets']:
 if a['asset_id'] in ids:a['decision']='rejected_pending_replacement';a['second_full_resolution_and_adjacent_review']='pending'
review.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('Prepared 8 continuity corrections; old decisions invalidated')
