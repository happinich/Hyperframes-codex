# Gyeorina V3 샘플 검수

- Voice ID: `1gYuTfEwELcoEo96wnGj`
- Model: `eleven_v3`
- Duration: 29.92초
- BGM: 없음
- 최종 청취 후보: `gyeorina-horror-sample-v3-v2.mp3`

## 결과

- 숫자 발음: 통과
  - `세 시 십칠 분` → Whisper `3시 17분`
  - `사백사 호` → Whisper `404호`
  - `팔 년` → Whisper `8년`
  - `세 번` → Whisper `3번`
- `오래된 별관`, `전화기 너머`: 정확히 인식
- 문장 반복: 없음
- 누락 문장: 없음
- Whisper가 `호출등`을 `호출둔`으로 인식했으므로 직접 청취 시 해당 단어만 확인한다.

첫 생성본은 마지막 대사를 반복해 비교 대상에서 제외했다. 두 번째 생성본은 반복 없이 전체 문장이 한 번씩만 출력됐다.
