# 고시원 공용 샤워실, 칸막이 아래 발이 두 켤레였다

- Project ID: `2026-017-goshiwon-shower`
- Created: `2026-09-02`
- Primary format: YouTube 16:9 (1920x1080, 60fps)
- Secondary format: Shorts 9:16 (1080x1920, separately adapted)
- Face policy: 얼굴 노출 없음. 그래픽, 타이포그래피, 아이콘, 화면 목업만 사용.
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
- Narration rule: 화면을 설명하는 메타 멘트 없이 짧고 감각적인 했다체를 기본으로 쓴다. 귀신·괴물 축에서는 흔적, 부분 노출, 직접 상호작용 순으로 존재를 확인시키며 한 영상에서 6~8분 공포 한 편을 완결한다.
- Sound rule: 내레이션을 중심으로 공간 앰비언스, 사건 효과음, 승인된 BGM을 분리 설계하고 반전 직전 의도적 적막을 씬 플랜에 표시한다.
- Voice generation: ElevenLabs API.
- Timing policy: 기획 단계부터 초 단위 씬 타임라인을 작성하고, MLX Whisper turbo로 실제 발화 시간만 보정.

## 목표

약 칠 분 안에 심야 고시원 공용 샤워실의 원혼이 흔적, 부분 노출, 직접
접촉 순으로 확인되는 단편을 완결한다. 첫 훅 이후 약 오십 초 안에 첫
이상을 제시하고, 회색 슬리퍼·보일러 빨간불·칸막이 아래 발로 위협을 교체한다.

## 시청자

늦은 밤 혼자 공포·도시괴담·귀신 이야기를 듣는 한국어 시청자.

## 한 문장 메시지

자기 것이 아닌 젖은 슬리퍼가 칸 앞에 있으면, 그 칸에는 이미 누군가 들어와 있다.

## 톤과 시각 방향

얼굴 없는 고시원 귀신 호러 시네마틱. 탁한 청록 형광등과 젖은 베이지 타일을
기본으로 두고, 보일러 빨간불과 회색 슬리퍼만 제한적으로 붉게 강조한다.
발, 머리카락, 등, 손목 순으로 존재를 보여 주되 얼굴은 머리가 가린다.

## 작품 성격과 연결

- Content nature: `fiction`
- Threat type: `explicit_ghost`
- Entity design: 항상 젖은 긴 검은 머리가 얼굴을 가린 원혼. 물에 불고 마른 등, 하얗게 불어 있는 발과 손목, 회색 고무 슬리퍼. 타일 위를 끌리듯 이동하고 물속에서 호수를 부른다.
- Reveal mode: `trace_to_partial_to_direct`
- Reveal beats: 맨발 물자국과 혼자 켜진 보일러 / 거울 안쪽 손자국 / 같은 방향의 창백한 발과 머리카락 / 칸막이 위 젖은 등과 손목 접촉 / 새 집 배수구와 문 아래 슬리퍼
- Series or playlist: `공포괴담 본편` · `귀신 괴담` · `주거 괴담`
- Cold-open line: `샤워실 칸막이 아래에 발이 두 켤레였다. 그런데 그 칸에는 나만 들어가 있었다.`
- Normal-world setup: 야간 물류 알바가 역 앞 고시원 삼백칠 호에 살며 왼쪽 칸만 쓰는 일상, 가운데 칸과 젖은 슬리퍼 금지
- First anomaly window: 40~60초
- Narration style: 했다체
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger candidate: 칸막이 아래 발이 두 켤레인 지점. 등·손목·호수 음성·사고 내막은 공개하지 않음
- Related long-form video for Shorts: `고시원 공용 샤워실, 칸막이 아래 발이 두 켤레였다`
- Long-form end-screen target: `텐트 밖에서 친구 목소리를 흉내 내는 것` 또는 `공포괴담 본편` 재생목록
- Submission permission or source notes: 실존 인물·고시원·사건과 무관한 완전한 창작 괴담

## 승인 및 자동 진행 기록

- 전체 대본: 사용자 승인 및 추천 순위 자동 진행 (`2026-09-02`)
- 제작 프로필: `horror_cinematic_story_v1`
- 비주얼 스타일: `horror_cinematic`
- 내레이션 보이스: Esther (`dJlwSfdSqMaQjm3NSl3B`)
- 음성·영상·BGM: 추천 순위 자동 진행. 음성과 영상은 각각 두 회 검수
- 완료 조건: 본편·쇼츠·게시 패키지 검수 후 관련 파일만 Git 커밋 및 GitHub 푸시
