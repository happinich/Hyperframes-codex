"""Keep new structural/physical clues at their narrated appearance."""
from pathlib import Path
import json,copy,re
P=Path(__file__).resolve().parent;f=P/'01_script/scene-plan.json';p=json.loads(f.read_text());scenes={s['id']:s for s in p['scenes']}
words=json.loads((P/'02_audio/chapters/story-02/03_sync/captions.words.json').read_text())['words'];chapter=next(c for c in p['chapters'] if c['id']=='C02');offset=chapter['start_seconds']
clean=lambda s:re.sub(r'[^가-힣0-9A-Za-z]','',s)
def cue(scene,phrase):
 local=[w for w in words if scene['start_seconds']-offset-.1<=w['start']<scene['end_seconds']-offset]
 for i,w in enumerate(local):
  if clean(phrase) in ''.join(clean(z['text']) for z in local[i:i+7]):return round(w['start']+offset-.15,6)
 raise ValueError(phrase)
s=scenes['C02-S08'];shots=sorted(s['shot_sequence'],key=lambda x:x['asset_id'],reverse=True);cut=cue(s,'나무껍질 사이에는')
for shot,a,b in zip(shots,[s['start_seconds'],cut],[cut,s['end_seconds']]):shot.update(start_seconds=a,end_seconds=b)
s['shot_sequence']=shots;s['motion_beats'][1].update(relative_seconds=round(cut-s['start_seconds'],6),action='new macro camera as narration identifies hollow bark seam')
s=scenes['C02-S11'];assert len(s['shot_sequence'])==2,'One-time refinement already applied'
baseline=copy.deepcopy(scenes['C02-S10']['shot_sequence'][1]);baseline.update(shot_id='C02-S11-SH0',reuse_reason='Deliberate continuation of branch caught on wire before root first touches boot; not counted as new camera.',new_information='caught branch remains still before boot contact')
a=cue(s,'바닥에 놓인 검은');b=cue(s,'다음 순간');baseline.update(start_seconds=s['start_seconds'],end_seconds=a)
s['shot_sequence'][0].update(start_seconds=a,end_seconds=b);s['shot_sequence'][1].update(start_seconds=b,end_seconds=s['end_seconds']);s['shot_sequence'].insert(0,baseline)
s['editing']['baseline_scene_id']='C02-S10';s['motion_beats']=[{'relative_seconds':0,'action':'continue caught-branch baseline before contact','timing_status':'locked_to_actual_voice'},{'relative_seconds':round(a-s['start_seconds'],6),'action':'new generated boot/root contact setup','timing_status':'locked_to_actual_voice'},{'relative_seconds':round(b-s['start_seconds'],6),'action':'new generated side view of tightening root','timing_status':'locked_to_actual_voice'}]
s=scenes['C02-S09'];s['prop_continuity']={'thrown_glove':'spare work glove; both worn gloves retained in later physical interaction shots','narration_unchanged':True}
f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');print('Refined S08 hollow cue and S11 pre-contact baseline without changing voice or narration')
