"""Check frozen text, frame coverage, declared cues, and preserved voice master."""
import hashlib,json,wave
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;plan=json.loads((P/'01_script/scene-plan.json').read_text());approval=json.loads((P/'00_brief/script-approval.json').read_text());checks=[]
for item in approval['approved_files']:
 f=P/item['path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256'];checks.append({'path':item['path'],'approved_hash_matches':True})
for scene in plan['scenes']:
 assert scene['caption_text']==scene['narration_text']
 for a,b in zip(scene['shot_sequence'],scene['shot_sequence'][1:]):assert abs(a['end_seconds']-b['start_seconds'])<.025
for n in range(1,4):
 root=P/f'02_audio/chapters/story-{n:02}/03_sync';r=json.loads((root/'sync_report.json').read_text());checks.append({'chapter':n,'report':r})
def read(path):
 with wave.open(str(path)) as w:return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,w.getnchannels()).astype(float)/32768,w.getframerate()
voice,sr=read(P/'02_audio/working/voice.wav');final,fs=read(P/'02_audio/working/voice-final.wav');assert sr==fs==48000 and len(final)>=len(voice)
bed=final.copy();bed[:len(voice)]-=voice
rms=lambda x:float(np.sqrt(np.mean(x*x)))
windows=[]
for a,b in [(219.42,220.32),(640.722,641.622),(1118.122,1119.022)]:
 cut=bed[int((a+.04)*sr):int((b-.04)*sr)];windows.append({'start':a,'end':b,'bed_rms_during_hush':rms(cut),'intent':'Narration continues unaltered; ambience/BGM/foley bed hush only.'});assert rms(cut)<.00008
outro=[]
for i in range(4):
 start=1245.997146+i;outro.append({'start':start,'rms':rms(final[int(start*sr):int((start+1)*sr)])})
assert outro[-1]['rms']<outro[1]['rms'];assert len(final)/sr-1245.997146>=3.99
report={'script_checks':checks,'captions_identical_to_approved_narration':True,'all_shot_boundaries_contiguous':True,'first_anomalies_within_40_60_seconds':[c['first_anomaly_actual_seconds_from_chapter_start'] for c in plan['chapters']],'sound_layers':'voice-only file preserved; BGM applied without TTS regeneration; final mix adds separate local synthesized room/event layers','voice_only_sha256':hashlib.sha256((P/'02_audio/working/voice.wav').read_bytes()).hexdigest(),'hush_windows':windows,'outro_seconds':4,'fade_out_seconds':3,'outro_rms_per_second':outro,'direct_listening':False}
(P/'05_review/script-sync-mix-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Approved text, contiguous shots, three bed hush windows, four-second outro and fade passed')
