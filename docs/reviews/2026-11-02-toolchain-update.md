# 주간 제작 환경 업데이트 · 2026-11-02

자동화 `hyperframes` · 브랜치 `main` · 시작 HEAD `127aeca`.
AGENTS, 성공 규칙, WORKFLOW와 2026-10-26 점검 기록을 먼저 읽었다. 시작 시 충돌하는 제작·설치 프로세스는 없었다. 기존 Git 상태 526항목은 보존 대상으로 기록했다.

## 적용 결과

| 도구 | 이전 | 적용 |
| --- | --- | --- |
| Hyperframes | 0.8.200 | 0.8.214 |
| Homebrew node@22 | 22.23.4 | 22.23.4_2 (실행 버전 동일) |
| Homebrew / 프로젝트 Python | 3.14.9 | 3.14.10 |
| uv | 0.13.5 | 0.13.6 |

FFmpeg/ffprobe 9.0.2, npm 10.9.9, canvas 3.2.3, MLX·mlx-metal 0.32.4, mlx-whisper 0.4.3, python-dotenv 1.2.4는 유지했다.
필수 Homebrew 의존성 icu4c@78 78.3→78.3_1, simdjson 5.0.5→5.1.1, openssl@4 4.0.3→4.1.0도 함께 갱신했다.
`HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1`로 다른 설치 프로그램의 자동 갱신을 제한하고, `HOMEBREW_NO_INSTALL_CLEANUP=1`로 이전 keg를 보존했다. 대상 세 도구의 링크 검사를 통과했으며 이 검사로 켜진 Homebrew 개발자 모드는 다시 껐다. 외부 tap 신뢰 설정은 바꾸지 않았다.

### 최신 Hyperframes 보안 문제로 안전한 중간 버전 선택

최신 안정판 0.8.229는 공식 배포에서 undici를 7.25.0으로 정확히 고정한다. 격리 후보의 `npm audit`가 undici high 및 이를 사용하는 Hyperframes moderate를 보고했다. 이는 취약 패키지 노드 2개이며 개별 보안 공지가 2개라는 뜻은 아니다.
[대표 TLS 검증 공지](https://github.com/advisories/GHSA-2m5v-pch6-74hx)는 7.30.1 미만을 포함한다. 실제 프로젝트가 공격받았다는 증거는 아니다.

레지스트리의 릴리스·의존 관계를 대조해 보안 검사 0건인 가장 높은 안정 후보 **0.8.214**를 선택했다. 0.8.215는 배포 목록에 없고, audit의 영향 범위는 Hyperframes >=0.8.216이다. 강제 override나 `npm audit fix --force`는 하지 않았다. 0.8.229는 격리 폴더에서만 설치했고 루트 환경에 적용하지 않았다. 따라서 운영 환경의 취약 후보 롤백은 필요하지 않았다.

[0.8.214 공식 릴리스](https://github.com/heygen-com/hyperframes/releases/tag/v0.8.214)의 색보정 그룹·LUT 처리 및 탭 저장 충돌 수정을 확인했다. 이번에는 기존 제작 경로의 3초 렌더만 검증했으므로 새 편집 기능 전체나 장편 성능 개선, 앱 꺼짐 해결을 입증하지 않는다. 최신판은 보안 의존성이 정리된 후 다시 검토한다.

### Node 22 상태

[공식 지원 일정](https://github.com/nodejs/Release/blob/main/schedule.json)상 Node 22는 2027-04-30까지 지원된다. [Homebrew node@22](https://formulae.brew.sh/formula/node@22)는 2026-10-30부터 maintenance/EOL 예고를 이유로 deprecated로 표시하며 아직 disabled는 아니다. 지원 종료와 같은 뜻으로 기록하지 않는다. 이번에는 같은 메이저의 bottle revision만 적용했다. Node 메이저 전환은 자동화 범위 밖이므로 별도 검토가 필요하다.

### Python 패키지 7개

| 패키지 | 이전 | 적용 |
| --- | --- | --- |
| filelock | 4.2.4 | 4.2.6 |
| huggingface_hub | 2.3.0 | 2.4.0 |
| torch | 2.14.1 | 2.15.0 |
| hf-xet | 1.7.0 | 1.8.0 |
| pytest | 9.1.1 | 9.2.0 |
| numba | 0.68.0 | 0.68.1 |
| anyio | 4.15.1 | 4.16.0 |

43개 전체 잠금을 새 가상환경에 적용했다. Python 요구 범위의 상한·하한과 활성 의존성을 별도로 검사했다. 후보는 기존 Python 3.14.9에서 먼저 검증했고 최종 `.venv`는 3.14.10으로 재구성해 같은 검사를 반복했다. mpmath 1.4.1은 SymPy 1.14.0의 `<1.4` 조건 때문에 1.3.0을 유지했다. 선택한 배포는 안정판이며 yanked 파일을 사용하지 않았다.

- [Python 3.14.10](https://www.python.org/downloads/release/python-31410/)의 SSL 인증서 사고 대응 및 tar 처리 보안 수정을 확인했다. [uv 0.13.6](https://github.com/astral-sh/uv/releases/tag/0.13.6)의 resolver 메모리·비가상환경 디렉터리 보호 수정을 확인했다. Python 3.15로 전환하지 않고 `.python-version`을 3.14.10으로 고정했다.
- [Torch 2.15.0](https://github.com/pytorch/pytorch/releases/tag/v2.15.0), [Numba 0.68.1](https://numba.readthedocs.io/en/stable/release/0.68.1-notes.html)의 안정 배포와 실제 NumPy/Numba 계산·Torch import를 대조했다. 새로운 MPS 기능은 별도로 켜지 않았다.
- [Hugging Face Hub 2.4.0](https://github.com/huggingface/huggingface_hub/releases/tag/v2.4.0), [hf-xet 1.8.0](https://github.com/huggingface/xet-core/releases/tag/v1.8.0)의 캐시·전송 변경을 확인하고 기존 Whisper 캐시를 오프라인 정렬에 사용했다. 실험적 S3 업로드 기능은 사용하지 않았다.
- [filelock 4.2.6](https://github.com/tox-dev/filelock/releases/tag/4.2.6)의 잠금 경합 수정, [pytest 9.2.0](https://docs.pytest.org/en/stable/changelog.html#pytest-9-2-0)의 API 변화, [AnyIO 4.16.0](https://anyio.readthedocs.io/en/stable/versionhistory.html)의 비동기 처리 변경을 확인했다. 기존 테스트와 HTTP TLS 경로가 통과했다.

### npm 잠금 변경

| 항목 | 이전 | 적용 |
| --- | --- | --- |
| ansi-regex | 6.4.0 | 6.5.0 |
| hono | 4.13.14 | 4.13.16 |
| hyperframes | 0.8.200 | 0.8.214 |
| postcss | 8.5.31 | 8.5.32 |
| tslib | 2.8.1 | 2.9.1 |
| ws | 8.22.0 | 8.22.1 |

위 6개는 선택한 0.8.214 후보의 실제 잠금 차이다. 후보와 최종 환경 모두 npm 보안 검사 0건이다. canvas 버전은 유지했다. 격리 환경에서 설치·보안 검사·가로/세로 lint·렌더를 완료한 뒤 패키지와 잠금을 적용했다.

## ElevenLabs V4 문서·지침 정리

인증된 읽기 전용 `GET /v1/models`가 HTTP 200을 반환했다. `eleven_v4`의 TTS 가능과 요청 최대 10,000자를 확인했다. 전체 응답과 키는 저장하거나 커밋하지 않았다.

[공식 음성 설정 문서](https://github.com/elevenlabs/skills/blob/main/text-to-speech/references/voice-settings.md)에 정확한 V4 모델용으로 미세 조정된 전문 복제 보이스(PVC)에만 적용하는 `clone_strength`가 추가되어 있다. 공급자 범위 0–1·초기 권고 0과 출처를 canonical JSON에 기록했다. **현재 생성기에는 미구현이며 요청에 추가하지 않는다.** 해당 보이스의 자격과 API 요청 경로·음질 검증은 별도 필요하다.

기존 문서의 “V4는 두 설정만 지원”을 “현재 파이프라인은 Stability·Similarity만 전송”으로 정확히 고쳤다. AGENTS·WORKFLOW·생성기 주석·로컬 제작 스킬을 맞췄다. 코드 동작은 바뀌지 않았다. 로컬 스킬 변경은 [재적용 패치](2026-11-02-producer-skill.patch)와 측정 JSON의 전후 해시로 보존했다. 이 0-context 패치는 스킬 디렉터리에서 `git apply --unidiff-zero`로 재적용할 수 있고, 임시 복사본에 실제 적용해 일치를 확인했다. 또한 `skill-creator`의 `quick_validate.py`가 통과했다.

모델 `eleven_v4`, Stability 0.5 / Similarity 0.75, 본편 1.00배속과 기존 순차 청크·태그 규칙을 유지했다. 유료 합성은 0회이므로 새 음질·음색을 청취 승인한 검사가 아니다.

## 검증 결과

| 항목 | 결과 |
| --- | --- |
| 후보 / 최종 pytest | 각각 69 passed |
| Python 활성 의존 조건·상하한 | 각각 43개 통과 |
| 후보 / 최종 로컬 Whisper 정렬 | 10초 기존 음성, 각각 100% (기준 92%) |
| MLX GPU·Numba·NumPy·Torch | 제곱합 328350 / import·연산 통과 |
| Pillow·TLS | RGB/RGBA PNG 왕복·httpx2 HTTPS 200, OpenSSL 4.1.0 |
| 후보 / 최종 npm audit | 각각 0건 |
| 후보 / 최종 가로·세로 lint | 통과 |
| 최종 가로 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 최종 세로 | 1080×1920, 60fps, H.264/AAC, 180프레임 |
| canvas 자막 파생본 | 1920×1080, 60fps, H.264/AAC, 180프레임 |
| 영상·오디오 길이 | 각 3.000초, 차이 0.1초 미만 |
| 1초 이상 freeze / black | 없음 |
| Homebrew 링크 검사 | node@22·python@3.14·uv 통과 |

가로·세로의 0·1.5·2.95초, canvas의 0.8·1.5·2.7초 프레임 9장을 각각 개별 확인했다. 움직이는 원·진행 막대·한글과 안전 여백을 확인했다. canvas 0.8초 “둘.”과 2.7초 “우리는 분명 셋이었어요.”는 정상이며 1.5초는 입력 타이밍의 정상 공백이다. 자막과 하단 진행 막대가 겹치지 않는다. 새 사진·음성·음악을 생성하지 않았다.

3초 진단 샘플은 신규 쇼츠 납품이나 완성 에피소드 전체 검수를 대신하지 않는다. 이전 실험 미디어를 입력으로 사용하고 새 실험 폴더에만 출력했다. 완료 프로젝트를 수정하지 않았다.

## 보존·복구·재현

`tmp/maintenance/2026-11-02/backups/`에 변경 전 설정·잠금·버전·Git 상태, 이전 `.venv`와 `node_modules`를 보관했고 이전 Homebrew keg도 남아 있다. 적용 실패나 미복구 변경은 없다. 보안 부적합 후보는 별도 `npm-rejected-0.8.229` 폴더와 audit 기록에 격리했다. 관련 없는 변경·완료 프로젝트·원본 음성·생성 미디어·별도 Remotion 저장소를 보존한다. 유료 생성·업로드 0회다.

```bash
uv venv --python 3.14.10 .venv
uv pip sync --python .venv/bin/python --link-mode copy requirements.lock
uv pip check --python .venv/bin/python
npm ci
npm audit
.venv/bin/python -m pytest -q
```

제작이 실행되지 않을 때 재구성한다. npm의 새 최신판이 아닌 잠금의 검증 버전을 사용한다. 명령 로그·격리 후보·ffprobe·실제 프레임은 날짜별 로컬 폴더, 휴대 가능한 결과는 [측정 요약](2026-11-02-toolchain-update.json)에 남겼다. 비밀정보·백업·생성 미디어는 커밋하지 않는다.
