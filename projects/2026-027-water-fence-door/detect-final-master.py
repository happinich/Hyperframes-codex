"""Decode the complete final master and record freeze/black/silence findings."""
from pathlib import Path
import json
import hashlib
import re
import subprocess

P = Path(__file__).resolve().parent
video = P / f'06_delivery/youtube/{P.name}-youtube.mp4'
log = P / '05_review/logs/youtube-final-detect.log'
cmd = ['ffmpeg', '-hide_banner', '-nostats', '-threads', '2',
       '-filter_threads', '2', '-i', str(video),
       '-vf', 'freezedetect=n=-55dB:d=3,blackdetect=d=1:pix_th=0.03:pic_th=0.98',
       '-af', 'silencedetect=n=-45dB:d=0.8', '-f', 'null', '-']
with log.open('w') as stream:
    run = subprocess.run(cmd, stdout=stream, stderr=subprocess.STDOUT)
text = log.read_text()
freeze = re.findall(r'freeze_start:\s*([\d.]+)', text)
black = re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)', text)
silence_starts = re.findall(r'silence_start:\s*([\d.]+)', text)
silence = [{'end': float(end), 'duration': float(duration),
            'start': float(end) - float(duration)} for end, duration in
           re.findall(r'silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)', text)]
plan = json.loads((P / '01_script/scene-plan.json').read_text())
planned = [s for s in plan['scenes'] if s.get('audio', {}).get('intentional_silence')]
unplanned = []
for interval in silence:
    match = next((s for s in planned
                  if interval['start'] >= s['start_seconds'] - 0.3
                  and interval['end'] <= s['end_seconds'] + 0.3), None)
    if match:
        interval.update({'classification': 'planned_narration_rest_with_low_background',
                         'scene': match['id'], 'plan': match['audio']['intentional_silence'],
                         'review': 'Timeline and measured interval compared; subjective listening unavailable'})
    else:
        unplanned.append(interval)
if len(silence_starts) != len(silence):
    unplanned.append({'reason': 'Unclosed silence interval requires inspection'})
errors = [line for line in text.splitlines()
          if re.search(r'Error while|Invalid data|corrupt decoded|non monoton', line, re.I)]
data = {'file': str(video.relative_to(P)), 'sha256': hashlib.sha256(video.read_bytes()).hexdigest(), 'exit_code': run.returncode,
        'decoded_entire_master': run.returncode == 0,
        'freeze_threshold_seconds': 3, 'freeze_noise_db': -55,
        'freeze_starts': freeze, 'black_threshold_seconds': 1,
        'black_intervals': black, 'silence_threshold_seconds': 0.8,
        'silence_noise_db': -45, 'silence_intervals': silence, 'unplanned_silence_intervals': unplanned,
        'decode_errors': errors,
        'result': 'passed' if run.returncode == 0 and not (freeze or black or unplanned or errors) else 'requires_review',
        'subjective_audio_listening': 'not_performed'}
(P / '05_review/final-master-detection.json').write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps(data, indent=2))
if run.returncode:
    raise SystemExit(run.returncode)
