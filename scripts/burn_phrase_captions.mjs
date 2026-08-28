#!/usr/bin/env node
/** Burn phrase-level white captions for the minimal dark tech production profile. */

import fs from "node:fs";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { createCanvas } = require("canvas");

function fail(message) {
  console.error(message);
  process.exit(1);
}

const projectArg = process.argv[2];
if (!projectArg) fail("Usage: node scripts/burn_phrase_captions.mjs <project-directory>");

const project = path.resolve(projectArg);
const projectId = path.basename(project);
const input = path.join(project, "06_delivery", "youtube", `${projectId}-youtube.mp4`);
const timingPath = path.join(project, "03_sync", "captions.words.json");
const output = path.join(
  project,
  "06_delivery",
  "youtube",
  `${projectId}-youtube-captioned-minimal.mp4`,
);

if (!fs.existsSync(input)) fail(`Missing approved master: ${input}`);
if (!fs.existsSync(timingPath)) fail(`Missing caption timings: ${timingPath}`);

const probe = spawnSync("ffprobe", [
  "-v", "error",
  "-select_streams", "v:0",
  "-show_entries", "format=duration:stream=avg_frame_rate,r_frame_rate",
  "-of", "json",
  input,
], { encoding: "utf8" });
if (probe.status !== 0) fail(probe.stderr || "ffprobe failed");

function parseFrameRate(value) {
  const [numerator, denominator = "1"] = String(value || "").split("/");
  const rate = Number(numerator) / Number(denominator);
  return Number.isFinite(rate) && rate > 0 ? rate : 60;
}

const media = JSON.parse(probe.stdout);
const duration = Number.parseFloat(media.format.duration);
const videoStream = media.streams?.[0] || {};
const fps = parseFrameRate(videoStream.avg_frame_rate || videoStream.r_frame_rate);
const frameCount = Math.ceil(duration * fps);
const width = 1920;
const layerHeight = 190;
const maxTextWidth = 1640;
const cues = JSON.parse(fs.readFileSync(timingPath, "utf8")).cues;

const canvas = createCanvas(width, layerHeight);
const ctx = canvas.getContext("2d");
ctx.textAlign = "center";
ctx.textBaseline = "middle";
ctx.lineJoin = "round";
ctx.miterLimit = 2;

let cueIndex = 0;

function activeCue(time) {
  while (cueIndex < cues.length - 1 && time >= cues[cueIndex].end) cueIndex += 1;
  const cue = cues[cueIndex];
  return cue && time >= cue.start && time < cue.end ? cue : null;
}

function fitFont(text) {
  let size = 60;
  while (size > 42) {
    ctx.font = `900 ${size}px "Apple SD Gothic Neo", "Noto Sans KR", Arial, sans-serif`;
    if (ctx.measureText(text).width <= maxTextWidth) break;
    size -= 2;
  }
  return size;
}

function drawCaption(cue) {
  ctx.clearRect(0, 0, width, layerHeight);
  if (!cue) return;

  const caption = cue.text.trim();
  fitFont(caption);
  const x = width / 2;
  const y = layerHeight / 2;

  ctx.shadowColor = "rgba(0,0,0,.95)";
  ctx.shadowBlur = 18;
  ctx.shadowOffsetY = 4;
  ctx.lineWidth = 8;
  ctx.strokeStyle = "rgba(0,0,0,.96)";
  ctx.strokeText(caption, x, y, maxTextWidth);
  ctx.fillStyle = "#ffffff";
  ctx.fillText(caption, x, y, maxTextWidth);
  ctx.shadowColor = "transparent";
}

const ffmpeg = spawn("ffmpeg", [
  "-hide_banner", "-loglevel", "error", "-y",
  "-f", "rawvideo", "-pix_fmt", "rgba", "-video_size", `${width}x${layerHeight}`,
  "-framerate", String(fps), "-i", "pipe:0",
  "-i", input,
  "-filter_complex", "[1:v][0:v]overlay=0:H-h-48:format=auto[v]",
  "-map", "[v]", "-map", "1:a?",
  "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
  "-r", String(fps),
  "-c:a", "copy", "-movflags", "+faststart", "-shortest", output,
], { stdio: ["pipe", "inherit", "inherit"] });

ffmpeg.on("error", (error) => fail(`Unable to start ffmpeg: ${error.message}`));

for (let frame = 0; frame < frameCount; frame += 1) {
  const time = (frame + 0.5) / fps;
  drawCaption(activeCue(time));
  const pixels = ctx.getImageData(0, 0, width, layerHeight).data;
  if (!ffmpeg.stdin.write(Buffer.from(pixels.buffer))) {
    await new Promise((resolve) => ffmpeg.stdin.once("drain", resolve));
  }
  if (frame % 900 === 0) console.log(`Phrase caption frames: ${frame}/${frameCount}`);
}
ffmpeg.stdin.end();

const exitCode = await new Promise((resolve) => ffmpeg.on("close", resolve));
if (exitCode !== 0) fail(`ffmpeg exited with code ${exitCode}`);
console.log(`Minimal captioned video: ${output}`);
