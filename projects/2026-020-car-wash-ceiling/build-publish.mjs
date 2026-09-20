import fs from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
const P=path.dirname(new URL(import.meta.url).pathname),id=path.basename(P);
const plan=JSON.parse(fs.readFileSync(path.join(P,'01_script/scene-plan.json')));
const title='세차장 문을 닫으려는데, 천장에서 머리카락이 내려왔어요 | 공포괴담';
const stamp=t=>`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
const chapters=[[0,'고개 들지 마요'],[1,'세차장 마감'],[3,'위로 당겨지는 머리카락'],[5,'카메라를 가린 손'],[8,'머리 위의 발소리'],[10,'차 안으로'],[12,'빈 조수석의 숨결'],[15,'빛의 경계'],[17,'출구에 남은 사람'],[20,'그날 이후'],[22,'수리점에서']].map(([i,t])=>`${stamp(plan.scenes[i].start_seconds)} ${t}`).filter((x,i,a)=>i!==1||plan.scenes[1].start_seconds>=10).join('\n');
const duration=stamp(Math.round(plan.duration_seconds));
const description=`마지막 손님이 떠난 세차장. 바닥은 말랐는데 천장에서 물이 떨어졌어요.\n밀대에 걸린 머리카락을 잡자, 누군가 위에서 당겼습니다.\n차 문을 잠갔는데도 안심할 수 없었던 밤의 이야기입니다.\n\n타임스탬프\n${chapters}\n\n작품 안내\n이 영상은 어둠 속 이야기의 창작 공포입니다. 실제 인물·세차장·사건과 관련이 없습니다. AI 생성 이미지와 내레이션을 활용했습니다.\n과도하게 큰 음량은 피하고 편안한 음량으로 감상해 주세요.\n\n다음 이야기: 장례식장 야간 청소 첫날, 영정사진 속 여자가 나왔다\n채널의 공포괴담 본편 또는 직업 괴담 재생목록에서 이어서 감상해 주세요.\n\n#무서운이야기 #공포괴담 #세차장괴담 #귀신이야기 #어둠속이야기`;
const longBlocks=[
 ['메인 제목',title],
 ['추천 제목 5가지','1. 천장에서 내려온 머리카락을 잡으면 안 됐습니다 | 세차장 괴담\n2. 차 문을 잠갔는데, 빈 조수석에서 숨소리가 났다\n3. 야간 세차장 관리인이 고개를 들지 말라고 한 이유\n4. 아무도 없는 세차장, CCTV 렌즈를 가린 손\n5. 차 문을 잠갔는데, 천장이 내려앉기 시작했다'],
 ['설명란',description],
 ['태그','무서운이야기,공포괴담,세차장괴담,귀신이야기,야간알바,직업괴담,한국괴담,창작공포,공포라디오,오디오드라마,잠들기전괴담,어둠속이야기'],
 ['고정 댓글','차 밖에 손이 붙어 있는데, 차 안에서 숨소리가 난다면 어디를 먼저 보실 건가요? 가장 소름 돋았던 장면을 댓글로 남겨주세요.\n※ 창작 공포입니다. 다음 이야기는 채널의 공포괴담 본편 재생목록에서 이어집니다.'],
 ['X 홍보문','세차장 천장에서 내려온 머리카락을 잡았습니다.\n그런데 누군가 위에서 당겼어요.\n차 안으로 숨은 뒤가 더 무서웠습니다.\n\n창작 공포 「세차장 천장의 여자」\n[본편 공개 URL 입력]\n#공포괴담 #무서운이야기'],
 ['Threads 홍보문','마지막 손님까지 나간 세차장. 바닥은 말라 있는데 물이 떨어져요.\n호스를 잠그러 갔다가, 천장에서 내려온 머리카락을 잡았습니다.\n차 문을 잠그면 안전할 줄 알았는데요.\n\n이번 창작 공포는 「세차장 천장의 여자」입니다.\n[본편 공개 URL 입력]'],
 ['Instagram 홍보문','차 밖의 손. 차 안의 숨소리.\n야간 세차장 마감 중 시작된 창작 공포 「세차장 천장의 여자」\n전체 이야기는 프로필의 유튜브 링크에서 확인해 주세요.\n#공포괴담 #무서운이야기 #세차장괴담 #귀신이야기 #어둠속이야기'],
 ['업로드 체크','본편: 1920x1080 / 60fps 클린 MP4\n외부 SRT 또는 VTT 업로드\n카테고리: 엔터테인먼트\n창작 공포 및 AI 생성 이미지·음성 사용 표시\nYouTube의 변경·합성 콘텐츠 항목을 확인하고 해당하면 표시\n마지막 18초에 장례식장 편 또는 공포괴담 재생목록 엔드스크린 설정\n홍보문 URL 표시를 실제 공개 URL로 교체\n쇼츠 공개 후 관련 동영상으로 이 본편 지정'],
 ['추천 게시 시간','초기 실험 시간: 일요일 또는 수요일 오후 10시 (한국 시간)\n쇼츠는 본편 공개 후 다음 날 오후 8시 30분을 제안합니다.\n채널 실측 최적 시간은 아닙니다. YouTube Studio 시청자 활동 데이터가 충분하면 활발한 시간 30~60분 전으로 조정하세요.\n업로드 또는 예약은 실행하지 않았습니다.'],
];
const shortBlocks=[
 ['쇼츠 제목','천장에서 내려온 머리카락을 잡았다 #공포괴담'],
 ['설명란','세차장 천장에서 내려온 머리카락을 잡았어요. 누군가 위에서 당겼습니다.\n차 안으로 숨었는데 지붕이 내려앉기 시작했어요.\n고개를 들면 무슨 일이 생기는지, 아래 관련 동영상에서 이어집니다.\n\n독립 대본·새 음성·새 세로 이미지로 제작한 창작 공포 티저입니다. 본편 영상에서 추출하지 않았습니다. AI 생성 이미지·음성을 활용했습니다.\n#쇼츠 #공포괴담 #무서운이야기 #세차장괴담'],
 ['태그','공포쇼츠,세차장괴담,무서운이야기,귀신이야기,창작공포,어둠속이야기'],
 ['고정 댓글','문을 잠갔다고 안전할까요? 전체 이야기는 이 쇼츠의 관련 동영상에서 이어집니다.'],
 ['본편 연결',`YouTube Studio → 쇼츠 → 관련 동영상\n정확히 선택할 본편: ${title}\n프로젝트: ${id}\n본편이 공개된 뒤 지정하세요. 설명란 URL만으로 연결하지 않습니다.`],
 ['추천 게시 시간','본편이 공개된 다음 날 오후 8시 30분 (한국 시간).\n채널 데이터가 적을 때의 실험 시간이며 최적 시간 보장은 아닙니다. 실제 예약은 실행하지 않았습니다.'],
];
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
for(const [format,blocks] of [['youtube',longBlocks],['shorts',shortBlocks]]){
 const short=format==='shorts', label=short?'쇼츠 게시 도우미':'유튜브 게시 도우미',filename=short?'shorts':'youtube';
 const all=blocks.map(([h,t])=>h+'\n'+t).join('\n\n');
 const html=`<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${label} · 세차장 천장의 여자</title><style>*{box-sizing:border-box}body{margin:0;background:#0b1419;color:#edf3f5;font-family:system-ui,sans-serif;line-height:1.75}main{max-width:1000px;margin:auto;padding:40px 22px 80px}header{padding:30px;background:linear-gradient(130deg,#20333d,#301e28);border-radius:22px}h1{font-size:30px;line-height:1.4}h2{font-size:20px;margin:0}p,small{color:#b9c9cf}button,a.link{display:inline-block;border:1px solid #47727a;background:#203b44;color:white;padding:11px 18px;border-radius:10px;cursor:pointer;font-size:15px;text-decoration:none;margin:5px 6px 5px 0}section{padding:24px;margin:20px 0;background:#152229;border:1px solid #30434d;border-radius:16px}.row{display:flex;justify-content:space-between;align-items:center;gap:15px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;margin:18px 0 0}video{width:100%;max-height:580px;background:#05080b;border-radius:12px}.thumbs{display:grid;grid-template-columns:1fr 1fr;gap:15px}.thumbs img{width:100%;border-radius:10px}#status{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);padding:10px 20px;border-radius:10px;background:#e8fff4;color:#10261e;display:none}@media(max-width:600px){main{padding:20px 12px}header,section{padding:18px}.thumbs{grid-template-columns:1fr}.row{align-items:flex-start}h1{font-size:25px}}</style></head><body><main><header><small>어둠 속 이야기 · 창작 공포</small><h1>${label}</h1><p>세차장 천장의 여자 · ${short?'새 이미지로 만든 독립 티저':duration+' 본편'} · 60fps</p><button id="copy-all">게시 내용 전체 복사</button><a class="link" href="../${short?'youtube/youtube':'shorts/shorts'}-publish.html">${short?'본편':'쇼츠'} 게시 도우미</a></header><section><h2>완성 영상</h2><video controls preload="metadata" src="../../06_delivery/${format}/${id}-${format}.mp4"></video><a class="link" href="../../06_delivery/${format}/${id}-${format}.mp4">영상 파일 열기</a><a class="link" href="../../03_sync/${short?'shorts-':''}captions.srt">SRT 자막</a><a class="link" href="../../03_sync/${short?'shorts-':''}captions.vtt">VTT 자막</a></section>${short?'':`<section id="thumbnails"><h2>썸네일 두 가지</h2><div class="thumbs"><a href="thumbnail-a.jpg"><img src="thumbnail-a.jpg" alt="고개 들지 마"></a><a href="thumbnail-b.jpg"><img src="thumbnail-b.jpg" alt="차 안에 누구"></a></div></section>`}${blocks.map(([h,t],i)=>`<section><div class="row"><h2>${esc(h)}</h2><button data-copy="block-${i}">복사</button></div><pre id="block-${i}">${esc(t)}</pre></section>`).join('')}<p>실제 업로드·자동 게시·예약은 실행하지 않았습니다.</p></main><div id="status" role="status"></div><script>const ALL=${JSON.stringify(all).replaceAll('<','\\u003c')};async function copyText(t){let ok=false;try{await navigator.clipboard.writeText(t);ok=true}catch{}if(!ok){const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.left='-9999px';document.body.append(a);a.select();ok=document.execCommand('copy');a.remove()}const s=document.getElementById('status');s.textContent=ok?'복사했습니다':'복사하지 못했습니다. 내용을 선택해 복사하세요.';s.style.display='block';setTimeout(()=>s.style.display='none',2600);return ok}document.getElementById('copy-all').onclick=()=>copyText(ALL);document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>copyText(document.getElementById(b.dataset.copy).textContent));</script></body></html>`;
 fs.writeFileSync(path.join(P,`07_publish/${format}/${filename}-publish.html`),html);
 fs.writeFileSync(path.join(P,`07_publish/${format}/${filename}-publish.md`),'# '+label+'\n\n'+blocks.map(([h,t])=>'## '+h+'\n\n'+t).join('\n\n')+'\n');
}
for(const k of ['a','b'])await sharp(path.join(P,`04_composition/assets/visuals/thumbnail-${k}.png`)).resize(1280,720,{fit:'cover'}).jpeg({quality:94}).toFile(path.join(P,`07_publish/youtube/thumbnail-${k}.jpg`));
fs.writeFileSync(path.join(P,'07_publish/publish-data.json'),JSON.stringify({main_title:title,chapters,content_nature:'fiction',upload_executed:false},null,2)+'\n');
