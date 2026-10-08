"""Compose approved anthology visuals to the final word timing, without burned longform captions."""
from pathlib import Path
import json, math, html
P=Path(__file__).resolve().parent
C=P/'04_composition'
read=lambda f:json.loads((P/f).read_text())
def write(f,x):
 q=P/f;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n')
plan=read('01_script/scene-plan.json');words=read('03_sync/captions.words.json')['words']
TOTAL=plan['duration_seconds'];V=plan['voice_duration_seconds']
by={s['id']:s for s in plan['scenes']}
local={k:[w for w in words if s.get('spoken_start_seconds',s['start_seconds'])-.001<=w['start']<=s.get('spoken_end_seconds',s['end_seconds'])+.001] for k,s in by.items()}
def anchor(sid,phrase):
 tokens=phrase.split();ws=local[sid]
 for i in range(len(ws)-len(tokens)+1):
  if all(tokens[j].strip(',.!?') in ws[i+j]['text'].strip(',.!?') for j in range(len(tokens))):return max(by[sid]['start_seconds'],ws[i]['start']-.35)
 raise ValueError('Missing visual cue: '+sid+' / '+phrase)
# Each entry: asset, optional spoken cue, crop mode, printed-photo mode.
M=read('01_script/visual-map.json')
shots=[]
for scene in plan['scenes']:
 sid=scene['id'];end=TOTAL if sid=='C03-S21' else scene['end_seconds']
 zones=[]
 for spec in M[sid]:
  asset,cue=spec[:2];mode=spec[2] if len(spec)>2 else 'wide';paper=spec[3] if len(spec)>3 else None
  zones.append({'asset':asset,'start':scene['start_seconds'] if cue is None else scene['start_seconds']+2.5 if cue=='__transition_midpoint__' else anchor(sid,cue),'mode':mode,'paper':paper})
 for i,z in enumerate(zones):
  ze=zones[i+1]['start'] if i+1<len(zones) else end
  if ze<=z['start']:raise ValueError('Nonmonotonic zones '+sid)
  count=max(1,math.ceil((ze-z['start'])/4.8))
  for k in range(count):
   shots.append({**z,'id':f'shot-{len(shots):04}','scene':sid,'chapter':(scene.get('chapter_id') or (('C01' if sid=='T01' else 'C02') if i==0 else ('C02' if sid=='T01' else 'C03'))),'start':z['start']+(ze-z['start'])*k/count,'end':z['start']+(ze-z['start'])*(k+1)/count,'crop':k%3})
 scene['visual_zones']=zones
 scene['motion_beats']=[{'at_seconds':round(s['start'],3),'action':'clue-directed framing and continuous pan/zoom with a second focus change at +2.2s','asset':s['asset']} for s in shots if s['scene']==sid]
plan['scenes'][-1].update(end_seconds=TOTAL,duration_seconds=TOTAL-plan['scenes'][-1]['start_seconds'])
write('01_script/scene-plan.json',plan)
write('04_composition/scene-data.json',{'duration':TOTAL,'voice_duration':V,'shots':shots,'burned_narration_captions':False})
def markup(items,length,silent=False,offset=0,portrait=False,shortid=1,captions=None):
 width,height=(1080,1920) if portrait else (1920,1080)
 cid=f'shorts-{shortid:02}' if portrait else 'youtube-master'
 audio=f'shorts-{shortid:02}-mix.wav' if portrait else 'voice.wav'
 tags=[]
 for s in items:
  sid=s['id']; mode=s.get('mode','wide'); paper=s.get('paper');asset=s['asset']
  isphoto=paper == 'photo'
  cover=False
  extra='<div class="paper-note">기록 사진</div>' if isphoto else ''
  cls='shot '+s.get('chapter','C01')+(' printed' if isphoto else '')+(' cover-shot' if cover else '')
  img=f'<img id="{sid}-image" class="photo clip" src="assets/visuals/{asset}.png" data-start="{s["start"]}" data-duration="{s["end"]-s["start"]}" alt="">'
  if isphoto: img=f'<div class="paper-content">{img}</div>'
  tags.append(f'<section class="{cls}" id="{sid}" data-mode="{mode}"><div class="view">{img}{extra}</div><div class="shade"></div><div class="light"></div></section>')
 caphtml='';capjs=''
 if portrait:
  caphtml='<div class="captions">'+''.join(f'<div class="caption" id="cap-{i}">{html.escape(c["text"])}</div>' for i,c in enumerate(captions or []))+'</div><div class="cta">관련 동영상에서 본편 보기</div>'
  capjs=f"const CAPS={json.dumps(captions,ensure_ascii=False)};CAPS.forEach((c,i)=>{{tl.set('#cap-'+i,{{opacity:1}},c.start);tl.set('#cap-'+i,{{opacity:0}},c.end)}});tl.to('.cta',{{opacity:1,duration:.3}},{length-3});"
 labels=[]
 if not portrait:
  for ch in plan['chapters']:
   start=ch['start_seconds']-offset
   if 0<=start<length or (silent and -1/60<start<0): labels.append({'start':max(0,start),'text':f'{ch["id"][-1]}  /  '+{'C01':'물을 뺀 저수조','C02':'캠핑장 울타리','C03':'배달된 문'}[ch['id']]})
 labelhtml=''.join(f'<div class="chapter-label" id="chapter-{i}">{html.escape(x["text"])}</div>' for i,x in enumerate(labels))
 labeljs=''.join(f"tl.set('#chapter-{i}',{{opacity:1}},{x['start']});tl.to('#chapter-{i}',{{opacity:0,duration:.4}},{x['start']+2});" for i,x in enumerate(labels))
 interhtml='';interjs=''
 if not portrait:
  for scene in plan['scenes']:
   if scene['id'] not in ['T01','T02']:continue
   t=scene['start_seconds']-offset
   if t+5<=0 or t>=length:continue
   ident=scene['id']; number='두 번째' if ident=='T01' else '세 번째'; place='캠핑장 울타리' if ident=='T01' else '배달된 문'
   interhtml+=f'<div id="dim-{ident}" class="chapter-dim"></div><div id="cue-{ident}" class="chapter-cue"><span>{number} 이야기</span><strong>{place}</strong></div>'
   interjs+=f"tl.fromTo('#dim-{ident}',{{opacity:0}},{{opacity:.78,duration:1.5,ease:'sine.inOut'}},{t});tl.to('#dim-{ident}',{{opacity:0,duration:2,ease:'sine.inOut'}},{t+3});tl.to('#cue-{ident}',{{opacity:1,y:0,duration:.4,ease:'sine.out'}},{t+1.4});tl.to('#cue-{ident}',{{opacity:0,duration:.5}},{t+4.2});"
 extra_framing="F.entrymark=[2.1,57,-34];" if any(x.get('mode')=='entrymark' for x in items) else ''
 endstart=TOTAL-20-offset
 endjs='' if portrait or endstart>=length else f"tl.to('.end-safe',{{opacity:1,duration:.5}},{max(0,endstart)});tl.to('.end-label',{{opacity:1,duration:.4}},{max(0,TOTAL-4-offset)});"
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>벽과 울타리로 막을 수 없었던 것들</title><style>
@font-face{{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}}*{{box-sizing:border-box}}html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden;background:#10110f;font-family:'Apple SD Gothic Neo',sans-serif}}#master{{position:relative;width:{width}px;height:{height}px;overflow:hidden}}.shot{{position:absolute;inset:0;display:none;overflow:hidden}}.view{{position:absolute;inset:0;overflow:hidden}}.photo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform,filter}}.shade{{position:absolute;inset:0;background:linear-gradient(0deg,#00000022,transparent 45%,#00000016);pointer-events:none}}.light{{position:absolute;inset:-10%;background:linear-gradient(115deg,transparent 20%,#d3c9a612 52%,transparent 82%);pointer-events:none}}.C02 .shade{{background:linear-gradient(0deg,#18130d24,transparent 50%)}}.printed{{background:#151b16}}.printed .view{{overflow:visible}}.paper-content{{position:absolute;inset:0;overflow:hidden}}.printed .view{{inset:75px 230px 95px;background:#e1decf;border:24px solid #e1decf;border-bottom-width:78px;box-shadow:0 30px 70px #0008;transform:rotate(-1.2deg)}}.portrait .printed .view{{inset:155px 72px 500px;border-width:16px;border-bottom-width:62px}}.paper-note{{position:absolute;left:16px;bottom:-59px;font-size:26px;color:#454941}}.timestamp{{position:absolute;right:18px;bottom:-58px;color:#2e3530;font:27px monospace}}.lens-paper{{position:absolute;left:58%;top:15%;width:20%;height:34%;padding:7px;background:#dbd9cd;transform:rotate(-4deg);box-shadow:0 6px 16px #0007}}.lens-paper img{{width:100%;height:100%;object-fit:cover}}.bandage{{position:absolute;left:34%;top:-16px;width:74px;height:27px;border-radius:4px;background:#bfa88b;box-shadow:inset 0 0 0 7px #cbb69a}}.chapter-label{{position:absolute;left:64px;top:54px;opacity:0;color:#f2f0e4;font-size:30px;letter-spacing:2px;text-shadow:0 2px 7px #000}}.chapter-dim{{position:absolute;inset:0;background:#070b08;opacity:0;pointer-events:none}}.chapter-cue{{position:absolute;left:116px;top:390px;color:#f1f0e5;opacity:0;transform:translateY(8px);text-shadow:0 3px 14px #000;pointer-events:none}}.chapter-cue span{{display:block;font-size:28px;letter-spacing:4px;color:#d1c6aa}}.chapter-cue strong{{display:block;font-size:60px;font-weight:600;letter-spacing:2px;margin-top:18px}}.end-safe{{position:absolute;right:0;top:0;width:860px;height:1080px;background:linear-gradient(90deg,transparent,#10140fe5);opacity:0}}.end-label{{position:absolute;left:64px;bottom:70px;opacity:0;color:#f2f0e4;font-size:29px}}.captions{{position:absolute;left:84px;right:174px;bottom:365px;color:#fff;text-align:center;font-size:55px;font-weight:850;line-height:1.3;word-break:keep-all;-webkit-text-stroke:7px #000;paint-order:stroke fill}}.caption{{position:absolute;left:0;right:0;bottom:0;opacity:0}}.cta{{position:absolute;left:84px;right:174px;bottom:270px;color:#f1efe3;font-size:32px;text-align:center;opacity:0;text-shadow:0 2px 7px #000}}
</style></head><body><main id="master" class="{'portrait' if portrait else 'landscape'}" data-composition-id="{cid}" data-width="{width}" data-height="{height}" data-fps="60" data-start="0" data-duration="{length}">
{'' if silent else f'<audio id="narration" src="assets/audio/{audio}" data-start="0" data-duration="{length}" data-track-index="0" data-volume="1"></audio>'}
{''.join(tags)}{caphtml}{labelhtml}{interhtml}<div class="end-safe"></div><div class="end-label">다음 공포 이야기는 관련 영상에서</div></main><script src="assets/gsap.min.js"></script><script>
const SHOTS={json.dumps(items,ensure_ascii=False)},D={length};window.__timelines={{}};const tl=gsap.timeline({{paused:true}});
SHOTS.forEach((s,i)=>{{const el=document.getElementById(s.id),img=el.classList.contains('cover-shot')?el.querySelector('.view'):el.querySelector('.photo'),light=el.querySelector('.light'),d=s.end-s.start,side=i%2?1:-1,mode=s.mode||'wide';let base=[1.035,1.12,1.20][s.crop||0],x=0,y=0;const b=s.chapter==='C02'?.90:1.01;
const F={{tank:[1.65,25,0],wetrung:[1.65,25,-34],office:[1.7,18,15],grip:[1.75,-28,-8],upperstairs:[2.5,0,66],creature:[2.0,41,24],cabinfront:[1.8,-33,25],tent:[1.55,24,0],carjoint:[1.7,-1,23],cabin:[1.4,-18,0],dents:[1.6,0,-4],hinges:[1.65,0,0],entryfloor:[1.7,0,-30],sock:[2.3,0,-15],tophand:[2.05,-5,56],wall:[1.6,0,25]}};{extra_framing}if(F[mode]){{[base,x,y]=F[mode];}}if(s.asset==='C03-phone'){{base=1.02;x=0;y=0;}}
tl.set(el,{{display:'block'}},s.start);tl.fromTo(img,{{scale:base,xPercent:x-side*.7,yPercent:y-.25,filter:'brightness('+b+') saturate(.77)'}},{{scale:base+.06,xPercent:x+side*.8,yPercent:y+.3,duration:d,ease:'none'}},s.start);tl.fromTo(light,{{xPercent:-5,opacity:.14}},{{xPercent:6,opacity:.33,duration:d,ease:'none'}},s.start);if(d>2.5)tl.to(img,{{filter:'brightness('+(b+.035)+') saturate(.77)',duration:Math.min(.7,d-2.2)}},s.start+2.2);tl.set(el,{{display:'none'}},s.end);}});
{capjs}{labeljs}{interjs}{endjs}tl.to({{}},{{duration:D}},0);window.__timelines['{cid}']=tl;tl.seek(.000001,false);gsap.set(document.getElementById(SHOTS[0].id),{{display:'block'}});
</script></body></html>'''
write('04_composition/index.html',markup(shots,TOTAL))
segmentdir=C/'segments';segmentdir.mkdir(exist_ok=True)
if not (segmentdir/'assets').exists():(segmentdir/'assets').symlink_to('../assets')
segments=[]
for i,scene in enumerate(plan['scenes']):
 sf=round(scene['start_seconds']*60); ef=math.ceil(TOTAL*60) if i+1==len(plan['scenes']) else round(plan['scenes'][i+1]['start_seconds']*60)
 start,length=sf/60,(ef-sf)/60
 items=[{**s,'start':max(0,s['start']-start),'end':min(length,s['end']-start)} for s in shots if s['end']>start+.001 and s['start']<start+length-.001]
 items[0]['start']=0;items[-1]['end']=length
 name=f'segments/part-{i+1:02}.html';write('04_composition/'+name,markup(items,length,True,start))
 segments.append({'filename':name,'scene':scene['id'],'startFrame':sf,'endFrame':ef,'duration':length})
write('04_composition/render-segments.json',segments)
shortplans=read('01_script/shorts-scene-plans.json')
for i,sp in enumerate(shortplans['shorts'],1):
 ws=read(f'03_sync/shorts-{i:02}-captions.words.json')['words'];d=sp['duration_seconds']
 ss=[]
 for j,s in enumerate(sp['scenes']):
  zones=[(s['start_seconds'],s['visual_asset'].removesuffix('.png'))]
  if i==2 and j==1:
   t=next(w['start'] for w in ws if w['text'].startswith('랜턴을'))-.15
   zones=[(s['start_seconds'],'SH2-01'),(t,'SH2-02')]
  if i==3 and j==0:
   t=next(w['start'] for w in ws if w['text'].startswith('잠금쇠가'))-.15
   zones.append((t,'SH3-02'))
  for k,(start,asset) in enumerate(zones):
   end=zones[k+1][0] if k+1<len(zones) else s['end_seconds']
   n=max(1,math.ceil((end-start)/4.8))
   for a in range(n):ss.append({'id':f'short-{i}-{len(ss)}','scene':s['id'],'chapter':f'C{i:02}','asset':asset,'start':start+(end-start)*a/n,'end':start+(end-start)*(a+1)/n,'crop':a%2,'mode':'wide','paper':None})
  s['visual_assets']=[x[1] for x in zones];s['motion_beats']=[{'at_seconds':round(t,3),'action':'clue change or deliberate portrait pan','asset':a} for t,a in zones]
 caps=[];buf=[]
 def flush():
  if buf:caps.append({'start':buf[0]['start'],'end':buf[-1]['end'],'text':' '.join(w['text'] for w in buf)});buf.clear()
 for w in ws:
  if buf and (len(' '.join(x['text'] for x in buf))+len(w['text'])>20 or w['start']-buf[-1]['end']>.4):flush()
  buf.append(w)
  if w['text'].endswith(('.','!','?')):flush()
 flush()
 for j in range(len(caps)-1,0,-1):
  if len(caps[j]['text'])<=8 and len(caps[j]['text'].split())==1 and caps[j]['start']-caps[j-1]['end']<.12:
   caps[j-1]['text']+=' '+caps[j]['text'];caps[j-1]['end']=caps[j]['end'];caps.pop(j)
 sp['shots']=ss;sp['caption_cues']=caps
 directory=C/f'shorts-{i:02}';directory.mkdir(exist_ok=True)
 if not (directory/'assets').exists():(directory/'assets').symlink_to('../assets')
 out=markup(ss,d,portrait=True,shortid=i,captions=caps)
 write(f'04_composition/shorts-{i:02}/index.html',out)
 variants=C/'variants';variants.mkdir(exist_ok=True)
 if not (variants/'assets').exists():(variants/'assets').symlink_to('../assets')
 write(f'04_composition/variants/shorts-{i:02}.html',out)
 if i==1:write('04_composition/variants/shorts.html',out)
write('01_script/shorts-scene-plans.json',shortplans)
write('04_composition/production-manifest.json',{'duration_seconds':TOTAL,'fps':60,'longform_shots':len(shots),'segments':len(segments),'chapter_styles':{c['id']:c.get('visual_style_id') for c in plan['chapters']},'shorts':3,'captioned_longform_requested':False})
print(json.dumps({'shots':len(shots),'segments':len(segments),'duration':TOTAL,'shorts':3}))
