"""Episode-specific publishing copy and native thumbnail compositions."""
from pathlib import Path
import json, html, shutil, hashlib

P=Path(__file__).resolve().parent
TITLE='돌아오지 말아야 할 것들 | 창작 공포 3편'
NEXT='마지막까지 남아 있던 것들 | 창작 공포 3편'
ALT=['옷에는 팔이 없었는데 소매가 제 손목을 잡았어요 | 창작 공포 3편', '막배가 떠난 잔교의 마른 철판 밑에서 올라온 것 | 창작 공포 3편', '철거한 펜션에서 객실 키가 반납됐어요 | 창작 공포 3편', '수선실, 잔교, 철거 현장에서 돌아온 것들 | 공포 이야기 3편', '반납하지 말아야 할 물건이 다시 돌아왔다 | 창작 괴담 3편']
DESC='''빈 코트 소매에 남은 봉제선, 막배 뒤 잔교의 마른 철판, 철거한 펜션에 돌아온 열쇠.
돌아와서는 안 될 것들을 만난 세 편의 독립적인 창작 공포 이야기입니다.

00:00 수선실에서 맡긴 소매가 저를 잡았어요
09:11 막배가 떠난 뒤 잔교 밑에서 손이 올라왔어요
18:17 철거한 펜션의 객실 키가 반납됐어요

세 이야기는 가상의 인물과 장소를 바탕으로 만든 오리지널 창작입니다. 실제 사건이나 제보를 실화로 재현한 영상이 아닙니다.
인형 스톱모션풍, 거친 2D 애니메이션풍, 먹·목탄풍으로 각 장소를 표현했습니다.

제작: 어둠 속 이야기
나레이션: ElevenLabs V4 · Esther · 본편 1.00배속
이미지: 이번 이야기용으로 생성한 이미지
음악: 이번 회차에 선택한 생성 드론 음악 / 환경음·효과음: 자체 제작
다른 채널의 이야기·영상·음성·음원을 재사용하지 않았습니다.

다음 이야기 추천: 마지막까지 남아 있던 것들 | 창작 공포 3편
마지막 화면에서 관련 영상 또는 창작 공포 재생목록을 선택해 주세요.

#공포이야기 #창작괴담 #어둠속이야기'''
PIN='세 이야기 중 어느 단서가 가장 섬뜩했나요? 노란 핀 / 마른 철판 / 번호 없는 키로 남겨 주세요. 결말을 말할 때는 첫 줄에 [스포일러]를 붙여 주세요.'
TAGS='공포 이야기,창작 괴담,어둠 속 이야기,수선실 괴담,소매 귀신,잔교 괴물,막배 괴담,철거 펜션,객실 키 괴담,심야 괴담,귀신,괴물,규칙 괴담,한국 공포'
SNS='빈 소매에서 손이 나왔고, 막배 뒤의 마른 잔교에서는 철판이 울렸습니다. 철거한 펜션에서는 없는 객실의 키가 돌아왔어요. 창작 공포 3편 「돌아오지 말아야 할 것들」.'
TIME='2026-10-13 22:00 KST 권장. 이번 회차의 실험 제안이며 채널 분석으로 확정한 최적 시간은 아닙니다.'
YT=P/'07_publish/youtube';SH=P/'07_publish/shorts';YT.mkdir(parents=True,exist_ok=True);SH.mkdir(parents=True,exist_ok=True)

def helper(title,fields,media='',extra=''):
 blocks=[]
 for i,(label,value) in enumerate(fields):
  blocks.append(f'<section><h2>{html.escape(label)}</h2><textarea id="copy-{i}" readonly rows="{max(2,min(12,value.count(chr(10))+2))}">{html.escape(value)}</textarea><button data-copy="copy-{i}">복사</button></section>')
 return f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{margin:0;background:#101419;color:#eee;font:17px/1.65 'Apple SD Gothic Neo',sans-serif}}main{{max-width:1060px;margin:auto;padding:36px 22px}}h1{{font-size:30px;line-height:1.35}}section{{margin:26px 0;padding:20px;background:#1c232b;border-radius:12px}}h2{{font-size:21px}}textarea{{display:block;box-sizing:border-box;width:100%;padding:14px;color:#eee;background:#111820;border:1px solid #607080;border-radius:6px;font-size:16px;line-height:1.6;font-family:inherit;resize:vertical}}button{{margin-top:12px;padding:10px 23px;border:0;border-radius:6px;background:#ceb37b;color:#111;font-weight:bold}}a{{color:#9ed0ff}}img{{width:min(100%,480px);margin:10px 14px 10px 0}}video{{width:min(100%,340px)}}.notice{{color:#c2cbd4}}#status{{position:sticky;bottom:0;background:#233b2b;padding:10px;display:none}}</style><main><h1>{html.escape(title)}</h1><p class="notice">창작 공포 · YouTube 자동 자막 사용 · 외부 자막 파일 없음</p>{media}{''.join(blocks)}{extra}<p id="status" role="status"></p></main><script>document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=async()=>{{const el=document.getElementById(b.dataset.copy);let ok=false;try{{await navigator.clipboard.writeText(el.value);ok=true}}catch(e){{el.focus();el.select();ok=document.execCommand('copy')}}const s=document.getElementById('status');s.textContent=ok?'복사했습니다.':'글자를 선택했습니다. 직접 복사해 주세요.';s.style.display='block';}});</script></html>'''

fields=[('추천 제목',TITLE),('설명',DESC),('태그',TAGS),('고정 댓글',PIN),('SNS 홍보 문구',SNS),('추천 공개 시간',TIME),('대체 제목 5개','\n'.join(f'{i}. {v}' for i,v in enumerate(ALT,1)))]
extra=f'<section><h2>게시 전략</h2><p>썸네일 A를 기본안으로 사용하고, B는 잔교의 손으로 비교합니다. A 문구: 소매 안의 손 / B 문구: 물 위의 손. 제목과 같은 문구를 반복하지 않습니다.</p><p>본편 마지막 20초에 관련 다음 영상 또는 창작 공포 재생목록을 연결합니다. 다음 영상 후보: {html.escape(NEXT)}. 실제 채널에 공개된 해당 영상이 있으면 선택하고, 없으면 공개된 창작 공포 재생목록을 선택합니다.</p><p>공개 48시간 뒤와 7일 뒤 CTR, 첫 30초 유지율, 09:06~09:12 및 18:11~18:17 전환 이탈, 평균 시청 시간, 엔드스크린 클릭을 비교합니다. 지표를 확인한 뒤 제목·썸네일을 조정합니다.</p><p>이 회차의 3편 합본은 사용자 요청에 따른 구성입니다.</p></section>'
media='<h2>썸네일</h2><img src="thumbnail-a.png" alt="소매 안의 손"><img src="thumbnail-b.png" alt="물 위의 손">'
(YT/'youtube-publish.html').write_text(helper(TITLE,fields,media,extra))
md='# '+TITLE+'\n\n'+''.join(f'## {k}\n\n{v}\n\n' for k,v in fields)+'## 썸네일 전략\n\n기본 A: 소매 안의 손 — 빈 소매의 천 손. 비교 B: 물 위의 손 — 마른 잔교에 올라온 회색 손. 제목을 반복하지 않는다.\n\n## 엔드스크린\n\n마지막 20초에 '+NEXT+' 또는 공개된 창작 공포 재생목록. 실제 공개 여부를 YouTube Studio에서 확인한다.\n\n## 검증 계획\n\n공개 48시간 및 7일 뒤 CTR, 첫 30초 유지율, 챕터 경계 이탈, 평균 시청 시간, 엔드스크린 클릭을 비교한다. 공개 시간은 가설이다.\n\n## 자막\n\nYouTube 자동 자막 사용. 외부 SRT/VTT 파일은 전달·업로드하지 않는다.\n'
(YT/'youtube-publish.md').write_text(md)
titles=['빈 소매 안에서 누가 제 손목을 잡았어요','막배 뒤 마른 잔교에서 올라온 손','철거한 펜션에 없는 객실의 키가 돌아왔다']
hooks=['빈 코트 소매 안에서 누가 제 손목을 잡았어요. 접수 사진에는 없던 봉제선이 다음 날 어깨까지 올라와 있었습니다.','막배 뒤 마른 철판에 눌림 자국 두 개가 생겼어요. 난간마다 회색 가루가 묻었는데 맨 끝만 깨끗했습니다.','철거한 펜션의 객실은 아홉 개인데 번호 없는 키가 반납됐습니다. 다음 날 그 키가 다시 걸리고 도면에는 없던 칸이 생겼어요.']
items=[]
for i,(title,hook) in enumerate(zip(titles,hooks),1):
 sid=f'shorts-{i:02}';stem=f'{P.name}-{sid}';publish_time=f'2026-10-{13+i:02} 20:30 KST 권장. 본편 공개 이후 하루 한 편씩 테스트합니다.'
 desc=hook+'\n\n가상의 인물과 장소로 만든 창작 공포입니다.\n전체 이야기는 이 쇼츠의 관련 동영상에서 이어집니다.\n\n#공포이야기 #창작괴담 #Shorts'
 pin='이 뒤에 무슨 일이 있었을까요? 전체 이야기는 관련 동영상에서 확인해 주세요. 결말 스포일러는 첫 줄에 표시해 주세요.'
 related='YouTube Studio → 이 쇼츠의 관련 동영상 → '+TITLE+' ('+P.name+'). 본편을 채널에 업로드한 후 이 정확한 영상을 선택합니다. 설명란 URL로 대체하지 않습니다.'
 sf=[('쇼츠 제목',title+' #Shorts'),('설명',desc),('해시태그','#공포이야기 #창작괴담 #Shorts'),('고정 댓글',pin),('추천 공개 시간',publish_time),('관련 동영상 지정',related)]
 (SH/f'{sid}-publish.md').write_text('# '+title+'\n\n'+''.join(f'## {k}\n\n{v}\n\n' for k,v in sf)+'## 제작\n\n본편과 별도로 작성·승인된 원고, 새 세로 이미지와 독립 9:16 편집. Esther V4 생성 후 1.07배속. 자막은 영상에 포함하며 외부 자막 파일은 없음.\n')
 (SH/f'{sid}-publish.html').write_text(helper(title,sf,f'<video controls preload="metadata" src="../../06_delivery/shorts/{stem}.mp4"></video>', '<p>관련 동영상 지정은 본편 업로드 후 YouTube Studio에서 완료하세요. 아직 실제 YouTube 영상 URL이 없으므로 링크를 임의로 기입하지 않았습니다.</p>'))
 items.append({'short_id':sid,'title':title,'related_video_title':TITLE,'related_video_project_id':P.name,'video':f'06_delivery/shorts/{stem}.mp4','recommended_publish_time':publish_time,'external_caption_files_delivery':False})
(SH/'shorts-publish.json').write_text(json.dumps({'project_id':P.name,'shorts':items},ensure_ascii=False,indent=2)+'\n')
(SH/'shorts-publish.md').write_text('# 029 · 쇼츠 세 편 게시 전략\n\n본편: '+TITLE+'\n\n'+''.join(f'- {i}. {title}: [게시 전략](shorts-{i:02}-publish.md) · [복사 도우미](shorts-{i:02}-publish.html)\n' for i,title in enumerate(titles,1))+'\n각 쇼츠는 별도 승인 원고와 새 세로 이미지로 제작했습니다. 1080×1920·60fps, Esther V4 생성 후 1.07배속이며 길이는 각각 21.76/20.88/19.78초입니다. 자막은 영상에 포함하며 외부 SRT/VTT는 전달하지 않습니다.\n\n본편 업로드 후 YouTube Studio의 관련 동영상에 위 본편을 정확히 지정하세요. 권장 공개 시간은 10월 14·15·16일 20:30 KST이며 실험 제안입니다.\n')
(SH/'shorts-publish.html').write_text(helper('029 · 쇼츠 세 편',[],extra=''.join(f'<section><h2>{i}. {html.escape(title)}</h2><video controls preload="metadata" src="../../06_delivery/shorts/{P.name}-shorts-{i:02}.mp4"></video><p><a href="shorts-{i:02}-publish.html">이 쇼츠의 게시 전략 열기</a></p></section>' for i,title in enumerate(titles,1))))

# Native typography over individually approved image assets; no semantic raster edits.
c=P/'04_composition/thumbnails';c.mkdir(exist_ok=True)
if not (c/'assets').exists():(c/'assets').symlink_to('../assets')
for letter,asset,lines,color in [('a','TH-A',['소매 안의','손'],'#f3ead8'),('b','TH-B',['물 위의','손'],'#c9dfdd')]:
 text=''.join(f'<span>{line}</span>' for line in lines)
 page=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>@font-face{{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}}*{{box-sizing:border-box}}body{{margin:0;background:#070b0f;font-family:'Apple SD Gothic Neo',sans-serif}}main{{position:relative;width:1280px;height:720px;overflow:hidden}}img{{position:absolute;width:100%;height:100%;object-fit:cover}}.shade{{position:absolute;inset:0;background:linear-gradient(90deg,#05090fee 0%,#05090f99 25%,transparent 56%)}}.copy{{position:absolute;left:58px;top:185px;font-size:{110 if letter=='a' else 92}px;font-weight:900;line-height:1.2;color:{color};text-shadow:0 5px 7px #000;-webkit-text-stroke:3px #090b0d;paint-order:stroke fill;letter-spacing:-3px}}.copy span{{display:block}}.label{{position:absolute;left:62px;top:115px;font-size:25px;letter-spacing:3px;color:#cfbf9c}}</style></head><body><main id="thumb-{letter}" data-composition-id="thumb-{letter}" data-width="1280" data-height="720" data-start="0" data-duration="0.1" data-fps="60"><img id="thumb-image-{letter}" class="clip" data-start="0" data-duration="0.1" src="assets/visuals/{asset}.png"><div class="shade"></div><div class="label">창작 공포 3편</div><div class="copy">{text}</div></main><script src="assets/gsap.min.js"></script><script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:.1}},0);window.__timelines['thumb-{letter}']=tl;</script></body></html>'''
 (c/f'thumbnail-{letter}.html').write_text(page)
print('Publishing helpers and thumbnail compositions prepared.')
