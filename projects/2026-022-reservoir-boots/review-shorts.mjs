import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';
const P=path.dirname(new URL(import.meta.url).pathname);
const read=f=>JSON.parse(fs.readFileSync(path.join(P,f)));
const plan=read('01_script/shorts-scene-plan.json'),words=read('03_sync/shorts-captions.words.json').words;
const failures=[],samples=[];
const text=fs.readFileSync(path.join(P,'01_script/shorts-narration.txt'),'utf8').trim().split(/\s+/).join(' ');
if(words.map(w=>w.text).join(' ')!==text)failures.push('Approved caption surface changed');
if(read('03_sync/shorts-sync_report.json').matched_character_ratio<.92)failures.push('Low alignment');
if(plan.duration<15||plan.duration>40||plan.fps!==60)failures.push('Format');
if(!text.endsWith('올라왔어요.'))failures.push('Incomplete cliffhanger');
if(plan.shots[0].start!==0||Math.abs(plan.shots.at(-1).end-plan.duration)>.001)failures.push('Coverage');
for(let i=1;i<plan.shots.length;i++)if(Math.abs(plan.shots[i-1].end-plan.shots[i].start)>.001)failures.push('Scene gap');
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
try{
 const page=await browser.newPage();await page.setViewport({width:1080,height:1920});
 page.on('pageerror',e=>failures.push(e.message));
 await page.goto('file://'+path.join(P,'04_composition/variants/shorts.html'));
 await page.evaluate(async()=>{await document.fonts.ready;for(const im of document.images)await im.decode()});
 for(let t=0;t<plan.duration-.02;t+=.25){
  const sample=await page.evaluate(t=>{
   const timeline=Object.values(window.__timelines)[0];timeline.seek(t,false);
   const shots=[...document.querySelectorAll('.shot')].filter(e=>getComputedStyle(e).display!=='none');
   const caps=[...document.querySelectorAll('.caption')].filter(e=>Number(getComputedStyle(e).opacity)>.9);
   return {shots:shots.map(e=>({id:e.id,transform:getComputedStyle(e.querySelector('.photo')).transform})),caps:caps.map(e=>{const r=e.getBoundingClientRect();return {text:e.textContent,left:r.left,right:r.right,top:r.top,bottom:r.bottom}})};
  },t);
  if(sample.shots.length!==1)failures.push('Visibility '+t);
  if(sample.caps.length>1)failures.push('Caption overlap '+t);
  if(sample.caps.some(c=>c.left<60||c.right>940||c.top<1160||c.bottom>1580))failures.push('Caption unsafe '+t);
  const expected=plan.captions.filter(c=>t>=c.start&&t<c.end);
  if(expected.map(c=>c.text).join('|')!==sample.caps.map(c=>c.text).join('|'))failures.push('Caption timing '+t);
  samples.push({t,...sample});
 }
 for(const shot of plan.shots){
  const slice=samples.filter(s=>s.t>=shot.start&&s.t<shot.end);
  if(slice.length<2||slice[0].shots[0]?.transform===slice.at(-1).shots[0]?.transform)failures.push('Static '+shot.id);
 }
}finally{await browser.close();}
fs.writeFileSync(path.join(P,'05_review/shorts-timeline-check.json'),JSON.stringify({status:failures.length?'fail':'pass',failures,caption_surface_identical:true,spoiler_review:'No entity identity, physical arm-in-boot reveal, escape method or ending. Final sentence complete.',samples},null,2)+'\n');
if(failures.length)throw Error(JSON.stringify(failures));
console.log('Short coverage, motion, every caption safe area and 250ms timing checks passed.');
