# 주간 제작 환경 업데이트

점검일: 2026-10-12, 한국 시간. 예약 작업 `hyperframes`.
작업 공간: `/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co`.

## 적용 결과

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| Hyperframes | 0.8.126 | 0.8.149 |
| source-map-js | 1.2.1 | 1.2.2 |
| uv | 0.12.23 | 0.13.0 |
| Homebrew node@22 | 22.23.3_1 | 22.23.3_2 |
| Homebrew python@3.14 | 3.14.8 | 3.14.8_2 |
| Homebrew ffmpeg | 9.0.2 | 9.0.2_1 |
| filelock | 4.0.10 | 4.1.1 |
| hf-xet | 1.6.0 | 1.7.0 |
| huggingface-hub | 2.1.1 | 2.2.0 |
| iniconfig | 2.3.0 | 2.3.1 |
| NumPy | 2.5.3 | 2.5.4 |

Node의 실제 런타임은 `22.23.3`, npm은 `10.9.9`, Python은 `3.14.8`,
FFmpeg/ffprobe는 `9.0.2`로 유지됩니다. Homebrew 세 항목은 같은 버전의
빌드 리비전 갱신입니다. 공식 formula가 요구하는 OpenSSL 4.0.3을 추가하고
simdjson을 5.0.0에서 5.0.3으로 갱신했습니다.

MLX·mlx-metal 0.32.3, mlx-whisper 0.4.3, python-dotenv 1.2.4,
pytest 9.1.1, pip 26.2.1, setuptools 84.0.0, canvas 3.2.3은
조회 시 최신 안정 버전이므로 유지했습니다. 기존 환경에 이미 설치되어 있던
Pillow 12.3.0도 잠금 파일에 포함해 재설치 시 보존합니다.
`requirements.lock`은 실제 설치된 43개 패키지를 고정하며 기본
`requirements.txt`의 네 직접 의존성은 변경할 필요가 없었습니다.

mpmath 최신 1.4.1은 SymPy 1.14.0의 `mpmath>=1.1.0,<1.4` 조건과
충돌하므로 1.3.0을 유지합니다. Node 메이저와 명시적으로 고정된 Python
3.14.8은 변경하지 않았습니다. [Node 공식 지원 일정](https://github.com/nodejs/Release/blob/main/schedule.json)에
따라 Node 22의 지원 종료 예정일은 2027-04-30입니다.

## 변경 내용과 공식 근거

- Hyperframes 최신 안정 릴리스를 npm 레지스트리와
  [공식 릴리스](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.149)에서 대조했습니다.
  이번 범위에는 [미리보기 검은 화면 및 스트림 시작 시점이 다른 영상의 A/V 싱크 수정](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.148),
  [렌더 정체 단계 진단 개선](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.147)이 포함됩니다.
  새 전사·배경 제거 API는 이번 점검에서 호출하지 않았습니다.
- 기존 npm 검사에서 고위험 취약점 1건을 확인했습니다.
  [source-map-js의 서비스 거부 취약점](https://github.com/advisories/GHSA-68fv-2mgg-jv7q)을
  호환되는 1.2.2로 수정했으며 최종 `npm audit` 결과는 0건입니다.
- [uv 0.13.0 공식 변경 기록](https://github.com/astral-sh/uv/releases/tag/0.13.0)은
  기본 Python 다운로드 대상을 3.15로 변경합니다. 기존 `.python-version`과
  `--python 3.14.8`을 유지한 새 환경 생성 및 잠금 설치를 검증했습니다.
  이 저장소는 변경된 제약 파일·해시·빌드 정리 옵션을 사용하지 않습니다.
- [NumPy 2.5.4](https://github.com/numpy/numpy/releases/tag/v2.5.4)는
  Python 3.12~3.15를 지원하는 수정 릴리스입니다.
  MLX, NumPy, Numba, Torch의 실제 import와 연산을 함께 확인했습니다.
- [Hugging Face Hub 2.2.0](https://github.com/huggingface/huggingface_hub/releases/tag/v2.2.0),
  [hf-xet 1.7.0](https://github.com/huggingface/xet-core/releases/tag/v1.7.0),
  [filelock 4.1.1](https://github.com/tox-dev/filelock/releases/tag/4.1.1)의 변경을 확인했습니다.
  Hub의 작업 통계 스트리밍 기본값·예외 형식 변경은 이 제작 경로에서 사용하지 않습니다.
  43개 Python 배포의 안정 버전은 [PyPI JSON API](https://docs.pypi.org/api/json/)로 조회했고
  개별 결과를 측정 요약에 기록했습니다.
- Homebrew의 [node@22](https://formulae.brew.sh/formula/node@22),
  [python@3.14](https://formulae.brew.sh/formula/python@3.14),
  [ffmpeg](https://formulae.brew.sh/formula/ffmpeg), [uv](https://formulae.brew.sh/formula/uv)
  메타데이터와 설치 bottle을 대조했습니다. 지정한 네 formula와 필수 의존성만 갱신했습니다.

## ElevenLabs V4 확인

인증된 읽기 전용 `GET /v1/models`는 HTTP 200을 반환했습니다.
`eleven_v4`가 목록에 있고 TTS 지원이 활성화되어 있으며, 무료·구독 요청의
최대 텍스트 길이는 각각 10,000자입니다. 모델 목록 확인은 실제 유료 합성의
품질이나 성공을 검증하는 요청은 아닙니다.

[ElevenLabs 공식 voice settings 자료](https://github.com/elevenlabs/plugin/blob/main/skills/general/text-to-speech/references/voice-settings.md)는
V4에서 Stability와 Similarity만 지원하고 SSML을 지원하지 않는다는 기존 기준과
일치합니다. `eleven_v4`, Stability 0.5, Similarity 0.75, 본편 1.00배속,
절제된 태그·문장 단위 순차 청크 방침을 유지합니다. API 요청기와 제작 스킬에
반영할 새로운 설정 변경은 없었습니다. 유료 TTS·이미지·음악 생성은 0회입니다.

## 검증

| 검증 | 결과 |
| --- | --- |
| 격리 Python 후보의 자동 테스트 | 63 passed |
| 적용 후 프로젝트 자동 테스트 | 63 passed |
| 적용 후 Python 의존성 검사 | 43개 호환 |
| uv 0.13.0 새 환경 및 잠금 파일 전체 설치 | Python 3.14.8, 43개 호환 |
| MLX Metal 실제 연산 | GPU, 제곱합 328350 |
| NumPy·Numba 실제 연산, Torch·SSL import | 성공, OpenSSL 4.0.3 |
| 기존 로컬 10초 음성의 Whisper 정렬 | 후보·최종 모두 100%, 기준 92% |
| npm 보안 검사 | 고위험 1건 → 전체 0건 |
| 가로·세로 Hyperframes lint | 각각 오류 0, 경고 0 |
| 가로 렌더 | 1920×1080, 60fps, 180프레임, 3초 |
| 세로 렌더 | 1080×1920, 60fps, 180프레임, 3초 |
| 각 렌더의 스트림 | H.264/AAC, 비디오·오디오 각각 3.000초 |
| drawElement 자체 프레임 검증 | 두 방향 통과 |
| 1초 이상 freeze/black 검출 | 두 방향 없음 |
| canvas 자막 샘플 | 1920×1080, 60fps, 180프레임, A/V 각각 3.000초 |

Whisper는 기존 실험 음성을 복사해 `mlx-community/whisper-large-v3-turbo`로
오프라인 정렬했습니다. 승인 원고와 원본 음성은 수정하지 않았습니다.
이 검사는 타이밍·호환성 확인이며 음색의 주관적 청취 검수를 뜻하지 않습니다.

격리 npm 후보로 두 방향을 렌더한 뒤, Homebrew와 프로젝트 설치를 마친
최종 환경으로 두 방향을 다시 렌더했습니다. 각 방향의 0·1.5·2.95초 프레임을
개별 확인해 한국어 표시, 화면 여백, 원의 이동·크기 변화, 진행 막대를 검수했습니다.
최종 환경의 해당 여섯 프레임은 검수한 후보 프레임과 해시가 모두 일치했습니다.
canvas 자막은 실제 표시되는 0.8·2.7초 프레임에서 한글·외곽선·위치를
확인했습니다. 1.5초의 미표시는 두 숫자 발화 사이의 정상적인 자막 공백입니다.
이번 3초 실험은 완료 영상 전체를 재검수한 것으로 간주하지 않습니다.

## 보존 및 복구

시작 시 브랜치는 `main`, HEAD는 `44f3a13`이며 기존 Git 상태 297개 항목이
모두 유지되는 것을 확인했습니다. 삭제된 007~009, 미추적 제작 자산,
완료 프로젝트 025~028, 별도 Remotion 저장소를 수정하지 않았습니다.
점검 시작 시 제작·음성 생성·렌더·다른 설치 프로세스는 없었습니다.

`tmp/maintenance/2026-10-12/backups/`에 변경 전 package·잠금 파일,
Python 전체 버전, Homebrew 설치 목록, Git 상태, 인터프리터 경로를 보관했습니다.
Homebrew 설치에는 `HOMEBREW_NO_INSTALL_CLEANUP=1`을 사용해 이전 keg를
보존했습니다. 실패한 업데이트나 복구가 필요한 변경은 없었습니다.

Homebrew 전체 cask 목록 조회는 기존 외부 탭의 새 신뢰 규칙 때문에 거부되어
공식 formula 목록으로 다시 기록했습니다. 외부 탭 신뢰를 추가하거나 제거하지
않았으며 해당 탭의 패키지는 이번 갱신 대상에 포함하지 않았습니다.
`prebuild-install`의 기존 유지보수 중단 경고는 남아 있지만 canvas 네이티브
모듈과 실제 자막 생성이 성공했고 npm 보안 검사는 0건입니다.

설치와 검증 로그·미디어는 `tmp/maintenance/2026-10-12/`와
`experiments/2026-10-12-toolchain-update/`에 로컬 보관합니다.
Git에는 잠금 파일, 실행 안내, 이 기록 및 측정 자료만 포함합니다.
외부 업로드는 하지 않았습니다. [측정 요약](2026-10-12-toolchain-update.json).

## 재현

```bash
uv venv --python 3.14.8 .venv
uv pip sync --python .venv/bin/python --link-mode copy requirements.lock
uv pip check --python .venv/bin/python
npm ci
npm audit
.venv/bin/python -m pytest -q
```

기존 환경에 대한 첫 줄은 재생성을 위한 예시이며 제작 중에 실행하지 않습니다.
격리 후보와 렌더 로그의 정확한 실행 경로는 측정 요약 및 로컬 점검 폴더에 보관합니다.
