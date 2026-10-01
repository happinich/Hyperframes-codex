import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import puppeteer from 'puppeteer-core';

const P=path.dirname(new URL(import.meta.url).pathname);
const out=path.join(P,'07_publish/youtube');
fs.mkdirSync(out,{recursive:true});
const common=`<meta charset="utf-8"><style>@font-face{font-family:'Apple SD Gothic Neo';src:local('Apple SD Gothic Neo')}*{box-sizing:border-box}html,body{margin:0;width:1280px;height:720px;overflow:hidden;background:#05090d;font-family:'Apple SD Gothic Neo',sans-serif}.frame{position:relative;width:1280px;height:720px;overflow:hidden}.frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.shade{position:absolute;inset:0;background:linear-gradient(90deg,#020507e6 0%,#020507ad 28%,#02050710 65%),linear-gradient(0deg,#020507a8,transparent 35%)}.title{position:absolute;left:64px;top:76px;font-weight:900;font-size:116px;line-height:1.16;letter-spacing:-7px;color:white;text-shadow:0 5px 22px #000}.red{color:#ff5364}.rule{position:absolute;left:64px;bottom:83px;width:146px;height:9px;background:#ff5364;box-shadow:0 0 20px #e52d48}</style>`;
const specs=[
 {id:'a',src:'shot-04.png',lines:'<span class="red">넷째</span><br>목소리'},
 {id:'b',src:'shot-23.png',lines:'천장의<br><span class="red">네 손</span>'},
];
for(const s of specs){
 const html=`<!doctype html><html lang="ko"><head>${common}</head><body><div class="frame"><img src="../../04_composition/assets/visuals/${s.src}"><div class="shade"></div><div class="title">${s.lines}</div><div class="rule"></div></div></body></html>`;
 fs.writeFileSync(path.join(out,`thumbnail-${s.id}.html`),html);
}
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox','--allow-file-access-from-files']});
try{
 for(const s of specs){
  const page=await browser.newPage();await page.setViewport({width:1280,height:720,deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(out,`thumbnail-${s.id}.html`)).href,{waitUntil:'load'});
  await page.evaluate(()=>document.fonts.ready);
  const loaded=await page.$eval('img',x=>x.complete&&x.naturalWidth>0);if(!loaded)throw new Error('Thumbnail source image did not load');
  await page.screenshot({path:path.join(out,`thumbnail-${s.id}.png`)});await page.close();
 }
}finally{await browser.close()}
console.log('Wrote two 1280x720 thumbnail compositions');
