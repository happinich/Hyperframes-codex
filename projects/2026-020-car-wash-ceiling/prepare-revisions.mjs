import fs from 'node:fs';
import path from 'node:path';
const P=path.dirname(new URL(import.meta.url).pathname);
const original=JSON.parse(fs.readFileSync(path.join(P,'04_composition/image-prompts.json'))).prompts;
const exact={
 'shot-02':'Tight driver POV of instrument panel and male hands on wheel, dashboard fills lower two-thirds, only a narrow strip of windshield with ONE filament of black hair outside at top. No exterior cars, no woman body, no faces.',
 'shot-04':'Extreme closeup of a small black inspection flashlight placed in a sedan door pocket next to a charcoal work glove. Entire frame is flashlight, glove, black door upholstery. No human head or body, no exterior scene.',
 'shot-06':'Ground-level tight frame of an EMPTY concrete wash bay floor, mostly dry matte concrete and one dark water spot beside steel drain. No vehicle, no person, no ghost, no hair. Floor dominates frame.',
 'shot-07':'Macro photo of closed brass tap with black rubber hose and dry grey wall. Tap and hose fill frame, indistinct background only. No vehicles or people.',
 'shot-08':'Extreme closeup of a steel drain grate on dry concrete, a fresh ring-shaped droplet splash nearby, phone edge in male gloved hand at lower corner. Floor fills entire frame, absolutely no bodies, no vehicle, no standing ghost.',
 'shot-09':'Closeup of ONE charcoal work glove picking a black hair caught in rubber squeegee blade on dry concrete. Hair thin and taut, floor and squeegee fill entire picture. No other hand, no pink clothing, no body, no vehicle.',
 'shot-10':'Macro shot ONE charcoal work glove open as a thin black hair rises vertically out of reach, matte gray industrial wall blurred behind. Hand and hair only; no woman, no face, no vehicle.',
 'shot-11':'Closeup of motionless vinyl pennants silhouetted against cold white light above EMPTY wash bay. No people, no ghost, no vehicles, no pink clothing.',
 'shot-12':'A security monitor fills most of the frame in dark office. On its screen a COMPLETELY EMPTY wash bay and narrow shadow on dry concrete, fluorescent lighting. No visible person, no cars, no readable lettering.',
 'shot-14':'Tight upward closeup of a WET FOOTPRINT on underside of grey steel beam, beads of water following the five toe marks. Empty architecture only, no actual foot or body. A supernatural trace in ordinary industrial ceiling. No people, no vehicles.',
 'shot-15':'Extreme closeup of male hand holding phone over desk with blurred maintenance contact note beneath glass. Crop ABOVE collar so no head or face can appear. No windows or background figures.',
 'shot-16':'Low empty office interior, desk and locked glass door. Outside an EMPTY cold-lit bay. No people anywhere, no ghost, no vehicles, no pink clothes.',
 'shot-17':'Upward tight photo of two parallel fluorescent fixtures under corrugated roof, one OFF one ON, grey beam between. Entire frame ceiling only. No vehicles or people.',
 'shot-18':'Macro photograph of male hand turning brass deadbolt on dark metal office door, shallow depth of field. No glass reflections of people, no exterior vehicles.',
 'shot-19':'Inside empty office looking at upper glass door edge: ONLY a few wet strands of long black hair descend over exterior glass, no body or face. The hair tip is above desk height, empty out-of-focus exterior.',
 'shot-20':'Extreme low close-up office door bottom, thin black trickle passing under seal toward dark work boots, gray tile floor. No exterior cars or figures visible.',
 'shot-21':'Tight upward interior office shot of one lifted ceiling tile with pale fingers emerging through narrow gap. ONLY ceiling tiles and hand, no wider wash background.',
 'shot-22':'Low crouched view from small office SIDE doorway to nearby blue sedan driver door, empty gap about three steps. No ghost, no other person, no SUV.',
 'shot-23':'From behind, adult man in charcoal jacket crouches into dark blue sedan. Back of head only, face not visible. EMPTY car wash around car, NO SUV and no ghost.',
 'shot-26':'Extreme close-up at TOP edge of blue sedan windshield: pale wet female hand in faded pink sleeve presses against exterior glass; thin wet black hair drapes over glass. Camera tight enough NO woman torso, NO standing person, NO feet or ground, NO face appears.',
 'shot-27':'Close-up EMPTY sedan passenger window from inside: TWO LIP-SHAPED condensation marks and a water bead running down interior glass. NO face, eyes, nose, human reflection or woman outside. Empty seat edge lower frame.',
 'shot-28':'Empty sedan passenger seat in dim cabin, misty lip-shaped mark on side glass, outside top edge of windshield ONLY fingertips and hair. No visible person anywhere, no standing ghost.',
 'shot-30':'Low driver viewpoint along roofed exit: fluorescent tube has just gone dark; high on the underside of roof a small patch of faded pink fabric and a trace of black hair partially visible behind beam. No neck, body or face, no suspended figure. Ominous environmental clue.',
 'shot-31':'Tight view of TWO WET HEEL-SHAPED marks on underside of grey steel beam, black water trailing along metal. Only physical traces on empty steel, no actual person or body, suspenseful architectural detail.',
 'shot-32':'Upward view of roof underside with an elongated impossible SHADOW painted by cold light across corrugated metal, a small pink fabric corner caught behind beam. Empty roof architecture, no actual human figure or body. Cars far below barely visible.',
 'shot-34':'From blue sedan driver viewpoint: white SUV offset RIGHT, clear LEFT exit lane, hand holding rectangular work light through SUV window aimed upward at ceiling. At upper edge ONE pale fingertip in pink sleeve enters light. No face, no body hanging, no injury.',
 'shot-38':'Closeup of white SUV partly open driver window, adult male work-jacket forearm and ONE pale pink-sleeved ghost hand clasping wrist gently but unnervingly, skin intact, no injury or gore. Both faces entirely out of frame. Light pointing downward.',
 'shot-42':'Closeup of grey steel beam with ONE pale pink-sleeved hand gripping its side, some wet black hair trailing behind beam, shadow extending across corrugated roof. Only hand, hair, metal, and shadow; no body or face.',
 'shot-43':'Extreme close-up of ONE pale hand in pink sleeve reaching across steel beam at sharp flashlight light-shadow boundary. Only beam, hand, and cool light. No entire body, no face.',
 'shot-44':'Two vehicles escape a steel-roof wash: blue sedan already outside, white SUV driving out after it. Flashlight from sedan reveals ONLY black hair behind beam inside roof. No full person or ghost body.',
 'shot-46':'Closeup of middle-aged man wrist in work jacket with faint gray finger-shaped smudges, intact skin, no blood, no injury. Hand rests under car light, no face or other figures.',
 'shot-48':'Daylight workshop. Empty passenger seat viewed from open door. Damp fabric headliner, one tiny pale fingernail protruding through dome-light casing gap. Close detail, no whole hand/body/face. Quiet right third for end screen.'
};
const base='Generate a COMPLETELY NEW independent camera composition, do NOT reproduce any earlier photograph or include its figures. ONE widescreen 16:9 photoreal cinematic still. Restrained fictional Korean supernatural mystery, cold white fluorescent lighting, high enough exposure to see clue on phone, credible scale and materials. No text/logo/watermark, no gore. Follow ONLY these visible subjects: ';
const jobs=original.filter(p=>p.purpose==='longform'&&(exact[p.id]||Number(p.id.slice(-2))>=30)).map(p=>({id:p.id,prompt:base+(exact[p.id]||p.prompt.split('Scene: ')[1]),reason:exact[p.id]?'tight framing / reveal order / anatomy correction':'remaining main production'}));
fs.writeFileSync(path.join(P,'04_composition/image-revisions.json'),JSON.stringify({jobs},null,2)+'\n');
console.log(jobs.length+' targeted shots');
