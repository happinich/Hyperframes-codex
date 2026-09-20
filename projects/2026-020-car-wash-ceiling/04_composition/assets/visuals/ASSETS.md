# 생성 시각 자산

- 제작 도구: Codex 내장 ImageGen. 외부 웹 사진을 다운로드하지 않았다.
- `shot-01.png`~`shot-48.png`: 본편 전용 16:9 생성 이미지. 얼굴 비노출 화자, 냉백색 형광등, 짙은 청색 세단, 흰색 SUV를 기준으로 검수했다.
- `short-new-01.png`~`short-new-06.png`: 본편 검수 이후 생성하는 쇼츠 전용 9:16 이미지. 본편 이미지 및 추출 프레임을 참조 입력으로 쓰지 않는다.
- `thumbnail-a.png`, `thumbnail-b.png`: 별도 생성 썸네일. 게시용 1280x720 JPG는 `07_publish/youtube/`에 저장한다.
- 프롬프트: `../../image-prompts.json`, `../../image-revisions.json`.
- 생성 원본 및 수정 이력: `../../image-sources.json`. 같은 ID가 여러 번 있으면 마지막 기록이 최종 선택이다. 마지막 수정 프롬프트는 해당 기록을 우선한다.
- 본편 파일과 쇼츠 파일의 해시 및 독립 생성 이력은 `../../../05_review/shorts-originality-check.json`으로 검증한다.

실제 인물·시설·사건의 사진이 아닌 창작 이미지다. 생성물의 상업적 사용에는 사용 서비스의 적용 약관이 따른다.
