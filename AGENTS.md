# Hyperframes-codex Agent Instructions

## Scope

These instructions apply to the entire `Hyperframes-codex` repository.

This repository is the standalone Hyperframes production workspace. Do not edit,
sync, or assume a runtime dependency on `/Users/happinich/Documents/Remotion-codex`.
Remotion-codex is a separate repository that may reuse production ideas, but
changes do not propagate between the two projects automatically.

## Canonical Rules

Before planning or editing a video project, read:

1. `config/success-rules.json`
2. `config/production-profiles.json`
3. `config/visual-styles.json`
4. `docs/WORKFLOW.ko.md`
5. `docs/SUCCESS_RULES.ko.md`
6. The latest relevant project that uses the same production profile

Treat the JSON configuration as the source of truth for numeric settings. Keep
the documentation and templates in sync when a shared rule changes.

## Worktree Safety

- Assume the worktree can already contain user changes, removed projects, local
  media, or generated outputs.
- Never restore, revert, delete, or rewrite changes that were not made for the
  current request.
- Never reopen or modify a completed project unless the user explicitly asks to
  revise that project.
- Keep each new video isolated under `projects/<project-id>/`.
- Keep edits focused. Do not refactor unrelated pipeline code while producing a
  video.

## Required Approval Gates

Follow these gates for every new long-form production:

1. Gather the topic, supplied sources, target duration, audience, and goal.
2. Research current or unstable claims when necessary.
3. Write the complete narration and a second-level scene plan.
4. Show the complete narration and wait for explicit approval.
5. Present the production profile and compatible visual-style options.
6. Wait for explicit visual-style approval.
7. Generate voice, then create the Hyperframes composition.
8. After the voice review passes, generate BGM candidates and wait for explicit
   BGM approval. Apply the approved track with `scripts/apply_bgm.py`, which
   never re-runs TTS, and extend the composition outro by the configured delay.

Script approval, visual-style approval, and BGM approval are separate. Do not
silently carry a previous project's style or BGM into a new project.

## Script And Scene Planning

- Start within three seconds with a sharp question, important number, reversal,
  or high-stakes claim. Remove greetings and slow setup.
- Write short, conversational Korean suitable for ElevenLabs V3.
- Preserve the user's argument and intended energy while checking factual claims.
- Make `01_script/narration.txt` the approved text source of truth.
- Keep `caption_text` identical to `narration_text`.
- Plan one claim per scene and at least one meaningful visible change every one
  to three seconds.
- Derive final scene boundaries from the actual narration timing, not estimates.
- Prevent oversized titles, single-character orphan lines, clipped text, and
  overlapping cards or diagrams.
- Do not display a total-runtime badge in the video.
- Plan both 16:9 YouTube delivery and a separately composed 9:16 Shorts version.

## Audio And Timing

- Use ElevenLabs model `eleven_v3` and the voice settings in
  `config/success-rules.json`.
- Split long text at sentence boundaries into approximately 1,000-1,300
  characters, generate chunks sequentially, and concatenate them without gaps.
- Keep API keys only in environment variables. Never place a real key in source,
  Markdown, JSON, logs, commits, or final responses.
- Preserve the voice-only master when mixing BGM.
- Apply the configured BGM ducking, outro delay, and fade-out settings.
- Use `mlx-community/whisper-large-v3-turbo` as the timing and correction model.
- Whisper supplies timing; it must not rewrite the approved narration.
- Require a caption alignment ratio of at least `0.92` and manually review long
  pauses, stretched speech, and unexplained word gaps.
- Prepare relevant visuals about 0.35 seconds before the associated spoken point
  when it improves perceived synchronization.

## Visual Production

- Keep the production face-free unless the user explicitly requests otherwise.
- Use `minimal_dark_tech_v1` as the preferred profile for new projects, but still
  obtain visual-style approval.
- Preserve `classic_rich_motion_v1` for the existing bright/editorial, finance,
  collage, map, table, and hub-diagram grammar.
- For horror stories, establish consistent character, location, period, palette,
  lighting, and horror-intensity references before generating scene images.
- Animate still images with deliberate pans, zooms, parallax, fog, shadow,
  lighting, focus, or crop changes that support the narration.
- Avoid a static explanatory screen longer than three seconds.
- Animate tables, charts, routes, connectors, and comparisons instead of showing
  them as motionless illustrations.
- Use only local, licensed, generated, or otherwise permitted visual assets.

## Frame Rate And Delivery

- New YouTube projects default to `1920x1080`, 16:9, 60fps.
- New Shorts projects default to `1080x1920`, 9:16, 60fps.
- Frame rate improves motion smoothness; narration synchronization still depends
  on Whisper timings and correctly planned motion beats.
- Preserve the fps recorded in completed projects. If no fps is recorded, the
  renderer must preserve an existing completed master's detected fps.
- Render a clean master first. Create the captioned derivative only after the
  clean master passes review.
- Keep SRT and VTT as separate uploadable caption files.
- Minimal dark projects use phrase captions. Classic projects use word-following
  karaoke captions unless the approved project brief says otherwise.

## Standard Commands

List available profiles and styles:

```bash
python3 scripts/new_project.py --list-production-profiles
python3 scripts/new_project.py --list-visual-styles
```

Create an approved project:

```bash
python3 scripts/new_project.py <project-id> \
  --title "<title>" \
  --production-profile <approved-profile-id> \
  --visual-style <approved-style-id>
```

Process narration and timing:

```bash
python3 scripts/create_planned_captions.py <project>
python3 scripts/generate_elevenlabs_audio.py <project> --replace --postprocess
python3 scripts/align_captions.py <project> --language ko
python3 scripts/analyze_audio_pacing.py <project> --language ko
```

Choose and apply BGM (after the voice review passes):

```bash
python3 scripts/generate_bgm_candidates.py <project>
python3 scripts/apply_bgm.py <project> --candidate cand-02 --dry-run
python3 scripts/apply_bgm.py <project> --candidate cand-02
```

Validate and render:

```bash
npm run hf:lint -- <project>/04_composition
python3 scripts/render_project.py <project> --format youtube --dry-run
python3 scripts/render_project.py <project> --format youtube
```

Create the approved profile-specific captioned version:

```bash
node scripts/burn_phrase_captions.mjs <project>
node scripts/burn_karaoke_captions.mjs <project>
```

Run only the caption renderer assigned to the project's production profile.

## Review Requirements

Before declaring a video complete:

- Verify resolution, aspect ratio, fps, codecs, audio stream, and duration with
  `ffprobe`.
- Check audio/video duration agreement and the final BGM outro.
- Run freeze detection and inspect every static interval over the allowed limit.
- Inspect early, middle, late, data-heavy, diagram, transition, and ending frames.
- Confirm that titles fit and no text or shapes overlap.
- Confirm that visual events match the spoken narration throughout the video.
- Inspect the captioned output separately for timing, safe-area placement,
  readability, and dropped frames.

## Publishing Package

Each finished YouTube project should include:

- Clean 1920x1080 MP4
- Profile-specific captioned MP4
- SRT and VTT files
- Two readable, provocative 1280x720 thumbnails
- One HTML YouTube publishing helper with copy buttons
- One main title and five alternative titles
- Description with accurate timestamps, sources, hashtags, and tags
- Pinned comment, SNS promotional copy, and recommended publishing time

Keep publishing assets under `07_publish/`. Do not claim that an artifact exists
until it has been generated and verified.

## Git And Generated Media

- Respect `.gitignore`; source recordings, local music, preview frames, and render
  outputs normally remain local.
- Never commit secrets, API credentials, private tokens, or downloaded media with
  unclear rights.
- Do not stage, commit, or push unless the user explicitly requests it.
- When committing, include only the files relevant to the approved task and leave
  unrelated worktree changes untouched.
