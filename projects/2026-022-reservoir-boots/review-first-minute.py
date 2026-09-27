"""Review the encoded first minute before the full master is assembled."""
import json
import subprocess
from pathlib import Path

p=Path(__file__).resolve().parent
out=p/'05_review/preview'
out.mkdir(exist_ok=True)
manifest=out/'first-minute-concat.txt'
manifest.write_text(''.join(f"file '{p}/06_delivery/youtube/parts/part-{i:02d}.mp4'\n" for i in range(1,5)))
video=out/'first-minute.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-i',str(p/'04_composition/assets/audio/voice.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-t','60','-movflags','+faststart',str(video)],check=True)
for i,t in enumerate([0,6,18,30,41,56]):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=480:270',str(out/f'first-{i:02d}.png')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(out/'first-%02d.png'),'-vf','tile=3x2','-frames:v','1',str(out/'first-minute-contact.png')],check=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
(out/'first-minute-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print(video)
