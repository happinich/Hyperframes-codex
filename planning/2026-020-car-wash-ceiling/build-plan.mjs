import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const dir = path.join(root, '01_script');
const narration = fs.readFileSync(path.join(dir, 'narration.txt'), 'utf8').trim();
fs.writeFileSync(path.join(dir, 'tts-narration.txt'), narration + '\n');
const paragraphs = narration.split(/\n\s*\n/);
const visuals = [
  ['경고 선공개', '차 안에서 앞유리 상단의 손가락', '계기판을 보는 주인공의 굳은 손'],
  ['마감과 첫 물소리', '세차장 세 칸과 연속 지붕 전경', '마른 끝 칸의 물방울'],
  ['물의 출처', '잠긴 수도꼭지와 마른 호스', '배수구의 동그란 물자국과 휴대전화'],
  ['당겨지는 머리카락', '밀대에 걸린 머리카락', '위로 당겨지는 머리카락과 놓친 장갑 손'],
  ['카메라 확인', '움직이지 않는 비닐 깃발', '모니터 바닥에 흔들리는 그림자'],
  ['첫 신체 노출', '렌즈를 덮는 창백한 손', '유리창 너머 철골에 거꾸로 붙은 발'],
  ['관리인에게 연락', '책상 아래 연락처와 휴대전화', '주인공의 낮은 시점과 사무실 문'],
  ['조명 경고', '한쪽만 꺼진 끝 칸 형광등', '잠근 사무실 문과 창밖 어둠'],
  ['사무실 접근', '문 위 머리카락과 내려가는 손잡이', '문 밑으로 흐르는 검은 물'],
  ['천장 침입', '들린 천장판과 손가락', '측문과 가까운 세단 운전석'],
  ['차량 피신', '낮게 달리는 주인공과 열린 운전석', '찌그러지는 차량 내장재와 실내등'],
  ['앞유리의 여자', '흰 SUV와 붉은 후미등', '분홍 소매의 손과 와이퍼까지 내려온 머리카락'],
  ['시선 유혹', '계기판 아래로 내린 시선', '얼굴을 가린 머리카락 뒤 불분명한 윤곽'],
  ['탈출 시작', '후미등을 따라 구르는 차량 바퀴', '앞유리에서 떨어지는 손과 꺼지는 진입로 조명'],
  ['출구 차단', '두 차량 사이 천장에 붙은 발', '반대로 접히는 무릎 일부와 분홍 옷자락'],
  ['작업등', '뒤쪽 칸부터 어두워지는 사이드미러', '작업등 빛을 피하는 발과 열린 통로'],
  ['창문 공격', '유리에 미끄러지는 손바닥', '몰딩을 벌리는 손가락과 앞으로 튀는 차'],
  ['관리인 위기', '지붕 밖 세단과 안쪽 흰 SUV 위치', '창문으로 당겨지는 관리인의 팔'],
  ['손전등 회수', '운전석 옆 손전등과 앞유리 물자국', '지붕 바깥에서 방향을 바꾸는 세단'],
  ['빛으로 구조', '유리 반사를 가리며 비추는 두 손', '철골을 잡고 거꾸로 접혀 올라가는 여자'],
  ['탈출 뒤 증거', '공도 옆 두 차량', '잿빛 손가락 자국이 남은 관리인 손목'],
  ['남은 흔적', '낮에 드러난 지붕의 긴 자국', '밖으로 뒤집힌 창문 몰딩'],
  ['수리점의 잔상', '몰딩에서 끝없이 나오는 머리카락', '빈 조수석 위 내장재에 번지는 젖은 자국'],
];
if (paragraphs.length !== visuals.length || /\d/.test(narration)) throw Error('Paragraph or numeral mismatch');
const words = s => s.split(/\s+/).length;
const targetVoice = 642;
const opening = 9;
const restWords = paragraphs.slice(1).reduce((n, s) => n + words(s), 0);
let start = 0;
const scenes = paragraphs.map((text, i) => {
  const duration = i === 0 ? opening : (targetVoice - opening) * words(text) / restWords;
  const end = i === paragraphs.length - 1 ? targetVoice : start + duration;
  const scene = {
    id: `s${String(i + 1).padStart(2, '0')}`, type: 'horror_story',
    start_seconds: +start.toFixed(3), end_seconds: +end.toFixed(3),
    duration_seconds: +(end - start).toFixed(3), estimated_words: words(text),
    target_wpm: +(words(text) / duration * 60).toFixed(1), purpose: visuals[i][0],
    narration_text: text, caption_text: text,
    visual: visuals[i].slice(1), image_count: i === 1 ? 4 : 2,
    additional_images: i === 1 ? ['운전석 옆 손전등', '마지막 손님이 나가는 입구'] : [],
    motion: '단서에 맞춰 느린 팬/줌과 초점 이동. 2.4초 간격의 미세 조명/가림 변화. 귀신 전체를 조기 노출하지 않는다.',
    motion_beats: [{offset_seconds: 0, action: '장소/단서 설정'}, {offset_seconds: 2.4, action: '단서 쪽 초점 또는 빛 이동'}, {offset_seconds: +(duration / 2).toFixed(3), action: '두 번째 독립 시점으로 전환'}],
    audio: {narration: 'Bin 추천, 승인 대기', ambience: '잔잔한 야외 전기/도로 소음', foley: visuals[i][0], bgm: '음성 검수 후 후보 승인'},
    transition_out: '대사 단어 타이밍에 맞춰 컷. 단서 선행 최대 0.35초',
    shorts_adaptation: i >= 10 && i <= 12 ? '별도 티저 재구성 후보' : '본편 전용',
  };
  start = end;
  return scene;
});
const plan = {project_id: '2026-020-car-wash-ceiling', status: 'draft_awaiting_script_approval', content_nature: 'fiction', production_profile: 'horror_cinematic_story_v1', visual_style: 'horror_cinematic', visual_style_status: 'proposed_not_approved', voice_status: 'proposed_not_approved', timing_source: 'estimated_word_weighted_not_audio_aligned', target_total_seconds: 646, narration_seconds_estimate: 642, bgm_outro_seconds: 4, width: 1920, height: 1080, fps: 60, image_count: 48, scenes};
fs.writeFileSync(path.join(dir, 'scene-plan.json'), JSON.stringify(plan, null, 2) + '\n');
const clock = seconds => `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
fs.writeFileSync(path.join(dir, 'scene-plan.md'), '# 초 단위 장면 계획\n\n모든 시간은 녹음 전 추정입니다. 목표 10분 46초이며 실제 음성으로 다시 정렬합니다.\n\n| 예상 구간 | 사건 | 이미지 |\n| --- | --- | --- |\n' + scenes.map(s => `| ${clock(s.start_seconds)}–${clock(s.end_seconds)} | ${s.purpose} | ${s.visual.join(' / ')} |`).join('\n') + '\n\n공간 소개 네 장, 나머지 단락 두 장씩 총 48장. 마지막 18초 오른쪽 엔드스크린 영역 확보. 물소리는 도입 약 40~50초 지점에 배치하며 실제 음성에서 재확인한다.\n');
fs.writeFileSync(path.join(dir, '대본-전체검토.md'), '# 세차장 천장의 여자\n\n창작 공포 · 약 10분 30초~11분 목표 · 전체 대본 검토본\n\n추천 보이스: Bin 남성. 음성은 아직 생성하지 않았습니다.\n\n## 본편 전체 대본\n\n' + narration + '\n\n## 쇼츠 별도 대본 · 승인 대기\n\n' + fs.readFileSync(path.join(dir, 'shorts-narration.txt'), 'utf8') + '\n\n## 제작 방향 · 별도 승인 대기\n\n호러 시네마틱: 차가운 형광등, 붉은 후미등, 젖은 철골과 유리. 본편 이미지 48장 계획, 60fps. 실제 길이는 녹음 후 확정합니다.\n');
console.log(JSON.stringify({paragraphs: paragraphs.length, words: words(narration), plannedVoiceSeconds: targetVoice, impliedWpm: words(narration) / targetVoice * 60, images: scenes.reduce((n,s)=>n+s.image_count,0)}));
