# 밤낚시 중, 물속 여자가 제 장화를 신고 올라왔어요

- Project ID: `2026-022-reservoir-boots`
- Created: `2026-09-27`
- Primary format: YouTube 16:9 (1920x1080, 60fps)
- Secondary format: Shorts 9:16 (1080x1920, separately adapted)
- Face policy: 화자와 친구의 얼굴은 노출하지 않음. 귀신은 젖은 머리카락으로 얼굴을 가린 실사풍 생성 이미지.
- Production profile: `horror_cinematic_story_v1` · 호러 시네마틱 스토리형
- Profile description: 한국의 일상 공간에서 시작해 귀신·괴물·현대 규칙 공포를 균형 있게 다루는 6~8분 단편을 콜드 오프닝, 단계적 존재 공개, 시네마틱 이미지 모션, 다층 사운드와 무스포 쇼츠 유입 구조로 제작하는 방식.
- Approved visual style: `horror_cinematic` · 호러 시네마틱
- Visual mood: 한국의 익숙한 야간 공간이 서서히 낯설어지고, 중후반에는 귀신이나 괴물의 실재가 확인되는 몰입형 공포 오디오 드라마
- Background: 어두운 병원 복도, 원룸 현관, 산길, 젖은 도로, CCTV 화면처럼 단서와 초자연 존재의 윤곽이 읽히는 저조도 실사·생성 이미지
- Palette: #020407, #071318, #10252a, #e8edf0, #ff334f
- Layout language: 풀블리드 시네마틱 이미지, 단서 클로즈업, CCTV·호출 패널·휴대전화 프레임, 짧은 경고 타이포를 이야기 감정선에 맞춰 교차한다.
- Motion density: 정지 이미지도 1~3초마다 줌, 패닝, 초점, 조명, 스캔, 그림자 중 하나가 변하고 3초 이상 완전 정지를 금지한다.
- Captioned renderer: `scripts/burn_story_captions.mjs`
- Captioned derivative default enabled: `false`
- Script mode: `cold_open_modern_horror_single_story`
- Opening rule: 첫 5~10초에 가장 위험하거나 이상한 대사 한 줄을 선제시한 뒤 장소와 정상 규칙을 앉히고, 40~60초 사이에 첫 이상 징후에 진입한다.
- Narration rule: 화면을 설명하는 메타 멘트 없이, 사람이 겪은 일을 청자에게 들려주듯 자연스러운 존댓말 구술형 이야기체로 쓴다. ~했어요, ~였죠, ~거든요, ~더라고요와 필요한 ~했습니다를 감정과 호흡에 따라 섞고, 했다·였다 단문을 연속하지 않는다. 귀신·괴물 축에서는 흔적, 부분 노출, 직접 상호작용 순으로 존재를 확인시키며 한 영상에서 6~8분 공포 한 편을 완결한다.
- Sound rule: 내레이션을 중심으로 공간 앰비언스, 사건 효과음, 승인된 BGM을 분리 설계하고 반전 직전 의도적 적막을 씬 플랜에 표시한다.
- Voice generation: ElevenLabs API.
- Timing policy: 기획 단계부터 초 단위 씬 타임라인을 작성하고, MLX Whisper turbo로 실제 발화 시간만 보정.

## 목표

승인된 창작 공포 한 편을 10분 30초~11분 목표로 제작. 장화, 손자국, 물속 존재의 직접 접촉을 단계적으로 보여 주고 독립 쇼츠로 연결.

## 시청자

몰입형 한국어 공포 이야기를 듣는 성인 시청자.

## 한 문장 메시지

밤낚시 좌대의 사라진 장화가 물속 여자의 손에 끼워져 돌아온다.

## 톤과 시각 방향

Bin 남성 구술형 나레이션. 푸른 저수지 수면과 따뜻한 좌대 전구를 대비하고 빨간 찌와 왼쪽 장화의 파란 테이프를 반복 단서로 사용.

## 작품 성격과 연결

- Content nature: `fiction` / 창작 공포
- Threat type: `explicit_ghost`
- Entity design: 젖은 검은 머리카락으로 얼굴이 가려진 성인 여성, 회색 니트. 손을 장화 안에 넣어 다가오며 후반에는 맨손으로 직접 붙잡음.
- Reveal mode: `trace_to_partial_to_direct`
- Reveal beats: 초반 흔적 / 중반 부분 노출 / 후반 직접 상호작용
- Series or playlist:
- Cold-open line:
- Normal-world setup: 장소에 간 이유와 정상적인 공간·업무 규칙
- First anomaly window: 40~60초
- Narration style: 사람이 직접 경험을 들려주는 존댓말 구술형 이야기체. 종결을 자연스럽게 섞고 했다·였다 단문을 연속하지 않음.
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger candidate: 문을 닫기 전에 빈 장화 한 짝이 난간 위로 올라오는 완결 문장. 정체·탈출·사진 결말은 공개하지 않음.
- Related long-form video for Shorts: 본 프로젝트의 「밤낚시 중, 물속 여자가 제 장화를 신고 올라왔어요 | 저수지 공포괴담」. 실제 공개 후 YouTube 관련 동영상으로 지정.
- Long-form end-screen target: 채널 공포괴담 본편 재생목록 또는 다음 이야기, 마지막 18초.
- Submission permission or source notes: 외부 실화·제보를 사용하지 않은 창작. 생성 이미지 및 AI 내레이션 사용.
