# Claude Code Instructions

이 저장소의 작업 지침은 `AGENTS.md` 한 곳에서 관리합니다. Codex와 Claude Code가
같은 규칙을 사용하므로, 규칙을 바꿀 때는 `AGENTS.md`만 수정하고 이 파일은
그대로 둡니다.

@AGENTS.md

## Claude Code 실행 환경 메모

- Python은 시스템 `python3`(3.9)를 사용합니다. 가상환경은 없으며 `mlx-whisper`는
  `~/Library/Python/3.9`에 설치되어 있습니다.
- `hyperframes` CLI(0.7.63)는 저장소 `node_modules`에 있습니다. 전역 설치가
  아니므로 `npx --no-install hyperframes` 또는 `npm run hf:*`로 실행합니다.
- HyperFrames hosted MCP는 연결되어 있지 않습니다. 렌더는 로컬 CLI 경로
  (`scripts/render_project.py`)를 사용합니다. 자세한 방침은
  `docs/HYPERFRAMES_MCP.ko.md`를 참고합니다.
- ElevenLabs와 SNS 게시용 키는 셸 환경변수로만 전달합니다
  (`ELEVENLABS_API_KEY`, `THREADS_ACCESS_TOKEN`, `INSTAGRAM_ACCESS_TOKEN`,
  `X_ACCESS_TOKEN`). 저장소에 키 파일을 만들지 않습니다.
