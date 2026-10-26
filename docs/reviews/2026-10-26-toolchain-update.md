# 주간 제작 환경 업데이트 · 2026-10-26

자동화 `hyperframes` · 기록 시각 2026-10-26T09:10:46+09:00 · 브랜치 `main`, 시작 HEAD `0020318`.
AGENTS, 성공 규칙, WORKFLOW와 2026-10-19 검증 기록을 먼저 읽었다. 시작 시 렌더·음성 생성·다른 설치 프로세스는 없었다. 기존 Git 상태 526항목을 보존했다.

## 적용한 안정 버전

| 도구 | 이전 | 적용 |
| --- | --- | --- |
| Hyperframes | 0.8.173 | 0.8.200 |
| Node.js (22 계열 유지) | 22.23.3 | 22.23.4 |
| Homebrew Python | 3.14.8_2 | 3.14.9 |
| 프로젝트 Python | 3.14.8 | 3.14.9 |
| uv | 0.13.1 | 0.13.5 |
| Homebrew CA 인증서 | 2026-09-25 | 2026-10-20 |

FFmpeg/ffprobe 9.0.2_1(실행 버전 9.0.2), npm 10.9.9, canvas 3.2.3은 유지했다. MLX·mlx-metal 0.32.4, mlx-whisper 0.4.3, python-dotenv 1.2.4, pytest 9.1.1도 공식 레지스트리의 현재 안정 버전과 일치했다. Node 22의 공식 지원 종료 예정일은 2027-04-30이며 메이저 변경은 하지 않았다.

Node 필수 의존성 brotli 1.2.0→1.2.1, c-ares 1.34.8→1.34.9가 함께 변경됐다. Homebrew 기본 계획은 다른 프로그램 22개까지 갱신하려 했으므로, [공식 옵션](https://docs.brew.sh/Manpage)의 `HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1`을 이번 명령에만 지정해 범위를 제한했다. 기존 keg는 `HOMEBREW_NO_INSTALL_CLEANUP=1`로 보존했다. 대상 도구의 링크 검사는 따로 통과했다. 링크 검사로 켜진 Homebrew 개발자 모드는 다시 껐으며 외부 tap 신뢰 범위는 변경하지 않았다.

### Python 패키지

| 패키지 | 이전 | 적용 |
| --- | --- | --- |
| filelock | 4.2.2 | 4.2.4 |
| httpcore2 | 2.14.0 | 2.16.0 |
| httpx2 | 2.14.0 | 2.16.0 |
| pip | 26.2.1 | 26.2.2 |
| setuptools | 84.0.0 | 84.2.1 |
| certifi | 2026.10.18 | 2026.10.23 |
| huggingface_hub | 2.2.0 | 2.3.0 |

43개 설치 배포의 Python 상·하한 및 활성 의존 조건을 별도로 검사했다. 기존 3.14.8 격리 환경에서 후보 패키지를 먼저 시험하고, Homebrew Python 적용 뒤 `.venv`를 3.14.9로 새로 구성해 같은 검증을 반복했다. 이전 `.venv`와 `node_modules`는 로컬 복구 폴더에 보관했다. `requirements-dev.txt`와 전체 잠금을 갱신했으며 변경 없는 런타임 직접 의존 파일은 다시 쓰지 않았다.

mpmath 최신 1.4.1은 SymPy 1.14.0의 `<1.4` 조건 때문에 1.3.0을 유지했다. 다른 주요 패키지는 실험판·yanked 배포를 선택하지 않았다.

### npm 의존성

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| @puppeteer/browsers | 3.2.5 | 3.2.6 |
| acorn | 새 의존성 | 8.19.0 |
| devtools-protocol | 0.0.1696802 | 0.0.1704951 |
| esbuild | 0.25.12 | 0.28.2 |
| hono | 4.13.13 | 4.13.14 |
| hyperframes | 0.8.173 | 0.8.200 |
| node-abi | 3.99.0 | 3.101.0 |
| puppeteer-core | 25.14.0 | 25.16.0 |

위 비플랫폼 항목 8개와 esbuild 플랫폼별 잠금 항목을 공식 의존 범위 안에서 갱신했다. `acorn`은 새 Hyperframes의 의존성이다. 설치하지 않는 다른 운영체제 패키지의 잠금 변경을 현재 Mac의 설치 수로 세지 않았다. 후보 설치·업데이트·보안 검사를 격리 디렉터리에서 완료한 뒤 검증된 패키지와 잠금을 적용했다.

`npm outdated --all`의 남은 `devtools-protocol` 차이는 Chromium BiDi의 넓은 peer 범위가 최신 0.0.1724436을 원한다고 표시하는 경우다. Puppeteer 25.16.0이 0.0.1704951을 정확히 지정하므로 그 공식 조합을 유지했다. 강제 override나 별도 루트 의존성을 추가하지 않았다. 최종 npm 보안 검사는 0건이다.

## 공식 변경 내용과 판단

- [Hyperframes 0.8.200](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.200)은 재생 위치 근처의 씬만 미리보기에 올리고 캡처 비용에 따라 렌더 자원을 배분한다. 포함된 [0.8.196](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.196)의 esbuild 보안 관련 의존성 변경도 공식 배포 관계로 적용했다. HDR·실험 모션블러를 켜지는 않았다. 3초 진단 렌더만 확인했으므로 장편 성능 개선율이나 앱 꺼짐 현상 해결을 입증한 것은 아니다.
- [Node 22.23.4](https://nodejs.org/en/blog/release/v22.23.4)는 TLS·DNS·Brotli 등을 수정한 보안 릴리스다. 현재 지원되는 22 계열의 패치만 갱신했다. [지원 일정](https://github.com/nodejs/Release/blob/main/schedule.json)도 확인했다.
- [Python 3.14.9](https://www.python.org/downloads/release/python-3149/)는 인증서 사고 대응을 포함한 긴급 보안 릴리스다. [uv 0.13.5](https://github.com/astral-sh/uv/releases/tag/0.13.5)와 [이전 CA 보안 공지](https://github.com/astral-sh/uv/security/advisories/GHSA-hq85-5cpj-mr62), [pip 26.2.2](https://pip.pypa.io/en/stable/news/#v26-2-2)를 함께 대조해 기존 가상환경도 새 pip로 구성했다. Homebrew CA 인증서도 갱신했다. 기본 Python 계열을 바꾸지 않고 `.python-version`을 3.14.9로 고정했다.
- [certifi 비교](https://github.com/certifi/python-certifi/compare/2026.10.18...2026.10.23)는 사고 대응 후 영향 없는 emSign 루트를 복원한 변경을 보여준다. 2026.10.23을 설치했고 영향 받은 루트를 다시 신뢰하도록 수동 설정하지 않았다.
- [httpx2](https://github.com/pydantic/httpx2/blob/main/src/httpx2/CHANGELOG.md)의 쿠키 처리 변경과 [httpcore2](https://github.com/pydantic/httpx2/blob/main/src/httpcore2/CHANGELOG.md)의 동기 버전·SSL 수정을 확인했다. 3.10 지원 제거는 현재 3.14.9와 충돌하지 않는다. 실제 HTTPS 요청과 기존 클라이언트 경로가 통과했다.
- [Hugging Face Hub 2.3.0](https://github.com/huggingface/huggingface_hub/releases/tag/v2.3.0)은 파일 목록·캐시 기능을 바꾼다. 새 실시간 Bucket 구독 기능은 켜지 않았고 기존 Whisper 캐시를 오프라인으로 사용할 수 있음을 확인했다. [filelock 4.2.3](https://github.com/tox-dev/filelock/releases/tag/4.2.3)의 잠금 오류 처리와 4.2.4의 배포 문서 수정, [setuptools 84.2.1](https://setuptools.pypa.io/en/latest/history.html#v84-2-1)의 안정 배포도 확인했다.

## ElevenLabs V4 유지

인증된 읽기 전용 `GET /v1/models`가 HTTP 200을 반환했고 `eleven_v4`의 TTS 가능 및 요청 최대 10,000자를 확인했다. 키나 전체 API 응답을 보고서·Git에 넣지 않았다.

[공식 V4 음성 설정](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md)은 Stability·Similarity만 사용하고 Style·Speed·Speaker Boost·SSML을 보내지 않는 기존 구현과 일치한다. `hyperframes-longform-producer` 스킬도 이 기준으로 대조했다. 바뀐 도구 버전의 고정 표기나 새 V4 설정 차이가 없어 요청기·제작 스킬을 불필요하게 수정하지 않았다.

모델은 `eleven_v4`, Stability 0.5 / Similarity 0.75, 본편 1.00배속, 절제된 태그와 문장 단위 순차 청크를 유지한다. 새 유료 합성을 하지 않았으므로 생성 음질·음색을 청취 승인한 검사는 아니다.

## 최종 검증

| 항목 | 결과 |
| --- | --- |
| 격리 후보 / 최종 Python 테스트 | 각각 69 passed |
| Python 호환성 | 43개, Python 상·하한·활성 의존 검사 통과 |
| 후보 / 최종 Whisper 정렬 | 기존 로컬 10초 음성, 각각 100% (기준 92%) |
| Metal / NumPy / Numba / Torch | GPU 제곱합 328350, 연산·가져오기 성공 |
| Pillow / HTTPS / SSL | RGB·RGBA PNG 경로 및 httpx2 TLS 요청 성공 |
| 후보 / 최종 npm audit | 각각 0건 |
| 후보 / 최종 가로·세로 lint | 오류 0·경고 0 |
| 가로 렌더 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 세로 렌더 | 1080×1920, 60fps, H.264/AAC, 180프레임 |
| canvas 자막 샘플 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 영상·오디오 길이 | 세 최종 출력 모두 각각 3.000초 |
| 1초 이상 freeze / black | 없음 |
| Homebrew 대상 링크 | node@22·python@3.14·uv 통과 |

최종 가로·세로 0·1.5·2.95초 프레임을 각각 개별 확인해 한글·여백·원 이동과 진행 막대를 검수했다. canvas 0.8초의 “둘.”, 2.7초의 “우리는 분명 셋이었어요.”에서 한글·외곽선·안전 위치를 확인했고 1.5초는 입력 타이밍상 정상 공백이다. 처음 검토에서 기존 시험 화면의 진행 막대와 자막이 겹쳤으므로 이번 로컬 가로 fixture만 `bottom:12%`→`5%`로 조정해 가로·canvas를 다시 렌더하고 모든 변경 프레임을 재검수했다. 제작 영상과 과거 실험 파일은 바꾸지 않았다.

실제 사용 브라우저는 HeadlessChrome/152.0.7977.30이며 drawElement 캡처 검증을 통과했다. 새 운영체제 Chrome을 설치한 것은 아니다. 위 영상은 설치 진단용 3초 샘플로 신규 15–40초 쇼츠 납품이나 완성 에피소드의 전체 검수를 대신하지 않는다.

## 보존·복구·기록

`tmp/maintenance/2026-10-26/backups/`에 설정·잠금·환경 정보·시작 Git 상태, 이전 가상환경과 Node 패키지를 보관했다. 이전 Homebrew keg도 남아 있다. 적용 실패·복구 필요 항목은 없다. 공식 릴리스 페이지가 없는 certifi 태그는 비교 기록으로 확인했고 Python 페이지의 압축 응답은 정상 해제해 읽었다. 후보 점검 출력의 중첩 npm 레코드 형식 차이도 수정해 실제 peer 의존 관계를 검증했다.

완료 프로젝트·승인 원고·원본 음성·생성 미디어·관련 없는 변경과 별도 Remotion 저장소는 보존했다. 유료 TTS·이미지·음악 생성과 업로드는 모두 0회다. 검증된 요구사항·잠금·현재 실행 문서·진단 텍스트 입력과 날짜별 보고서만 관련 커밋에 포함하며 비밀정보·생성 미디어·로컬 백업은 제외한다.

[측정 요약](2026-10-26-toolchain-update.json). 기존 점검 보고서는 수정하지 않았다.

## 새 환경 재현

```bash
uv venv --python 3.14.9 .venv
uv pip sync --python .venv/bin/python --link-mode copy requirements.lock
uv pip check --python .venv/bin/python
npm ci
npm audit
.venv/bin/python -m pytest -q
```

환경 재생성은 제작이 없을 때 실행한다. uv 검사와 별도로 Python 요구 범위의 상·하한도 대조한다. 정확한 실행 명령·출력·ffprobe·실제 프레임은 날짜별 로컬 점검 폴더에 남겼다.
