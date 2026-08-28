import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {createCanvas, loadImage} from "canvas";

const here = path.dirname(fileURLToPath(import.meta.url));
const width = 1280;
const height = 720;

const variants = [
  {
    source: "thumbnail-a-background.png",
    output: "thumbnail-a.png",
    side: "left",
    lines: [
      {text: "5명 체크인", color: "#ffffff"},
      {text: "CCTV엔 6명", color: "#ff334f"},
    ],
  },
  {
    source: "thumbnail-b-background.png",
    output: "thumbnail-b.png",
    side: "right",
    lines: [
      {text: "다섯 명인데", color: "#ffffff"},
      {text: "컵은 6개", color: "#ff334f"},
    ],
  },
];

function drawCover(ctx, image) {
  const scale = Math.max(width / image.width, height / image.height);
  const sourceWidth = width / scale;
  const sourceHeight = height / scale;
  const sourceX = (image.width - sourceWidth) / 2;
  const sourceY = (image.height - sourceHeight) / 2;
  ctx.drawImage(
    image,
    sourceX,
    sourceY,
    sourceWidth,
    sourceHeight,
    0,
    0,
    width,
    height,
  );
}

function drawHeadline(ctx, variant) {
  const isLeft = variant.side === "left";
  const panelX = isLeft ? 28 : 690;
  const panelWidth = 562;
  const gradient = ctx.createLinearGradient(
    isLeft ? panelX : panelX + panelWidth,
    0,
    isLeft ? panelX + panelWidth : panelX,
    0,
  );
  gradient.addColorStop(0, "rgba(0, 0, 0, 0.78)");
  gradient.addColorStop(1, "rgba(0, 0, 0, 0.30)");
  ctx.fillStyle = gradient;
  ctx.fillRect(panelX, 145, panelWidth, 325);

  const accentX = isLeft ? 52 : 1198;
  ctx.fillStyle = "#e31b36";
  ctx.fillRect(accentX, 176, 9, 238);

  ctx.font = "800 82px 'Apple SD Gothic Neo', sans-serif";
  ctx.textAlign = isLeft ? "left" : "right";
  ctx.textBaseline = "middle";
  ctx.lineJoin = "round";
  ctx.lineWidth = 12;
  ctx.strokeStyle = "rgba(0, 0, 0, 0.96)";
  const x = isLeft ? 82 : 1170;
  const yPositions = [250, 370];
  variant.lines.forEach((line, index) => {
    ctx.strokeText(line.text, x, yPositions[index]);
    ctx.fillStyle = line.color;
    ctx.fillText(line.text, x, yPositions[index]);
  });
}

for (const variant of variants) {
  const image = await loadImage(path.join(here, variant.source));
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");
  drawCover(ctx, image);
  drawHeadline(ctx, variant);
  fs.writeFileSync(path.join(here, variant.output), canvas.toBuffer("image/png"));
  console.log(`Created ${variant.output}`);
}
