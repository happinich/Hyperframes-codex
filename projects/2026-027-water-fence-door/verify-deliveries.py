"""Technical and timing checks. This does not substitute for subjective listening."""
from pathlib import Path
import json, subprocess, re, wave, hashlib
import numpy as np
P=Path(__file__).resolve().parent
R=P/'05_review'
def probe(f):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(f)]))
def waveform(f):
    with wave.open(str(f),'rb') as w:
        assert w.getsampwidth()==2
        sr=w.getframerate();channels=w.getnchannels()
        x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,channels).astype(np.float32)/32768
    return x,sr
def db(x):return float(20*np.log10(max(float(x),1e-12)))
def signal(f):
    x,sr=waveform(f)
    active=np.flatnonzero(np.max(np.abs(x[:sr]),axis=1)>10**(-45/20))
    metrics={'duration_seconds':len(x)/sr,'sample_rate':sr,'channels':x.shape[1],
             'sample_peak_dbfs':db(np.max(np.abs(x))), 'clipped_samples':int(np.sum(np.abs(x)>=.999)),
             'first_active_sample_seconds_at_minus45db':float(active[0]/sr) if len(active) else None,
             'first_100ms_rms_dbfs':db(np.sqrt(np.mean(x[:sr//10]**2))),
             'final_100ms_rms_dbfs':db(np.sqrt(np.mean(x[-sr//10:]**2)))}
    if len(x)>100*sr:
        metrics['final_four_seconds_halfsecond_rms_dbfs']=[db(np.sqrt(np.mean(x[-4*sr+i*sr//2:-4*sr+(i+1)*sr//2 if i<7 else None]**2))) for i in range(8)]
    return metrics
def normalized(s):return re.sub(r'\s+','',s)
plan=json.loads((P/'01_script/scene-plan.json').read_text());shortplan=json.loads((P/'01_script/shorts-scene-plans.json').read_text())['shorts']
result={'subjective_listening':'Not performed; no auditory perception available.','outputs':[]}
for i in range(4):
    short=i>0
    stem=f'{P.name}-shorts-{i:02}' if short else f'{P.name}-youtube'
    f=P/('06_delivery/shorts' if short else '06_delivery/youtube')/(stem+'.mp4')
    if not f.exists():continue
    pp=probe(f);v=next(s for s in pp['streams'] if s['codec_type']=='video');a=next(s for s in pp['streams'] if s['codec_type']=='audio')
    expected=shortplan[i-1]['duration_seconds'] if short else plan['duration_seconds']
    assert (v['width'],v['height'])==((1080,1920) if short else (1920,1080))
    assert v['r_frame_rate']=='60/1' and v['avg_frame_rate']=='60/1' and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
    assert a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2
    assert abs(float(v['duration'])-expected)<.04 and abs(float(a['duration'])-expected)<.04
    source=P/f'01_script/shorts-{i:02}-narration.txt' if short else P/'01_script/narration.txt'
    wordfile=P/f'03_sync/shorts-{i:02}-captions.words.json' if short else P/'03_sync/captions.words.json'
    ws=json.loads(wordfile.read_text())['words']
    assert normalized(' '.join(w['text'] for w in ws))==normalized(source.read_text())
    assert all(w['end']>=w['start'] and w['start']>=0 and w['end']<=expected+.03 for w in ws)
    assert all(ws[k]['start']<=ws[k+1]['start'] for k in range(len(ws)-1))
    wav=P/f'04_composition/assets/audio/shorts-{i:02}-mix.wav' if short else P/'04_composition/assets/audio/voice.wav'
    metrics=signal(wav)
    assert metrics['clipped_samples']==0
    assert metrics['first_active_sample_seconds_at_minus45db']<1
    row={'file':str(f.relative_to(P)), 'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),
         'bytes':f.stat().st_size,'resolution':[v['width'],v['height']],'fps':60,'video_frames':int(v['nb_frames']),
         'video_duration':float(v['duration']),'audio_duration':float(a['duration']),
         'av_difference_seconds':abs(float(v['duration'])-float(a['duration'])),
         'first_word':ws[0],'last_word':ws[-1], 'approved_caption_text_exact':True, 'signal':metrics}
    result['outputs'].append(row)
R.mkdir(exist_ok=True);(R/'technical-delivery-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
