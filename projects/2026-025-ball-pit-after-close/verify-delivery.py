"""Verify exported media and approved source hashes without regenerating assets."""
import hashlib,json,re,subprocess,shutil
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parent
def read(n): return json.loads((P/n).read_text())
def probe(p): return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
authorization=read('00_brief/production-authorization.json')
for name,key in [('narration.txt','main_script_sha256'),('shorts-narration.txt','shorts_script_sha256')]:
    assert hashlib.sha256((P/'01_script'/name).read_bytes()).hexdigest()==authorization[key],name
images=read('05_review/image-review.json')['assets']
for a in images:
    assert a['decision']=='approved' and a['review1'].startswith('PASS') and a['review2'].startswith('PASS'),a['id']
    assert hashlib.sha256((P/a['relative_path']).read_bytes()).hexdigest()==a['sha256'],a['id']
long={a['sha256'] for a in images if a['kind']=='longform'}
assert all(a['sha256'] not in long for a in images if a['kind']=='shorts')
for letter in 'ab':
    s=probe(P/f'07_publish/youtube/thumbnail-{letter}.png')['streams'][0]
    assert (s['width'],s['height'])==(1280,720)
report={'approved_scripts_unchanged':True,'reviewed_image_hashes_unchanged':True,'shorts_fresh_assets':True,'videos':{}}
for fmt,shape,stem in [('youtube',(1920,1080),'captions'),('shorts',(1080,1920),'shorts-captions')]:
    video=P/f'06_delivery/{fmt}/{P.name}-{fmt}.mp4'
    data=probe(video);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'])==shape
    assert Fraction(v['avg_frame_rate'])==60 and Fraction(v['r_frame_rate'])==60
    assert v['codec_name']=='h264' and a['codec_name']=='aac' and a['sample_rate']=='48000'
    duration=float(data['format']['duration']);vd=float(v['duration']);ad=float(a['duration'])
    assert abs(vd-ad)<.05,(fmt,vd,ad)
    assert 360<=duration<=480 if fmt=='youtube' else 15<=duration<=40
    log=P/f'05_review/{fmt}-final-detect.log'
    with log.open('w') as f:
        subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(video),'-vf','fps=12,scale=480:-2,freezedetect=n=-50dB:d=3,blackdetect=d=1:pix_th=0.10','-af','volumedetect,silencedetect=noise=-50dB:d=0.8','-f','null','-'],stdout=f,stderr=subprocess.STDOUT,check=True)
    text=log.read_text()
    freezes=re.findall(r'freeze_(?:start|duration|end):[^\n]+',text)
    black=re.findall(r'black_start:[^\n]+',text)
    assert not freezes and not black,(fmt,freezes,black)
    peak=float(re.search(r'max_volume: ([\d.-]+) dB',text)[1]);assert peak<-.1
    for ext in ['srt','vtt']:
        src=P/f'03_sync/{stem}.{ext}';assert src.exists() and src.stat().st_size>50
        shutil.copy2(src,P/f'06_delivery/{fmt}/{P.name}-{fmt}.{ext}')
    first_audio=next(s for s in data['streams'] if s['codec_type']=='audio')['start_time']
    report['videos'][fmt]={'path':str(video),'dimensions':shape,'fps':60,'duration':duration,'video_duration':vd,'audio_duration':ad,'audio_start':first_audio,'peak_db':peak,'codecs':['h264','aac'],'freezes_over_3_seconds':freezes,'black_over_1_second':black,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'probe':data}
    frames=[0,duration-.1] if fmt=='shorts' else [0,duration-17,duration-2]
    for i,t in enumerate(frames):
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(P/f'05_review/preview/{fmt}-final-{i}.png')],check=True)
report['subjective_audio_listening']='unavailable; ASR/timing/levels reviewed, no ear-based claim'
(P/'05_review/delivery-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({f:{k:v for k,v in d.items() if k not in ['probe','sha256']} for f,d in report['videos'].items()},ensure_ascii=False,indent=2))
