"""Extract one full-resolution encoded frame for every approved visual cue."""
import json
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent
data = json.loads((P/'04_composition/scene-data.json').read_text())
video = P/'06_delivery/youtube'/f'{P.name}-youtube.mp4'
frames = P/'05_review/frames'
for i, shot in enumerate(data['shots']):
    t = shot['start']+min(.6, (shot['end']-shot['start'])/2)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-q:v','2',str(frames/f'encoded-cue-{i:02d}.jpg')], check=True)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','1','-i',str(frames/'encoded-cue-%02d.jpg'),'-vf','scale=384:216,tile=4x13','-frames:v','1',str(frames/'encoded-cues-contact.png')], check=True)
print('52 full-resolution encoded cue frames and supplementary contact sheet ready.')
