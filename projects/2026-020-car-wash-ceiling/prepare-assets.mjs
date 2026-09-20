import fs from 'node:fs';
import path from 'node:path';
const P=path.dirname(new URL(import.meta.url).pathname);
const scenes=[
'Inside a dark blue sedan, a pale wet female hand pressing from OUTSIDE the top of windshield, fingers spread, faded pink sleeve; windshield rim visible. Cold-open clue only. No face.',
'Driver point of view down at illuminated dashboard; clenched male hands in charcoal work sleeves on wheel, no face. At top edge only wet black hair touches outside wiper.',
'Wide establishing view of three self-service car wash bays under one continuous steel roof over a shared exit lane. Small glass office on left, dark blue sedan nose toward exit in middle bay. No ghost or hair.',
'A compact inspection flashlight resting beside the driver seat in a dark blue sedan, male gloved hand placing it there. Normal mundane start, no ghost.',
'Last customer car driving away beyond a roofed car wash forecourt onto dark suburban road, viewed behind hanging wash hoses. No people or ghost.',
'Empty end wash bay with dry concrete, one tiny wet circular drip mark near floor drain. Cool white fixtures. No ghost, no hair, no person.',
'Close low view of tightly shut brass water valve and a correctly hanging wash hose, dry concrete beyond. No supernatural body visible.',
'Floor drain and small circular water drops in otherwise dry concrete. A male hand holds phone with indistinct muted screen off to side, no readable text, no ghost.',
'Macro on floor squeegee rubber blade catching a long strand of black wet hair, charcoal work glove reaching to lift it. No body.',
'Side-on gloved hand releasing taut black hair stretching vertically upward beyond frame; hair tip lifting clear of dry concrete, ominous negative space. No ghost body.',
'Motionless vinyl pennants at open car wash entrance, desolate dry still night, empty roofed lanes beyond. No ghost.',
'Realistic office security monitor showing empty wash bay with a narrow hanging shadow on floor; no ghost body in monitor, plausible CCTV framing. No readable labels.',
'Close-up white dome CCTV mounted to steel column, pale wet female fingers curling over its lens from above, sleeve faded pink, no face or extra hands.',
'Through office glass an isolated bare pale female foot grips the underside of overhead steel beam, sole pressing upward, dark-gray trouser ankle; rest of figure concealed in shadows. Anatomically coherent.',
'Office desk with mobile telephone held by charcoal-sleeved male hand, printed maintenance contact slip blurred under desk glass, no legible text, ordinary objects.',
'Low crouched view from office floor toward locked glass door, cold white light outside, empty lower doorway; no face, no ghost yet.',
'End wash bay overhead lighting: one long fluorescent fixture dark, adjacent fixture lit, heavy shadow above steel cross member. Do not show entity.',
'Close-up male hand turning office deadbolt; behind glass a completely empty upper dark area, unease from darkness, no ghost.',
'Long wet black hair hanging outside office door glass, tracked toward the edge of a desk as if following hidden occupant; only hair, no face.',
'Black watery line creeping under closed office door toward work shoes, shadow on low ceiling matching hidden crouching person; no visible full figure.',
'Suspended office ceiling tile lifted slightly, exactly one pale wet hand pushing fingertips through the narrow gap, dark fingernails, faded pink sleeve barely visible, no gore.',
'Low view through open office side door to nearby driver door of dark blue sedan in center wash bay, clear short escape distance, no additional figures.',
'Rear view of a charcoal work-jacket adult man crouching into dark blue sedan driver seat, no face, office side door behind, blue-white light.',
'Interior looking upward: sedan fabric headliner denting downward above driver, plastic dome lamp tilted under pressure. No visible ghost, no face.',
'Looking through sedan windshield toward white compact SUV reversing into covered car wash lane, rear lights toward viewer, no people outside, no ghost body.',
'Wet pale female palm with exactly five fingers against OUTSIDE upper windshield, faded pink sleeve and long wet black hair falling over wiper, no face; viewed from seated driver.',
'Inside passenger window fog shaped like two lips, one bead of condensation running on INTERIOR surface; empty passenger seat visible, no person. Night car wash reflections outside.',
'Wide cabin view from rear seat: empty front passenger seat, wet hand outside windshield top, male driver only shoulders and hands, no face, unnerving empty-space composition.',
'Low interior windshield view following red rear lights of white SUV heading forward toward exit, blue sedan steering wheel bottom, bright exit narrow. No entity visible.',
'Roofed exit lane fluorescent light goes dark while a faded pink sleeve and long hair hangs from roof beam far ahead between cars. No face.',
'Two bare female heels pressed to underside of exit steel beam, dark-gray trouser legs bent unnaturally backward but coherent joints. Only lower legs, no face.',
'Interior sedan dashboard foreground and narrow road toward white SUV, a female silhouette clings flat to roof underside above exit, faded pink top, charcoal trousers, wet hanging hair hides head.',
'Side mirror of blue sedan reflecting three bays descending into darkness, no ghost in mirror, red tail lights and cold fluorescent fragment.',
'White SUV pulled to RIGHT side of shared exit lane leaving a clear LEFT lane; driver arm holds rectangular work lamp upward through slightly open window, male face hidden. Pale hand approaching beam light above.',
'Extreme close-up wet female palm dragging along outside passenger glass of dark blue sedan, faded pink sleeve, thin black water streak. Exactly five fingers.',
'Single pale fingertip prying rubber seal at upper passenger window from outside, small narrow gap and wet black strand caught inside. No gore, physically plausible rubber deformation.',
'Wide exterior: blue sedan has passed SUV using left lane and is outside roof; white SUV still near roof edge. Dry open forecourt foreground, readable car positions, no people outside.',
'White SUV driver arm pulled outward through barely open window by pale female hand with pink sleeve reaching down from roof. Driver face obscured inside, other arm not visible. No injury or gore.',
'Inside blue sedan a work-gloved male hand reaches for the small inspection flashlight beside driver seat, empty passenger seat, no ghost shown.',
'Blue sedan angled on UNROOFED forecourt facing roof-edge white SUV, viewed from driver side rear, room to turn safely, no sedan under roof.',
'Driver viewpoint: hands shield flashlight reflection at windshield and aim narrow beam at pale hand gripping SUV driver arm. Focus on light path, no faces.',
'Woman clinging upside down beneath steel beam, faded wet pink top and dark gray trousers, long black hair completely covers face. Her back bends first as arms haul body up, unsettling realistic motion, no extra limbs.',
'As flashlight beam slips aside, one pale female hand reaches along beam TOWARD blue sedan outside roof; strong dark-versus-light boundary, sleeve pink, no face.',
'White SUV escaping roof edge while flashlight lights hanging hair just inside shadow, blue sedan safely outside. Final moments before road departure.',
'Two cars parked on shoulder of lit suburban road at night, blue sedan and white SUV, ordinary streetlights; nobody identifiable, roofed wash far away.',
'Close-up middle-aged male wrist with gray finger-shaped pressure marks, no blood, work jacket sleeve, seen under vehicle dome light, no faces.',
'Daylight inspection of blue sedan roof with a long shallow pressure dent and thin scratches; warped passenger rubber seal also readable, no ghost.',
'In a daylight workshop, empty sedan passenger seat beneath damp headliner; a single pale fingernail emerges through slightly opening dome lamp housing. Mechanic gloved hand and taut black hair at passenger window edge, no faces. Reserve right third quiet for endscreen.'
];
if(scenes.length!==48)throw Error('48 shots required');
const base='Use case: photorealistic-natural. ONE full-frame cinematic 16:9 movie still, not collage. Fictional modern Korean horror. Same three-bay steel-roof car wash, glass office left, dark blue compact sedan and white SUV only when specified. Cool white fluorescent and restrained red tail-light palette, dry night unless specified daylight. Authentic materials, mobile-readable shadows, natural perspective. No text, no logo, no watermark. Narrator face never visible. Entity only when specified, wet long black hair hiding face, faded pink long-sleeve top, dark gray trousers, bare feet. No gratuitous gore, no arbitrary figures. Scene: ';
const prompts=scenes.map((s,i)=>({id:`shot-${String(i+1).padStart(2,'0')}`,purpose:'longform',prompt:base+s}));
const shorts=[
'Extreme low upward view inside empty wash bay: long wet black hair descending toward lens from dark overhead beam, cool fluorescent tubes form towering vertical lines. No ghost face, no body.',
'Tight vertical shot of gloved fingers releasing one taut wet hair; the strand rises vertically toward distant steel roof. New viewpoint, not matching any widescreen frame.',
'Vertical from driver lap toward cabin roof: the blue sedan ceiling pressing down, dome lamp bending, red dashboard at bottom, no visible face or entity.',
'Vertical passenger-side angle across windshield: one pale hand in faded pink sleeve clamped to exterior top corner, long hair over glass; keep bottom third clean for captions.',
'Extreme vertical macro of empty passenger window with fresh lip-shaped condensation forming INSIDE glass, seat edge low frame; no person visible, no ending reveal.',
'Vertical driver POV focused on trembling fingers holding phone low, windshield top swallowed by wet hair outside, narrow cool light; no face, no text. Threat unresolved.'
];
shorts.forEach((s,i)=>prompts.push({id:`short-new-${String(i+1).padStart(2,'0')}`,purpose:'shorts_original',prompt:'Use case: photorealistic-natural. Create a NEW original 9:16 portrait horror movie image for a standalone teaser, not a crop, not an edit of another image. Korean self-service car wash, cold white fluorescence and dark blue sedan. Natural credible materials and geometry. No text/logos/watermark, no gore. Upper-middle main clue, bottom third readable for captions. '+s}));
prompts.push({id:'thumbnail-a',purpose:'thumbnail',prompt:'Create a polished provocative Korean horror YouTube thumbnail, 16:9 1280x720 style. Right side extreme closeup of pale wet female hand gripping outside TOP of windshield of dark blue car, long black hair hanging down, one cold fluorescent line, red accent. NO face or gore. Left side bold huge Korean text exactly "고개 들지 마" in white with one red accent word, highly readable on phone, restrained four-color cinematic contrast. No other text, no logos, no watermark.'});
prompts.push({id:'thumbnail-b',purpose:'thumbnail',prompt:'Create a distinct provocative Korean horror YouTube thumbnail, 16:9 1280x720 style. From empty car passenger seat, pale lips-shaped fog on INTERIOR glass with black wet hair outside upper corner, cold fluorescent night reflections, ominous physical clue, no person face, no gore. Left side huge bold Korean headline exactly "차 안에 누구" in white with red accent, black navy background. Single decisive clue, simple high contrast mobile readable, no other writing or logos.'});
fs.mkdirSync(path.join(P,'04_composition/assets/visuals'),{recursive:true});
for(const d of ['05_review/logs','05_review/frames','06_delivery/youtube/parts'])fs.mkdirSync(path.join(P,d),{recursive:true});
fs.writeFileSync(path.join(P,'04_composition/image-prompts.json'),JSON.stringify({generator:'built-in image_gen',shorts_policy:'all six freshly generated portrait assets; no longform frame extraction or image reuse',prompts},null,2)+'\n');
console.log(prompts.length+' independent image prompts ready');
