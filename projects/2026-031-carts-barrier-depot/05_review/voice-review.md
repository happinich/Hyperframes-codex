# 현재 검수 상태

사용자의 2026-10-18 상시 위임으로 후속 추천을 확정했다. 현재 음성은 clarity revision 이후 버전이며 아래 초기 청취 패키지는 역사 자료다. 직접 청취 판정은 수행하지 않았다. 현재의 근거는 voice-spot-check/, final-audio-signal-review.json, 00_brief/script-approval.json이다. 추가 사용자 답변 대기 상태가 아니다.

---

# 031 음성 청취 검수

화면은 카트=거친 2D / 방음벽=어두운 회화 / 차고지=픽셀아트로 승인됐다. 화자는 C01 Jian.K, C02·C03 동일 Hyuk으로 확정됐다.

## 약 90초 청취 모음

카트 → 방음벽 → 차고지 순서로 각 편의 평상시 구술과 긴장 구간을 묶었다. 실제 생성한 본편에서 뽑았으며 원래 1.00배속, BGM 없음.

![세 편 음성 청취 모음](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/three-story-listening-preview.mp3)

## 본편 전체

| 이야기 | 보이스 | 길이 | 청취 파일 |
|---|---|---|---|
| 카트 | Jian.K | 6분 52초 | [전체 음성](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/C01-preview.mp3) |
| 방음벽 | Hyuk | 6분 50초 | [전체 음성](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/C02-preview.mp3) |
| 차고지 | Hyuk | 6분 55초 | [전체 음성](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/C03-preview.mp3) |

## 별도 쇼츠 음성

각 약 20.5초. 원본 생성 뒤 피치 보존 1.07x 후처리. 본편과 같은 화자다.

- [카트 쇼츠](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/SH01-preview.mp3)
- [방음벽 쇼츠](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/SH02-preview.mp3)
- [차고지 쇼츠](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/SH03-preview.mp3)

## 검수 결과와 남은 확인

- 본편 정렬 일치율 C01 99.65%, C02 99.42%, C03 99.12%. 자동 기준 92%를 통과했다. 별도로 반복·삽입 검사를 했다.
- C01의 두 누락 의심은 짧은 구간 재분석으로 원음에 있는 것을 확인하고 타이밍을 보정했다.
- C02 첫 테이크는 실제 반복·뒤섞임이 있어 제외하고, 이전 요청 ID만 연결한 새 테이크로 대체했다. SH02 반복 첫 문장과 추가 끝 문장은 제거했고 재분석에서 원고가 한 번씩 나오는 것을 확인했다.
- C03 5분 43초 부근의 ‘바퀴 자국’은 Whisper가 ‘다큐 자국’으로 인식한다. 별도 문장 생성에서도 같은 인식이 나와 원본을 유지했다. 이 구간의 실제 발음을 청취해 확인해야 한다.

  ![차고지 바퀴 자국 발음 확인](/Volumes/WorkSpace/Projects/ChatGPT/Hyperframs-co/projects/2026-031-carts-barrier-depot/05_review/voice-review/C03-wheel-pronunciation-check.mp3)
- C02 문장 사이 0.80초, SH03 문장 사이 0.82초 간격은 이야기 호흡으로 유지했다. 0.8초를 넘는 완전 무음은 최종 선택 음성에서 검출되지 않았다.
- 청취본은 세 편 음량을 정적 게인으로 약 -23 LUFS에 맞췄다. 음성 원본·배속 원본은 보존했다. 직접 귀로 듣고 음색·연기·의도치 않은 배경음을 판정한 상태는 아니다.
- 음성 기준 본편은 두 5초 전환과 4초 BGM 여운을 포함해 약 20분 50초 예정. 장면 내부 숏·효과의 발화 지점 검토와 최종 편집에 따라 달라질 수 있다.

제작 규칙의 ‘음성 검수 후 BGM 후보 생성’ 순서에 따라 청취 확인을 기다린다. BGM 후보는 아직 생성하지 않았으며 화면·최종 영상 제작도 진행 중이다.
