from __future__ import annotations

import json
from pathlib import Path

import pytest

from bgm_config import resolve_style_preset

REPO_ROOT = Path(__file__).resolve().parents[1]
PRESETS_PATH = REPO_ROOT / "config" / "bgm-presets.json"
VISUAL_STYLES_PATH = REPO_ROOT / "config" / "visual-styles.json"


@pytest.fixture(scope="module")
def presets() -> dict:
    return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def visual_style_ids() -> list:
    data = json.loads(VISUAL_STYLES_PATH.read_text(encoding="utf-8"))
    return sorted(data["styles"])


def test_defaults_present(presets: dict):
    defaults = presets["defaults"]
    assert defaults["candidate_count"] == 4
    assert defaults["candidate_length_ms"] == 40000
    assert defaults["output_format"] == "mp3_44100_128"
    assert defaults["preview_seconds"] == 30
    assert defaults["preview_start_ratio"] == 0.6


def test_every_visual_style_has_a_preset(presets: dict, visual_style_ids: list):
    missing = [s for s in visual_style_ids if s not in presets["styles"]]
    assert missing == []


def test_every_preset_has_enough_variation_hints(presets: dict):
    default_count = presets["defaults"]["candidate_count"]
    for style_id, preset in presets["styles"].items():
        assert preset["base_prompt"].strip(), style_id
        assert len(preset["variation_hints"]) >= default_count, style_id


def test_presets_resolve_through_bgm_config(presets: dict, visual_style_ids: list):
    for style_id in visual_style_ids:
        assert resolve_style_preset(presets, style_id)["base_prompt"]
