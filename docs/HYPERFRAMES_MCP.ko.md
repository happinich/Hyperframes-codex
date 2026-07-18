# HyperFrames 연결 방침

## 현재 선택

이 저장소는 HyperFrames의 공개 HTML 컴포지션 형식과 로컬 CLI 렌더러를 기본 실행 경로로 사용합니다. 이유는 전달받은 `mp3`, `m4a`, `mp4` 음원을 로컬에서 정규화하고, 작성 대본과 Whisper 타임코드를 함께 검수해야 하기 때문입니다.

현재 이 Codex 세션의 사용 가능 MCP 목록에는 HyperFrames 도구가 노출되어 있지 않으므로, 이 대화 안에서 hosted MCP의 `compose` 또는 `render_video`를 직접 호출할 수는 없습니다.

## Hosted MCP를 연결할 경우

HyperFrames 공식 hosted MCP URL은 다음과 같습니다.

```text
https://mcp.heygen.com/mcp/hyperframes
```

HeyGen 계정으로 OAuth 인증한 뒤 사용할 수 있으며, 공식 문서에 따르면 `compose`, `list_compositions`, `get_composition`, `render_video`, `get_render_status`, `get_credits` 도구를 제공합니다. 기획이 확정된 뒤 클라우드 프리뷰나 보조 렌더에 사용할 수 있습니다.

## 음성 파일 처리 제한

공식 MCP 문서에는 채팅을 통한 신규 바이너리 업로드가 현재 지원되지 않는다고 명시되어 있습니다. 따라서 사용자가 ElevenLabs에서 전달하는 음원은 아래의 로컬 파이프라인으로 처리합니다.

1. ElevenLabs API로 생성한 원본 MP3를 `02_audio/inbox/`에 보관합니다.
2. `scripts/ingest_audio.py`가 원본을 보관하고 렌더용 WAV를 생성합니다.
3. `scripts/align_captions.py`가 `mlx-community/whisper-large-v3-turbo` 타이밍에 승인된 원문을 맞춥니다.
4. HyperFrames HTML은 승인된 프로젝트별 비주얼 스타일로 제작합니다. 화면 스타일 승인 전에는 컴포지션 생성을 시작하지 않습니다.
5. 정확 문구 자막은 `03_sync/captions.srt`로 별도 납품합니다.
6. `scripts/render_project.py`가 YouTube 또는 Shorts MP4를 로컬 렌더합니다.

이 방식은 MCP가 추후 활성화되어도 바뀌지 않습니다. hosted MCP는 선택적인 클라우드 작성/렌더 경로이고, 원본 음성과 정확 자막의 기준 파일은 이 저장소에 남깁니다.

## 참고

- HyperFrames MCP 안내: <https://hyperframes.mintlify.app/guides/mcp>
- HyperFrames 공식 사이트: <https://hyperframes.video/>
- HyperFrames npm CLI: <https://www.npmjs.com/package/hyperframes>
