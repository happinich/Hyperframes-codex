# Hyperframes Video Studio

얼굴 노출 없는 내레이션 기반 모션 영상을 여러 편 동시에 제작하기 위한 작업 공간입니다. 각 영상은 `projects/<project-id>/` 안에서 독립적으로 관리하고, 공통 도구와 디자인 자산은 최상위에 한 번만 둡니다.

## 제작 순서

1. 주제와 목표를 정하면 제가 `01_script/narration.txt`와 초 단위 `scene-plan.json`을 작성합니다.
2. 음성은 ElevenLabs API로 생성합니다. API 키는 저장소에 넣지 않고, `02_audio/elevenlabs-request.json`에는 voice/model/output 설정만 기록합니다.
3. 대본 승인 직후 `planned-captions.srt`를 함께 생성해 예상 자막과 씬 타이밍을 검수합니다.
4. 받은 파일은 `02_audio/inbox/`에 놓고 아래 명령으로 표준 WAV를 만듭니다.
5. MLX Whisper turbo가 발화 시간을 찾고, 작성된 대본 원문으로 YouTube 업로드용 `captions.srt`를 만듭니다.
6. 제작 프로필과 화면 스타일 후보를 먼저 제시하고 사용자 승인을 받은 뒤 HyperFrames HTML 컴포지션을 만들어 YouTube 16:9를 우선 렌더합니다. 신규 기본은 미니멀 다크 테크형이며, 기존 카드·차트 중심 방식은 별도 클래식 프로필로 보존합니다. 동일 기획에서 Shorts용 9:16 재구성도 보관합니다.

```bash
python3 scripts/new_project.py first-video \
  --title "첫 영상" \
  --production-profile minimal_dark_tech_v1 \
  --visual-style minimal_dark_tech
python3 scripts/create_planned_captions.py projects/first-video
python3 scripts/ingest_audio.py projects/first-video path/to/recording.m4a
python3 scripts/import_srt_captions.py projects/first-video path/to/provided-captions.srt
python3 scripts/align_captions.py projects/first-video
python3 scripts/render_project.py projects/first-video --format youtube
python3 scripts/render_project.py projects/first-video --format shorts
```

`align_captions.py`는 Apple Silicon용 `mlx-whisper`를 사용합니다. 설치 방법과 검수 기준은 [docs/WORKFLOW.ko.md](docs/WORKFLOW.ko.md)를 참고합니다.

Hosted MCP와 로컬 음성 처리의 역할 구분은 [docs/HYPERFRAMES_MCP.ko.md](docs/HYPERFRAMES_MCP.ko.md)에 정리되어 있습니다.

완성본 제작 중 검증된 장기 운영 규칙은 [docs/SUCCESS_RULES.ko.md](docs/SUCCESS_RULES.ko.md)와 [config/success-rules.json](config/success-rules.json)에 저장되어 있습니다.

신규 미니멀 다크 테크형과 기존 리치 모션형의 구분, 자막본 파일명과 선택 명령은 [docs/PRODUCTION_PROFILES.ko.md](docs/PRODUCTION_PROFILES.ko.md)에 정리되어 있습니다.

## 폴더 지도

```text
library/                       공통 로고, 폰트, 배경음, 효과음
projects/
  <project-id>/
    00_brief/                  대상 시청자, 메시지, 출력 포맷
    01_script/                 읽을 원문과 타임라인/씬 설계
    02_audio/inbox/            ElevenLabs에서 받은 원본
    02_audio/working/          영상에 쓰는 정규화 음원
    03_sync/                   기획용 SRT, Whisper 최종 SRT, 품질 보고서
    04_composition/            HyperFrames용 HTML/JS/렌더 음원과 variants/ 세로본
    05_review/                 프리뷰 및 QA 체크리스트
    06_delivery/youtube/       1920x1080 최종본
    06_delivery/shorts/        1080x1920 파생본
    07_publish/youtube/        `youtube-publish.md` 단일 게시 문서
    07_publish/shorts/         세로본 단일 게시 문서
scripts/                       프로젝트 생성, 음성 처리, 렌더 자동화
templates/project/             새 영상의 원본 템플릿
docs/                          제작 규칙과 씬 설계 방식
```

영상 납품에는 자막이 번인되지 않은 MP4, 업로드용 SRT, 게시용 제목·설명·태그·출처·썸네일 문구를 한데 모은 `07_publish/youtube/youtube-publish.md`도 포함합니다. 자세한 기준은 [docs/PUBLISHING.ko.md](docs/PUBLISHING.ko.md)를 참고합니다.

## HyperFrames 연결 상태

현재 Codex 세션에는 `Hyperframes` MCP 도구가 연결되어 있지 않습니다. 폴더와 컴포지션 출력 규격은 HyperFrames 기반 렌더를 염두에 두고 구성했으며, MCP가 활성화되면 `04_composition/index.html`과 동기화 산출물을 입력으로 사용합니다. 로컬 CLI는 이 저장소에 설치되어 있으며 `render_project.py`가 이를 호출합니다.
