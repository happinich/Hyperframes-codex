# 주간 제작 환경 업데이트 · 2026-11-16

자동화 `hyperframes` · 시작 09:03:58 KST · `main`, 시작 HEAD `a6dce55`.
AGENTS·성공 규칙·작업 흐름·[11월 9일 검증 기록](2026-11-09-toolchain-update.md)을 읽고,
제작과 설치가 진행 중이지 않은 것을 확인했다. 변경 전 Git 상태와 설정·잠금·설치 정보를 보관했다.

## 적용한 안정 업데이트

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| Hyperframes | 0.8.214 | 0.9.55 |
| Homebrew Node.js 22 | 22.23.4_2 | 22.23.5_1 (실행 22.23.5) |
| uv | 0.13.7 | 0.13.8 |
| filelock | 4.2.9 | 4.2.10 |
| NumPy | 2.5.4 | 2.5.5 |
| regex | 2026.11.8 | 2026.11.15 |

- [Hyperframes 0.9.55](https://github.com/heygen-com/hyperframes/releases/tag/v0.9.55)는 파일 서버의 Host 검사와 스테이징 관련 수정 등을 포함한다. npm 배포가 [TLS 검증 문제](https://github.com/advisories/GHSA-2m5v-pch6-74hx)를 수정한 undici **7.30.1**을 직접 지정해 이전 보류 원인이 해소됐다. 의존성을 강제로 덮어쓰지 않았다. 클라우드 기능은 릴리스 문서로 확인했으며 실행하지 않았다.
- [Node 22.23.5](https://nodejs.org/en/blog/release/v22.23.5)는 HTTP/2의 메모리 처리와 TLS 정책 등을 수정한 보안 릴리스다. 설치 계획에 포함된 libnghttp2 `1.70.0→1.71.0`, libnghttp3 `1.18.0→1.19.0`, ca-certificates `2026-10-20→2026-11-05`, simdjson `5.1.1→5.2.0`, lz4 `1.10.0→1.11.1`만 함께 갱신했다. 구 keg와 인증서 번들 사본을 보관했다. `brew linkage --test`에서 Node·uv·Python·FFmpeg를 확인하고 개발자 모드를 원래 꺼진 상태로 돌렸다. 외부 tap의 신뢰 설정은 변경하지 않았다.
- [uv 0.13.8](https://github.com/astral-sh/uv/releases/tag/0.13.8)은 Unix 평문 인증 파일의 접근 권한과 패키지 해석 쪽을 수정했다. 이 프로젝트는 Python 3.14.10을 명시하고 기존 잠금 기반 설치를 유지한다.
- [filelock 4.2.10](https://github.com/tox-dev/filelock/releases/tag/4.2.10)은 잠금 대기가 기한에 걸렸을 때 반복하던 문제를, [NumPy 2.5.5](https://github.com/numpy/numpy/releases/tag/v2.5.5)는 배열 변환과 스레드 처리 문제 등을 수정했다. [regex 2026.11.15](https://pypi.org/project/regex/2026.11.15/)는 배포 changelog가 이전 버전에 머물러 공식 소스 배포 두 개를 SHA-256 검증 후 비교했다. 부분 일치 문자열 탐색의 범위 밖 읽기와 정규식 컴파일 예외 수정이 소스와 공급자 테스트에 있다. 별도 CVE 번호를 추정하지 않았다.

Homebrew Python·프로젝트 Python `3.14.10`, FFmpeg/ffprobe `9.0.2`(Homebrew `9.0.2_1`), npm `10.9.9`, canvas `3.2.3`, MLX·mlx-metal `0.32.4`, mlx-whisper `0.4.3`, python-dotenv `1.2.4`, pytest `9.2.0`, pip `26.3`은 유지했다. 상위 Python 요구사항은 변경 없고 전이 의존성만 잠금에 반영했다. mpmath `1.4.1`은 SymPy `1.14.0`의 `<1.4` 조건 때문에 `1.3.0`을 유지했다. [Node 공식 지원표](https://nodejs.org/en/about/previous-releases)에 따라 22·24·26은 LTS이며, [22 계열](https://github.com/nodejs/Release/blob/main/schedule.json)은 2027-04-30까지 지원한다. Homebrew deprecated 상태는 동일하고 메이저는 유지했다.

### npm 하위 패키지

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| `@hono/node-server` | 2.1.6 | 2.1.8 |
| `@puppeteer/browsers` | 3.2.6 | 3.2.7 |
| `devtools-protocol` | 0.0.1704951 | 0.0.1717327 |
| `hono` | 4.13.17 | 4.13.18 |
| `postcss` | 8.5.32 | 8.5.33 |
| `puppeteer-core` | 25.16.0 | 25.17.0 |
| `undici` | 기존 프로젝트 의존성에 없음 | 7.30.1 |
| `webdriver-bidi-protocol` | 1.0.1 | 1.0.2 |
| `ws` | 8.22.2 | 8.23.0 |

공식 npm 레지스트리에서 안정 버전과 호환 범위를 확인했다. [Hono](https://github.com/honojs/hono/releases/tag/v4.13.18)의 요청 검증 수정, [Hono Node Server](https://github.com/honojs/node-server/releases/tag/v2.1.8)의 스트림 정리, [ws](https://github.com/websockets/ws/releases/tag/8.23.0)의 메모리 고갈 방어가 포함된다. 기준 환경, 격리 후보, 최종 환경 및 잠금으로 다시 설치한 격리 환경의 npm audit는 각각 0건이다. 이 수치는 검사 당시 레지스트리가 반환한 결과다.

## ElevenLabs V4

[공식 설정 문서](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md)는 지난주와 바이트 단위로 같다. 인증된 [GET /v1/models](https://elevenlabs.io/docs/api-reference/models/list)는 HTTP 200을 반환했고 `eleven_v4`의 TTS 지원 및 구독 요청 최대 10,000자를 확인했다. `eleven_v4`, Stability 0.5, Similarity 0.75, 본편 1.00배속과 기존 청크·태그 규칙을 유지했다. `clone_strength`는 해당 모델에 맞춰 미세 조정된 PVC에 한정된 공급자 설정이며 현재 파이프라인에는 구현하지 않았다. 모델이나 설정 변경이 없어 제작 스킬을 다시 쓰지 않았다. 새 합성·음질 청취 테스트는 하지 않았다.

## 최종 검증

| 검사 | 결과 |
| --- | --- |
| 격리 후보와 최종 pytest | 각각 69 passed |
| Python 패키지·활성 의존성 범위 | 43개 통과, pip·uv 검사 통과 |
| MLX GPU·NumPy/Numba·Torch·Pillow·TLS | 연산·import·PNG 저장/읽기·HTTPS 요청 통과 |
| 로컬 10초 Whisper 정렬 | 격리와 최종 모두 100%, 기준 92% |
| npm audit·잠금 재설치 | 0건, `npm ci` 재현 성공 |
| 가로·세로 제작 CLI (`--strict`, 세로 `--composition`) | 각각 lint 오류 0, 로컬 글꼴 경고 1 |
| 가로·세로·canvas 자막 출력 | 1920×1080 / 1080×1920 / 1920×1080, 각각 60fps·180프레임·H.264/AAC |
| ffprobe 영상·음성 길이 | 세 출력 모두 영상 3.000초 / 음성 3.000초 |
| 프리즈·검정 화면 검사 | 세 출력 모두 1초 이상 구간 없음 |

실제 가로·세로 0·1.5·2.95초와 canvas 0.8·1.5·2.7초의 9프레임을 확인했다. 글자 잘림 없이 원과 진행 막대가 이동했고, 자막 “둘.”과 “우리는 분명 셋이었어요.”의 표시 및 1.5초의 의도된 공백을 확인했다. 로컬 글꼴 경고는 Mac에 설치된 Apple SD Gothic Neo에 대한 이식성 경고다. 현재 Mac 출력은 정상이고 다른 머신·클라우드의 글꼴은 검증하지 않았다. 격리 후보는 단일 작업자에서 drawElement 자체 검증을 통과했고, 최종 제작 명령은 기본 병렬 캡처 설정에 따라 스크린샷 방식을 선택했다. 이 진단으로 장편의 렌더 시간이나 클라우드 호환성을 판단하지 않는다.

## 보존 및 재현

`tmp/maintenance/2026-11-16/backups/`에 이전 `.venv`, `node_modules`, 설정·잠금·Git 상태·Homebrew 링크 정보를 보관했다. 변경 전 상태는 기본 표시 526항목, 추적되지 않은 개별 파일까지 2,707항목이다. 완료 프로젝트·원고·원본 음성·생성 미디어·별도 Remotion 저장소를 변경하지 않았다. 검증은 기존 실험의 복사본을 사용했고, 유료 생성과 납품 업로드는 0회다. 환경에 적용했다가 복구할 변경은 없었다.

```bash
uv venv --python 3.14.10 .venv
uv pip sync --strict --python .venv/bin/python --link-mode copy requirements.lock
npm ci
npm audit
.venv/bin/python -m pytest -q
```

상세 [측정 요약](2026-11-16-toolchain-update.json)과 로컬 로그·프레임은 날짜별 기록에 보관한다. 관련 잠금·실행 문서·검증 기록만 커밋한다.
