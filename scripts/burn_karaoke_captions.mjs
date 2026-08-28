#!/usr/bin/env node
/** Burn word-following Korean captions into an approved YouTube master. */

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
if (!projectArg) fail("Usage: node scripts/burn_karaoke_captions.mjs <project-directory>");

const project = path.resolve(projectArg);
const projectId = path.basename(project);
const input = path.join(project, "06_delivery", "youtube", `${projectId}-youtube.mp4`);
const timingPath = path.join(project, "03_sync", "captions.words.json");
const output = path.join(project, "06_delivery", "youtube", `${projectId}-youtube-captioned.mp4`);

if (!fs.existsSync(input)) fail(`Missing approved master: ${input}`);
if (!fs.existsSync(timingPath)) fail(`Missing word timings: ${timingPath}`);

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
// Preserve the authored frame rate. Concatenated masters can report a slightly
// noisy average rate even when every source segment is constant-rate 60fps.
const fps = parseFrameRate(videoStream.r_frame_rate || videoStream.avg_frame_rate);
const frameCount = Math.ceil(duration * fps);
const width = 1920;
const layerHeight = 190;
const timing = JSON.parse(fs.readFileSync(timingPath, "utf8"));
const cues = timing.cues;
const words = timing.words;
let scanIndex = 0;
for (const cue of cues) {
  cue.words = [];
  while (scanIndex < words.length && words[scanIndex].start < cue.end) {
    if (words[scanIndex].end > cue.start) cue.words.push(words[scanIndex]);
    scanIndex += 1;
  }
}

const canvas = createCanvas(width, layerHeight);
const ctx = canvas.getContext("2d");
ctx.font = '700 58px "Apple SD Gothic Neo", Arial, sans-serif';
ctx.textAlign = "left";
ctx.textBaseline = "middle";
ctx.lineJoin = "round";
ctx.miterLimit = 2;

let cueIndex = 0;
let wordIndex = 0;

function activeCue(time) {
  while (cueIndex < cues.length - 1 && time >= cues[cueIndex].end) cueIndex += 1;
  const cue = cues[cueIndex];
  return cue && time >= cue.start && time < cue.end ? cue : null;
}

function activeWord(time) {
  while (wordIndex < words.length - 1 && time >= words[wordIndex].end) wordIndex += 1;
  const word = words[wordIndex];
  return word && time >= word.start && time < word.end ? word : null;
}

function drawCaption(cue, current) {
  ctx.clearRect(0, 0, width, layerHeight);
  if (!cue) return;

  const tokens = cue.text.split(/\s+/).filter(Boolean);
  const gap = ctx.measureText(" ").width;
  const widths = tokens.map((token) => ctx.measureText(token).width);
  const totalWidth = widths.reduce((sum, value) => sum + value, 0) + gap * Math.max(0, tokens.length - 1);
  let x = Math.max(80, (width - totalWidth) / 2);
  const y = layerHeight / 2;
  const currentIndex = current ? cue.words.indexOf(current) : -1;

  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];
    const isCurrent = index === currentIndex;
    ctx.lineWidth = 11;
    ctx.strokeStyle = "rgba(0,0,0,0.96)";
    ctx.strokeText(token, x, y);
    ctx.fillStyle = isCurrent ? "#ff334d" : "#ffffff";
    ctx.fillText(token, x, y);
    x += widths[index] + gap;
  }
}

const ffmpeg = spawn("ffmpeg", [
  "-hide_banner", "-loglevel", "error", "-y",
  "-f", "rawvideo", "-pix_fmt", "rgba", "-video_size", `${width}x${layerHeight}`,
  "-framerate", String(fps), "-i", "pipe:0",
  "-i", input,
  "-filter_complex", "[1:v]tpad=stop_mode=clone:stop_duration=1[base];[base][0:v]overlay=0:H-h-55:format=auto:shortest=1[v]",
  "-map", "[v]", "-map", "1:a?",
  "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
  "-r", String(fps), "-fps_mode", "cfr", "-video_track_timescale", String(Math.round(fps * 1000)),
  "-c:a", "copy", "-t", String(duration), "-movflags", "+faststart", output,
], { stdio: ["pipe", "inherit", "inherit"] });

ffmpeg.on("error", (error) => fail(`Unable to start ffmpeg: ${error.message}`));

for (let frame = 0; frame < frameCount; frame += 1) {
  const time = (frame + 0.5) / fps;
  drawCaption(activeCue(time), activeWord(time));
  const pixels = ctx.getImageData(0, 0, width, layerHeight).data;
  if (!ffmpeg.stdin.write(Buffer.from(pixels.buffer))) {
    await new Promise((resolve) => ffmpeg.stdin.once("drain", resolve));
  }
  if (frame % 900 === 0) console.log(`Caption frames: ${frame}/${frameCount}`);
}
ffmpeg.stdin.end();

const exitCode = await new Promise((resolve) => ffmpeg.on("close", resolve));
if (exitCode !== 0) fail(`ffmpeg exited with code ${exitCode}`);
console.log(`Captioned video: ${output}`);
