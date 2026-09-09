import fs from 'node:fs';
import path from 'node:path';
const root=path.dirname(new URL(import.meta.url).pathname);
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const write=(p,v)=>fs.writeFileSync(path.join(root,p),typeof v==='string'?v:JSON.stringify(v,null,2)+'\n');
if(process.argv[2]==='init'){
 const source=path.resolve(root,'../../planning',path.basename(root));
 for(const n of ['narration.txt','scene-plan.md','script-review.md'])fs.copyFileSync(path.join(source,'01_script',n),path.join(root,'01_script',n));
 fs.copyFileSync(path.join(root,'01_script/narration.txt'),path.join(root,'01_script/tts-narration.txt'));
 const c=read('02_audio/elevenlabs-request.json');c.request.voice_id='jB1Cifc2UQbq1gR3wnb0';delete c.bgm;write('02_audio/elevenlabs-request.json',c);
 fs.appendFileSync(path.join(root,'00_brief/brief.md'),'\n## Final production authorization\n\nUser authorized the reviewed script, recommended Bin voice, horror_cinematic style, autonomous BGM selection, full production and final GitHub push. Content nature: fiction. All numeric speech is Korean. No additional approval requested.\n');
 const text=fs.readFileSync(path.join(root,'01_script/narration.txt'),'utf8').trim();
 const anchors=['로봇청소기가 거실','지난겨울에','이상한 알림이','그런데 다음 날 새벽','그래서 충전기','다음 날 저는 관리사무소','저도 친구 집','새벽 두 시 십삼 분.','제가 보고 있는 게','카메라는 바닥','그런데 화면 속 손','그 말이 끝나자','저는 현관문','다음 날 집주인','저는 친구 집에','그런데 일주일 뒤','잠시 뒤, 침대'];
 const images=['wall','room','debris','room','cabinet','plan','room','tracks','wall','entity','hand','entity','stairs','wall','bedroom','bedroom','bedroom'];
 const modes=['hook','none','map','map','none','blueprint','none','none','none','camera','none','none','none','none','none','map','ending'];
 const p=read('01_script/scene-plan.json');let time=0;
 p.horror_direction={threat_type:'explicit_ghost',entity_design:'Grey pajamas, dry plaster skin, faded floral wallpaper attached to face, flattened sideways body, long fingers.',reveal_mode:'trace_to_camera_to_direct',reveal_beats:['debris','camera silhouette','hand contact','wall emergence']};
 const offset=a=>text.startsWith(a)?0:text.indexOf('\n\n'+a)+2;
 p.scenes=anchors.map((a,i)=>{const start=offset(a);const end=i+1<anchors.length?offset(anchors[i+1]):text.length;if(start<0||end<=start)throw Error(a);const narration=text.slice(start,end).trim();const d=narration.split(/\s+/).length/130*60;const s={id:'S'+String(i+1).padStart(2,'0'),type:modes[i],start_seconds:time,end_seconds:time+d,duration_seconds:d,narration_text:narration,caption_text:narration,purpose:a,visual:images[i],motion:'Narration-timed camera move, focus and local light modulation every 2.5 seconds',motion_beats:[],audio:{ambience:'quiet apartment room tone',foley:[],bgm:'autonomous selection authorized'},transition_out:'crossfade',shorts_adaptation:'standalone teaser'};time+=d;return s;});write('01_script/scene-plan.json',p);
 write('01_script/shorts-narration.txt','로봇청소기가 우리 집에 없는 방을 청소했어요.\n\n솔에는 처음 보는 꽃무늬 벽지가 감겨 있었죠.\n\n관리인은 카메라를 절대 켜지 말라고 했습니다.\n\n그런데 청소기가 벽 속에 끼어 버렸어요.\n\n정지 버튼도 안 먹혔죠.\n\n저는 뭐에 걸렸는지 보려고, 그 카메라를 켰습니다.\n');
 fs.copyFileSync(path.join(root,'01_script/shorts-narration.txt'),path.join(root,'01_script/shorts-tts-narration.txt'));
 write('02_audio/shorts-elevenlabs-request.json',{...c,script_source:'../01_script/shorts-narration.txt',tts_script_source:'../01_script/shorts-tts-narration.txt',target_audio:'inbox/'+path.basename(root)+'-shorts.mp3'});
 for(const d of ['04_composition/assets/visuals','05_review/logs','05_review/frames'])fs.mkdirSync(path.join(root,d),{recursive:true});
}
