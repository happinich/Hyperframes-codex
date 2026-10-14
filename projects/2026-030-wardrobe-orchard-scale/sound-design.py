"""Add quiet original room tone and timed object sounds without altering the voice master."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parents[1] / 'scripts'))
from audio_mixing import mix_bgm_with_voice

SR = 48000
plan_path = P / '01_script/scene-plan.json'
plan = json.loads(plan_path.read_text())
scenes = {s['id']: s for s in plan['scenes']}
duration = plan['end_screen_end_seconds']
D = P / '02_audio/sound-design'
D.mkdir(exist_ok=True)
rng = np.random.default_rng(30)

def save(path, data):
    if data.ndim == 1:
        data = np.column_stack((data, data))
    with wave.open(str(path), 'wb') as f:
        f.setparams((2, 2, SR, 0, 'NONE', 'not compressed'))
        f.writeframes((np.clip(data, -1, 1) * 32767).astype('<i2').tobytes())

def clean(s):
    return re.sub(r'[^가-힣0-9A-Za-z]', '', s)

timing = {}
for num, chapter in enumerate(plan['chapters'], 1):
    words = json.loads((P / f'02_audio/chapters/story-{num:02}/03_sync/captions.words.json').read_text())['words']
    for s in plan['scenes']:
        if s['chapter_id'] != chapter['id']:
            continue
        local_start = s['start_seconds'] - chapter['start_seconds']
        local_end = s['end_seconds'] - chapter['start_seconds']
        timing[s['id']] = [(w['text'], w['start'] + chapter['start_seconds'])
                           for w in words if local_start - .2 <= w['start'] < local_end + .2]

def locate(sid, phrase):
    words = timing[sid]
    target = clean(phrase)
    for i in range(len(words)):
        line = ''
        for j in range(i, min(len(words), i + 8)):
            line += clean(words[j][0])
            if target in line:
                return words[i][1]
    raise ValueError(f'No timing for {sid}: {phrase}')

specs = [('C01-S04', '장롱 옆을', 'click'), ('C01-S05', '발바닥이', 'fabric'), ('C01-S07', '창문을', 'click'), ('C01-S09', '의자 다리 하나가', 'door'), ('C01-S11', '한 손이', 'door'), ('C01-S12', '가슴에 닿았어요', 'thud'), ('C01-S13', '가로대 하나가', 'snip'), ('C01-S14', '장롱이 바닥을', 'door'), ('C02-S04', '호스를', 'fabric'), ('C02-S07', '밑동이', 'door'), ('C02-S11', '발등을', 'fabric'), ('C02-S13', '쇠막대로', 'metal'), ('C02-S14', '지지대들이', 'metal'), ('C02-S17', '나무뿌리가', 'click'), ('C03-S05', '영점 단추를', 'click'), ('C03-S06', '좌판 가운데가', 'door'), ('C03-S07', '빗자루 끝이', 'thud'), ('C03-S08', '창고문에서', 'metal'), ('C03-S13', '조회 단추를', 'click'), ('C03-S14', '단추가 눌렸습니다', 'click'), ('C03-S16', '전자음이', 'click'), ('C03-S17', '문턱 바닥이', 'thud')]

lengths = {'fabric': .52, 'click': .14, 'snip': .23, 'thud': .37,
           'metal': .58, 'key': .44, 'gravel': .66, 'door': .78}
foley = {}
for kind, length in lengths.items():
    t = np.arange(round(length * SR)) / SR
    noise = rng.normal(0, 1, len(t))
    noise = sosfilt(butter(2, [150, 3600], btype='bandpass', fs=SR, output='sos'), noise)
    noise /= max(np.max(np.abs(noise)), 1e-9)
    if kind == 'thud':
        x = np.sin(2 * np.pi * (83 * t - 24 * t * t)) * np.exp(-13 * t) + .13 * noise
    elif kind == 'metal':
        x = .65 * np.sin(2 * np.pi * 540 * t) * np.exp(-7 * t) + .3 * np.sin(2 * np.pi * 970 * t) * np.exp(-12 * t) + .08 * noise
    elif kind == 'key':
        x = .5 * np.sin(2 * np.pi * 1610 * t) * np.exp(-10 * t) + .3 * np.sin(2 * np.pi * 2330 * t) * np.exp(-13 * t) + .07 * noise
    elif kind == 'click':
        x = noise * np.exp(-43 * t)
    elif kind == 'snip':
        x = noise * (np.exp(-55 * t) + .65 * np.exp(-70 * np.maximum(0, t-.10)) * (t >= .10))
    else:
        x = noise * (.65 + .35 * np.sin(2 * np.pi * (16 if kind == 'fabric' else 9) * t))
    env = np.minimum(1, t / .012) * np.minimum(1, (length - t) / .07)
    x = x * env
    x = x / max(np.max(np.abs(x)), 1e-9) * (.015 if kind in ('thud', 'metal') else .008)
    foley[kind] = x
    save(D / f'foley-{kind}.wav', x)

events = []
for sid, phrase, kind in specs:
    at = locate(sid, phrase)
    event = {'scene_id': sid, 'spoken_cue': phrase, 'start_seconds': round(at, 3),
             'kind': kind, 'duration_seconds': lengths[kind]}
    events.append(event)
    scenes[sid]['audio'].setdefault('foley_events', []).append(event)
    scenes[sid]['audio']['bgm'] = 'approved_cand-04'
    scenes[sid]['audio']['room_ambience'] = 'original_generated_layer'

for s in plan['scenes']:
    s['audio']['bgm'] = 'approved_cand-04'
    s['audio']['room_ambience'] = 'original_generated_layer'

sources = {}
for n, (freq, cutoff) in enumerate([(54, 700), (0, 550), (115, 570)], 1):
    t = np.arange(24 * SR) / SR
    noise = sosfilt(butter(2, cutoff, fs=SR, output='sos'), rng.normal(0, 1, len(t)))
    noise /= max(np.max(np.abs(noise)), 1e-9)
    x = .0018 * np.sin(2 * np.pi * freq * t) + .0011 * noise
    sources[n] = x
    save(D / f'room-{n:02}.wav', x)

def write_bus(path, ambient=False, chapter=None, events_for_bus=None, seconds=None):
    total = duration if seconds is None else seconds
    with wave.open(str(path), 'wb') as out:
        out.setparams((2, 2, SR, 0, 'NONE', 'not compressed'))
        for start in range(0, round(total * SR), SR):
            n = min(SR, round(total * SR) - start)
            indices = np.arange(start, start + n)
            t = indices / SR
            x = np.zeros(n)
            if ambient:
                chapters = [plan['chapters'][chapter - 1]] if chapter else plan['chapters']
                for c in chapters:
                    num = int(c['id'][-1])
                    begin = 0 if chapter else c['start_seconds']
                    end = total if chapter else c['end_seconds']
                    fade = np.clip((t - begin)/.65, 0, 1) * np.clip((end - t)/1.2, 0, 1)
                    x += sources[num][indices % len(sources[num])] * fade
            else:
                for event in events_for_bus or events:
                    pos = round(event['start_seconds'] * SR)
                    signal = foley[event['kind']]
                    lo = max(start, pos)
                    hi = min(start + n, pos + len(signal))
                    if hi > lo:
                        x[lo-start:hi-start] += signal[lo-pos:hi-pos]
            out.writeframes((np.column_stack((x, x)) * 32767).astype('<i2').tobytes())

write_bus(D / 'ambience-bus.wav', ambient=True)
write_bus(D / 'foley-bus.wav')
voice = P / '02_audio/working/voice.wav'
voice_hash = hashlib.sha256(voice.read_bytes()).hexdigest()
master = P / '02_audio/working/voice-final.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(P / '02_audio/working/voice-bgm.wav'),
                '-i', str(D / 'ambience-bus.wav'), '-i', str(D / 'foley-bus.wav'),
                '-filter_complex', '[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first:dropout_transition=0[a]',
                '-map', '[a]', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', str(master)], check=True)
shutil.copy2(master, P / '04_composition/assets/audio/voice.wav')
for number in range(1, 4):
    short = P / f'02_audio/shorts/shorts-{number:02}/02_audio/working/voice.wav'
    with_bgm = D / f'shorts-{number:02}-bgm.wav'
    mix_bgm_with_voice(voice_audio=short, bgm_audio=P / '02_audio/bgm/candidates/cand-04.mp3',
                       target_audio=with_bgm, gain_db=-20, outro_seconds=0, fade_out_seconds=.45,
                       output_codec_args=['-c:a', 'pcm_s16le'])
    # The portrait composition uses this independent sound master.
    shutil.copy2(with_bgm, P / f'04_composition/assets/audio/shorts-{number:02}.wav')
assert hashlib.sha256(voice.read_bytes()).hexdigest() == voice_hash
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
(P / '05_review/sound-design-review.json').write_text(json.dumps({
    'status': 'signal_review_pending', 'provenance': 'Original deterministic numpy/scipy synthesis; no external sampled recordings',
    'voice_only_sha256': voice_hash, 'voice_master_preserved': True, 'bgm_candidate': 'cand-04',
    'events': events, 'ambience_and_foley_separate_layers': True, 'shorts_outro_delay_seconds': 0,
    'subjective_listening_performed': False
}, ensure_ascii=False, indent=2) + '\n')
print(f'Added room tone and {len(events)} timed effects to approved BGM; three Shorts mixed separately.')
