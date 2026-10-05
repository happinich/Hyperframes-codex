"""Build local publishing helpers from actual voice timings; no uploads."""
import html,json
from pathlib import Path
P=Path(__file__).resolve().parent;OUT=P/'07_publish'
plan=json.loads((P/'01_script/scene-plan.json').read_text());lookup={s['id']:s for s in plan['scenes']}
def stamp(t):
 w=int(t);return f"{w//60:02d}:{w%60:02d}"
main_title="문 닫은 키즈카페, 볼풀에서 공이 하나씩 돌아왔다 | 창작 공포"
timeline=[('s01','볼풀에서 나온 것'),('s05','돌아온 빨간 공'),('s08','볼풀을 걷어 봤다'),('s11','파란 매트 아래'),('s15','소리를 따라 움직이는 몸'),('s18','손등에 닿은 것'),('s22','열린 직원실 문'),('s25','계단 밖으로'),('s29','철거 뒤의 청소 영상'),('s31','복도에서 들린 소리')]
timestamps='\n'.join(f"{stamp(lookup[s]['start_seconds'])} {t}" for s,t in timeline)
description=f"""아무도 없는 키즈카페에서 마감을 끝냈어요. 볼풀 안에 던진 빨간 공이 제 발앞으로 돌아왔습니다. 공을 걷어 보니, 파란 매트가 아래에서 부풀고 있었어요.

혼자 맡은 야간 마감에서 시작되는 완결형 창작 공포 이야기입니다.

타임스탬프
{timestamps}

작품 안내
이 이야기는 창작 허구이며 실화·제보·검증된 사건이 아닙니다. 실제 인물이나 특정 매장을 재현하지 않았습니다. AI 생성 이미지·음성·BGM과 자체 제작 공간음·효과음을 사용했습니다. 외부 사실 자료를 인용하지 않았습니다.

마지막 화면의 관련 공포 이야기 또는 재생목록에서 다음 이야기를 이어 보세요.

#무서운이야기 #키즈카페괴담 #볼풀괴담 #창작공포 #공포라디오"""
main={
 '메인 제목':main_title,
 '추천 제목 5가지':'\n'.join(f'{i}. {x}' for i,x in enumerate(['마감이 끝난 볼풀에서 누가 공을 던졌어요','빈 키즈카페의 매트 아래에는 아이가 없었어요','쓰레기통에 넣은 빨간 공이 다시 돌아왔어요','혼자 마감한 날, 테이블이 입구를 막았습니다','키즈카페를 철거한 뒤에도 남아 있던 빨간 공'],1)),
 '설명란':description,
 '태그':'무서운이야기,키즈카페괴담,볼풀괴담,창작공포,괴물괴담,야간마감,빨간공,한국괴담,공포라디오,오디오드라마,무서운썰',
 '고정 댓글':'빨간 공이 돌아온 순간, 매트가 부푼 순간, 테이블이 움직인 순간 중 언제부터 위험하다고 느끼셨나요? ※ 창작 공포 이야기입니다.',
 'SNS 홍보문':'아무도 없는 키즈카페. 볼풀에 던진 공이 제 발앞으로 돌아왔어요. 아이를 찾으려고 공을 걷었는데, 파란 매트가 부풀기 시작했습니다. 완결형 창작 공포 [본편 공개 URL 입력] #키즈카페괴담 #무서운이야기',
 '추천 게시 시간':'초기 운영 가설: 수요일 또는 일요일 한국 시간 22:00 본편, 다음 날 20:30 쇼츠. 채널 시청자 활동 데이터로 조정하세요. 업로드·예약은 실행하지 않았습니다.',
 '썸네일':'A: 누가 던졌지 / 누군가 던진 빨간 공\nB: 아이 아니야 / 테이블을 감은 몸의 일부',
 '업로드 체크':'1920×1080 60fps 클린 MP4\nSRT 또는 VTT 별도 업로드; 본편 번인 자막 없음\n창작 허구 및 AI 이미지·음성·BGM 활용 표기\n마지막 18초에 채널의 창작 공포 재생목록을 엔드스크린으로 지정\n쇼츠 공개 후 Related Video에 이 본편 지정',
 '엔드스크린 대상':'채널의 창작 공포 이야기 재생목록. 공개 URL을 확인하지 못했으므로 주소를 만들어 넣지 않았습니다. 업로드 시 채널의 실제 재생목록을 선택하세요.',
}
short_title='아무도 없는 볼풀에서 공이 날아왔어요 #공포괴담'
shorts={
 '쇼츠 제목':short_title,
 '설명란':'빨간 공이 발앞으로 돌아왔어요. 공을 전부 걷어 봤는데 아이는 없었습니다. 그런데 파란 매트가 부풀기 시작했어요.\n\n아래 관련 동영상에서 완결된 창작 공포 이야기를 보세요. 독립 대본·음성·새 세로 이미지로 제작했고 AI 이미지·음성·BGM을 사용했습니다.\n\n#쇼츠 #무서운이야기 #키즈카페괴담 #볼풀괴담',
 '태그':'공포쇼츠,키즈카페괴담,볼풀괴담,빨간공,창작공포,무서운이야기',
 '고정 댓글':'볼풀 아래에는 무엇이 있었을까요? 아래 관련 동영상에서 본편을 이어 보세요.',
 '본편 연결':f'YouTube Studio → 쇼츠 → 관련 동영상(Related Video)\n정확한 대상: {main_title}\n프로젝트: {P.name}\n본편 공개 후 해당 영상으로 지정하세요. 설명란 URL만으로 연결하지 않습니다.',
 '추천 게시 시간':'본편 공개 다음 날 한국 시간 20:30부터 실험하고 채널 시청자 데이터로 조정. 업로드·예약은 실행하지 않았습니다.',
}

def markdown(title: str, blocks: dict[str, str]) -> str:
    return "# " + title + "\n\n" + "\n\n".join(f"## {key}\n\n{value}" for key, value in blocks.items()) + "\n"


def helper(title: str, blocks: dict[str, str], *, short: bool) -> str:
    videos = (f"../../06_delivery/shorts/{P.name}-shorts.mp4" if short else f"../../06_delivery/youtube/{P.name}-youtube.mp4")
    srt = "../../03_sync/shorts-captions.srt" if short else "../../03_sync/captions.srt"
    vtt = "../../03_sync/shorts-captions.vtt" if short else "../../03_sync/captions.vtt"
    previews = "" if short else '<div class="thumbs"><a href="thumbnail-a.png"><img src="thumbnail-a.png" alt="돌아오는 공 썸네일"></a><a href="thumbnail-b.png"><img src="thumbnail-b.png" alt="테이블을 감은 몸 썸네일"></a></div>'
    sections = "".join(f'<section><div class="row"><h2>{html.escape(key)}</h2><button data-copy="b{i}">복사</button></div><pre id="b{i}">{html.escape(value)}</pre></section>' for i, (key, value) in enumerate(blocks.items()))
    all_text = "\n\n".join(f"{key}\n{value}" for key, value in blocks.items())
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#0b151c;color:#edf4f5;font-family:system-ui,sans-serif;line-height:1.7}}main{{max-width:1000px;margin:auto;padding:32px 22px 70px}}header,section{{padding:24px;border:1px solid #37505b;border-radius:16px;margin:18px 0;background:#162832}}header{{background:linear-gradient(120deg,#18313c,#382b2b)}}h1{{font-size:30px}}h2{{font-size:20px;margin:0}}.row{{display:flex;align-items:center;justify-content:space-between;gap:12px}}button,a.link{{display:inline-block;background:#254b59;border:1px solid #57808e;color:#fff;border-radius:10px;padding:10px 15px;margin:5px 5px 5px 0;text-decoration:none;cursor:pointer;font-size:15px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}}video{{width:100%;max-height:570px;background:#05090b}}.thumbs{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}.thumbs img{{width:100%;border-radius:9px}}small,p{{color:#bfd0d8}}#status{{display:none;position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#e9fff6;color:#173425;padding:10px 20px;border-radius:10px}}@media(max-width:600px){{main{{padding:15px 12px}}header,section{{padding:17px}}.thumbs{{grid-template-columns:1fr}}}}
</style></head><body><main><header><small>창작 공포 · 키즈카페 마감</small><h1>{html.escape(title)}</h1><button id="copy-all">게시 내용 전체 복사</button></header><section><h2>영상과 자막</h2><video controls preload="metadata" src="{videos}"></video><a class="link" href="{videos}">영상 파일</a><a class="link" href="{srt}">SRT 자막</a><a class="link" href="{vtt}">VTT 자막</a>{previews}</section>{sections}<p>업로드와 예약은 실행하지 않았습니다.</p></main><div id="status" role="status"></div><script>
const ALL={json.dumps(all_text,ensure_ascii=False)};async function copyText(t){{let ok=false;try{{await navigator.clipboard.writeText(t);ok=true}}catch{{}}if(!ok){{const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.left='-9999px';document.body.append(a);a.select();ok=document.execCommand('copy');a.remove()}}const s=document.getElementById('status');s.textContent=ok?'복사했습니다':'선택하여 복사해 주세요.';s.style.display='block';setTimeout(()=>s.style.display='none',2400)}}document.getElementById('copy-all').onclick=()=>copyText(ALL);document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>copyText(document.getElementById(b.dataset.copy).textContent));</script></body></html>'''



for folder, title, data, short in [
    (OUT / "youtube", "유튜브 게시 도우미", main, False),
    (OUT / "shorts", "쇼츠 게시 도우미", shorts, True),
]:
    folder.mkdir(parents=True, exist_ok=True)
    prefix = "shorts" if short else "youtube"
    (folder / f"{prefix}-publish.md").write_text(markdown(title, data), encoding="utf-8")
    (folder / f"{prefix}-publish.html").write_text(helper(title, data, short=short), encoding="utf-8")

(OUT / "publish-data.json").write_text(json.dumps({"main_title": main_title, "short_title": short_title, "fiction": True, "related_video_target": main_title, "main": main, "shorts": shorts}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Wrote YouTube and Shorts publishing helpers")
