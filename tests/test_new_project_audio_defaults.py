import json
import sys

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
