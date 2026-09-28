# 심야 도서관 반납함에서 나온 손

- Project ID: `2026-023-library-return-slot`
- Created: `2026-09-28`
- Primary format: YouTube 16:9 (1920x1080, 60fps)
- Secondary format: Shorts 9:16 (1080x1920, separately adapted)
- Face policy: 얼굴 노출 없음. 화자는 뒷모습 또는 손·발만 보이는 생성 실사 이미지로 표현.
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

폐관 후 도서관 반납함에서 나온 종이 존재와 직접 맞닥뜨리는 일인칭 현대 괴담을 제작한다. 창작 픽션이며 실화로 표기하지 않는다. 본편은 약 6~8분, 별도 각색 쇼츠는 15~40초를 목표로 한다.

## 시청자

일상 공간이 조금씩 낯설어지는 한국어 공포 이야기를 듣는 성인 시청자.

## 한 문장 메시지

반납함의 책장은 작업실 문을 닫아도 멈추지 않는다.

## 톤과 시각 방향

따뜻한 작업등에서 차가운 복도와 비상계단으로 이동한다. 회색 종이 주름, 붉은 천 책갈피, 파란 카트를 연속성 단서로 유지한다. 에스더 여성 보이스를 사용하고 본편 번인 자막은 만들지 않는다.

## 작품 성격과 연결

- Content nature: `fiction`
- Threat type: `creature_or_unknown_entity`
- Entity design: 회색 종이가 다층으로 접혀 손과 몸을 이루고, 납작한 책 표지 같은 얼굴 면이 있다. 얇은 종이와 붉은 천이 문틈을 통과한다.
- Reveal mode: `trace_to_partial_to_direct`
- Reveal beats: 초반 흔적 / 중반 부분 노출 / 후반 직접 상호작용
- Series or playlist: 어둠 속 이야기 / 일상 공간 괴담
- Cold-open line: 반납함에서 나온 종이 손이 제 발목을 붙잡았어요.
- Normal-world setup: 월말 도서관 야간 반납 도서 분류. 외부 반납함에서 작업실 받침 상자, 파란 카트, 복도, 비상계단으로 이어지는 동선.
- First anomaly window: 40~60초
- Narration style: 사람이 직접 경험을 들려주는 존댓말 구술형 이야기체. 종결을 자연스럽게 섞고 했다·였다 단문을 연속하지 않음.
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger candidate: 닫힌 방화문 아래로 종이가 접혀 나오기 시작하는 지점에서 중단
- Related long-form video for Shorts: 이 프로젝트의 완성된 본편. 게시 후 유튜브 Related Video 설정 필요.
- Long-form end-screen target: 같은 채널의 일상 공간 괴담 재생목록
- Submission permission or source notes: 직접 창작한 픽션. 외부 제출물 없음.
