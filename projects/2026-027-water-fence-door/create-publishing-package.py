"""Build episode-specific local and portable publishing helpers for three Shorts."""
from pathlib import Path
import json
import html
import shutil
import hashlib
import argparse

P = Path(__file__).resolve().parent
TITLE = '벽과 울타리로 막을 수 없었던 것들 | 공포 이야기 3편'
plan = json.loads((P / '01_script/scene-plan.json').read_text())
shortplans = json.loads((P / '01_script/shorts-scene-plans.json').read_text())['shorts']
titles = ['물이 없는 저수조에서 누가 헤엄쳤다', '울타리 밖의 몸이 접히기 시작했다', '배달된 문 뒤에서 의자가 끌렸다']
times = ['본편 공개 다음 날 20:30 KST', '본편 공개 2일 후 20:30 KST', '본편 공개 3일 후 20:30 KST']
questions = ['마른 사다리에서 물이 떨어진다면 더 가까이 보실 건가요?', '울타리 밖에서 움직임을 따라 한다면 바로 떠나실 건가요?', '문 뒤에 벽이 있어야 한다면, 그 소리는 어디서 났을까요?']
alts = ['물을 뺀 저수조, 산속 울타리, 배달된 문 | 창작 괴담 3편', '물이 없는데 누가 헤엄치고 있었다 | 공포 이야기 3편', '철망보다 높았던 것이 차창 아래로 내려왔다 | 괴담 3편', '이삿짐에 없던 문이 왔고, 안쪽에서 잠금쇠가 돌아갔다', '빈 곳에서 들린 소리, 그 뒤에 남은 흔적 | 공포 이야기 3편']
def timestamp(seconds, millis=False):
    whole=int(seconds); base=f'{whole//60:02}:{whole%60:02}'
    return base+f'.{round((seconds-whole)*1000):03}' if millis else base
chapter_timestamps='\n'.join(timestamp(c['start_seconds'])+' '+c['title'] for c in plan['chapters'])
end_screen_start=timestamp(plan['duration_seconds']-20,True)
end_screen_end=timestamp(plan['duration_seconds'],True)
duration_label=f"{int(plan['duration_seconds'])//60}분 {int(plan['duration_seconds'])%60}초"
description = f'''벽과 울타리를 사이에 두면 안전할 줄 알았습니다.
물을 뺀 저수조, 산속 캠핑장, 새로 이사한 집에서 시작되는 세 편의 창작 공포 이야기입니다.

{chapter_timestamps}

세 이야기는 가상의 인물과 장소로 만든 오리지널 창작입니다. 실제 사건이나 제보를 실화로 재현한 영상이 아닙니다.
이미지는 생성형 AI로 제작한 비실사 일러스트이며, 내레이션은 AI 음성으로 제작했습니다.
다른 채널의 이야기·영상·음성·음원을 재사용하지 않았습니다.
화면 자막 없이 감상할 수 있으며, 한국어 자막은 플레이어의 자막 기능으로 선택할 수 있습니다.

가장 오래 남은 장소가 저수조, 캠핑장, 배달된 문 중 어디였는지 댓글로 알려 주세요.
어둠 속 이야기 — 한국 일상 공간에서 시작되는 창작 공포.

#공포이야기 #창작괴담 #어둠속이야기'''
main = {
    'project_id': P.name, 'channel': '어둠 속 이야기', 'title': TITLE,
    'alternative_titles': alts, 'description': description,
    'tags': ['공포 이야기', '창작 괴담', '어둠 속 이야기', '저수조 괴담', '캠핑장 공포', '이사 괴담', '괴물', '도시괴담', '한국 공포', '심야 괴담'],
    'hashtags': ['#공포이야기', '#창작괴담', '#어둠속이야기'],
    'pinned_comment': '세 곳 중 어디가 가장 무서웠나요? ① 빈 저수조 ② 캠핑장 울타리 ③ 배달된 문\n가장 이상했던 단서도 함께 알려 주세요. 결말을 이야기할 때는 첫 줄에 [스포일러]를 붙여 주세요.',
    'sns_copy': '마른 저수조에서 물장구가 들렸고, 울타리 밖의 몸이 옆으로 접혔습니다. 배달된 문 뒤에는 벽이 있어야 했어요. 익숙한 세 곳에서 시작되는 창작 공포, 「벽과 울타리로 막을 수 없었던 것들」. 어둠 속 이야기에서 공개합니다.',
    'recommended_release': '최종 확인을 마친 공개일 22:00 KST',
    'schedule_basis': '채널 시청자 활동 데이터가 없는 상태의 기본 운영 일정. 최고 성과 시간이라는 의미는 아니다.',
    'duration_seconds': plan['duration_seconds'], 'truth_label': 'fiction',
    'published_youtube_url': None, 'published_video_id': None,
    'chapters': [{'start_seconds': c['start_seconds'], 'title': c['title']} for c in plan['chapters']],
    'thumbnail_recommendation': 'A로 시작. B는 배달된 문 소재에 반응이 높을 때 대안으로 비교한다. 두 이미지를 동시에 합성하지 않는다.',
    'end_screen': {'start_seconds': round(plan['duration_seconds']-20, 3), 'duration_seconds': 20,
                   'primary': '아무도 없어야 할 곳에 남아 있던 것들 | 공포 이야기 3편',
                   'target_project_id': '2026-026-three-places-after-hours',
                   'selection_condition': '026 본편이 공개되어 있으면 해당 영상을 선택한다. 아직 공개하지 않았다면 채널의 공개 공포 본편 재생목록을 선택한다.',
                   'secondary': '어둠 속 이야기 구독', 'target_url': None},
    'analytics': '공개 48시간 후와 7일 후 CTR, 첫 30초 유지율, 챕터 경계 이탈, 평균 시청 시간, 엔드스크린 클릭을 확인한다. 이번 합본은 사용자 요청에 따른 회차 한정이며 향후 기본 포맷은 단일 이야기다.'
}
shorts = []
for i in range(1, 4):
    shorts.append({'project_id': P.name, 'short_id': f'shorts-{i:02}', 'title': titles[i-1],
                   'description': f'{titles[i-1]}. 결말은 본편에서 이어집니다.\n본편: {TITLE}\n\n가상의 장소와 인물로 만든 창작 공포입니다. AI 일러스트와 AI 음성을 사용했습니다.\n\n#Shorts #공포이야기 #창작괴담 #어둠속이야기',
                   'hashtags': ['#Shorts', '#공포이야기', '#창작괴담', '#어둠속이야기'],
                   'pinned_comment': questions[i-1] + '\n본편은 화면의 관련 동영상에서 이어집니다. 결말 댓글은 [스포일러] 표시를 부탁드립니다.',
                   'recommended_release': times[i-1], 'schedule_basis': main['schedule_basis'],
                   'duration_seconds': shortplans[i-1]['duration_seconds'], 'truth_label': 'fiction',
                   'related_video': {'title': TITLE, 'project_id': P.name, 'youtube_url': None, 'youtube_video_id': None,
                                     'action': '본편 공개 후 이 제목의 실제 업로드 영상을 YouTube의 관련 동영상 항목에서 선택한다. 쇼츠 설명의 일반 URL에 의존하지 않는다.'},
                   'sns_copy': titles[i-1] + '. 짧은 창작 공포 예고편. 정체와 결말은 관련 본편에서 이어집니다.',
                   'spoiler_check': '별도 대본·새 세로 이미지. 정체, 신체 접촉, 탈출 선택, 최종 반전을 공개하지 않는다.'})

CSS = '''*{box-sizing:border-box}body{margin:0;background:#101410;color:#ebece4;font:16px/1.6 system-ui,sans-serif}main{max-width:1040px;margin:auto;padding:28px 20px 70px}h1{font-size:30px;line-height:1.35}h2{font-size:21px;margin:0}section{background:#1b211c;border:1px solid #374138;border-radius:13px;padding:20px;margin:18px 0}textarea{display:block;width:100%;min-height:100px;resize:vertical;border:1px solid #536052;border-radius:8px;background:#121812;color:#f2f2e8;padding:14px;font:16px/1.6 system-ui;margin-top:12px}button,a.button{cursor:pointer;background:#d4dac7;color:#101510;border:0;border-radius:7px;padding:10px 15px;display:inline-block;text-decoration:none;font:inherit;margin:9px 8px 0 0}button:focus-visible,a:focus-visible{outline:3px solid #ccad6b}.thumbs{display:grid;grid-template-columns:1fr 1fr;gap:15px}img{width:100%;height:auto;border-radius:8px}video{max-width:100%;max-height:660px;background:#101410;border-radius:8px}.note{color:#c4cbbc}.status{min-height:25px;color:#d6d3af}nav{display:flex;gap:12px;flex-wrap:wrap}li{margin:6px 0}@media(max-width:650px){.thumbs{grid-template-columns:1fr}h1{font-size:24px}main{padding:18px 13px}}'''
JS = '''document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{const t=document.getElementById(b.dataset.copy),s=b.parentElement.querySelector('.status');try{await navigator.clipboard.writeText(t.value);s.textContent='복사했습니다.';}catch(e){t.focus();t.select();const ok=document.execCommand('copy');s.textContent=ok?'복사했습니다.':'텍스트를 선택했습니다. 복사 단축키로 복사해 주세요.';}}));'''
def block(label, content, ident, rows=4):
    return f'<section><h2>{html.escape(label)}</h2><textarea id="{ident}" readonly rows="{rows}" aria-label="{html.escape(label)}">{html.escape(content)}</textarea><button data-copy="{ident}">{html.escape(label)} 복사</button><p class="status" role="status" aria-live="polite"></p></section>'
def document(title, body):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+CSS+'</style></head><body><main>'+body+'</main><script>'+JS+'</script></body></html>'
def main_html(portable=False):
    thumbprefix = ''
    links = ''.join(f'<a class="button" href="{("shorts-"+str(i).zfill(2)+"-publish.html") if portable else ("../shorts/shorts-"+str(i).zfill(2)+"-publish.html")}">쇼츠 {i} 게시 전략</a>' for i in range(1,4))
    body=f'<h1>{html.escape(TITLE)}</h1><p class="note">어둠 속 이야기 · 오리지널 창작 · {duration_label} · 본편 1개와 별도 쇼츠 3개</p><nav>{links}</nav>'
    if not portable:
        body += f'<section><h2>본편 영상</h2><video controls preload="metadata" src="../../06_delivery/youtube/{P.name}-youtube.mp4"></video></section>'
    else: body += '<p>본편 MP4는 요청에 따라 드라이브에 포함하지 않았습니다. 로컬 작업 폴더에서 업로드해 주세요.</p>'
    body += block('본편 제목',TITLE,'title',2)+block('대안 제목 5개','\n'.join(alts),'alternatives',6)+block('설명',description,'description',20)
    body += block('태그',', '.join(main['tags']),'tags',3)+block('고정 댓글',main['pinned_comment'],'pinned',5)+block('SNS 홍보 문구',main['sns_copy'],'sns',5)
    body += '<section><h2>썸네일 2종</h2><p>A: 물이 없는데 / B: 벽 뒤에 누가</p><div class="thumbs"><div><img src="thumbnail-a.png" alt="썸네일 A 물이 없는데"><a class="button" href="thumbnail-a.png" download>썸네일 A 저장</a></div><div><img src="thumbnail-b.png" alt="썸네일 B 벽 뒤에 누가"><a class="button" href="thumbnail-b.png" download>썸네일 B 저장</a></div></div><p>'+html.escape(main['thumbnail_recommendation'])+'</p></section>'
    body += f'<section><h2>공개와 연결</h2><p>본편 권장: 최종 확인을 마친 공개일 22:00 KST</p><p>'+main['schedule_basis']+'</p><ul><li>한국어 SRT 또는 VTT를 업로드합니다.</li><li>마지막 20초({end_screen_start}~{end_screen_end})의 오른쪽 영역에 관련 본편/공개 재생목록과 구독 요소를 배치합니다.</li><li>본편 공개 후 쇼츠 3개의 ‘관련 동영상’에 이 본편을 직접 지정합니다.</li><li>실제 공개 URL은 업로드 후 확정됩니다.</li></ul></section>'
    body += '<section><h2>엔드스크린 대상</h2><p>'+html.escape(main['end_screen']['primary'])+'</p><p>'+html.escape(main['end_screen']['selection_condition'])+'</p></section>'
    body += '<section><h2>공개 후 확인</h2><p>'+main['analytics']+'</p></section>'
    return document('027 본편 게시 전략',body)
def short_html(i, portable=False):
    s=shorts[i-1];file=f'{P.name}-shorts-{i:02}.mp4'
    prefix='' if portable else '../../06_delivery/shorts/'
    body=f'<h1>쇼츠 {i} · {html.escape(s["title"])}</h1><a class="button" href="{"longform-publish.html" if portable else "../youtube/youtube-publish.html"}">본편 게시 전략</a><section><h2>완성 영상</h2><video controls preload="metadata" src="{prefix+file}"></video><p>1080×1920 · 60fps · {s["duration_seconds"]:.2f}초 · 별도 세로 구성 · 번인 자막</p></section>'
    body+=block('쇼츠 제목',s['title'],'title',2)+block('쇼츠 설명',s['description'],'description',11)+block('쇼츠 고정 댓글',s['pinned_comment'],'pinned',5)+block('쇼츠 SNS 문구',s['sns_copy'],'sns',4)
    body+=block('관련 동영상 제목',TITLE,'related',2)
    body+=f'<section><h2>공개 일정과 본편 연결</h2><p>권장: {s["recommended_release"]}</p><p>{s["schedule_basis"]}</p><p>{s["related_video"]["action"]}</p><p>대상 프로젝트: {P.name}</p><p>{s["spoiler_check"]}</p></section>'
    return document(f'027 쇼츠 {i} 게시 전략',body)
def md(data, short=False):
    fields=[('제목',data['title']),('설명',data['description']),('고정 댓글',data['pinned_comment']),('SNS 홍보',data['sns_copy']),('권장 공개',data['recommended_release']),('일정 기준',data['schedule_basis'])]
    if short:fields += [('관련 동영상',TITLE+'\n\n'+data['related_video']['action']),('스포일러 검수',data['spoiler_check'])]
    else:fields += [('대안 제목 5개','\n'.join(f'{i+1}. {t}' for i,t in enumerate(alts))),('태그',', '.join(data['tags'])),('썸네일',data['thumbnail_recommendation']),('엔드스크린',f'마지막 20초, {end_screen_start}부터 오른쪽에 관련 본편 또는 공개 재생목록과 구독 요소.'),('공개 후 분석',data['analytics'])]
    if not short: fields += [('엔드스크린 연결 대상',data['end_screen']['primary']+'\n\n'+data['end_screen']['selection_condition'])]
    return '# '+data['title']+'\n\n'+ '\n\n'.join('## '+k+'\n\n'+v for k,v in fields)+'\n'
def save(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n' if isinstance(data,(dict,list)) else data)

# Deliver final timing files next to their corresponding encoded videos.
for i in range(4):
    stem=P.name+(f'-shorts-{i:02}' if i else '-youtube')
    delivery=P/('06_delivery/shorts' if i else '06_delivery/youtube')
    delivery.mkdir(parents=True,exist_ok=True)
    for ext in ('srt','vtt'):
        source=P/'03_sync'/((f'shorts-{i:02}-captions' if i else 'captions')+'.'+ext)
        shutil.copy2(source,delivery/(stem+'.'+ext))

save(P/'07_publish/youtube/youtube-publish.json',main)
save(P/'07_publish/youtube/youtube-publish.md',md(main))
save(P/'07_publish/youtube/youtube-publish.html',main_html())
save(P/'07_publish/shorts/shorts-publish.json',{'project_id':P.name,'shorts':shorts})
for i,s in enumerate(shorts,1):
    save(P/f'07_publish/shorts/shorts-{i:02}-publish.html',short_html(i))
    save(P/f'07_publish/shorts/shorts-{i:02}-publish.md',md(s,True))
save(P/'07_publish/shorts/shorts-publish.html',document('027 쇼츠 게시 전략', '<h1>쇼츠 3편 게시 전략</h1>'+''.join(f'<section><h2>{i}. {html.escape(s["title"])}</h2><p>{s["recommended_release"]}</p><a class="button" href="shorts-{i:02}-publish.html">영상과 게시 전략 열기</a></section>' for i,s in enumerate(shorts,1))))

save(P/'07_publish/shorts/shorts-publish.md', '# 027 쇼츠 3편 게시 전략\n\n'+''.join(f'## {i}. {s["title"]}\n\n- [{s["title"]}](shorts-{i:02}-publish.html)\n- 영상: ../../06_delivery/shorts/{P.name}-shorts-{i:02}.mp4\n- 권장 공개: {s["recommended_release"]}\n\n' for i,s in enumerate(shorts,1)))

parser=argparse.ArgumentParser();parser.add_argument('--drive',action='store_true');args=parser.parse_args()
if args.drive:
    D=P/'07_publish/drive-upload';D.mkdir(parents=True,exist_ok=True)
    files=[(P/'07_publish/youtube/youtube-publish.md','longform-publish.md'),
           (P/'07_publish/youtube/youtube-publish.json','longform-publish.json')]
    files += [(P/f'07_publish/youtube/thumbnail-{x}.png',f'thumbnail-{x}.png') for x in 'ab']
    files += [(P/f'06_delivery/youtube/{P.name}-youtube.{ext}',f'longform-captions.{ext}') for ext in ['srt','vtt']]
    for i in range(1,4):
        files += [(P/f'06_delivery/shorts/{P.name}-shorts-{i:02}.{ext}',f'{P.name}-shorts-{i:02}.{ext}') for ext in ['mp4','srt','vtt']]
        files += [(P/f'07_publish/shorts/shorts-{i:02}-publish.md',f'shorts-{i:02}-publish.md')]
    for src,name in files:
        if not src.is_file():raise SystemExit('Required final delivery file missing: '+str(src))
        shutil.copy2(src,D/name)
    save(D/'longform-publish.html',main_html(True))
    for i in range(1,4):save(D/f'shorts-{i:02}-publish.html',short_html(i,True))
    save(D/'README.md', '# 027 전달 패키지\n\n'+TITLE+'\n\n여성 Esther · ElevenLabs eleven_v4 · 본편 원음 1.00배 · 쇼츠 1.07배 · 이야기 사이 5초 전환.\n\n본편 MP4 제외. 본편/쇼츠 게시 전략 HTML·MD, 썸네일 2종, 쇼츠 3개, 본편과 쇼츠 SRT·VTT를 포함합니다. HTML은 모든 파일을 함께 내려받아 열어 주세요. 본편 공개 후 각 쇼츠의 관련 동영상에 027 본편을 지정합니다.\n\n영상은 창작이며 실제 사건을 재현한 것이 아닙니다. 주관적 청취는 도구상 수행하지 못했습니다. 음성 인식과 신호 분석 검수 기록은 로컬 검수 폴더에 보관합니다.\n')
    manifest=[]
    for f in sorted(D.iterdir()):
        if f.name=='delivery-manifest.json' or not f.is_file():continue
        manifest.append({'filename':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    save(D/'delivery-manifest.json',{'project_id':P.name,'excluded':['longform_mp4'],'files':manifest,'file_count_including_manifest':len(manifest)+1})
    print('Portable delivery files:',len(manifest)+1)
else:print('Publishing helpers created; Drive package waits for verified final MP4s and captions.')
