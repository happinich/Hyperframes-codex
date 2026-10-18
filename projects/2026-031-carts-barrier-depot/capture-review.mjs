import puppeteer from 'puppeteer-core';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const P=path.dirname(fileURLToPath(import.meta.url)),C=path.join(P,'04_composition');
const plan=JSON.parse(await fs.readFile(path.join(C,'scene-data.json'),'utf8')),segments=JSON.parse(await fs.readFile(path.join(C,'render-segments.json'),'utf8'));
const out=path.join(P,'05_review/composition-frames');await fs.mkdir(out,{recursive:true});
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,protocolTimeout:60000,args:['--allow-file-access-from-files','--no-sandbox']});
const page=await browser.newPage();let errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.setViewport({width:1920,height:1080,deviceScaleFactor:1});
let selected=process.argv.slice(2);const shots=plan.shots.filter(s=>!selected.length||selected.includes(s.logical_asset));
for(const s of shots){const t=(s.startFrame+s.endFrame)/120,segment=segments.find(x=>t*60>=x.startFrame&&t*60<x.endFrame);await page.goto(pathToFileURL(path.join(C,segment.filename)).href);await page.evaluate(()=>document.fonts.ready);await page.evaluate(t=>{const tl=Object.values(window.__timelines)[0];tl.pause();tl.seek(t,false)},t-segment.startFrame/60);await page.screenshot({path:path.join(out,s.logical_asset+'.png')});}
for(let n=1;n<=3;n++){await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});await page.goto(pathToFileURL(path.join(C,`shorts-${String(n).padStart(2,'0')}/index.html`)).href);await page.evaluate(()=>document.fonts.ready);for(const t of [0.1,5.8,11,14.5,19.3]){await page.evaluate(t=>{Object.values(window.__timelines)[0].pause().seek(t,false)},t);await page.screenshot({path:path.join(out,`SH${n}-${t}.png`)});}}
await fs.writeFile(path.join(out,'capture-report.json'),JSON.stringify({shots:shots.length,short_frames:15,errors},null,2));await browser.close();console.log({shots:shots.length,errors});
