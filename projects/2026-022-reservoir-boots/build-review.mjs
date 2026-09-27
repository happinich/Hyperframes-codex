import fs from 'node:fs';
import path from 'node:path';
import {execFileSync,spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const P=path.dirname(fileURLToPath(import.meta.url));
const manifest=JSON.parse(fs.readFileSync(path.join(P,'02_audio/bgm/candidates.json'),'utf8'));
const escape=t=>String(t).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const stats=manifest.candidates.map(c=>{
 const file=path.join(P,'02_audio/bgm/candidates',c.id+'.mp3');
 const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_format','-show_streams','-of','json',file],{encoding:'utf8'}));
 const result=spawnSync('ffmpeg',['-hide_banner','-i',file,'-af','volumedetect','-f','null','-'],{encoding:'utf8'});
 if(result.status!==0)throw Error('Audio decode failed: '+c.id);
 const mean=result.stderr.match(/mean_volume: ([-\d.]+) dB/),peak=result.stderr.match(/max_volume: ([-\d.]+) dB/);
 if(!mean||!peak)throw Error('Missing volume measurements: '+c.id);
 return {id:c.id,duration:Number(probe.format.duration),sample_rate:Number(probe.streams[0].sample_rate),channels:probe.streams[0].channels,mean_db:Number(mean[1]),peak_db:Number(peak[1])};
});
const levels=stats;
const notes=['기본 저역 드론 변형','저역 공명 변형','음량이 가장 절제된 변형'];
fs.writeFileSync(path.join(P,'05_review/bgm-audio-check.json'),JSON.stringify({status:'decoded_three_candidates',scope:'ffprobe duration/streams and ffmpeg volumedetect; not subjective listening',recommended:'cand-03',recommendation_basis:'Lowest measured mean and peak levels at the same configured -18 dB gain',candidates:stats.map(s=>({...s,...levels.find(v=>v.id===s.id)})),approved:false},null,2)+'\n');
const cards=manifest.candidates.map((c,i)=>`<section class="card ${c.id==='cand-03'?'recommended':''}" id="${escape(c.id)}"><div class="top"><h2>${escape(c.id)} · ${notes[i]}</h2>${c.id==='cand-03'?'<span class="badge">추천</span>':''}</div><p class="muted">원본 평균 ${levels[i].mean_db}dB / 피크 ${levels[i].peak_db}dB · 약 60초 생성 음악</p><p><strong>실제 목소리 + BGM 비교본</strong></p><audio controls preload="metadata" src="${escape(c.preview_href)}"></audio><p class="muted">전체 음성의 중후반에서 30초를 추출한 비교용입니다. 본편 영상 추출본이 아닙니다.</p><details><summary>BGM만 듣기 · 생성 조건 보기</summary><audio controls preload="none" src="${escape(c.bgm_href)}"></audio><p class="prompt">${escape(c.prompt)}</p></details><button type="button" data-copy="${escape(c.id)} 승인">${escape(c.id)} 승인 문구 복사</button></section>`).join('\n');
const page=`<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>저수지의 장화 · BGM 선택</title><style>
*{box-sizing:border-box}body{margin:0;background:#08151c;color:#edf6fa;font-family:system-ui,sans-serif;line-height:1.7}main{max-width:980px;margin:0 auto;padding:32px 24px 60px}h1{font-size:clamp(26px,5vw,38px);line-height:1.3}h2{font-size:21px;margin:0}.card{padding:24px;margin:22px 0;border:1px solid #395362;border-radius:17px;background:#152830}.recommended{border:2px solid #77cae2}.top{display:flex;gap:14px;justify-content:space-between;align-items:center;flex-wrap:wrap}.badge{border-radius:30px;background:#abddec;color:#0a2632;padding:3px 12px;font-weight:800}audio{width:100%;margin:8px 0}.muted{color:#b1c5cf;font-size:14px}a{color:#9dddf0}.prompt{font-size:13px;color:#afc3cf;overflow-wrap:anywhere}button{border:0;border-radius:9px;padding:12px 16px;background:#9fd7ea;color:#09222d;font-weight:800;cursor:pointer;margin-top:16px}button:focus-visible,a:focus-visible{outline:3px solid #f5d28e}.notice{padding:18px;border:1px solid #44616e;border-radius:12px}.eyebrow{font-size:13px;color:#a2bbc9}details{padding-top:9px}summary{cursor:pointer}#copy-status{min-height:24px}
</style></head><body><main><p class="eyebrow">창작 공포 · 2026-022-reservoir-boots · Bin 남성</p><h1>저수지의 장화<br>BGM 후보 비교</h1><p>이번 이야기를 위해 새로 생성한 세 후보입니다. 비교본은 음성 아래에 원본 BGM을 -18dB 낮추어 합성했습니다.</p><div class="notice"><strong>추천: cand-03</strong><p>동일 게인에서 측정된 평균과 최대 음량이 가장 낮아 목소리를 가리지 않는 선택으로 추천합니다. 이는 음색이나 공포감을 전편 청취 평가했다는 뜻은 아닙니다. 실제 비교본을 재생해 선택해 주세요.</p><p>선택 후 본편에서는 음성 종료 뒤 4초 여운, 마지막 3초 페이드아웃을 적용합니다. 아직 최종 BGM 합성이나 본편 렌더를 하지 않았습니다.</p></div>${cards}<p id="copy-status" role="status" aria-live="polite"></p><p><a href="voice-review.html">전체 음성과 장소 참고 이미지 보기</a></p><p class="muted">버튼은 승인 문구를 복사할 뿐 자동으로 승인·게시하지 않습니다. 이 대화에 선택한 후보를 알려 주세요.</p></main><script>
async function copyText(text){if(navigator.clipboard){try{await navigator.clipboard.writeText(text);return;}catch{}}const t=document.createElement('textarea');t.value=text;t.style.cssText='position:fixed;left:-9999px';document.body.append(t);t.select();const ok=document.execCommand('copy');t.remove();if(!ok)throw Error('복사를 사용할 수 없습니다.');}
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{try{await copyText(b.dataset.copy);document.getElementById('copy-status').textContent=b.dataset.copy+' · 복사했습니다. 대화에 붙여 넣어 주세요.';}catch(e){document.getElementById('copy-status').textContent=e.message+' '+b.dataset.copy;}}));
document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause();})));
</script></body></html>`;
fs.writeFileSync(path.join(P,'05_review/bgm-selection.html'),page);
console.log('BGM comparison helper generated.');
