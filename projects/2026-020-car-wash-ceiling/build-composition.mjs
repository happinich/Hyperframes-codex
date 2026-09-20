import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const P=path.dirname(new URL(import.meta.url).pathname);
const read=n=>JSON.parse(fs.readFileSync(path.join(P,n),'utf8'));
const put=(n,v)=>fs.writeFileSync(path.join(P,n),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');
const probe=n=>Number(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',path.join(P,n)],{encoding:'utf8'}));
const words=read('03_sync/captions.words.json').words;
const plan=read('01_script/scene-plan.json');
const duration=probe('02_audio/working/voice.wav')+4;
const groups=[[1,2],[3,4,5,6],[7,8],[9,10],[11,12],[13,14],[15,16],[17,18],[19,20],[21,22],[23,24],[25,26],[27,28],[29,30],[31,32],[33,34],[35,36],[37,38],[39,40],[41,42,43,44],[45,46],[47],[47,48]];
const triggers=[['전화기에서'],['친구가 빌려준','마지막 손님이','그런데 아무도'],['떨어지는 물은'],['그제야 손을'],['모니터에는'],['저는 사무실 유리창을'],['사무실 안이라고'],['저는 그 말을'],['문 밑으로'],['관리인 아저씨가 옆문이'],['잠금 버튼을'],['앞유리 맨'],['앞유리의 손은'],['그런데 바로'],['저는 그보다'],['아저씨가 손잡이'],['젖은 손가락'],['작업등은'],['저는 차를 다시'],['작업등과','그 모습에','아저씨가 차를'],['아저씨 손목에는'],[],['실내등 덮개가']];
let offset=0;const shots=[];
for(const [i,s]of plan.scenes.entries()){
 const ws=s.narration_text.split(/\s+/);s.word_offset=offset;s.word_count=ws.length;
 if(ws.join(' ')!==words.slice(offset,offset+ws.length).map(w=>w.text).join(' '))throw Error('Source mismatch '+s.id);
 s.start_seconds=i?Math.max(0,words[offset].start-.25):0;s.speech_start=words[offset].start;s.speech_end=words[offset+ws.length-1].end;
 const cue=phrase=>{const x=s.narration_text.indexOf(phrase);if(x<0)throw Error('Missing '+phrase);const n=s.narration_text.slice(0,x).trim().split(/\s+/).filter(Boolean).length;return Math.max(s.start_seconds,words[offset+n].start-.25);};
 s.motion_beats=groups[i].map((n,j)=>{const t=j?cue(triggers[i][j-1]):s.start_seconds;shots.push({id:s.id+'-shot-'+String(n).padStart(2,'0'),visual:'shot-'+String(n).padStart(2,'0'),start:t,trigger:j?triggers[i][j-1]:s.purpose});return {time:t,action:'reveal shot-'+n,spoken_trigger:j?triggers[i][j-1]:s.purpose};});
 offset+=ws.length;
}
if(offset!==words.length)throw Error('Unmapped words');
shots.forEach((s,i)=>s.end=shots[i+1]?.start??duration);
plan.scenes.forEach((s,i)=>{s.end_seconds=plan.scenes[i+1]?.start_seconds??duration;s.duration_seconds=s.end_seconds-s.start_seconds;});
plan.duration_seconds=duration;plan.voice_duration_seconds=duration-4;plan.outro_seconds=4;plan.timing_source='mlx-community/whisper-large-v3-turbo aligned to final voice';plan.master_format={width:1920,height:1080,fps:60};
put('01_script/scene-plan.json',plan);put('04_composition/scene-data.json',{duration,shots});
const escape=t=>t.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
function html(items,total,{short=false,silent=false,endScreen=total-18,captions=[]}={}){
 const W=short?1080:1920,H=short?1920:1080;
 return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>세차장 천장의 여자${short?' · 쇼츠':''}</title><style>
*{box-sizing:border-box}html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#081013;color:#f5f3ed;font-family:'Apple SD Gothic Neo',sans-serif}#master{position:relative;width:${W}px;height:${H}px;overflow:hidden}.shot{position:absolute;inset:0;display:none;overflow:hidden}.photo{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;will-change:transform}.light{position:absolute;inset:-20%;background:linear-gradient(110deg,transparent 22%,#bfe8e413 48%,transparent 70%);pointer-events:none}.shade{position:absolute;inset:0;background:linear-gradient(0deg,#02080855,transparent 38%,#02080822);pointer-events:none}.end-safe{position:absolute;right:0;top:0;width:900px;height:1080px;background:linear-gradient(90deg,transparent,#05090ad9);opacity:0}.end-label{position:absolute;right:165px;bottom:110px;font-size:28px;color:#ccd1cb;opacity:0}.captions{position:absolute;left:75px;right:155px;bottom:355px;font-size:55px;font-weight:800;line-height:1.35;text-align:center;word-break:keep-all;-webkit-text-stroke:7px #050708;paint-order:stroke fill}.caption{position:absolute;left:0;right:0;bottom:0;opacity:0}.short-hook{position:absolute;left:75px;right:150px;top:190px;font-size:66px;font-weight:900;line-height:1.25;text-shadow:0 4px 15px #000}.short-cta{position:absolute;left:80px;right:150px;bottom:230px;font-size:31px;text-align:center;opacity:0}.short-frame{position:absolute;left:55px;right:140px;top:380px;bottom:510px;border:2px solid #c7b6a85c;pointer-events:none}
@font-face{font-family:'Apple SD Gothic Neo';src:local('Apple SD Gothic Neo')}.shade{background:linear-gradient(0deg,#02080855,transparent 38%,#02080822)}
</style></head><body><main id="master" data-composition-id="${short?'shorts':'youtube'}-master" data-width="${W}" data-height="${H}" data-fps="60" data-start="0" data-duration="${total}">
${silent?'':`<audio id="voice" src="assets/audio/${short?'shorts-mix':'voice'}.wav" data-start="0" data-duration="${total}" data-track-index="0" data-volume="1"></audio>`}
${items.map(s=>`<section class="shot" id="${s.id}"><img class="photo clip" id="${s.id}-photo" src="assets/visuals/${s.visual}.png" data-start="${s.start}" data-duration="${s.end-s.start}" alt=""><div class="shade"></div><div class="light"></div></section>`).join('')}
${short?`<div class="short-hook">천장에서<br>머리카락이 내려왔다</div><div class="captions">${captions.map((c,i)=>`<div class="caption" id="cap-${i}">${escape(c.text)}</div>`).join('')}</div><div class="short-cta">고개를 들면 어떻게 될까<br>아래 관련 동영상에서</div>`:'<div class="end-safe"></div><div class="end-label">다음 이야기는 계속됩니다</div>'}
</main><script src="assets/gsap.min.js"></script><script>
const DATA=${JSON.stringify(items)},D=${total};window.__timelines={};const tl=gsap.timeline({paused:true});
DATA.forEach((s,i)=>{const el=document.getElementById(s.id),img=el.querySelector('.photo'),light=el.querySelector('.light'),d=s.end-s.start,side=i%2?1:-1;tl.set(el,{display:'block'},s.start);tl.fromTo(img,{scale:1.075,xPercent:-side*1.5,yPercent:-.6},{scale:1.16,xPercent:side*1.5,yPercent:.6,duration:d,ease:'none'},s.start);tl.set(img,{filter:'brightness(1.1)'},s.start);tl.fromTo(light,{xPercent:-7,opacity:.25},{xPercent:9,opacity:.6,duration:d,ease:'none'},s.start);for(let t=s.start+1.2;t<s.end-.3;t+=2.4){tl.to(light,{opacity:Math.floor(t)%2?.18:.65,duration:Math.min(.7,s.end-t),ease:'sine.inOut'},t);}tl.set(el,{display:'none'},s.end);});
${short?`const caps=${JSON.stringify(captions)};caps.forEach((c,i)=>{tl.set('#cap-'+i,{opacity:1},c.start);tl.set('#cap-'+i,{opacity:0},c.end);});tl.to('.short-hook',{opacity:0,duration:.2},3.7);tl.to('.short-cta',{opacity:1,duration:.3},D-4);`:`${endScreen<total?`tl.to('.end-safe',{opacity:1,duration:.5},${Math.max(0,endScreen)});tl.to('.end-label',{opacity:1,duration:.5},${Math.max(0,total-4)});`:''}`}
tl.to({},{duration:D},0);window.__timelines['${short?'shorts':'youtube'}-master']=tl;tl.seek(.000001,false);gsap.set(document.getElementById(DATA[0].id),{display:'block'});
</script></body></html>`;
}
put('04_composition/index.html',html(shots,duration));
fs.mkdirSync(path.join(P,'04_composition/segments'),{recursive:true});
if(!fs.existsSync(path.join(P,'04_composition/segments/assets')))fs.symlinkSync('../assets',path.join(P,'04_composition/segments/assets'));
const segments=plan.scenes.map((s,i)=>{const startFrame=Math.round(s.start_seconds*60),endFrame=i===plan.scenes.length-1?Math.ceil(duration*60):Math.round(s.end_seconds*60);const start=startFrame/60,total=(endFrame-startFrame)/60;const local=shots.filter(x=>x.end>start+.02&&x.start<endFrame/60-.02).map(x=>({...x,start:Math.max(0,x.start-start),end:Math.min(total,x.end-start)}));local[0].start=0;local.at(-1).end=total;const filename='segments/part-'+String(i+1).padStart(2,'0')+'.html';put('04_composition/'+filename,html(local,total,{silent:true,endScreen:duration-18-start}));return {filename,startFrame,endFrame,duration:total};});
put('04_composition/render-segments.json',segments);
if(fs.existsSync(path.join(P,'03_sync/shorts-captions.words.json'))){
const sw=read('03_sync/shorts-captions.words.json').words;const paras=fs.readFileSync(path.join(P,'01_script/shorts-narration.txt'),'utf8').trim().split(/\n\s*\n/);let wi=0;const pics=['short-new-01','short-new-02','short-new-03','short-new-04','short-new-05','short-new-06'];const sd=probe('04_composition/assets/audio/shorts-voice.wav')+4;
if(paras.length!==pics.length)throw Error('Short requires six independently scripted image beats');
const items=paras.map((p,i)=>{const start=i?Math.max(0,sw[wi].start-.15):0;wi+=p.split(/\s+/).length;return {id:'short-'+i,start,visual:pics[i]};});items.forEach((s,i)=>s.end=items[i+1]?.start??sd);
const captions=[];let b=[];const flush=()=>{if(b.length)captions.push({start:b[0].start,end:b.at(-1).end,text:b.map(w=>w.text).join(' ')});b=[];};for(const w of sw){if(b.length&&(b.map(x=>x.text).join(' ').length+w.text.length>23||w.start-b.at(-1).end>.3))flush();b.push(w);if(/[.!?]$/.test(w.text))flush();}flush();
fs.mkdirSync(path.join(P,'04_composition/variants'),{recursive:true});if(!fs.existsSync(path.join(P,'04_composition/variants/assets')))fs.symlinkSync('../assets',path.join(P,'04_composition/variants/assets'));put('04_composition/variants/shorts.html',html(items,sd,{short:true,captions}));put('01_script/shorts-scene-plan.json',{duration:sd,fps:60,voice_multiplier:1.07,spoiler_free:true,shots:items,captions});
}
console.log({duration,images:shots.length,segments:segments.length});
