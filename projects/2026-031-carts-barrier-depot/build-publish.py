"""Author local and portable publishing copy; no platform publishing action."""
import html,json,shutil,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;O=P/'07_publish';Y=O/'youtube';S=O/'shorts';Y.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
title='아무도 없는데, 누가 밀고 있었다｜창작 괴담 3편'
alts=['막차가 끝난 차고지에서, 빈 버스가 나를 따라왔다｜창작 괴담 3편','마른 바닥, 젖은 손잡이… 마지막 한 대가 이상했다｜직업 괴담 3편','벽 안의 발소리와 운전기사 없는 버스｜창작 공포 3편','퇴근하려던 사람들만 본 것들｜마트·방음벽·차고지 괴담','그날 야간 근무를 끝내지 말았어야 했다｜창작 괴담 3편']
sources=[('돌비공포라디오 · 야근 금지 회사','https://www.youtube.com/watch?v=yL4tbBaVuH4'),('왓섭! 공포라디오 · 오대산에서 생긴 일','https://www.youtube.com/watch?v=bsI8CG-SuhQ'),('괴들남 공포이야기 · 제주도 택시 손님 사건','https://www.youtube.com/watch?v=G9cW9c8qu3g'),('Mr. Nightmare · 공간 시점 참고','https://www.youtube.com/watch?v=Kyjxoqovpyw&t=35s')]
desc='''모두 돌아간 뒤에도 움직이는 것이 있었습니다.
마른 바닥 위의 젖은 손잡이, 방음벽 안에서 따라오는 발소리, 현재 위치로 바뀌는 버스 행선지.
서로 다른 일터에서 겪는 세 편의 완결 창작 괴담입니다.

00:00 맨 뒤 카트의 젖은 손잡이
06:56 방음벽 안에서 따라오는 것
13:51 예비 버스의 다음 정류장

※ 본 영상은 창작 공포 이야기입니다. 검증된 실화 또는 실제 사건 재현물이 아닙니다.
공개 공포 영상의 일반 모티프에서 착안해 인물·장소·사건·결말을 새로 구성했습니다. 원작 대사·녹음·영상·삽화는 사용하지 않았습니다.

참고 모티프 및 화면 시점 출처
'''+ '\n'.join(f'{name}\n{url}' for name,url in sources)+'''

AI 생성 음성과 생성 일러스트를 사용했습니다. 실제 촬영·실제 현장 녹음이 아닙니다.
본편 자막은 YouTube 자동 자막을 이용해 주세요.
재생목록 분류: 직업 괴담 · 공포괴담 본편

#공포라디오 #창작괴담 #직업괴담'''
tags='공포라디오,창작괴담,직업괴담,야간근무,마트괴담,카트괴담,방음벽,미확인존재,버스괴담,차고지,괴담모음,무서운이야기,한국공포,잠들기전괴담'
pin='셋 중에서 혼자 마주치기 가장 싫은 것은 무엇인가요? ① 젖은 손잡이 ② 벽 안의 발소리 ③ 빈 버스\n다음 편도 평범한 일터에서 시작되는 창작 괴담으로 찾아오겠습니다. 경험을 남기실 때는 개인정보를 빼 주세요. 별도 작품으로 채택할 때 사용 허락과 익명 처리 범위를 먼저 확인합니다.'
sns='아무도 없는데, 누가 밀고 있었다.\n마트의 마지막 카트부터 운전석이 빈 예비 버스까지. 세 편의 완결 창작 괴담을 한 영상에 담았습니다.\n#공포라디오 #창작괴담 #직업괴담'
metadata={'project_id':P.name,'title':title,'alternative_titles':alts,'description':desc,'tags':tags,'pinned_comment':pin,'sns_copy':sns,'content_nature':'fiction','recommended_publish_kst':'2026-10-21 22:00','schedule_basis':'config/horror-channel-strategy.json fallback_release_schedule_kst; audience heatmap not supplied','playlist':'직업 괴담','end_screen':{'start_seconds':1231.997,'end_seconds':1249.997,'primary':'직업 괴담 public playlist','secondary':'subscribe','youtube_control_action':'업로드 후 해당 공개 재생목록과 구독 요소를 배치'},'main_mp4':f'{P.name}-youtube.mp4','captions':'YouTube automatic; no external SRT/VTT','thumbnail_primary':'thumbnail-a.png','thumbnail_alternative':'thumbnail-b.png','public_upload_status':'not_requested_not_uploaded'}
def helper(name,fields,video,portable=False,thumbs=False):
 blocks=[]
 for i,(label,value) in enumerate(fields):
  blocks.append(f'<section><h2>{html.escape(label)}</h2><button onclick="copy({i})">복사</button><textarea id="field-{i}" readonly>{html.escape(value)}</textarea></section>')
 thumb=''.join(f'<a href="thumbnail-{k}.png"><img src="thumbnail-{k}.png" alt="썸네일 {k.upper()}"></a>' for k in 'ab') if thumbs else ''
 return f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(name)}</title><style>body{{font-family:system-ui,sans-serif;max-width:1000px;margin:32px auto;padding:0 22px;color:#e8e5dc;background:#111923}}h1{{line-height:1.3}}h2{{font-size:20px}}section{{padding:18px 0;border-bottom:1px solid #40505b}}button{{padding:9px 18px;cursor:pointer}}textarea{{display:block;margin-top:12px;width:100%;min-height:120px;white-space:pre-wrap;background:#1a2632;color:#eee9df;border:1px solid #51616c;padding:14px;font:16px/1.5 system-ui}}video{{width:100%;max-height:560px}}img{{width:48%;margin:1%}}a{{color:#cbdcae}}small{{color:#aebbc6}}</style><h1>{html.escape(name)}</h1><p>창작 공포 · 게시용 자료. 복사 버튼은 이 폴더를 내려받아 브라우저에서 사용할 수 있습니다.</p><p><a href="{video}">최종 MP4 열기</a></p><video controls preload="metadata" src="{video}"></video>{thumb}{''.join(blocks)}<p id="status" role="status"></p><script>async function copy(i){{const t=document.getElementById('field-'+i);try{{await navigator.clipboard.writeText(t.value)}}catch(e){{t.focus();t.select();document.execCommand('copy')}}document.getElementById('status').textContent='복사했습니다.'}}</script></html>'''
fields=[('메인 제목',title),('대안 제목 5개','\n'.join(alts)),('설명',desc),('태그',tags),('고정 댓글',pin),('SNS 홍보',sns),('추천 게시 시간','2026-10-21(수) 22:00 KST. 시청자 활동 데이터가 없어 채널 기본 일정을 사용한 제안입니다.'),('엔드스크린','20:32–20:50: 공개 재생목록 「직업 괴담」 + 구독. 표시가 문과 손잡이 단서를 가리지 않게 오른쪽 안전 영역에 배치하세요.')]
md='# '+title+'\n\n'+'\n\n'.join('## '+k+'\n\n'+v for k,v in fields)+'\n';(Y/'youtube-publish.md').write_text(md);(Y/'youtube-publish.html').write_text(helper(title,fields,'../../06_delivery/youtube/'+metadata['main_mp4'],thumbs=True));(Y/'youtube-publish.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
for k in 'ab':shutil.copy2(O/f'thumbnail-{k}.png',Y/f'thumbnail-{k}.png')
short_titles=['카트 안은 비었는데, 운동화가 돌아갔다','벽을 두드린 손을 뗐는데도 대답이 왔다','빈 버스의 행선지가 내 위치로 바뀌었다']
days=['2026-10-22(목) 20:30 KST','2026-10-23(금) 20:30 KST','2026-10-24(토) 20:30 KST'];shorts=[]
for n,st in enumerate(short_titles,1):
 sid=f'shorts-{n:02}';sd=f'평범한 야간 근무에서 시작된 창작 괴담입니다.\n세 편의 완결 이야기는 이 쇼츠의 관련 동영상에서 이어집니다.\n※ 창작 이야기 · AI 생성 음성/이미지 사용.\n#공포라디오 #창작괴담 #Shorts';related=f'프로젝트: {P.name}\n본편 제목: {title}\n본편 파일: {metadata["main_mp4"]}\n업로드 후 YouTube Studio의 「관련 동영상」에서 이 본편을 선택하세요. 본편 공개 이후 쇼츠를 게시하세요. 설명란의 비클릭 URL로 대체하지 않습니다.';sp='그 자리에 있었다면 바로 나왔을까요, 한 번 더 확인했을까요? 관련 동영상에서 세 편의 완결 창작 괴담을 들을 수 있습니다.'
 sf=[('제목',st+' #Shorts'),('설명',sd),('고정 댓글',sp),('관련 동영상 · 정확한 본편 대상',related),('추천 게시 시간',days[n-1]+' · 시청자 활동 데이터 없는 기본 일정 제안'),('SNS 홍보',st+'\n관련 동영상에서 본편을 만나세요. #창작괴담 #Shorts')]
 (S/f'{sid}-publish.md').write_text('# '+st+'\n\n'+'\n\n'.join('## '+k+'\n\n'+v for k,v in sf)+'\n');(S/f'{sid}-publish.html').write_text(helper(st,sf,f'../../06_delivery/shorts/{P.name}-{sid}.mp4'));shorts.append({'short_id':sid,'title':st+' #Shorts','description':sd,'pinned_comment':sp,'recommended_publish_kst':days[n-1],'related_video_project_id':P.name,'related_video_title':title,'related_video_filename':metadata['main_mp4'],'related_video_url':'available_only_after_main_youtube_upload'})
(S/'shorts-publish.json').write_text(json.dumps({'project_id':P.name,'shorts':shorts},ensure_ascii=False,indent=2)+'\n');(O/'README.md').write_text(f'# {title}\n\n본편은 youtube/youtube-publish.html, 쇼츠 세 편은 shorts/shorts-01~03-publish.html에서 확인하세요.\n\n창작 공포이며 실화로 표시하지 않습니다. 본편은 자동 자막, 쇼츠는 번인 자막입니다. 외부 SRT/VTT는 납품하지 않습니다.\n\n추천 본편 게시: 2026-10-21 22:00 KST. 실제 YouTube 업로드는 수행하지 않았습니다.\n')
print('Publishing MD/HTML/JSON written for main and 3 Shorts')
