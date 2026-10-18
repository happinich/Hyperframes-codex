"""Exact diegetic Korean clues and independently animated vector props."""
import html,json
from pathlib import Path
P=Path(__file__).resolve().parent
PLAN=json.loads((P/'01_script/scene-plan.json').read_text())
def speech_time(scene_id,phrase):
 scene=next(s for s in PLAN['scenes'] if s['id']==scene_id);chapter=next(c for c in PLAN['chapters'] if c['id']==scene['chapter_id']);ci=int(chapter['id'][-1]);words=json.loads((P/f'02_audio/chapters/story-{ci:02}/03_sync/captions.words.json').read_text())['words'];source=(P/f'02_audio/chapters/story-{ci:02}/01_script/narration.txt').read_text();start=source.find(scene['narration_text']);pos=source.find(phrase,max(0,start));return chapter['start_seconds']+words[len(source[:pos].split())]['start']-.35 if pos>=0 else scene['start_seconds']
def aff(quad,w,h):
 tl,tr,bl=quad;return f'matrix({(tr[0]-tl[0])/w} {(tr[1]-tl[1])/w} {(bl[0]-tl[0])/h} {(bl[1]-tl[1])/h} {tl[0]} {tl[1]})'
def svg(body,portrait=False):return f'<svg class="clue-layer" viewBox="0 0 {"941 1672" if portrait else "1672 941"}">{body}</svg>'
def led(quad,label,key):
 return f'<g transform="{aff(quad,600,100)}"><text id="{key}" x="300" y="73" text-anchor="middle" font-family="Apple SD Gothic Neo,monospace" font-size="69" letter-spacing="7" font-weight="700" fill="#c4d3b4">{html.escape(label)}</text></g>'
def overlays_for_shot(item,offset_seconds,local_duration):
 asset=item.get('logical_asset',item['asset']);key=item['id']+'-clue';start=max(0,item['startFrame']/60-offset_seconds);end=min(local_duration,item['endFrame']/60-offset_seconds);body='';cues=[]
 def at(scene,phrase):return max(start,speech_time(scene,phrase)-offset_seconds)
 def show(t,selector=key):
  if t<end:cues.append(f"tl.set('#{selector}',{{opacity:1}},{t:.4f});")
 baseline=[[485,152],[1188,152],[485,247]]
 displays={
 'C03-S01-A1':([[842,158],[1125,159],[842,206]],'세차선'),
 'C03-S01-A2':([[892,79],[1287,145],[892,152]],'세차선'),
 'C03-S03-A1':(baseline,'차고지 정문'),
 'C03-S03-A2':([[1128,138],[1192,140],[1128,152]],'차고지 정문'),
 'C03-S04-A2':([[1383,127],[1583,148],[1383,159]],'차고지 정문'),
 'C03-S05-A2':(baseline,'세차선'), 'C03-S06-A2':(baseline,'정비동 앞'),
 'C03-S07-A2':([[1133,156],[1391,179],[1133,206]],'정비동 앞'),
 'C03-S09-A1':([[1283,289],[1415,294],[1283,319]],'세차선'),
 'C03-S09-A2':([[842,127],[1113,136],[842,176]],'세차선'),
 'C03-S10-A1':([[1056,185],[1213,196],[1056,222]],'세차선'),
 'C03-S10-A2':([[1092,163],[1252,171],[1092,197]],'출고 대기선')}
 if asset in displays:
  quad,label=displays[asset];body+=led(quad,label,key+'-led')
  if asset=='C03-S04-A2':cues.append(f"tl.set('#{key}-led',{{textContent:''}},{at('C03-S04','수정 완료'):.4f});")
  if asset=='C03-S10-A2':cues.append(f"tl.set('#{key}-led',{{textContent:'차단봉 앞'}},{at('C03-S10','차단봉 앞'):.4f});")
 if asset=='C01-S05-A1':
  body+=f'<defs><clipPath id="{key}-screen"><rect x="651" y="39" width="373" height="826" rx="48"/></clipPath></defs><g clip-path="url(#{key}-screen)"><rect x="651" y="39" width="373" height="826" fill="#101316"/><text x="688" y="115" font-size="28" fill="#e7e9df">사진</text><svg x="652" y="220" width="372" height="420" viewBox="530 280 560 400" preserveAspectRatio="xMidYMid meet"><image href="assets/visuals/C01-photo-evidence.png" x="0" y="0" width="1672" height="941"/></svg><rect x="793" y="825" width="90" height="5" rx="3" fill="#c5c8c5"/></g>'
 if asset=='C03-S02-A2':
  # Cover nonsemantic native header texture with a small exact table heading.
  body+=f'<g transform="{aff([[432,539],[840,515],[440,570]],600,50)}"><rect width="600" height="50" fill="#cba47b"/><text x="30" y="36" font-size="28" fill="#473d31">차량 번호</text><text x="300" y="36" font-size="28" fill="#473d31">기사 키</text></g>'
 if asset=='C03-S03-A2':
  body+=f'<g transform="{aff([[1052,510],[1370,535],[1018,682]],600,400)}"><rect width="600" height="400" fill="#d0d2c4"/><text x="300" y="75" text-anchor="middle" font-size="48" fill="#26312d">예비 버스</text><path d="M25 105H575 M25 245H575" stroke="#8d9b93" stroke-width="4"/><text id="{key}-row1" opacity="0" x="300" y="200" text-anchor="middle" font-size="65" font-weight="700" fill="#25322d">출고 예정 없음</text><text id="{key}-row2" opacity="0" x="300" y="335" text-anchor="middle" font-size="65" font-weight="700" fill="#25322d">배정 기사 없음</text></g>'
  show(at('C03-S03','출고 예정도'),key+'-row1');show(at('C03-S03','배정 기사도'),key+'-row2')
 if asset=='C03-S04-A2':
  body+=f'<polygon points="278,137 886,172 900,537 295,576" fill="#111b20"/><g transform="rotate(2.8 580 300)" fill="#c8d2c5"><text x="580" y="255" text-anchor="middle" font-size="30">예비 버스 · 행선지 전송</text><rect x="355" y="295" width="455" height="66" fill="#273331" stroke="#687772"/><text x="580" y="342" text-anchor="middle" font-size="39">공란 전송</text><text id="{key}" x="580" y="450" text-anchor="middle" font-size="45" opacity="0">수정 완료</text></g>'
  show(at('C03-S04','수정 완료'))
 if asset=='C03-S08-A2':
  body+=f'<g id="{key}" opacity="0"><rect x="75" y="75" width="330" height="70" fill="#10212add"/><text x="105" y="123" font-size="35" fill="#ece7d8">그날 낮 · 시스템 시험</text></g>';show(start);cues.append(f"tl.set('#{key}',{{opacity:0}},{min(end,start+3):.4f});")
 if asset=='C02-S13-A2':
  body+=f'<g id="{key}" opacity="0"><rect x="65" y="60" width="230" height="62" fill="#101821dc"/><text x="92" y="104" font-size="33" fill="#e8e4d9">동료의 현장 사진</text></g>';show(start);cues.append(f"tl.set('#{key}',{{opacity:0}},{min(end,start+3):.4f});")
 if asset=='C03-S11-A1':
  body+=f'<g id="{key}" style="transform-origin:985px 45px" shape-rendering="crispEdges"><path d="M985 45V122" fill="none" stroke="#141a1b" stroke-width="15"/><path d="M985 45V122" fill="none" stroke="#80725b" stroke-width="8"/><path d="M985 122L953 174H1013Z" fill="none" stroke="#141a1b" stroke-width="17" stroke-linejoin="round"/><path d="M985 122L953 174H1013Z" fill="none" stroke="#b39557" stroke-width="9" stroke-linejoin="round"/></g>'
  t=at('C03-S11','손잡이 하나가');cues.append(f"tl.fromTo('#{key}',{{rotation:-4}},{{rotation:4,duration:2.4,repeat:{max(0,int((end-t)/2.4)-1)},yoyo:true,ease:'sine.inOut',svgOrigin:'985 45'}},{t:.4f});")
 if asset=='C03-S12-A1':
  body+=f'<g transform="{aff([[884,208],[1490,247],[884,568]],600,350)}"><text x="300" y="205" text-anchor="middle" fill="#c6c9b9" font-size="67" font-weight="700">차단봉 앞</text></g>'
 if asset=='C03-S13-A2':
  body+=f'<g><rect x="141" y="201" width="667" height="402" fill="#111b20"/><text x="176" y="256" font-size="28" fill="#c9d4cb">시험 운행 기록 · 예비 버스</text><path d="M170 280H780 M170 365H780 M170 450H780" stroke="#52625f" stroke-width="2"/><text x="188" y="337" font-size="33" fill="#acb7b0">정문 · 확인</text><text x="188" y="422" font-size="33" fill="#acb7b0">세차선 · 정비동 · 확인</text><g id="{key}" opacity="0"><rect x="170" y="470" width="605" height="102" fill="#273329"/><text x="190" y="535" font-size="39" fill="#e1e7c9">차단봉 앞</text><text x="557" y="535" font-size="39" fill="#e1e7c9">승차 처리</text></g></g>';show(at('C03-S13','승차 처리'))
 return (svg(body) if body else ''),cues
