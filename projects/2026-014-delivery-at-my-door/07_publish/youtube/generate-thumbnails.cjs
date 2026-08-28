const fs = require('fs');
const path = require('path');
const { createCanvas, loadImage } = require('canvas');

const WIDTH = 1280;
const HEIGHT = 720;
const root = path.resolve(__dirname, '../..');
const visualDir = path.join(root, '04_composition', 'assets', 'visuals');

function drawCover(ctx, image) {
  const scale = Math.max(WIDTH / image.width, HEIGHT / image.height);
  const width = image.width * scale;
  const height = image.height * scale;
  ctx.drawImage(image, (WIDTH - width) / 2, (HEIGHT - height) / 2, width, height);
}

function drawText(ctx, text, x, y, size, color) {
  ctx.font = `900 ${size}px "Apple SD Gothic Neo", sans-serif`;
  ctx.lineJoin = 'round';
  ctx.strokeStyle = 'rgba(0,0,0,0.92)';
  ctx.lineWidth = Math.max(8, Math.round(size * 0.075));
  ctx.strokeText(text, x, y);
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
}

function drawLabel(ctx, text, x, y, width) {
  ctx.fillStyle = 'rgba(229,28,74,0.96)';
  ctx.fillRect(x, y, width, 50);
  ctx.font = '800 27px "Apple SD Gothic Neo", sans-serif';
  ctx.fillStyle = '#fff';
  ctx.fillText(text, x + 22, y + 34);
}

async function render({ source, output, side, label, white, red, kicker }) {
  const image = await loadImage(path.join(visualDir, source));
  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext('2d');
  drawCover(ctx, image);

  const gradient = ctx.createLinearGradient(side === 'left' ? 0 : WIDTH, 0, side === 'left' ? 820 : 440, 0);
  gradient.addColorStop(0, 'rgba(0,0,0,0.9)');
  gradient.addColorStop(0.68, 'rgba(0,0,0,0.58)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  const x = side === 'left' ? 70 : 650;
  drawLabel(ctx, label, side === 'left' ? 62 : 916, 64, side === 'left' ? 260 : 292);
  drawText(ctx, white, x, 310, 98, '#ffffff');
  drawText(ctx, red, x, 445, 108, '#ff2858');
  ctx.font = '800 31px "Apple SD Gothic Neo", sans-serif';
  ctx.fillStyle = '#ffffff';
  ctx.shadowColor = '#000000';
  ctx.shadowBlur = 8;
  ctx.fillText(kicker, x + 6, 555);

  fs.writeFileSync(path.join(__dirname, output), canvas.toBuffer('image/png'));
}

Promise.all([
  render({
    source: 'corridor-double.png',
    output: 'thumbnail-a.png',
    side: 'left',
    label: '새벽 배달 괴담',
    white: '문 앞에',
    red: '내가 있다',
    kicker: '전화를 건 사람은 집 안에 있었다',
  }),
  render({
    source: 'proof-photo.png',
    output: 'thumbnail-b.png',
    side: 'right',
    label: '완료 사진의 비밀',
    white: '사진 속',
    red: '나는 둘',
    kicker: '촬영 위치는 집 안이었다',
  }),
]).catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
