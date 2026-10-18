"""Retime approved narration and camera clues from child Whisper word artifacts."""
import json, subprocess, difflib, sys
from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parents[1]
sys.path.insert(0,str(R/'scripts'))
from align_captions import normalized, make_cues, write_captions, TimedToken
def read(f): return json.loads(f.read_text())
def save(f,d): f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def duration(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(f)],text=True))
anchors={
'C01':[
('', '그쪽에는'),('', '오른쪽에는'),('고장 카트 손잡이에는','닿지도 않은'),('', '테이프 위에는'),('', '손전등으로'),('이번에는 카트들이','빨간 카트는 그대로였는데'),('', '틈 아래로'),('', '앞 카트가 쇠말뚝에'),('', '그 손이 앞쪽을'),('빨간 카트가 대열에서','저는 바닥에 떨어진 체인을'),('젖은 운동화가 카트 아래에서','그 손이 제 손목을'),('저는 체인의 다른 끝을','빨간 카트가 더 밀자','그 손이 손목을 놓았습니다'),('같이 돌아왔을 때','직원은 제 손목에'),('', '저는 전날 찍은 사진을'),('지금도 마트에 가면','그런데 한 번씩')],
'C02':[
('', '그건 벽의 아래쪽에'),('', '점검로 왼쪽에는'),('', '그러자 소리도'),('', '틈 바닥에는'),('동료가 도로에서','그 전에 분필선'),('몇 걸음 걸었는데','그 순간 제가'),('계단 앞에','얇은 회색 조각이'),('그가 알아듣기 전에','그제야 소리가'),('회색 등판 같은 것이','저는 뒤를 돌아볼'),('그 밑에서 회색 마디','다른 마디가 난간을'),('저는 몸을 멈춘 채','저는 드라이버를'),('작업화 한 짝을','작업등에 비친'),('날이 밝아','동료가 찍은 현장'),('며칠 뒤 새 패널을','포장이 뜯기지 않은')],
'C03':[
('', '앞 유리의 행선지는'),('', '마지막 버스가 들어오면'),('예비 버스의 앞 유리에','저는 기록표를 다시'),('격리 스위치 봉인은','저는 사무실 단말기에서'),('예비 버스의 가운데 문이','이번에는'),('버스가 잠깐 흔들리더니','정비동 앞'),('버스와 제 사이에는','그랬더니 차체가'),('저는 출입증에','버스를 움직이는 대신'),('그래서 세차선 표지판','버스는 다시'),('손잡이에 태그를','카트를 따라 버스가'),('안쪽 좌석은','버스 문 앞에 드리운'),('구역 표지판 옆의','정비사가 버스 옆면의'),('제 출입증은 차단봉','그런데 그 뒤에'),('저는 그 일을 그만두지는','그런데 가운데 문이')]
}
plan=read(P/'01_script/scene-plan.json');offset=0.;combined=[];missing=[]
for ci,ch in enumerate(plan['chapters'],1):
 child=P/f'02_audio/chapters/story-{ci:02}';timing=read(child/'03_sync/captions.words.json');words=timing['words'];spoken=(child/'01_script/narration.txt').read_text();scenes=[s for s in plan['scenes'] if s['chapter_id']==ch['id']];cursor=0;seconds=duration(child/'02_audio/working/voice.wav')
 assert spoken.split()==[w['text'] for w in words]
 for si,scene in enumerate(scenes):
  count=len(scene['narration_text'].split());assert scene['narration_text'].split()==[w['text'] for w in words[cursor:cursor+count]]
  start=0 if not cursor else words[cursor]['start'];end=seconds if cursor+count==len(words) else words[cursor+count]['start'];scene.update(start_seconds=round(offset+start,3),end_seconds=round(offset+end,3),duration_seconds=round(end-start,3),timing_status='actual_approved_word_alignment',audio_local_start_seconds=start,audio_local_end_seconds=end)
  for sj,shot in enumerate(scene['shot_sequence']):
   anchor=anchors[ch['id']][si][sj]
   if anchor and anchor in spoken:
    wi=len(spoken[:spoken.index(anchor)].split());t=max(0,words[wi]['start']-.35)
   elif not anchor:t=start
   else:missing.append({'shot':shot['shot_id'],'anchor':anchor});t=start if sj==0 else (start+end)/2
   shot.update(start_seconds=round(offset+t,3),timing_status='spoken_clue_anchor_minus_0.35s',spoken_anchor=anchor)
  cursor+=count
 # Continuous coverage follows actual clue anchors, not arbitrary midpoints.
 pool=[sh for sc in scenes for sh in sc['shot_sequence']];pool[0]['start_seconds']=round(offset,3)
 for i,sh in enumerate(pool):sh['end_seconds']=pool[i+1]['start_seconds'] if i+1<len(pool) else round(offset+seconds,3)
 for sc in scenes:
  sc['motion_beats']=[{'absolute_seconds':sh['start_seconds'],'action':'cut to distinct camera setup '+sh['asset_id'],'spoken_anchor':sh['spoken_anchor']} for sh in sc['shot_sequence']]
 ch.update(start_seconds=round(offset,3),end_seconds=round(offset+seconds,3),actual_audio_seconds=seconds)
 for w in words:combined.append({**w,'start':round(w['start']+offset,3),'end':round(w['end']+offset,3),'chapter_id':ch['id']})
 childplan=read(child/'01_script/scene-plan.json');childplan['scenes']=json.loads(json.dumps(scenes))
 for sc in childplan['scenes']:
  sc['start_seconds']-=offset;sc['end_seconds']-=offset
  for sh in sc['shot_sequence']:sh['start_seconds']-=offset;sh['end_seconds']-=offset
 save(child/'01_script/scene-plan.json',childplan)
 offset+=seconds+(5 if ci<3 else 0)
plan.update(timing_source='actual child Whisper with clue-specific anchors',actual_voice_plus_chapter_transitions_seconds=round(offset,3),end_screen_start_seconds=round(offset+4-18,3),end_screen_end_seconds=round(offset+4,3),planned_total_with_bgm_outro_seconds=round(offset+4,3))
plan['end_screen'].update(start_seconds=plan['end_screen_start_seconds'],end_seconds=plan['end_screen_end_seconds']);save(P/'01_script/scene-plan.json',plan)
tokens=[TimedToken(w['text'],w['start'],w['end'],w['matched']) for w in combined];cues=make_cues(tokens,26,3.6);save(P/'03_sync/captions.words.json',{'duration':round(offset,3),'cues':cues,'words':combined,'source':'concatenated individually aligned chapter words; two intentional five-second transitions'})
write_captions(cues,P/'03_sync');save(P/'03_sync/sync_report.json',{'status':'accepted_under_standing_user_delegation','minimum_child_alignment':min(read(P/f'02_audio/chapters/story-{i:02}/03_sync/sync_report.json')['matched_character_ratio'] for i in [1,2,3]),'direct_listening_performed':False,'clarity_revisions_verified':True,'external_caption_delivery':False})
shorts=read(P/'01_script/shorts-scene-plan.json')
for i,sh in enumerate(shorts['shorts'],1):
 child=P/f'02_audio/shorts/shorts-{i:02}';timing=read(child/'03_sync/captions.words.json');words=timing['words'];cursor=0
 for sc in sh['scenes']:
  n=len(sc['narration_text'].split());assert sc['narration_text'].split()==[w['text'] for w in words[cursor:cursor+n]];sc.update(start_seconds=0 if not cursor else words[cursor]['start'],end_seconds=timing['duration'] if cursor+n==len(words) else words[cursor+n]['start']);cursor+=n
 sh['actual_spoken_seconds']=timing['duration'];sh['actual_audio_seconds']=duration(child/'02_audio/working/voice.wav')
save(P/'01_script/shorts-scene-plan.json',shorts);save(P/'05_review/clue-timing-review.json',{'missing_anchors':missing,'actual_voice_seconds':offset,'composition_seconds':offset+4,'direct_listening_performed':False})
print(json.dumps({'missing_anchors':missing,'duration':offset+4},ensure_ascii=False))
