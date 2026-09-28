import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const P = path.dirname(new URL(import.meta.url).pathname);
const read = file => JSON.parse(fs.readFileSync(path.join(P, file), 'utf8'));
const write = (file, data) => fs.writeFileSync(path.join(P, file), typeof data === 'string' ? data : JSON.stringify(data, null, 2) + '\n');
const duration = file => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', path.join(P, file)], {encoding: 'utf8'}));
const words = read('03_sync/captions.words.json').words;
const plan = read('01_script/scene-plan.json');
const total = duration('04_composition/assets/audio/voice.wav');
const voiceDuration = duration('02_audio/working/voice.wav');
const secondCues = [
  '손가락을 펼칠', '사람 없는 도서관은', '그걸 카트', '모니터를 봤어요',
  '더 이상한 건', '손을 떼자', '책 모서리에', '그 말을 듣고',
  '끝이 하나', '문 가운데', '납작한 종이', '종이를 떼어',
  '얼굴이 있어야', '붉은 천이', '그때 문 아래로', '가위 끝으로',
  '아래층으로 내려가는', '신발 옆에', '문이 닫히자', '방화문 아래에',
  '얼마 전에는', '천 안쪽에서',
];
const firstCues = {10: '저는 카트 손잡이를', 13: '유리창 너머', 15: '가위를 꺼냈습니다', 22: '손을 넣지 않고'};
const shots = [];
let offset = 0;
for (const [i, scene] of plan.scenes.entries()) {
  const tokens = scene.narration_text.split(/\s+/);
  const actual = words.slice(offset, offset + tokens.length).map(w => w.text);
  if (tokens.join(' ') !== actual.join(' ')) throw new Error('Approved narration mismatch at ' + scene.id);
  const cue = phrase => {
    const index = scene.narration_text.indexOf(phrase);
    if (index < 0) throw new Error('Missing spoken cue ' + scene.id + ': ' + phrase);
    const count = scene.narration_text.slice(0, index).trim().split(/\s+/).filter(Boolean).length;
    return Math.max(0, words[offset + count].start - 0.35);
  };
  scene.word_offset = offset;
  scene.word_count = tokens.length;
  scene.speech_start = words[offset].start;
  scene.speech_end = words[offset + tokens.length - 1].end;
  scene.start_seconds = i === 0 ? 0 : Math.max(0, scene.speech_start - 0.35);
  const first = firstCues[i + 1] ? cue(firstCues[i + 1]) : scene.start_seconds;
  const second = cue(secondCues[i]);
  if (second <= first || second >= scene.speech_end) throw new Error('Invalid image cues at ' + scene.id);
  scene.motion_beats = [
    {time: first, action: 'reveal approved image ' + (i * 2 + 1), spoken_trigger: firstCues[i + 1] || 'scene entry'},
    {time: second, action: 'reveal approved image ' + (i * 2 + 2), spoken_trigger: secondCues[i]},
  ];
  for (const [j, time] of [first, second].entries()) shots.push({id: `scene-${i + 1}-image-${j + 1}`, visual: `shot-${String(i * 2 + j + 1).padStart(2, '0')}`, start: time, scene: scene.id});
  offset += tokens.length;
}
if (offset !== words.length || shots.length !== 44) throw new Error('Unmapped approved words/images');
shots.forEach((shot, i) => shot.end = shots[i + 1]?.start ?? total);
plan.scenes.forEach((scene, i) => {
  scene.end_seconds = plan.scenes[i + 1]?.start_seconds ?? total;
  scene.duration_seconds = scene.end_seconds - scene.start_seconds;
});
plan.status = 'timed_to_approved_voice';
plan.duration_seconds = total;
plan.voice_duration_seconds = voiceDuration;
plan.outro_seconds = total - voiceDuration;
plan.timing_source = 'mlx-community/whisper-large-v3-turbo aligned to final paced voice; visuals lead cues by 0.35s';
write('01_script/scene-plan.json', plan);
write('04_composition/scene-data.json', {duration: total, voice_duration: voiceDuration, shots});

function html(items, length, {silent = false, endScreen = null} = {}) {
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>심야 도서관 반납함에서 나온 손</title><style>
*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#071117}#master{position:relative;width:1920px;height:1080px;overflow:hidden}.shot{position:absolute;inset:0;display:none;overflow:hidden}.photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform,filter}.shade{position:absolute;inset:0;pointer-events:none;background:linear-gradient(0deg,#02060944,transparent 32%,#02060918)}.light{position:absolute;inset:-12%;pointer-events:none;background:linear-gradient(110deg,transparent 23%,#a9dee514 51%,transparent 76%)}.end-safe{position:absolute;right:0;top:0;width:860px;height:1080px;background:linear-gradient(90deg,transparent,#05090abb);opacity:0}.end-label{position:absolute;right:165px;bottom:110px;color:#d5dadd;font:28px 'Apple SD Gothic Neo',sans-serif;opacity:0}
</style></head><body><main id="master" data-composition-id="youtube-master" data-width="1920" data-height="1080" data-fps="60" data-start="0" data-duration="${length}">
${silent ? '' : `<audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="${length}" data-track-index="0" data-volume="1"></audio>`}
${items.map(s => `<section class="shot" id="${s.id}"><img class="photo clip" id="${s.id}-photo" src="assets/visuals/${s.visual}.png" data-start="${s.start}" data-duration="${s.end - s.start}" alt=""><div class="shade"></div><div class="light"></div></section>`).join('')}
<div class="end-safe"></div><div class="end-label">다음 이야기는 계속됩니다</div></main><script src="assets/gsap.min.js"></script><script>
const DATA=${JSON.stringify(items)},D=${length};window.__timelines={};const tl=gsap.timeline({paused:true});
DATA.forEach((s,i)=>{const el=document.getElementById(s.id),img=el.querySelector('.photo'),light=el.querySelector('.light'),d=s.end-s.start,side=i%2?1:-1;tl.set(el,{display:'block'},s.start);tl.fromTo(img,{scale:1.06,xPercent:-side*1.4,yPercent:-.4,filter:'brightness(1.05)'},{scale:1.15,xPercent:side*1.4,yPercent:.4,filter:'brightness(.99)',duration:d,ease:'none'},s.start);tl.fromTo(light,{xPercent:-5,opacity:.18},{xPercent:8,opacity:.48,duration:d,ease:'none'},s.start);for(let t=s.start+1.4;t<s.end-.25;t+=2.6)tl.to(light,{opacity:Math.round(t)%2?.13:.53,duration:Math.min(.8,s.end-t),ease:'sine.inOut'},t);tl.set(el,{display:'none'},s.end);});
${endScreen === null || endScreen >= length ? '' : `tl.to('.end-safe',{opacity:1,duration:.5},${Math.max(0, endScreen)});tl.to('.end-label',{opacity:1,duration:.5},${Math.max(0, length - 4)});`}
tl.to({},{duration:D},0);window.__timelines['youtube-master']=tl;tl.seek(.000001,false);gsap.set(document.getElementById(DATA[0].id),{display:'block'});
</script></body></html>`;
}
write('04_composition/index.html', html(shots, total, {endScreen: total - 18}));
const dir = path.join(P, '04_composition/segments');
fs.mkdirSync(dir, {recursive: true});
if (!fs.existsSync(path.join(dir, 'assets'))) fs.symlinkSync('../assets', path.join(dir, 'assets'));
const segments = plan.scenes.map((scene, i) => {
  const startFrame = Math.round(scene.start_seconds * 60);
  const endFrame = i === plan.scenes.length - 1 ? Math.ceil(total * 60) : Math.round(plan.scenes[i + 1].start_seconds * 60);
  const start = startFrame / 60;
  const length = (endFrame - startFrame) / 60;
  const local = shots.filter(s => s.end > start + .01 && s.start < start + length - .01)
    .map(s => ({...s, start: Math.max(0, s.start - start), end: Math.min(length, s.end - start)}));
  if (!local.length) throw new Error('Empty segment ' + scene.id);
  local[0].start = 0;
  local.at(-1).end = length;
  const filename = `segments/part-${String(i + 1).padStart(2, '0')}.html`;
  write('04_composition/' + filename, html(local, length, {silent: true, endScreen: total - 18 - start}));
  return {filename, startFrame, endFrame, duration: length};
});
write('04_composition/render-segments.json', segments);
console.log(JSON.stringify({voiceDuration, total, sceneCount: plan.scenes.length, shotCount: shots.length, segments: segments.length}));
