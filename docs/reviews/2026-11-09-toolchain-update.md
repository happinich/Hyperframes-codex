# 주간 제작 환경 업데이트 · 2026-11-09

자동화 `hyperframes` · 시작 2026-11-09 08:57:41 KST · 브랜치 `main`, 시작 HEAD `a63d0ea`.
AGENTS·성공 규칙·WORKFLOW와 2026-11-02 점검 기록을 먼저 읽었다. 렌더·음성 생성·다른 설치가 없는 것을 확인하고 변경 전 설정·잠금·설치 버전·Git 상태 526항목을 보관했다.

## 적용한 안정 업데이트

| 도구 | 이전 | 적용 |
| --- | --- | --- |
| uv | 0.13.6 | 0.13.7 |
| click | 8.5.0 | 8.5.1 |
| filelock | 4.2.6 | 4.2.9 |
| pip | 26.2.2 | 26.3 |
| regex | 2026.9.29 | 2026.11.8 |

Homebrew Node 22.23.4_2(실행 버전 22.23.4), Python/프로젝트 Python 3.14.10, FFmpeg/ffprobe 9.0.2_1(실행 버전 9.0.2), npm 10.9.9, canvas 3.2.3은 유지했다. MLX·mlx-metal 0.32.4, mlx-whisper 0.4.3, python-dotenv 1.2.4, pytest 9.2.0도 최신 안정 버전과 일치했다. Python 후보 4개는 안정·non-yanked 배포를 확인했다.

Homebrew dry-run은 uv 한 개만 변경했다. 의존 프로그램 자동 갱신과 cleanup을 이번 명령의 환경 변수로 제한해 기존 keg를 남겼고, 외부 tap 신뢰 설정은 바꾸지 않았다. uv 링크 검사도 통과했다. 검사로 켜진 Homebrew 개발자 모드는 다시 껐다.

### npm 하위 패키지 6개

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| @hono/node-server | 2.1.5 | 2.1.6 |
| @swc/helpers | 0.5.23 | 0.5.24 |
| ansi-regex | 6.5.0 | 6.6.0 |
| hono | 4.13.16 | 4.13.17 |
| semver | 7.8.5 | 7.8.6 |
| ws | 8.22.1 | 8.22.2 |

프로젝트의 공식 의존 범위 안에서 격리 설치·업데이트·보안 검사와 가로/세로 렌더를 통과한 잠금 및 패키지를 적용했다. Hyperframes와 canvas 직접 버전은 그대로다. 후보·최종 환경 모두 npm audit 0건이다. 정확히 지정된 의존 버전을 강제 override하지 않았다.

## Hyperframes 최신판 보류

[Hyperframes 0.9.25](https://github.com/heygen-com/hyperframes/releases/tag/v0.9.25)는 렌더 난수 고정과 음소거 영상 컷의 오디오 대기 수정을 포함한다. 하지만 npm 공식 배포는 여전히 undici **7.25.0**을 정확히 지정한다. 별도 격리 후보 설치는 성공했지만 audit는 undici high 1개와 이를 사용하는 Hyperframes moderate 1개를 보고했다. 이는 취약 패키지 노드 2개이며 개별 보안 공지 수가 아니다. [대표 TLS 검증 공지](https://github.com/advisories/GHSA-2m5v-pch6-74hx)의 수정 버전은 7.30.1이다.

최신판은 루트에 적용하지 않았고 검증된 **0.8.214**를 유지했다. 강제 보안 수정으로 공식 조합을 바꾸지 않았다. 최신 기능의 성능·안정성 개선을 우리 제작에서 검증하거나 적용했다고 주장하지 않는다. 현재 루트의 보안 검사 0건과 분리해 기록한다. 최신판 후보는 `tmp/maintenance/2026-11-09/npm-latest-candidate/`에만 있다.

## 공식 변경 내용과 호환성 판단

- [uv 0.13.7](https://github.com/astral-sh/uv/releases/tag/0.13.7)은 workspace 경로의 glob 오인과 숫자로 시작하는 프로젝트 이름 처리 등을 수정한다. 안정 버전 자체만 적용했고 release note의 preview 기능은 켜지 않았다. Python 3.14.10 선택을 유지했다.
- [pip 26.3](https://pip.pypa.io/en/stable/news/#v26-3)은 설치 중 예기치 않은 import 차단·중단 복구, URL 자격 증명 노출 방지 및 Homebrew 가상환경 설정 경로 수정을 포함한다. 후보와 최종 환경의 `pip check` 및 기존 테스트로 대조했다. 이 프로젝트의 설치는 고정된 잠금을 uv로 적용했다.
- [Click 8.5.1](https://github.com/pallets/click/releases/tag/8.5.1)은 명령/옵션 복사와 오류 종료 처리 등을 수정한 패치다. [filelock 4.2.9](https://github.com/tox-dev/filelock/releases/tag/4.2.9)는 read/write 잠금의 bool 조건 검사를 바로잡고, 포함된 4.2.7은 죽은 lease 표식 회수 문제를 수정한다. 기존 명령 테스트·캐시를 쓰는 Whisper 정렬이 통과했다.
- [regex 2026.11.8](https://pypi.org/project/regex/2026.11.8/)의 공식 sdist 내 changelog는 아직 2026.9.29부터 시작한다. 따라서 새 보안 수정이라는 추정을 하지 않고, 이전/새 공식 sdist를 메모리에서 비교했다. fuzzy 비용 상한 검사와 서로 배타적인 버전 플래그 검사를 확인했고 기존 테스트·실제 정렬 경로로 호환성을 검증했다. 별도 새 취약점 공지가 있다는 뜻은 아니다.
- [Hono Node Server 2.1.6](https://github.com/honojs/node-server/releases/tag/v2.1.6)의 요청 경로·WebSocket 업그레이드 보안 수정과 [Hono 4.13.17](https://github.com/honojs/hono/releases/tag/v4.13.17)의 cookie/URL 처리 수정을 확인했다. [ws 8.22.2](https://github.com/websockets/ws/releases/tag/8.22.2)는 URL 처리, [semver 7.8.6](https://github.com/npm/node-semver/releases/tag/v7.8.6)은 범위 파싱을 수정한다. 나머지 두 항목도 공식 레지스트리의 호환 범위 내 안정 버전이며 렌더와 audit로 대조했다. 초기 audit 0건이어도 공급자 보안 수정을 포함하는 패치는 별도로 확인했다.

mpmath 1.4.1은 SymPy 1.14.0의 `<1.4` 조건 때문에 1.3.0을 유지했다. [Node 공식 일정](https://github.com/nodejs/Release/blob/main/schedule.json)의 22 계열 지원 종료 2027-04-30과 Homebrew deprecated 표시는 지난주와 동일하다. Node 메이저는 변경하지 않았다.

## ElevenLabs V4 유지

인증된 읽기 전용 `GET /v1/models`에서 HTTP 200, `eleven_v4` TTS 가능 및 요청 최대 10,000자를 확인했다. 전체 응답·비밀정보는 저장하지 않았다. 첫 점검 helper는 stdin에서 dotenv 자동 경로 찾기가 실패해 `.env` 경로를 명시하고 재확인했다. 제작 코드를 수정할 문제로 해석하지 않았다.

[공식 V4 설정 문서](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md)는 지난주 자료와 바이트 단위로 같았다. 저장소의 요청 설정과 로컬 `hyperframes-longform-producer` 스킬도 기존 검증 해시·문구와 일치한다. 추가 설정 변화가 없어 재작성하지 않았다. `clone_strength`는 여전히 조건부 PVC용 공급자 안내일 뿐 이 파이프라인에는 미구현이며 전송하지 않는다.

`eleven_v4`, Stability 0.5 / Similarity 0.75, 본편 1.00배속과 기존 청크·태그 규칙을 유지했다. 유료 합성 없이 API 가용성만 확인했으므로 새 음색·음질 청취 검사가 아니다.

## 최종 검증

| 항목 | 결과 |
| --- | --- |
| 후보 / 최종 pytest | 각각 69 passed |
| Python 의존 조건 및 상·하한 | 43개 통과 |
| 최종 pip / uv 검사 | 모두 통과 |
| 후보 / 최종 로컬 Whisper 정렬 | 기존 10초 음성, 각각 100% (기준 92%) |
| MLX GPU / NumPy·Numba / Torch | 제곱합 328350, 연산·import 통과 |
| Pillow / TLS | RGB·RGBA PNG 왕복과 httpx2 HTTPS 200 |
| 선택 후보 / 최종 npm audit | 각각 0건 |
| 후보 / 최종 가로·세로 lint | 0 errors, 0 warnings |
| 최종 가로 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 최종 세로 | 1080×1920, 60fps, H.264/AAC, 180프레임 |
| canvas 자막 파생본 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 영상·오디오 길이 | 모두 3.000초, 길이 차이 0.1초 미만 |
| 1초 이상 freeze / black | 없음 |

가로·세로 0·1.5·2.95초, canvas 0.8·1.5·2.7초의 9개 실제 출력 프레임을 각각 확인했다. 한글·안전 여백·원 이동·진행 막대를 검수했다. canvas의 “둘.”과 “우리는 분명 셋이었어요.”가 정상이며 1.5초의 공백은 입력 타이밍상 정상이다. 자막과 진행 막대 겹침이 없다.

이것은 3초 설치 진단 샘플이며 새 쇼츠 납품이나 완성 에피소드의 전체 시청·청취 검수를 대신하지 않는다. 2026-11-02 실험의 로컬 fixture·음성·자막 입력을 복사해 새 실험 폴더에만 출력했다.

## 보존·복구·재현

`tmp/maintenance/2026-11-09/backups/`에 변경 전 설정·잠금·설치 정보·Git 상태와 이전 `.venv`/`node_modules`를 보관했다. 기존 Homebrew keg를 남겼으며 적용 실패·미복구 변경은 없다. 격리에서 거절된 최신판은 운영 환경에 들어가지 않았다. 완료 프로젝트·원고·음성·생성 미디어·관련 없는 변경 및 별도 Remotion 저장소는 보존했다. 유료 생성·업로드 0회다.

```bash
uv venv --python 3.14.10 .venv
uv pip sync --python .venv/bin/python --link-mode copy requirements.lock
uv pip check --python .venv/bin/python
npm ci
npm audit
.venv/bin/python -m pytest -q
```

제작이 없을 때 재구성한다. 검증된 npm 잠금을 사용하고 최신 Hyperframes를 자동으로 덮어 설치하지 않는다. 관련 잠금·개발 요구사항·현재 실행 문서·새 진단 텍스트 입력과 이 보고서만 커밋한다. 생성 미디어·백업·비밀정보는 제외한다. 상세 [측정 요약](2026-11-09-toolchain-update.json), 로컬 명령·ffprobe·실제 프레임은 날짜별 점검 폴더에 보관한다.
