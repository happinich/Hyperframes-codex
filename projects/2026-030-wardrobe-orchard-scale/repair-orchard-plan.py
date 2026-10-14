"""Repair storyboard indexing without changing a single approved narration word."""
from pathlib import Path
import json,copy,re,hashlib
P=Path(__file__).resolve().parent
f=P/'01_script/scene-plan.json';plan=json.loads(f.read_text())
af=P/'01_script/image-generation-plan.json';ap=json.loads(af.read_text())
old=[s for s in plan['scenes'] if s['chapter_id']=='C02']
assert len(old)==17, 'One-time repair already applied'
texts=[s['narration_text'] for s in old]
last=texts[-1];point=last.index('둘 다 움직이는지')
texts=texts[:-1]+[last[:point].strip(),last[point:].strip()]
assert ' '.join(texts).split()==' '.join(s['narration_text'] for s in old).split()
fresh=copy.deepcopy(old[3])
fresh['purpose']=fresh['visual']='지지끈 없는 낮은 나무와 빠지지 않는 호스'
descriptions=[
 'waist-high view from lane toward one shorter leafless tree with exactly two thick branches, no support ribbon on its trunk, black irrigation hose runs under its base; neighboring trees have white support strings, no creature roots exposed yet, no person',
 'ground-level close view of black hose caught under soil beside the same bare tree base, one brown gloved hand pulls hose from frame edge, surface soil gently heaved in a broad oval mound but no roots or creature revealed yet, no face']
new_assets=[]
for i,(shot,desc) in enumerate(zip(fresh['shot_sequence'],descriptions),1):
 shot.update(camera_position=desc,camera_height='floor_level' if i==2 else 'waist_level',subject_focus=fresh['purpose'],new_information=desc)
 a=copy.deepcopy(next(a for a in ap['assets'] if a['asset_id']==f'C02-S04-A{i}'))
 a['prompt']=a['prompt'].split('Specific shot: ')[0]+'Specific shot: '+desc+'. Narrated purpose: '+fresh['purpose']+'. Keep the decisive clue centrally readable on a phone. ONE standalone landscape frame, no panels, no text, no numbers, no faces, no gore. Use reference only for paper material and fixed orchard lane geography.'
 new_assets.append(a)
seq=old[:3]+[fresh]+old[3:]
assetlookup={a['asset_id']:a for a in ap['assets'] if a['chapter_id']=='C02'}
replacements=[]
for j,s in enumerate(seq,1):
 old_id=s['id'];sid=f'C02-S{j:02}'
 s['id']=sid;s['narration_text']=s['caption_text']=texts[j-1]
 s['editing']['clue']=s['purpose']
 for k,shot in enumerate(s['shot_sequence'],1):
  a=copy.deepcopy(new_assets[k-1] if j==4 else assetlookup[shot['asset_id']])
  aid=f'{sid}-A{k}';shot['shot_id']=f'{sid}-SH{k}';shot['asset_id']=aid
  a.update(asset_id=aid,scene_id=sid,output_path=str(P/'04_composition/assets/visuals'/f'{aid.lower()}.png'),camera=copy.deepcopy(shot))
  replacements.append(a)
ch=next(c for c in plan['chapters'] if c['id']=='C02')
words=json.loads((P/'02_audio/chapters/story-02/03_sync/captions.words.json').read_text())['words'];cursor=0
anchors=['가지가','저는 트럭','마지막 호스를','그때 발밑','제가 호스를','아까 길','굵은 밑동이','바닥을 받친','저는 길 옆','나중에 물어보니','다음 순간','제가 장화','저는 장화에서','동료가 제 팔','작업 길 중간','대신 길','마지막 묶음','제 발밑에서']
clean=lambda t:re.sub(r'[^가-힣0-9A-Za-z]','',t)
for j,s in enumerate(seq):
 n=len(s['narration_text'].split());local=words[cursor:cursor+n]
 assert [w['text'] for w in local]==s['narration_text'].split()
 cursor+=n;start=0 if j==0 else local[0]['start'];end=ch['actual_voice_seconds'] if j==len(seq)-1 else words[cursor]['start']
 cut=None;target=clean(anchors[j])
 for z in range(len(local)):
  if target in ''.join(clean(w['text']) for w in local[z:z+6]):cut=local[z]['start'];break
 if cut is None or not(start+.5<cut<end-.5):cut=(start+end)/2
 s.update(start_seconds=round(ch['start_seconds']+start,6),end_seconds=round(ch['start_seconds']+end,6),duration_seconds=round(end-start,6))
 for shot,a,b in zip(s['shot_sequence'],[start,cut],[cut,end]):shot.update(start_seconds=round(ch['start_seconds']+a,6),end_seconds=round(ch['start_seconds']+b,6),timing_source='Whisper_approved_word_anchor')
 s['motion_beats']=[{'relative_seconds':0,'action':'first distinct camera setup; low practical light sweep','timing_status':'locked_to_actual_voice'},{'relative_seconds':round(cut-start,6),'action':'new generated camera setup at spoken cue '+anchors[j],'timing_status':'locked_to_actual_voice'}]
assert cursor==len(words)
plan['scenes']=[s for s in plan['scenes'] if s['chapter_id']=='C01']+seq+[s for s in plan['scenes'] if s['chapter_id']=='C03']
ap['assets']=[a for a in ap['assets'] if a['chapter_id']=='C01']+replacements+[a for a in ap['assets'] if a['chapter_id']=='C03']
f.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n');af.write_text(json.dumps(ap,ensure_ascii=False,indent=2)+'\n')
(P/'05_review/orchard-storyboard-repair.json').write_text(json.dumps({'reason':'Missing normal observation storyboard shifted later image descriptions one paragraph early. Added distinct normal tree/hose scene and split final paragraph at an existing sentence boundary.','approved_words_unchanged':True,'voice_unchanged':True,'scenes':len(plan['scenes']),'landscape_assets':len(ap['assets']),'chapter_duration_unchanged':ch['actual_voice_seconds']},ensure_ascii=False,indent=2)+'\n')
print('Repaired',len(plan['scenes']),'scenes',len(ap['assets']),'assets, approved words unchanged')
