from __future__ import annotations

from bgm_review_page import render_selection_page

CANDIDATES = [
    {
        "id": "cand-01",
        "prompt": "낮은 드론과 <불협> 현악",
        "bgm_href": "../02_audio/bgm/candidates/cand-01.mp3",
        "preview_href": "../02_audio/bgm/previews/mix-01.mp3",
    },
    {
        "id": "cand-02",
        "prompt": "드론 중심",
        "bgm_href": "../02_audio/bgm/candidates/cand-02.mp3",
        "preview_href": "../02_audio/bgm/previews/mix-02.mp3",
    },
]


def test_page_lists_every_candidate():
    html = render_selection_page("2026-011-demo", CANDIDATES)
    assert "cand-01" in html
    assert "cand-02" in html


def test_page_embeds_both_players_per_candidate():
    html = render_selection_page("2026-011-demo", CANDIDATES)
    assert html.count("<audio") == 4


def test_page_escapes_prompt_markup():
    html = render_selection_page("2026-011-demo", CANDIDATES)
    assert "&lt;불협&gt;" in html
    assert "<불협>" not in html


def test_page_shows_apply_command():
    html = render_selection_page("2026-011-demo", CANDIDATES)
    assert "apply_bgm.py projects/2026-011-demo --candidate cand-01" in html


def test_page_is_standalone_html():
    html = render_selection_page("2026-011-demo", CANDIDATES)
    assert html.startswith("<!doctype html>")
    assert "http://" not in html and "https://" not in html
