#!/usr/bin/env python3
"""Render the static BGM candidate comparison page."""

from __future__ import annotations

from html import escape

PAGE_STYLE = """
  body { margin: 0; padding: 40px; background: #0b0e15; color: #f5f7ff;
         font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
  h1 { font-size: 22px; margin: 0 0 6px; }
  p.lead { color: #a4aec8; margin: 0 0 32px; font-size: 14px; }
  .card { border: 1px solid #1e2740; border-radius: 10px; padding: 20px;
          margin-bottom: 20px; background: #111726; }
  .card h2 { font-size: 16px; margin: 0 0 10px; }
  .prompt { color: #a4aec8; font-size: 13px; line-height: 1.6; margin: 0 0 16px; }
  .row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
  .row span { width: 130px; font-size: 13px; color: #8e9ab8; }
  audio { flex: 1; }
  code { display: block; background: #05070d; border: 1px solid #1e2740;
         border-radius: 6px; padding: 10px 12px; font-size: 12px;
         color: #7ee3c3; margin-top: 12px; overflow-x: auto; }
"""


def render_selection_page(project_name: str, candidates: list) -> str:
    cards = []
    for candidate in candidates:
        candidate_id = escape(str(candidate["id"]))
        cards.append(
            f"""    <div class="card">
      <h2>{candidate_id}</h2>
      <p class="prompt">{escape(str(candidate["prompt"]))}</p>
      <div class="row"><span>BGM 단독</span>
        <audio controls preload="none" src="{escape(str(candidate["bgm_href"]))}"></audio>
      </div>
      <div class="row"><span>내레이션 믹스</span>
        <audio controls preload="none" src="{escape(str(candidate["preview_href"]))}"></audio>
      </div>
      <code>python3 scripts/apply_bgm.py projects/{escape(project_name)} --candidate {candidate_id}</code>
    </div>"""
        )
    body = "\n".join(cards)
    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BGM 후보 선택 - {escape(project_name)}</title>
    <style>{PAGE_STYLE}</style>
  </head>
  <body>
    <h1>BGM 후보 선택</h1>
    <p class="lead">{escape(project_name)} · 내레이션 믹스는 실제 더킹 값으로 만들어졌습니다. 하나를 고른 뒤 아래 명령을 실행하세요.</p>
{body}
  </body>
</html>
"""
