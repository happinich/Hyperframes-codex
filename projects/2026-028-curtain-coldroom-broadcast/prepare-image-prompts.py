"""Prepare individually generated, camera-specific image prompts from approved shots."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
plan=json.loads((P/'01_script/scene-plan.json').read_text())
styles={
 'C01': 'DARK SHADOW THEATRE: matte cut-paper silhouettes, burgundy curtain, dark wooden stage, amber work light, tactile rough paper edges. Nonphotographic, no glossy 3D. Preserve the reference operating rope as a separate thin tan two-strand vertical loop on stage left; no decorative tiebacks.',
 'C02': 'EARLY-2000s LOW-POLY SURVIVAL-HORROR GAME ART: coarse square blue-gray frost textures, low-poly edges, sparse cold white work light and yellow light from exit, no photographic realism, no glossy modern CGI. Keep the low wheeled trolley left, tall shelving right, PVC strip curtain ahead and bypass aisle right.',
 'C03': 'DARK PIXEL ART: clearly visible square pixels, deliberate stepped outlines, clustered shading and dithering, dark navy, green equipment and dim amber school light. No smooth photorealism or painterly smoothing. Guard office left, broadcast room right opposite it, stairwell beyond, glass main entrance behind the initial reference camera.',
}
characters={
 'C01': 'The narrator is one adult night-stage worker in a charcoal work jacket, dark trousers, dark cloth gloves, plain dark shoes. Show only hands, torso or back; no human face. Manager is a separate adult in a dark olive work jacket, only back or hands. One ghost: black matte work vest, shadow-black body and feet, head/face swallowed in darkness, TWO normal-five-digit hands with a long pale scar across the back of each. Where the narration needs impossible reach, hide the elongated arm behind the curtain rather than adding hands or duplicating the body. The scar is NOT a sixth finger. No gore.',
 'C02': 'One inventory worker: navy padded freezer jacket and trousers, orange work gloves, black safety boots. Show hands/back/torso without face. Shoes remain on until escape beat; only RIGHT boot is grabbed and left behind, worker exits with right sock and left boot. One creature: broad low gray body lying close to floor, rough frost-covered seamless skin, one broad low head with a single horizontal black mouth slit, TWO arms each ending in ONE large hand with EXACTLY FOUR short thick digits. Four digits is intentional nonhuman design, not ordinary malformed human anatomy. No extra limbs, no folding joints, no voice imitation. Creature existence/full shape must not appear before the narration allows it.',
 'C03': 'One temporary guard in navy security jacket, gray trousers and dark shoes; show only hands/torso/back with NO face. All responding students remain unseen: no ghost people needed. One recurring ordinary brown wooden classroom chair with black steel frame, four legs, rectangular low backrest. Chair is not present in hallway until the narration says it moved. No floating chair. Phone interfaces and monitor displays must be blank or simple dark/green space because exact text is overlaid in video editing. No misspelled numbers/words.',
}
refs={'C01':'C01-reference-stage.png','C02':'C02-reference-freezer.png','C03':'C03-reference-school.png'}
jobs=[]
for scene in plan['scenes']:
 if not scene['id'].startswith('C'):continue
 cid=scene['chapter_id']
 for shot in scene['shot_sequence']:
  prompt=f'''Use case: illustration-story. Asset type: final single landscape 16:9 scene for an approved Korean fictional horror anthology.
Generate ONE coherent full-frame image, not a grid, collage, storyboard or repeated panels. The input is a LOCATION/STYLE REFERENCE only, not an edit target. Create a genuinely NEW camera viewpoint with the same architecture and art material. A simple crop of the reference is forbidden.
Style/medium: {styles[cid]}
Story and character continuity: {characters[cid]}
Current approved narration paragraph, use only to choose the correct visible state (do not add captions): {scene['narration_text']}
THIS SHOT'S SUBJECT: {shot['subject_focus']}.
Camera position: {shot['camera_position']}. Angle: {shot['camera_angle']}. Height: {shot['camera_height']}. Shot size: {shot['shot_size']}.
Current location: {shot['location_id']}. Preserve anchors: {'; '.join(shot['spatial_anchors'])}.
Visible stage: {scene['entity_reveal_stage']}. In the opening hook show only the hand/clue named by the shot; never the entity's full identity. In normal/trace images do not add a creature or ghost body. In later contact images make the two touching surfaces distinct and physically readable, preserving the intended supernatural design.
Readability: low, ominous light with local contrast on the one decisive clue; keep it large enough for mobile. Dark negative space must retain readable contours. No generic camera shake look.
Constraints: no visible narrator faces; no random extra people/hands/fingers; no logos, watermark, generated writing, subtitles or title text. Device screen and photo/document inserts should have a clean blank editable area, unless the named shot specifically needs the visual scene inside a photograph. Do not show a later ending or object before its narrated reveal. Do not place every prop from the paragraph in this shot; focus on THIS SHOT'S SUBJECT.'''
  jobs.append({'asset_id':shot['asset_id'],'chapter_id':cid,'scene_id':scene['id'],'ref_path':str((P/'04_composition/assets/visuals'/refs[cid]).resolve()),'target_path':str((P/'04_composition/assets/visuals'/f"{shot['asset_id']}.png").resolve()),'prompt':prompt,'status':'pending'})
(P/'01_script/image-prompts.json').write_text(json.dumps({'project_id':P.name,'mode':'built_in_imagegen_one_call_per_asset','jobs':jobs},ensure_ascii=False,indent=2)+'\n')
print(f'Prepared {len(jobs)} camera-specific image prompts; no images generated by this script.')
