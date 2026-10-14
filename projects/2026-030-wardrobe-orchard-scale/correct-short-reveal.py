from pathlib import Path
import json
P=Path(__file__).resolve().parent;f=P/'01_script/shorts-image-generation-plan.json';d=json.loads(f.read_text());rows={a['asset_id']:a for a in d['assets']}
fixes={
'SH02-04':('Root arch reveals creature body in spoiler-free teaser','Change ONLY the lower trunk of the large TWO-branched leafless tree: ONE ordinary SOLID vertical stump planted firmly into smooth dirt, all roots COMPLETELY UNDERGROUND. REMOVE raised root legs, arch, openings and all exposed roots. No feet, entity anatomy, hollow seams, eyes or face. Keep olive worker back, lane, paper stage style, shed and dusk unchanged.'),
'SH03-02':('Raised visor is opaque rather than transparent','Change ONLY the raised upper LID/VISOR into clear transparent acrylic: warehouse background must be visibly seen THROUGH the entire lid; retain thin rectangular rim, two hinges and its raised angle. Keep SINGLE low-poly controller, blank display, red and green buttons, SAME natural grey-sleeved hand touching yellow left button. No writing or extra fingers.'),
'SH03-04':('Chair seat recovers before pressure-release event','Change ONLY the empty wooden chair at left: its seat center visibly bows DOWN under invisible weight, matching the bowed chair in second PORTRAIT reference. Preserve four chair legs, NO figure on chair. Keep TWO round shallow pressed dust circles and empty platform/controller, low-poly pixel warehouse. No shoeprints, figures, writing or extra objects.')}
for aid,(reason,prompt) in fixes.items():
 a=rows[aid];path=Path(a['output_path']);n=len(a.get('rejected_versions',[]))+1;old=path.with_name(path.stem+f'-rejected-v{n}.png');path.rename(old);a.setdefault('rejected_versions',[]).append({'path':str(old),'reason':reason});a.update(prompt=prompt,edit_target_path=str(old),status='planned')
rows['SH03-04']['support_reference_paths']=[rows['SH03-03']['output_path']]
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
