# 제작 운영 방식

## 제작 프로필

새 프로젝트는 먼저 제작 프로필을 구분합니다. 현재 채널은 공포 이야기에 집중하므로 기본 권장은 `horror_cinematic_story_v1`입니다. 설명형 영상의 `minimal_dark_tech_v1`과 기존 방식인 `classic_rich_motion_v1`도 별도로 보존합니다. 세부 규칙은 [`PRODUCTION_PROFILES.ko.md`](PRODUCTION_PROFILES.ko.md)와 `config/production-profiles.json`을 기준으로 합니다.

- `horror_cinematic_story_v1`: 콜드 오프닝, 6~8분 현대 일상형 단편 괴담, 시네마틱 이미지 모션, 다층 사운드, 무스포 쇼츠 연결.
- `minimal_dark_tech_v1`: 검정 배경, 흰색 타이포, 네온 초록 강조, 1~3초 문장 단위 모션.
- `classic_rich_motion_v1`: 기존 밝은 카드·지도·표·다층 패널, 3초 단위 정보 변화.
- 공포 본편은 클린 마스터와 외부 SRT/VTT가 기본이며, 자막본은 별도 승인된 경우에만 만듭니다. 설명형 프로필은 기존 고정형 구문 자막 파생본을 유지할 수 있습니다.
- 완료된 기존 프로젝트는 이름을 바꾸거나 다시 렌더하지 않습니다.
- 신규 프로젝트는 브리프, 씬 플랜, 연출 노트, 컴포지션, 납품 메타데이터에 프로필 ID를 기록합니다.

## 역할과 승인 시점

| 단계 | 제가 하는 일 | 사용자가 하는 일 | 다음 단계 조건 |
| --- | --- | --- | --- |
| 기획 | 브리프, 낭독 대본, 초 단위 씬 플랜 작성 | 메시지와 톤 확인 | 원문 승인 |
| 음성 | ElevenLabs API 요청 설정 정리, 생성 파일 정규화, 무음/길이 확인 | API 키와 voice/model 설정 제공 | 최종 음성 1개 확정 |
| 싱크 | 기획용 SRT 생성, Whisper 시간 추출, 원문 기반 최종 SRT/VTT 생성 | 발음 오류가 있으면 재녹음 | 자막 QA 통과 |
| 편집 | 모션 씬 제작, 배경음/효과 배치 | 프리뷰 피드백 | 영상 QA 통과 |
| 출력 | 16:9 마스터와 9:16 쇼츠 최소 1편 렌더 | 게시 승인 | 납품 |
| 게시 준비 | 제목, 설명, 태그, 챕터, 썸네일 문구, 고정 댓글, 출처 정리 | YouTube Studio 입력 및 게시 | 업로드 완료 |

화면 구성에 들어가기 전에는 별도의 **비주얼 스타일 승인 단계**를 둡니다. 주제와 대본이 승인되어도 화면 스타일이 선택되지 않았다면 HyperFrames HTML 제작을 시작하지 않습니다.

대본 검토 자료에는 **보이스 캐스팅 추천**을 함께 넣습니다. 주인공의 성별만
기계적으로 따라가지 않고, 화자의 시점, 감정 거리, 후반부 긴장 상승, 귀신·괴물
대사와의 음색 대비를 검토해 남성·여성 보이스 중 우선 추천과 대안을 제시합니다.
화자 성별이 서사상 고정되지 않았다면 그 사실도 명시합니다. 실제 보이스 선택과
음성 생성은 대본 승인과 분리해 사용자 승인을 받은 뒤 진행합니다.

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

먼저 사용 가능한 제작 프로필과 스타일을 확인합니다.

```bash
python3 scripts/new_project.py --list-production-profiles
python3 scripts/new_project.py --list-visual-styles
```

사용자에게 스타일 후보와 추천 이유를 보여주고 승인을 받은 뒤 프로젝트를 생성합니다.

```bash
python3 scripts/new_project.py 2026-014-night-call \
  --title "새벽 호출벨이 세 번 울리면" \
  --production-profile horror_cinematic_story_v1 \
  --visual-style horror_cinematic
```

설명형 미니멀 프로필과 기존 리치 모션 방식은 별도로 선택합니다.

```bash
python3 scripts/new_project.py 2026-001-ai-workflow \
  --title "AI 업무 자동화의 시작" \
  --production-profile classic_rich_motion_v1 \
  --visual-style adaptive_mix
```

`01_script/narration.txt`에는 실제로 읽을 말만 기록합니다. 제목, 지시문, 괄호 연기 표시는 넣지 않습니다. 연출 설명은 `01_script/scene-plan.json`과 `01_script/production-notes.md`에 분리합니다.

원고를 생성하거나 리라이팅할 때는 아래의 하이퍼프레임스 롱폼 성공 팁을 내부 프롬프트 규칙으로 적용합니다.

- 초반 3초 후킹: 지루한 인사말과 일반론을 삭제하고, 첫 문장은 질문형 문장, 핵심 수치, 또는 반전 사실로 시작합니다.
- 시각 자료 힌트 주입: 자막, 이미지, 그래프가 타이밍에 맞춰 등장하기 쉽도록 "지금 화면에 나오는 이 부분을 보시면...", "이 수치가 의미하는 것은..." 같은 시각적 안내 멘트를 자연스럽게 넣습니다.
- 구어체 텐션 극대화: 일레븐랩스 V3 억양이 살아나도록 "~아시죠?", "~거든요" 같은 대화체 종결을 활용하고, 문장을 짧고 타이트하게 쪼갭니다.

공포 프로필에서는 설명형 규칙을 그대로 사용하지 않습니다. 첫 5~10초에 가장 소름 돋는 대사 한 줄을 선제시한 뒤 장소에 간 이유와 정상 상태를 구체적으로 앉히고, 40~60초 사이에 첫 이상 징후를 보여줍니다. "지금 화면을 보시면" 같은 메타 안내 멘트는 몰입을 깨므로 금지합니다. 새 대본은 사람이 경험을 직접 들려주는 존댓말 구술형 이야기체를 기본으로 하며, `~했어요`, `~였죠`, `~거든요`, `~더라고요`, 필요한 `~했습니다`를 자연스럽게 섞습니다. `했다·였다` 단문을 연속하지 않고 한 영상에서 6~8분 이야기 한 편을 완결합니다. 귀신·괴물 축은 흔적, 부분 노출, 직접 상호작용 순으로 존재를 확인시킵니다. 세부 기준은 [`HORROR_CHANNEL_STRATEGY.ko.md`](HORROR_CHANNEL_STRATEGY.ko.md)를 따릅니다.

씬 플랜은 녹음 전부터 초 단위로 작성합니다. 각 씬에는 `start_seconds`, `end_seconds`, `duration_seconds`, `estimated_words`, `target_wpm`, `narration_text`, `caption_text`, `motion_beats`를 넣습니다. 실제 음성 생성 후 MLX Whisper turbo 타이밍이 들어오면 예상 시간을 실제 발화 시간으로 보정하되, 자막 문구는 승인된 원문을 유지합니다.

대본과 씬 플랜을 작성한 직후에는 아래 명령으로 기획 단계 자막을 함께 만듭니다. 이 파일은 음성 생성 전 검수용이며, 게시에는 사용하지 않습니다.

```bash
python3 scripts/create_planned_captions.py projects/2026-001-ai-workflow
```

## ElevenLabs API 기준

ElevenLabs API를 사용할 때 필요한 입력값은 아래와 같습니다. API 키는 `.env`나 로컬 환경 변수로만 사용하고 프로젝트 파일에는 기록하지 않습니다.

로컬 API 키 입력 파일은 저장소 최상단의 `/Users/happinich/Documents/Hyperframes-codex/.env`입니다. `.env.example`을 형식 참고용으로 사용하며, 실제 `.env`는 `.gitignore`에 의해 Git에 포함되지 않습니다. `generate_elevenlabs_audio.py`는 실행 시 이 파일을 자동으로 읽되, 이미 설정된 운영체제 환경 변수가 있으면 그 값을 우선합니다.

| 항목 | 용도 |
| --- | --- |
| `ELEVENLABS_API_KEY` | 로컬 환경 변수로만 보관하는 API 키 |
| `voice_id` | 사용할 목소리 ID |
| `model_id` | 기본 권장값은 최신 V3 모델인 `eleven_v3` |
| `language_code` | 한국어 고정을 위해 `ko` 사용 |
| `output_format` | 기본 `mp3_44100_128`, 필요 시 더 높은 비트레이트로 조정 |
| `voice_settings` | 안정성, 유사도, 스타일, 스피커 부스트 등 목소리 설정 |
| `apply_text_normalization` | 한국어 숫자 정규화를 보조하기 위해 `on` 사용 |
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

숫자는 ElevenLabs가 문맥에 따라 자릿수로 잘못 읽을 수 있습니다. 화면과 자막에는 승인 원문인 `01_script/narration.txt`의 숫자 표기를 유지하고, 음성 API에는 `scripts/prepare_tts_script.py`가 만든 `01_script/tts-narration.txt`를 전달합니다. 예를 들어 `1401호`, `104동`, `3시 17분`은 각각 `천사백일 호`, `백사 동`, `세 시 십칠 분`으로 바꿉니다. 발음용 파일에 숫자가 하나라도 남으면 생성하지 않습니다.

BGM은 `02_audio/elevenlabs-request.json`의 `bgm.source` 또는 실행 시 `--bgm`으로 지정합니다. 배경음악은 목소리 길이보다 짧으면 자동으로 반복됩니다. 최종 길이는 기본적으로 `목소리 길이 + 4초 여운`이며, 목소리가 나오는 동안은 `-18dB`, 목소리 종료 후 여운 구간은 `-14dB`로 살짝 올라갑니다. 마지막 `3초`에는 페이드아웃되어 뚝 끊기지 않게 마무리합니다. 믹싱된 파일은 기존 `target_audio` 위치에 저장되고, 원본 목소리만 있는 파일은 같은 폴더에 `*-voice-only.mp3`로 보관됩니다.

```bash
export ELEVENLABS_API_KEY="..."
python3 scripts/prepare_tts_script.py projects/2026-001-ai-workflow --replace
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

## 화면 스타일 선택

HyperFrames 영상의 화면 톤을 하나로 고정하지 않습니다. 새 프로젝트마다 `config/visual-styles.json`의 후보를 먼저 제시하고 사용자의 승인을 받습니다.

| 스타일 | 특징 | 잘 맞는 주제 |
| --- | --- | --- |
| 호러 시네마틱 | 저조도 실사·생성 이미지, 단서 클로즈업, 형광등·CCTV·적색 경고 신호 | 창작 공포, 도시괴담, 규칙괴담 |
| 미니멀 다크 테크 | 순수 검정·흰색 타이포·네온 초록, 1~3초 정보 변화 | AI, 개발 도구, 워크플로 |
| 밝은 에디토리얼 | 화이트·아이스 블루, 깨끗한 데이터 카드 | 정책, 교육, 사업 소개 |
| 다크 시네마틱 | 딥 네이비·블랙, 국소 조명과 강한 긴장감 | 위기, 경고, 미스터리 |
| 명암 분할 | 문제는 어둡게, 해결은 밝게 대비 | AI 전환, 전후 비교 |
| 따뜻한 다큐멘터리 | 크림·종이 질감, 성장 기록 분위기 | 창업기, 현장 기록 |
| 프리미엄 금융 | 차콜·딥 그린·골드, 절제된 리포트 | 부동산, 주식, 경제 |
| 네온 테크 | 블랙·시안·퍼플, 데이터 스트림 | AI, 자동화, 소프트웨어 |
| 종이 콜라주 | 오프화이트, 포스트잇과 손그림 | 이야기 해설, 문화, 책 |
| 주제 혼합형 | 위기는 어둡게, 해결은 밝게 장면 전환 | 5분 이상 문제 해결 서사 |

스타일을 고를 때는 `밝게/어둡게`만 정하지 않습니다. 배경 밝기, 색상 팔레트, 질감, 데이터 표현 방식, 전환 속도까지 함께 승인받습니다. 같은 스타일을 연속 사용해야 한다면 레이아웃과 시각 소재를 바꿔 이전 프로젝트와 구분합니다.

## 포맷 전략

새 YouTube 본편은 처음부터 `1920x1080`, `60fps`, 안전 영역 좌우 `120px`을 기준으로 설계합니다. 공포 본편에는 화면 자막을 넣지 않고 클린 마스터와 외부 SRT/VTT를 제공합니다. 렌더러는 프로젝트의 `scene-plan.json`에 기록된 fps를 사용하므로 완료된 기존 프로젝트는 원래 프레임레이트를 유지합니다. 모든 새 본편은 같은 소재를 `15~40초`의 독립된 무스포 티저로 다시 각색해 쇼츠 최소 1편을 함께 납품합니다. 본편 음성을 그대로 자르는 방식은 기본값으로 사용하지 않습니다. 쇼츠는 정체, 반전, 결말을 공개하지 않고 절정 직전 완전한 문장으로 끊습니다. 쇼츠 전용 대본을 별도 승인받고 Eleven V3로 새 음성을 만든 다음, 피치를 유지하는 `1.05~1.10배` 후처리를 적용하며 기본값은 `1.07배`입니다. 쇼츠는 단순 크롭이 아니라 `1080x1920`, `60fps` 중앙 집중 레이아웃으로 다시 배치하고, 모바일용 번인 자막과 외부 SRT/VTT를 모두 만듭니다.

## 게시 자료

최종 렌더와 자막 검수를 마치면 `07_publish/youtube/youtube-publish.md` 한 파일에 YouTube 업로드 자료를 작성합니다. 검색 친화적인 제목 후보, 복사용 설명란, 챕터, 태그 입력란용 키워드, 썸네일 문구, 고정 댓글과 업로드 체크리스트를 모두 이 문서에 넣습니다. 설명란에는 영상에서 참고한 공식 자료 링크를 반드시 넣습니다.

공포 영상은 설명란에 `창작 공포`, `제보 각색`, `검증된 경험담` 중 하나의 작품 성격을 표시합니다. `07_publish/shorts/shorts-publish.html`에는 쇼츠 제목, 설명, 해시태그, 고정 댓글, 추천 게시 시간과 연결할 본편을 기록합니다. 쇼츠는 일반 URL 대신 YouTube Studio의 `관련 동영상`으로 본편을 연결하고, 롱폼은 마지막 15~20초를 엔드스크린용으로 비워 둡니다.

## 완료 후 GitHub 푸시

사용자의 상시 승인에 따라 요청한 제작 작업이 완전히 끝나고 검수까지 통과하면
관련 파일만 선별해 커밋하고 현재 브랜치를 `origin`에 푸시합니다. 작업 트리에
남아 있는 다른 프로젝트 변경, 삭제, 로컬 미디어는 커밋에 포함하지 않습니다.
푸시에 실패하면 로컬 커밋은 보존하고 실패 원인을 결과에 기록합니다.

## 검수 후 스토리 자막 버전

무자막 마스터의 영상·음성 싱크와 화면 배치를 먼저 검수합니다. 공포 본편은 이 클린 마스터와 외부 업로드용 SRT/VTT를 기본 납품하며, 사용자가 별도로 승인했을 때만 자막 버전을 생성합니다.

```bash
node scripts/burn_story_captions.mjs projects/2026-001-ai-workflow
```

자막 버전은 `06_delivery/youtube/<project-id>-youtube-captioned-story.mp4`로 저장합니다. 기본 스타일은 하단 중앙의 `44px`, 굵기 `700` 흰색 구문 자막과 `6px` 검정 외곽선입니다. `captions.words.json`의 실제 발화 타이밍을 사용하되 문장부호, 쉼표, 발화 간격과 최대 28글자를 기준으로 의미 단위에서 나눕니다. 단어별 빨간색 추적이나 이동 효과는 사용하지 않으며, 자막은 YouTube 재생 컨트롤과 겹치지 않는 안전 영역에 둡니다.

## 배경음악 선택 및 적용

음성 검수가 완료된 후, 배경음악을 추가하기 전에 후보를 생성하고 승인합니다. `generate_bgm_candidates.py`는 프로젝트의 승인된 비주얼 스타일을 읽고 ElevenLabs Music API를 통해 후보를 생성한 뒤 음성 프리뷰와 함께 혼합하여 `05_review/bgm-selection.html` 페이지에 저장합니다. 사용자가 이 페이지에서 정확히 하나의 후보를 선택하면 `apply_bgm.py`로 적용합니다.

```bash
python3 scripts/generate_bgm_candidates.py projects/2026-001-ai-workflow
```

`apply_bgm.py`는 TTS를 재실행하지 않으므로, 승인된 음성 테이크와 자막 타이밍이 그대로 유지됩니다. 선택한 후보 ID를 지정하여 적용하며, `--dry-run` 플래그로 실제 쓰기 전에 계획을 미리 확인할 수 있습니다.

```bash
python3 scripts/apply_bgm.py projects/2026-001-ai-workflow --candidate cand-02 --dry-run
python3 scripts/apply_bgm.py projects/2026-001-ai-workflow --candidate cand-02
```

배경음악 적용 후 최종 오디오는 음성 길이에 설정된 아웃트로 딜레이 4초가 추가됩니다. HyperFrames 컴포지션의 아웃트로도 같은 길이만큼 연장해야 하며, 연장 후 다시 렌더링합니다.
