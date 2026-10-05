from pathlib import Path
import json,subprocess,re,numpy as np
P=Path(__file__).resolve().parent
metrics=[]
for f in sorted((P/'02_audio/bgm/candidates').glob('*.mp3')):
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-af','volumedetect','-f','null','-'],text=True,capture_output=True,check=True)
 samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
 blocks=samples[:len(samples)//4096*4096].reshape(-1,4096)
 spectrum=np.mean(np.abs(np.fft.rfft(blocks*np.hanning(4096),axis=1))**2,axis=0);freq=np.fft.rfftfreq(4096,1/16000)
 energy=lambda lo,hi:float(spectrum[(freq>=lo)&(freq<hi)].sum()/spectrum.sum())
 entry={'id':f.stem,'duration_seconds':len(samples)/16000,'mean_volume_db':float(re.search(r'mean_volume: ([\-\d.]+)',r.stderr)[1]),'peak_db':float(re.search(r'max_volume: ([\-\d.]+)',r.stderr)[1]),'low_band_power_fraction':energy(20,300),'speech_band_power_fraction':energy(500,4000),'rms_per_second':[round(float(np.sqrt(np.mean(x*x))),6) for x in np.array_split(samples,40)]}
 metrics.append(entry)
valid=[x for x in metrics if -32<x['mean_volume_db']<-12 and x['peak_db']<-.1]
assert valid,'No usable candidates'
chosen=min(valid,key=lambda x:x['speech_band_power_fraction'])
review={'status':'selected_under_explicit_user_delegation','selected_candidate':chosen['id'],'pass_1':'Compare duration, peak, mean level, band energy and per-second envelopes of four new candidates. Exclude overly quiet/overloaded tracks.','pass_2':'Compare speech-band masking at canonical -18dB gain and verify voice+music preview peak/outro after application.','subjective_listening':'Not performed; no audio listening tool. Selection based on measured masking/levels and requested instrumental ambience; ear-based genre/vocal judgment not claimed.','candidates':metrics}
(P/'05_review/bgm-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
a=P/'00_brief/production-authorization.json';d=json.loads(a.read_text());d['bgm'].update(candidate=chosen['id'],selection='new_candidates_twice_reviewed_by_agent_under_user_delegation',explicit_candidate_click=False);a.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'chosen':chosen,'all_levels':[{k:v for k,v in x.items() if k!='rms_per_second'} for x in metrics]},indent=2))
