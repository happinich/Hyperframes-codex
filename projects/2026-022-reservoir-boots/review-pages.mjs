import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import puppeteer from 'puppeteer-core';

const P=path.dirname(fileURLToPath(import.meta.url));
const browser=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files']});
const results=[];
fs.mkdirSync(path.join(P,'05_review/frames'),{recursive:true});
try{
 for(const name of ['voice-review','bgm-selection']){
  const page=await browser.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.setViewport({width:1240,height:1000});
  await page.goto('file://'+path.join(P,'05_review',name+'.html'),{waitUntil:'networkidle0'});
  const links=await page.$$eval('a[href],audio[src],img[src]',nodes=>nodes.map(n=>n.getAttribute('href')||n.getAttribute('src')));
  for(const href of links)if(!fs.existsSync(path.resolve(P,'05_review',href)))errors.push('missing '+href);
  const media=await page.$$eval('audio',nodes=>nodes.map(n=>({source:n.getAttribute('src'),duration:n.duration,error:n.error?.code??null})));
  if(media.some(m=>m.error))errors.push('audio metadata error');
  if(name==='bgm-selection'){
   await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async t=>window.copied=t}}));
   await page.click('[data-copy="cand-03 승인"]');
   const copied=await page.evaluate(()=>window.copied);
   if(copied!=='cand-03 승인')errors.push('clipboard failed');
   await page.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});document.execCommand=c=>{const t=document.activeElement;if(c!=='copy'||t.tagName!=='TEXTAREA')return false;window.copied=t.value;return true;};});
   await page.click('[data-copy="cand-01 승인"]');
   if(await page.evaluate(()=>window.copied)!=='cand-01 승인')errors.push('local-file fallback failed');
  }
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:path.join(P,'05_review/frames',name+'-desktop.png')});
  await page.setViewport({width:390,height:844});
  await page.evaluate(()=>window.scrollTo(0,0));
  if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))errors.push('mobile overflow');
  await page.screenshot({path:path.join(P,'05_review/frames',name+'-mobile.png')});
  results.push({page:name,status:errors.length?'fail':'pass',errors,media});
  await page.close();
 }
}finally{await browser.close();}
fs.writeFileSync(path.join(P,'05_review/review-pages-check.json'),JSON.stringify(results,null,2)+'\n');
if(results.some(r=>r.status==='fail'))throw Error(JSON.stringify(results));
console.log('Review helpers: assets, audio, copy/fallback and mobile layout passed.');
