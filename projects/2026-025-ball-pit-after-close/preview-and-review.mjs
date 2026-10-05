import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';
import {fileURLToPath, pathToFileURL} from 'node:url';
const P=path.dirname(fileURLToPath(import.meta.url));
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
const page=await browser.newPage();
const issues=[];
page.on('pageerror',e=>issues.push(String(e)));
await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
await page.goto(pathToFileURL(path.join(P,'04_composition/variants/shorts.html')).href);
await page.evaluate(async()=>{await Promise.race([document.fonts.ready,new Promise(r=>setTimeout(r,3000))]);await Promise.race([Promise.all([...document.images].map(i=>i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r}))),new Promise(r=>setTimeout(r,3000))]);});
const images=await page.evaluate(()=>[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0})));
for(const i of images)if(!i.loaded)issues.push('Unloaded image '+i.src);
const samples=[0,1.8,4,8,11.3,13,15.3,18.4,20.4,21.8];
const states=[];
for(const t of samples){
 await page.evaluate(t=>{window.__timelines['shorts-master'].seek(t,false)},t);
 const state=await page.evaluate(()=>[...document.querySelectorAll('.caption,.hook,.cta')].filter(e=>Number(getComputedStyle(e).opacity)>.9).map(e=>{const r=e.getBoundingClientRect();return{text:e.innerText,x:r.x,y:r.y,width:r.width,height:r.height};}));
 if(state.some(s=>s.x<60||s.x+s.width>940||s.y<100||s.y+s.height>1710))issues.push('Unsafe text at '+t);
 await page.screenshot({path:path.join(P,`05_review/preview/shorts-preview-${t}.png`)});
 states.push({time:t,visible:state});
}
fs.writeFileSync(path.join(P,'05_review/shorts-layout-review.json'),JSON.stringify({issues,states},null,2)+'\n');
await browser.close();
console.log(JSON.stringify({samples:samples.length,issues}));
if(issues.length)process.exitCode=1;
