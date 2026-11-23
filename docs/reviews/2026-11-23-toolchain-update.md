# 주간 제작 환경 업데이트 · 2026-11-23

자동화 `hyperframes` · 시작 09:04:49 KST · `main`, 시작 HEAD `6c9e250`.
AGENTS·성공 규칙·작업 흐름·[직전 검증 기록](2026-11-16-toolchain-update.md)을 읽고,
제작·설치 충돌이 없는 것을 확인했다. 변경 전 Git 상태 2,707항목과 설정·잠금·설치 정보는
`tmp/maintenance/2026-11-23/backups/`에 보관했다.

## 적용 버전

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| Hyperframes | 0.9.55 | 0.9.83 |
| uv | 0.13.8 | 0.13.9 |
| certifi | 2026.10.23 | 2026.11.20 |
| filelock | 4.2.10 | 4.3.0 |
| httpcore2 | 2.16.0 | 2.16.2 |
| httpx2 | 2.16.0 | 2.16.2 |
| PyYAML | 6.0.3 | 6.0.4 |
| regex | 2026.11.15 | 2026.11.19 |

Python은 PyPI의 안정·non-yanked 배포와 Python 요구 범위를 확인해 격리 설치했다.
mpmath 1.4.1은 SymPy 1.14.0의 `<1.4` 조건 때문에 1.3.0을 유지했다.
Homebrew Python·프로젝트 Python 3.14.10, Node.js 22.23.5(Homebrew 22.23.5_1),
FFmpeg/ffprobe 9.0.2(Homebrew 9.0.2_1), npm 10.9.9, canvas 3.2.3,
MLX·mlx-metal 0.32.4, mlx-whisper 0.4.3, python-dotenv 1.2.4,
pytest 9.2.0와 pip 26.3은 최신 확인 결과에 맞춰 유지했다.

Homebrew dry-run은 uv 한 항목만 갱신했다. 범위를 제한하고 자동 cleanup을 끈 뒤
설치했으며 이전 keg를 남겼다. 외부 tap 신뢰 설정은 바꾸지 않았다.
Node·uv·Python·FFmpeg linkage 검사를 통과했고 검사로 켜진 개발자 모드는 다시 껐다.
[Node 공식 지원표](https://nodejs.org/en/about/previous-releases)의 LTS 22·24·26과
[지원 일정](https://github.com/nodejs/Release/blob/main/schedule.json)의 22 계열 종료일
2027-04-30을 대조했다. 기존 Node 메이저를 유지했다.

### npm 의존성

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| `@hono/node-server` | 2.1.8 | 2.1.11 |
| `hono` | 4.13.18 | 4.13.20 |
| `node-abi` | 3.101.0 | 3.104.0 |
| `puppeteer-core` | 25.17.0 | 25.18.1 |
| `source-map-js` | 1.2.2 | 1.2.4 |
| `typed-query-selector` | 2.12.3 | 2.12.4 |

Hyperframes 직접 의존성과 공식 npm 범위 내 하위 패키지를 격리 설치해 렌더·audit로
검증했다. undici는 7.30.1을 유지하며 강제 override는 없다. 기준 환경·격리 후보·최종
환경에서 npm audit는 각각 0건이다. 새 잠금으로 `npm ci`를 다시 실행해 재현도 확인했다.

## 공식 변경 내용

- [Hyperframes 0.9.83](https://github.com/heygen-com/hyperframes/releases/tag/v0.9.83)은 많은 클립·스타일이 있는 페이지의 컴파일 비용과 샌드박스 history 접근을 수정한다. 짧은 로컬 진단에서 CLI 호환성을 검증했으며 장편 렌더 성능이 좋아졌다고 측정한 것은 아니다.
- [uv 0.13.9](https://github.com/astral-sh/uv/releases/tag/0.13.9)는 인덱스에 다른 패키지 이름으로 제시된 wheel을 거부하고, 환경 marker 처리와 잠금 동등성 판단을 수정한다. preview 기능은 켜지 않았다.
- [filelock 4.3.0](https://github.com/tox-dev/filelock/releases/tag/4.3.0)은 POSIX soft lock 표식 복구·정리와 권한 처리 등을 보완한다. 기존 테스트와 캐시를 사용하는 Whisper 정렬을 검증했다.
- [PyYAML 6.0.4](https://github.com/yaml/pyyaml/releases/tag/6.0.4)는 merge key의 지수적 확장 문제를 수정하고 wheel의 libyaml을 갱신한다. Python 3.14 요구 조건을 만족했다.
- [HTTPX2](https://github.com/pydantic/httpx2/blob/main/src/httpx2/CHANGELOG.md)와 [HTTPCore2](https://github.com/pydantic/httpx2/blob/main/src/httpcore2/CHANGELOG.md)는 타입 별칭·리디렉션·프록시 처리와 HTTP/2 흐름 제어 등을 수정했다. 기존 정렬·테스트와 실제 HTTPS GET이 통과했다. certifi는 [공식 PyPI 배포](https://pypi.org/project/certifi/2026.11.20/)로 인증서 번들 갱신을 확인했다.
- [regex 2026.11.19](https://pypi.org/project/regex/2026.11.19/)는 이전·현재 공식 소스 배포를 SHA-256 확인 후 비교했다. Unicode 단어 경계, 반복 그룹과 공유 iterator 관련 변경을 확인했다. 별도 보안 공지나 CVE를 추정하지 않았다.

## ElevenLabs V4 확인과 문서 동기화

[공식 모델 문서](https://elevenlabs.io/docs/overview/models#character-limits)와 인증된
읽기 전용 `GET /v1/models`에서 `eleven_v4` 요청 상한 **100,000자**를 확인했다.
API HTTP 200, TTS 지원 가능이며 `maximum_text_length_per_request`와 구독자 상한이
모두 100,000이었다. 지난주 응답의 구독자 상한 10,000에서 바뀐 점을 기록한다.

`config/success-rules.json`의 공급자 상한과 출처·검증일, WORKFLOW 문구를 동기화했다.
생성기는 이 메타데이터를 청크 확대에 사용하지 않는다. 실제 제작 청크는 기존
1,000~1,300자, 순차 생성·문맥 연결, 본편 1.00배속을 유지한다.
[공식 보이스 설정 문서](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md)는
지난주와 바이트 단위로 같았다. 모델 교체, Stability 0.5 / Similarity 0.75 변경은 없다.
조건부 PVC용 `clone_strength`는 계속 미구현·미전송이다. 제작 스킬에는 고정된 구 상한이
없어 수정하지 않았다. 유료 TTS나 10만 자 요청은 실행하지 않았으며 음질 검증도 아니다.

## 검증 결과

| 검사 | 결과 |
| --- | --- |
| 격리·최종 테스트 | 각각 69 passed |
| Python·의존 조건 | 43개 메타데이터 범위 대조, pip·uv 검사 통과 |
| MLX GPU / NumPy·Numba·Torch | 연산·import 통과 |
| Pillow / TLS | PNG 왕복 및 HTTPS GET 200 |
| 로컬 10초 Whisper 정렬 | 격리·최종 100%, 기준 92% |
| npm 보안 검사 | 기준·격리·최종 0건, 잠금 재설치 통과 |
| 제작 CLI 가로·세로 | `--strict`, 세로 `--composition` 경로 통과 |
| lint | 오류 0, 로컬 글꼴 이식성 경고 1 |
| 가로 / 세로 / canvas 자막 출력 | 1920×1080 / 1080×1920 / 1920×1080, 각각 60fps·180프레임·H.264/AAC |
| 영상·음성 길이 | 각각 3.000초, 불일치 없음 |
| 1초 이상 freeze / black | 없음 |

가로·세로 0·1.5·2.95초, canvas 0.8·1.5·2.7초의 실제 9프레임을 개별 확인했다.
한글 잘림·겹침 없이 원과 진행 막대가 이동하며 “둘.”, “우리는 분명 셋이었어요.”가
기존 타이밍에 나타난다. 1.5초 자막 공백은 입력상 정상이다. 로컬 Apple 글꼴 경고는
현재 Mac에서 정상 출력됨을 확인했고 클라우드·다른 기기 호환성을 뜻하지 않는다.

## 보존·복구·재현

변경 전 `.venv`·`node_modules`와 설정·잠금·설치 정보를 백업했다. 실패해 원복할
운영 변경은 없으며 초기 점검 로그 생성 두 명령은 작업 폴더 준비 전에 실행되어
실패했으나 폴더 생성 후 정상 재실행했다. 제작 환경·원본·완료 작품에는 그 실패의
영향이 없다. 미디어는 이전 진단 자산을 복사해 이번 점검 폴더에만 출력했다.
관련 없는 Git 2,707항목·완료 프로젝트·별도 Remotion 저장소를 보존했다.
유료 생성·납품 업로드 0회다.

```bash
uv venv --python 3.14.10 .venv
uv pip sync --strict --python .venv/bin/python --link-mode copy requirements.lock
npm ci
npm audit
.venv/bin/python -m pytest -q
```

잠금·공급자 메타데이터·실행 문서·이 기록만 커밋한다. [측정 요약](2026-11-23-toolchain-update.json)과
로컬 로그·복구 자료는 날짜별 점검 폴더에 보관한다. 이 진단은 완성 작품의 전체 시청·청취를 대신하지 않는다.
