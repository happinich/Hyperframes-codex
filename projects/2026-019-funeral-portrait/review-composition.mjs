import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';
import sharp from 'sharp';
const P=path.dirname(new URL(import.meta.url).pathname);
const data=JSON.parse(fs.readFileSync(path.join(P,'04_composition/scene-data.json')));
const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--allow-file-access-from-files']});
const failures=[];
try{
 for(const short of [false,true]){
 const page=await browser.newPage();
 await page.setViewport({width:short?1080:1920,height:short?1920:1080,deviceScaleFactor:1});
 page.on('pageerror',e=>failures.push(e.message));
 await page.goto('file://'+path.join(P,'04_composition',short?'variants/shorts.html':'index.html'));
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(im=>im.decode()));});
 const sd=short?JSON.parse(fs.readFileSync(path.join(P,'01_script/shorts-scene-plan.json'))).duration:0;
 const times=short?[0,.6,3.5,6,sd*.4,sd*.6,sd-4,sd-.2]:data.shots.map(s=>s.start+Math.min(1,(s.end-s.start)/2));
 const images=[];
 for(const [i,t]of times.entries()){
 await page.evaluate(t=>{Object.values(window.__timelines)[0].seek(t,false);},t);
 const bounds=await page.evaluate(()=>[...document.querySelectorAll('.statement,.map-panel,.captions')].filter(e=>getComputedStyle(e).visibility!=='hidden'&&e.getBoundingClientRect().width).map(e=>({class:e.className,x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,right:e.getBoundingClientRect().right,bottom:e.getBoundingClientRect().bottom})));
 if(bounds.some(b=>b.x<0||b.y<0||b.right>(short?1080:1920)||b.bottom>(short?1920:1080)))failures.push({t,bounds});
 const file=path.join(P,`05_review/frames/${short?'shorts':'main'}-${String(i).padStart(2,'0')}.png`);
 await page.screenshot({path:file});
 images.push({input:await sharp(file).resize(short?216:384,short?384:216).png().toBuffer(),left:(i%4)*(short?216:384),top:Math.floor(i/4)*(short?384:216)});
 }
 await sharp({create:{width:4*(short?216:384),height:Math.ceil(times.length/4)*(short?384:216),channels:3,background:'#10151b'}}).composite(images).png().toFile(path.join(P,`05_review/frames/${short?'shorts':'main'}-contact.png`));
 const actual=await page.evaluate(()=>Object.values(window.__timelines)[0].duration());
 if(!short&&Math.abs(actual-data.duration)>.02)failures.push({duration:actual,expected:data.duration});
 await page.close();
 }
}finally{await browser.close();}
fs.writeFileSync(path.join(P,'05_review/layout-check.json'),JSON.stringify({status:failures.length?'fail':'pass',failures},null,2));
if(failures.length)throw Error(JSON.stringify(failures));
console.log('Both layouts, duration and image loading passed. Contact sheets saved.');
