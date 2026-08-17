# BGM 선택 및 적용 기능 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 영상 내용과 승인된 비주얼 스타일에 맞는 BGM 후보를 생성해 비교 청취하고, 승인된 하나를 TTS 재생성 없이 기존 내레이션에 믹싱하는 기능을 만든다.

**Architecture:** 순수 로직(`bgm_config.py`), ffmpeg 믹싱(`audio_mixing.py`), 리뷰 페이지 생성(`bgm_review_page.py`)을 각각 분리한 모듈로 두고, 두 개의 CLI 스크립트(`generate_bgm_candidates.py`, `apply_bgm.py`)가 이를 조합한다. 기존 `generate_elevenlabs_audio.py`는 믹싱 함수를 공유 모듈에서 import하도록만 바꾸고 동작은 그대로 유지한다.

**Tech Stack:** Python 3.9 (시스템 `python3`), ffmpeg/ffprobe, pytest, ElevenLabs Music API (`POST /v1/music`)

## Global Constraints

- Python은 시스템 `python3` 3.9.6이다. 새 모듈은 반드시 `from __future__ import annotations`로 시작한다. `X | None` 같은 표기를 런타임 값으로 쓰지 않는다.
- `scripts/`에는 `__init__.py`가 없다. 스크립트를 `python3 scripts/foo.py`로 실행하면 `sys.path[0]`이 `scripts/`가 되므로 형제 모듈은 `from audio_mixing import ...`로 import한다. (검증 완료)
- API 키는 `ELEVENLABS_API_KEY` 환경변수로만 읽는다. 키를 소스·JSON·로그·커밋·응답에 절대 넣지 않는다.
- `02_audio/working/voice.wav`(voice-only 마스터)는 어떤 경우에도 덮어쓰지 않는다.
- 믹싱 기본값은 `config/success-rules.json`의 `audio_rules.bgm`에서 읽는다: 더킹 `-18dB`, 아웃트로 `4초`, 페이드아웃 `3초`. 아웃트로 게인 `-14dB`는 success-rules에 없으므로 코드 기본값으로 둔다.
- `music_length_ms` 허용 범위는 3,000~600,000ms이다.
- **커밋은 사용자가 명시적으로 요청했을 때만 실행한다** (`AGENTS.md`). 요청 전에는 각 태스크의 커밋 단계를 건너뛰고 작업 트리에만 남긴다.
- `projects/2026-010-sixth-guest/` 안의 파일은 읽기만 한다. 검증 출력은 전부 저장소 밖 임시 경로로 보낸다.
- 기존 파이프라인 스크립트(`render_project.py`, 캡션 렌더러, `ingest_audio.py`)는 수정하지 않는다.

## File Structure

| 파일 | 책임 |
|---|---|
| `scripts/audio_mixing.py` (신규) | ffmpeg 믹싱과 길이 측정. 부작용이 있는 미디어 처리만 담당 |
| `scripts/bgm_config.py` (신규) | 설정 해석, 프롬프트 조립, 값 검증. 순수 함수만. 파일 IO 없음 |
| `scripts/bgm_review_page.py` (신규) | 비교 청취 HTML 문자열 생성. 순수 함수 |
| `scripts/apply_bgm.py` (신규) | 승인된 후보를 기존 음성에 적용하는 CLI |
| `scripts/generate_bgm_candidates.py` (신규) | 후보 생성 CLI. ElevenLabs Music API 호출 |
| `config/bgm-presets.json` (신규) | 비주얼 스타일 9종의 프롬프트 프리셋 |
| `scripts/generate_elevenlabs_audio.py` (수정) | 믹싱 함수를 import로 전환 |
| `tests/` (신규) | pytest 단위 테스트 |

순수 로직을 `bgm_config.py`로 분리한 것은 스펙에서 한 단계 더 나눈 것이다. 스펙은 공유 모듈로 `audio_mixing.py`만 언급했으나, ffmpeg를 호출하지 않는 로직을 섞으면 테스트가 전부 미디어 파일을 요구하게 되어 분리했다.

---

### Task 1: 테스트 환경과 `audio_mixing.py` 추출

기존에 잘 돌아가는 믹싱 코드를 공유 모듈로 옮긴다. **동작이 조금도 바뀌면 안 된다.** 이 태스크가 안전망(테스트)도 함께 만든다.

**Files:**
- Create: `requirements-dev.txt`
- Create: `tests/conftest.py`
- Create: `tests/test_audio_mixing.py`
- Create: `scripts/audio_mixing.py`
- Modify: `scripts/generate_elevenlabs_audio.py:29-32` (상수 제거), `:172-244` (함수 제거), `:17` 부근 (import 추가)

**Interfaces:**
- Consumes: 없음 (첫 태스크)
- Produces:
  - `audio_mixing.DEFAULT_BGM_GAIN_DB: float = -18.0`
  - `audio_mixing.DEFAULT_BGM_OUTRO_SECONDS: float = 4.0`
  - `audio_mixing.DEFAULT_BGM_OUTRO_GAIN_DB: float = -14.0`
  - `audio_mixing.DEFAULT_BGM_FADE_OUT_SECONDS: float = 3.0`
  - `audio_mixing.audio_duration_seconds(path: Path) -> float`
  - `audio_mixing.mix_bgm_with_voice(*, voice_audio: Path, bgm_audio: Path, target_audio: Path, gain_db: float = ..., outro_seconds: float = ..., outro_gain_db: float = ..., fade_out_seconds: float = ...) -> None`

- [ ] **Step 1: pytest 개발 의존성 파일 생성**

`requirements.txt`는 런타임 의존성만 유지하고, 테스트 도구는 분리한다. `requirements-dev.txt`를 만든다:

```text
pytest>=7.4.0
```

설치:

```bash
python3 -m pip install --user -r requirements-dev.txt
```

- [ ] **Step 2: pytest가 `scripts/`를 import할 수 있게 conftest 작성**

`scripts/`에 `__init__.py`가 없으므로 sys.path에 직접 넣는다.

```python
# tests/conftest.py
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
```

- [ ] **Step 3: 실패하는 테스트 작성**

ffmpeg의 `sine` 소스로 테스트용 오디오를 만든다. 실제 미디어 파일이 필요 없다.

```python
# tests/test_audio_mixing.py
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from audio_mixing import (
    DEFAULT_BGM_FADE_OUT_SECONDS,
    DEFAULT_BGM_GAIN_DB,
    DEFAULT_BGM_OUTRO_SECONDS,
    audio_duration_seconds,
    mix_bgm_with_voice,
)


def make_tone(path: Path, seconds: float, frequency: int) -> Path:
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", f"sine=frequency={frequency}:duration={seconds}",
            str(path),
        ],
        check=True,
    )
    return path


@pytest.fixture
def voice(tmp_path: Path) -> Path:
    return make_tone(tmp_path / "voice.wav", 5.0, 220)


@pytest.fixture
def bgm(tmp_path: Path) -> Path:
    return make_tone(tmp_path / "bgm.mp3", 2.0, 440)


def test_defaults_match_success_rules():
    assert DEFAULT_BGM_GAIN_DB == -18.0
    assert DEFAULT_BGM_OUTRO_SECONDS == 4.0
    assert DEFAULT_BGM_FADE_OUT_SECONDS == 3.0


def test_audio_duration_seconds_reads_actual_length(voice: Path):
    assert audio_duration_seconds(voice) == pytest.approx(5.0, abs=0.05)


def test_mix_appends_outro_tail(voice: Path, bgm: Path, tmp_path: Path):
    target = tmp_path / "mixed.mp3"
    mix_bgm_with_voice(
        voice_audio=voice, bgm_audio=bgm, target_audio=target, outro_seconds=4.0
    )
    assert audio_duration_seconds(target) == pytest.approx(9.0, abs=0.15)


def test_mix_loops_bgm_shorter_than_voice(voice: Path, bgm: Path, tmp_path: Path):
    target = tmp_path / "looped.mp3"
    mix_bgm_with_voice(voice_audio=voice, bgm_audio=bgm, target_audio=target)
    assert audio_duration_seconds(target) > audio_duration_seconds(bgm)


def test_mix_does_not_modify_voice(voice: Path, bgm: Path, tmp_path: Path):
    before = voice.read_bytes()
    mix_bgm_with_voice(
        voice_audio=voice, bgm_audio=bgm, target_audio=tmp_path / "out.mp3"
    )
    assert voice.read_bytes() == before
```

- [ ] **Step 4: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest tests/test_audio_mixing.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'audio_mixing'`

- [ ] **Step 5: `scripts/audio_mixing.py` 생성**

`generate_elevenlabs_audio.py:29-32`의 상수와 `:172-244`의 두 함수를 **한 글자도 바꾸지 않고** 옮긴다. 아래가 옮긴 결과 전문이다.

```python
#!/usr/bin/env python3
"""Shared ffmpeg helpers for measuring audio length and mixing BGM under narration."""

from __future__ import annotations

import subprocess
from pathlib import Path

DEFAULT_BGM_GAIN_DB = -18.0
DEFAULT_BGM_OUTRO_SECONDS = 4.0
DEFAULT_BGM_OUTRO_GAIN_DB = -14.0
DEFAULT_BGM_FADE_OUT_SECONDS = 3.0


def audio_duration_seconds(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def mix_bgm_with_voice(
    *,
    voice_audio: Path,
    bgm_audio: Path,
    target_audio: Path,
    gain_db: float = DEFAULT_BGM_GAIN_DB,
    outro_seconds: float = DEFAULT_BGM_OUTRO_SECONDS,
    outro_gain_db: float = DEFAULT_BGM_OUTRO_GAIN_DB,
    fade_out_seconds: float = DEFAULT_BGM_FADE_OUT_SECONDS,
) -> None:
    voice_duration = audio_duration_seconds(voice_audio)
    outro_duration = max(outro_seconds, 0.0)
    total_duration = voice_duration + outro_duration
    fade_duration = min(max(fade_out_seconds, 0.0), max(total_duration, 0.0))
    fade_start = max(total_duration - fade_duration, 0.0)
    bgm_main_volume = 10 ** (gain_db / 20)
    bgm_outro_volume = 10 ** (outro_gain_db / 20)
    filter_complex = (
        f"[0:a]atrim=0:{voice_duration:.3f},asetpts=PTS-STARTPTS,"
        f"apad=pad_dur={outro_duration:.3f},atrim=0:{total_duration:.3f}[voice];"
        f"[1:a]atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS,"
        f"volume='if(lt(t,{voice_duration:.3f}),{bgm_main_volume:.8f},{bgm_outro_volume:.8f})':eval=frame,"
        f"atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={fade_start:.3f}:d={fade_duration:.3f}[bgm];"
        "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        f"atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS[mixed]"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(voice_audio),
            "-stream_loop",
            "-1",
            "-i",
            str(bgm_audio),
            "-filter_complex",
            filter_complex,
            "-map",
            "[mixed]",
            "-t",
            f"{total_duration:.3f}",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(target_audio),
        ],
        check=True,
    )
```

- [ ] **Step 6: 테스트가 통과하는지 확인**

Run: `python3 -m pytest tests/test_audio_mixing.py -v`
Expected: PASS — 5 passed

- [ ] **Step 7: `generate_elevenlabs_audio.py`에서 중복 제거**

`scripts/generate_elevenlabs_audio.py`에서 다음을 삭제한다:
- 29~32행의 `DEFAULT_BGM_*` 상수 4줄
- 172~188행의 `audio_duration_seconds` 함수 전체
- 191~244행의 `mix_bgm_with_voice` 함수 전체

그리고 17행 `from dotenv import load_dotenv` 바로 다음 줄에 아래를 추가한다:

```python
from audio_mixing import (
    DEFAULT_BGM_FADE_OUT_SECONDS,
    DEFAULT_BGM_GAIN_DB,
    DEFAULT_BGM_OUTRO_GAIN_DB,
    DEFAULT_BGM_OUTRO_SECONDS,
    audio_duration_seconds,
    mix_bgm_with_voice,
)
```

`subprocess` import는 `merge_audio_parts`가 계속 쓰므로 **삭제하지 않는다.**

- [ ] **Step 8: 기존 스크립트가 깨지지 않았는지 확인**

Run: `python3 scripts/generate_elevenlabs_audio.py --help`
Expected: usage 출력. `--bgm`, `--bgm-gain-db`, `--bgm-outro-seconds`, `--bgm-outro-gain-db`, `--bgm-fade-out-seconds` 다섯 플래그가 모두 보여야 한다.

Run: `python3 -m py_compile scripts/generate_elevenlabs_audio.py scripts/audio_mixing.py && echo OK`
Expected: `OK`

- [ ] **Step 9: 실제 음원으로 회귀 확인 (저장소 밖으로만 출력)**

```bash
python3 -c "
import sys, os, tempfile
sys.path.insert(0, 'scripts')
from pathlib import Path
from audio_mixing import audio_duration_seconds, mix_bgm_with_voice
voice = Path('projects/2026-010-sixth-guest/02_audio/working/voice.wav')
bgm = Path('library/audio/music/midnight-library.mp3')
before = voice.stat().st_mtime
out = Path(tempfile.gettempdir()) / 'bgm-regression.mp3'
mix_bgm_with_voice(voice_audio=voice, bgm_audio=bgm, target_audio=out)
v = audio_duration_seconds(voice)
m = audio_duration_seconds(out)
print('voice  :', round(v, 3))
print('mixed  :', round(m, 3))
print('delta  :', round(m - v, 3))
print('voice untouched:', voice.stat().st_mtime == before)
os.remove(out)
"
```

Expected: `delta`가 `4.0`에 가깝고 `voice untouched: True`

- [ ] **Step 10: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add requirements-dev.txt tests/conftest.py tests/test_audio_mixing.py scripts/audio_mixing.py scripts/generate_elevenlabs_audio.py
git commit -m "refactor: extract BGM mixing helpers into audio_mixing module"
```

---

### Task 2: `bgm_config.py` 순수 로직

파일 IO도 ffmpeg 호출도 없는 함수만 모은다. 테스트가 빠르고 미디어 파일이 필요 없다.

**Files:**
- Create: `scripts/bgm_config.py`
- Create: `tests/test_bgm_config.py`

**Interfaces:**
- Consumes: 없음
- Produces:
  - `bgm_config.MIN_MUSIC_LENGTH_MS: int = 3000`
  - `bgm_config.MAX_MUSIC_LENGTH_MS: int = 600000`
  - `bgm_config.BgmSettings` — frozen dataclass, 필드 `gain_db: float`, `outro_seconds: float`, `outro_gain_db: float`, `fade_out_seconds: float`
  - `bgm_config.load_bgm_settings(success_rules: dict) -> BgmSettings`
  - `bgm_config.resolve_style_preset(presets: dict, style_id: str) -> dict`
  - `bgm_config.build_prompt(base_prompt: str, variation_hint: str, content_hint: str) -> str`
  - `bgm_config.validate_music_length_ms(value: int) -> int`
  - `bgm_config.preview_window(total_seconds: float, start_ratio: float, preview_seconds: float) -> tuple`

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_bgm_config.py
from __future__ import annotations

import pytest

from bgm_config import (
    MAX_MUSIC_LENGTH_MS,
    MIN_MUSIC_LENGTH_MS,
    build_prompt,
    load_bgm_settings,
    preview_window,
    resolve_style_preset,
    validate_music_length_ms,
)

SUCCESS_RULES = {
    "audio_rules": {
        "bgm": {
            "enabled": True,
            "voice_ducking_gain_db": -18,
            "outro_delay_seconds": 4,
            "fade_out_seconds": 3,
        }
    }
}

PRESETS = {
    "styles": {
        "dark_cinematic": {
            "base_prompt": "낮은 드론.",
            "variation_hints": ["현악 중심", "드론 중심"],
        }
    }
}


def test_load_bgm_settings_reads_success_rules():
    settings = load_bgm_settings(SUCCESS_RULES)
    assert settings.gain_db == -18.0
    assert settings.outro_seconds == 4.0
    assert settings.fade_out_seconds == 3.0


def test_load_bgm_settings_defaults_outro_gain_absent_from_rules():
    assert load_bgm_settings(SUCCESS_RULES).outro_gain_db == -14.0


def test_load_bgm_settings_handles_empty_config():
    settings = load_bgm_settings({})
    assert settings.outro_seconds == 4.0


def test_resolve_style_preset_returns_preset():
    assert resolve_style_preset(PRESETS, "dark_cinematic")["base_prompt"] == "낮은 드론."


def test_resolve_style_preset_lists_available_on_miss():
    with pytest.raises(KeyError) as excinfo:
        resolve_style_preset(PRESETS, "neon_tech")
    assert "dark_cinematic" in str(excinfo.value)


def test_build_prompt_joins_parts():
    assert build_prompt("기본.", "변주.", "내용.") == "기본. 변주. 내용."


def test_build_prompt_skips_empty_parts():
    assert build_prompt("기본.", "", "  ") == "기본."


def test_validate_music_length_ms_accepts_bounds():
    assert validate_music_length_ms(MIN_MUSIC_LENGTH_MS) == MIN_MUSIC_LENGTH_MS
    assert validate_music_length_ms(MAX_MUSIC_LENGTH_MS) == MAX_MUSIC_LENGTH_MS


def test_validate_music_length_ms_rejects_out_of_range():
    with pytest.raises(ValueError):
        validate_music_length_ms(MAX_MUSIC_LENGTH_MS + 1)
    with pytest.raises(ValueError):
        validate_music_length_ms(MIN_MUSIC_LENGTH_MS - 1)


def test_preview_window_uses_ratio():
    start, duration = preview_window(1000.0, 0.6, 30.0)
    assert start == pytest.approx(600.0)
    assert duration == pytest.approx(30.0)


def test_preview_window_clamps_to_end():
    start, duration = preview_window(100.0, 0.99, 30.0)
    assert start == pytest.approx(70.0)
    assert duration == pytest.approx(30.0)


def test_preview_window_handles_short_audio():
    start, duration = preview_window(10.0, 0.6, 30.0)
    assert start == 0.0
    assert duration == pytest.approx(10.0)
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest tests/test_bgm_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'bgm_config'`

- [ ] **Step 3: `scripts/bgm_config.py` 구현**

```python
#!/usr/bin/env python3
"""Pure configuration helpers for BGM candidate generation and mixing."""

from __future__ import annotations

from dataclasses import dataclass

MIN_MUSIC_LENGTH_MS = 3000
MAX_MUSIC_LENGTH_MS = 600000

DEFAULT_GAIN_DB = -18.0
DEFAULT_OUTRO_SECONDS = 4.0
DEFAULT_OUTRO_GAIN_DB = -14.0
DEFAULT_FADE_OUT_SECONDS = 3.0


@dataclass(frozen=True)
class BgmSettings:
    gain_db: float
    outro_seconds: float
    outro_gain_db: float
    fade_out_seconds: float


def load_bgm_settings(success_rules: dict) -> BgmSettings:
    """Read audio_rules.bgm from success-rules.json content.

    outro_gain_db has no key in success-rules.json, so it falls back to the
    code default that generate_elevenlabs_audio.py has always used.
    """
    audio_rules = success_rules.get("audio_rules") or {}
    bgm = audio_rules.get("bgm") or {}
    return BgmSettings(
        gain_db=float(bgm.get("voice_ducking_gain_db", DEFAULT_GAIN_DB)),
        outro_seconds=float(bgm.get("outro_delay_seconds", DEFAULT_OUTRO_SECONDS)),
        outro_gain_db=float(bgm.get("outro_gain_db", DEFAULT_OUTRO_GAIN_DB)),
        fade_out_seconds=float(bgm.get("fade_out_seconds", DEFAULT_FADE_OUT_SECONDS)),
    )


def resolve_style_preset(presets: dict, style_id: str) -> dict:
    styles = presets.get("styles") or {}
    if style_id not in styles:
        available = ", ".join(sorted(styles)) or "(none)"
        raise KeyError(
            f"no BGM preset for visual style '{style_id}'. Available: {available}"
        )
    return styles[style_id]


def build_prompt(base_prompt: str, variation_hint: str, content_hint: str) -> str:
    parts = [base_prompt.strip(), variation_hint.strip(), content_hint.strip()]
    return " ".join(part for part in parts if part)


def validate_music_length_ms(value: int) -> int:
    if not MIN_MUSIC_LENGTH_MS <= value <= MAX_MUSIC_LENGTH_MS:
        raise ValueError(
            f"music_length_ms must be between {MIN_MUSIC_LENGTH_MS} and "
            f"{MAX_MUSIC_LENGTH_MS}, got {value}"
        )
    return value


def preview_window(
    total_seconds: float, start_ratio: float, preview_seconds: float
) -> tuple:
    """Return (start_seconds, duration_seconds) for the narration preview slice."""
    if total_seconds <= preview_seconds:
        return 0.0, total_seconds
    start = total_seconds * start_ratio
    if start + preview_seconds > total_seconds:
        start = total_seconds - preview_seconds
    return max(start, 0.0), preview_seconds
```

- [ ] **Step 4: 테스트가 통과하는지 확인**

Run: `python3 -m pytest tests/test_bgm_config.py -v`
Expected: PASS — 12 passed

- [ ] **Step 5: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add scripts/bgm_config.py tests/test_bgm_config.py
git commit -m "feat: add pure BGM configuration helpers"
```

---

### Task 3: `config/bgm-presets.json` 프리셋 9종

`config/visual-styles.json`에 있는 9개 스타일 전부에 프리셋을 채운다. 하나라도 빠지면 그 스타일 프로젝트에서 기능이 동작하지 않는다.

**Files:**
- Create: `config/bgm-presets.json`
- Create: `tests/test_bgm_presets.py`

**Interfaces:**
- Consumes: `bgm_config.resolve_style_preset` (Task 2)
- Produces: `config/bgm-presets.json` — `schema_version`, `defaults`, `styles` 최상위 키

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_bgm_presets.py
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
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest tests/test_bgm_presets.py -v`
Expected: FAIL — `FileNotFoundError` (config/bgm-presets.json 없음)

- [ ] **Step 3: `config/bgm-presets.json` 작성**

```json
{
  "schema_version": "1.0.0",
  "defaults": {
    "candidate_count": 4,
    "candidate_length_ms": 40000,
    "output_format": "mp3_44100_128",
    "preview_seconds": 30,
    "preview_start_ratio": 0.6
  },
  "styles": {
    "minimal_dark_tech": {
      "label_ko": "미니멀 다크 테크",
      "base_prompt": "절제된 신스 펄스와 낮은 베이스, 넓은 여백. 일정한 템포의 미니멀 아르페지오. 보컬 없음, 오케스트라 없음, 과한 리버브 없음.",
      "variation_hints": [
        "아르페지오를 조금 더 또렷하게",
        "베이스 중심으로 상단을 비우고",
        "짧은 노이즈 텍스처를 얇게 추가",
        "템포를 약간 낮춰 더 차분하게"
      ]
    },
    "bright_editorial": {
      "label_ko": "밝은 에디토리얼",
      "base_prompt": "밝고 깨끗한 어쿠스틱 기타와 가벼운 마림바, 부드러운 패드. 낙관적이고 단정한 진행. 보컬 없음, 강한 드럼 없음.",
      "variation_hints": [
        "마림바를 전면에",
        "피아노 중심으로 바꿔서",
        "리듬 없이 패드만 유지",
        "가벼운 핑거스냅을 얇게 추가"
      ]
    },
    "dark_cinematic": {
      "label_ko": "다크 시네마틱",
      "base_prompt": "낮은 서브 드론과 지속되는 불협 현악, 멀리서 들리는 겨울 바람. 느리고 일정한 긴장. 보컬 없음, 갑작스러운 큰 스팅어 없음, 드럼 비트 없음.",
      "variation_hints": [
        "현악 중심으로 활 긁는 질감을 조금 더",
        "드론 중심으로 거의 정적에 가깝게",
        "금속성 울림과 미세한 하모닉스 추가",
        "낮은 피아노 단음을 드문드문"
      ]
    },
    "contrast_split": {
      "label_ko": "명암 분할",
      "base_prompt": "대비되는 두 음색이 번갈아 나타나는 구성. 낮은 드론과 밝은 벨이 교대하며 긴장과 해소를 반복. 보컬 없음.",
      "variation_hints": [
        "벨 쪽을 더 밝고 선명하게",
        "드론 쪽을 더 무겁게",
        "교대 간격을 더 짧게",
        "두 음색이 겹치는 중간 지대를 넓게"
      ]
    },
    "warm_documentary": {
      "label_ko": "따뜻한 다큐멘터리",
      "base_prompt": "따뜻한 피아노와 얇은 현악, 느린 호흡. 회상하는 듯한 진행. 보컬 없음, 타악기 최소.",
      "variation_hints": [
        "피아노 단독에 가깝게",
        "현악을 조금 더 두껍게",
        "어쿠스틱 기타 아르페지오 추가",
        "더 느리고 여백 있게"
      ]
    },
    "premium_finance": {
      "label_ko": "프리미엄 금융",
      "base_prompt": "정제된 신스 패드와 절제된 펄스, 낮은 긴장을 유지하는 일정한 진행. 신뢰감 있는 질감. 보컬 없음, 화려한 멜로디 없음.",
      "variation_hints": [
        "펄스를 더 규칙적으로",
        "저역 패드를 두껍게",
        "얇은 벨 하이라이트 추가",
        "긴장을 조금 더 올려서"
      ]
    },
    "neon_tech": {
      "label_ko": "네온 테크",
      "base_prompt": "신스웨이브 아르페지오와 단단한 저역, 야간 도시의 질감. 일정한 그루브. 보컬 없음, 공격적인 드롭 없음.",
      "variation_hints": [
        "아르페지오를 더 빠르게",
        "저역 중심으로 상단을 절제",
        "테이프 노이즈 질감 추가",
        "코드 진행을 더 어둡게"
      ]
    },
    "paper_collage": {
      "label_ko": "종이 콜라주",
      "base_prompt": "가벼운 피치카토 현과 종이 스치는 질감의 퍼커션, 장난기 있는 진행. 보컬 없음, 무거운 저역 없음.",
      "variation_hints": [
        "피치카토를 더 통통 튀게",
        "퍼커션 질감을 전면에",
        "목관 악기를 얇게 추가",
        "템포를 낮춰 더 여유 있게"
      ]
    },
    "adaptive_mix": {
      "label_ko": "적응형 믹스",
      "base_prompt": "중립적인 앰비언트 패드와 은은한 펄스. 어떤 주제에도 얹을 수 있는 절제된 배경. 보컬 없음, 강한 성격 없음.",
      "variation_hints": [
        "조금 더 밝은 쪽으로",
        "조금 더 어두운 쪽으로",
        "리듬감을 살짝 부여",
        "거의 정적인 패드만"
      ]
    }
  }
}
```

- [ ] **Step 4: 테스트가 통과하는지 확인**

Run: `python3 -m pytest tests/test_bgm_presets.py -v`
Expected: PASS — 4 passed

- [ ] **Step 5: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add config/bgm-presets.json tests/test_bgm_presets.py
git commit -m "feat: add BGM prompt presets for all nine visual styles"
```

---

### Task 4: `apply_bgm.py` — 승인된 후보 적용

API를 호출하지 않으므로 완전히 오프라인으로 검증된다. 후보 생성보다 먼저 만드는 이유가 여기에 있다.

`mix_bgm_with_voice`는 출력 코덱이 `libmp3lame`으로 고정돼 있는데 컴포지션은 `voice.wav`를 참조한다. 그래서 **기본값을 유지한 채** 코덱 인자를 선택적으로 받도록 확장한다. 기존 호출자(`generate_elevenlabs_audio.py`)는 인자를 넘기지 않으므로 동작이 바뀌지 않는다.

**Files:**
- Modify: `scripts/audio_mixing.py` (`mix_bgm_with_voice`에 `output_codec_args` 매개변수 추가)
- Create: `scripts/apply_bgm.py`
- Create: `tests/test_apply_bgm.py`

**Interfaces:**
- Consumes: `audio_mixing.audio_duration_seconds`, `audio_mixing.mix_bgm_with_voice` (Task 1), `bgm_config.load_bgm_settings` (Task 2)
- Produces:
  - `audio_mixing.MP3_CODEC_ARGS: list = ["-c:a", "libmp3lame", "-b:a", "192k"]`
  - `audio_mixing.WAV_CODEC_ARGS: list = ["-c:a", "pcm_s16le"]`
  - `apply_bgm.resolve_candidate(project: Path, candidate: str) -> Path`
  - `apply_bgm.update_composition_duration(index_html: Path, total_seconds: float) -> bool`
  - `apply_bgm.update_request_config(project: Path, bgm_path: Path) -> None`

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_apply_bgm.py
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from apply_bgm import resolve_candidate, update_composition_duration
from audio_mixing import WAV_CODEC_ARGS, audio_duration_seconds, mix_bgm_with_voice


def make_tone(path: Path, seconds: float, frequency: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", f"sine=frequency={frequency}:duration={seconds}",
            str(path),
        ],
        check=True,
    )
    return path


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    make_tone(root / "02_audio" / "bgm" / "candidates" / "cand-01.mp3", 2.0, 440)
    make_tone(root / "02_audio" / "bgm" / "candidates" / "cand-02.mp3", 2.0, 330)
    return root


def test_resolve_candidate_by_id(project: Path):
    assert resolve_candidate(project, "cand-02").name == "cand-02.mp3"


def test_resolve_candidate_by_filename(project: Path):
    assert resolve_candidate(project, "cand-01.mp3").name == "cand-01.mp3"


def test_resolve_candidate_lists_available_on_miss(project: Path):
    with pytest.raises(SystemExit) as excinfo:
        resolve_candidate(project, "cand-99")
    assert "cand-01.mp3" in str(excinfo.value)


def test_update_composition_duration_rewrites_attribute(tmp_path: Path):
    index_html = tmp_path / "index.html"
    index_html.write_text(
        '<audio id="voice" data-start="0" data-duration="1153.031" '
        'src="assets/audio/voice.wav"></audio>',
        encoding="utf-8",
    )
    assert update_composition_duration(index_html, 1157.031) is True
    assert 'data-duration="1157.031"' in index_html.read_text(encoding="utf-8")


def test_update_composition_duration_reports_no_match(tmp_path: Path):
    index_html = tmp_path / "index.html"
    index_html.write_text("<div>no audio element</div>", encoding="utf-8")
    assert update_composition_duration(index_html, 10.0) is False


def test_wav_output_is_pcm(tmp_path: Path):
    voice = make_tone(tmp_path / "voice.wav", 3.0, 220)
    bgm = make_tone(tmp_path / "bgm.mp3", 1.0, 440)
    target = tmp_path / "voice-bgm.wav"
    mix_bgm_with_voice(
        voice_audio=voice,
        bgm_audio=bgm,
        target_audio=target,
        output_codec_args=WAV_CODEC_ARGS,
    )
    codec = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_name",
            "-of", "default=noprint_wrappers=1:nokey=1", str(target),
        ],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert codec == "pcm_s16le"
    assert audio_duration_seconds(target) == pytest.approx(7.0, abs=0.15)
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest tests/test_apply_bgm.py -v`
Expected: FAIL — `ImportError: cannot import name 'WAV_CODEC_ARGS' from 'audio_mixing'`

- [ ] **Step 3: `audio_mixing.py`에 코덱 인자 추가**

`scripts/audio_mixing.py`의 `DEFAULT_BGM_FADE_OUT_SECONDS = 3.0` 아래에 추가:

```python
MP3_CODEC_ARGS = ["-c:a", "libmp3lame", "-b:a", "192k"]
WAV_CODEC_ARGS = ["-c:a", "pcm_s16le"]
```

`mix_bgm_with_voice` 시그니처의 `fade_out_seconds` 줄 다음을 아래로 교체:

```python
    fade_out_seconds: float = DEFAULT_BGM_FADE_OUT_SECONDS,
    output_codec_args: list = None,
) -> None:
```

함수 본문 첫 줄(`voice_duration = ...`) 앞에 추가:

```python
    codec_args = list(output_codec_args) if output_codec_args else list(MP3_CODEC_ARGS)
```

그리고 `subprocess.run` 인자 리스트에서 아래 네 줄을

```python
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
```

다음 한 줄로 교체한다:

```python
            *codec_args,
```

- [ ] **Step 4: `scripts/apply_bgm.py` 구현**

```python
#!/usr/bin/env python3
"""Mix an approved BGM candidate under an existing narration voice track.

This never calls the ElevenLabs TTS API, so an approved voice take and its
caption timings stay intact.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

from audio_mixing import WAV_CODEC_ARGS, audio_duration_seconds, mix_bgm_with_voice
from bgm_config import load_bgm_settings

REPO_ROOT = Path(__file__).resolve().parents[1]
SUCCESS_RULES_PATH = REPO_ROOT / "config" / "success-rules.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_candidate(project: Path, candidate: str) -> Path:
    candidates_dir = project / "02_audio" / "bgm" / "candidates"
    direct = Path(candidate)
    if direct.is_file():
        return direct
    for suffix in ("", ".mp3"):
        guess = candidates_dir / f"{candidate}{suffix}"
        if guess.is_file():
            return guess
    available = (
        sorted(p.name for p in candidates_dir.glob("*.mp3"))
        if candidates_dir.is_dir()
        else []
    )
    raise SystemExit(
        f"candidate not found: {candidate}. "
        f"Available: {', '.join(available) or '(none)'}"
    )


def update_composition_duration(index_html: Path, total_seconds: float) -> bool:
    text = index_html.read_text(encoding="utf-8")
    pattern = re.compile(r'(<audio[^>]*id="voice"[^>]*data-duration=")([0-9.]+)(")')
    updated, count = pattern.subn(rf"\g<1>{total_seconds:.3f}\g<3>", text)
    if count:
        index_html.write_text(updated, encoding="utf-8")
    return bool(count)


def update_request_config(project: Path, bgm_path: Path) -> None:
    config_path = project / "02_audio" / "elevenlabs-request.json"
    if not config_path.is_file():
        return
    config = load_json(config_path)
    bgm_block = config.get("bgm") or {}
    bgm_block["source"] = os.path.relpath(bgm_path, config_path.parent)
    config["bgm"] = bgm_block
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mix an approved BGM candidate under an existing voice track"
    )
    parser.add_argument("project", type=Path, help="Project directory")
    parser.add_argument(
        "--candidate", required=True, help="Candidate id (cand-02) or path"
    )
    parser.add_argument("--outro-seconds", type=float)
    parser.add_argument("--gain-db", type=float)
    parser.add_argument(
        "--dry-run", action="store_true", help="Report the plan without writing files"
    )
    args = parser.parse_args()

    project = args.project.resolve()
    voice = project / "02_audio" / "working" / "voice.wav"
    if not voice.is_file():
        parser.error(
            f"missing voice track: {voice}. "
            "Run generate_elevenlabs_audio.py and ingest_audio.py first"
        )

    settings = load_bgm_settings(load_json(SUCCESS_RULES_PATH))
    gain_db = args.gain_db if args.gain_db is not None else settings.gain_db
    outro_seconds = (
        args.outro_seconds if args.outro_seconds is not None else settings.outro_seconds
    )

    bgm_path = resolve_candidate(project, args.candidate)
    voice_seconds = audio_duration_seconds(voice)
    total_seconds = voice_seconds + outro_seconds

    print(f"Voice      : {voice} ({voice_seconds:.3f}s)")
    print(f"BGM        : {bgm_path}")
    print(f"Gain       : {gain_db:.1f}dB under voice")
    print(f"Outro      : {outro_seconds:.1f}s at {settings.outro_gain_db:.1f}dB")
    print(f"Fade out   : {settings.fade_out_seconds:.1f}s")
    print(f"New length : {total_seconds:.3f}s")

    if args.dry_run:
        print("Dry run. No files written.")
        return 0

    mixed = project / "02_audio" / "working" / "voice-bgm.wav"
    mix_bgm_with_voice(
        voice_audio=voice,
        bgm_audio=bgm_path,
        target_audio=mixed,
        gain_db=gain_db,
        outro_seconds=outro_seconds,
        outro_gain_db=settings.outro_gain_db,
        fade_out_seconds=settings.fade_out_seconds,
        output_codec_args=WAV_CODEC_ARGS,
    )
    print(f"Wrote      : {mixed}")

    render_audio = project / "04_composition" / "assets" / "audio" / "voice.wav"
    render_audio.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mixed, render_audio)
    print(f"Replaced   : {render_audio}")
    print(f"Preserved  : {voice} (voice-only master, untouched)")

    update_request_config(project, bgm_path)

    index_html = project / "04_composition" / "index.html"
    if index_html.is_file():
        if update_composition_duration(index_html, total_seconds):
            print(f"Updated    : {index_html} data-duration={total_seconds:.3f}")
        else:
            print(f"WARNING    : no voice audio element found in {index_html}")

    print()
    print(
        f"NEXT: extend the composition outro by {outro_seconds:.1f}s "
        "and re-render. Captions end before the voice, so they are unaffected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: 테스트가 통과하는지 확인**

Run: `python3 -m pytest tests/test_apply_bgm.py -v`
Expected: PASS — 6 passed

- [ ] **Step 6: 전체 테스트로 회귀 확인**

Run: `python3 -m pytest tests/ -v`
Expected: PASS — 27 passed (Task 1의 5개 + Task 2의 12개 + Task 3의 4개 + Task 4의 6개)

- [ ] **Step 7: 실제 프로젝트로 dry-run 확인 (파일을 쓰지 않음)**

```bash
python3 scripts/apply_bgm.py projects/2026-010-sixth-guest \
  --candidate library/audio/music/midnight-library.mp3 --dry-run
```

Expected: `New length : 1157.0` 부근이 출력되고 `Dry run. No files written.`으로 끝난다.

- [ ] **Step 8: 2026-010이 변경되지 않았는지 확인**

Run: `git status --short projects/2026-010-sixth-guest`
Expected: 출력 없음

- [ ] **Step 9: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add scripts/apply_bgm.py scripts/audio_mixing.py tests/test_apply_bgm.py
git commit -m "feat: apply approved BGM to an existing voice track without re-running TTS"
```

---

### Task 5: `bgm_review_page.py` — 비교 청취 페이지

문자열만 만드는 순수 함수라 브라우저 없이 테스트된다.

**Files:**
- Create: `scripts/bgm_review_page.py`
- Create: `tests/test_bgm_review_page.py`

**Interfaces:**
- Consumes: 없음
- Produces: `bgm_review_page.render_selection_page(project_name: str, candidates: list) -> str`
  - `candidates`의 각 항목은 dict이며 키는 `id`(str), `prompt`(str), `bgm_href`(str), `preview_href`(str)

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_bgm_review_page.py
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
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest tests/test_bgm_review_page.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'bgm_review_page'`

- [ ] **Step 3: `scripts/bgm_review_page.py` 구현**

```python
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
```

- [ ] **Step 4: 테스트가 통과하는지 확인**

Run: `python3 -m pytest tests/test_bgm_review_page.py -v`
Expected: PASS — 5 passed

- [ ] **Step 5: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add scripts/bgm_review_page.py tests/test_bgm_review_page.py
git commit -m "feat: render BGM candidate comparison page"
```

---

### Task 6: `generate_bgm_candidates.py` — 후보 생성 CLI

앞선 모듈들을 조합하고 ElevenLabs Music API를 호출한다.

**Files:**
- Create: `scripts/generate_bgm_candidates.py`
- Create: `tests/test_generate_bgm_candidates.py`

**Interfaces:**
- Consumes: `bgm_config.*` (Task 2), `config/bgm-presets.json` (Task 3), `audio_mixing.*` (Task 1, 4), `bgm_review_page.render_selection_page` (Task 5)
- Produces:
  - `generate_bgm_candidates.default_content_hint(brief_path: Path) -> str`
  - `generate_bgm_candidates.build_candidate_specs(preset: dict, count: int, content_hint: str) -> list` — 각 항목은 `{"id": "cand-01", "prompt": "..."}`

- [ ] **Step 1: 실패하는 테스트 작성**

API를 호출하지 않는 두 함수만 단위 테스트한다. 네트워크 호출부는 Step 6의 스모크 테스트로 검증한다.

```python
# tests/test_generate_bgm_candidates.py
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
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인**

Run: `python3 -m pytest tests/test_generate_bgm_candidates.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'generate_bgm_candidates'`

- [ ] **Step 3: `scripts/generate_bgm_candidates.py` 구현**

```python
#!/usr/bin/env python3
"""Generate BGM candidates for a project and build the comparison page."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

from audio_mixing import audio_duration_seconds, mix_bgm_with_voice
from bgm_config import (
    build_prompt,
    load_bgm_settings,
    preview_window,
    resolve_style_preset,
    validate_music_length_ms,
)
from bgm_review_page import render_selection_page

REPO_ROOT = Path(__file__).resolve().parents[1]
SUCCESS_RULES_PATH = REPO_ROOT / "config" / "success-rules.json"
PRESETS_PATH = REPO_ROOT / "config" / "bgm-presets.json"
MUSIC_URL = "https://api.elevenlabs.io/v1/music"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def default_content_hint(brief_path: Path) -> str:
    if not brief_path.is_file():
        return ""
    for block in brief_path.read_text(encoding="utf-8").split("\n\n"):
        text = " ".join(
            line.strip()
            for line in block.strip().splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
        if text:
            return text
    return ""


def build_candidate_specs(preset: dict, count: int, content_hint: str) -> list:
    hints = preset.get("variation_hints") or []
    if count > len(hints):
        raise ValueError(
            f"requested {count} candidates but the preset has only {len(hints)} "
            "variation_hints"
        )
    specs = []
    for index in range(count):
        specs.append(
            {
                "id": f"cand-{index + 1:02d}",
                "prompt": build_prompt(
                    preset.get("base_prompt", ""), hints[index], content_hint
                ),
            }
        )
    return specs


def request_music_bytes(
    *, api_key: str, prompt: str, length_ms: int, output_format: str
) -> bytes:
    query = urllib.parse.urlencode({"output_format": output_format})
    payload = json.dumps(
        {"prompt": prompt, "music_length_ms": length_ms}, ensure_ascii=False
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{MUSIC_URL}?{query}",
        data=payload,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return response.read()


def slice_narration(voice: Path, target: Path, start: float, duration: float) -> None:
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{start:.3f}", "-t", f"{duration:.3f}", "-i", str(voice),
            str(target),
        ],
        check=True,
    )


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    parser = argparse.ArgumentParser(
        description="Generate BGM candidates and a comparison page for a project"
    )
    parser.add_argument("project", type=Path, help="Project directory")
    parser.add_argument("--count", type=int)
    parser.add_argument("--length-ms", type=int)
    parser.add_argument("--content-hint", default=None)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        parser.error("missing API key. Set ELEVENLABS_API_KEY in your shell environment")

    project = args.project.resolve()
    profile_path = project / "04_composition" / "profile.json"
    if not profile_path.is_file():
        parser.error(f"missing composition profile: {profile_path}")
    style_id = load_json(profile_path).get("visual_style_id")

    presets = load_json(PRESETS_PATH)
    try:
        preset = resolve_style_preset(presets, style_id)
    except KeyError as error:
        parser.error(str(error))

    defaults = presets.get("defaults") or {}
    count = args.count or defaults.get("candidate_count", 4)
    length_ms = validate_music_length_ms(
        args.length_ms or defaults.get("candidate_length_ms", 40000)
    )
    output_format = defaults.get("output_format", "mp3_44100_128")

    content_hint = args.content_hint
    if content_hint is None:
        content_hint = default_content_hint(project / "00_brief" / "brief.md")

    try:
        specs = build_candidate_specs(preset, count, content_hint)
    except ValueError as error:
        parser.error(str(error))

    bgm_dir = project / "02_audio" / "bgm"
    candidates_dir = bgm_dir / "candidates"
    previews_dir = bgm_dir / "previews"
    if candidates_dir.exists() and any(candidates_dir.glob("*.mp3")) and not args.replace:
        parser.error(f"candidates already exist: {candidates_dir}. Pass --replace")
    candidates_dir.mkdir(parents=True, exist_ok=True)
    previews_dir.mkdir(parents=True, exist_ok=True)

    voice = project / "02_audio" / "working" / "voice.wav"
    settings = load_bgm_settings(load_json(SUCCESS_RULES_PATH))
    narration_slice = None
    if voice.is_file():
        start, duration = preview_window(
            audio_duration_seconds(voice),
            defaults.get("preview_start_ratio", 0.6),
            defaults.get("preview_seconds", 30),
        )
        narration_slice = previews_dir / "narration-slice.wav"
        slice_narration(voice, narration_slice, start, duration)
    else:
        print(f"WARNING: no voice track at {voice}. Skipping narration mix previews.")

    print(f"Style      : {style_id}")
    print(f"Candidates : {count} x {length_ms}ms")

    rendered = []
    failures = 0
    for index, spec in enumerate(specs, start=1):
        print(f"  {spec['id']}: generating...")
        try:
            audio = request_music_bytes(
                api_key=api_key,
                prompt=spec["prompt"],
                length_ms=length_ms,
                output_format=output_format,
            )
        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            failures += 1
            print(f"  {spec['id']}: FAILED ({error})")
            continue

        candidate_path = candidates_dir / f"{spec['id']}.mp3"
        candidate_path.write_bytes(audio)

        preview_href = ""
        if narration_slice is not None:
            preview_path = previews_dir / f"mix-{index:02d}.mp3"
            mix_bgm_with_voice(
                voice_audio=narration_slice,
                bgm_audio=candidate_path,
                target_audio=preview_path,
                gain_db=settings.gain_db,
                outro_seconds=0.0,
                outro_gain_db=settings.outro_gain_db,
                fade_out_seconds=settings.fade_out_seconds,
            )
            preview_href = f"../02_audio/bgm/previews/{preview_path.name}"

        rendered.append(
            {
                "id": spec["id"],
                "prompt": spec["prompt"],
                "bgm_href": f"../02_audio/bgm/candidates/{candidate_path.name}",
                "preview_href": preview_href,
            }
        )

    if not rendered:
        print(f"All {failures} candidate(s) failed.")
        return 1

    (bgm_dir / "candidates.json").write_text(
        json.dumps(
            {
                "style_id": style_id,
                "length_ms": length_ms,
                "output_format": output_format,
                "content_hint": content_hint,
                "candidates": rendered,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    review_page = project / "05_review" / "bgm-selection.html"
    review_page.parent.mkdir(parents=True, exist_ok=True)
    review_page.write_text(
        render_selection_page(project.name, rendered), encoding="utf-8"
    )

    print()
    print(f"Generated  : {len(rendered)} candidate(s), {failures} failed")
    print(f"Review page: {review_page}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 테스트가 통과하는지 확인**

Run: `python3 -m pytest tests/test_generate_bgm_candidates.py -v`
Expected: PASS — 6 passed

- [ ] **Step 5: 전체 테스트로 회귀 확인**

Run: `python3 -m pytest tests/ -v`
Expected: PASS — 38 passed (27 + Task 5의 5개 + Task 6의 6개)

- [ ] **Step 6: 최소 비용 스모크 테스트**

후보 1개, 최소 길이(3,000ms)로 실제 API를 한 번만 호출한다. 임시 프로젝트를 만들어 실행하고 끝나면 지운다.

```bash
python3 scripts/new_project.py zz-bgm-smoke --title "BGM 스모크" \
  --production-profile classic_rich_motion_v1 --visual-style dark_cinematic
python3 scripts/generate_bgm_candidates.py projects/zz-bgm-smoke \
  --count 1 --length-ms 3000 --content-hint "테스트"
```

Expected: `Generated  : 1 candidate(s), 0 failed`가 출력되고
`projects/zz-bgm-smoke/05_review/bgm-selection.html`이 생성된다.
음성 파일이 없으므로 `WARNING: no voice track` 경고가 함께 나오는 것이 정상이다.

정리:

```bash
rm -rf projects/zz-bgm-smoke
```

- [ ] **Step 7: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add scripts/generate_bgm_candidates.py tests/test_generate_bgm_candidates.py
git commit -m "feat: generate BGM candidates with narration mix previews"
```

---

### Task 7: `.gitignore`와 문서 반영

생성 미디어가 커밋되지 않게 하고, 새 승인 게이트를 규칙 문서에 남긴다.

**Files:**
- Modify: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `docs/WORKFLOW.ko.md`

**Interfaces:**
- Consumes: Task 4, 6의 CLI
- Produces: 없음 (문서)

- [ ] **Step 1: `.gitignore`에 생성 미디어 경로 추가**

`projects/*/05_review/frames/*` 규칙 아래에 추가한다. `candidates.json`은 재현 기록이므로 추적을 유지한다.

```text
projects/*/02_audio/bgm/candidates/*
projects/*/02_audio/bgm/previews/*
```

- [ ] **Step 2: 무시 규칙이 동작하는지 확인**

```bash
mkdir -p projects/zz-ignore-check/02_audio/bgm/candidates
touch projects/zz-ignore-check/02_audio/bgm/candidates/cand-01.mp3
git status --short projects/zz-ignore-check
rm -rf projects/zz-ignore-check
```

Expected: `git status`에 `cand-01.mp3`가 나타나지 않는다.

- [ ] **Step 3: `AGENTS.md`의 승인 게이트에 BGM 단계 추가**

`## Required Approval Gates`의 7번 항목을 아래 두 줄로 교체한다.

```markdown
7. Generate voice, then create the Hyperframes composition.
8. After the voice review passes, generate BGM candidates and wait for explicit
   BGM approval. Apply the approved track with `scripts/apply_bgm.py`, which
   never re-runs TTS, and extend the composition outro by the configured delay.
```

그리고 같은 절 마지막 문단을 아래로 교체한다.

```markdown
Script approval, visual-style approval, and BGM approval are separate. Do not
silently carry a previous project's style or BGM into a new project.
```

- [ ] **Step 4: `AGENTS.md`의 Standard Commands에 BGM 명령 추가**

`Validate and render:` 블록 바로 앞에 다음 절을 추가한다. 제목은 "Choose and apply BGM (after the voice review passes):"로 하고, 코드 블록에는 아래 세 명령을 넣는다.

```bash
python3 scripts/generate_bgm_candidates.py <project>
python3 scripts/apply_bgm.py <project> --candidate cand-02 --dry-run
python3 scripts/apply_bgm.py <project> --candidate cand-02
```

- [ ] **Step 5: `docs/WORKFLOW.ko.md`에 같은 단계 반영**

음성 생성과 렌더 사이에 BGM 선택 단계를 서술하는 절을 추가한다. 다음 세 가지를 반드시 포함한다.

- 후보 생성 명령과 `05_review/bgm-selection.html`에서 승인한다는 점
- `apply_bgm.py`가 TTS를 재실행하지 않으므로 승인된 자막 타이밍이 유지된다는 점
- BGM 적용 후 오디오가 아웃트로 4초만큼 길어지므로 컴포지션 아웃트로를 연장하고 재렌더해야 한다는 점

- [ ] **Step 6: 문서와 코드가 어긋나지 않는지 확인**

```bash
python3 scripts/apply_bgm.py --help
python3 scripts/generate_bgm_candidates.py --help
```

Expected: `AGENTS.md`에 적은 플래그(`--candidate`, `--dry-run`, `--count`, `--length-ms`, `--content-hint`, `--replace`)가 전부 usage에 존재한다.

- [ ] **Step 7: 커밋** (사용자가 커밋을 요청한 경우에만)

```bash
git add .gitignore AGENTS.md docs/WORKFLOW.ko.md
git commit -m "docs: add BGM approval gate and commands"
```

---

## 완료 기준

- `python3 -m pytest tests/ -v`가 38개 전부 통과한다.
- `python3 scripts/generate_elevenlabs_audio.py --help`가 기존 BGM 플래그 5개를 그대로 보여준다.
- `apply_bgm.py --dry-run`이 실제 프로젝트에서 `음성 길이 + 4초`를 보고한다.
- `git status --short projects/2026-010-sixth-guest`가 비어 있다.
- 생성된 후보 mp3가 `git status`에 나타나지 않는다.
