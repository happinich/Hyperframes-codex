# 롱폼 스토리 자막 스타일 검토

- 검토일: `2026-08-25`
- 대상: `2026-013-three-signals-0317`
- 승인 상태: 사용자 승인 (`2026-08-25`)
- 기존 빨간 단어 추적 자막본: 검수 기록과 접촉 시트는 보존하고, 전체 MP4는 승인된 신규 자막본으로 교체
- 신규 샘플: `05_review/preview/2026-013-three-signals-0317-story-caption-sample-60s.mp4`

## 조사 결론

단어별 강조와 큰 키네틱 자막은 무음 자동재생 비중이 높은 Shorts, Reels, TikTok형 영상에서 여전히 강하다. 반면 내레이션을 들으며 이미지와 분위기에 몰입하는 롱폼 이야기 영상은 계속 움직이는 단어 강조보다 작은 구문형 자막이나 사용자가 켜고 끌 수 있는 SRT/CC가 적합하다.

YouTube는 업로드 자막을 권장하며 시청자가 글꼴, 크기, 색상과 배경을 조정할 수 있게 한다. W3C는 자막을 한두 줄로 유지하고, 문장을 나눌 때 논리적인 구문에서 끊으며, 중요한 화면 정보를 가리지 않도록 권장한다.

이 프로젝트에는 다음 조합을 권장한다.

- 화면 삽입 자막: 작고 정적인 구문형
- 별도 자막: SRT와 VTT를 계속 제공
- 단어별 색 추적: 사용하지 않음
- 강조가 꼭 필요한 문장은 영상 본문 타이포그래피로 처리

## 샘플 사양

- 1920x1080, 60fps, 첫 60초
- 44px, 700 weight
- 흰색 글자, 6px 검은 외곽선
- 하단 중앙, 한 줄 우선
- 빨간 단어 강조와 이동 효과 없음
- 문장부호, 쉼표, 발화 간격과 최대 글자 수를 이용한 구문 분리
- 기존 자막본과 클린 마스터는 보존

## 참고

- [YouTube 자동 자막 안내](https://support.google.com/youtube/answer/6373554)
- [YouTube 자막 표시 설정](https://support.google.com/youtube/answer/100078)
- [W3C 오디오·비디오 전사 가이드](https://www.w3.org/WAI/media/av/transcribing/)
- [W3C 자막이 화면 정보를 가리지 않아야 한다는 지침](https://www.w3.org/WAI/WCAG22/Understanding/captions-live)
- [YouTube Expressive Captions 발표](https://blog.youtube/news-and-events/expressive-captions/)

## 승인 및 적용

- 승인 샘플: `05_review/preview/2026-013-three-signals-0317-story-caption-sample-60s.mp4`
- 전체 출력: `06_delivery/youtube/2026-013-three-signals-0317-youtube-captioned-story.mp4`
- 공용 제작 규칙: 두 롱폼 제작 프로필 모두 이 스타일을 기본값으로 변경
- 과거 phrase/karaoke 렌더러는 기존 결과 재현용으로 보존
