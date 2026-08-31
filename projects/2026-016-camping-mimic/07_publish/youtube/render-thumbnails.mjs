import sharp from "sharp";
import path from "node:path";
import {fileURLToPath} from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const visuals = path.resolve(here, "../../04_composition/assets/visuals");
const output = path.join(here, "thumbnails");

async function render(input, target, overlay) {
  await sharp(path.join(visuals, input))
    .resize(1280, 720, {fit: "cover"})
    .composite([{input: Buffer.from(overlay)}])
    .png()
    .toFile(path.join(output, target));
}

const base = `font-family="Apple SD Gothic Neo, sans-serif" font-weight="900" paint-order="stroke" stroke="#000" stroke-width="18" stroke-linejoin="round"`;

await render("tent-shadow.png", "thumbnail-a.png", `
<svg width="1280" height="720" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0.46" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.78"/></linearGradient></defs>
  <rect width="1280" height="720" fill="url(#g)"/>
  <text x="706" y="292" ${base} font-size="112" fill="#ffffff">밖에도</text>
  <text x="772" y="475" ${base} font-size="164" fill="#ff334f">민수</text>
  <rect x="1208" y="88" width="12" height="540" rx="6" fill="#ff334f"/>
</svg>`);

await render("tent-tear.png", "thumbnail-b.png", `
<svg width="1280" height="720" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g" x1="1" x2="0"><stop offset="0.42" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.82"/></linearGradient></defs>
  <rect width="1280" height="720" fill="url(#g)"/>
  <text x="88" y="292" ${base} font-size="145" fill="#ffffff">지퍼</text>
  <text x="88" y="470" ${base} font-size="145" fill="#ff334f">열지 마</text>
  <path d="M88 530 H520" stroke="#ff334f" stroke-width="13" stroke-linecap="round"/>
</svg>`);
