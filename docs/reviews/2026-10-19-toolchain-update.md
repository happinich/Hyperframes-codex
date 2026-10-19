# 주간 제작 환경 업데이트 · 2026-10-19

예약 작업 `hyperframes`. 작업 공간 `/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co`.
기존 AGENTS·성공 규칙·실행 문서 및 2026-10-12 검증 기록을 읽고 설치·제작 충돌을
확인한 뒤, 격리 후보 검증 → 적용 → 최종 설치 검증 순으로 진행했다.
시작 시 제작·렌더·음성 생성·다른 설치 프로세스는 발견되지 않았다.

## 적용 결과

| 도구 | 이전 | 적용 |
| --- | --- | --- |
| Hyperframes | 0.8.149 | 0.8.173 |
| uv | 0.13.0 | 0.13.1 |
| Homebrew node@22 빌드 | 22.23.3_2 | 22.23.3_3 |

Node 실제 런타임 22.23.3·npm 10.9.9, Python 3.14.8_2(런타임 3.14.8),
FFmpeg/ffprobe 9.0.2_1(런타임 9.0.2), canvas 3.2.3은 유지했다.
공식 formula에서 Python과 FFmpeg에 새 안정 버전·리비전이 없음을 확인했다.
Node는 현재 지원되는 22 메이저를 유지한다.
[공식 지원 일정](https://github.com/nodejs/Release/blob/main/schedule.json)의
22 계열 종료 예정일은 2027-04-30이다. 메이저 변경은 수행하지 않았다.

Homebrew가 Node의 필수 의존성으로 simdjson 5.0.3→5.0.5,
simdutf 9.2.1_1→9.3.2, SQLite 3.53.4→3.54.1을 함께 갱신했다.
Python·Node의 메모리 SQLite 쿼리와 Python SSL·연산도 적용 후 확인했다.

### Python 패키지

| 패키지 | 이전 | 적용 |
| --- | --- | --- |
| mlx | 0.32.3 | 0.32.4 |
| filelock | 4.1.1 | 4.2.2 |
| certifi | 2026.7.22 | 2026.10.18 |
| pluggy | 1.6.0 | 1.7.0 |
| httpx2 | 2.13.1 | 2.14.0 |
| truststore | 0.10.4 | 0.10.5 |
| pillow | 12.3.0 | 13.0.0 |
| httpcore2 | 2.13.1 | 2.14.0 |
| more-itertools | 11.1.0 | 11.2.1 |
| mlx-metal | 0.32.3 | 0.32.4 |

MLX·mlx-metal은 같은 버전으로 맞췄다. mlx-whisper 0.4.3,
python-dotenv 1.2.4, pytest 9.1.1, pip 26.2.1 등 나머지 설치 버전은 유지했다.
PyPI에서 설치된 43개 배포를 확인하고 후보의 Python 요구 범위·비실험 안정 배포를
대조했다. `requirements.txt`의 MLX 두 항목과 전체 `requirements.lock`을 동기화했다.
개발 직접 의존성은 갱신이 필요 없었다.

mpmath 최신 1.4.1은 SymPy 1.14.0의 `<1.4` 조건과 충돌하므로 1.3.0을 유지했다.

### npm 패키지

Hyperframes와 함께 16개 하위 패키지를 허용된 의존 범위 안에서 갱신했다.
안정 배포의 자체 의존 관계를 사용했으며 실험 옵션을 활성화하거나 상위 패키지의
범위를 강제하는 override를 추가하지 않았다.

| 패키지 | 이전 | 적용 |
| --- | --- | --- |
| @hono/node-server | 2.1.3 | 2.1.5 |
| @puppeteer/browsers | 3.2.3 | 3.2.5 |
| @swc/helpers | 0.5.21 | 0.5.23 |
| bundle-name | 4.1.0 | 4.1.1 |
| chromium-bidi | 17.0.2 | 157.0.8090-0 |
| default-browser | 5.5.0 | 5.5.1 |
| devtools-protocol | 0.0.1687809 | 0.0.1696802 |
| giget | 3.2.0 | 3.3.1 |
| hyperframes | 0.8.149 | 0.8.173 |
| modern-tar | 0.8.5 | 0.8.6 |
| nanoid | 3.3.19 | 3.3.20 |
| node-abi | 3.97.0 | 3.99.0 |
| postcss | 8.5.28 | 8.5.31 |
| prettier | 3.8.3 | 3.9.10 |
| puppeteer-core | 25.12.0 | 25.14.0 |
| webdriver-bidi-protocol | 0.4.3 | 1.0.1 |
| zod | 3.25.76 | 4.6.7 |

`chromium-bidi`의 `-0`은 안정 Puppeteer가 지정하는 Chromium 프로토콜 빌드 표기다.
별도 실험 채널이나 베타 Puppeteer를 선택한 것이 아니다. 패키지의 공식 의존 관계와
Node 요구 범위(현재 Puppeteer는 >=22.12.0)를 대조하고 실제 렌더를 확인했다.
최종 `npm outdated --all`에서 설치된 패키지의 current/wanted 불일치는 없다.
상위 패키지 범위 밖의 esbuild·canvas 애드온·기타 메이저는 강제하지 않았다.

## 공식 변경 내용과 호환성 판단

- [Hyperframes 0.8.173](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.173)은
  CDN 대기 처리와 비정수 원본 프레임레이트 출력 등을 수정한다. 이번 범위의
  [0.8.167](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.167)은 긴 프로젝트의
  미리보기 부하·메모리 동작을 개선하고,
  [0.8.172](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.172)은 오디오 파일
  탐색과 씬 밖 SVG grain 노출을 수정한다. 이번 점검은 3초 렌더이며 장편 성능 개선율을
  직접 측정하거나 기존 앱 재시작 현상의 해결을 보장한 검사는 아니다.
- [uv 0.13.1](https://github.com/astral-sh/uv/releases/tag/0.13.1)은 파일 저장·동시 설치와
  잠금 관련 처리를 개선한다. 기본 Python 다운로드 대상은 여전히 3.15이므로
  `.python-version`과 `--python 3.14.8`을 유지한다. 이 버전의 `uv pip check`는
  Requires-Python 상한을 무시하므로 별도로 metadata·packaging 기반 상·하한 및
  활성 의존 범위를 43개 모두 검증했다. preview 옵션은 사용하지 않았다.
- [MLX 0.32.4](https://github.com/ml-explore/mlx/releases/tag/v0.32.4)는 Metal 메모리·배열
  연산 등을 수정한다. 실제 Metal 연산과 오프라인 Whisper 정렬로 기존 경로를 검증했다.
- [Pillow 13.0.0](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html)은 보안
  수정과 API 제거를 포함한다. 제거된 I 모드 PNG의 암묵적 클리핑·일부 내부 API를
  제작 스크립트가 사용하지 않음을 검색하고 RGB/RGBA 변환·확대·그리기·PNG 저장과
  재열기를 격리·최종 환경에서 확인했다. Python 3.14는 지원 범위다.
- [Puppeteer 변경 기록](https://pptr.dev/CHANGELOG)은 프로세스 종료·네트워크·가시성
  처리 수정을 포함한다. 공식 패키지의 의존 범위로 브라우저 도구를 갱신하고
  Hyperframes가 실제 사용하는 기존 HeadlessChrome 152.0.7977.30으로 검증했다.
  일반 사용자의 Chrome 앱을 갱신한 것은 아니다.
- [filelock](https://github.com/tox-dev/py-filelock/releases/tag/4.2.2)의 상대 경로 잠금,
  [truststore](https://github.com/sethmlarson/truststore/releases/tag/v0.10.5)의 TLS 동시성,
  [pluggy](https://pluggy.readthedocs.io/en/latest/changelog.html)의 Python 3.14 훅 처리를
  확인했다. [httpx2](https://github.com/pydantic/httpx2/blob/main/src/httpx2/CHANGELOG.md)·
  [httpcore2](https://github.com/pydantic/httpx2/blob/main/src/httpcore2/CHANGELOG.md)는 프록시·
  연결 처리 수정을 포함한다. [certifi](https://github.com/certifi/python-certifi/releases/tag/2026.10.18)의
  CA 목록 변경도 확인했다. [more-itertools](https://github.com/more-itertools/more-itertools/releases/tag/v11.2.1)는
  패키징 수정이다. 최종 환경의 HTTPS GET과 테스트가 통과했다.
- [Hono](https://github.com/honojs/node-server/releases/tag/v2.1.5)는 HTTP/2 종료·정적
  요청 처리를, [PostCSS](https://github.com/postcss/postcss/releases/tag/8.5.31)는 소스맵을,
  [Prettier](https://github.com/prettier/prettier/releases/tag/3.9.10)는 Markdown 표 처리를
  수정한다. 나머지 npm 후보도 공식 레지스트리의 배포·의존 조건을 확인하고 동일
  lint·렌더·보안 검사 경로로 검증했다. 세부 메타데이터와 원문은 로컬 점검 폴더에 있다.

## ElevenLabs V4

인증된 읽기 전용 `GET /v1/models`가 HTTP 200을 반환했고 `eleven_v4`의
TTS 지원과 구독 요청 최대 10,000자를 확인했다.
[공식 voice settings 자료](https://github.com/elevenlabs/plugin/blob/main/skills/general/text-to-speech/references/voice-settings.md)는
Stability·Similarity만 사용하고 SSML·Style·Speed·Speaker Boost를 보내지 않는 기존
기준과 일치한다. 해당 공식 예시의 V4 TTS 경로와
[TTS API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)도 대조했다.
[모델 개요](https://elevenlabs.io/docs/overview/models)는 대화 API도 안내하지만 기존 TTS
지원 중단의 근거로 해석하지 않았다.

`eleven_v4`, Stability 0.5, Similarity 0.75, 본편 1.00배속, 절제된 태그·문장 단위
순차 청크를 유지했다. 신규 합성을 하지 않았으므로 생성 품질·음색의 청취 통과를
의미하지 않는다. 요청기·제작 스킬에 반영할 새 V4 설정 변경은 없었다.
제작 스킬에는 이번에 바뀐 도구 버전의 오래된 고정 표기가 없어 재작성하지 않았다.

## 최종 검증

| 항목 | 결과 |
| --- | --- |
| 격리 Python 자동 테스트 | 69 passed |
| 최종 Python 자동 테스트 | 69 passed |
| Python 호환성 | 43개, 활성 의존 및 Python 상·하한 대조 통과 |
| MLX Metal 제곱합 | GPU, 328350 |
| NumPy·Numba·Torch·SSL | 성공 |
| Pillow RGB/RGBA PNG 경로 | 성공 |
| Python·Node SQLite | 성공 |
| 후보·최종 Whisper 정렬 | 기존 로컬 10초 음성, 각각 100% (기준 92%) |
| 후보·최종 npm 보안 검사 | 모두 0건 |
| 후보·최종 가로·세로 lint | 모두 오류 0, 경고 0 |
| 최종 가로 렌더 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 최종 세로 렌더 | 1080×1920, 60fps, H.264/AAC, 180프레임 |
| 영상·음성 길이 | 세 출력 모두 각각 3.000초 |
| drawElement 자체 프레임 검증 | 가로·세로 통과 |
| 1초 이상 freeze/black | 세 출력 모두 없음 |
| canvas 자막 샘플 | 1920×1080, 60fps, 180프레임, 한글 표시 성공 |

전체 하위 npm 의존성 검사에서 추가 후보를 확인해 갱신했으므로, 그 최종 잠금으로
격리 렌더와 실제 설치 후 렌더·canvas 검사를 다시 수행했다.
가로·세로 각각 0·1.5·2.95초 여섯 프레임을 개별 시각 확인해 한글·여백·원의
이동·크기·진행 막대를 확인했다. canvas 0.8·2.7초에서 한글·외곽선·위치를,
1.5초에서 발화 사이의 정상 공백을 확인했다. 테스트용 3초 화면이며 제작 영상이나
새 쇼츠의 승인·전체 검수를 대체하지 않는다. 원본 음성은 복사본만 사용했고
Whisper는 오프라인 모델 캐시로 정렬했다.

## 보존·복구·저장

시작 브랜치 `main`, HEAD `4210af6`. 기존 Git 상태 526개 항목을
그대로 보존했다. 완료 프로젝트·승인 원고·원본 음성·생성 미디어·별도 Remotion
저장소는 변경하지 않았다. 유료 TTS·이미지·음악 생성 및 업로드는 모두 0회다.

`tmp/maintenance/2026-10-19/backups/`에 변경 전 설정·잠금 파일, 전체 Python 버전,
Homebrew 목록, Git 상태를 보관했다. `HOMEBREW_NO_INSTALL_CLEANUP=1`로 기존
keg를 남겼다. 실패한 적용이나 복구가 필요한 변경은 없다. 외부 tap 신뢰 경고는
기존 상태로 남기고 신뢰 범위를 변경하지 않았다. 설치·출력·프레임 검증 로그는
같은 날짜의 로컬 점검 폴더와 실험 폴더에 보관한다.

requirements·잠금 파일·실행 문서·검증용 텍스트 입력과 이 기록만 관련 커밋에 포함한다.
비밀정보·원본 API 응답 전체·생성 미디어는 커밋하지 않는다.
[측정 요약](2026-10-19-toolchain-update.json).

## 재현

```bash
uv venv --python 3.14.8 .venv
uv pip sync --python .venv/bin/python --link-mode copy requirements.lock
uv pip check --python .venv/bin/python
npm ci
npm audit
.venv/bin/python -m pytest -q
```

첫 명령은 새 환경 재생성 예시이며 제작 중에는 실행하지 않는다. Python 요구 범위의
상한은 uv 검사만으로 통과시키지 않고 별도로 대조한다. 이번 사용한 검증 스크립트·
정확한 명령과 결과는 로컬 점검 폴더에 보관한다.
