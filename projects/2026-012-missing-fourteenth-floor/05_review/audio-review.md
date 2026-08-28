# 음성 검수: 새벽 3시 17분, 아파트 한 층이 사라졌다

- 검수일: 2026-08-21
- 보이스: ElevenLabs Bin (`jB1Cifc2UQbq1gR3wnb0`)
- 모델: `eleven_v3`
- 생성 방식: 숫자를 한글 발음으로 변환한 뒤 문장 경계 기준 7개 청크 순차 생성 및 병합
- 원본 생성 길이: 21분 7.7초
- 최종 보정 길이: 18분 21.4초
- 보정 방식: 말소리 속도나 음높이는 바꾸지 않고 문장 사이 정적만 약 0.3초 남김
- 숫자 발음 보정 전 백업: `05_review/audio/voice-before-number-normalization.wav`
- 숫자 발음 보정 후 무음 정리 전 백업: `02_audio/working/voice-before-pacing-trim-number-normalized.wav`
- 최종 보이스 마스터: `02_audio/working/voice.wav`
- 청취용 MP3: `05_review/audio/voice-review-number-corrected.mp3`

## 자동 검수

- Whisper: `mlx-community/whisper-large-v3-turbo`
- 발음용 원고 일치율: 97.4% (`0.92` 기준 통과)
- 화면 자막 원문 일치율: 97.0%
- 평균 속도: 95.0 WPM
- 0.8초 이상 실제 무음: 0건
- 느린 15초 구간: 6건
- 0.8초 이상 단어 간격: 47건

## 수동 판정

`1401호`, `1402호`, `104동`, 날짜와 시각을 TTS 전용 원고에서 한글 발음으로 풀어 전체 음성을 다시 생성했다. 숫자 샘플과 전체 Whisper 전사에서 기존의 자릿수 오독 패턴이 제거됐다.
느린 구간과 단어 간격은 세대 번호 나열, 기록 낭독, 마지막 반전 문장에 집중되어 있어 공포 호흡으로 유지한다. 승인 대본과 화면 자막의 숫자 표기는 바꾸지 않았다. **숫자 발음 보정 음성 검수 통과**로 판정한다.

## 다음 단계

사용자가 BGM `cand-03`을 승인했다. 음성 전용 마스터는 보존하고, -18dB 더킹과 4초 아웃트로 및 3초 페이드아웃을 적용한 `voice-bgm.wav`를 영상에 사용한다.
