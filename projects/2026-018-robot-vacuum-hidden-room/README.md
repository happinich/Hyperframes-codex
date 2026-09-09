# 로봇청소기가 발견한 안쪽 방

창작 공포 단편. 승인된 대본의 남성 일인칭 서술에 맞춰 Bin 내레이션과 호러 시네마틱 화면을 사용했다.

## 게시 파일

- [본편 게시 도우미](07_publish/youtube/youtube-publish.html): 영상, 썸네일 2종, 메인 제목·대안 5개, 설명·챕터·태그·홍보문·추천 시간 및 복사 버튼.
- [쇼츠 게시 도우미](07_publish/shorts/shorts-publish.html): 독립 티저와 본편 관련 동영상 지정 안내.
- [본편 게시 문서](07_publish/youtube/youtube-publish.md)
- [쇼츠 게시 문서](07_publish/shorts/shorts-publish.md)

본편은 약 7분 55초, 1920x1080/60fps 클린 MP4와 외부 SRT/VTT다. 쇼츠는 약 21초, 1080x1920/60fps, 별도 생성한 1.07배 피치 보존 내레이션과 번인 자막이다. 유튜브 업로드나 예약은 실행하지 않는다.

## 로컬 영상

저장소의 기본 규칙에 따라 큰 음성·영상·작업 프레임은 Git에 올리지 않는다. 해당 워크스페이스에는 아래 경로로 보관한다.

- `06_delivery/youtube/2026-018-robot-vacuum-hidden-room-youtube.mp4`
- `06_delivery/shorts/2026-018-robot-vacuum-hidden-room-shorts.mp4`
- `03_sync/captions.srt`, `captions.vtt`
- `03_sync/shorts-captions.srt`, `shorts-captions.vtt`

## 제작과 검수

승인 대본은 `01_script/narration.txt`, 확정 타임라인은 `01_script/scene-plan.json`, 화면별 단서는 `04_composition/scene-data.json`이다. 자세한 작업 순서와 음성 보정 내역은 [제작 기록](01_script/production-notes.md)을 참조한다.

공유 파이프라인이나 완료된 다른 프로젝트는 변경하지 않았다. 본편은 저장 공간 사용을 제한하기 위해 동일한 Hyperframes 화면을 17개 구간으로 렌더한 뒤 연속 음성과 합친다. 음성 청크나 BGM은 다시 생성하지 않는다.

최종 검사 결과는 `05_review/`의 JSON과 체크리스트에 기록한다. 사람이 전편 청취한 것으로 표기하지 않고, 실제로 수행한 Whisper 재대조·오디오 신호 검사·렌더 프레임 검사를 구분한다.
