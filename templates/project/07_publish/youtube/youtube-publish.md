# YouTube 게시 문서: {{VIDEO_TITLE}}

이 문서 하나로 YouTube 업로드와 게시 후 확인을 진행합니다.

## 업로드 파일

- 최종 영상: `../../06_delivery/youtube/{{PROJECT_ID}}-youtube.mp4`
- 업로드 자막: `../../03_sync/captions.srt`
- 기획 단계 임시 자막: `../../03_sync/planned-captions.srt`
- 영상 형식: `1920x1080`, `16:9`, `30fps`
- 러닝타임: `{{RUNTIME}}`
- 영상 언어: 한국어
- 카테고리 권장: 과학기술

## 제목

### 사용 제목

```text
{{YOUTUBE_TITLE}}
```

### 대체 제목

```text
{{ALTERNATE_TITLE_1}}
{{ALTERNATE_TITLE_2}}
```

## 설명란

아래 블록 전체를 YouTube 설명란에 입력합니다.

```text
{{DESCRIPTION}}

⏱️ 챕터
00:00 {{CHAPTER_1}}

📌 참고 사항
{{AVAILABILITY_NOTE}}

🔗 공식 자료
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

- 모바일에서도 즉시 읽히는 짧은 문구를 중앙에 배치합니다.
- 영상 그래픽 톤과 일치하는 카드 또는 핵심 오브젝트를 사용합니다.

## 고정 댓글

```text
{{PINNED_COMMENT}}
```

## 업로드 체크리스트

- [ ] 최종 영상 파일을 업로드한다.
- [ ] 제목, 설명란, 태그, 썸네일을 이 문서 기준으로 입력한다.
- [ ] 설명란 공식 링크와 `00:00` 챕터 표시를 확인한다.
- [ ] 영상에는 자막을 번인하지 않고 `../../03_sync/captions.srt`를 YouTube 자막으로 업로드한다.
- [ ] 음성 생성 전 검수에는 `../../03_sync/planned-captions.srt`를 참고하고, 게시에는 Whisper 보정 후 생성된 `captions.srt`만 사용한다.
- [ ] 영상 언어와 업로드 자막 싱크를 확인한다.
- [ ] 고정 댓글을 게시한다.

## 제작 및 사실 확인 메모

- 사용한 공식 자료와 변경 가능성이 있는 제공 조건을 기록합니다.
