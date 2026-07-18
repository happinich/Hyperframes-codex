#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { createCanvas, loadImage } from "canvas";

const here = path.dirname(new URL(import.meta.url).pathname);
const delivery = path.resolve(here, "../../06_delivery/youtube");
const width = 1280;
const height = 720;

function cover(ctx, image) {
  const scale = Math.max(width / image.width, height / image.height);
  const sourceWidth = width / scale;
  const sourceHeight = height / scale;
  const sx = (image.width - sourceWidth) / 2;
  const sy = (image.height - sourceHeight) / 2;
  ctx.drawImage(image, sx, sy, sourceWidth, sourceHeight, 0, 0, width, height);
}

function roundedRect(ctx, x, y, w, h, radius) {
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, radius);
}

function text(ctx, value, x, y, size, color, options = {}) {
  const { align = "left", outline = 0, maxWidth } = options;
  ctx.save();
  ctx.font = `900 ${size}px "Apple SD Gothic Neo", "Noto Sans KR", sans-serif`;
  ctx.textAlign = align;
  ctx.textBaseline = "alphabetic";
  ctx.lineJoin = "round";
  if (outline > 0) {
    ctx.lineWidth = outline;
    ctx.strokeStyle = "rgba(0,0,0,.9)";
    ctx.strokeText(value, x, y, maxWidth);
  }
  ctx.fillStyle = color;
  ctx.fillText(value, x, y, maxWidth);
  ctx.restore();
}

async function renderA() {
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");
  const image = await loadImage(path.join(here, "thumbnail-background-a.png"));
  cover(ctx, image);

  const shade = ctx.createLinearGradient(0, 0, 760, 0);
  shade.addColorStop(0, "rgba(2,8,20,.98)");
  shade.addColorStop(.72, "rgba(2,8,20,.88)");
  shade.addColorStop(1, "rgba(2,8,20,0)");
  ctx.fillStyle = shade;
  ctx.fillRect(0, 0, 790, height);

  roundedRect(ctx, 54, 42, 270, 48, 24);
  ctx.fillStyle = "#ef2947";
  ctx.fill();
  text(ctx, "WEALTH EXIT 2026", 189, 76, 25, "#ffffff", { align: "center" });

  text(ctx, "부자", 58, 185, 76, "#ffffff", { outline: 8 });
  text(ctx, "2,400명", 58, 286, 105, "#ffd33d", { outline: 10 });
  text(ctx, "한국 탈출", 58, 394, 104, "#ff354f", { outline: 10 });

  roundedRect(ctx, 54, 444, 602, 118, 22);
  ctx.fillStyle = "rgba(255,255,255,.96)";
  ctx.fill();
  text(ctx, "강남은 안 판다", 355, 526, 69, "#071329", { align: "center" });

  roundedRect(ctx, 54, 596, 422, 60, 30);
  ctx.fillStyle = "rgba(7,19,41,.86)";
  ctx.strokeStyle = "rgba(255,211,61,.78)";
  ctx.lineWidth = 2;
  ctx.fill();
  ctx.stroke();
  text(ctx, "떠나도 남기는 마지막 자산", 265, 637, 28, "#ffffff", { align: "center" });

  fs.writeFileSync(path.join(delivery, "thumbnail-a.png"), canvas.toBuffer("image/png"));
}

async function renderB() {
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");
  const image = await loadImage(path.join(here, "thumbnail-background-b.png"));
  cover(ctx, image);

  const shade = ctx.createLinearGradient(585, 0, 1280, 0);
  shade.addColorStop(0, "rgba(1,6,15,0)");
  shade.addColorStop(.2, "rgba(1,6,15,.82)");
  shade.addColorStop(1, "rgba(1,6,15,.98)");
  ctx.fillStyle = shade;
  ctx.fillRect(540, 0, 740, height);

  roundedRect(ctx, 773, 52, 420, 54, 27);
  ctx.fillStyle = "#ffd33d";
  ctx.fill();
  text(ctx, "부자들이 지키는 마지막 자산", 983, 89, 27, "#071329", { align: "center" });

  text(ctx, "한국 떠나도", 1230, 233, 82, "#ffffff", { align: "right", outline: 9 });
  text(ctx, "이건", 1230, 356, 111, "#ffd33d", { align: "right", outline: 10 });
  text(ctx, "안 판다", 1230, 474, 112, "#ff354f", { align: "right", outline: 10 });

  roundedRect(ctx, 730, 535, 500, 110, 20);
  ctx.fillStyle = "rgba(255,255,255,.96)";
  ctx.fill();
  text(ctx, "강남 핵심 아파트", 980, 609, 58, "#071329", { align: "center" });

  fs.writeFileSync(path.join(delivery, "thumbnail-b.png"), canvas.toBuffer("image/png"));
}

fs.mkdirSync(delivery, { recursive: true });
await Promise.all([renderA(), renderB()]);
console.log(path.join(delivery, "thumbnail-a.png"));
console.log(path.join(delivery, "thumbnail-b.png"));
