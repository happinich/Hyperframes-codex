"""030 episode publishing copy and typography over reviewed new backgrounds."""
from pathlib import Path
import json,html
P=Path(__file__).resolve().parent;TITLE='빈 저울의 영점을 맞췄더니 옆 의자가 눌렸어요 | 창작 공포 3편';WORK='빈집·과수원·고물상의 밤 | 창작 공포 3편'
ALT=['빈집 장롱 안에 없던 의자가 생겼어요 | 창작 공포 3편','폐원한 과수원에서 나무가 따라왔어요 | 창작 공포 3편','아무것도 없는 저울에 32kg이 남아 있었어요 | 창작 괴담 3편','장롱 뒤의 여자와 움직이는 나무, 영점 금지 저울 | 공포 이야기 3편',WORK]
DESC='''빈집 정리 중 생겨난 작은 의자, 폐원한 과수원의 바람을 따르지 않는 나무, 고물상 빈 저울에 남은 무게.
각기 다른 장소에서 시작해 끝까지 이어지는 세 편의 독립적인 창작 공포 이야기입니다.

00:00 장롱 뒤에 서 있던 여자
07:55 폐원한 과수원의 나무가 따라왔어요
16:48 빈 저울의 영점을 맞추지 마세요

가상의 인물과 장소를 바탕으로 만든 오리지널 창작입니다. 실제 사건이나 제보를 실화로 재현한 영상이 아닙니다.
장롱편은 거친 회화풍, 과수원편은 종이 무대풍, 고물상편은 고전 3D 게임풍으로 표현했습니다.

제작: 어둠 속 이야기
나레이션: ElevenLabs V4 · Esther · 본편 원래 속도 1.00x
이미지·음악: 이번 회차용 생성 자산 / 공간음·사건 효과음: 자체 제작
YouTube 자동 자막을 사용합니다.

화면 구도 참고 자료: 카메라 높이에 따라 단서가 드러나는 방식만 참고했습니다. 이야기·결말·영상·음원은 재사용하지 않았습니다.
https://www.youtube.com/watch?v=Kyjxoqovpyw&t=35s
https://www.youtube.com/watch?v=qfBDx-TeBaQ&t=935s

다음 감상 추천: 「돌아오지 말아야 할 것들 | 창작 공포 3편」 또는 창작 공포 재생목록.
마지막 화면의 관련 영상이나 재생목록을 선택해 주세요.

#공포이야기 #창작괴담 #어둠속이야기'''
PIN='세 이야기 중 가장 섬뜩했던 단서는 무엇이었나요? 장롱 안 의자 / 과수원의 나무 / 빈 저울의 무게로 남겨 주세요. 결말을 이야기할 때는 첫 줄에 [스포일러]를 붙여 주세요.'
TAGS='공포 이야기,창작 괴담,어둠 속 이야기,빈집 괴담,장롱 귀신,과수원 괴물,나무 괴담,고물상 괴담,영점 금지,규칙 괴담,심야 괴담,귀신,괴물,한국 공포'
TIME='2026-10-15 22:00 KST 권장. 채널 분석으로 확정한 최적 시간이 아닌 이번 회차의 실험 제안입니다.'
SNS='빈집 장롱 안에는 없던 의자가 생겼고, 폐원한 과수원에서는 나무의 자리가 바뀌었습니다. 고물상 빈 저울의 영점을 맞추자 옆 의자가 눌렸어요. 독립적인 창작 공포 3편을 한 영상으로 만나보세요.'
YT=P/'07_publish/youtube';SH=P/'07_publish/shorts';YT.mkdir(parents=True,exist_ok=True);SH.mkdir(parents=True,exist_ok=True)
def helper(title,fields,media='',extra=''):
 blocks=''.join(f'<section><h2>{html.escape(k)}</h2><textarea id="copy-{i}" readonly rows="{min(16,max(2,v.count(chr(10))+2))}">{html.escape(v)}</textarea><button data-copy="copy-{i}">복사</button></section>' for i,(k,v) in enumerate(fields))
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{margin:0;background:#11161b;color:#eee;font:17px/1.6 sans-serif}}main{{max-width:1020px;margin:auto;padding:32px 24px}}h1{{font-size:30px;line-height:1.4}}h2{{font-size:21px}}section{{background:#202831;padding:20px;border-radius:12px;margin:24px 0}}textarea{{width:100%;box-sizing:border-box;padding:14px;background:#101820;color:#eee;font:16px/1.6 sans-serif;border:1px solid #798693;resize:vertical}}button{{padding:12px 25px;margin-top:12px;background:#d9bb80;border:0;border-radius:6px;font-weight:bold}}img{{width:min(100%,460px);margin:10px}}video{{width:min(100%,340px)}}a{{color:#add5ff}}</style></head><body><main><h1>{html.escape(title)}</h1><p>창작 공포 · YouTube 자동 자막 · 외부 SRT/VTT 없음</p>{media}{blocks}{extra}<p id="status" role="status"></p></main><script>document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=async()=>{{const t=document.getElementById(b.dataset.copy);try{{await navigator.clipboard.writeText(t.value)}}catch{{t.focus();t.select();document.execCommand('copy')}}document.getElementById('status').textContent='복사했습니다.'}});</script></body></html>'''
fields=[('메인 제목',TITLE),('대안 제목 5개','\n'.join(ALT)),('설명',DESC),('고정 댓글',PIN),('태그',TAGS),('SNS 홍보 문구',SNS),('추천 공개 시간',TIME),('마지막 화면','25:38~25:58의 오른쪽 안전 영역에 기존 029 영상 「돌아오지 말아야 할 것들 | 창작 공포 3편」을 실제 채널에서 확인 후 지정. 아직 게시하지 않았다면 창작 공포 재생목록 지정.'),('썸네일 운영','A: 빈 곳의 무게 — 빈 철판과 32. B: 누가 놓았지 — 장롱 안 뒤돌아선 의자. 제목과 문구를 반복하지 않으며 각 안은 하나의 단서를 사용합니다.')]
(YT/'youtube-publish.md').write_text('# 030 · YouTube 게시 전략\n\n'+''.join(f'## {k}\n\n{v}\n\n' for k,v in fields)+'## 납품\n\n본편 1920×1080·60fps 약 25:58, 연속 번인 자막 없음. 새 9:16 쇼츠 3편·번인 자막 포함. 본편 MP4는 로컬, 게시 자료·썸네일·쇼츠는 Drive 전달. 실제 YouTube 업로드는 수행하지 않았습니다.\n')
(YT/'youtube-publish.html').write_text(helper(TITLE,fields,'<img src="thumbnail-a.png" alt="빈 곳의 무게"><img src="thumbnail-b.png" alt="누가 놓았지">'))
(YT/'publishing.json').write_text(json.dumps({'project_id':P.name,'working_title':WORK,'main_title':TITLE,'alternative_titles':ALT,'description':DESC,'pinned_comment':PIN,'tags':TAGS,'recommended_time':TIME,'youtube_upload_status':'not_uploaded'},ensure_ascii=False,indent=2)+'\n')
short_titles=['장롱 안 의자는 뒤를 보고 있었어요','바람이 없는데 나무의 자리가 바뀌었어요','영점을 누르자 빈 의자가 눌렸어요'];items=[]
for n,title in enumerate(short_titles,1):
 sid=f'shorts-{n:02}';stem=f'{P.name}-{sid}';related=f'YouTube 관련 동영상에서 본편 「{TITLE}」 (프로젝트 {P.name})를 선택합니다. 본편 업로드 후 실제 이 영상을 지정하고 설명란 URL로 대체하지 않습니다.'
 sf=[('제목',title+' #Shorts'),('설명','독립적인 오리지널 창작 공포의 결말 없는 티저입니다. 본편의 정체와 결말은 관련 동영상에서 이어집니다. 가상의 인물과 장소이며 실화가 아닙니다.\n\n#공포이야기 #창작괴담 #Shorts'),('해시태그','#공포이야기 #창작괴담 #Shorts'),('고정 댓글','관련 동영상에서 세 편의 본편을 이어 볼 수 있습니다. 결말 댓글에는 [스포일러]를 붙여 주세요.'),('추천 공개 시간',f'2026-10-{15+n:02} 20:30 KST 권장. 실험 제안입니다.'),('관련 동영상 지정',related)]
 (SH/f'{sid}-publish.md').write_text('# '+title+'\n\n'+''.join(f'## {k}\n\n{v}\n\n' for k,v in sf)+'## 제작\n\n별도 원고·별도 V4 음성·새 세로 이미지 4장·독립 9:16 구성. 음성은 피치를 유지한 1.07x 후처리, 본편 결말 노출 없음. 1080×1920·60fps, 영상 내 자막 포함. 외부 SRT/VTT 없음.\n')
 (SH/f'{sid}-publish.html').write_text(helper(title,sf,f'<video controls preload="metadata" src="../../06_delivery/shorts/{stem}.mp4"></video>'))
 items.append({'short_id':sid,'title':title,'related_video_title':TITLE,'related_video_project_id':P.name,'video':f'06_delivery/shorts/{stem}.mp4','recommended_time':sf[4][1],'external_caption_files_delivery':False})
(SH/'shorts-publish.json').write_text(json.dumps({'project_id':P.name,'shorts':items},ensure_ascii=False,indent=2)+'\n')
(SH/'shorts-publish.md').write_text('# 030 · 쇼츠 3편\n\n본편: '+TITLE+'\n\n'+''.join(f'- {n}. {title}: [게시 자료](shorts-{n:02}-publish.md) · [복사 도우미](shorts-{n:02}-publish.html)\n' for n,title in enumerate(short_titles,1))+'\n길이 약 15.93 / 16.45 / 15.79초, 각 4장의 새 세로 이미지와 별도 음성. 관련 동영상에 위 본편을 정확히 지정합니다.\n')
(SH/'shorts-publish.html').write_text(helper('030 · 쇼츠 3편',[],extra=''.join(f'<section><h2>{n}. {html.escape(t)}</h2><a href="shorts-{n:02}-publish.html">게시 도우미 열기</a></section>' for n,t in enumerate(short_titles,1))))
c=P/'04_composition/thumbnails';c.mkdir(exist_ok=True)
if not (c/'assets').exists():(c/'assets').symlink_to('../assets')
for letter,asset,lines in [('a','TH-A',['빈 곳의','무게']),('b','TH-B',['누가','놓았지'])]:
 overlay='<svg viewBox="0 0 1672 941" style="position:absolute;inset:0;width:100%;height:100%"><text x="1450" y="183" text-anchor="middle" font-size="65" font-family="monospace" fill="#bad89f">32</text></svg>' if letter=='a' else ''
 page=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>*{{box-sizing:border-box}}body{{margin:0;background:#090c10;font-family:sans-serif}}main{{position:relative;width:1280px;height:720px;overflow:hidden}}img{{position:absolute;width:100%;height:100%;object-fit:cover}}.copy{{position:absolute;left:52px;top:212px;color:#f5ead5;font-weight:900;font-size:101px;line-height:1.24;letter-spacing:-3px;text-shadow:0 4px 7px #000;-webkit-text-stroke:3px #07090c;paint-order:stroke fill}}.copy span{{display:block}}.label{{position:absolute;left:60px;top:127px;font-size:25px;letter-spacing:3px;color:#d4c4a8}}.accent{{position:absolute;left:60px;top:176px;width:89px;height:9px;background:#bd3831}}</style></head><body><main data-composition-id="thumb-{letter}" data-width="1280" data-height="720" data-duration="0.1" data-fps="60"><img src="assets/visuals/{asset}.png">{overlay}<div class="label">창작 공포 3편</div><div class="accent"></div><div class="copy">{''.join('<span>'+s+'</span>' for s in lines)}</div></main><script src="assets/gsap.min.js"></script><script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:.1}},0);window.__timelines={{'thumb-{letter}':tl}};</script></body></html>'''
 (c/f'thumbnail-{letter}.html').write_text(page)
 # Snapshot CLI uses index.html; isolate each thumbnail composition without changing shared assets.
 folder=c/letter;folder.mkdir(exist_ok=True)
 if not (folder/'assets').exists():(folder/'assets').symlink_to('../../assets')
 (folder/'index.html').write_text(page)
print('030 public title, 5 alternatives, helpers, 3 Related Video targets and 2 thumbnail compositions prepared')
