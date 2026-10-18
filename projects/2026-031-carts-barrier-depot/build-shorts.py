"""Separate portrait compositions; fresh native assets and aligned teaser voices."""
import hashlib,html,json,shutil,wave,math
from pathlib import Path
from scene_overlays import aff,led,svg
P=Path(__file__).resolve().parent;C=P/'04_composition';V=C/'assets/visuals';plan=json.loads((P/'01_script/shorts-scene-plan.json').read_text())
lf=json.loads((P/'01_script/scene-plan.json').read_text());lfhash={hashlib.sha256((V/(s.get('baseline_asset_id',s['asset_id'])+'.png')).read_bytes()).hexdigest() for c in lf['scenes'] for s in c['shot_sequence']};provenance=[]
for n,short in enumerate(plan['shorts'],1):
 timing=json.loads((P/f'02_audio/shorts/shorts-{n:02}/03_sync/captions.words.json').read_text());captions=timing['cues'];audio=P/f'02_audio/sound-design/shorts-{n:02}-bgm.wav'
 with wave.open(str(audio)) as w:duration=math.ceil(w.getnframes()/w.getframerate()*60)/60
 phrases={1:['카트 열두 대를 모았는데,','맨 뒤 바퀴만','혼자 돌고 있었어요.','지붕 아래 바닥은 말라 있었는데','빨간 손잡이에는','젖은 손가락 자국 네 개가 남았죠.','저는 사진을 찍고','카트 안을 확인했습니다.','짐칸은 비어 있었어요.','그런데 그 카트와 앞 카트 사이에서','젖은 운동화 앞코가','제 쪽으로 돌아갔습니다.'],2:['방음벽 안에서 누군가','제 발에 맞춰 걸었어요.','밤에 느슨해진 패널을','확인하던 중이었죠.','벽을 두드린 손을 뗐는데도','안쪽에서 세 번의 소리가 돌아왔습니다.','이음새를 비추자','흰 긁힘 여섯 줄이 보였어요.','아래쪽 발전기가 켜진 순간,','그 선들이 제 발밑으로','빠르게 옮겨 왔습니다.'],3:['운전석이 빈 예비 버스의','행선지가 켜졌어요.','저는 야간 배차를 끝내고','세차선으로 걸어가던 중이었습니다.','표시를 껐는데','가운데 문이 열리고,','버스가 시동 소리도 없이 굴렀죠.','앞 유리에 새로 뜬 행선지는','제가 서 있던 세차선이었습니다.','제가 정비동 쪽으로 물러서자','글자가 다시 바뀌었습니다.']}[n]
 assert ' '.join(phrases)==short['narration_text']
 words=timing['words'];captions=[];cursor=0
 for phrase in phrases:
  count=len(phrase.split());a=words[cursor]['start'];cursor+=count;b=words[cursor]['start'] if cursor<len(words) else timing['duration'];captions.append({'text':phrase,'start':a,'end':b})
 (P/f'03_sync/shorts-{n:02}-phrase-captions.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2)+'\n')
 shutil.copy2(audio,C/f'assets/audio/shorts-{n:02}.wav');folder=C/f'shorts-{n:02}';folder.mkdir(exist_ok=True)
 if not(folder/'assets').exists():(folder/'assets').symlink_to('../assets')
 sections=[];cues=[]
 for i,scene in enumerate(short['scenes']):
  a=scene['start_seconds'];b=short['scenes'][i+1]['start_seconds'] if i<4 else duration;id=scene['asset_id'];path=V/(id+'.png');h=hashlib.sha256(path.read_bytes()).hexdigest();assert h not in lfhash
  provenance.append({'asset_id':id,'relative_path':str(path.relative_to(P)),'sha256':h,'fresh_portrait':True,'longform_hash_collision':False});body=''
  if n==3:
   if i==0:body+=led([[352,485],[754,502],[352,551]],'차고지 정문',f'led-{i}')
   if i==3:
    body+=led([[499,563],[747,581],[499,604]],'세차선',f'led-{i}')
    body+=f'<g transform="{aff([[37,407],[167,430],[37,507]],200,120)}"><text x="100" y="77" text-anchor="middle" font-size="47" fill="#d4ded9">세차선</text></g>'
   if i==4:
    body+=led([[591,497],[763,517],[591,531]],'세차선',f'led-{i}')
    # Change begins but the new destination is withheld at a complete-sentence cliffhanger.
    cues.append(f"tl.set('#led-{i}',{{textContent:'▦ ▦ ▦'}},{b-1.15:.4f});")
  if n==1 and i==2:
   # Camera/viewer screen uses a separately generated portrait clue, never a long-form crop.
   body+=f'<defs><clipPath id="phone-screen"><polygon points="295,550 416,565 390,832 271,811"/></clipPath></defs><g clip-path="url(#phone-screen)"><rect x="270" y="545" width="155" height="295" fill="#10161a"/><svg x="270" y="573" width="155" height="208" viewBox="0 420 941 750" preserveAspectRatio="xMidYMid meet"><image href="assets/visuals/SH01-portrait-A02.png" width="941" height="1672"/></svg><circle cx="342" cy="797" r="12" fill="#d4d6cb"/></g>'
  sections.append(f'<section id="view-{i}" class="view"><img src="assets/visuals/{id}.png" alt="">{svg(body,True) if body else ""}<div class="light"></div></section>')
  scale=1.04;end_scale=1.12;origin='50% 50%'
  if n==2 and i==0:scale=1.19;end_scale=1.28;origin='15% 70%'
  cues.extend([f"tl.set('#view-{i}',{{display:'block'}},{a:.4f});",f"tl.fromTo('#view-{i}',{{scale:{scale},transformOrigin:'{origin}',xPercent:{(-1)**i*.7}}},{{scale:{end_scale},xPercent:{(-1)**(i+1)*.7},duration:{b-a:.4f},ease:'none'}},{a:.4f});",f"tl.fromTo('#view-{i} .light',{{xPercent:-7,opacity:.13}},{{xPercent:7,opacity:.34,duration:2.1,repeat:{max(0,int((b-a)/2.1)-1)},yoyo:true,ease:'sine.inOut'}},{a:.4f});",f"tl.set('#view-{i}',{{display:'none'}},{b:.4f});"])
 cap=''.join(f'<div id="cap-{i}" class="cap">{html.escape(c["text"])}</div>' for i,c in enumerate(captions))
 for i,c in enumerate(captions):cues.extend([f"tl.set('#cap-{i}',{{opacity:1}},{c['start']:.4f});",f"tl.set('#cap-{i}',{{opacity:0}},{c['end']:.4f});"])
 page=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{html.escape(short['title'])} · 쇼츠</title><style>@font-face{{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}}*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#11151a;font-family:'Apple SD Gothic Neo',sans-serif}}#master{{position:relative;width:1080px;height:1920px;overflow:hidden}}.view{{position:absolute;inset:0;overflow:hidden;display:none}}.view img{{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;{'image-rendering:pixelated' if n==3 else ''}}}.clue-layer{{position:absolute;inset:0;width:100%;height:100%}}.light{{position:absolute;inset:-10%;background:linear-gradient(110deg,transparent 35%,#dfc7a016 50%,transparent 65%)}}.shade{{position:absolute;inset:0;background:linear-gradient(transparent 48%,#05080da5 82%,#05080d82)}}.caption-band{{position:absolute;left:80px;right:180px;bottom:360px;height:280px;display:flex;align-items:end;justify-content:center}}.cap{{position:absolute;bottom:0;left:0;right:0;text-align:center;color:#fff;font-size:57px;font-weight:850;line-height:1.28;word-break:keep-all;text-shadow:0 4px 10px #000;-webkit-text-stroke:5px #000;paint-order:stroke fill;opacity:0}}.related{{position:absolute;right:180px;bottom:285px;color:#e4dfd4;font-size:32px;text-shadow:0 3px 9px #000;opacity:0}}</style></head><body><main id="master" data-composition-id="shorts-{n:02}" data-width="1080" data-height="1920" data-fps="60" data-start="0" data-duration="{duration}"><audio id="voice" src="assets/audio/shorts-{n:02}.wav" data-start="0" data-duration="{duration}" data-track-index="0" data-volume="1"></audio>{''.join(sections)}<div class="shade"></div><div class="caption-band">{cap}</div><div class="related">관련 동영상에서 본편 보기</div></main><script src="assets/gsap.min.js"></script><script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});{''.join(cues)}tl.to('.related',{{opacity:1,duration:.35}},{duration-3:.4f});tl.to({{}},{{duration:{duration}}},0);window.__timelines['shorts-{n:02}']=tl;tl.seek(.000001,false);gsap.set('#view-0',{{display:'block'}});</script></body></html>'''
 (folder/'index.html').write_text(page);short['composition']=f'04_composition/shorts-{n:02}/index.html';short['render_duration_seconds']=duration
 print(f'SH{n:02}: {duration:.3f}s, 5 fresh portrait assets, {len(captions)} cues')
plan['status']='composition_prepared_under_standing_delegation_pending_output_review';(P/'01_script/shorts-scene-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');(P/'05_review/shorts-asset-provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
