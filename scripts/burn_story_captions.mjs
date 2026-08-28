#!/usr/bin/env node
/** Burn restrained phrase captions for long-form narration and review samples. */

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

function option(name, fallback) {
  const index = process.argv.indexOf(name);
  if (index === -1) return fallback;
  const value = Number(process.argv[index + 1]);
  if (!Number.isFinite(value) || value < 0) fail(`Invalid ${name} value`);
  return value;
}

const projectArg = process.argv[2];
if (!projectArg) {
  fail("Usage: node scripts/burn_story_captions.mjs <project> [--sample-start 0] [--sample-duration 60]");
}

const project = path.resolve(projectArg);
const projectId = path.basename(project);
const repositoryRoot = path.resolve(project, "..", "..");
const rulesPath = path.join(repositoryRoot, "config", "success-rules.json");
const input = path.join(project, "06_delivery", "youtube", `${projectId}-youtube.mp4`);
const timingPath = path.join(project, "03_sync", "captions.words.json");
const sampleStart = option("--sample-start", 0);
const requestedDuration = option("--sample-duration", 0);

if (!fs.existsSync(input)) fail(`Missing approved master: ${input}`);
if (!fs.existsSync(timingPath)) fail(`Missing caption timings: ${timingPath}`);
if (!fs.existsSync(rulesPath)) fail(`Missing success rules: ${rulesPath}`);

const successRules = JSON.parse(fs.readFileSync(rulesPath, "utf8"));
const captionRules = successRules.defaults.subtitles.post_review_captioned_version;

const probe = spawnSync("ffprobe", [
  "-v", "error",
  "-select_streams", "v:0",
  "-show_entries", "format=duration:stream=r_frame_rate,avg_frame_rate",
  "-of", "json",
  input,
], { encoding: "utf8" });
if (probe.status !== 0) fail(probe.stderr || "ffprobe failed");

function frameRate(value) {
  const [numerator, denominator = "1"] = String(value || "").split("/");
  const result = Number(numerator) / Number(denominator);
  return Number.isFinite(result) && result > 0 ? result : 60;
}

const media = JSON.parse(probe.stdout);
const sourceDuration = Number.parseFloat(media.format.duration);
const videoStream = media.streams?.[0] || {};
const fps = frameRate(videoStream.r_frame_rate || videoStream.avg_frame_rate);
const duration = requestedDuration > 0
  ? Math.min(requestedDuration, Math.max(0, sourceDuration - sampleStart))
  : Math.max(0, sourceDuration - sampleStart);
if (duration <= 0) fail("Sample starts after the end of the video");

const isSample = requestedDuration > 0;
const output = isSample
  ? path.join(project, "05_review", "preview", `${projectId}-story-caption-sample-${Math.round(duration)}s.mp4`)
  : path.join(project, "06_delivery", "youtube", `${projectId}-youtube${captionRules.output_suffix}.mp4`);
fs.mkdirSync(path.dirname(output), { recursive: true });

const width = 1920;
const layerHeight = 150;
const maxTextWidth = captionRules.max_text_width_px;
const fontSize = captionRules.font_size_px;
const fontWeight = captionRules.font_weight;
const outlineWidth = captionRules.outline_width_px;
const maxGlyphsPerCue = captionRules.max_glyphs_per_cue;
const frameCount = Math.ceil(duration * fps);
const timing = JSON.parse(fs.readFileSync(timingPath, "utf8"));

function semanticCues(words) {
  const cues = [];
  const pending = [];
  const connectors = new Set(["그리고", "하지만", "그런데", "그러나", "그래서", "결국", "문제는"]);

  function flush() {
    if (pending.length === 0) return;
    cues.push({
      start: pending[0].start,
      end: pending[pending.length - 1].end,
      text: pending.map((word) => word.text).join(" "),
    });
    pending.length = 0;
  }

  words.forEach((word, index) => {
    const candidateText = [...pending, word].map((item) => item.text).join(" ");
    const candidateGlyphs = candidateText.replace(/\s/gu, "").length;
    if (pending.length > 0 && candidateGlyphs > maxGlyphsPerCue) flush();

    pending.push(word);
    const next = words[index + 1];
    const text = pending.map((item) => item.text).join(" ");
    const glyphCount = text.replace(/\s/gu, "").length;
    const plainWord = word.text.replace(/[.,!?，。“”'’")\]]/gu, "");
    const terminal = /[.!?][”"'’\)\]]?$/u.test(word.text);
    const commaBreak = /[,，][”"'’\)\]]?$/u.test(word.text) && glyphCount >= 12;
    const pauseBreak = next && next.start - word.end >= 0.7 && !connectors.has(plainWord);
    const lengthBreak = glyphCount >= maxGlyphsPerCue && !connectors.has(plainWord);
    if (!next || terminal || commaBreak || pauseBreak || lengthBreak) flush();
  });
  return cues;
}

const cues = semanticCues(timing.words);
const maxCueGlyphs = Math.max(...cues.map((cue) => cue.text.replace(/\s/gu, "").length));
const maxCueDuration = Math.max(...cues.map((cue) => cue.end - cue.start));
console.log(`Story caption cues: ${cues.length}; max glyphs: ${maxCueGlyphs}; max duration: ${maxCueDuration.toFixed(2)}s`);
const canvas = createCanvas(width, layerHeight);
const ctx = canvas.getContext("2d");
ctx.font = `${fontWeight} ${fontSize}px "Apple SD Gothic Neo", "Noto Sans CJK KR", Arial, sans-serif`;
ctx.textAlign = "center";
ctx.textBaseline = "middle";
ctx.lineJoin = "round";
ctx.miterLimit = 2;

let cueIndex = 0;
while (cueIndex < cues.length - 1 && cues[cueIndex].end <= sampleStart) cueIndex += 1;

function activeCue(time) {
  while (cueIndex < cues.length - 1 && time >= cues[cueIndex].end) cueIndex += 1;
  const cue = cues[cueIndex];
  return cue && time >= cue.start && time < cue.end ? cue : null;
}

function drawCaption(cue) {
  ctx.clearRect(0, 0, width, layerHeight);
  if (!cue) return;

  const caption = cue.text.trim();
  const x = width / 2;
  const y = layerHeight / 2;
  ctx.shadowColor = "rgba(0,0,0,.95)";
  ctx.shadowBlur = 12;
  ctx.shadowOffsetY = 3;
  ctx.lineWidth = outlineWidth;
  ctx.strokeStyle = captionRules.outline_color;
  ctx.strokeText(caption, x, y, maxTextWidth);
  ctx.fillStyle = captionRules.base_text_color;
  ctx.fillText(caption, x, y, maxTextWidth);
  ctx.shadowColor = "transparent";
}

const ffmpegArgs = ["-hide_banner", "-loglevel", "error", "-y"];
ffmpegArgs.push(
  "-f", "rawvideo", "-pix_fmt", "rgba", "-video_size", `${width}x${layerHeight}`,
  "-framerate", String(fps), "-i", "pipe:0",
);
if (sampleStart > 0) ffmpegArgs.push("-ss", String(sampleStart));
ffmpegArgs.push(
  "-i", input,
  "-filter_complex", "[1:v][0:v]overlay=0:H-h-60:format=auto[v]",
  "-map", "[v]", "-map", "1:a?",
  "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
  "-r", String(fps), "-fps_mode", "cfr", "-video_track_timescale", String(Math.round(fps * 1000)),
  "-c:a", "copy", "-t", String(duration), output,
);

const ffmpeg = spawn("ffmpeg", ffmpegArgs, { stdio: ["pipe", "inherit", "inherit"] });
ffmpeg.on("error", (error) => fail(`Unable to start ffmpeg: ${error.message}`));

for (let frame = 0; frame < frameCount; frame += 1) {
  const localTime = (frame + 0.5) / fps;
  drawCaption(activeCue(sampleStart + localTime));
  const pixels = ctx.getImageData(0, 0, width, layerHeight).data;
  if (!ffmpeg.stdin.write(Buffer.from(pixels.buffer))) {
    await new Promise((resolve) => ffmpeg.stdin.once("drain", resolve));
  }
  if (frame % 900 === 0) console.log(`Story caption frames: ${frame}/${frameCount}`);
}
ffmpeg.stdin.end();

const exitCode = await new Promise((resolve) => ffmpeg.on("close", resolve));
if (exitCode !== 0) fail(`ffmpeg exited with code ${exitCode}`);
console.log(`Story caption video: ${output}`);
