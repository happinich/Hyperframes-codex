import fs from 'node:fs';import path from 'node:path';import {createCanvas,loadImage} from 'canvas';
const P=path.dirname(new URL(import.meta.url).pathname);
for(const type of ['main-scene-pass2','shorts-final']){
 const dir=path.join(P,'05_review/frames',type),files=fs.readdirSync(dir).filter(f=>f.endsWith('.png')).sort();
 const portrait=type.startsWith('short'),w=portrait?270:480,h=portrait?500:295,cols=portrait?5:3,per=portrait?5:12;
 for(let start=0;start<files.length;start+=per){const group=files.slice(start,start+per),c=createCanvas(w*cols,h*Math.ceil(group.length/cols)),ctx=c.getContext('2d');ctx.fillStyle='#151b19';ctx.fillRect(0,0,c.width,c.height);ctx.font='16px sans-serif';
 for(let i=0;i<group.length;i++){const im=await loadImage(path.join(dir,group[i]));let x=i%cols*w,y=Math.floor(i/cols)*h;ctx.fillStyle='#fff';ctx.fillText(group[i].replace('.png',''),x+8,y+19);ctx.drawImage(im,x,y+25,w,h-25);}
 fs.writeFileSync(path.join(dir,`sheet-${Math.floor(start/per)+1}.jpg`),c.toBuffer('image/jpeg'));}
}
