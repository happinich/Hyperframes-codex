# 제작 환경 및 ElevenLabs V4 업데이트

검증일: 2026-10-05. 작업 공간: `/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co`.

## 설치 결과

| 항목 | 이전 | 적용 버전 |
| --- | --- | --- |
| Hyperframes | 0.7.63 | 0.8.126 |
| Node.js 22 | 22.22.0 | 22.23.3 |
| Node에 포함된 npm | 10.9.4 | 10.9.9 |
| Homebrew Python | 3.14.6 | 3.14.8 |
| FFmpeg / ffprobe | 8.1.2 | 9.0.2 |
| uv | 0.10.6 | 0.12.23 |
| 프로젝트 MLX / mlx-metal | 프로젝트 환경 재구성 | 0.32.3 |
| mlx-whisper | 프로젝트 환경 재구성 | 0.4.3 |
| python-dotenv | 프로젝트 환경 재구성 | 1.2.4 |
| pytest / pip | 프로젝트 환경 재구성 | 9.1.1 / 26.2.1 |
| 자막 생성용 canvas | 명시적 의존성 없음 | 3.2.3 |

`node@22`를 같은 메이저 버전 내에서 갱신했습니다. 프로젝트 `.venv`는 Python 3.14.8로 생성했으며 macOS 개발 도구의 `/usr/bin/python3` 3.9.6은 별도입니다. 명령과 설치 안내는 `.venv/bin/python` 및 `uv`를 사용합니다. `requirements.lock`은 실제 설치된 42개 Python 패키지를 고정합니다.

Hyperframes 설치 후 `npm audit fix`로 취약한 하위 의존성을 갱신했습니다. canvas 추가 후 최종 npm 보안 검사 결과는 **취약점 0건**입니다. 기존 세 자막 스크립트가 사용하는 canvas를 직접 의존성으로 선언하고 실제 자막 영상 생성을 확인했습니다.

## 새 프로젝트의 V4 기준

새 본편과 쇼츠는 `eleven_v4`, 한국어 `ko`, Stability `0.5`, Similarity `0.75`를 기본으로 사용합니다. 생성기와 프로젝트 생성기는 `config/success-rules.json`에서 기본값을 읽습니다. V4가 지원하지 않는 Style·Speed·Speaker Boost 설정은 요청에서 제거하며 SSML은 사전에 거부합니다.

[ElevenLabs V4 공식 문서](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)에 따른 오디오 태그를 발음용 `tts-narration.txt` 또는 `request.performance_direction`에 사용합니다. 승인 원고와 자막에는 태그를 넣지 않습니다. 생성 전에는 태그를 제거한 문장이 승인 원고의 한국어 숫자 발음 변환과 일치하는지 검사하고, Whisper의 발화 일치율 계산에서도 태그를 제외합니다.

V4의 요청당 한도는 10,000자이며, 실제 제작은 검수가 쉬운 1,000~1,300자 문장 청크를 유지합니다. [공식 TTS API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)의 이전 요청 ID 또는 앞뒤 문맥을 전달하여 순차 생성합니다. 청크 연결은 실제 API 2청크 실험에서도 성공했습니다.

대본은 자연스러운 한국어 존댓말 구술체, 절제된 긴장감, 점진적인 감정 상승을 기본으로 합니다. 감정 태그는 필요한 대사에 드물게 사용하고, 목소리 안에 효과음·BGM을 요청하지 않습니다. 생성된 비음성·배경음 혼입 여부는 음성 검수 항목입니다. 쇼츠는 별도로 승인된 원고로 V4 음성을 생성하고 기존의 피치 유지 1.07배 후처리 기준을 유지합니다.

프로젝트 템플릿, AGENTS.md, 제작 문서 및 로컬 `hyperframes-longform-producer` 스킬을 함께 갱신했습니다. 이 저장소의 재사용 Remotion 프롬프트 문서도 갱신했으며 별도 Remotion 저장소는 수정하지 않았습니다. 새 프로젝트의 BGM은 미리 지정하지 않고 기존의 별도 승인 절차로 선택합니다. 완료 프로젝트와 기존의 명시적 모델 설정은 유지했습니다.

## 실제 검증

- Python 자동 검증: **61 passed**. V4 요청 설정 필터, 원고 변경 차단, SSML 거부, V3 명시적 설정 유지, 오디오 태그 정렬 및 새 프로젝트 기본값을 포함합니다.
- MLX Metal 연산, Whisper import 및 실제 한국어 정렬 성공.
- 동일한 승인 원고와 Esther 목소리로 V3/V4 비교 음성 생성. 두 모델 모두 Whisper 원고 정렬 **100%**, 기준 92% 통과.
- V4 이전 요청 ID 2개를 수신하고 두 번째 청크에서 첫 번째 ID 사용. 병합 후 실제 Whisper 정렬 **100%**.
- Hyperframes lint: 가로·세로 테스트 구성 모두 오류 0, 경고 0.
- 가로 1920×1080 및 세로 1080×1920 각각 3초, 60fps, 180프레임, H.264/AAC 렌더 성공. 각 영상의 오디오와 비디오는 모두 3.000초.
- drawElement 캡처의 Hyperframes 자체 프레임 비교 검증 통과.
- 1초 이상 freeze/black 검출 없음. 두 영상의 시작·중간·끝 프레임을 개별 확인해 한국어 표시, 여백, 모션 변화를 검수.
- canvas/FFmpeg로 1920×1080, 60fps, 3초 자막 파생본 생성. 실제 자막이 표시되는 프레임에서 글리프·외곽선·배치를 확인.
- 기존 `projects/` 및 `planning/`의 작업 트리 상태 176개 항목이 업데이트 전과 동일함을 확인. 기존의 삭제·미추적 파일은 이 작업에 포함하지 않음.
- 로컬 제작 스킬 검증: `Skill is valid!`.

이번 렌더는 설치 호환성을 확인하는 3초 테스트입니다. 새 공포 에피소드 제작이나 완료 영상 전체의 재검수로 간주하지 않습니다.

## 음성 비교

[비교 청취 페이지](../../experiments/2026-10-05-v4-upgrade/comparison.html)와 [측정 기록](../../experiments/2026-10-05-v4-upgrade/comparison-metrics.json).

| 측정 | V3 | V4 |
| --- | --- | --- |
| 실제 MP3 길이 | 50.80초 | 48.88초 |
| Whisper 원고 정렬 | 100% | 100% |
| 평균 발화 속도 | 110.5 WPM | 115.6 WPM |
| 0.8초 초과 단어 간격 | 3곳 | 1곳 |
| 자동 무음 검출 | 0곳 | 0곳 |

각 모델을 한 번씩 생성한 실사용 비교이며 V4에만 절제된 한국어 연기 지시를 추가했습니다. 따라서 이 수치만으로 V4의 일반적인 품질 우위를 주장하지 않습니다. V4의 9.64~10.56초 간격은 숫자 “넷” 직전의 서사적 멈춤입니다. 느린 마지막 창은 15초보다 짧은 말미 구간이므로 전체 속도 문제로 판단하지 않았습니다. 자동 정렬은 음색·감정의 자연스러움이나 배경음 혼입을 판정하지 않으며, 주관적인 청취 검수를 완료했다고 주장하지 않습니다.

2청크 MP3 스트림 복사 병합 시 FFmpeg가 경계에서 비단조 DTS 경고 한 번을 기록했습니다. 병합 MP3와 디코딩 WAV 길이는 모두 10.031초이며 원고 정렬은 100%입니다. 청크별 MP3 합계는 10.000초로, 최종 MP3와 약 31ms 차이가 있습니다. 이 실험에서는 발화 누락이 검출되지 않았으며 실제 제작에서는 평소와 같이 경계 호흡과 음질을 검수합니다.

## 재현

```bash
uv venv --python 3.14.8 .venv
uv pip sync --python .venv/bin/python --link-mode copy requirements.lock
npm ci
.venv/bin/python -m pytest -q
npm audit
```

실험 소스·정렬 데이터·메타데이터는 `experiments/2026-10-05-v4-upgrade/`에 저장했습니다. 생성 음성, 영상, 검수 프레임은 로컬에 보관하고 Git에는 포함하지 않습니다. API 키는 환경 변수로만 사용했습니다.
