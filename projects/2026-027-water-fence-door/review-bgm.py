"""Compare measured masking and event tags of four newly generated music tracks."""
from pathlib import Path
import json, subprocess, numpy as np, re
P=Path(__file__).resolve().parent
metrics=[]
for f in sorted((P/'02_audio/bgm/candidates').glob('*.mp3')):
    detect=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True).stderr
    samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
    blocks=samples[:len(samples)//4096*4096].reshape(-1,4096)
    spectrum=np.mean(np.abs(np.fft.rfft(blocks*np.hanning(4096),axis=1))**2,axis=0);freq=np.fft.rfftfreq(4096,1/16000)
    power=lambda lo,hi:float(spectrum[(freq>=lo)&(freq<hi)].sum()/spectrum.sum())
    scribe=json.loads((P/f'05_review/scribe-bgm-{f.stem[-2:]}.json').read_text())
    spoken=[w for w in scribe.get('words',[]) if w.get('type')=='word' and any(c.isalnum() for c in w.get('text',''))]
    events=[w.get('text') for w in scribe.get('words',[]) if w.get('type')=='audio_event']
    entry={'id':f.stem,'duration_seconds':len(samples)/16000,'mean_db':float(re.search(r'mean_volume: ([\-\d.]+)',detect)[1]),'peak_db':float(re.search(r'max_volume: ([\-\d.]+)',detect)[1]),'low_band_fraction':power(20,300),'speech_band_fraction':power(500,4000),'recognized_words':spoken,'audio_events':events,'rms_seconds':[float(np.sqrt(np.mean(x*x))) for x in np.array_split(samples,60)]}
    metrics.append(entry)
valid=[m for m in metrics if m['peak_db']<-.1 and -36<m['mean_db']<-10 and not m['recognized_words']]
assert valid,'All candidates require repair/review; no valid instrumental candidate'
chosen=min(valid,key=lambda m:m['speech_band_fraction'])
review={'status':'selected_under_user_delegation_measured_review','selected_candidate':chosen['id'],'review_pass_1':'Duration, peak, mean level, spectral masking and envelopes compared across four new tracks; independent Scribe event/word tagging checks recognizable voices.','review_pass_2':'Pending mixed preview/outro clipping and narration-preservation checks after application.','subjective_listening':'Unavailable. No subjective ear-based genre/emotion review is claimed.','candidates':metrics}
(P/'05_review/bgm-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'selected':chosen['id'],'metrics':[{k:v for k,v in m.items() if k!='rms_seconds'} for m in metrics]},ensure_ascii=False,indent=2))
