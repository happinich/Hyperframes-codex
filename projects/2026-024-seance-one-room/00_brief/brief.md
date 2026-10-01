# 강령술 원룸: 넷째 목소리

- Project ID: `2026-024-seance-one-room`
- Created: `2026-09-30`
- Primary format: YouTube 16:9 (1920x1080, 60fps)
- Secondary format: Shorts 9:16 (1080x1920, separately adapted)
- Face policy: 얼굴 노출 없음. 원룸·손·기기 중심의 생성 이미지와 그래픽 사용.
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

셋이 모인 원룸에서 넷째 목소리와 손이 나타나는 6~8분 창작 공포 단편을 제작한다. 본편에서 존재와 친구의 배신을 확인시키고, 독립 쇼츠로 스포일러 없이 본편에 유입시킨다.

## 시청자

한국어 현대 생활 공포와 일인칭 괴담을 듣는 시청자.

## 한 문장 메시지

한 번 눈을 뜬 사람을 따라붙는 존재는 다음 사람을 부르기 전까지 떠나지 않는다.

## 톤과 시각 방향

추천 화면 스타일 `horror_cinematic` 승인. 차가운 편의점 간판 빛, 좁은 원룸, 수저·도어락·휴대폰 단서를 선명하게 보여 준다. Esther 여성 보이스의 절제된 일인칭 낭독. 화면 자막 없는 본편과 별도 업로드용 SRT/VTT.

## 작품 성격과 연결

- Content nature: `fiction` · 창작 공포
- Threat type: `explicit_ghost`
- Entity design: 차갑고 검은 손과 네 손가락. 카메라 화면에서 먼저 보이고 실제 손목에 접촉한다. 얼굴과 몸통은 보여 주지 않는다.
- Reveal mode: `trace_to_partial_to_direct`
- Reveal beats: 넷째 목소리·여분 수저 / 손목의 네 줄·이불 자국 / 카메라 속 손 / 실제 손목 접촉
- Series or playlist: `공포괴담 본편` 후보
- Cold-open line: “우리는 분명 셋이었어요. 그런데 제 오른쪽 귀 바로 옆에서, 누군가 아주 작게 말했습니다. 넷.”
- Normal-world setup: 금요일 과제를 마친 대학 동기 셋이 좁은 원룸에서 배달 음식을 먹고 영화를 보기로 한다.
- First anomaly window: 40~60초
- Narration style: 사람이 직접 경험을 들려주는 존댓말 구술형 이야기체. 종결을 자연스럽게 섞고 했다·였다 단문을 연속하지 않음.
- Long-form burned captions: 기본 없음, 별도 승인 시에만 생성
- Shorts cliffhanger: 별도 승인된 `01_script/shorts-narration.txt`. 도어락 네 번에서 끝나는 완전한 문장. 정체·배신·결말은 공개하지 않음.
- Related long-form video for Shorts: 이 프로젝트 본편. 업로드 후 YouTube Related Video에서 연결.
- Long-form end-screen target: `공포괴담 본편` 재생목록 후보. 게시 전 실제 대상 확인.
- Submission permission or source notes: 사용자가 제공한 `강령술_원룸.txt`를 기반으로 한 창작 대본. 외부 원본의 영상·음성·이미지는 사용하지 않음.
