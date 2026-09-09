# 연출 노트: {{TITLE}}

`narration.txt`에는 읽을 문장만 넣고, 이 파일에는 발음·호흡·연출 지시를 적습니다.

## ElevenLabs 지시

- Voice:
- API model: `eleven_v3`
- Language code: `ko`
- Output format: `mp3_44100_128`
- Pace:
- Emotion:
- Pronunciation notes:
- Required user inputs: `ELEVENLABS_API_KEY`, `voice_id`, 필요 시 `voice_settings`.

## 원고 변환 프롬프트 규칙

설명형 하이퍼프레임스 롱폼 성공 팁:

1. 초반 3초 후킹: 영상 시작 부분의 지루한 인사말이나 일반론은 삭제한다. 첫 문장은 시청자의 호기심을 자극하는 날카로운 질문형 문장, 핵심 수치, 또는 반전 사실로 시작한다.
2. 시각 자료 힌트 주입: 하이퍼프레임스에서 자막, 이미지, 그래프를 타이밍에 맞춰 띄우기 좋도록 문맥 중간에 "지금 화면에 나오는 이 부분을 보시면...", "이 수치가 의미하는 것은..." 같은 시각적 안내 멘트를 자연스럽게 삽입한다.
3. 구어체 텐션 극대화: 일레븐랩스 V3의 억양이 살아나도록 문장 끝을 완전한 대화체로 바꾼다. 예: "~아시죠?", "~거든요". 호흡이 늘어지지 않도록 문장은 짧고 타이트하게 쪼갠다.

프로필 전용 규칙:

- Script mode: `{{PRODUCTION_PROFILE_SCRIPT_MODE}}`
- Opening: {{PRODUCTION_PROFILE_OPENING_RULE}}
- Narration: {{PRODUCTION_PROFILE_NARRATION_RULE}}
- Sound: {{PRODUCTION_PROFILE_SOUND_RULE}}
- 공포 프로필에서는 설명형 시각 안내 멘트를 사용하지 않는다.
- 공포 프로필은 첫 5~10초 콜드 훅 뒤 장소와 정상 규칙을 앉히고 40~60초 사이 첫 이상 징후를 배치한다.
- 새 공포 대본은 사람이 경험을 직접 들려주는 존댓말 구술형 이야기체로 쓴다. `~했어요`, `~였죠`, `~거든요`, `~더라고요`, 필요한 `~했습니다`를 섞고 했다·였다 단문과 한 가지 종결의 반복을 피한다.
- 한 영상에 6~8분 이야기 한 편을 완결하며, 쇼츠는 정체·반전·결말을 공개하지 않는다.
- 귀신·괴물 축은 흔적, 부분 노출, 직접 상호작용 순으로 존재를 확인시키고 같은 얼굴·전신을 반복하지 않는다.

## 편집 메모

- 음악 방향:
- 위협 유형:
- 존재 디자인 및 움직임 규칙:
- 공개 단계별 핵심 장면:
- 핵심 이미지/도표:
- 출처 확인이 필요한 자산:
- 제작 프로필: `{{PRODUCTION_PROFILE_ID}}` · {{PRODUCTION_PROFILE_LABEL}}
- 프로필 설명: {{PRODUCTION_PROFILE_DESCRIPTION}}
- 레이아웃 문법: {{PRODUCTION_PROFILE_LAYOUT}}
- 프로필 모션 밀도: {{PRODUCTION_PROFILE_MOTION}}
- 원고 모드: `{{PRODUCTION_PROFILE_SCRIPT_MODE}}`
- 오프닝 기준: {{PRODUCTION_PROFILE_OPENING_RULE}}
- 내레이션 기준: {{PRODUCTION_PROFILE_NARRATION_RULE}}
- 사운드 기준: {{PRODUCTION_PROFILE_SOUND_RULE}}
- 목표 낭독 속도: {{PRODUCTION_PROFILE_TARGET_WPM_RANGE}} WPM
- 자막 적용 렌더러: `{{PRODUCTION_PROFILE_CAPTION_RENDERER}}`
- 자막 파생본 기본 활성화: `{{PRODUCTION_PROFILE_CAPTION_DEFAULT_ENABLED}}`
- 승인된 화면 스타일: `{{VISUAL_STYLE_ID}}` · {{VISUAL_STYLE_LABEL}}
- 화면 분위기: {{VISUAL_STYLE_MOOD}}
- 배경: {{VISUAL_STYLE_BACKGROUND}}
- 팔레트: {{VISUAL_STYLE_PALETTE}}
- 스타일별 모션: {{VISUAL_STYLE_MOTION}}
- 모션 기준: {{PRODUCTION_PROFILE_MOTION}}
