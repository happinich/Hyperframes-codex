# 음성 검수 기록

- 승인 원고: `01_script/narration.txt`와 별도 `01_script/shorts-narration.txt`.
- 모델·보이스: ElevenLabs `eleven_v3`, Esther `dJlwSfdSqMaQjm3NSl3B`.
- 원본 본편: `02_audio/inbox/2026-024-seance-one-room-narration.mp3`, 약 642.4초. 긴 무음 99건, 평균 89.9어절/분으로 목표 6~8분을 초과했다.
- 보존본: 원본 MP3와 `02_audio/working/voice-original.wav`를 유지한다.
- 현재 본편 목소리 단독 검수본: `02_audio/working/voice-review.mp3` 및 `02_audio/working/voice.wav`, 약 469.1초. 0.5초 이상 쉼을 0.25초 남기고 다듬은 뒤 피치 유지 속도 보정. 앞 약 82.36초는 1.15배, 이후는 1.28배.
- Whisper: `mlx-community/whisper-large-v3-turbo`, 대본 일치율 98.91%, 요구치 92% 초과. 대본은 Whisper 출력으로 바꾸지 않았다.
- 페이싱: 평균 123.1어절/분, 0.8초 초과 무음 0건, 긴 단어 간격 5건, 말미의 느린 창 1건. 초반 빠른 창의 일부를 1.15배 구간으로 완화했다.
- 쇼츠: 독립 Esther V3 음성, 피치 유지 1.07배와 첫 음절 전 0.1초 패드. Whisper 대본 일치율 100%. 본편 음성과 프레임을 발췌하지 않음.
- 2026-10-01 재검수: 사용자의 자체 검수·완료 위임에 따라 승인 대기를 해소. 목소리 단독 WAV 469.071초, 48kHz 스테레오, 평균 -17.5dB·최대 -3.5dB로 클리핑 없음. Whisper 일치율 98.91%, 0.8초 초과 무음 0건, 긴 단어 간격 5건은 문장 호흡 위치로 확인. 청각 감상 자체는 도구 환경에서 수행할 수 없어 발음·감정의 주관적 평가는 주장하지 않는다.
- BGM 후보 4개 중 최초 선택한 `cand-04`의 원곡 평균 음량은 -44.7dB여서 최종 여운 평균이 -57.7dB로 너무 약했다. 최종 검수에서 제외하고 형광등 험과 낮은 드론의 `cand-01`(원곡 평균 -19.9dB)을 선택했다. `scripts/apply_bgm.py`로 목소리 아래 -18dB, 말미 4초 -14dB 및 3초 페이드 적용. 새 여운은 평균 -35.8dB·최대 -18.7dB로 확인. 목소리 단독 마스터는 변경하지 않았다.
- 공간음과 사건 효과음은 `make-sound-design.py`로 생성한 `room-ambience.wav`, `event-foley.wav`를 별도 소스로 유지한다. 원고의 도어락 4회·5회 음절 시각에 맞춘 낮은 신호음, 포장지·문 소리를 최종 믹스에 추가했다. 렌더용 `04_composition/assets/audio/voice.wav`는 473.071초, 평균 -17.2dB·최대 -3.1dB. 인코딩된 본편 AAC의 최대는 -2.7dB로 클리핑 없음.
- 쇼츠 믹스: 같은 최종 후보를 -22dB 아래 배치, 21.495초. 별도 대본과 신규 세로 이미지를 사용한다.
