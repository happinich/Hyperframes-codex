"""Metadata and full-duration detector checks; reported evidence is not ear review."""
from pathlib import Path
import subprocess,json,hashlib,re,datetime
P=Path(__file__).resolve().parent;R=P/'05_review';results=[]
files=[P/f'06_delivery/youtube/{P.name}-youtube.mp4']+[P/f'06_delivery/shorts/{P.name}-shorts-{n:02}.mp4' for n in range(1,4)]
for n,path in enumerate(files):
 if not path.exists():raise FileNotFoundError(path)
 raw=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True);probe=json.loads(raw);v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');dur=float(probe['format']['duration']);diff=abs(float(v['duration'])-float(a['duration']));expected=(1920,1080) if n==0 else (1080,1920)
 assert (v['width'],v['height'])==expected and v['r_frame_rate']=='60/1'
 assert v['codec_name']=='h264' and a['codec_name']=='aac' and int(a['sample_rate'])==48000
 assert diff<=.1,(path,diff)
 assert (1200<=dur<=2400) if n==0 else (15<=dur<=40)
 log=R/f'logs/{"youtube" if n==0 else f"shorts-{n:02}"}-freeze-black.log'
 with log.open('w') as out:subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-an','-vf','fps=15,scale=480:-2,freezedetect=n=-55dB:d=3,blackdetect=d=1:pix_th=0.10:pic_th=0.98','-f','null','-'],stdout=out,stderr=subprocess.STDOUT,check=True)
 lines=[x for x in log.read_text().splitlines() if 'freeze_' in x or 'black_start:' in x]
 results.append({'file':str(path.relative_to(P)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'duration_seconds':dur,'video':{'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'codec':v['codec_name'],'frames':v.get('nb_frames'),'duration':v['duration']},'audio':{'codec':a['codec_name'],'sample_rate':a['sample_rate'],'channels':a['channels'],'duration':a['duration']},'av_difference_seconds':round(diff,6),'detector_sampling_fps':15,'detector_dimensions_width':480,'freeze_noise_db':-55,'freeze_duration_threshold_seconds':3,'black_duration_threshold_seconds':1,'detected_intervals':lines,'technical_status':'pass' if not lines else 'manual_interval_review_required'})
 print(path.name,round(dur,3),'AV diff',round(diff,6),'detected intervals',len(lines),flush=True)
(R/'final-technical-qa.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':results,'listening_review_performed':False},ensure_ascii=False,indent=2)+'\n')
