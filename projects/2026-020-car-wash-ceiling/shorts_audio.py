"""Create pitch-preserved Shorts voice and independent alignment artifacts."""
import shutil
import json
import subprocess
import sys
from pathlib import Path

project = Path(__file__).resolve().parent
repo = project.parent.parent
shadow = project / '02_audio/working/shorts-shadow'
for directory in ['01_script', '02_audio/working', '03_sync', '04_composition']:
    (shadow / directory).mkdir(parents=True, exist_ok=True)
for name in ['narration.txt', 'tts-narration.txt']:
    shutil.copyfile(project / '01_script' / ('shorts-' + name), shadow / '01_script' / name)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(project / f'02_audio/inbox/{project.name}-shorts.mp3'), '-af', 'atempo=1.07', '-ar', '48000', '-ac', '2', str(shadow / '02_audio/working/voice.wav')], check=True)
subprocess.run([sys.executable, str(repo / 'scripts/trim_audio_pauses.py'), str(shadow), '--keep-pause', '0.4', '--replace'], check=True)
shutil.copyfile(shadow / '02_audio/working/voice.wav', shadow / '02_audio/working/voice-before-head-pad.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(shadow / '02_audio/working/voice-before-head-pad.wav'), '-af', 'afade=t=in:st=0:d=0.006,adelay=120|120', str(shadow / '02_audio/working/voice.wav')], check=True)
subprocess.run([sys.executable, str(repo / 'scripts/align_captions.py'), str(shadow), '--language', 'ko'], check=True)
for name in ['captions.srt', 'captions.vtt', 'captions.words.json', 'sync_report.json', 'whisper_raw.json']:
    shutil.copyfile(shadow / '03_sync' / name, project / '03_sync' / ('shorts-' + name))
shutil.copyfile(shadow / '02_audio/working/voice.wav', project / '04_composition/assets/audio/shorts-voice.wav')
report_path = project / '03_sync/shorts-sync_report.json'
report = json.loads(report_path.read_text())
report.update(subtitle_delivery_mode='burned_short_captions_and_external_srt_vtt', subtitle_text_source='01_script/shorts-narration.txt', spoken_text_source='01_script/shorts-tts-narration.txt', note='Independent Shorts narration; words drive both burned captions and external SRT/VTT. Main audio and captions are not reused.')
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
