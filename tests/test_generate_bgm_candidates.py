from __future__ import annotations

from pathlib import Path

import pytest

from generate_bgm_candidates import build_candidate_specs, default_content_hint


@pytest.fixture
def minimal_bgm_project(tmp_path: Path, monkeypatch):
    """
    Fixture that creates a minimal project structure with config files
    needed for BGM candidate generation testing.

    Returns a dict with:
      - project: Path to the project directory
      - success_rules_path: Path to success-rules.json
      - presets_path: Path to bgm-presets.json
    """
    import json

    project = tmp_path / "test_project"
    project.mkdir()
    (project / "00_brief").mkdir()
    (project / "02_audio").mkdir()
    (project / "02_audio" / "bgm").mkdir()
    (project / "02_audio" / "bgm" / "candidates").mkdir()
    (project / "02_audio" / "bgm" / "previews").mkdir()
    (project / "04_composition").mkdir()
    (project / "05_review").mkdir()

    # Create profile.json
    profile_data = {"visual_style_id": "minimal_dark_tech"}
    (project / "04_composition" / "profile.json").write_text(
        json.dumps(profile_data), encoding="utf-8"
    )

    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key")

    # Create success-rules.json
    success_rules_path = tmp_path / "success-rules.json"
    success_rules_data = {
        "audio_rules": {
            "bgm": {
                "voice_ducking_gain_db": -6.0,
                "outro_gain_db": -20.0,
                "fade_out_seconds": 2.0,
            }
        }
    }
    success_rules_path.write_text(json.dumps(success_rules_data), encoding="utf-8")

    # Create bgm-presets.json
    presets_path = tmp_path / "bgm-presets.json"
    presets_data = {
        "defaults": {
            "candidate_count": 2,
            "candidate_length_ms": 30000,
            "preview_seconds": 10,
        },
        "styles": {
            "minimal_dark_tech": {
                "base_prompt": "minimal electronic",
                "variation_hints": ["variation 1", "variation 2"],
            }
        },
    }
    presets_path.write_text(json.dumps(presets_data), encoding="utf-8")

    return {
        "project": project,
        "success_rules_path": success_rules_path,
        "presets_path": presets_path,
    }

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


def test_request_music_bytes_empty_response_raises_error(monkeypatch):
    """Test that empty response body from API is treated as a failure."""
    from unittest.mock import Mock, patch
    import generate_bgm_candidates

    mock_response = Mock()
    mock_response.read.return_value = b""
    mock_response.__enter__ = Mock(return_value=mock_response)
    mock_response.__exit__ = Mock(return_value=None)

    with patch("urllib.request.urlopen", return_value=mock_response):
        with pytest.raises(ValueError, match="empty response"):
            generate_bgm_candidates.request_music_bytes(
                api_key="test",
                prompt="test",
                length_ms=30000,
                output_format="mp3_44100_128",
            )


def test_candidate_processing_loop_handles_partial_failures(
    tmp_path: Path, monkeypatch, capsys
):
    """
    Test that when one candidate fails during API request processing,
    the loop continues and reports the partial success correctly.
    """
    from unittest.mock import patch
    import json
    import generate_bgm_candidates

    # Set up minimal project structure
    project = tmp_path / "test_project"
    project.mkdir()
    (project / "00_brief").mkdir()
    (project / "02_audio").mkdir()
    (project / "02_audio" / "bgm").mkdir()
    (project / "02_audio" / "bgm" / "candidates").mkdir()
    (project / "02_audio" / "bgm" / "previews").mkdir()
    (project / "04_composition").mkdir()
    (project / "05_review").mkdir()

    # Create profile.json
    profile_data = {"visual_style_id": "minimal_dark_tech"}
    (project / "04_composition" / "profile.json").write_text(
        json.dumps(profile_data), encoding="utf-8"
    )

    # Set required environment variable
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key-123")

    # Create minimal success-rules.json
    success_rules_path = tmp_path / "success-rules.json"
    success_rules_data = {
        "audio_rules": {
            "bgm": {
                "voice_ducking_gain_db": -6.0,
                "outro_gain_db": -20.0,
                "fade_out_seconds": 2.0,
            }
        }
    }
    success_rules_path.write_text(json.dumps(success_rules_data), encoding="utf-8")

    # Create bgm-presets.json
    presets_path = tmp_path / "bgm-presets.json"
    presets_data = {
        "defaults": {
            "candidate_count": 2,
            "candidate_length_ms": 30000,
            "preview_seconds": 10,
        },
        "styles": {
            "minimal_dark_tech": {
                "base_prompt": "minimal electronic",
                "variation_hints": ["variation 1", "variation 2"],
            }
        },
    }
    presets_path.write_text(json.dumps(presets_data), encoding="utf-8")

    # Mock the file paths to use our test files
    with patch.object(
        generate_bgm_candidates, "SUCCESS_RULES_PATH", success_rules_path
    ), patch.object(
        generate_bgm_candidates, "PRESETS_PATH", presets_path
    ), patch.object(
        generate_bgm_candidates, "request_music_bytes"
    ) as mock_request:

        # First candidate: API call fails
        # Second candidate: API call succeeds
        call_count = [0]

        def request_impl(**kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # First candidate fails during API call
                raise OSError("Permission denied writing candidate")
            return b"fake mp3 audio data"

        mock_request.side_effect = request_impl

        import sys

        old_argv = sys.argv
        try:
            sys.argv = [
                "generate_bgm_candidates.py",
                str(project),
                "--count",
                "2",
            ]
            result = generate_bgm_candidates.main()
        finally:
            sys.argv = old_argv

        # Verify: run should succeed (return 0) because we have 1 success
        assert result == 0, f"Expected exit code 0, got {result}"

        # Verify: only the second candidate file should exist
        candidates_dir = project / "02_audio" / "bgm" / "candidates"
        assert not (candidates_dir / "cand-01.mp3").exists()
        assert (candidates_dir / "cand-02.mp3").exists()

        # Verify: candidates.json should contain only the successful candidate
        candidates_json_path = project / "02_audio" / "bgm" / "candidates.json"
        assert candidates_json_path.exists()
        candidates_data = json.loads(candidates_json_path.read_text(encoding="utf-8"))
        assert len(candidates_data["candidates"]) == 1
        assert candidates_data["candidates"][0]["id"] == "cand-02"

        # Verify: output shows failure message for cand-01
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert "cand-01" in captured.out
        assert "Generated" in captured.out
        assert "1 failed" in captured.out


def test_all_candidates_fail_exits_nonzero(
    tmp_path: Path, monkeypatch, capsys
):
    """
    Test that when all candidates fail, the run exits with code 1
    and reports all failures.
    """
    from unittest.mock import patch
    import json
    import generate_bgm_candidates

    # Set up minimal project structure
    project = tmp_path / "test_project_all_fail"
    project.mkdir()
    (project / "00_brief").mkdir()
    (project / "02_audio").mkdir()
    (project / "02_audio" / "bgm").mkdir()
    (project / "02_audio" / "bgm" / "candidates").mkdir()
    (project / "02_audio" / "bgm" / "previews").mkdir()
    (project / "04_composition").mkdir()
    (project / "05_review").mkdir()

    # Create profile.json
    profile_data = {"visual_style_id": "minimal_dark_tech"}
    (project / "04_composition" / "profile.json").write_text(
        json.dumps(profile_data), encoding="utf-8"
    )

    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key")

    # Create success-rules.json
    success_rules_path = tmp_path / "success-rules.json"
    success_rules_data = {
        "audio_rules": {
            "bgm": {
                "voice_ducking_gain_db": -6.0,
                "outro_gain_db": -20.0,
                "fade_out_seconds": 2.0,
            }
        }
    }
    success_rules_path.write_text(json.dumps(success_rules_data), encoding="utf-8")

    # Create bgm-presets.json
    presets_path = tmp_path / "bgm-presets.json"
    presets_data = {
        "defaults": {
            "candidate_count": 2,
            "candidate_length_ms": 30000,
            "preview_seconds": 10,
        },
        "styles": {
            "minimal_dark_tech": {
                "base_prompt": "minimal electronic",
                "variation_hints": ["variation 1", "variation 2"],
            }
        },
    }
    presets_path.write_text(json.dumps(presets_data), encoding="utf-8")

    with patch.object(
        generate_bgm_candidates, "SUCCESS_RULES_PATH", success_rules_path
    ), patch.object(
        generate_bgm_candidates, "PRESETS_PATH", presets_path
    ), patch.object(
        generate_bgm_candidates, "request_music_bytes"
    ) as mock_request:

        # Make all requests fail
        mock_request.side_effect = ValueError("API failure")

        import sys

        old_argv = sys.argv
        try:
            sys.argv = [
                "generate_bgm_candidates.py",
                str(project),
                "--count",
                "2",
            ]
            result = generate_bgm_candidates.main()
        finally:
            sys.argv = old_argv

        # Verify: exit code should be 1
        assert result == 1, f"Expected exit code 1 when all fail, got {result}"

        # Verify: output should report all failures
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert "All 2 candidate(s) failed" in captured.out


def test_subprocess_error_caught_in_preview_mix(
    minimal_bgm_project, capsys
):
    """
    Test that subprocess.CalledProcessError during preview mix is caught
    and counted as a failure, allowing the run to continue.
    """
    from unittest.mock import patch, MagicMock
    import json
    import subprocess
    import generate_bgm_candidates

    project = minimal_bgm_project["project"]
    success_rules_path = minimal_bgm_project["success_rules_path"]
    presets_path = minimal_bgm_project["presets_path"]

    # Create a fake voice file
    voice_file = project / "02_audio" / "working" / "voice.wav"
    voice_file.parent.mkdir(parents=True, exist_ok=True)
    voice_file.write_bytes(b"fake wav data")

    with patch.object(
        generate_bgm_candidates, "SUCCESS_RULES_PATH", success_rules_path
    ), patch.object(
        generate_bgm_candidates, "PRESETS_PATH", presets_path
    ), patch.object(
        generate_bgm_candidates, "request_music_bytes"
    ) as mock_request, patch.object(
        generate_bgm_candidates, "mix_bgm_with_voice"
    ) as mock_mix, patch.object(
        generate_bgm_candidates, "audio_duration_seconds", return_value=60.0
    ), patch.object(
        generate_bgm_candidates, "slice_narration"
    ):

        call_count = [0]

        def request_impl(**kwargs):
            call_count[0] += 1
            return b"fake mp3 audio data"

        mock_request.side_effect = request_impl

        # First candidate: mix_bgm_with_voice raises CalledProcessError (ffmpeg fails)
        # Second candidate: succeeds
        def mix_impl(*args, **kwargs):
            if call_count[0] == 1:
                # Simulate ffmpeg failure during preview mix
                proc_error = subprocess.CalledProcessError(1, "ffmpeg")
                raise proc_error
            # Second candidate succeeds (no exception)

        mock_mix.side_effect = mix_impl

        import sys

        old_argv = sys.argv
        try:
            sys.argv = [
                "generate_bgm_candidates.py",
                str(project),
                "--count",
                "2",
            ]
            result = generate_bgm_candidates.main()
        finally:
            sys.argv = old_argv

        # Verify: run should succeed because second candidate succeeded
        assert result == 0, f"Expected exit code 0, got {result}"

        # Verify: both candidate files should exist (API call succeeded for both)
        candidates_dir = project / "02_audio" / "bgm" / "candidates"
        assert (candidates_dir / "cand-01.mp3").exists()
        assert (candidates_dir / "cand-02.mp3").exists()

        # Verify: candidates.json has only the successful candidate
        # (cand-01's preview mix failed, so it's not rendered)
        candidates_json_path = project / "02_audio" / "bgm" / "candidates.json"
        candidates_data = json.loads(candidates_json_path.read_text(encoding="utf-8"))
        # Both candidates should be in candidates.json if the mix failure was caught
        # Actually, if mix fails, it should not be added to rendered list
        assert len(candidates_data["candidates"]) == 1
        assert candidates_data["candidates"][0]["id"] == "cand-02"

        # Verify: output shows failure message for cand-01 during mix
        captured = capsys.readouterr()
        assert "FAILED" in captured.out
        assert "cand-01" in captured.out


def test_programming_error_propagates_out(
    minimal_bgm_project
):
    """
    Test that programming errors (TypeError) in dependencies propagate out
    rather than being silently caught, so bugs are surfaced.
    """
    from unittest.mock import patch
    import generate_bgm_candidates

    project = minimal_bgm_project["project"]
    success_rules_path = minimal_bgm_project["success_rules_path"]
    presets_path = minimal_bgm_project["presets_path"]

    with patch.object(
        generate_bgm_candidates, "SUCCESS_RULES_PATH", success_rules_path
    ), patch.object(
        generate_bgm_candidates, "PRESETS_PATH", presets_path
    ), patch.object(
        generate_bgm_candidates, "request_music_bytes"
    ) as mock_request:

        # Simulate a programming error: TypeError from a monkeypatched dependency
        def request_impl(**kwargs):
            # Simulate a bug in the code: passing wrong type
            raise TypeError(
                "unsupported operand type(s) for +: 'int' and 'str'"
            )

        mock_request.side_effect = request_impl

        import sys

        old_argv = sys.argv
        try:
            sys.argv = [
                "generate_bgm_candidates.py",
                str(project),
                "--count",
                "1",
            ]
            # The TypeError should propagate and not be caught
            with pytest.raises(TypeError):
                generate_bgm_candidates.main()
        finally:
            sys.argv = old_argv
