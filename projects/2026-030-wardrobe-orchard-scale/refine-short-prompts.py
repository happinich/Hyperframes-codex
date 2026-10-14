from pathlib import Path
import json
P=Path(__file__).resolve().parent;f=P/'01_script/shorts-image-generation-plan.json';d=json.loads(f.read_text())
extra={
'SH01-01':'Establish the brown two-door wardrobe north wall, LEFT window and RIGHT door. No bed, chair, feet or ghost; natural painterly room.',
'SH01-03':'Show an OUTSIDE LEFT-window viewpoint looking into the same room just BEFORE the chair reveal: brown wardrobe interior is EMPTY, no person or phone. This shot is the setup to the following chair image.',
'SH01-04':'The chair is INSIDE the cabinet, both wardrobe doors WIDELY OPEN. Its BACK faces the viewer, its SEAT faces the cabinet REAR PANEL. Cabinet inner sides surround chair. NO chair outside cabinet, feet, people or grey cloth.',
'SH02-01':'Short solid leafless tree with exactly TWO main branches at right orchard ROW, central dirt lane slopes UP to small yellow-lit shed. No ribbon, fissure, roots or face.',
'SH02-03':'Short solid leafless tree with same TWO main branches now closer to central lane, plain fixed concrete pole visible nearby as distance anchor. Central lane slopes UP to yellow shed, no ribbons, cavity, exposed roots or faces.',
'SH03-02':'Protective transparent visor is RAISED above controls. One natural ordinary grey-sleeved hand; index fingertip physically touches the yellow LEFT zero button. RED center query and GREEN right restore buttons untouched. SINGLE controller, dark BLANK display. No tape blocking pressed button, no writing or numbers.',
'SH03-04':'Show exactly TWO separate smooth ROUND shallow compressed dust marks side by side, no shoe sole patterns, footprints, visible figure or body. No gravel, craters or extra tracks.'}
for a in d['assets']:
 if a['asset_id'] in extra:a['prompt']+='\nREQUIRED SPECIFIC DETAILS: '+extra[a['asset_id']]
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
