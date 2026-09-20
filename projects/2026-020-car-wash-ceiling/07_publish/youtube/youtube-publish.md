# YouTube 게시 문서: {{VIDEO_TITLE}}

이 문서 하나로 YouTube 업로드와 게시 후 확인을 진행합니다.

## 업로드 파일

- 최종 영상: `../../06_delivery/youtube/2026-020-car-wash-ceiling-youtube.mp4`
- 승인 후 자막 영상: `../../06_delivery/youtube/2026-020-car-wash-ceiling-youtube-captioned-story.mp4`
- 업로드 자막: `../../03_sync/captions.srt`
- 기획 단계 임시 자막: `../../03_sync/planned-captions.srt`
- 영상 형식: `1920x1080`, `16:9`, `60fps`
- 러닝타임: `{{RUNTIME}}`
- 영상 언어: 한국어
- 카테고리 권장: 엔터테인먼트
- 작품 성격: `{{CONTENT_NATURE}}` (`fiction` / `adapted_submission` / `verified_account`)
- 연결 재생목록: `{{PLAYLIST_NAME}}`

## 제목

### 사용 제목

```text
{{YOUTUBE_TITLE}}
```

### 대체 제목

```text
{{ALTERNATE_TITLE_1}}
{{ALTERNATE_TITLE_2}}
{{ALTERNATE_TITLE_3}}
{{ALTERNATE_TITLE_4}}
{{ALTERNATE_TITLE_5}}
```

## 설명란

아래 블록 전체를 YouTube 설명란에 입력합니다.

```text
{{DESCRIPTION}}

🎧 작품 안내
{{CONTENT_NATURE_NOTICE}}

⏱️ 챕터
00:00 {{CHAPTER_1}}

▶️ 다음 이야기·몰아듣기
{{PLAYLIST_OR_NEXT_VIDEO_URL}}

🔗 참고·제보 출처
{{SOURCE_NAME}}
{{SOURCE_URL}}

#{{HASHTAG_1}} #{{HASHTAG_2}} #{{HASHTAG_3}}
```

## 태그 입력란

```text
{{TAG_1}}, {{TAG_2}}, {{TAG_3}}
```

## 썸네일

### 권장 문구

```text
{{THUMBNAIL_COPY}}
```

### 디자인 방향

- 한글 4~8자의 짧은 문구를 사용합니다.
- 문틈, 호출벨, CCTV 화면처럼 결정적인 단서 하나를 크게 보여줍니다.
- 제목 문구를 그대로 반복하지 않고 제목이 숨긴 규칙이나 대사를 보여줍니다.
- 검정·딥 네이비·흰색·경고 빨강의 대비를 사용합니다.

## 고정 댓글

```text
{{PINNED_COMMENT}}
```

## 업로드 체크리스트

- [ ] 최종 영상 파일을 업로드한다.
- [ ] 제목, 설명란, 태그, 썸네일을 이 문서 기준으로 입력한다.
- [ ] 설명란 공식 링크와 `00:00` 챕터 표시를 확인한다.
- [ ] 클린 마스터 또는 승인된 스토리 자막본 중 게시할 영상을 선택한다.
- [ ] `../../03_sync/captions.srt`도 YouTube 자막으로 업로드해 시청자가 자막 표시를 조절할 수 있게 한다.
- [ ] 음성 생성 전 검수에는 `../../03_sync/planned-captions.srt`를 참고하고, 게시에는 Whisper 보정 후 생성된 `captions.srt`만 사용한다.
- [ ] 영상 언어와 업로드 자막 싱크를 확인한다.
- [ ] 고정 댓글을 게시한다.
- [ ] 마지막 15~20초에 관련 다음 영상 또는 공개 재생목록과 구독 엔드스크린을 배치한다.
- [ ] 엔드스크린 요소가 영상의 핵심 자막·단서와 겹치지 않는지 확인한다.
- [ ] `창작 공포`, `제보 각색`, `검증된 경험담` 표시가 실제 제작 근거와 일치하는지 확인한다.

## 추천 게시 시간

- 예약 시간: `{{RECOMMENDED_PUBLISH_TIME_KST}}`
- 기준: YouTube Studio `분석 > 시청자 > 시청자가 YouTube를 이용하는 시간`의 피크 30~60분 전

## 제작 및 사실 확인 메모

- 사용한 참고 자료, 제보 사용 허락, 익명 처리 범위, 각색 여부를 기록합니다.
