import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import puppeteer from 'puppeteer-core';
const P=path.dirname(new URL(import.meta.url).pathname);
const read=f=>JSON.parse(fs.readFileSync(path.join(P,f)));
const data=read('04_composition/scene-data.json'),assets=read('04_composition/image-sources.json');
const failures=[],samples=[];
for(const a of assets){
 const hash=createHash('sha256').update(fs.readFileSync(a.file)).digest('hex');
 if(!a.render_approved||hash!==a.sha256)failures.push('Unapproved or changed image '+a.id);
}
for(const [i,s]of data.shots.entries()){
 if(s.end<=s.start)failures.push('Nonpositive shot '+s.id);
 if(i&&Math.abs(data.shots[i-1].end-s.start)>.001)failures.push('Gap '+s.id);
}
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
try{
 const page=await browser.newPage();await page.setViewport({width:1920,height:1080});
 await page.goto('file://'+path.join(P,'04_composition/index.html'));
 await page.evaluate(async()=>{await document.fonts.ready;for(const im of document.images)await im.decode()});
 for(const s of data.shots){
  const states=[];
  for(const t of [s.start+.02,Math.min(s.start+2,s.end-.02)]){
   states.push(await page.evaluate(t=>{Object.values(window.__timelines)[0].seek(t,false);const visible=[...document.querySelectorAll('.shot')].filter(e=>getComputedStyle(e).display!=='none');return visible.map(e=>({id:e.id,transform:getComputedStyle(e.querySelector('.photo')).transform,light:getComputedStyle(e.querySelector('.light')).opacity}));},t));
  }
  if(states.some(x=>x.length!==1||x[0].id!==s.id))failures.push('Visibility '+s.id);
  if(states[0][0]?.transform===states[1][0]?.transform)failures.push('Static '+s.id);
  samples.push({shot:s.id,start:s.start,end:s.end,states});
 }
 const end=await page.evaluate(t=>{Object.values(window.__timelines)[0].seek(t,false);return Number(getComputedStyle(document.querySelector('.end-safe')).opacity)},data.duration-17);
 if(end<.9)failures.push('End screen missing');
}finally{await browser.close()}
fs.writeFileSync(path.join(P,'05_review/motion-check.json'),JSON.stringify({status:failures.length?'fail':'pass',failures,samples},null,2)+'\n');
if(failures.length)throw Error(JSON.stringify(failures));console.log('52 shot coverage, approved hashes, camera motion and ending safe area passed.');
