import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const here = path.dirname(fileURLToPath(import.meta.url));
const visuals = path.resolve(here, "../../04_composition/assets/visuals");

const escapeXml = (value) => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");

function svgLayer(markup) {
  return Buffer.from(`
    <svg width="1280" height="720" xmlns="http://www.w3.org/2000/svg">
      <style>
        .ko { font-family: "Apple SD Gothic Neo", "Noto Sans CJK KR", sans-serif; }
        .heavy { font-weight: 900; letter-spacing: -3px; }
      </style>
      ${markup}
    </svg>
  `);
}

async function background(file, position = "center") {
  return sharp(path.join(visuals, file))
    .resize(1280, 720, { fit: "cover", position })
    .modulate({ brightness: 0.62, saturation: 0.78 })
    .blur(0.3)
    .png()
    .toBuffer();
}

async function createA() {
  const base = await background("hospital-03.png", "entropy");
  const overlay = svgLayer(`
    <defs>
      <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#020308" stop-opacity="0.97"/>
        <stop offset="0.62" stop-color="#020308" stop-opacity="0.62"/>
        <stop offset="1" stop-color="#020308" stop-opacity="0.12"/>
      </linearGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="12" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect width="1280" height="720" fill="url(#shade)"/>
    <rect x="48" y="45" width="330" height="54" rx="27" fill="#ff334d"/>
    <text x="213" y="82" text-anchor="middle" class="ko" font-size="27" font-weight="800" fill="#fff">공포괴담 3편 연속</text>
    <text x="58" y="250" class="ko heavy" font-size="93" fill="#fff">응답하면</text>
    <text x="58" y="355" class="ko heavy" font-size="112" fill="#ff334d" filter="url(#glow)">사라진다</text>
    <text x="60" y="428" class="ko" font-size="34" font-weight="800" fill="#d7e5f4">폐쇄 병실 · 내일의 CCTV · 빈 택시</text>
    <rect x="870" y="500" width="350" height="142" rx="24" fill="#04060c" fill-opacity="0.88" stroke="#ff334d" stroke-width="3"/>
    <text x="1045" y="598" text-anchor="middle" font-family="monospace" font-size="82" font-weight="900" fill="#ff334d">03:17</text>
  `);
  await sharp(base).composite([{ input: overlay }]).png().toFile(path.join(here, "thumbnail-a.png"));
}

async function createB() {
  const left = await sharp(path.join(visuals, "cctv-04.png")).resize(740, 720, { fit: "cover", position: "entropy" }).png().toBuffer();
  const right = await sharp(path.join(visuals, "taxi-02.png")).resize(740, 720, { fit: "cover", position: "entropy" }).png().toBuffer();
  const base = await sharp({ create: { width: 1280, height: 720, channels: 3, background: "#03050a" } })
    .composite([{ input: left, left: 0, top: 0 }, { input: right, left: 540, top: 0 }])
    .modulate({ brightness: 0.58, saturation: 0.72 })
    .png()
    .toBuffer();
  const overlay = svgLayer(`
    <defs>
      <linearGradient id="v" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#020308" stop-opacity="0.16"/><stop offset="1" stop-color="#020308" stop-opacity="0.92"/></linearGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect width="1280" height="720" fill="url(#v)"/>
    <path d="M640 0 L705 720" stroke="#ff334d" stroke-width="7" opacity="0.8"/>
    <text x="60" y="160" class="ko heavy" font-size="128" fill="#ff334d" filter="url(#glow)">절대</text>
    <text x="60" y="280" class="ko heavy" font-size="106" fill="#fff">받지 마라</text>
    <rect x="55" y="515" width="1170" height="128" rx="22" fill="#03050a" fill-opacity="0.86" stroke="#ffffff" stroke-opacity="0.22"/>
    <text x="640" y="592" text-anchor="middle" class="ko" font-size="40" font-weight="900" fill="#fff">호출벨  ·  CCTV  ·  택시 앱</text>
    <text x="640" y="635" text-anchor="middle" class="ko" font-size="24" font-weight="800" fill="#ff6a7d">새벽 세 시 십칠 분에 울린 세 가지 신호</text>
  `);
  await sharp(base).composite([{ input: overlay }]).png().toFile(path.join(here, "thumbnail-b.png"));
}

await Promise.all([createA(), createB()]);
console.log(`Generated ${escapeXml("thumbnail-a.png")} and ${escapeXml("thumbnail-b.png")}`);
