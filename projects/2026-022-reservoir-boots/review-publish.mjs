import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';
const P=path.dirname(new URL(import.meta.url).pathname);
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
const failures=[],results=[];
try{
 for(const format of ['youtube','shorts']){
  const helper=path.join(P,`07_publish/${format}/${format}-publish.html`);
  if(!fs.existsSync(helper)||!fs.existsSync(path.join(P,`06_delivery/${format}/${path.basename(P)}-${format}.mp4`)))continue;
  const page=await browser.newPage();page.on('pageerror',e=>failures.push(e.message));
  await page.goto('file://'+helper);
  await page.evaluate(()=>{window.copied=[];navigator.clipboard.writeText=async t=>{window.copied.push(t)}});
  await page.click('#copy-all');
  const all=await page.evaluate(()=>window.copied[0]);
  if(!all||!all.includes('추천 게시 시간'))failures.push('Copy all missing time');
  const buttons=await page.$$('[data-copy]');
  for(const b of buttons)await b.click();
  const copied=await page.evaluate(()=>window.copied.length);
  if(copied!==buttons.length+1)failures.push('Block copying failed');
  await page.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw Error('forced fallback')};document.execCommand=()=>{window.fallbackUsed=true;return true}});
  await page.click('#copy-all');
  if(!await page.evaluate(()=>window.fallbackUsed))failures.push('Clipboard fallback missing');
  const links=await page.$$eval('a[href]',xs=>xs.map(x=>x.getAttribute('href')));
  for(const href of links)if(!fs.existsSync(path.resolve(path.dirname(helper),href)))failures.push('Broken '+href);
  await page.setViewport({width:390,height:844});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(overflow)failures.push('Mobile overflow');
  await page.screenshot({path:path.join(P,`05_review/frames/publish-${format}-mobile.png`)});
  await page.setViewport({width:1400,height:1000});
  await page.screenshot({path:path.join(P,`05_review/frames/publish-${format}-desktop.png`)});
  results.push({format,blocks:buttons.length,copy_all:true,copy_blocks:true,clipboard_fallback:true,local_links_exist:true,mobile_overflow:overflow});
  await page.close();
 }
}finally{await browser.close()}
fs.writeFileSync(path.join(P,'05_review/publish-check.json'),JSON.stringify({status:failures.length?'fail':'pass',failures,results},null,2)+'\n');
if(failures.length)throw Error(JSON.stringify(failures));console.log('Publishing copy buttons, fallback, mobile layout and links passed.');
