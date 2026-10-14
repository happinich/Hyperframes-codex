from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
phrases={1:['장롱 뒤에는 사람이 설 틈이 없었어요.','그런데 가구를 당길 때마다,','그 틈에서 의자를 끄는 소리가 났습니다.','창밖에서 다시 봤어요.','아까 비어 있던 장롱 안에','작은 의자가 놓여 있었습니다.','의자는 저를 보고 있지 않았어요.'],2:['그 과수원에는','바람에 흔들리지 않는 나무가 하나 있었어요.','가까이 갔더니,','제 발밑 흙이 움직였습니다.','저는 길 쪽으로 물러났어요.','그러자 고정된 지지대와','나무 사이의 거리가 달라져 있었습니다.','그 나무만 앞으로 나와 있었어요.'],3:['빈 저울에 서른두 킬로그램이 남아 있었어요.','영점으로 맞추지 말라는 말을 들었는데,','저는 단추를 눌렀습니다.','저울은 영이 됐어요.','그 순간,','아무도 앉지 않은 의자가 내려앉았습니다.','바닥의 먼지에도 새 자국이 생겼어요.']}
clean=lambda s:re.sub(r'[^가-힣0-9A-Za-z]','',s)
plans=[]
for n,parts in phrases.items():
 f=P/f'02_audio/shorts/shorts-{n:02}/03_sync/captions.words.json';d=json.loads(f.read_text());words=d['words'];position=0;cues=[]
 for phrase in parts:
  target=clean(phrase);acc='';begin=position
  while position<len(words) and acc!=target:
   acc+=clean(words[position]['text']);position+=1
   assert target.startswith(acc),(n,phrase,acc)
  assert acc==target,(n,phrase)
  cues.append({'start':words[begin]['start'],'end':words[position-1]['end'],'text':phrase})
 assert position==len(words)
 d['cues']=cues;d['cue_mode']='reviewed_semantic_phrase_from_approved_source';f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');plans.append({'short_id':f'SH{n:02}','cues':cues,'source_words_unchanged':True,'status':'pending_output_review'})
(P/'01_script/shorts-caption-plan.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2)+'\n');print('Shorts captions regrouped without word/timing/source changes')
