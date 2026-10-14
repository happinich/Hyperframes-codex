"""Build frame-locked Hyperframes pages from the approved, timed scene plan."""
from __future__ import annotations

import html
import json
import math
from pathlib import Path
from scene_overlays import overlays_for_shot

P = Path(__file__).resolve().parent
C = P / "04_composition"
plan = json.loads((P / "01_script/scene-plan.json").read_text())
fps = 60
total = plan["end_screen_end_seconds"]
titles = {chapter["id"]: chapter["title"] for chapter in plan["chapters"]}


def frame(seconds: float) -> int:
    return round(seconds * fps)


def save(path: Path, value: str | object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + "\n")


shots = []
for scene in plan["scenes"]:
    a, b = frame(scene["start_seconds"]), frame(scene["end_seconds"])
    m = a + (b - a) // 2  # Legacy midpoint unused; actual word boundaries govern shots.
    for i, shot in enumerate(scene["shot_sequence"]):
        shots.append({
            "id": f"shot-{len(shots):03d}", "scene": scene["id"], "chapter": scene["chapter_id"],
            "asset": shot["asset_id"].lower(), "startFrame": frame(shot["start_seconds"]),
            "endFrame": frame(shot["end_seconds"]), "size": shot["shot_size"],
            "focus": shot["subject_focus"], "camera": shot["camera_position"],
        })
shots[-1]["endFrame"] = frame(total)

transitions = []
for earlier, later in zip(plan["chapters"], plan["chapters"][1:]):
    a, b = frame(earlier["end_seconds"]), frame(later["start_seconds"])
    transitions.append({"startFrame": a, "endFrame": b, "chapter": later["id"], "title": titles[later["id"]]})


def page(items: list[dict], duration_frames: int, offset_frames: int = 0, silent: bool = False) -> str:
    duration = duration_frames / fps
    sections = []
    diegetic_cues = []
    for item in items:
        start = max(0, item["startFrame"] - offset_frames) / fps
        end = min(duration_frames, item["endFrame"] - offset_frames) / fps
        clue, clue_cues = overlays_for_shot(item, offset_frames / fps, duration)
        diegetic_cues.extend(clue_cues)
        sections.append(
            f'<section id="{item["id"]}" class="shot {item["chapter"]}"><div class="view">'
            f'<img id="{item["id"]}-image" class="photo clip" src="assets/visuals/{item["asset"]}.png" '
            f'data-start="{start}" data-duration="{end-start}" alt="">{clue}</div>'
            '<div class="beam"></div><div class="vignette"></div></section>'
        )
    cards = []
    cues = list(diegetic_cues)
    for n, transition in enumerate(transitions, 2):
        a = transition["startFrame"] - offset_frames
        b = transition["endFrame"] - offset_frames
        if b <= 0 or a >= duration_frames:
            continue
        key = f"card-{n}"
        bg = f"{key}-background"
        asset = "c02-s02-a1" if transition["chapter"] == "C02" else "c03-s02-a1"
        cards.append(
            f'<div id="{bg}" class="chapter-backdrop"><img src="assets/visuals/{asset}.png" alt=""></div>'
            f'<div id="{key}" class="chapter-card"><small>{n}번째 이야기</small>'
            f'<strong>{html.escape(transition["title"])}</strong></div>'
        )
        start = max(0, a) / fps
        stop = min(duration_frames, b) / fps
        cues.append(
            f"tl.set('#{bg}',{{display:'block'}}, {start});"
            f"tl.fromTo('#{bg} img',{{scale:1.025,xPercent:-2}},"
            f"{{scale:1.13,xPercent:2,duration:{stop-start},ease:'none'}}, {start});"
            f"tl.set('#{key}',{{opacity:1}}, {start});"
            f"tl.set('#{key}',{{opacity:0}}, {stop});"
            f"tl.set('#{bg}',{{display:'none'}}, {stop});"
        )
    end = frame(plan["end_screen_start_seconds"]) - offset_frames
    if end < duration_frames:
        cues.append(f"tl.to('.end-safe',{{opacity:1,duration:.6}}, {max(0,end)/fps});")
        cues.append(f"tl.to('.end-label',{{opacity:1,duration:.4}}, {max(0,end)/fps});")
    local = [{**s, "start": max(0, s["startFrame"] - offset_frames) / fps,
              "end": min(duration_frames, s["endFrame"] - offset_frames) / fps}
             for s in items]
    card_motion_css = ('.chapter-backdrop{position:absolute;inset:0;display:none;overflow:hidden}'
                       '.chapter-backdrop img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
                       '.chapter-card{background:linear-gradient(90deg,#090e14d5,#090e1485)}') if cards else ''
    audio = '' if silent else f'<audio id="voice" src="assets/audio/voice.wav" data-start="0" data-duration="{duration}" data-track-index="0" data-volume="1"></audio>'
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{html.escape(plan['title'])}</title>
<style>@font-face{{font-family:"Apple SD Gothic Neo";src:local("Apple SD Gothic Neo")}}*{{box-sizing:border-box}}html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#101316;font-family:"Apple SD Gothic Neo",sans-serif}}#master{{position:relative;width:1920px;height:1080px;overflow:hidden}}.shot{{position:absolute;inset:0;display:none;overflow:hidden}}.view{{position:absolute;inset:0;overflow:hidden}}.photo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}.clue-layer{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}}.vignette{{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 52%,#03070888 100%)}}.beam{{position:absolute;inset:-8%;background:linear-gradient(110deg,transparent 34%,#d2b88814 49%,transparent 64%)}}.C02 .beam{{background:linear-gradient(105deg,transparent 34%,#b2d2df16 49%,transparent 64%)}}.C03 .beam{{background:linear-gradient(105deg,transparent 34%,#d4c8a016 49%,transparent 64%)}}.chapter-card{{position:absolute;inset:0;padding:380px 130px;color:#f0e7d4;background:linear-gradient(90deg,#090e14e8,#090e14c2);opacity:0}}.chapter-card small{{display:block;font-size:30px;letter-spacing:6px;color:#c6b894}}.chapter-card strong{{display:block;margin-top:30px;max-width:1500px;font-size:66px;line-height:1.25;word-break:keep-all}}.end-safe{{position:absolute;right:0;top:0;width:850px;height:1080px;background:linear-gradient(90deg,transparent,#0b1119ed);opacity:0}}.end-label{{position:absolute;left:72px;bottom:70px;color:#e8decc;font-size:31px;opacity:0}}{card_motion_css}</style></head><body>
<main id="master" data-composition-id="youtube-master" data-width="1920" data-height="1080" data-fps="60" data-start="0" data-duration="{duration}">{audio}{''.join(sections)}{''.join(cards)}<div class="end-safe"></div><div class="end-label">다음 공포 이야기는 관련 영상에서</div></main>
<script src="assets/gsap.min.js"></script><script>const SHOTS={json.dumps(local,ensure_ascii=False)};window.__timelines={{}};const tl=gsap.timeline({{paused:true}});
SHOTS.forEach((s,i)=>{{const e=document.getElementById(s.id),v=e.querySelector('.view'),beam=e.querySelector('.beam'),d=s.end-s.start,sign=i%2?1:-1;
tl.set(e,{{display:'block'}},s.start);const detail=s.size==='detail',high=s.camera.includes('high');tl.fromTo(v,{{scale:1.035,xPercent:detail?0:-sign*1.5,yPercent:high?-.8:-.25}},{{scale:detail?1.10:1.08,xPercent:detail?sign*.5:sign*1.5,yPercent:high?.8:.25,duration:d,ease:'none'}},s.start);
tl.fromTo(beam,{{xPercent:-sign*8,opacity:.18}},{{xPercent:sign*8,opacity:.42,duration:Math.min(2.6,d),repeat:Math.max(0,Math.floor(d/2.6)-1),yoyo:true,ease:'sine.inOut'}},s.start);
tl.set(e,{{display:'none'}},s.end);}});{''.join(cues)}tl.to({{}},{{duration:{duration}}},0);window.__timelines['youtube-master']=tl;tl.seek(.000001,false);if(SHOTS.length)gsap.set(document.getElementById(SHOTS[0].id),{{display:'block'}});</script></body></html>'''


save(C / "index.html", page(shots, frame(total)))
save(C / "scene-data.json", {"duration_seconds": total, "shots": shots, "transitions": transitions,
                             "burned_narration_captions": False, "fps": fps})
(C / "segments").mkdir(exist_ok=True)
if not (C / "segments/assets").exists():
    (C / "segments/assets").symlink_to("../assets")
segments = []
boundaries = sorted({0, frame(total)} | {frame(s["start_seconds"]) for s in plan["scenes"]} |
                    {frame(s["end_seconds"]) for s in plan["scenes"]} |
                    {t["startFrame"] for t in transitions} | {t["endFrame"] for t in transitions})
for i, (a, b) in enumerate(zip(boundaries, boundaries[1:]), 1):
    local = [s for s in shots if s["endFrame"] > a and s["startFrame"] < b]
    filename = f"segments/part-{i:02d}.html"
    save(C / filename, page(local, b-a, a, silent=True))
    segments.append({"filename": filename, "scene": local[0]["scene"] if local else "transition",
                     "startFrame": a, "endFrame": b, "duration": (b-a)/fps})
save(C / "render-segments.json", segments)
save(C / "production-manifest.json", {"status": "composition_prepared_pending_image_and_output_review",
                                          "fps": fps, "duration_seconds": total, "longform_camera_shots": len(shots),
                                          "segments": len(segments), "burned_longform_captions": False})
print(json.dumps({"shots": len(shots), "segments": len(segments), "duration": total}))
