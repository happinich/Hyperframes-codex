# 텐트 밖에서 친구 목소리를 흉내 내는 것

- Project ID: `2026-016-camping-mimic`
- Created: `2026-08-31`
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

약 칠 분 안에 늦가을 산속 캠핑장의 고립감과 목소리 모방 괴물의 직접적인
위협을 완결한다. 첫 이상은 오십 초 안팎에 제시하고, 목소리와 그림자에서
시작해 손가락, 텐트 파손, 추격, 전신 확인 순으로 공포를 확대한다.

## 시청자

늦은 밤 도시괴담, 크리처 공포, 몰입형 오디오 콘텐츠를 듣는 한국어 시청자.

## 한 문장 메시지

친숙한 목소리가 들려도 눈으로 확인하기 전에는 절대 믿어서는 안 된다.

## 톤과 시각 방향

얼굴 없는 산속 크리처 호러 시네마틱. 비에 젖은 청록빛 숲과 따뜻한 주황색
텐트를 대비시키고, 괴물은 젖은 나무껍질 같은 표면과 비정상적으로 긴 팔,
뒤로 접히는 관절을 일관되게 유지한다. 흔적과 실루엣은 어둡게 시작하되
후반 전조등 장면에서는 외형과 움직임을 분명하게 확인시킨다.

## 작품 성격과 연결

- Content nature: `fiction`
- Threat type: `creature_or_unknown_entity`
- Entity design: 사람보다 한 머리 이상 큰 키, 젖은 나무껍질 같은 회갈색 표면, 무릎 아래까지 내려오는 팔, 뒤로 접히는 다리 관절, 눈 대신 깊은 구멍, 얼굴을 가로지르는 검은 틈. 입 대신 가슴에서 모방 음성이 나온다.
- Reveal mode: `trace_to_partial_to_direct`
- Reveal beats: 숲속 모방 음성 / 텐트 벽의 접힌 실루엣과 긴 손가락 / 텐트 파손과 추격 / 자동차 전조등 앞 전신 확인
- Series or playlist: `공포괴담 본편` · `괴물·미확인 존재`
- Cold-open line: `민수는 내 옆 침낭에서 자고 있었다. 그런데 텐트 밖에서도 민수 목소리가 들렸다.`
- Normal-world setup: 장소에 간 이유와 정상적인 공간·업무 규칙
- First anomaly window: 40~60초
- Narration style: 했다체
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger candidate: 텐트 안의 민수와 밖의 민수 목소리를 동시에 확인하는 지점
- Related long-form video for Shorts: `텐트 밖에서 친구 목소리를 흉내 내는 것`
- Long-form end-screen target: `공포괴담 본편` 재생목록 또는 `끝나지 않는 건조기 1분`
- Submission permission or source notes: 실존 인물·장소·사건과 무관한 완전한 창작 괴담

## 승인 및 자동 진행 기록

- 전체 대본: 사용자 사전 승인 (`2026-08-31`)
- 제작 프로필: `horror_cinematic_story_v1`, 사용자 사전 승인 위임
- 비주얼 스타일: `horror_cinematic`, 추천안 자동 선택
- 내레이션 보이스: Esther (`dJlwSfdSqMaQjm3NSl3B`), 최근 승인 보이스 유지
- 음성·영상·BGM: 사용자 사전 승인 위임. 자동 검수 두 회 통과 후 다음 단계 진행
- 완료 조건: 본편·쇼츠·게시 패키지 검수 후 관련 파일만 Git 커밋 및 GitHub 푸시
