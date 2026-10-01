"""Build the independently approved Short voice and its own caption timing."""

import json
import shutil
import subprocess
import sys
from pathlib import Path


project = Path(__file__).resolve().parent
repo = project.parent.parent
shadow = project / "02_audio/working/shorts-shadow"
for directory in ("01_script", "02_audio/working", "03_sync", "04_composition"):
    (shadow / directory).mkdir(parents=True, exist_ok=True)

for name in ("narration.txt", "tts-narration.txt"):
    shutil.copyfile(project / "01_script" / ("shorts-" + name), shadow / "01_script" / name)

source = project / "02_audio/inbox" / f"{project.name}-shorts.mp3"
voice = shadow / "02_audio/working/voice.wav"
subprocess.run(
    [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-af", "atempo=1.07,adelay=100|100", "-ar", "48000", "-ac", "2", str(voice),
    ],
    check=True,
)
subprocess.run(
    [sys.executable, str(repo / "scripts/align_captions.py"), str(shadow), "--language", "ko"],
    check=True,
)
for name in ("captions.srt", "captions.vtt", "captions.words.json", "sync_report.json", "whisper_raw.json"):
    shutil.copyfile(shadow / "03_sync" / name, project / "03_sync" / ("shorts-" + name))
render_voice = project / "04_composition/assets/audio/shorts-voice.wav"
render_voice.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(voice, render_voice)

report_path = project / "03_sync/shorts-sync_report.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
report.update(
    subtitle_delivery_mode="burned_short_captions_and_external_srt_vtt",
    subtitle_text_source="01_script/shorts-narration.txt",
    spoken_text_source="01_script/shorts-tts-narration.txt",
    note="Independent Eleven V3 Short voice; pitch-preserved 1.07x postprocess and 0.1 s head pad. No long-form audio or image reuse.",
)
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Short voice: {render_voice}")
