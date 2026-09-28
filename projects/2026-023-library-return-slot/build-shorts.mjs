import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const P = path.dirname(new URL(import.meta.url).pathname);
const read = file => JSON.parse(fs.readFileSync(path.join(P, file), 'utf8'));
const write = (file, data) => fs.writeFileSync(path.join(P, file), typeof data === 'string' ? data : JSON.stringify(data, null, 2) + '\n');
const duration = file => Number(execFileSync('ffprobe', ['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',path.join(P,file)], {encoding:'utf8'}));
const paragraphs = fs.readFileSync(path.join(P,'01_script/shorts-narration.txt'),'utf8').trim().split(/\n\s*\n/);
const words = read('03_sync/shorts-captions.words.json').words;
if (paragraphs.length !== 6 || paragraphs.join(' ').split(/\s+/).join(' ') !== words.map(w => w.text).join(' ')) throw new Error('Shorts script/alignment mismatch');
const total = duration('04_composition/assets/audio/shorts-mix.wav');
if (total < 15 || total > 40) throw new Error('Shorts duration outside 15-40 seconds: ' + total);
let offset = 0;
const shots = paragraphs.map((p,i) => {
  const first = words[offset].start;
  offset += p.split(/\s+/).length;
  return {id:'short-'+(i+1), visual:'short-new-'+String(i+1).padStart(2,'0'), start:i ? Math.max(0,first-.15) : 0, narration:p};
});
shots.forEach((s,i) => s.end = shots[i+1]?.start ?? total);
const captions = [];
let buffer = [];
function flush() {
  if (!buffer.length) return;
  captions.push({start:buffer[0].start, end:buffer.at(-1).end, text:buffer.map(w=>w.text).join(' ')});
  buffer = [];
}
for (const w of words) {
  if (buffer.length && (buffer.map(x=>x.text).join(' ').length + w.text.length > 19 || w.start-buffer.at(-1).end > .35)) flush();
  buffer.push(w);
  if (/[.!?]$/.test(w.text)) flush();
}
flush();
const esc = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>심야 도서관 반납함 - 쇼츠</title><style>
@font-face{font-family:'Apple SD Gothic Neo';src:local('Apple SD Gothic Neo')}*{box-sizing:border-box}html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#071015;color:white;font-family:'Apple SD Gothic Neo',sans-serif}#master{position:relative;width:1080px;height:1920px;overflow:hidden}.shot{position:absolute;inset:0;display:none;overflow:hidden}.photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform,filter}.shade{position:absolute;inset:0;background:linear-gradient(0deg,#010608a6,transparent 47%,#01060855);pointer-events:none}.light{position:absolute;inset:-10%;background:linear-gradient(125deg,transparent 35%,#9fd9e514 55%,transparent 78%);pointer-events:none}.hook{position:absolute;left:70px;right:160px;top:160px;font-size:67px;font-weight:900;line-height:1.24;text-shadow:0 4px 15px #000;word-break:keep-all}.captions{position:absolute;left:70px;right:160px;bottom:350px;font-size:55px;font-weight:850;line-height:1.33;text-align:center;word-break:keep-all;-webkit-text-stroke:7px #000;paint-order:stroke fill}.caption{position:absolute;left:0;right:0;bottom:0;opacity:0}.cta{position:absolute;left:75px;right:160px;bottom:275px;font-size:32px;text-align:center;opacity:0;text-shadow:0 3px 12px #000}
</style></head><body><main id="master" data-composition-id="shorts-master" data-width="1080" data-height="1920" data-fps="60" data-start="0" data-duration="${total}">
<audio id="shorts-audio" src="assets/audio/shorts-mix.wav" data-start="0" data-duration="${total}" data-track-index="0" data-volume="1"></audio>
${shots.map(s=>`<section class="shot" id="${s.id}"><img id="${s.id}-photo" class="photo clip" src="assets/visuals/${s.visual}.png" data-start="${s.start}" data-duration="${s.end-s.start}" alt=""><div class="shade"></div><div class="light"></div></section>`).join('')}
<div class="hook">아무도 없었는데<br>반납함이 열렸다</div><div class="captions">${captions.map((c,i)=>`<div class="caption" id="cap-${i}">${esc(c.text)}</div>`).join('')}</div><div class="cta">그 뒤에 무엇이 있었을까요?<br>관련 동영상에서 본편 보기</div></main><script src="assets/gsap.min.js"></script><script>
const SHOTS=${JSON.stringify(shots)},CAPS=${JSON.stringify(captions)},D=${total};window.__timelines={};const tl=gsap.timeline({paused:true});
SHOTS.forEach((s,i)=>{const el=document.getElementById(s.id),img=el.querySelector('.photo'),light=el.querySelector('.light'),d=s.end-s.start,side=i%2?1:-1;tl.set(el,{display:'block'},s.start);tl.fromTo(img,{scale:1.08,xPercent:-side*1.5,yPercent:-.5},{scale:1.17,xPercent:side*1.5,yPercent:.5,duration:d,ease:'none'},s.start);tl.fromTo(light,{opacity:.18,xPercent:-4},{opacity:.53,xPercent:9,duration:d,ease:'none'},s.start);for(let t=s.start+1.1;t<s.end-.25;t+=2.2)tl.to(light,{opacity:Math.round(t)%2?.16:.62,duration:Math.min(.65,s.end-t)},t);tl.set(el,{display:'none'},s.end)});
CAPS.forEach((c,i)=>{tl.set('#cap-'+i,{opacity:1},c.start);tl.set('#cap-'+i,{opacity:0},c.end)});
tl.to('.hook',{opacity:0,duration:.2},3.3);tl.to('.cta',{opacity:1,duration:.3},D-3.8);tl.to({},{duration:D},0);window.__timelines['shorts-master']=tl;tl.seek(.000001,false);gsap.set(document.getElementById(SHOTS[0].id),{display:'block'});
</script></body></html>`;
const variant = path.join(P,'04_composition/variants');
fs.mkdirSync(variant,{recursive:true});
if (!fs.existsSync(path.join(variant,'assets'))) fs.symlinkSync('../assets',path.join(variant,'assets'));
write('04_composition/variants/shorts.html',html);
write('01_script/shorts-scene-plan.json',{duration_seconds:total,voice_speed_multiplier:1.07,format:{width:1080,height:1920,fps:60},shots,captions,spoiler_free:true});
console.log(JSON.stringify({duration:total,shots:shots.length,captions:captions.length}));
