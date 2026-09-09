import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import sharp from 'sharp';

const P=path.dirname(new URL(import.meta.url).pathname);
const read=p=>JSON.parse(fs.readFileSync(path.join(P,p),'utf8'));
const write=(p,v)=>fs.writeFileSync(path.join(P,p),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const probe=p=>Number(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',path.join(P,p)],{encoding:'utf8'}));
const words=read('03_sync/captions.words.json').words;
const narration=fs.readFileSync(path.join(P,'01_script/narration.txt'),'utf8').trim();
const normalized=s=>s.replace(/\s+/g,' ').trim();
if(normalized(words.map(w=>w.text).join(' '))!==normalized(narration))throw Error('Caption source mismatch');
const duration=probe('02_audio/working/voice.wav')+4;
const plan=read('01_script/scene-plan.json');
let wordOffset=0;
for(const s of plan.scenes){
 const n=s.narration_text.split(/\s+/).length;
 s.word_offset=wordOffset;s.word_count=n;
 s.start_seconds=wordOffset?Math.max(0,words[wordOffset].start-.35):0;
 s.speech_start=words[wordOffset].start;
 s.speech_end=words[wordOffset+n-1].end;
 wordOffset+=n;
}
if(wordOffset!==words.length)throw Error('Scene text does not cover narration');
const cue=(s,phrase)=>{
 const i=s.narration_text.indexOf(phrase);if(i<0)throw Error(`Missing cue ${s.id}: ${phrase}`);
 const n=s.narration_text.slice(0,i).trim().split(/\s+/).filter(Boolean).length;
 return Math.max(s.start_seconds,words[s.word_offset+n].start-.22);
};
const shot=(s,visual,phrase=null,overlay='none')=>({start:phrase?cue(s,phrase):s.start_seconds,visual,overlay,trigger:phrase||s.purpose});
let shots=[];
for(const [i,s] of plan.scenes.entries()){
 s.end_seconds=plan.scenes[i+1]?.start_seconds??duration;
 s.duration_seconds=s.end_seconds-s.start_seconds;
 let a=[];
 switch(s.id){
 case 'S01':a=[shot(s,'wall',null,'hook')];break;
 case 'S02':a=[shot(s,'room'),shot(s,'room','집은 거실과','normal-map'),shot(s,'room','로봇청소기는'),shot(s,'room','앱에 연결하니','normal-map')];break;
 case 'S03':a=[shot(s,'room',null,'notice'),shot(s,'room','잠에서 깨서','extra-map'),shot(s,'room','그런데 로봇청소기가'),shot(s,'debris','기계를 들어'),shot(s,'debris','그때까지만'),shot(s,'room','저는 청소기를','normal-map')];break;
 case 'S04':a=[shot(s,'room',null,'notice'),shot(s,'room','이번에는','extra-map'),shot(s,'room','“안쪽 방.”','named-map'),shot(s,'room','고객센터에','history'),shot(s,'room','상담원은 기기를')];break;
 case 'S05':a=[shot(s,'cabinet'),shot(s,'closed','문까지'),shot(s,'closed','새벽 두 시'),shot(s,'closed','잠긴 문'),shot(s,'room','거실 벽 아래'),shot(s,'closed','마치 벽')];break;
 case 'S06':a=[shot(s,'room',null,'blueprint-now'),shot(s,'room','그런데 누렇게','blueprint-old'),shot(s,'room','그 방 위에는','blueprint-cross'),shot(s,'room','관리인은 도면'),shot(s,'closed','“그 기계'),shot(s,'closed','그리고 무슨 일이','warning')];break;
 case 'S07':a=[shot(s,'room'),shot(s,'tracks','벽 앞에'),shot(s,'closed','수납장에서'),shot(s,'room','친구가')];break;
 case 'S08':a=[shot(s,'tracks'),shot(s,'tracks','센서가'),shot(s,'room','그런데 청소기는'),shot(s,'tracks','자국은'),shot(s,'tracks','벽 쪽에서')];break;
 case 'S09':a=[shot(s,'tracks'),shot(s,'wall','그런데 앞 범퍼가'),shot(s,'wall','기계 앞부분이'),shot(s,'wall','지도에는','stuck-map'),shot(s,'wall','뭐에 걸렸는지만','connecting')];break;
 case 'S10':a=[shot(s,'passage',null,'camera'),shot(s,'entity','그런데 거기서','camera'),shot(s,'entity','사람 하나가','camera')];break;
 case 'S11':a=[shot(s,'hand'),shot(s,'hand','손가락 관절은'),shot(s,'wall','저는 손목을'),shot(s,'wall','그러자 로봇청소기에서'),shot(s,'wall','“안쪽 방으로','returning')];break;
 case 'S12':a=[shot(s,'entity'),shot(s,'entity','얼굴에는')];break;
 case 'S13':a=[shot(s,'stairs'),shot(s,'stairs','등 뒤에서는')];break;
 case 'S14':a=[shot(s,'evidence'),shot(s,'evidence','대신 콘크리트'),shot(s,'evidence','청소기는')];break;
 case 'S15':a=[shot(s,'bedroom'),shot(s,'bedroom','이제 끝났다고')];break;
 case 'S16':a=[shot(s,'bedroom'),shot(s,'bedroom','분명히 삭제한','notice'),shot(s,'bedroom','알림을 누르자','bed-map'),shot(s,'bedroom','침대 옆 벽','bed-map'),shot(s,'bedroom','그리고 그 방 안에서','entity-map')];break;
 case 'S17':a=[shot(s,'bedroom',null,'entity-map'),shot(s,'bedroom','앱 지도','cross-map'),shot(s,'bedroom','그리고 제가','on-bed')];break;
 }
 a.sort((x,y)=>x.start-y.start);
 s.visual=a[0].visual;s.motion_beats=a.map(x=>({time:x.start,action:x.overlay==='none'?`camera refocus: ${x.visual}`:x.overlay,spoken_trigger:x.trigger}));
 s.audio.intentional_silences=[];
 shots.push(...a);
}
shots.forEach((s,i)=>{s.end=shots[i+1]?.start??duration;s.id=`shot-${i}`;});
plan.master_format={width:1920,height:1080,fps:60,aspect_ratio:'16:9'};
plan.shorts_format={width:1080,height:1920,fps:60,aspect_ratio:'9:16'};
plan.duration_seconds=duration;plan.timing_source='final trimmed voice / mlx-community/whisper-large-v3-turbo';
plan.voice_duration_seconds=duration-4;plan.outro_seconds=4;
write('01_script/scene-plan.json',plan);
write('04_composition/scene-data.json',{duration,shots});

function diagram(mode){
 const bed=/bed|entity|cross|on-bed/.test(mode);
 const normal=mode==='normal-map'||mode==='blueprint-now';
 const blueprint=mode.startsWith('blueprint');
 const person=/entity-map|cross-map|on-bed/.test(mode);
 return `<div class="map-panel ${blueprint?'paper':''} ${bed?'bed-map':''}"><div class="map-label">${blueprint?'거실 평면도':bed?'현재 공간':'청소 지도'}</div><svg viewBox="0 0 800 520" aria-label="이야기 속 가상 평면도">
 <g fill="${blueprint?'#cfc6ae':'#16313c'}" stroke="${blueprint?'#414640':'#95b5bf'}" stroke-width="5"><path d="M75 70H580V440H75Z"/>${bed?'<path d="M75 200H190V70" fill="none"/>':'<path d="M75 250H265V440M265 70V185M390 70V185H580" fill="none"/>'}</g>
 <text x="285" y="300" class="map-text">${bed?'침실':'거실'}</text>
 ${bed?'<rect x="330" y="325" width="150" height="86" rx="8" fill="#52666b" stroke="#d4e2e4" stroke-width="4"/><path d="M340 344h130" stroke="#d4e2e4" stroke-width="3"/>':''}
 ${normal?'':`<g class="extra"><rect x="585" y="95" width="132" height="300" fill="#5c1d25" stroke="#ff5965" stroke-width="5"/><text x="650" y="236" text-anchor="middle" class="map-text small">${mode==='extra-map'?'새 공간':blueprint?'수납실':'안쪽 방'}</text></g>`}
 ${blueprint?'':`<path class="route" d="M190 350L190 310L515 310L515 170${normal?'':'L652 170L652 335'}" fill="none" stroke="#9de5d1" stroke-width="5" stroke-dasharray="12 9"/>`}
 ${person?`<g class="person" transform="translate(${mode==='on-bed'?405:650},${mode==='on-bed'?355:320})"><circle cy="-12" r="11" fill="#ff354e"/><path d="M-11 5h22l6 27h-34Z" fill="#ff354e"/></g>`:''}
 ${mode==='blueprint-cross'?'<path class="cross" d="M590 110L710 380M710 110L590 380" stroke="#b62527" stroke-width="14"/>':''}
 </svg><div class="map-footer">${mode==='history'?'안쪽 방 · 이동 기록 7분 이상':mode==='stuck-map'?'정지 요청 · 응답 없음':blueprint?'이야기 재구성 도면':'공간 탐색 중'}</div></div>`;
}
function overlay(s){
 if(s.overlay.includes('map')||s.overlay.startsWith('blueprint')||s.overlay==='history'||s.overlay==='on-bed')return diagram(s.overlay);
 const messages={hook:'벽 속으로<br>사라졌어요.',notice:'새로운 공간을<br>발견했습니다.',warning:'카메라는<br><em>켜지 마요.</em>',connecting:'실시간 카메라<br><em>연결 중</em>',returning:'안쪽 방으로<br>돌아갑니다.'};
 if(messages[s.overlay])return `<div class="statement ${s.overlay}">${messages[s.overlay]}</div>`;
 if(s.overlay==='camera')return '<div class="camera-frame"><span>실시간 카메라</span><i></i></div>';
 return '';
}
const styles=`*{box-sizing:border-box}html,body{margin:0;background:#06090c;color:#f4f5f5;font-family:"Apple SD Gothic Neo",Arial,sans-serif;width:1920px;height:1080px;overflow:hidden}#master{position:relative;width:1920px;height:1080px;overflow:hidden}.shot{position:absolute;inset:0;visibility:hidden;overflow:hidden}.photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform}.shade{position:absolute;inset:0;background:linear-gradient(0deg,#0007,transparent 35%,#0001);pointer-events:none}.light{position:absolute;inset:-20%;background:linear-gradient(110deg,transparent 15%,#b5e2da15 45%,transparent 65%);pointer-events:none}.statement{position:absolute;left:120px;top:145px;font-size:70px;font-weight:800;line-height:1.25;letter-spacing:-.035em;text-shadow:0 4px 24px #000;word-break:keep-all}.statement.hook{font-size:76px;top:180px}.statement.notice{font-size:42px;top:100px;left:105px;border-left:4px solid #ff4c5b;padding:18px 24px;background:#060b11cc}.statement.warning,.statement.connecting,.statement.returning{top:360px;left:140px}em{color:#ff5a68;font-style:normal}.map-panel{position:absolute;left:130px;top:155px;width:860px;padding:32px;border:2px solid #54717b;border-radius:28px;background:#07131bef;box-shadow:0 30px 90px #0008}.map-label{font-size:30px;font-weight:700;letter-spacing:.05em}.map-panel svg{width:100%;height:510px}.map-text{fill:#e6eeee;font-size:30px;font-weight:700}.map-text.small{font-size:23px}.map-footer{font-size:24px;color:#9caeb8}.paper{background:#dfd5bd;color:#373d39;transform:rotate(-2deg)}.paper .map-text{fill:#333e36}.paper .map-footer{color:#64665a}.bed-map{left:80px;top:160px;width:820px}.camera-frame{position:absolute;inset:70px;border:2px solid #ffffff66}.camera-frame span{position:absolute;top:25px;left:30px;font-size:26px;color:#e9f1f2}.camera-frame i{position:absolute;top:29px;right:30px;width:14px;height:14px;background:#ed4960;border-radius:50%}.scan{position:absolute;left:0;right:0;top:-80px;height:70px;background:linear-gradient(transparent,#cdf8f809,transparent);opacity:0}.end-safe{position:absolute;top:0;right:0;width:930px;height:1080px;background:linear-gradient(90deg,transparent,#05090ce0);opacity:0;pointer-events:none}.end-label{position:absolute;right:180px;bottom:120px;font-size:26px;color:#bac5ca;opacity:0;letter-spacing:.1em}`;
function html({short=false,items,total,captions=[],silent=false,endScreenStart=total-18,endLabelStart=total-4}){
 const W=short?1080:1920,H=short?1920:1080,assets='assets/';
 const extra=short?`html,body,#master{width:1080px;height:1920px}.photo{object-fit:cover}.statement{left:80px;right:140px;top:240px;font-size:72px}.statement.hook{top:220px;font-size:80px}.statement.warning,.statement.connecting{top:260px;left:80px}.statement.notice{left:80px;top:250px;font-size:46px}.map-panel{left:65px;top:370px;width:890px}.captions{position:absolute;left:78px;right:155px;bottom:385px;text-align:center;z-index:8;font-size:56px;font-weight:800;line-height:1.3;word-break:keep-all;-webkit-text-stroke:7px #08090b;paint-order:stroke fill;text-shadow:0 4px 12px #000}.caption{position:absolute;left:0;right:0;bottom:0;opacity:0}.short-cta{position:absolute;left:80px;right:160px;bottom:225px;font-size:34px;line-height:1.3;opacity:0;text-align:center;color:#e5eeee}.camera-frame{inset:170px 75px 400px}`:'';
 return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>로봇청소기 지도에 우리 집에 없는 방이 생겼다${short?' · 쇼츠':''}</title><style>${styles}${extra}@font-face{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}.shot{display:none}</style></head><body><main id="master" data-composition-id="${short?'shorts-master':'youtube-master'}" data-width="${W}" data-height="${H}" data-fps="60" data-start="0" data-duration="${total}">${silent?'':`<audio id="voice" data-start="0" data-duration="${total}" data-track-index="0" src="${assets}audio/${short?'shorts-mix':'voice'}.wav" data-volume="1"></audio>`}${items.map(s=>`<section id="${s.id}" class="shot"><img class="photo clip" id="${s.id}-photo" data-start="${s.start}" data-duration="${s.end-s.start}" src="${assets}visuals/${s.visual}.png" alt=""><div class="shade"></div><div class="light"></div>${overlay(s)}<div class="scan"></div></section>`).join('')}${short?`<div class="captions">${captions.map((c,i)=>`<div class="caption" id="cap-${i}">${esc(c.text)}</div>`).join('')}</div><div class="short-cta">카메라에 찍힌 것은<br>아래 관련 동영상에서</div>`:'<div class="end-safe"></div><div class="end-label">다음 이야기는 계속됩니다</div>'}</main><script src="${assets}gsap.min.js"></script><script>
const DATA=${JSON.stringify(items)},DURATION=${total},SHORT=${short};
window.__timelines={};const tl=gsap.timeline({paused:true});
DATA.forEach((s,i)=>{
 const el=document.getElementById(s.id),img=el.querySelector('.photo'),d=s.end-s.start;
 const side=i%2?1:-1;
 tl.set(el,{display:'block',visibility:'visible',opacity:1},s.start);
 tl.fromTo(img,{scale:1.07,xPercent:-side*1.2,yPercent:0},{scale:1.16,xPercent:side*1.4,yPercent:i%3-1,duration:d,ease:'none'},s.start);
 const dim=s.overlay.includes('map')||s.overlay.startsWith('blueprint')||s.overlay==='history';
 tl.set(img,{filter:dim?'brightness(.56)':'brightness(1.12)'},s.start);
 tl.fromTo(el.querySelector('.light'),{xPercent:-4,opacity:.35},{xPercent:6,opacity:.7,duration:d,ease:'sine.inOut'},s.start);
 for(let t=s.start+1.1;t<s.end-.5;t+=2.4){const span=Math.min(1.2,s.end-t);tl.to(el.querySelector('.light'),{opacity:((i+Math.floor(t))%2)?.25:.7,duration:span,ease:'sine.inOut'},t);}
 const map=el.querySelector('.map-panel');if(map){tl.fromTo(map,{opacity:0,y:12},{opacity:1,y:0,duration:Math.min(.25,d),ease:'power1.out'},s.start);const route=el.querySelector('.route');if(route)tl.fromTo(route,{strokeDashoffset:100},{strokeDashoffset:-80,duration:d,ease:'none'},s.start);const ex=el.querySelector('.extra');if(ex)tl.fromTo(ex,{opacity:.45},{opacity:1,duration:Math.min(1.1,d),ease:'none'},s.start);}
 const person=el.querySelector('.person');if(person&&s.overlay==='cross-map')tl.fromTo(person,{x:620,y:320},{x:405,y:355,duration:Math.max(.1,d-.1),ease:'none'},s.start);
 if(person&&s.overlay==='entity-map')tl.fromTo(person,{x:650,y:320},{x:620,y:320,duration:d,ease:'none'},s.start);
 const c=el.querySelector('.camera-frame');if(c){for(let t=s.start+.5;t<s.end-.5;t+=2.5)tl.fromTo(el.querySelector('.scan'),{opacity:0,y:0},{opacity:.8,y:SHORT?1900:1160,duration:Math.min(1,s.end-t),ease:'none'},t);}
 tl.set(el,{display:'none',visibility:'hidden',opacity:0},s.end);
});
${short?`const CAPS=${JSON.stringify(captions)};CAPS.forEach((c,i)=>{tl.set('#cap-'+i,{opacity:1},c.start);tl.set('#cap-'+i,{opacity:0},c.end)});tl.to('.short-cta',{opacity:1,duration:.3},DURATION-4);`:`${endScreenStart<total?`tl.to(\'.end-safe\',{opacity:1,duration:.4},${Math.max(0,endScreenStart)});`:""}${endLabelStart<total?`tl.to(\'.end-label\',{opacity:1,duration:.5},${Math.max(0,endLabelStart)});`:""}`}
tl.to({},{duration:DURATION},0);${short?'window.__timelines["shorts-master"]=tl;':'window.__timelines["youtube-master"]=tl;'}
tl.seek(.000001,false);gsap.set(document.getElementById(DATA[0].id),{display:'block',visibility:'visible',opacity:1});
</script></body></html>`;
}
write('04_composition/index.html',html({items:shots,total:duration}));
fs.mkdirSync(path.join(P,'04_composition/segments'),{recursive:true});
if(!fs.existsSync(path.join(P,'04_composition/segments/assets')))fs.symlinkSync('../assets',path.join(P,'04_composition/segments/assets'));
const segments=plan.scenes.map((s,i)=>{
 const startFrame=Math.round(s.start_seconds*60),endFrame=i===plan.scenes.length-1?Math.ceil(duration*60):Math.round(s.end_seconds*60);
 const start=startFrame/60,end=endFrame/60,localDuration=(endFrame-startFrame)/60;
 const localShots=shots.filter(x=>x.end>start+.02&&x.start<end-.02).map(x=>({...x,start:Math.max(0,x.start-start),end:Math.min(localDuration,x.end-start)}));
 localShots[0].start=0;localShots.at(-1).end=localDuration;
 const filename=`segments/part-${String(i+1).padStart(2,'0')}.html`;
 write('04_composition/'+filename,html({items:localShots,total:localDuration,silent:true,endScreenStart:duration-18-start,endLabelStart:duration-4-start}));
 return {filename,startFrame,endFrame,duration:localDuration};
});
write('04_composition/render-segments.json',segments);
const sw=read('03_sync/shorts-captions.words.json').words;
const stext=fs.readFileSync(path.join(P,'01_script/shorts-narration.txt'),'utf8').trim();
const paragraphs=stext.split(/\n\n/);let wi=0;
const simages=['short-wall','debris','closed','short-wall','short-camera','short-camera'];
const smodes=['hook','none','warning','none','none','connecting'];
const shortDuration=probe('04_composition/assets/audio/shorts-voice.wav')+4;
const shorts=paragraphs.map((p,i)=>{const n=p.split(/\s+/).length,st=i?Math.max(0,sw[wi].start-.1):0;wi+=n;return {id:'short-'+i,start:st,visual:simages[i],overlay:smodes[i]};});
shorts.forEach((s,i)=>s.end=shorts[i+1]?.start??shortDuration);
const captions=[];let batch=[];
for(const w of sw){
 if(batch.length&&(batch.map(x=>x.text).join(' ').length+w.text.length>23||w.start-batch.at(-1).end>.3)){captions.push({start:batch[0].start,end:batch.at(-1).end,text:batch.map(x=>x.text).join(' ')});batch=[];}
 batch.push(w);if(/[.!?]$/.test(w.text)){captions.push({start:batch[0].start,end:batch.at(-1).end,text:batch.map(x=>x.text).join(' ')});batch=[];}
}
if(batch.length)captions.push({start:batch[0].start,end:batch.at(-1).end,text:batch.map(x=>x.text).join(' ')});
fs.mkdirSync(path.join(P,'04_composition/variants'),{recursive:true});
if(!fs.existsSync(path.join(P,'04_composition/variants/assets')))fs.symlinkSync('../assets',path.join(P,'04_composition/variants/assets'));
write('04_composition/variants/shorts.html',html({short:true,items:shorts,total:shortDuration,captions}));
write('01_script/shorts-scene-plan.json',{duration:shortDuration,fps:60,voice_multiplier:1.07,spoiler_free:true,shots:shorts,captions});
for(const k of ['a','b'])await sharp(path.join(P,`04_composition/assets/visuals/thumbnail-${k}.png`)).resize(1280,720,{fit:'cover'}).jpeg({quality:94}).toFile(path.join(P,`07_publish/youtube/thumbnail-${k}.jpg`));
console.log({duration,shortDuration,shots:shots.length,captions:captions.length});
