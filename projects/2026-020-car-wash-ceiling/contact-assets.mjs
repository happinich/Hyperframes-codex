import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
const P=path.dirname(new URL(import.meta.url).pathname);
const dir=path.join(P,'04_composition/assets/visuals');
const files=fs.readdirSync(dir).filter(f=>f.endsWith('.png')).sort();
for(let offset=0;offset<files.length;offset+=16){
 const batch=files.slice(offset,offset+16),pieces=[];
 for(const [i,file]of batch.entries()){
  const left=i%4*384,top=Math.floor(i/4)*240;
  pieces.push({input:await sharp(path.join(dir,file)).resize(384,216,{fit:'contain',background:'#13212b'}).png().toBuffer(),left,top});
  pieces.push({input:Buffer.from(`<svg width="384" height="24"><rect width="384" height="24" fill="#13212b"/><text x="12" y="17" fill="white" font-size="14">${file}</text></svg>`),left,top:top+216});
 }
 await sharp({create:{width:1536,height:Math.ceil(batch.length/4)*240,channels:3,background:'#13212b'}}).composite(pieces).png().toFile(path.join(P,`05_review/frames/assets-${Math.floor(offset/16)+1}.png`));
}
console.log('Contact sheets: '+files.length+' image files');
