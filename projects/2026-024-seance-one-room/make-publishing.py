"""Build the two local publishing helpers from the timed project plan."""
from __future__ import annotations

import html
import json
from pathlib import Path

P = Path(__file__).resolve().parent
OUT = P / "07_publish"
plan = json.loads((P / "01_script/scene-plan.json").read_text(encoding="utf-8"))


def stamp(seconds: float) -> str:
    whole = round(seconds)
    return f"{whole // 60:02d}:{whole % 60:02d}"


main_title = "강령술 놀이를 한 원룸, 수저가 네 벌 왔어요 | 창작 공포"
timeline = [
    ("s01", "셋인데 들린 넷째 목소리"),
    ("s02", "친구 셋이 모인 금요일"),
    ("s04", "수저 네 벌"),
    ("s06", "손님 세기 놀이"),
    ("s09", "꺼진 방의 소리"),
    ("s11", "귀 바로 옆의 숫자"),
    ("s14", "친구들이 떠난 뒤"),
    ("s16", "밤마다 울린 도어락"),
    ("s18", "편의점 직원의 질문"),
    ("s20", "은채의 전화"),
    ("s23", "카메라에만 보인 것"),
    ("s25", "다섯 번째 소리"),
]
lookup = {scene["id"]: scene for scene in plan["scenes"]}
timestamps = "\n".join(f"{stamp(lookup[sid]['start_seconds'])} {label}" for sid, label in timeline)
description = f"""원룸에 있던 사람은 셋이었어요. 그런데 배달 봉투에는 수저가 네 벌 들어 있었습니다. 자정이 넘은 뒤, 친구가 꺼낸 '손님 세기' 놀이에서 누군가 넷을 셌어요.

한 사람의 시점으로 들려주는 완결형 창작 공포 이야기입니다.

타임스탬프
{timestamps}

작품 안내
이 이야기는 창작 허구입니다. 실제 인물이나 사건을 재현하지 않았습니다. AI 생성 이미지와 음성, 생성 BGM을 활용했습니다. 외부 사실 자료를 인용하지 않았습니다.

마지막 화면의 관련 공포 이야기 또는 재생목록에서 다음 이야기를 이어 보세요.

#무서운이야기 #원룸괴담 #공포괴담 #창작공포 #강령술"""
main = {
    "메인 제목": main_title,
    "추천 제목 5가지": "\n".join(f"{i}. {title}" for i, title in enumerate([
        "원룸에 셋이 있었는데 도어락은 네 번 울렸어요",
        "수저가 한 벌 더 온 밤, 제 귀에서 누가 숫자를 셌어요",
        "강령술 장난을 치고 나서 돌아온 여분 수저",
        "그날 원룸에서 눈을 뜨면 안 됐어요",
        "셋이 시작한 놀이가 끝나지 않은 이유",
    ], 1)),
    "설명란": description,
    "태그": "무서운이야기,원룸괴담,공포괴담,창작공포,귀신이야기,강령술,손님세기,넷째목소리,도어락괴담,한국괴담,공포라디오,오디오드라마",
    "고정 댓글": "네 번째 수저, 귀 옆의 목소리, 도어락 네 번 중 언제부터 누군가 원룸에 있다고 느끼셨나요? ※ 창작 공포 이야기입니다.",
    "X 홍보문": "우리 셋이 모인 원룸에 수저가 네 벌 왔어요. 자정이 지나자 귀 바로 옆에서 누가 '넷'이라고 셌습니다. 창작 공포 〈강령술 원룸〉 [본편 공개 URL 입력] #공포괴담 #무서운이야기",
    "Threads 홍보문": "대학 친구 셋이 제 원룸에 모였어요. 배달 수저는 네 벌이었고, 그날 밤 우리는 눈을 감고 사람 수를 세기 시작했습니다. 본편 공개 후: [URL 입력]",
    "Instagram 홍보문": "셋이었는데 넷째 목소리가 들렸어요. 원룸에서 시작된 창작 공포 〈강령술 원룸〉. 본편은 프로필의 유튜브 링크에서. #무서운이야기 #원룸괴담 #공포괴담",
    "업로드 체크": "1920×1080 / 60fps 클린 MP4\nSRT 또는 VTT 별도 업로드\n창작 허구 및 AI 이미지·음성·BGM 활용 표기\n마지막 18초에 관련 영상 또는 재생목록 엔드스크린 지정\n쇼츠 공개 후 Related Video에 이 본편 지정",
    "추천 게시 시간": "초기 실험: 한국 시간 오후 10시 본편, 다음 날 오후 8시 30분 쇼츠. 채널의 시청자 활동 데이터로 조정할 가설입니다. 업로드·예약은 아직 실행하지 않았습니다.",
}
short_title = "셋이 눈을 감았는데, 넷째 목소리가 들렸어요 #공포괴담"
shorts = {
    "쇼츠 제목": short_title,
    "설명란": "사람은 셋. 그런데 귀 옆에서 누군가 '넷'을 셌어요. 손목을 잡은 차가운 손은 누구의 것이었을까요?\n\n아래 관련 동영상에서 완결된 창작 공포 이야기를 보세요. 별도 대본·음성·세로 이미지로 제작했고 AI 생성 이미지·음성·BGM을 활용했습니다.\n\n#쇼츠 #무서운이야기 #원룸괴담 #공포괴담",
    "태그": "공포쇼츠,원룸괴담,넷째목소리,도어락괴담,무서운이야기,창작공포",
    "고정 댓글": "그날 밤 원룸에 있던 넷째는 누구였을까요? 아래 관련 동영상에서 본편을 이어 보세요.",
    "본편 연결": f"YouTube Studio → 쇼츠 → 관련 동영상(Related Video)\n정확한 대상: {main_title}\n프로젝트: {P.name}\n본편 공개 후 해당 영상으로 지정하세요. 설명란 URL만으로 연결하지 않습니다.",
    "추천 게시 시간": "초기 실험: 본편 공개 다음 날 한국 시간 오후 8시 30분. 채널 데이터로 조정할 가설입니다. 업로드·예약은 아직 실행하지 않았습니다.",
}


def markdown(title: str, blocks: dict[str, str]) -> str:
    return "# " + title + "\n\n" + "\n\n".join(f"## {key}\n\n{value}" for key, value in blocks.items()) + "\n"


def helper(title: str, blocks: dict[str, str], *, short: bool) -> str:
    videos = (f"../../06_delivery/shorts/{P.name}-shorts.mp4" if short else f"../../06_delivery/youtube/{P.name}-youtube.mp4")
    srt = "../../03_sync/shorts-captions.srt" if short else "../../03_sync/captions.srt"
    vtt = "../../03_sync/shorts-captions.vtt" if short else "../../03_sync/captions.vtt"
    previews = "" if short else '<div class="thumbs"><a href="thumbnail-a.png"><img src="thumbnail-a.png" alt="넷째 목소리 썸네일"></a><a href="thumbnail-b.png"><img src="thumbnail-b.png" alt="천장의 네 손 썸네일"></a></div>'
    sections = "".join(f'<section><div class="row"><h2>{html.escape(key)}</h2><button data-copy="b{i}">복사</button></div><pre id="b{i}">{html.escape(value)}</pre></section>' for i, (key, value) in enumerate(blocks.items()))
    all_text = "\n\n".join(f"{key}\n{value}" for key, value in blocks.items())
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#0b151c;color:#edf4f5;font-family:system-ui,sans-serif;line-height:1.7}}main{{max-width:1000px;margin:auto;padding:32px 22px 70px}}header,section{{padding:24px;border:1px solid #37505b;border-radius:16px;margin:18px 0;background:#162832}}header{{background:linear-gradient(120deg,#18313c,#382b2b)}}h1{{font-size:30px}}h2{{font-size:20px;margin:0}}.row{{display:flex;align-items:center;justify-content:space-between;gap:12px}}button,a.link{{display:inline-block;background:#254b59;border:1px solid #57808e;color:#fff;border-radius:10px;padding:10px 15px;margin:5px 5px 5px 0;text-decoration:none;cursor:pointer;font-size:15px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}}video{{width:100%;max-height:570px;background:#05090b}}.thumbs{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}.thumbs img{{width:100%;border-radius:9px}}small,p{{color:#bfd0d8}}#status{{display:none;position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#e9fff6;color:#173425;padding:10px 20px;border-radius:10px}}@media(max-width:600px){{main{{padding:15px 12px}}header,section{{padding:17px}}.thumbs{{grid-template-columns:1fr}}}}
</style></head><body><main><header><small>창작 공포 · 강령술 원룸</small><h1>{html.escape(title)}</h1><button id="copy-all">게시 내용 전체 복사</button></header><section><h2>영상과 자막</h2><video controls preload="metadata" src="{videos}"></video><a class="link" href="{videos}">영상 파일</a><a class="link" href="{srt}">SRT 자막</a><a class="link" href="{vtt}">VTT 자막</a>{previews}</section>{sections}<p>업로드와 예약은 실행하지 않았습니다.</p></main><div id="status" role="status"></div><script>
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
