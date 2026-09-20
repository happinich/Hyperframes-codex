# 세차장 천장의 여자

- Project ID: `2026-020-car-wash-ceiling`
- Created: `2026-09-20`
- Primary format: YouTube 16:9 (1920x1080, 60fps)
- Secondary format: Shorts 9:16 (1080x1920, separately adapted)
- Face policy: 화자 얼굴은 노출하지 않는다. 생성 실사 이미지와 귀신의 신체 일부를 사용한다.
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

단일 창작 공포 10분 30초~11분, 이미지 48장, 60fps. 기존 6~8분 기본값 대신 이번 프로젝트에 사용자 요청 길이를 적용한다. 쇼츠 최소 한 편을 별도 제작한다.

## 시청자

한국어 야간 공포 이야기 청취자.

## 한 문장 메시지

탈출한 줄 알았는데, 내가 숨었던 차의 천장이 그 여자의 새로운 자리가 됐다.

## 톤과 시각 방향

냉백색 형광등과 붉은 후미등, 빛이 닿는 경계에 버티는 손. 사용자 별도 질문 답변으로 Bin 남성과 추천 호러 시네마틱을 승인받았다. 이후 전체 검수와 진행을 위임받았다. 음성은 ASR/신호 검사로 검토하고 BGM cand-02를 선정했다. 본편의 생성 이미지 48장과 별개로 쇼츠 전용 이미지 6장을 새로 생성한다.

## 작품 성격과 연결

- Content nature: `fiction`
- Threat type: `explicit_ghost`
- Entity design: 젖은 검은 머리, 바랜 분홍 긴소매, 짙은 회색 바지, 맨발. 철골에 거꾸로 붙으며 빛을 피하지만 완전히 사라지지 않는다.
- Reveal mode: `trace_to_partial_to_direct`
- Reveal beats: 물과 머리카락 / 카메라의 손과 철골의 발 / 창문 침입과 관리인 공격 / 실내등의 손톱
- Series or playlist: 직업 괴담
- Cold-open line: 고개 들지 마요. 저 여자, 눈 마주치면 떨어져요.
- Normal-world setup: 장소에 간 이유와 정상적인 공간·업무 규칙
- First anomaly window: 기획 40~60초, 실제 첫 물자국 장면 약 36초. 승인 음성의 자연스러운 호흡을 유지하며 불필요한 정적을 추가하지 않는다.
- Narration style: 사람이 직접 경험을 들려주는 존댓말 구술형 이야기체. 종결을 자연스럽게 섞고 했다·였다 단문을 연속하지 않음.
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger: 앞유리의 손, 빈 조수석 숨소리, 눈맞춤 경고. 검수·진행은 사용자 위임. 탈출 방법과 마지막 반전은 공개하지 않는다.
- Related long-form video for Shorts: 2026-020-car-wash-ceiling 본편, 게시 URL 아직 없음
- Long-form end-screen target: 직업 괴담 재생목록 또는 2026-019 장례식장 편. 실제 공개 대상 확인 후 설정.
- Submission permission or source notes: 직접 창작. 실제 인물·시설·사건을 지칭하지 않는다.
