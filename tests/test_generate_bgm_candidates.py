from __future__ import annotations

from pathlib import Path

import pytest

from generate_bgm_candidates import build_candidate_specs, default_content_hint

PRESET = {
    "base_prompt": "낮은 드론.",
    "variation_hints": ["현악 중심", "드론 중심", "금속성 울림", "피아노 단음"],
}


def test_build_candidate_specs_numbers_ids_from_one():
    specs = build_candidate_specs(PRESET, 3, "겨울 산속 펜션 괴담.")
    assert [s["id"] for s in specs] == ["cand-01", "cand-02", "cand-03"]


def test_build_candidate_specs_uses_distinct_variations():
    specs = build_candidate_specs(PRESET, 4, "")
    prompts = [s["prompt"] for s in specs]
    assert len(set(prompts)) == 4


def test_build_candidate_specs_includes_all_three_parts():
    spec = build_candidate_specs(PRESET, 1, "겨울 산속 펜션 괴담.")[0]
    assert "낮은 드론." in spec["prompt"]
    assert "현악 중심" in spec["prompt"]
    assert "겨울 산속 펜션 괴담." in spec["prompt"]


def test_build_candidate_specs_rejects_count_above_hints():
    with pytest.raises(ValueError) as excinfo:
        build_candidate_specs(PRESET, 5, "")
    assert "4" in str(excinfo.value)


def test_default_content_hint_reads_first_paragraph(tmp_path: Path):
    brief = tmp_path / "brief.md"
    brief.write_text(
        "# 제목\n\n첫 문단입니다. 계속됩니다.\n\n두 번째 문단.\n", encoding="utf-8"
    )
    assert default_content_hint(brief) == "첫 문단입니다. 계속됩니다."


def test_default_content_hint_returns_empty_when_missing(tmp_path: Path):
    assert default_content_hint(tmp_path / "nope.md") == ""
