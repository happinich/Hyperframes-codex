import fs from 'node:fs';
import path from 'node:path';
import puppeteer from 'puppeteer-core';
const P=path.dirname(new URL(import.meta.url).pathname);
const browser=await puppeteer.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--allow-file-access-from-files']});
const results=[];
try{
 for(const format of ['youtube','shorts']){
 const page=await browser.newPage();await page.setViewport({width:1240,height:1000});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file://'+path.join(P,`07_publish/${format}/${format}-publish.html`));
 await page.evaluate(()=>{window.testCopied='';Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async t=>window.testCopied=t}})});
 await page.click('#copy-all');const all=await page.evaluate(()=>window.testCopied);
 if(!all.includes('설명란\n')||!all.includes('추천 게시 시간\n'))throw Error('Incomplete copy-all');
 await page.click('[data-copy="block-0"]');const title=await page.evaluate(()=>window.testCopied);
 if(!title||title.includes('설명란\n'))throw Error('Title copy failed');
 await page.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});document.execCommand=command=>{const a=document.activeElement;if(command!=='copy'||a.tagName!=='TEXTAREA')return false;window.testCopied=a.value.slice(a.selectionStart,a.selectionEnd);return true;};});
 await page.click('[data-copy="block-1"]');
 const fallback=await page.evaluate(()=>window.testCopied===document.getElementById('block-1').textContent);
 if(!fallback)throw Error('Local-file copy fallback failed');
 const links=await page.$$eval('a[href]',a=>a.map(x=>x.getAttribute('href')));
 for(const href of links){if(href.startsWith('http'))continue;const target=path.resolve(P,`07_publish/${format}`,href.split('#')[0]);if(!fs.existsSync(target))errors.push('missing '+href);}
 await page.screenshot({path:path.join(P,`05_review/frames/publish-${format}.png`),fullPage:false});
 await page.setViewport({width:390,height:844});await page.screenshot({path:path.join(P,`05_review/frames/publish-${format}-mobile.png`)});
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);if(overflow)errors.push('mobile horizontal overflow');
 results.push({format,status:errors.length?'fail':'pass',errors,copy_all_length:all.length});
 await page.close();
 }
}finally{await browser.close();}
fs.writeFileSync(path.join(P,'05_review/publish-check.json'),JSON.stringify(results,null,2)+'\n');
if(results.some(r=>r.errors.length))throw Error(JSON.stringify(results));
console.log('Publishing helper copy controls, local links and mobile layouts passed.');
