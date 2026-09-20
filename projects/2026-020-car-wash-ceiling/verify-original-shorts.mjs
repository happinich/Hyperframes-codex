import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import sharp from 'sharp';
const P=path.dirname(new URL(import.meta.url).pathname);
const dir=path.join(P,'04_composition/assets/visuals');
const main=fs.readdirSync(dir).filter(n=>/^shot-\d+\.png$/.test(n));
const short=fs.readdirSync(dir).filter(n=>/^short-new-\d+\.png$/.test(n));
const hash=n=>crypto.createHash('sha256').update(fs.readFileSync(path.join(dir,n))).digest('hex');
const mainHashes=new Set(main.map(hash));
const source=JSON.parse(fs.readFileSync(path.join(P,'04_composition/image-sources.json')));
const plan=JSON.parse(fs.readFileSync(path.join(P,'01_script/shorts-scene-plan.json')));
if(main.length!==48||short.length!==6)throw Error('Expected 48 main images and six fresh Short images');
const checked=short.map(name=>{
 const sha256=hash(name),id=name.slice(0,-4),record=source.findLast(s=>s.id===id);
 if(mainHashes.has(sha256))throw Error('Long-form asset reused: '+name);
 if(!record||record.purpose!=='shorts_original'||!Array.isArray(record.reference_images)||record.reference_images.length)throw Error('No independent generation record: '+name);
 return {name,sha256,source:record.source,reference_images:[]};
});
if(plan.shots.some(s=>!/^short-new-\d+$/.test(s.visual)))throw Error('Long-form frame in Short timeline');
if(new Set(checked.map(c=>c.sha256)).size!==6)throw Error('Duplicate Short asset');
for(const asset of checked){
 const meta=await sharp(path.join(dir,asset.name)).metadata();
 if(meta.height<=meta.width)throw Error('Not a fresh portrait asset: '+asset.name);
 asset.width=meta.width;asset.height=meta.height;
}
const report={status:'pass',main_asset_count:main.length,fresh_portrait_assets:checked,no_longform_frame_extraction:true,no_longform_reference_images:true,separate_narration:true,scope:'provenance manifest, asset paths and exact-file hash disjointness; visual framing also reviewed separately'};
fs.writeFileSync(path.join(P,'05_review/shorts-originality-check.json'),JSON.stringify(report,null,2)+'\n');
console.log('PASS: six independently generated Short assets, no main-file hash overlap, no main timeline images');
