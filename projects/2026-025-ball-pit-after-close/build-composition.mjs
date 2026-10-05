import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const P = path.dirname(new URL(import.meta.url).pathname);
const read = name => JSON.parse(fs.readFileSync(path.join(P, name), 'utf8'));
const write = (name, value) => fs.writeFileSync(path.join(P, name), typeof value === 'string' ? value : JSON.stringify(value, null, 2) + '\n');
const duration = name => Number(execFileSync('ffprobe', ['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',path.join(P,name)], {encoding:'utf8'}));
const plan = read('01_script/scene-plan.json');
const words = read('03_sync/captions.words.json').words;
const total = duration('04_composition/assets/audio/voice.wav');
const voice = duration('02_audio/working/voice.wav');
if (Math.abs(total - voice - 4) > .05) throw new Error('BGM outro is not four seconds');
let offset = 0;
const shots = [];
const choices = {s02:['shot-02','shot-03','shot-04'],s06:['shot-06','shot-05'],s09:['shot-09'],s13:['shot-13','shot-07'],s25:['shot-25']};
for (const scene of plan.scenes) {
  const count = scene.narration_text.trim().split(/\s+/).length;
  const actual = words.slice(offset,offset+count).map(w=>w.text).join(' ');
  if (actual !== scene.narration_text.trim().split(/\s+/).join(' ')) throw new Error('Narration mismatch at '+scene.id);
  offset += count;
  const end = scene.id === 's31' ? total : scene.end_seconds;
  const visuals = choices[scene.id] || [`shot-${scene.id.slice(1)}`];
  const span = end - scene.start_seconds;
  if(scene.id==='s23'){
    const aligned=words.slice(offset-count,offset);
    const put=aligned.find(w=>w.text==='넣었습니다.');
    if(!put)throw new Error('Missing phone placement timing');
    const cut=put.start-.35;
    const zones=[{start:scene.start_seconds,end:cut,visual:'shot-22'},{start:cut,end,visual:'shot-23'}];
    let j=0;
    for(const z of zones){const n=Math.max(1,Math.ceil((z.end-z.start)/4.5));for(let k=0;k<n;k++,j++)shots.push({id:`${scene.id}-${j}`,scene:scene.id,visual:z.visual,crop:j%3,start:z.start+(z.end-z.start)*k/n,end:z.start+(z.end-z.start)*(k+1)/n});}
    continue;
  }
  // Change framing every few seconds; longer scenes alternate approved views of the same place.
  const parts = Math.max(1,Math.ceil(span/4.5));
  for(let j=0;j<parts;j++){
    shots.push({id:`${scene.id}-${j}`,scene:scene.id,visual:visuals[Math.floor(j*visuals.length/parts)],crop:j%3,start:scene.start_seconds+span*j/parts,end:scene.start_seconds+span*(j+1)/parts});
  }
}
if (offset!==words.length) throw new Error('Unmapped aligned words');
for (const s of shots) if (!fs.existsSync(path.join(P,'04_composition/assets/visuals',s.visual+'.png'))) throw new Error('Missing approved image '+s.visual);
plan.scenes.at(-1).end_seconds=total;
plan.scenes.at(-1).duration_seconds=total-plan.scenes.at(-1).start_seconds;
plan.scenes.at(-1).end_screen_safe_start_seconds=total-18;
plan.duration_seconds=total;
plan.voice_duration_seconds=voice;
plan.outro_seconds=total-voice;
plan.status='timed_to_reviewed_voice_and_delegated_bgm_selection';
write('01_script/scene-plan.json',plan);
write('04_composition/scene-data.json',{duration:total,voice_duration:voice,shots});

function html(items,length,{silent=false,endScreen=null}={}) {
 const focused=items.some(s=>s.scene==='s29'||s.scene==='s30');
 return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>볼풀 마감: 돌아오는 공</title><style>
@font-face{font-family:'Apple SD Gothic Neo';src:local('Apple SD Gothic Neo')}*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#071117}#master{position:relative;width:1920px;height:1080px;overflow:hidden}.shot{position:absolute;inset:0;display:none;overflow:hidden}.photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform,filter}.shade{position:absolute;inset:0;pointer-events:none;background:linear-gradient(0deg,#02060944,transparent 35%,#02060918)}.light{position:absolute;inset:-12%;pointer-events:none;background:linear-gradient(110deg,transparent 23%,#a9dee514 51%,transparent 76%)}.imprints{position:absolute;inset:0;pointer-events:none}.imprints i{position:absolute;top:46%;width:2.3%;height:23%;border-radius:55%;transform:rotate(22deg);background:linear-gradient(90deg,#213b4155 0%,#030b10bc 33%,#030b10d1 63%,#2d46545a 100%);box-shadow:inset 2px 0 7px #a2b5bd36,3px 4px 9px #0105077a;filter:blur(3px)}.imprints i:nth-child(1){left:42%}.imprints i:nth-child(2){left:47.2%}.imprints i:nth-child(3){left:52.4%}.imprints i:nth-child(4){left:57.6%}.monitor-frame{position:absolute;inset:35px;border:12px solid #142027;box-shadow:0 0 0 35px #050b0e;pointer-events:none}.monitor-label{position:absolute;top:58px;left:66px;color:#e2eeee;font:28px "Apple SD Gothic Neo",sans-serif;letter-spacing:2px}.monitor-label:before{content:"";display:inline-block;width:12px;height:12px;background:#bd4c46;border-radius:50%;margin-right:14px}.recording{position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,#10202218 0,#10202218 1px,transparent 1px,transparent 5px)}.end-safe{position:absolute;right:0;top:0;width:860px;height:1080px;background:linear-gradient(90deg,transparent,#05090abb);opacity:0}.end-label{position:absolute;left:80px;bottom:75px;color:#e2e7ea;font:30px 'Apple SD Gothic Neo',sans-serif;opacity:0}.counter{position:absolute;left:60px;top:65px;color:#e8ecf0;font:44px 'Apple SD Gothic Neo',sans-serif;text-shadow:0 4px 20px #000;opacity:0}
</style></head><body><main id="master" data-composition-id="youtube-master" data-width="1920" data-height="1080" data-fps="60" data-start="0" data-duration="${length}">
${silent?'':`<audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="${length}" data-track-index="0" data-volume="1"></audio>`}
${items.map(s=>`<section class="shot" id="${s.id}"><img id="${s.id}-photo" class="photo clip" src="assets/visuals/${s.visual}.png" data-start="${s.start}" data-duration="${s.end-s.start}" alt=""><div class="shade"></div><div class="light"></div>${["s29","s30"].includes(s.scene)?'<div class="recording"></div><div class="monitor-frame"></div><div class="monitor-label">녹화 영상</div>':''}</section>`).join('')}
<div class="counter"></div><div class="end-safe"></div><div class="end-label">다음 공포 이야기는 관련 영상에서</div></main><script src="assets/gsap.min.js"></script><script>
const DATA=${JSON.stringify(items)},D=${length};window.__timelines={};const tl=gsap.timeline({paused:true});
DATA.forEach((s,i)=>{const el=document.getElementById(s.id),img=el.querySelector('.photo'),light=el.querySelector('.light'),imp=el.querySelector('.imprints'),d=s.end-s.start,side=i%2?1:-1,${focused?"focus=(s.scene==='s29'||s.scene==='s30')&&!s.id.endsWith('-0'),base=focus?3.2:[1.045,1.19,1.10][s.crop||0],dx=focus?(s.scene==='s29'?90:-25):0,dy=focus?(s.scene==='s29'?30:90):0":"base=[1.045,1.19,1.10][s.crop||0]"};tl.set(el,{display:'block'},s.start);tl.fromTo(img,{scale:base,xPercent:${focused?"dx-side*1.1":"-side*1.1"},yPercent:${focused?"dy-.3":"-.3"},filter:'brightness(1.04)'},{scale:base+.065,xPercent:${focused?"dx+side*1.1":"side*1.1"},yPercent:${focused?"dy+.4":".4"},filter:'brightness(.96)',duration:d,ease:'none'},s.start);if(imp)tl.fromTo(imp,{scale:1.04,xPercent:-side*1.4,yPercent:-.3},{scale:1.13,xPercent:side*1.4,yPercent:.4,duration:d,ease:'none'},s.start);tl.fromTo(light,{xPercent:-5,opacity:.13},{xPercent:7,opacity:.46,duration:d,ease:'none'},s.start);for(let t=s.start+1.3;t<s.end-.2;t+=2.3)tl.to(light,{opacity:Math.round(t)%2?.1:.47,duration:Math.min(.5,s.end-t)},t);tl.set(el,{display:'none'},s.end)});
${endScreen===null||endScreen>=length?'':`tl.to('.end-safe',{opacity:1,duration:.5},${Math.max(0,endScreen)});tl.to('.end-label',{opacity:1,duration:.5},${Math.max(0,length-4)});`}
tl.to({},{duration:D},0);window.__timelines['youtube-master']=tl;tl.seek(.000001,false);gsap.set(document.getElementById(DATA[0].id),{display:'block'});
</script></body></html>`;
}
write('04_composition/index.html',html(shots,total,{endScreen:total-18}));
const dir=path.join(P,'04_composition/segments');fs.mkdirSync(dir,{recursive:true});
if(!fs.existsSync(path.join(dir,'assets')))fs.symlinkSync('../assets',path.join(dir,'assets'));
const segments=plan.scenes.map((scene,i)=>{
 const startFrame=Math.round(scene.start_seconds*60);
 const endFrame=i===plan.scenes.length-1?Math.ceil(total*60):Math.round(plan.scenes[i+1].start_seconds*60);
 const start=startFrame/60,length=(endFrame-startFrame)/60;
 const local=shots.filter(s=>s.end>start+.01&&s.start<start+length-.01).map(s=>({...s,start:Math.max(0,s.start-start),end:Math.min(length,s.end-start)}));
 if(!local.length)throw new Error('Empty segment '+scene.id);
 local[0].start=0;local.at(-1).end=length;
 const filename=`segments/part-${String(i+1).padStart(2,'0')}.html`;
 write('04_composition/'+filename,html(local,length,{silent:true,endScreen:total-18-start}));
 return {filename,startFrame,endFrame,duration:length};
});
write('04_composition/render-segments.json',segments);
console.log(JSON.stringify({voice,total,shots:shots.length,segments:segments.length}));
