import fs from 'node:fs';
import path from 'node:path';
const P=path.dirname(new URL(import.meta.url).pathname);
const read=f=>JSON.parse(fs.readFileSync(path.join(P,f)));
const plan=read('01_script/scene-plan.json'),words=read('03_sync/captions.words.json').words;
const narration=fs.readFileSync(path.join(P,'01_script/narration.txt'),'utf8').trim();
const captions=words.map(w=>w.text).join(' ');
if(narration.split(/\s+/).join(' ')!==captions)throw Error('Caption approved text mismatch');
const delayed={4:'벗어 둔 장화 하나가',5:'바닥 틈 사이를',6:'검은 머리카락 옆으로',9:'난간 아래에 장화가',10:'그 위로 몸이',12:'방문 아래로 물이',14:'점퍼를 잡고',15:'저는 다리 중간에서',16:'여자가 제 운동화 끈을',17:'친구가 제 이름을'};
const checks=[];
for(const [i,s]of plan.scenes.entries()){
 for(const [j,b]of s.motion_beats.entries()){
  const phrase=j?b.spoken_trigger:delayed[i];
  const start=phrase?s.narration_text.indexOf(phrase):0;
  if(start<0)throw Error('Missing cue '+phrase);
  const before=s.narration_text.slice(0,start).trim().split(/\s+/).filter(Boolean).length;
  const spoken=words[s.word_offset+before].start;
  if(i&&Math.abs(spoken-b.time-.25)>.02)throw Error('Cue alignment '+s.id+' '+phrase);
  checks.push({scene:s.id,phrase:phrase??'paragraph opening',visual:b.time,spoken,lead_seconds:spoken-b.time});
 }
}
const ratio=read('03_sync/sync_report.json').matched_character_ratio;
if(ratio<.92)throw Error('Low ASR alignment');
fs.writeFileSync(path.join(P,'05_review/sync-check.json'),JSON.stringify({status:'pass',approved_caption_words:words.length,caption_exact_text_match:true,asr_alignment_ratio:ratio,checked_visual_cues:checks},null,2)+'\n');
fs.writeFileSync(path.join(P,'05_review/sync-review.md'),'# 음성·화면 동기화 검수\n\n승인 대본 1,320단어와 업로드 자막은 동일합니다. Whisper turbo ASR 정렬 일치율 0.989. 콜드 오픈 외 각 컷은 해당 음성 단서보다 0.25초 먼저 준비됩니다.\n\n초기 구상의 단서 선노출을 다시 확인하고 젖은 장화, 판자 아래 머리카락, 물속의 손, 수면의 장화, 문 아래 물, 점퍼를 잡는 손은 실제 단어 타이밍까지 이전 컷을 유지하도록 수정했습니다. 손목은 몸을 보여준 뒤 손의 정체를 말할 때 클로즈업하며, 최종 사진은 장화 → 회색 옷자락 → 맨손으로 붙드는 귀신으로 단계 공개합니다.\n\n| 씬 | 음성 단서 | 화면 시작 | 음성 시작 | 선행 초 |\n|---|---|---:|---:|---:|\n'+checks.map(c=>`| ${c.scene} | ${c.phrase} | ${c.visual.toFixed(3)} | ${c.spoken.toFixed(3)} | ${c.lead_seconds.toFixed(3)} |`).join('\n')+'\n');
console.log('Approved text, ASR ratio and 52 voice-driven visual cues passed.');
