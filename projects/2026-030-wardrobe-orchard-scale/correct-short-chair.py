from pathlib import Path
import json
P=Path(__file__).resolve().parent;f=P/'01_script/shorts-image-generation-plan.json';d=json.loads(f.read_text());rows={a['asset_id']:a for a in d['assets']}
fixes={
'SH01-03':('Unwanted worker remains inside room during outside look-back','REMOVE the entire woman from inside room: head, body, both legs and hands. The room is EMPTY, wardrobe interior EMPTY. Keep this freshly generated portrait camera outside the left window, same open wardrobe, dolly, window frame, warm gouache paint and palette. No chair yet, no human, ghost, feet or phone.'),
'SH01-04':('Chair seat faces viewer rather than rear panel','Rotate ONLY the small chair 180 degrees. We see its REAR side: backrest and REAR legs toward camera, FRONT legs farther away close to wardrobe back wall. Its seat points AWAY from camera toward rear panel. Hide broad front seat surface behind rear backrest. The SECOND landscape reference is orientation guidance ONLY; generate an independent portrait image, never crop or extract it. Retain full open wardrobe with chair INSIDE cabinet, painted material. No person, feet, grey fabric or ghost.')}
for aid,(reason,prompt) in fixes.items():
 a=rows[aid];path=Path(a['output_path']);old=path.with_name(path.stem+'-rejected-v1.png');path.rename(old);a['rejected_versions']=[{'path':str(old),'reason':reason}];a.update(prompt=prompt,edit_target_path=str(old),status='planned')
rows['SH01-04']['support_reference_paths']=[str(P/'04_composition/assets/visuals/c01-s07-a2.png')]
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
