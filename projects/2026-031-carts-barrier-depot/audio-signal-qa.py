import json,subprocess,wave,hashlib
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;out=[]
for f in [P/'02_audio/working/voice-final.wav']+[P/f'02_audio/sound-design/shorts-{n:02}-bgm.wav' for n in range(1,4)]:
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);tail=r.stderr[r.stderr.rfind('{'):];j=json.JSONDecoder().raw_decode(tail)[0]
 with wave.open(str(f)) as w:x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,w.getnchannels())/32768;sr=w.getframerate();duration=len(x)/sr
 out.append({'file':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'duration':duration,'sample_rate':sr,'channels':x.shape[1],'peak_dbfs':float(20*np.log10(max(np.max(np.abs(x)),1e-9))),'first_100ms_peak':float(np.max(np.abs(x[:int(.1*sr)]))),'last_100ms_peak':float(np.max(np.abs(x[-int(.1*sr):]))),'clipped_samples':int(np.sum(np.abs(x)>=.99997)),'loudness':j,'direct_listening':False,'review_scope':'Whisper text reconciliation, signal levels, deliberate silence windows and mix separation; no subjective ear assessment claimed.'})
(P/'05_review/final-audio-signal-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print([(a['file'],a['loudness']['input_i'],a['loudness']['input_tp'],a['clipped_samples']) for a in out])
