# Final Verification

## Deliverables

- Long-form: `../06_delivery/youtube/2026-023-library-return-slot-youtube.mp4` (local, ignored by Git)
- Independent Short: `../06_delivery/shorts/2026-023-library-return-slot-shorts.mp4` (local, ignored by Git)
- External captions: `../03_sync/captions.srt`, `captions.vtt`, `shorts-captions.srt`, `shorts-captions.vtt`
- Publishing helpers: `../07_publish/youtube/youtube-publish.html`, `../07_publish/shorts/shorts-publish.html`
- Two thumbnails: `../07_publish/youtube/thumbnail-a.jpg`, `thumbnail-b.jpg`

## Automated Media Checks

| Check | Long-form | Short |
|---|---:|---:|
| Format | 1920x1080, 16:9 | 1080x1920, 9:16 |
| Frame rate | 60/1 fps | 60/1 fps |
| Codec | H.264 video, AAC audio | H.264 video, AAC audio |
| Duration | 477.233 s | 27.833 s |
| Audio duration | 477.227 s | 27.819 s |
| Audio peak | -2.9 dBFS | -2.9 dBFS |
| Freeze detection | None >= 3 s at -50 dB threshold | None >= 3 s at -50 dB threshold |
| Whisper alignment | 99.19% | 100.00% |

The final 0.4 s of the long-form outro measured -80.3 dB mean / -68.7 dB peak; the Short measured -51.2 dB mean / -40.1 dB peak. Both fade smoothly instead of cutting off. Short voice-only audio has a 0.1 s silent head pad before the first syllable; no first-word clipping detected by waveform measurement. Final audio/video streams start at 0 and agree within 0.021 s.

## Visual Review

All 44 long-form images and six independently generated portrait Short images received full-size and narrative-order reviews; see `image-review.md`. The encoded contact sheet and selected full-resolution frames cover opening, first anomaly, entity reveal, scissors, stair escape, aftermath, coat ending, and end screen. The first Short frame, middle captions, and final complete-sentence cliffhanger were inspected. No clipped title, overlapping card, unexpected face, premature spoiler, or 3-second static interval was observed. The two final thumbnail overlays are legible at 1280x720 and use different visual clues.

## Audio And Text Review

Approved Korean narration is unchanged in the published SRT/VTT. Five of 961 forced-aligned words were not exact Whisper surface matches: one number-normalization token (`다섯`/`5`) and four close ASR spellings or phonetic confusions (`문`/`분`, `너머`/`넘어`, `닫힌`/`다친`, `손은`/`소는`). They were not silently rewritten into the subtitles. The remaining timing follows the approved script. Pacing diagnostics found zero long silences; ten 0.8-0.96 s gaps are at sentence boundaries. An end-truncated window and six windows at 136-144 WPM were reviewed as pacing flags, not automatic failures. Voice-only originals remain preserved; no TTS was rerun during BGM or sound-design mixing. Separate quiet ambience and event-foley layers were added and peak-tested.

Direct human auditory judgment is unavailable in this environment, so tonal nuance and any TTS homophone should still be checked by ear before public upload. No upload or scheduling was performed.
