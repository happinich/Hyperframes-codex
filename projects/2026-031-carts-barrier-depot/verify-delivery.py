"""Decode the complete delivered streams, inspect format and scan frozen/black runs."""
import json,subprocess,hashlib,re,sys
from pathlib import Path
P=Path(__file__).resolve().parent;D=P/'05_review/delivery-frames';D.mkdir(exist_ok=True);R=P/'05_review/logs';records=[]
files=([P/f'06_delivery/shorts/{P.name}-shorts-{i:02}.mp4' for i in range(1,4)] if '--shorts' in sys.argv else [P/f'06_delivery/youtube/{P.name}-youtube.mp4'])
for f in files:
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');short='shorts-' in f.name;expect=(1080,1920) if short else (1920,1080);assert (v['width'],v['height'])==expect and v['r_frame_rate']=='60/1';assert v['codec_name']=='h264' and a['codec_name']=='aac';vd=float(v['duration']);ad=float(a['duration']);assert abs(vd-ad)<.1
 result=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vf','freezedetect=n=-60dB:d=3,blackdetect=d=1:pix_th=0.10','-an','-f','null','-'],capture_output=True,text=True);assert result.returncode==0;log=R/(f.stem+'-decode-freeze.log');log.write_text(result.stderr);freeze=[l for l in result.stderr.splitlines() if 'freeze_' in l];black=[l for l in result.stderr.splitlines() if 'black_start:' in l]
 if short:times=[.05,5.8,11,14.5,19.3,vd-.08]
 else:times=[.05,7,20,96.1,130.3,176.7,217.4,289.4,318.9,384.35,419,506.7,580.3,648.75,674.2,719.6,792.58,836.2,881.56,890.68,921.08,948.54,981.3,1043.0,1112.29,1127.18,1139.58,1208.99,1233,vd-.1]
 frames=[]
 for t in times:
  out=D/f'{f.stem}-{t:.2f}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1',str(out)],check=True);frames.append({'time_seconds':t,'path':str(out.relative_to(P))})
 records.append({'filename':f.name,'relative_path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'frames':int(v['nb_frames']),'video_codec':v['codec_name'],'pixel_format':v['pix_fmt'],'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'channels':a['channels'],'video_duration_seconds':vd,'audio_duration_seconds':ad,'duration_delta_seconds':round(vd-ad,6),'full_decode':'passed','freeze_intervals_over_3s':freeze,'black_intervals_over_1s':black,'extracted_review_frames':frames,'subjective_listening':False})
 print(f.name,vd,ad,'freeze',len(freeze),'black',len(black),flush=True)
(P/('05_review/shorts-technical-review.json' if '--shorts' in sys.argv else '05_review/longform-technical-review.json')).write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
