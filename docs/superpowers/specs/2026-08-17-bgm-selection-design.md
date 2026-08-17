# BGM 선택 및 적용 기능 설계

- 작성일: 2026-08-17
- 대상 저장소: `Hyperframes-codex`
- 상태: 설계 승인됨, 구현 계획 대기

## 배경

`config/success-rules.json`의 `audio_rules.bgm`은 BGM 규칙을 완전히 정의하고 있고
(`enabled: true`, 루프, 더킹 `-18dB`, 아웃트로 `4초`, 페이드아웃 `3초`),
`scripts/generate_elevenlabs_audio.py`의 `mix_bgm_with_voice()`가 그 규칙을 이미 구현하고 있다.
voice-only 마스터 보존도 구현되어 있다.

빠져 있는 것은 두 가지다.

1. **음원을 고르는 단계가 없다.** `library/audio/music/`에는 30초짜리 파일 하나뿐이고,
   프로젝트에 어울리는 BGM을 정하는 절차가 존재하지 않는다.
   실제로 `2026-010-sixth-guest`는 `elevenlabs-request.json`의 `bgm.source`가 `null`인 채로
   "공포 BGM은 목소리 원본 검수 후 별도로 선택한다"는 메모만 남기고 납품되었다.

2. **이미 만든 음성에 BGM만 얹을 수 없다.** 믹싱이 TTS 생성 경로 안에서만 실행되므로
   (`generate_elevenlabs_audio.py`가 항상 ElevenLabs TTS를 먼저 호출한 뒤 믹싱한다),
   BGM을 붙이려면 19분 음성을 통째로 재생성해야 한다. 비용 문제에 더해, 새 테이크가 나오면
   승인된 자막 타이밍과 개별 복구한 청크가 모두 무효가 된다.

## 목표

- 프로젝트 내용과 승인된 비주얼 스타일에 맞는 BGM 후보를 자동으로 생성한다.
- 후보를 실제 더킹 상태로 비교 청취하고 하나를 승인할 수 있게 한다.
- 승인된 BGM을 **TTS 재생성 없이** 기존 음성에 적용한다.
- 기존 믹싱 규칙과 설정 체계(`elevenlabs-request.json`의 `bgm` 블록)를 그대로 사용한다.

## 비목표

- 구간별 BGM 전환(도입/긴장/반전마다 다른 트랙). 필요해지면 별도 설계로 다룬다.
- Shorts 전용 BGM. 동일 로직을 재사용할 수 있으나 이번 범위 밖이다.
- 로컬 음원 카탈로그 구축. 조달은 ElevenLabs Music API 생성으로 한다.
- `2026-010-sixth-guest` 본편. BGM 없이 확정하기로 결정되었다.

## 사용자 흐름

1. 음성 생성과 자막 정렬이 끝나고 음성 검수를 통과한다.
2. `generate_bgm_candidates.py`를 실행한다. 후보 4개와 비교 청취 페이지가 만들어진다.
3. 사용자가 `05_review/bgm-selection.html`에서 후보를 듣고 하나를 고른다.
4. `apply_bgm.py`로 승인된 후보를 적용한다. 음성이 아웃트로 4초만큼 길어진다.
5. 컴포지션의 아웃트로 구간을 4초 연장하고 재렌더한다.

BGM 승인은 대본 승인, 비주얼 스타일 승인과 **별개의 게이트**다.
`AGENTS.md`의 승인 게이트 구조에 하나가 추가되는 셈이다.

## 구성 요소

| 파일 | 신규/수정 | 역할 |
|---|---|---|
| `config/bgm-presets.json` | 신규 | 비주얼 스타일별 BGM 프롬프트 프리셋과 생성 기본값 |
| `scripts/audio_mixing.py` | 신규 | `mix_bgm_with_voice()`, `audio_duration_seconds()`를 옮겨 공유 |
| `scripts/generate_bgm_candidates.py` | 신규 | 후보 생성, 믹스 미리듣기, 비교 페이지 생성 |
| `scripts/apply_bgm.py` | 신규 | 승인된 후보를 기존 음성에 믹싱하고 설정을 갱신 |
| `scripts/generate_elevenlabs_audio.py` | 수정 | 믹싱 함수를 `audio_mixing.py`에서 import하도록 변경 |

`generate_elevenlabs_audio.py` 수정은 함수를 옮기고 import로 바꾸는 것뿐이며 동작은 바뀌지 않는다.
`render_project.py`와 캡션 렌더러는 건드리지 않는다.

## 데이터 흐름

```text
00_brief/brief.md
01_script/narration.txt
04_composition/profile.json      ─┐
config/bgm-presets.json           ├→ generate_bgm_candidates.py
config/success-rules.json        ─┘        │
                                           ├→ 02_audio/bgm/candidates/cand-01..04.mp3
                                           ├→ 02_audio/bgm/previews/mix-01..04.mp3
                                           ├→ 02_audio/bgm/candidates.json
                                           └→ 05_review/bgm-selection.html
                                                       ↓ 사용자 승인
02_audio/working/voice.wav (voice-only, 보존)
02_audio/bgm/candidates/cand-NN.mp3        ─┐
config/success-rules.json                   ├→ apply_bgm.py
02_audio/elevenlabs-request.json           ─┘        │
                                                     ├→ 02_audio/working/voice-bgm.wav
                                                     ├→ 04_composition/assets/audio/voice.wav (교체)
                                                     └→ 02_audio/elevenlabs-request.json (bgm.source 갱신)
```

`02_audio/working/voice.wav`는 절대 덮어쓰지 않는다. 이것이 voice-only 마스터다.
컴포지션이 참조하는 `04_composition/assets/audio/voice.wav`만 믹스본으로 교체한다.

## 디렉터리 규약

```text
02_audio/bgm/
  candidates/cand-01.mp3 ... cand-04.mp3   생성된 BGM 후보 (각 40초)
  previews/mix-01.mp3 ... mix-04.mp3       내레이션 30초 + 더킹 믹스
  candidates.json                          프롬프트, 생성 시각, 파라미터 기록
05_review/bgm-selection.html               비교 청취 페이지
```

`02_audio/bgm/candidates/`와 `02_audio/bgm/previews/`는 생성 미디어이므로 `.gitignore`에 추가한다.
`candidates.json`은 재현에 필요한 기록이므로 추적한다.

## `config/bgm-presets.json` 스키마

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
    "dark_cinematic": {
      "label_ko": "다크 시네마틱",
      "base_prompt": "낮은 서브 드론과 지속되는 불협 현악, 멀리서 들리는 겨울 바람. 느리고 일정한 긴장. 보컬 없음, 갑작스러운 큰 스팅어 없음, 드럼 비트 없음.",
      "variation_hints": [
        "현악 중심, 활 긁는 질감을 조금 더",
        "드론 중심, 거의 정적에 가깝게",
        "금속성 울림과 미세한 하모닉스 추가",
        "낮은 피아노 단음을 드문드문"
      ]
    }
  }
}
```

- `base_prompt`는 스타일 고유의 고정 성격이다.
- `variation_hints`는 후보마다 하나씩 붙여 서로 다른 후보를 만든다.
  `candidate_count`는 해당 스타일의 `variation_hints` 개수를 넘을 수 없다.
- `preview_start_ratio`는 미리듣기로 쓸 내레이션 구간의 시작 지점이다.
  전체 길이의 60% 지점에서 30초를 잘라 쓴다. 도입부보다 본론이 실제 체감에 가깝다.
- 스타일 키는 `config/visual-styles.json`의 키와 일치해야 한다.
  프리셋에 없는 스타일이면 오류로 종료한다.

초기 구현에서는 `config/visual-styles.json`에 존재하는 9개 스타일 전부에 대해
`base_prompt`와 `variation_hints` 4개씩을 채운다.

## 프롬프트 구성 규칙

최종 프롬프트는 다음을 순서대로 이어 붙인 하나의 문자열이다.

1. 해당 스타일의 `base_prompt`
2. 후보별 `variation_hints[i]`
3. 프로젝트 내용 보정어

내용 보정어는 `--content-hint` 인자로 받는다. 넘기지 않으면 `00_brief/brief.md`의
첫 문단을 쓴다. 프롬프트 전문은 `candidates.json`에 그대로 기록해 재현 가능하게 한다.

ElevenLabs Music API는 부정 프롬프트를 별도 파라미터로 받지 않으므로,
피해야 할 요소("보컬 없음", "드럼 비트 없음")는 `base_prompt` 문장 안에 자연어로 포함한다.

## CLI 인터페이스

```bash
python3 scripts/generate_bgm_candidates.py <project> \
  [--count 4] [--length-ms 40000] [--content-hint "<한 문장>"] [--replace]

python3 scripts/apply_bgm.py <project> --candidate cand-02 \
  [--outro-seconds 4] [--gain-db -18] [--dry-run]
```

`--dry-run`은 예상 결과 길이와 적용될 파라미터만 출력하고 파일을 쓰지 않는다.
기존 `render_project.py`가 `--dry-run`을 제공하는 방식과 맞춘다.

## ElevenLabs Music API 사용

- 엔드포인트: `POST https://api.elevenlabs.io/v1/music`
- 인증: `ELEVENLABS_API_KEY` 환경변수. 저장소에 키를 두지 않는다.
- 본문: `prompt`, `music_length_ms`
- 쿼리: `output_format`
- `music_length_ms` 허용 범위는 3,000~600,000ms이다. 범위를 벗어나면 요청 전에 오류로 종료한다.

10분 상한 때문에 19분 영상을 한 번에 생성할 수 없다. 40초 후보를 만들고
믹싱 시 `-stream_loop -1`로 반복하는 방식이 이 제약을 자연스럽게 해결한다.
`success-rules.json`의 `loop_to_voice_length: true`와도 일치한다.

## 믹싱 규칙

값은 모두 `config/success-rules.json`의 `audio_rules.bgm`에서 읽는다.
CLI 인자로 넘기면 그것이 우선한다.

| 항목 | 값 |
|---|---|
| 음성 구간 BGM 게인 | `-18dB` |
| 아웃트로 길이 | `4초` (기본값으로 확정) |
| 아웃트로 구간 BGM 게인 | `-14dB` |
| 페이드아웃 | 마지막 `3초` |
| 루프 | 음성 길이 + 아웃트로까지 반복 |

구현은 기존 `mix_bgm_with_voice()`를 그대로 재사용한다. 필터 체인을 새로 쓰지 않는다.

## 컴포지션 길이 처리

BGM 적용 후 오디오는 아웃트로만큼 길어진다. 예: 1153.03초 → 1157.03초.

`apply_bgm.py`는 다음을 수행한다.

- `04_composition/index.html`의 voice `<audio>` 요소 `data-duration` 속성을 새 길이로 갱신한다.
- 새 총 길이와 "아웃트로 구간을 4초 연장해야 함"을 표준 출력에 명시한다.

모션 타임라인 자체는 자동으로 늘리지 않는다. 마지막 장면의 연장은 연출 판단이 필요하므로
사람이 처리한다. 자막은 음성 종료 전에 끝나므로 영향을 받지 않는다.

## 비교 청취 페이지

`05_review/bgm-selection.html`은 정적 HTML이다. 후보마다 한 행을 차지한다.

- 후보 번호와 사용된 프롬프트 전문
- BGM 단독 재생 플레이어
- 내레이션 더킹 믹스 재생 플레이어
- 적용 명령을 복사할 수 있는 코드 블록 (`apply_bgm.py <project> --candidate cand-02`)

선택 버튼이나 서버 통신은 두지 않는다. 사용자가 듣고 명령을 복사해 실행하는 방식이
기존 `youtube-publish.html`의 복사 버튼 방식과 같은 결이다.

## 에러 처리

| 상황 | 동작 |
|---|---|
| `ELEVENLABS_API_KEY` 없음 | 환경변수 이름을 알려주고 종료 |
| 후보 디렉터리가 이미 있음 | `--replace` 없으면 종료 |
| 프리셋에 해당 스타일 없음 | 사용 가능한 스타일 목록을 출력하고 종료 |
| `--count`가 `variation_hints` 개수 초과 | 사용 가능한 최대 개수를 알려주고 종료 |
| 후보 1개 생성 실패 | 해당 후보만 건너뛰고 계속. 마지막에 실패 개수를 보고 |
| 후보 전부 실패 | 종료 코드 1 |
| `music_length_ms` 범위 밖 | 요청 전 검증해 종료 |
| `voice.wav` 없음 | 음성 생성 단계를 먼저 거치라는 안내와 함께 종료 |
| 지정한 후보 파일 없음 | 존재하는 후보 목록을 출력하고 종료 |

부분 실패를 조용히 넘기지 않는다. 성공/실패 개수를 항상 출력한다.

## 검증 방법

`apply_bgm.py`는 외부 API를 호출하지 않으므로 오프라인으로 검증할 수 있다.

1. 기존 `projects/2026-010-sixth-guest/02_audio/working/voice.wav`와
   `library/audio/music/midnight-library.mp3`를 입력으로 임시 출력 경로에 믹싱한다.
2. `ffprobe`로 결과 길이가 `음성 길이 + 4초`인지 확인한다.
3. `volumedetect`로 클리핑이 없는지, 아웃트로 구간에 BGM이 남아 있는지 확인한다.
4. 원본 `voice.wav`가 수정되지 않았음을 확인한다.

`generate_bgm_candidates.py`는 후보 1개, 최소 길이(3,000ms)로 스모크 테스트한다.
비용을 줄이기 위해 전체 4개 생성은 실제 사용 시점에만 한다.

2026-010 프로젝트 파일은 검증 중에도 수정하지 않는다. 출력은 임시 경로로만 보낸다.

## 확인이 필요한 외부 사항

Eleven Music으로 생성한 음원을 YouTube 수익화 영상에 쓸 수 있는지는 계정 플랜의
라이선스 조항에 달려 있다. 구현 전에 사용 중인 플랜에서 상업적 이용 범위를 확인해야 한다.
이 설계는 라이선스가 허용된다는 전제 위에 있다.
