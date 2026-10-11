"""Compose distinct approved camera assets, timed clue text and chapter rests."""
from pathlib import Path
import json, html, math
P=Path(__file__).resolve().parent
C=P/'04_composition'
def read(f):return json.loads((P/f).read_text())
def write(f,data):
 q=P/f;q.parent.mkdir(parents=True,exist_ok=True)
 q.write_text(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)+'\n')
plan=read('01_script/scene-plan.json');TOTAL=plan['duration_seconds']
places={'C01':'빈 극장의 커튼','C02':'냉동창고 비닐막','C03':'마지막 퇴실 방송'}
shots=[]
for scene in plan['scenes']:
 if scene['id'].startswith('T'):
  n=int(scene['id'][-1]);prev=plan['chapters'][n-1]['scene_ids'][-1];nxt=plan['chapters'][n]['scene_ids'][1]
  ps=next(x for x in plan['scenes'] if x['id']==prev)['shot_sequence'][-1]
  ns=next(x for x in plan['scenes'] if x['id']==nxt)['shot_sequence'][0]
  items=[{**ps,'start_seconds':scene['start_seconds'],'end_seconds':scene['start_seconds']+2.5,'chapter':'C'+str(n).zfill(2)}, {**ns,'start_seconds':scene['start_seconds']+2.5,'end_seconds':scene['end_seconds'],'chapter':'C'+str(n+1).zfill(2)}]
 else:items=[{**s,'chapter':scene['chapter_id']} for s in scene['shot_sequence']]
 for item in items:
  shots.append({'id':f'shot-{len(shots):03}','scene_id':scene['id'],'chapter':item['chapter'],'asset':item['asset_id'],'start':item['start_seconds'],'end':item['end_seconds'],'size':item['shot_size'],'focus':item['subject_focus'],'text':item.get('screen_text',[]),'camera_position':item['camera_position'],'new_viewpoint':not scene['id'].startswith('T') and not item.get('reuse_reason'),'baseline':item.get('baseline_shot_id')})
shots[-1]['end']=TOTAL
for shot in shots:
 shot['start']=round(shot['start']*60)/60
 shot['end']=round(shot['end']*60)/60
shots[-1]['end']=math.ceil(TOTAL*60)/60
def markup(items,duration,offset=0,silent=False,portrait=False,number=1,captions=None):
 width,height=(1080,1920) if portrait else (1920,1080)
 ident=f'shorts-{number:02}' if portrait else 'youtube-master'
 tags=[];effects=[];text_timing=[]
 for index,s in enumerate(items):
  text=[];device=''
  for k,t in enumerate(s.get('text',[])):
   if portrait and s['asset']=='SH3-02':
    device='<div class="portrait-screen"><span>잔류 인원</span><strong>2</strong></div>'
    continue
   if portrait and s['asset']=='SH3-01':
    device='<div class="manual-warning">마지막 퇴실 방송<br>응답하지 말 것</div>'
    continue
   if t.get('role')=='device_clue' and s['asset'] in ('C03-S04-B','C03-S22-B'):
    count=t['text'].split()[-1]
    responses={'2':[],'3':['아무도 없어요','네'],'4':['아무도 없어요','네','네'],'1':['아무도 없어요']}[count]
    device=f'<div class="device-screen"><span>잔류 인원</span><strong>{html.escape(count)}</strong><div class="response-list">'+''.join(f'<p>{html.escape(r)}</p>' for r in responses)+'</div></div>'
    continue
   eid=f'{s["id"]}-text-{k}'
   text.append(f'<div class="clue-text" id="{eid}">{html.escape(t["text"])}</div>')
   text_timing.append({'id':eid,'start':s['start']+.15,'end':min(s['end'],s['start']+3.2)})
  tags.append(f'<section id="{s["id"]}" class="shot {s["chapter"]}" data-size="{s["size"]}"><div class="view"><div class="surface"><img id="{s["id"]}-image" class="photo clip" src="assets/visuals/{s["asset"]}.png" data-start="{s["start"]}" data-duration="{s["end"]-s["start"]}" alt="">{device}</div><div class="edge-shadow"></div><div class="beam"></div></div><div class="vignette"></div>{"".join(text)}</section>')
 labels=[]
 if False:
  for chapter in plan['chapters']:
   t=chapter['start_seconds']-offset
   # First title follows the cold open; subsequent titles appear in the chapter rest.
   t+=6.4 if chapter['id']=='C01' else .4
   if 0<=t<duration:labels.append({'id':f'label-{chapter["id"]}','start':t,'end':min(duration,t+2.8),'text':places[chapter['id']]})
 label_html=''.join(f'<div id="{x["id"]}" class="chapter-label">{html.escape(x["text"])}</div>' for x in labels)
 inter_html='';inter_js=''
 if not portrait:
  for scene in plan['scenes']:
   if not scene['id'].startswith('T'):continue
   # Segment boundaries and rest effects share the same 60fps grid.
   # A 5ms floating overlap previously introduced negative GSAP tweens into
   # the next chapter and left the dim/title visible after its first cut.
   t=round(scene['start_seconds']*60)/60-offset
   end=round(scene['end_seconds']*60)/60-offset
   if t>=duration-.001 or end<=.001:continue
   n=int(scene['id'][-1])+1;sid=scene['id']
   inter_html+=f'<div id="dim-{sid}" class="chapter-dim"></div><div id="cue-{sid}" class="chapter-cue"><span>{n}번째 이야기</span><strong>{places[f"C{n:02}"]}</strong></div>'
   inter_js+=f"tl.fromTo('#dim-{sid}',{{opacity:0}},{{opacity:.72,duration:1.5,ease:'sine.inOut'}},{t});tl.to('#dim-{sid}',{{opacity:0,duration:2,ease:'sine.inOut'}},{t+3});tl.to('#cue-{sid}',{{opacity:1,y:0,duration:.4}},{t+1.4});tl.to('#cue-{sid}',{{opacity:0,duration:.5}},{t+4.2});"
 cap_html='';cap_js=''
 if portrait:
  cap_html='<div class="captions">'+''.join(f'<div id="cap-{i}" class="caption">{html.escape(c["text"])}</div>' for i,c in enumerate(captions or []))+'</div><div class="cta">관련 동영상에서 본편 보기</div>'
  cap_js=f"const CAPS={json.dumps(captions,ensure_ascii=False)};CAPS.forEach((c,i)=>{{tl.set('#cap-'+i,{{opacity:1}},c.start);tl.set('#cap-'+i,{{opacity:0}},c.end)}});tl.to('.cta',{{opacity:1,duration:.3}},{duration-3});"
 label_js=''.join(f"tl.set('#{x['id']}',{{opacity:1}},{x['start']});tl.to('#{x['id']}',{{opacity:0,duration:.35}},{x['end']});" for x in labels+text_timing)
 end_t=TOTAL-20-offset
 end_js='' if portrait or end_t>=duration else f"tl.to('.end-safe',{{opacity:1,duration:.6}},{max(0,end_t)});tl.to('.end-label',{{opacity:1,duration:.4}},{max(0,TOTAL-4-offset)});"
 audio=f'shorts-{number:02}-mix.wav' if portrait else 'voice.wav'
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{html.escape(plan['title'])}</title><style>
@font-face{{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}}*{{box-sizing:border-box}}html,body{{margin:0;width:{width}px;height:{height}px;overflow:hidden;background:#10100e;font-family:'Apple SD Gothic Neo',sans-serif}}#master{{position:relative;width:{width}px;height:{height}px;overflow:hidden}}.shot{{position:absolute;inset:0;display:none;overflow:hidden}}.view{{position:absolute;inset:0;overflow:hidden;will-change:transform}}.surface{{position:absolute;inset:0;will-change:transform}}.device-screen{{position:absolute;left:31.9%;top:40.2%;width:29.3%;height:29.6%;padding:20px 24px;background:#06120e;color:#76df5c;border:4px solid #17392d;overflow:hidden;font-family:monospace}}.device-screen span{{font-size:29px;letter-spacing:4px}}.device-screen strong{{position:absolute;right:42px;top:30px;font-size:160px;line-height:1;color:#64e442}}.response-list{{position:absolute;left:24px;bottom:16px;width:60%;font-size:20px;line-height:1.25;color:#76a36b}}.response-list p{{margin:8px 0}}.photo{{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;will-change:transform}}.C03 .photo{{image-rendering:pixelated}}.vignette{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 48%,transparent 50%,#02040855 100%);pointer-events:none}}.edge-shadow{{position:absolute;top:0;bottom:0;left:-15%;width:37%;background:linear-gradient(90deg,#080606b0,transparent);pointer-events:none}}.beam{{position:absolute;inset:-10%;background:linear-gradient(115deg,transparent 31%,#c7a97916 48%,transparent 64%);pointer-events:none}}.C02 .beam{{background:linear-gradient(102deg,transparent 35%,#a2c7d01a 52%,transparent 73%)}}.C03 .beam{{background:linear-gradient(90deg,transparent 30%,#d4aa5114 50%,transparent 73%)}}.chapter-label{{position:absolute;top:56px;left:68px;max-width:1100px;font-size:32px;letter-spacing:2px;color:#eee7d8;opacity:0;text-shadow:0 3px 10px #000}}.clue-text{{position:absolute;left:70px;bottom:75px;font-size:38px;max-width:1200px;padding:14px 22px;color:#f4ead8;background:#0e1011d9;border-left:3px solid #c4a16c;opacity:0;word-break:keep-all}}.C03 .clue-text{{color:#8ae07c;border-color:#7fcd72;font-family:monospace}}.chapter-dim{{position:absolute;inset:0;opacity:0;background:#080a0d;pointer-events:none}}.chapter-cue{{position:absolute;left:110px;top:405px;opacity:0;color:#e9e5d8;transform:translateY(8px);text-shadow:0 4px 12px #000}}.chapter-cue span{{font-size:28px;letter-spacing:5px;color:#c9bc9e;display:block}}.chapter-cue strong{{display:block;font-size:62px;letter-spacing:2px;margin-top:20px}}.end-safe{{position:absolute;right:0;top:0;width:850px;height:1080px;background:linear-gradient(90deg,transparent,#0c1117e5);opacity:0}}.end-label{{position:absolute;left:70px;bottom:72px;font-size:30px;color:#ddd7c8;opacity:0}}.captions{{position:absolute;left:84px;right:174px;bottom:370px;color:#fff;font-size:55px;font-weight:850;line-height:1.3;text-align:center;word-break:keep-all;-webkit-text-stroke:7px #000;paint-order:stroke fill}}.caption{{position:absolute;left:0;right:0;bottom:0;opacity:0}}.cta{{position:absolute;left:84px;right:174px;bottom:278px;font-size:31px;color:#e9dfca;text-align:center;opacity:0;text-shadow:0 3px 8px #000}}
{'.clue-text{top:136px;bottom:auto;left:84px;max-width:810px;font-size:42px}.portrait-screen{position:absolute;left:29.6%;top:47%;width:43.8%;height:13.2%;background:#062019;color:#7ee967;padding:24px;font-family:monospace}.portrait-screen span{font-size:34px;letter-spacing:3px}.portrait-screen strong{display:block;font-size:112px;line-height:1.15;text-align:center}.manual-warning{position:absolute;left:27%;top:53%;color:#302b27;transform:rotate(-5deg);font-size:34px;font-weight:800;line-height:1.7}' if portrait else ''}</style></head><body><main id="master" data-composition-id="{ident}" data-width="{width}" data-height="{height}" data-fps="60" data-start="0" data-duration="{duration}">{'' if silent else f'<audio id="narration" src="assets/audio/{audio}" data-start="0" data-duration="{duration}" data-track-index="0" data-volume="1"></audio>'}{''.join(tags)}{label_html}{inter_html}{cap_html}<div class="end-safe"></div><div class="end-label">다음 공포 이야기 · 관련 영상에서</div></main><script src="assets/gsap.min.js"></script><script>
const SHOTS={json.dumps(items,ensure_ascii=False)};window.__timelines={{}};const tl=gsap.timeline({{paused:true}});
SHOTS.forEach((s,i)=>{{const el=document.getElementById(s.id),img=el.querySelector('.surface'),beam=el.querySelector('.beam'),shadow=el.querySelector('.edge-shadow'),d=s.end-s.start;const direction=i%2?1:-1;let x=s.size==='detail'?direction*.55:direction*2,scale=s.size==='detail'?1.015:1.025;
tl.set(el,{{display:'block'}},s.start);tl.fromTo(img,{{scale:scale,xPercent:-x,yPercent:s.chapter==='C02'?-.55:0}},{{scale:scale+(s.size==='detail'?.035:.095),xPercent:x,yPercent:s.chapter==='C02'?.55:0,duration:d,ease:'none'}},s.start);
// Each genuine camera shot has a directed light/shadow reveal; no synthetic crop recuts or random shake.
tl.fromTo(beam,{{xPercent:direction*-3,opacity:.2}},{{xPercent:direction*4,opacity:.55,duration:d,ease:'sine.inOut'}},s.start);
if(s.chapter==='C01')tl.fromTo(shadow,{{xPercent:-2,opacity:.65}},{{xPercent:4,opacity:.2,duration:d,ease:'sine.inOut'}},s.start);

tl.set(el,{{display:'none'}},s.end);}});
{label_js}{inter_js}{cap_js}{end_js}tl.to({{}},{{duration:{duration}}},0);window.__timelines['{ident}']=tl;tl.seek(.000001,false);gsap.set(document.getElementById(SHOTS[0].id),{{display:'block'}});
</script></body></html>'''
write('04_composition/index.html',markup(shots,TOTAL))
write('04_composition/scene-data.json',{'duration':TOTAL,'shots':shots,'burned_narration_captions':False,'camera_asset_changes':sum(s['new_viewpoint'] for s in shots)})
segdir=C/'segments';segdir.mkdir(exist_ok=True)
if not (segdir/'assets').exists():(segdir/'assets').symlink_to('../assets')
segments=[]
for i,scene in enumerate(plan['scenes']):
 sf=round(scene['start_seconds']*60);ef=math.ceil(TOTAL*60) if i==len(plan['scenes'])-1 else round(plan['scenes'][i+1]['start_seconds']*60)
 start=sf/60;length=(ef-sf)/60
 local=[{**s,'start':max(0,s['start']-start),'end':min(length,s['end']-start)} for s in shots if s['end']>start+.001 and s['start']<start+length-.001]
 local[0]['start']=0;local[-1]['end']=length
 filename=f'segments/part-{i+1:02}.html';write('04_composition/'+filename,markup(local,length,start,True))
 segments.append({'filename':filename,'scene':scene['id'],'startFrame':sf,'endFrame':ef,'duration':length})
write('04_composition/render-segments.json',segments)
shorts=read('01_script/shorts-scene-plans.json')
for n,short in enumerate(shorts['shorts'],1):
 timing=read(f'03_sync/shorts-{n:02}-captions.words.json');caps=[];buf=[]
 def flush():
  if buf:caps.append({'start':buf[0]['start'],'end':buf[-1]['end'],'text':' '.join(w['text'] for w in buf)});buf.clear()
 for w in timing['words']:
  if buf and (len(' '.join(a['text'] for a in buf))+len(w['text'])>20 or w['start']-buf[-1]['end']>.4):flush()
  buf.append(w)
  if w['text'].endswith(('.','!','?')):flush()
 flush()
 items=[{'id':f'short-{n}-{i}','scene_id':s['id'],'chapter':f'C{n:02}','asset':s['asset_id'],'start':s['start_seconds'],'end':s['end_seconds'],'size':'detail' if i==1 else 'wide','text':s.get('screen_text',[])} for i,s in enumerate(short['scenes'])]
 short['shots']=items;short['caption_cues']=caps
 folder=C/f'shorts-{n:02}';folder.mkdir(exist_ok=True)
 if not (folder/'assets').exists():(folder/'assets').symlink_to('../assets')
 page=markup(items,short['duration_seconds'],portrait=True,number=n,captions=caps)
 write(f'04_composition/shorts-{n:02}/index.html',page)
 variants=C/'variants';variants.mkdir(exist_ok=True)
 if not (variants/'assets').exists():(variants/'assets').symlink_to('../assets')
 write(f'04_composition/variants/shorts-{n:02}.html',page)
 if n==1:write('04_composition/variants/shorts.html',page)
write('01_script/shorts-scene-plans.json',shorts)
write('04_composition/production-manifest.json',{'status':'composition_prepared_pending_all_image_and_output_reviews','fps':60,'duration_seconds':TOTAL,'chapter_styles':{c['id']:c['visual_style_recommendation']['id'] for c in plan['chapters']},'longform_camera_shots':len(shots),'shorts':3,'external_caption_files_delivery':False,'burned_longform_captions':False})
print(json.dumps({'shots':len(shots),'segments':len(segments),'duration':TOTAL,'shorts':3}))
