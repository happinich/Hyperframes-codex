# {{TITLE}}

- Project ID: `{{PROJECT_ID}}`
- Created: `{{CREATED_DATE}}`
- Primary format: YouTube 16:9 (1920x1080, 60fps)
- Secondary format: Shorts 9:16 (1080x1920, separately adapted)
- Face policy: 얼굴 노출 없음. 그래픽, 타이포그래피, 아이콘, 화면 목업만 사용.
- Production profile: `{{PRODUCTION_PROFILE_ID}}` · {{PRODUCTION_PROFILE_LABEL}}
- Profile description: {{PRODUCTION_PROFILE_DESCRIPTION}}
- Approved visual style: `{{VISUAL_STYLE_ID}}` · {{VISUAL_STYLE_LABEL}}
- Visual mood: {{VISUAL_STYLE_MOOD}}
- Background: {{VISUAL_STYLE_BACKGROUND}}
- Palette: {{VISUAL_STYLE_PALETTE}}
- Layout language: {{PRODUCTION_PROFILE_LAYOUT}}
- Motion density: {{PRODUCTION_PROFILE_MOTION}}
- Captioned renderer: `{{PRODUCTION_PROFILE_CAPTION_RENDERER}}`
- Captioned derivative default enabled: `{{PRODUCTION_PROFILE_CAPTION_DEFAULT_ENABLED}}`
- Script mode: `{{PRODUCTION_PROFILE_SCRIPT_MODE}}`
- Opening rule: {{PRODUCTION_PROFILE_OPENING_RULE}}
- Narration rule: {{PRODUCTION_PROFILE_NARRATION_RULE}}
- Sound rule: {{PRODUCTION_PROFILE_SOUND_RULE}}
- Voice generation: ElevenLabs API.
- Google Drive delivery: 최종 검수 후 프로젝트별 폴더에 롱폼 메인 MP4·게시 전략·썸네일·쇼츠를 함께 업로드하고 파일명·용량·폴더를 검증한다. 원본 정책은 `publishing_rules.google_drive_delivery`.
- Voice casting: 처음 원고를 제안할 때부터 이야기별로 남성·여성 중 우선 추천·음색·이유·대안을 기록한다. 합본 전체를 여성으로 자동 지정하거나 기계적인 성별 순환을 적용하지 않는다. 캐스팅 성별을 먼저 정한 뒤 실제 보이스를 고른다.
- Female voice first choice: `config/success-rules.json`의 `audio_rules.voice_preferences.female_first_choice`에 기록된 Jian.K. 사용자 청취 승인일 2026-10-15. 여성 화자 선택 시 실제 ID를 `02_audio/elevenlabs-request.json`에 적용하고 작품별 명시적 선택이 있으면 우선.
- Timing policy: 기획 단계부터 초 단위 씬 타임라인을 작성하고, MLX Whisper turbo로 실제 발화 시간만 보정.

## 공포 합본 형식

- 전체 목표 길이: `config/horror-channel-strategy.json`의 20~40분. 편당 길이는 서사에 맞춰 결정.
- 편수: 기본 세 편, 두 긴 서사가 각각 완결 구조를 갖추면 두 편. 편수 선택 이유를 기록.
- 편별 제목·원고·씬 플랜·공포 유형·비주얼 스타일 승인·쇼츠 대본을 별도로 기록.
- 편 사이 전환과 마지막 엔드스크린 구간을 총 길이에 포함.

## 목표

작성 예정.

## 시청자

작성 예정.

## 한 문장 메시지

작성 예정.

## 톤과 시각 방향

작성 예정.

공포 프로젝트는 [9가지 스타일 가이드](../../../docs/HORROR_VISUAL_STYLES.ko.md)를 참고해 아래 내용을 기록합니다.

- 우선 추천 스타일과 이야기 적합 이유:
- 대안 1~2개와 장단점:
- 밝기·팔레트·질감·모션·모바일 단서 가독성:
- 최근 작품과의 다양성 검토:
- 최종 선택 이유:
- 해당 이야기의 스타일 승인 또는 명시적 선택 위임 근거:
- 본편·쇼츠·썸네일의 시각 언어 일관성 계획:

## 이야기별 보이스 캐스팅

원본 규칙: `script_rules.horror_story.voice_casting_review`. 첫 원고 제안 때부터 편별로 작성합니다. 주인공 성별이 고정되지 않았다면 그 사실을 밝히고, 직업만으로 성별을 정하지 않습니다.

| 이야기 | 우선 추천 성별·음색 | 시점·감정선에 맞는 이유 | 다른 성별 대안과 장단점 | 주인공 성별 고정 여부 | 실제 보이스·승인 근거 |
| --- | --- | --- | --- | --- | --- |
| 작성 예정 | 작성 예정 | 작성 예정 | 작성 예정 | 작성 예정 | 선택 대기 |

여성 1순위 Jian.K는 여성 캐스팅을 선택한 편에 적용합니다. 남성 후보는 해당 원고 샘플의 발음·호흡·문장 반복·과장 여부를 확인한 뒤 선정합니다. 본편과 그 이야기의 별도 쇼츠는 같은 캐스팅을 기본으로 검토합니다.

## 이야기별 편집 방향

공포 프로젝트는 [편집 기법 가이드](../../../docs/HORROR_EDITING_TECHNIQUES.ko.md)를 따라
`01_script/editing-plan.json`에 선택을 기록합니다. 승인된 원고·비주얼 범위 안의
편집 선택은 에이전트가 이야기별로 진행하고, 실제 지시는 씬 플랜에 연결합니다.

- 핵심 단서와 긴장 단계:
- 주된 기법 ID와 적합 이유:
- 필요한 보조 기법 ID와 적용 장면:
- 제외할 기법과 이유:
- 선택 스타일의 재료·움직임에 맞춘 조절:
- 최근 작품과의 반복·다양성 검토:
- 별도 쇼츠에 맞춘 선택과 스포일러 방지:
- 같은 공간의 카메라 구성: 전체 공간 / 관찰·행동 / 핵심 디테일 등 이야기별 위치·각도·높이 계획. 단순 크롭·흔들림은 다른 촬영 위치로 세지 않음.
- 다른 시점을 위한 새 이미지 자산 / 반복 구도의 의도와 기준 컷:
- 화면 글자 방식과 근거: 제목·시간·단서 문구와 나레이션 전체 번인 자막을 구분. 글자 없음도 의도와 검토 근거를 기록.
- 두 차례 검수 기록: `05_review/editing-review.md`

## 작품 성격과 연결

- Content nature: `fiction` / `adapted_submission` / `verified_account`
- Threat type: `explicit_ghost` / `creature_or_unknown_entity` / `modern_rule_horror` / `psychological_or_mystery_horror`
- Entity design: 외형·의복·표면·움직임 규칙. 존재가 없으면 `none`.
- Reveal mode: `trace_to_partial_to_direct` / `implicit_only`
- Reveal beats: 초반 흔적 / 중반 부분 노출 / 후반 직접 상호작용
- Series or playlist:
- Cold-open line:
- Normal-world setup: 장소에 간 이유와 정상적인 공간·업무 규칙
- First anomaly window: 40~60초
- Narration style: 사람이 직접 경험을 들려주는 존댓말 구술형 이야기체. 종결을 자연스럽게 섞고 했다·였다 단문을 연속하지 않음.
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger candidate: 정체·반전·결말 공개 전 중단 지점
- Related long-form video for Shorts:
- Long-form end-screen target:
- Submission permission or source notes:

## 2026-10-18 사용자 상시 제작 위임

사용자 지시: “앞으로 작업은 추천되로 진행해줘. 나한테 안물어봐도되.” 현재 및 이후 Hyperframes 제작에서는 원고, 편별 남녀 캐스팅과 실제 보이스, 비주얼 스타일, 음성 검수 판단, BGM, 편집, 썸네일, 쇼츠 및 납품을 추천안에 따라 진행하고 같은 선택을 재질문하지 않는다. 기존의 각 검토 단계와 품질 기준은 유지하되 사용자 답변 대기 대신 위임 근거·실제 선택·이유·검수 결과를 각각 기록한다. 이후 프로젝트별 사용자 명시 지시가 우선하며 완료 프로젝트는 보존한다.
