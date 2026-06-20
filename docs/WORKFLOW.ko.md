# 제작 운영 방식

## 역할과 승인 시점

| 단계 | 제가 하는 일 | 사용자가 하는 일 | 다음 단계 조건 |
| --- | --- | --- | --- |
| 기획 | 브리프, 낭독 대본, 초 단위 씬 플랜 작성 | 메시지와 톤 확인 | 원문 승인 |
| 음성 | ElevenLabs API 요청 설정 정리, 생성 파일 정규화, 무음/길이 확인 | API 키와 voice/model 설정 제공 | 최종 음성 1개 확정 |
| 싱크 | 기획용 SRT 생성, Whisper 시간 추출, 원문 기반 최종 SRT/VTT 생성 | 발음 오류가 있으면 재녹음 | 자막 QA 통과 |
| 편집 | 모션 씬 제작, 배경음/효과 배치 | 프리뷰 피드백 | 영상 QA 통과 |
| 출력 | 16:9 마스터 렌더, 필요 시 9:16 재편집 | 게시 승인 | 납품 |
| 게시 준비 | 제목, 설명, 태그, 챕터, 썸네일 문구, 고정 댓글, 출처 정리 | YouTube Studio 입력 및 게시 | 업로드 완료 |

## 왜 자막에 Whisper 텍스트를 그대로 쓰지 않는가

자동 받아쓰기에는 고유명사, 숫자, 외래어 오류가 생길 수 있습니다. 이 프로젝트에서는 `01_script/narration.txt`가 자막의 단일 기준 원문입니다. MLX Whisper turbo는 그 원문이 언제 발화되었는지 찾는 타이밍 엔진으로 사용합니다. 자막은 MP4에 번인하지 않고 YouTube 업로드용 별도 SRT/VTT로 납품합니다.

`scripts/align_captions.py`는 아래 결과물을 만듭니다.

| 파일 | 용도 |
| --- | --- |
| `03_sync/planned-captions.srt` | 대본 승인 직후 씬 플랜 예상 시간으로 만든 검수용 자막 |
| `03_sync/whisper_raw.json` | MLX Whisper turbo가 인식한 내용과 단어 시간 |
| `03_sync/captions.srt` | YouTube 업로드용 최종 자막, 문구는 대본 원문 |
| `03_sync/captions.vtt` | 웹/플레이어 자막 |
| `03_sync/captions.words.json` | HyperFrames 애니메이션용 타임 코드 |
| `03_sync/sync_report.json` | 원문과 인식 결과의 일치율 및 검수 상태 |
| `03_sync/pacing_report.json` | 무음, 단어 간격, 15초 단위 말 속도 검수 상태 |
| `04_composition/transcript-data.js` | 필요 시 모션 타이밍 참고용 자막 데이터. 화면 번인에는 사용하지 않음 |

정렬 일치율이 `0.92` 미만이면 화면 문구는 여전히 원문이지만 싱크 정확도를 보장할 수 없으므로 편집을 멈추고 음성을 청취 검수합니다. 최종 렌더 전에는 반드시 SRT를 음성과 함께 한 번 확인합니다.

## 초기 설정

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

기본 모델은 Apple Silicon에서 빠르게 동작하는 `mlx-community/whisper-large-v3-turbo`입니다. 이 프로젝트에서는 Whisper가 자막 문구를 새로 쓰지 않고, 승인된 대본 원문의 실제 발화 시간만 찾습니다.

## 프로젝트 시작

```bash
python3 scripts/new_project.py 2026-001-ai-workflow --title "AI 업무 자동화의 시작"
```

`01_script/narration.txt`에는 실제로 읽을 말만 기록합니다. 제목, 지시문, 괄호 연기 표시는 넣지 않습니다. 연출 설명은 `01_script/scene-plan.json`과 `01_script/production-notes.md`에 분리합니다.

원고를 생성하거나 리라이팅할 때는 아래의 하이퍼프레임스 롱폼 성공 팁을 내부 프롬프트 규칙으로 적용합니다.

- 초반 3초 후킹: 지루한 인사말과 일반론을 삭제하고, 첫 문장은 질문형 문장, 핵심 수치, 또는 반전 사실로 시작합니다.
- 시각 자료 힌트 주입: 자막, 이미지, 그래프가 타이밍에 맞춰 등장하기 쉽도록 "지금 화면에 나오는 이 부분을 보시면...", "이 수치가 의미하는 것은..." 같은 시각적 안내 멘트를 자연스럽게 넣습니다.
- 구어체 텐션 극대화: 일레븐랩스 V3 억양이 살아나도록 "~아시죠?", "~거든요" 같은 대화체 종결을 활용하고, 문장을 짧고 타이트하게 쪼갭니다.

씬 플랜은 녹음 전부터 초 단위로 작성합니다. 각 씬에는 `start_seconds`, `end_seconds`, `duration_seconds`, `estimated_words`, `target_wpm`, `narration_text`, `caption_text`, `motion_beats`를 넣습니다. 실제 음성 생성 후 MLX Whisper turbo 타이밍이 들어오면 예상 시간을 실제 발화 시간으로 보정하되, 자막 문구는 승인된 원문을 유지합니다.

대본과 씬 플랜을 작성한 직후에는 아래 명령으로 기획 단계 자막을 함께 만듭니다. 이 파일은 음성 생성 전 검수용이며, 게시에는 사용하지 않습니다.

```bash
python3 scripts/create_planned_captions.py projects/2026-001-ai-workflow
```

## ElevenLabs API 기준

ElevenLabs API를 사용할 때 필요한 입력값은 아래와 같습니다. API 키는 `.env`나 로컬 환경 변수로만 사용하고 프로젝트 파일에는 기록하지 않습니다.

| 항목 | 용도 |
| --- | --- |
| `ELEVENLABS_API_KEY` | 로컬 환경 변수로만 보관하는 API 키 |
| `voice_id` | 사용할 목소리 ID |
| `model_id` | 기본 권장값은 최신 V3 모델인 `eleven_v3` |
| `language_code` | 한국어 고정을 위해 `ko` 사용 |
| `output_format` | 기본 `mp3_44100_128`, 필요 시 더 높은 비트레이트로 조정 |
| `voice_settings` | 안정성, 유사도, 스타일, 스피커 부스트 등 목소리 설정 |
| `bgm` | 선택 항목. 지정하면 최종 목소리 파일 생성 직후 배경음악을 자동 루프/믹싱 |

생성 요청 설정은 `02_audio/elevenlabs-request.json`에 남기고, 결과 MP3만 `02_audio/inbox/`에 저장합니다.

설명형 한국어 내레이션의 기본값은 복제 목소리의 억양 변화를 살리면서 과한 흔들림을 줄이는 설정을 사용합니다.

```json
{
  "stability": 0.5,
  "similarity_boost": 0.75,
  "style": 0.15,
  "use_speaker_boost": true
}
```

V3는 긴 원고에서 타임아웃이나 음성 끊김이 생길 수 있으므로 `generate_elevenlabs_audio.py`가 원고를 공백 포함 1,000~1,300자 안팎으로 문장 단위 분할하고, 각 파트를 순차 생성한 뒤 ffmpeg로 최종 MP3를 병합합니다.

BGM은 `02_audio/elevenlabs-request.json`의 `bgm.source` 또는 실행 시 `--bgm`으로 지정합니다. 배경음악은 목소리 길이보다 짧으면 자동으로 반복됩니다. 최종 길이는 기본적으로 `목소리 길이 + 4초 여운`이며, 목소리가 나오는 동안은 `-18dB`, 목소리 종료 후 여운 구간은 `-14dB`로 살짝 올라갑니다. 마지막 `3초`에는 페이드아웃되어 뚝 끊기지 않게 마무리합니다. 믹싱된 파일은 기존 `target_audio` 위치에 저장되고, 원본 목소리만 있는 파일은 같은 폴더에 `*-voice-only.mp3`로 보관됩니다.

```bash
export ELEVENLABS_API_KEY="..."
python3 scripts/generate_elevenlabs_audio.py projects/2026-001-ai-workflow --replace --postprocess
```

```bash
python3 scripts/generate_elevenlabs_audio.py projects/2026-001-ai-workflow --replace --bgm library/audio/music/midnight-library.mp3
```

`--postprocess`는 생성 직후 `ingest_audio.py`, `align_captions.py`, `analyze_audio_pacing.py`를 차례대로 실행합니다. 속도 검수에서 긴 무음, 긴 단어 간격, 지나치게 느린 15초 구간이 많으면 `pacing_review_required`가 되고 렌더가 중단됩니다.

## 음성 수신 후

```bash
python3 scripts/ingest_audio.py projects/2026-001-ai-workflow ~/Downloads/narration.m4a
python3 scripts/import_srt_captions.py projects/2026-001-ai-workflow ~/Downloads/narration.srt
python3 scripts/align_captions.py projects/2026-001-ai-workflow --language ko
python3 scripts/analyze_audio_pacing.py projects/2026-001-ai-workflow --language ko
```

원본 오디오는 변경하지 않고 `02_audio/inbox/<project-id>-narration.<ext>`로 보관됩니다. 영상용 오디오는 `02_audio/working/voice.wav`로 정규화되며, HyperFrames가 자체 프로젝트 안에서 읽을 수 있도록 `04_composition/assets/audio/voice.wav`에도 복사됩니다.
제공된 SRT는 원문과 완전히 일치할 때만 최종 자막 후보로 보관합니다. 이후 `align_captions.py`가 `mlx-community/whisper-large-v3-turbo` 결과로 싱크를 독립 검증하고 YouTube 업로드용 최종 자막 산출물을 갱신합니다. HyperFrames 렌더에는 자막을 화면 요소로 넣지 않습니다.

## 화면 톤

HyperFrames 영상은 기본적으로 밝은 분위기를 사용합니다. 배경은 화이트, 옅은 블루, 민트, 연한 그라데이션을 중심으로 잡고, 텍스트는 진한 네이비/차콜로 대비를 만듭니다. 어두운 배경은 경고, 장애, 보안처럼 주제상 필요한 경우에만 짧게 사용합니다.

## 포맷 전략

YouTube 본편은 처음부터 `1920x1080`, `30fps`, 안전 영역 좌우 `120px`, 하단 자막 안전 영역 `140px`을 기준으로 설계합니다. Shorts는 단순 크롭이 아니라 동일 대본에서 핵심 씬을 `1080x1920` 중앙 집중 레이아웃으로 다시 배치합니다. 씬 플랜의 각 씬에 `shorts_adaptation`을 미리 기록해 재작업을 줄입니다.

## 게시 자료

최종 렌더와 자막 검수를 마치면 `07_publish/youtube/youtube-publish.md` 한 파일에 YouTube 업로드 자료를 작성합니다. 검색 친화적인 제목 후보, 복사용 설명란, 챕터, 태그 입력란용 키워드, 썸네일 문구, 고정 댓글과 업로드 체크리스트를 모두 이 문서에 넣습니다. 설명란에는 영상에서 참고한 공식 자료 링크를 반드시 넣습니다.
