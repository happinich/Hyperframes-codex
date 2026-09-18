"""Verify delivered media and extract actual encoded-frame review sheets."""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

P=Path(__file__).resolve().parent
fmt=sys.argv[1] if len(sys.argv)>1 else 'youtube'
video=P/f'06_delivery/{fmt}/{P.name}-{fmt}.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
expected=(1920,1080) if fmt=='youtube' else (1080,1920)
assert (v['width'],v['height'])==expected
assert v['avg_frame_rate']=='60/1'
assert v['codec_name']=='h264' and a['codec_name']=='aac'
assert abs(float(v['duration'])-float(a['duration']))<.1
if fmt=='shorts':assert 15<=float(v['duration'])<=40
log=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','freezedetect=n=-55dB:d=3,blackdetect=d=1:pix_th=0.05','-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
(P/f'05_review/logs/{fmt}-media.log').write_text(log)
freeze=re.findall(r'freeze_duration: ([0-9.]+)',log)
black=re.findall(r'black_duration:([0-9.]+)',log)
assert not freeze,freeze
assert not black,black
length=float(v['duration'])
times=[0,.5,3.5,6,10,length*.6,length-4.2,length-.2] if fmt=='shorts' else sorted(set([0,10,45]+[length*i/22 for i in range(1,22)]+[length-18,length-4,length-.2]))
for i,t in enumerate(times):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=384:216' if fmt=='youtube' else 'scale=216:384',str(P/f'05_review/frames/encoded-{fmt}-{i:02d}.png')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(P/f'05_review/frames/encoded-{fmt}-%02d.png'),'-vf',f'tile=4x{math.ceil(len(times)/4)}','-frames:v','1',str(P/f'05_review/frames/encoded-{fmt}-contact.png')],check=True)
report={'status':'pass','metadata':probe,'freeze_intervals':freeze,'black_intervals':black,'frame_review_times':times,'frame_contact_sheet':f'frames/encoded-{fmt}-contact.png','audio_max_db':re.findall(r'max_volume: ([0-9.-]+) dB',log),'audio_mean_db':re.findall(r'mean_volume: ([0-9.-]+) dB',log)}
(P/f'05_review/{fmt}-media-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(fmt,'metadata, audio, freeze and black-frame checks passed')
