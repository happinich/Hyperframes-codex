import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const P = path.dirname(new URL(import.meta.url).pathname);
const variants = [
  {id:'a', lines:['반납함의','손'], accent:1},
  {id:'b', lines:['책이','돌아왔다'], accent:1},
];
for (const v of variants) {
  const rows = v.lines.map((line,i) => `<text x="65" y="${i ? 390 : 265}" fill="${i === v.accent ? '#ef4f45' : '#fff8ee'}" stroke="#02070b" stroke-width="13" paint-order="stroke" font-size="103" font-weight="900">${line}</text>`).join('');
  const svg = `<svg width="1280" height="720" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g"><stop stop-color="#030b16" stop-opacity=".62"/><stop offset="1" stop-color="#030b16" stop-opacity="0"/></linearGradient></defs><rect x="0" y="0" width="720" height="720" fill="url(#g)"/><g font-family="Apple SD Gothic Neo, sans-serif" letter-spacing="-3">${rows}</g></svg>`;
  const source = path.join(P,`04_composition/assets/visuals/thumbnail-${v.id}.png`);
  const output = path.join(P,`07_publish/youtube/thumbnail-${v.id}.jpg`);
  await sharp(source).resize(1280,720,{fit:'cover'}).composite([{input:Buffer.from(svg)}]).jpeg({quality:94}).toFile(output);
  const meta = await sharp(output).metadata();
  if (meta.width !== 1280 || meta.height !== 720) throw new Error('Bad thumbnail size: '+v.id);
  console.log(output);
}
