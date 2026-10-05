import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';
import {fileURLToPath,pathToFileURL} from 'node:url';
const P=path.dirname(fileURLToPath(import.meta.url));
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));const reports=[];
try{
 for(const fmt of ['youtube','shorts']){
  const file=path.join(P,`07_publish/${fmt}/${fmt}-publish.html`);
  await page.setViewport({width:1100,height:1000,deviceScaleFactor:1});
  await page.goto(pathToFileURL(file).href,{waitUntil:'load'});
  // Exercise the real copy handlers while capturing text inside this isolated browser.
  await page.evaluate(()=>{window.__copied=[];Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async t=>{window.__copied.push(t)}}});});
  const expected=await page.evaluate(()=>[...document.querySelectorAll('[data-copy]')].map(b=>({id:b.dataset.copy,text:document.getElementById(b.dataset.copy).textContent})));
  for(const b of expected)await page.click(`[data-copy="${b.id}"]`);
  const actual=await page.evaluate(()=>window.__copied);
  if(JSON.stringify(actual)!==JSON.stringify(expected.map(x=>x.text)))throw new Error('Copy mismatch '+fmt);
  await page.click('#copy-all');
  const all=await page.evaluate(()=>window.__copied.at(-1));if(!all.includes('창작')||all.length<400)throw new Error('Copy-all failed '+fmt);
  const links=await page.evaluate(()=>[...document.querySelectorAll('a[href],img[src],video[src]')].map(e=>e.href||e.src));
  for(const u of links)if(u.startsWith('file:')&&!fs.existsSync(fileURLToPath(u)))throw new Error('Missing local resource '+u);
  await page.screenshot({path:path.join(P,`05_review/preview/${fmt}-publish-preview.png`)});
  const media=await page.evaluate(()=>{const v=document.querySelector('video');return{duration:v.duration,width:v.videoWidth,height:v.videoHeight};});
  reports.push({format:fmt,copy_buttons:expected.length,copy_all:true,local_links:links.length,media});
 }
 fs.writeFileSync(path.join(P,'05_review/publishing-review.json'),JSON.stringify({reports,errors},null,2)+'\n');
 console.log(JSON.stringify({reports,errors}));if(errors.length)process.exitCode=1;
}finally{await browser.close()}
