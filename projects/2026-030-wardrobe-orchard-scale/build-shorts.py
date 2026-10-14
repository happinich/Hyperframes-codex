"""Build three independent portrait Shorts from fresh images and aligned speech."""
import hashlib
import html
import json
import shutil
import wave
from pathlib import Path
from scene_overlays import overlays_for_shot

P = Path(__file__).resolve().parent
C = P / '04_composition'
assets = C / 'assets'
plan = json.loads((P / '01_script/shorts-image-generation-plan.json').read_text())['assets']
long_hashes = {hashlib.sha256(Path(a['output_path']).read_bytes()).hexdigest()
               for a in json.loads((P / '01_script/image-generation-plan.json').read_text())['assets']
               if Path(a['output_path']).exists()}
for number in range(1, 4):
    selection = [a for a in plan if a['asset_id'].startswith(f'SH{number:02}-')]
    assert len(selection) == 4
    for a in selection:
        path = Path(a['output_path'])
        assert path.exists(), path
        assert hashlib.sha256(path.read_bytes()).hexdigest() not in long_hashes
    timing = json.loads((P / f'02_audio/shorts/shorts-{number:02}/03_sync/captions.words.json').read_text())
    duration = timing['duration']
    captions = timing['cues']
    approved_mix = P / f'02_audio/sound-design/shorts-{number:02}-bgm.wav'
    source_voice = approved_mix if approved_mix.exists() else P / f'02_audio/shorts/shorts-{number:02}/02_audio/working/voice.wav'
    with wave.open(str(source_voice)) as source_info:
        duration = source_info.getnframes()/source_info.getframerate()
    target_voice = assets / f'audio/shorts-{number:02}.wav'
    target_voice.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_voice, target_voice)
    folder = C / f'shorts-{number:02}'
    folder.mkdir(exist_ok=True)
    link = folder / 'assets'
    if not link.exists():
        link.symlink_to('../assets')
    spans = {1:[0,2.63,7.81,11.21,duration],2:[0,4.79,9.59,14.11,duration],3:[0,5.75,9.45,13.05,duration]}[number]
    visual_parts=[];clue_cues=[]
    for i,a in enumerate(selection):
        clue,events=overlays_for_shot({'asset':a['asset_id'].lower(),'id':f'view-{i}','startFrame':round(spans[i]*60),'endFrame':round(spans[i+1]*60)},0,duration)
        visual_parts.append(f'<section id="view-{i}" class="view"><img src="assets/visuals/{a["asset_id"].lower()}.png" alt="">{clue}<div class="light"></div></section>');clue_cues.extend(events)
    visual=''.join(visual_parts)
    cap_html = ''.join(f'<div id="cap-{i}" class="cap">{html.escape(c["text"])}</div>'
                       for i, c in enumerate(captions))
    cues = list(clue_cues)
    for i in range(4):
        a, b = spans[i], spans[i+1]
        cues += [f"tl.set('#view-{i}',{{display:'block'}},{a:.4f});",
                 f"tl.fromTo('#view-{i}',{{scale:1.025,xPercent:{(-1)**i*1.6}}},"
                 f"{{scale:1.11,xPercent:{(-1)**(i+1)*1.6},duration:{b-a:.4f},ease:'none'}},{a:.4f});",
                 f"tl.fromTo('#view-{i} .light',{{xPercent:-7,opacity:.12}},{{xPercent:7,opacity:.3,duration:Math.min(2.2,{b-a:.4f}),repeat:Math.max(0,Math.floor({b-a:.4f}/2.2)-1),yoyo:true}},{a:.4f});",
                 f"tl.set('#view-{i}',{{display:'none'}},{b:.4f});"]
    for i, cue in enumerate(captions):
        cues += [f"tl.set('#cap-{i}',{{opacity:1}},{cue['start']:.4f});",
                 f"tl.set('#cap-{i}',{{opacity:0}},{cue['end']:.4f});"]
    script = ''.join(cues)
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>빈집·과수원·고물상의 밤 쇼츠 {number}</title>
<style>@font-face{{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}}*{{box-sizing:border-box}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#11151a;font-family:"Apple SD Gothic Neo",sans-serif}}
#master{{position:relative;width:1080px;height:1920px;overflow:hidden}}.view{{position:absolute;inset:0;overflow:hidden;display:none}}
.view img{{width:100%;height:100%;object-fit:cover;position:absolute;inset:0}}.clue-layer{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}}.light{{position:absolute;inset:-10%;background:linear-gradient(110deg,transparent 35%,#dfc7a016 50%,transparent 65%)}}.shade{{position:absolute;inset:0;background:linear-gradient(transparent 48%,#05080da5 82%,#05080d82)}}
.caption-band{{position:absolute;left:80px;right:180px;bottom:360px;height:280px;display:flex;align-items:end;justify-content:center}}
.cap{{position:absolute;bottom:0;left:0;right:0;text-align:center;color:white;font-size:57px;font-weight:850;line-height:1.28;word-break:keep-all;text-shadow:0 4px 10px #000;-webkit-text-stroke:5px #000;paint-order:stroke fill;opacity:0}}
.related{{position:absolute;right:180px;bottom:285px;color:#e4dfd4;font-size:32px;text-shadow:0 3px 9px #000;opacity:0}}</style></head>
<body><main id="master" data-composition-id="shorts-{number:02}" data-width="1080" data-height="1920" data-fps="60" data-start="0" data-duration="{duration}">
<audio id="voice" src="assets/audio/shorts-{number:02}.wav" data-start="0" data-duration="{duration}" data-track-index="0" data-volume="1"></audio>
{visual}<div class="shade"></div><div class="caption-band">{cap_html}</div><div class="related">관련 동영상에서 본편 보기</div></main>
<script src="assets/gsap.min.js"></script><script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});{script}
tl.to('.related',{{opacity:1,duration:.35}},{max(0,duration-3):.4f});tl.to({{}},{{duration:{duration}}},0);
window.__timelines['shorts-{number:02}']=tl;tl.seek(.000001,false);gsap.set('#view-0',{{display:'block'}});</script></body></html>'''
    (folder / 'index.html').write_text(page)
    (C / f'variants/shorts-{number:02}.html').write_text(page)
    print(f'Short {number}: {duration:.2f}s, 4 fresh portrait images, {len(captions)} caption cues')
