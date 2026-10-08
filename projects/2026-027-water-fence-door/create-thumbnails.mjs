import {createCanvas,loadImage} from 'canvas';
import fs from 'node:fs';
import path from 'node:path';
const P=path.dirname(new URL(import.meta.url).pathname),out=path.join(P,'07_publish/youtube');
fs.mkdirSync(out,{recursive:true});
for(const [id,lines] of [['a',['물이','없는데']],['b',['벽 뒤에','누가']]]){
 const canvas=createCanvas(1280,720),ctx=canvas.getContext('2d');
 const img=await loadImage(path.join(P,`04_composition/assets/visuals/thumbnail-${id}-source.png`));
 ctx.drawImage(img,0,0,1280,720);
 const g=ctx.createLinearGradient(0,0,800,0);g.addColorStop(0,'rgba(3,9,12,.55)');g.addColorStop(.8,'rgba(3,9,12,0)');ctx.fillStyle=g;ctx.fillRect(0,0,800,720);
 ctx.font='900 132px "Apple SD Gothic Neo"';ctx.textBaseline='top';ctx.lineJoin='round';ctx.lineWidth=11;ctx.strokeStyle='#071116';
 for(let i=0;i<2;i++){ctx.strokeText(lines[i],65,206+i*152);ctx.fillStyle=i===0?'#f3e8cf':'#e6b35c';ctx.fillText(lines[i],65,206+i*152);}
 fs.writeFileSync(path.join(out,`thumbnail-${id}.png`),canvas.toBuffer('image/png'));
 fs.writeFileSync(path.join(out,`thumbnail-${id}-text.txt`),lines.join(' ')+'\n');
}
