import json
import sys

import pytest

import new_project


def test_new_project_uses_canonical_audio_defaults_without_preselected_bgm(tmp_path, monkeypatch):
    monkeypatch.setattr(new_project, "PROJECTS", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "new_project.py", "v4-default-test", "--title", "환경 검증",
        "--production-profile", "horror_cinematic_story_v1",
        "--visual-style", "horror_cinematic",
    ])
    assert new_project.main() == 0
    generated = json.loads((tmp_path / "v4-default-test/02_audio/elevenlabs-request.json").read_text())
    defaults = json.loads((new_project.ROOT / "config/success-rules.json").read_text())["audio_rules"]["elevenlabs"]
    assert generated["request"]["model_id"] == defaults["model_id"] == "eleven_v4"
    assert generated["request"]["voice_settings"] == defaults["voice_settings"]
    assert generated["request"]["context_stitching"] is True
    assert generated["bgm"]["source"] is None


@pytest.mark.parametrize("profile,style,editing_status", [
    ("horror_cinematic_story_v1", "horror_paper_stage", "pending_story_selection"),
    ("classic_rich_motion_v1", "adaptive_mix", "not_applicable"),
])
def test_project_scaffold_connects_editing_records_without_preselecting_effects(
    tmp_path, monkeypatch, profile, style, editing_status
):
    monkeypatch.setattr(new_project, "PROJECTS", tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "new_project.py", "editing-scaffold-test", "--title", "이야기별 편집 검증",
        "--production-profile", profile, "--visual-style", style,
    ])
    assert new_project.main() == 0
    project = tmp_path / "editing-scaffold-test"
    plan = json.loads((project / "01_script/editing-plan.json").read_text())
    scenes = json.loads((project / "01_script/scene-plan.json").read_text())
    assert plan["production_profile_id"] == scenes["style"]["production_profile_id"] == profile
    assert plan["visual_style_id"] == scenes["style"]["visual_style_id"] == style
    assert plan["status"] == editing_status
    assert plan["primary_technique_id"] is None
    assert plan["support_technique_ids"] == []
    assert plan["review"]["rendered_output"] == "pending"
    assert (project / plan["review"]["record_path"]).is_file()
    assert (project / plan["longform"]["scene_plan_path"]).is_file()
    assert (new_project.ROOT / plan["catalog"]).is_file()
    assert scenes["scenes"][0]["editing"]["technique_ids"] == []
    for relative in (
        "00_brief/brief.md", "01_script/editing-plan.json", "01_script/scene-plan.json",
        "01_script/production-notes.md", "05_review/editing-review.md", "05_review/checklist.md",
    ):
        path = project / relative
        assert "{{" not in path.read_text(), path
