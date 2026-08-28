# 최종 검수 기록

## 승인 상태

- 전체 음성: 승인
- 보이스: Esther (`dJlwSfdSqMaQjm3NSl3B`)
- BGM: `cand-03` 승인 및 적용
- 클린 마스터: 통과
- 고정형 스토리 자막본: 통과
- 필수 세로 쇼츠: 통과

## 출력 사양

- 해상도: `1920x1080`
- 화면비: `16:9`
- 프레임레이트: `60fps`
- 영상 코덱: `H.264`
- 오디오 코덱: `AAC`, `48kHz`, 스테레오
- 최종 길이: `367.04초` (`6분 7초`)

## 동기화와 오디오

- Whisper 모델: `mlx-community/whisper-large-v3-turbo`
- 자막 정렬 비율: `99.66%`
- 자막 표면 일치율: `99.37%`
- 보이스 길이: `363.033초`
- BGM 아웃트로: `4초`
- 아웃트로 페이드: `3초`
- 전체 평균 볼륨: `-16.9dB`
- 전체 최대 볼륨: `-3.0dB`

## 화면 검수

- 전 구간에서 3초 이상 완전히 멈춘 화면 없음
- 제목과 도형의 겹침 또는 화면 밖 잘림 없음
- 총 영상 시간 배지 없음
- 고정 상단 제목 없음
- 장면 전환 지점의 초반·중반·후반 대표 프레임 확인
- 하단 자막 안전 영역과 본문 그래픽의 충돌 없음

## 게시 파일

- 클린 영상: `../06_delivery/youtube/2026-014-delivery-at-my-door-youtube.mp4`
- 자막 영상: `../06_delivery/youtube/2026-014-delivery-at-my-door-youtube-captioned-story.mp4`
- SRT: `../06_delivery/youtube/2026-014-delivery-at-my-door-ko.srt`
- VTT: `../06_delivery/youtube/2026-014-delivery-at-my-door-ko.vtt`
- 게시 도우미: `../07_publish/youtube/youtube-publish.html`

## 쇼츠 검수

- 대본 방식: 본편 발췌가 아닌 쇼츠 전용 요약·재각색
- 음성: Esther, Eleven V3 별도 생성
- 속도: 피치 보존 `1.07배` 후처리
- 음성 길이: `26.771초`
- 출력 길이: `27.605초`
- 출력 사양: `1080x1920`, `9:16`, `60fps`, H.264/AAC
- 구성: 본편 단순 크롭이 아닌 별도 세로 컴포지션
- 첫 프레임: 핵심 휴대전화 단서가 즉시 표시됨
- 첫 음성: 시작 무음 또는 잘린 음성 없음
- Whisper 대본 일치율: `100%`
- 끝 발화: `그리고 사진 속에는 제가 두 명 있었습니다.`로 완결
- 3초 이상 완전 정지 구간 없음
- 모바일용 고정 구문 자막과 외부 SRT/VTT 검수 완료
- 쇼츠 영상: `../06_delivery/shorts/2026-014-delivery-at-my-door-shorts.mp4`
- 쇼츠 게시 도우미: `../07_publish/shorts/shorts-publish.html`
