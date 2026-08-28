# 오디오 검수 기록

- 검수일: 2026-08-14
- 최종 상태: 컴포지션 제작 가능
- 보이스: ElevenLabs `Bin`
- 모델: `eleven_v3`
- 최종 길이: 19분 13.031초
- 평균 낭독 속도: 108.0 WPM
- Whisper 모델: `mlx-community/whisper-large-v3-turbo`
- 대본 일치율: 97.9%
- 0.8초 이상 실제 무음: 0곳
- 1.0초 초과 단어 간격: 0곳
- 1.5초 이상 늘어진 단어: 0개

## 보정 내용

1. 최초 7개 청크 음성은 문장 사이 정적이 반복되어 원본 길이가 21분 44.891초까지 늘어났다.
2. 최초 생성 MP3와 보정 전 WAV를 보존하고, 문장 사이 호흡이 약 0.7초 안에 들어오도록 무음 구간을 정리했다.
3. 7번째 청크 일부가 최초 생성에서 누락된 것을 발견해 518자와 433자의 두 파트로 다시 생성했다.
4. 재생성한 마지막 청크는 단독 Whisper 검수에서 99.1% 일치, 미매칭 토큰 0개를 기록했다.
5. 장문 Whisper의 반복 인식 오류를 막기 위해 이전 구간 문맥 조건을 비활성화하고 전체 음성을 다시 정렬했다.

## 보존 파일

- 최초 API 병합본: `02_audio/inbox/2026-010-sixth-guest-narration-before-repair.mp3`
- 최종 보정 MP3: `02_audio/inbox/2026-010-sixth-guest-narration.mp3`
- 최초 정규화 WAV: `02_audio/working/voice-before-pacing-trim.wav`
- 마지막 청크 교체 전 WAV: `02_audio/working/voice-before-last-chunk-repair.wav`
- 최종 영상용 WAV: `02_audio/working/voice.wav`

## 판정

자동 속도 보고서의 0.8초 기준 경고는 63곳이지만 모두 0.80~0.98초 범위의 문장 끝 호흡이다. 실제 무음은 없고 1초를 넘는 단어 간격도 없어 공포 내레이션의 자연스러운 템포로 수동 승인한다.
