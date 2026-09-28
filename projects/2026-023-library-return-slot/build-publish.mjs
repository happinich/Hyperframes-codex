import fs from 'node:fs';
import path from 'node:path';

const P = path.dirname(new URL(import.meta.url).pathname);
const id = path.basename(P);
const plan = JSON.parse(fs.readFileSync(path.join(P,'01_script/scene-plan.json'),'utf8'));
const mmss = t => `${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
const title = '도서관 야간 근무 중, 반납함에서 들린 책장 소리 | 창작 공포';
const chapterNames = [
  [0,'반납함에서 나온 손'],[1,'평범했던 야간 근무'],[3,'아무도 없는 반납함'],
  [4,'표지 없는 책'],[6,'제자리로 돌아온 책'],[8,'종이로 만든 손'],
  [10,'방화문 아래의 종이'],[12,'유리창 너머의 형체'],[14,'가위와 붉은 책갈피'],
  [16,'계단으로 이어진 것'],[18,'남겨 둔 운동화'],[20,'점검 중인 반납함'],[21,'코트 주머니의 소리'],
];
const chapters = chapterNames.map(([i,label])=>`${mmss(plan.scenes[i].start_seconds)} ${label}`).join('\n');
const description = `밤에 아무도 도서관에 오지 않았습니다. 그런데 비어 있던 반납함에서 책장 넘기는 소리가 났어요. 제가 밀어 둔 표지 없는 책은 다시 제자리로 돌아왔습니다.\n\n야간 근무자 한 사람의 시점으로 들려주는 창작 공포 이야기입니다. 종이 손이 나타나기 전부터 공간과 단서를 따라가 보세요.\n\n타임스탬프\n${chapters}\n\n작품 안내\n이 이야기는 창작 허구입니다. 실제 도서관, 인물, 사건을 재현한 영상이 아닙니다. AI 생성 이미지와 음성을 활용했습니다.\n\n다음 이야기는 채널의 공포괴담 재생목록에서 이어집니다.\n\n#무서운이야기 #도서관괴담 #공포괴담 #창작공포 #어둠속이야기`;
const time = '실험용 게시 시간: 한국 시간 오후 10시. 쇼츠는 본편 공개 다음 날 오후 8시 30분을 우선 테스트하세요. 최적 시간이라는 확정값이 아니라 초기 가설입니다. 채널의 실제 시청자 활동·유지율 데이터가 쌓이면 조정하세요. 업로드 또는 예약은 실행하지 않았습니다.';
const longBlocks = [
  ['메인 제목',title],
  ['추천 제목 5가지','1. 아무도 오지 않은 반납함에서 책장 소리가 났어요\n2. 도서관에서 표지 없는 책을 발견한 뒤 벌어진 일\n3. 밀어 둔 책이 반납함으로 다시 돌아왔습니다\n4. 야간 도서관, 방화문 아래로 종이가 들어왔어요\n5. 그날 반납함에는 사람이 아닌 것이 있었습니다'],
  ['설명란',description],
  ['태그','무서운이야기,도서관괴담,공포괴담,창작공포,귀신이야기,심야도서관,반납함괴담,종이손,한국괴담,공포라디오,오디오드라마,어둠속이야기'],
  ['고정 댓글','가장 먼저 이상하다고 느낀 순간은 언제였나요? 빈 반납함의 책장 소리, 다시 돌아온 책, 방화문 아래의 종이 중 하나를 골라 주세요. ※ 이 작품은 창작 공포입니다.'],
  ['X 홍보문','아무도 오지 않은 도서관 반납함에서 책장 소리가 났어요.\n밀어 둔 표지 없는 책은 다시 상자 안으로 돌아왔습니다.\n창작 공포 「심야 도서관 반납함」\n[본편 공개 URL 입력]\n#공포괴담 #무서운이야기'],
  ['Threads 홍보문','야간 근무 중이었어요.\n반납함 앞에는 아무도 없었는데 책장 넘기는 소리가 났습니다.\n표지 없는 책을 옆으로 밀어 놨죠. 그런데 돌아보니 다시 받침 상자 안에 서 있었어요.\n창작 공포 「심야 도서관 반납함」\n[본편 공개 URL 입력]'],
  ['Instagram 홍보문','아무도 없던 도서관 반납함에서 책장이 넘어갔어요.\n다시 돌아온 건 책만이 아니었습니다.\n창작 공포 「심야 도서관 반납함」 본편은 프로필의 유튜브 링크에서.\n#무서운이야기 #도서관괴담 #공포괴담 #창작공포'],
  ['업로드 체크','1920x1080 / 60fps 클린 MP4\nSRT 또는 VTT 자막 별도 업로드 (본편 번인 없음)\n카테고리: 엔터테인먼트\n창작 공포 및 AI 이미지·음성 사용 표기\n마지막 18초에 관련 공포괴담 영상 또는 재생목록 엔드스크린 지정\n공개 URL 입력 후 SNS 홍보문 게시\n쇼츠 공개 후 관련 동영상으로 이 본편 지정'],
  ['추천 게시 시간',time],
];
const shortTitle = '아무도 없는데 반납함에서 책장 소리가 났어요 #공포괴담';
const shortBlocks = [
  ['쇼츠 제목',shortTitle],
  ['추천 제목 5가지','1. 표지 없는 책이 반납함으로 돌아왔어요\n2. 아무도 오지 않은 도서관에 책 한 권이 생겼습니다\n3. 방화문 아래로 책갈피가 넘어왔어요\n4. 닫힌 문 밑에서 종이가 접히기 시작했습니다\n5. 도서관 반납함에서 들린 이상한 소리'],
  ['설명란','아무도 오지 않은 도서관 반납함에서 책장 넘기는 소리가 났습니다. 표지 없는 책을 밀어 두자 다시 돌아왔어요. 닫힌 문 아래의 종이는 왜 움직였을까요?\n\n아래 관련 동영상에서 전체 이야기가 이어집니다. 독립 대본·새 음성·새 세로 이미지로 만든 창작 공포 티저입니다. AI 이미지·음성을 활용했습니다.\n\n#쇼츠 #무서운이야기 #도서관괴담 #공포괴담'],
  ['태그','공포쇼츠,도서관괴담,반납함괴담,무서운이야기,창작공포,어둠속이야기'],
  ['고정 댓글','문 아래에서 접히던 종이는 결국 어떻게 됐을까요? 아래 관련 동영상으로 본편을 이어 보세요.'],
  ['본편 연결',`YouTube Studio → 쇼츠 → 관련 동영상\n정확한 대상: ${title}\n프로젝트: ${id}\n본편 공개 후 지정하세요. 쇼츠 설명란 URL만으로 연결하지 않습니다.`],
  ['추천 게시 시간',time],
];
const esc = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function build(kind, blocks) {
  const video = path.join(P,`06_delivery/${kind}/${id}-${kind}.mp4`);
  if (!fs.existsSync(video)) throw new Error('Video not rendered: '+video);
  const isShort = kind === 'shorts';
  const all = blocks.map(([heading,body])=>heading+'\n'+body).join('\n\n');
  const thumbnails = isShort ? '' : '<section><h2>썸네일 2가지</h2><div class="thumbs"><a href="thumbnail-a.jpg"><img src="thumbnail-a.jpg" alt="반납함의 손"></a><a href="thumbnail-b.jpg"><img src="thumbnail-b.jpg" alt="책이 돌아왔다"></a></div></section>';
  const cards = blocks.map(([heading,body],i)=>`<section><div class="row"><h2>${esc(heading)}</h2><button data-copy="block-${i}">복사</button></div><pre id="block-${i}">${esc(body)}</pre></section>`).join('');
  const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${isShort?'쇼츠':'유튜브'} 게시 도우미 · 심야 도서관 반납함</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b151c;color:#edf4f5;font-family:system-ui,sans-serif;line-height:1.7}main{max-width:1000px;margin:auto;padding:32px 22px 70px}header,section{padding:24px;border:1px solid #37505b;border-radius:16px;margin:18px 0;background:#162832}header{background:linear-gradient(120deg,#18313c,#382b2b)}h1{font-size:30px;line-height:1.35}h2{font-size:20px;margin:0}.row{display:flex;align-items:center;justify-content:space-between;gap:12px}button,a.link{display:inline-block;background:#254b59;border:1px solid #57808e;color:#fff;border-radius:10px;padding:10px 15px;margin:5px 5px 5px 0;text-decoration:none;cursor:pointer;font-size:15px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}video{width:100%;max-height:570px;background:#05090b}.thumbs{display:grid;grid-template-columns:1fr 1fr;gap:15px}.thumbs img{width:100%;border-radius:9px}small,p{color:#bfd0d8}#status{display:none;position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#e9fff6;color:#173425;padding:10px 20px;border-radius:10px}@media(max-width:600px){main{padding:15px 12px}header,section{padding:17px}.thumbs{grid-template-columns:1fr}}
</style></head><body><main><header><small>어둠 속 이야기 · 창작 공포</small><h1>${isShort?'쇼츠':'유튜브'} 게시 도우미</h1><p>심야 도서관 반납함 · ${isShort?'독립 쇼츠':mmss(plan.duration_seconds)+' 본편'} · 60fps</p><button id="copy-all">게시 내용 전체 복사</button></header><section><h2>완성 영상</h2><video controls preload="metadata" src="../../06_delivery/${kind}/${id}-${kind}.mp4"></video><a class="link" href="../../06_delivery/${kind}/${id}-${kind}.mp4">영상 파일</a><a class="link" href="../../03_sync/${isShort?'shorts-':''}captions.srt">SRT 자막</a><a class="link" href="../../03_sync/${isShort?'shorts-':''}captions.vtt">VTT 자막</a></section>${thumbnails}${cards}<p>실제 업로드 및 예약은 실행하지 않았습니다.</p></main><div id="status" role="status"></div><script>const ALL=${JSON.stringify(all).replaceAll('<','\\u003c')};async function copyText(t){let ok=false;try{await navigator.clipboard.writeText(t);ok=true}catch{}if(!ok){const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.left='-9999px';document.body.append(a);a.select();ok=document.execCommand('copy');a.remove()}const s=document.getElementById('status');s.textContent=ok?'복사했습니다':'선택하여 복사해 주세요.';s.style.display='block';setTimeout(()=>s.style.display='none',2400)}document.getElementById('copy-all').onclick=()=>copyText(ALL);document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>copyText(document.getElementById(b.dataset.copy).textContent));</script></body></html>`;
  fs.writeFileSync(path.join(P,`07_publish/${kind}/${kind}-publish.html`),html);
  fs.writeFileSync(path.join(P,`07_publish/${kind}/${kind}-publish.md`),'# '+(isShort?'쇼츠':'유튜브')+' 게시 패키지\n\n'+blocks.map(([h,b])=>'## '+h+'\n\n'+b).join('\n\n')+'\n');
}
build('youtube',longBlocks);
build('shorts',shortBlocks);
fs.writeFileSync(path.join(P,'07_publish/publish-data.json'),JSON.stringify({main_title:title,short_title:shortTitle,chapters,content_nature:'fiction',upload_executed:false},null,2)+'\n');
console.log('Publishing helpers generated for long-form and original Short.');
