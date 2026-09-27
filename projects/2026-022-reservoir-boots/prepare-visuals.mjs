import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const P=path.dirname(fileURLToPath(import.meta.url));
const scene=JSON.parse(fs.readFileSync(path.join(P,'01_script/scene-plan.json'),'utf8'));
const details=[
 'Cold-open close-up: two green boots on a wet platform lip. Pale adult wrists in gray knitted sleeves enter the boot openings from ABOVE. Hands are hidden INSIDE boots, not feet. Blue tape on the left boot. Crop out face and the rest of the body.',
 'Cold-open side close-up of one green rubber boot supporting a gray-sleeved pale forearm emerging from its top opening. A wet black lock of hair hangs at frame edge. Readable unnatural arm-in-boot contact, no legs or face.',
 'Establishing land view: single narrow wooden bridge to the floating platform and attached warm wooden cabin. Long landing net leaning on land railing. Distant platform unlit. No people or ghost.',
 'Normal setup inside the platform railing: fishing chair, single fishing rod, cabin warm light, blue water. A man seen only from behind in dark jacket and trousers sets down a bag. No ghost.',
 'Normal prop insert: pair of muddy green rubber boots with small blue tape on LEFT opening beside cabin door, one pair of plain dark sneakers nearby, dark jacket zipper in foreground. No body in boots, no paranormal detail.',
 'Water-level close-up of a small red fishing float drifting sideways in blue night water, thin fishing line extending toward platform, no face or creature.',
 'View from occupied platform across still blue water at a distant EMPTY, UNLIT platform. Red float near water foreground. Empty chair silhouettes only, no person.',
 'First-person view of a normal male hand turning the fishing reel, other hand holding rod, taut line aimed down over platform railing. Natural hands, no entity visible.',
 'Close blue water with a few small round bubbles rising beside the floating wooden deck. Fishing line slack above. No body, no face, no drowning victim.',
 'Cabin doorway at night: one muddy green boot tipped sideways, its pair upright, little blue tape on the left boot. Warm porch light and wet droplets only, no ghost.',
 'Close-up looking into empty green boot opening, water droplets along inside rubber, dark interior but visibly empty, blue tape on rim. No hand or foot.',
 'First-person flashlight beam through a narrow gap between wooden deck planks into water, black floating strands barely discernible under boards. No fingers or face.',
 'Partial clue close-up: long wet black hair spreads in flashlight-lit water directly beneath wooden platform. No visible head, facial features or full body.',
 'One anatomically normal pale adult hand emerging just above blue water, five fingers curled around thin fishing line. Wrist below water, not attached to visible body, no extra digits.',
 'Wider frightened first-person view at railing: loose rod angled toward water, the pale hand recedes under surface and disappears in ripples. No visible face or whole ghost.',
 'Adult male narrator from rear inside warm doorway making a phone call, dark jacket and sneakers. Phone screen plain dim glow with no readable interface. Open platform behind, no ghost.',
 'Close insert of a normal male hand holding phone beside cabin doorway, red fishing float visible in distant water, blue/amber contrast. No digits, text or logos on screen.',
 'Empty patch beside the cabin door where green boots had stood, damp wood, no boots, narrator dark sneaker visible at lower edge. No ghost.',
 'Close deck clue: alternating normal five-digit wet palm prints from cabin door toward railing. Correct left/right hands, not footprints, no actual hands or bodies.',
 'Two green boots seem to walk over blue water near platform, alternating tilt, blue tape on left boot. Lower shafts partly submerged. No visible foot, leg, human or arm; mystery remains hidden.',
 'Approaching green boot pair in dark water beside platform edge, tiny wet gray knitted sleeve fabric just visible BETWEEN boot openings, no face or lower body. Boots oriented toward platform.',
 'Low platform-level view: one green boot catches on a low wooden lip, gray-sleeved pale wrist entering its opening. Other boot still at water edge. Ghost body out of frame.',
 'Adult female ghost in wet gray knit leaning low over two green boots, arms supporting body with wrists entering boot openings. Long wet black hair hides face entirely. Trailing wet garment obscures lower body; no visible legs, no blood or cut surfaces.',
 'Closer side angle of the same gray-knit, wet-haired female entity hauling upper torso onto wood using her two arms inside green boots. One blue tape tab on left boot. No face, no extra arms, no exposed lower body.',
 'Warm cramped cabin interior: dark-clothed male from behind closes front wooden door with simple brass latch. Cot to the side, phone in one hand. No ghost inside.',
 'Inside cabin close-up of closed wooden front door and latched lock, dark green boot-shaped shadow outside lower door gap, phone with dim screen on cot side. No face, no text.',
 'Close floor-level warm cabin shot: water seeps under closed front door, wet rubber sole barely visible outside threshold. No exposed finger yet, no impossible floor penetration.',
 'Extreme floor-level shot: one pale slender adult finger reaches horizontally THROUGH a real small gap under wooden door into water on cabin floor. Finger attached to concealed hand outside, not growing from wood.',
 'Over-shoulder view of dark-clothed man inside cabin toward a small BACK door opening directly onto narrow wooden bridge. Warm room and cold blue outside. No readable text, face hidden.',
 'Close view through partly open back door: a single green boot physically blocking the door outside on bridge, gray sleeve above it partly cropped. Door hinges and bridge direction coherent.',
 'Escape insert: dark jacket zipper unzipped and normal adult hand pulling bare arm out of sleeve; a pale gray-sleeved hand holds the EMPTY jacket edge behind. Crop away heads, torsos anatomically coherent, no copied jackets.',
 'Narrator seen from rear running landward along wet narrow bridge, now in dark shirt WITHOUT jacket, dark trousers and sneakers. Empty dark jacket caught behind near cabin, no face.',
 'First-person fallen view on wet bridge: two normal male palms bracing wood, one plain sneaker stuck in gap between boards at side, no gore, no extra limbs.',
 'Low shot along bridge: approaching green boots with pale wrists in openings and gray-sleeved entity bent low; wet black hair near narrator hand at lower frame. Hair hides face, lower body clothed/cropped.',
 'Clue close-up: one gray-sleeved pale hand OUTSIDE boot grips a sneaker lace on wet wood, other green boot beside frame supports entity. Five fingers with natural contact, no extra fingers or severed wrists.',
 'Side view of same wet gray-knit ghost supporting her upper body on arms inside green boots beside discarded jacket, trailing soaked gray fabric lies flat concealing lower body. No knees/feet visible, no blood, no face.',
 'Landward end of narrow bridge at night: adult male friend seen from behind at shore with handheld flashlight pointed toward narrator, narrator crawling toward land in dark shirt. No face, no ghost close-up.',
 'Close narrator lower legs: one bare foot freed from an abandoned sneaker on wet bridge, other foot still in dark sneaker. Hands bracing boards. No injury or duplicate shoes.',
 'Close physical threat: green boot opening is pressed against narrator bare ankle; pale ghost hand INSIDE the boot grips ankle from opening, gray sleeve nearby. Intact rubber with a clear opening, no solid-object penetration, no gore.',
 'Rescue wide from land: friend pulls narrator arms landward, long landing-net handle reaches between green boot opening and bare lower leg at bridge edge. Faces hidden; normal adults, no extra bodies.',
 'Rescue contact detail: landing-net pole inserted into clear gap BETWEEN flexible green boot rim and intact bare ankle, pale five-fingered hand grasps pole from boot opening. Wooden/rubber/skin contact plausible, no pierced flesh.',
 'Narrator and friend safely on shore seen from back, narrator dark shirt one barefoot and one sneaker, still looking at bridge. Dark jacket and green boot pair far at bridge end. No repeated person or face.',
 'Water splashes beside bridge as ghost disappears out of sight. Two EMPTY green boots remain upright on wooden bridge, landing-net handle slides toward water. No visible woman or detached body parts.',
 'Two adult men walking toward parked plain dark car on land, seen from rear, narrator has one bare foot and one sneaker, no jacket. Reservoir and cabin in background, no ghost near car.',
 'View from plain car side window toward distant wooden bridge: flashlight glow on two empty green boots standing side by side, cabin warm lamp behind them. No ghost at car, no text.',
 'Reservoir entrance at night with two anonymous responders seen from back and two men waiting by plain car. No police emblems, readable signs or faces. Quiet credible Korean rural setting.',
 'Recovered scene insert: dim mobile phone on warm cabin cot, through open doorway a rod lies partly in water; long landing net caught BELOW bridge visible at window edge. No ghost, no readable screen.',
 'Next morning natural daylight: two muddy green rubber boots side by side on wooden bridge, blue tape clearly on LEFT opening. No hand, no body, no ghost.',
 'Daylight macro inside green boot opening: exactly FIVE distinct shallow nail scratch grooves on inside rubber surface, blue tape on near rim. No nails, fingers, gore or lettering.',
 'Photo taken from shore immediately after rescue: warm cabin, single wooden bridge receding into dark blue reservoir, two empty green boots at far bridge end. Subtle wet gray cloth beneath far bridge, no phone frame or text.',
 'Same nighttime shore photograph closer to UNDERSIDE of wooden bridge: wet gray knitted cloth clings underneath structure, black wet hair hangs downward, pale hands partly visible grasping wood toward land. No noose, no hanging by neck, no face.',
 'Final reveal low shore view: adult wet-haired female ghost clinging to UNDERSIDE bridge with two normal pale hands, gray wet knit upper body below boards, crawling LANDWARD. No boots worn, no face, no rope, no blood. Entity on left half, right half dark readable water for end screen.'
];
if(details.length!==52)throw Error('Expected 52 separately generated shots');
let index=0;
const jobs=[];
for(const s of scene.scenes)for(let j=0;j<s.planned_image_count;j++){
 const n=++index;const id='shot-'+String(n).padStart(2,'0');
 jobs.push({id,scene:s.id,purpose:'longform',detail:details[n-1],prompt:'Generate ONE NEW photorealistic cinematic 16:9 LANDSCAPE frame for an original fictional Korean reservoir horror story. Use supplied reference only for environment lighting/geometry, NOT as a fixed camera shot. '+details[n-1]+' Continuity: midnight blue water, warm tungsten wooden cabin, one narrow land-to-platform wooden bridge, plain dark green rubber boots with blue tape on LEFT when boots visible. Adult narrator dark clothes, faces never visible. If entity present: adult woman gray knitted top, long soaked black hair entirely covering face. Readable shadow details on mobile, natural object geometry, no text, numbers, logos, collage, captions, gore or gratuitous injuries. Recompose the camera for this specific detail. No extra limbs or accidental faces.'});
}
fs.writeFileSync(path.join(P,'04_composition/image-prompts.json'),JSON.stringify(jobs,null,2)+'\n');
console.log('Prepared '+jobs.length+' individual main image prompts.');
