"""Refine reviewed threat reveals without changing the approved voice or words."""
from pathlib import Path
import json,copy,re
P=Path(__file__).resolve().parent;f=P/'01_script/scene-plan.json';p=json.loads(f.read_text());scenes={s['id']:s for s in p['scenes']}
words=json.loads((P/'02_audio/chapters/story-03/03_sync/captions.words.json').read_text())['words'];offset=next(c['start_seconds'] for c in p['chapters'] if c['id']=='C03')
clean=lambda s:re.sub(r'[^가-힣0-9A-Za-z]','',s)
def cue(sid,phrase):
 s=scenes[sid];local=[w for w in words if s['start_seconds']-offset-.1<=w['start']<s['end_seconds']-offset]
 hits=[w['start']+offset for i,w in enumerate(local) if clean(phrase) in ''.join(clean(z['text']) for z in local[i:i+8])]
 if not hits:raise ValueError((sid,phrase))
 return round(hits[-1]-.15,6)
def insert_baseline(sid,prior,cut,reason):
 s=scenes[sid];assert len(s['shot_sequence'])==2,(sid,'already refined')
 b=copy.deepcopy(scenes[prior]['shot_sequence'][-1]);b.update(shot_id=sid+'-SH0',start_seconds=s['start_seconds'],end_seconds=cut,reuse_reason=reason,new_information=reason)
 s['shot_sequence'][0]['start_seconds']=cut;s['shot_sequence'].insert(0,b);s['editing']['baseline_scene_id']=prior
s=scenes['C03-S04'];assert len(s['shot_sequence'])==2
b=copy.deepcopy(scenes['C03-S03']['shot_sequence'][0]);cut=round(s['start_seconds']+3.0,6);b.update(shot_id='C03-S04-SH0',start_seconds=s['start_seconds'],end_seconds=cut,reuse_reason='Same covered controller camera returns with 32 instead of blank; intentional clue comparison, not a new camera setup.');s['shot_sequence'][0]['start_seconds']=cut;s['shot_sequence'].insert(0,b);s['editing'].update(baseline_scene_id='C03-S03',selection_reason='Repeat the identical covered-controller camera with its newly stated 32 value, then show the genuinely empty platform. No geometry change supplies the clue.')
insert_baseline('C03-S05','C03-S04',cue('C03-S05','영점 단추를'),'Continue notebook/empty platform setup until zero button is actually pressed; deliberate baseline continuation.')
s=scenes['C03-S05'];cut=cue('C03-S05','제 옆 빈 의자의');s['shot_sequence'][-2]['end_seconds']=cut;s['shot_sequence'][-1]['start_seconds']=cut
insert_baseline('C03-S06','C03-S05',cue('C03-S06','의자 앞바닥의'),'Continue bowed chair before round dust marks are first narrated.')
insert_baseline('C03-S09','C03-S08',cue('C03-S09','손수레 손잡이를'),'Keep bent-exit baseline while crossing aisle; flattened cart appears only when handle is touched.')
s=scenes['C03-S12'];cut=cue('C03-S12','저는 팔을 뗐어요');s['shot_sequence'][0]['end_seconds']=cut;s['shot_sequence'][1]['start_seconds']=cut
s=scenes['C03-S17'];assert len(s['shot_sequence'])==2
cut=cue('C03-S17','직원은 넘어지듯');end=cue('C03-S17','그 저울은');b=copy.deepcopy(s['shot_sequence'][0]);b.update(shot_id='C03-S17-SH3',asset_id='C03-S17-A3',start_seconds=cut,end_seconds=end,camera_position='low angle empty office threshold after worker released',new_information='Two shallow shoe-shaped dents remain in empty concrete threshold',reuse_reason=None)
s['shot_sequence'][0]['end_seconds']=cut;s['shot_sequence'][1]['start_seconds']=end;s['shot_sequence'].insert(1,b)
for s in p['scenes']:
 if s['chapter_id']=='C03':
  s['motion_beats']=[{'relative_seconds':round(a['start_seconds']-s['start_seconds'],6),'action':a.get('reuse_reason') or 'Generated view reveals '+a['new_information'],'timing_status':'locked_to_actual_voice'} for a in s['shot_sequence']]
p['review_refinements']='C03 delayed physical/dust/cart reveals, same-camera 32 comparison and empty threshold aftermath; voice/narration unchanged.'
f.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
zero=cue('C03-S05','영이 나타났습니다')+.15;query=cue('C03-S13','표시기에 서른두라는')+.15;backzero=cue('C03-S13','다시 영으로')+.15;zero2=scenes['C03-S16']['audio']['foley_events'][0]['start_seconds']
layouts={}
def add(a,q,value,events=None,color='#b8d8a2',font=62):layouts[a.lower()]={'quad':q,'initial':value,'events':events or [],'color':color,'font_size':font,'review_status':'pending_composed_frame_review'}
add('C03-S03-A1',[[1002,254],[1304,314],[961,337]],'', [{'seconds':scenes['C03-S04']['start_seconds'],'text':'32'}])
add('C03-S04-A1',[[912,354],[1012,366],[894,378]],'32')
add('C03-S04-A2',[[606,491],[783,541],[567,551]],'32',color='#56442b',font=52)
add('C03-S05-A1',[[854,286],[1278,357],[816,376]],'32',[{'seconds':zero,'text':'0'}])
add('C03-S05-A2',[[516,342],[581,345],[505,359]],'0')
add('C03-S01-A2',[[516,342],[581,345],[505,359]],'0')
add('C03-S06-A2',[[490,386],[551,388],[474,406]],'0')
add('C03-S07-A1',[[216,167],[309,169],[204,187]],'0')
add('C03-S09-A2',[[209,405],[284,400],[220,430]],'0')
add('C03-S10-A1',[[950,69],[1105,57],[927,105]],'0')
add('C03-S10-A2',[[1403,33],[1549,20],[1395,64]],'0')
add('C03-S11-A2',[[1462,350],[1588,359],[1451,383]],'0')
add('C03-S12-A2',[[1307,68],[1482,79],[1287,109]],'0')
add('C03-S13-A1',[[1248,94],[1419,84],[1217,143]],'0')
add('C03-S13-A2',[[397,364],[807,321],[414,472]],'0',[{'seconds':query,'text':'32'},{'seconds':backzero,'text':'0'}])
add('C03-S14-A1',[[1098,408],[1194,410],[1087,430]],'32')
add('C03-S14-A2',[[1058,489],[1142,494],[1044,512]],'32')
add('C03-S15-A1',[[953,429],[1042,438],[941,451]],'32')
add('C03-S15-A2',[[586,405],[897,439],[552,478]],'32')
add('C03-S16-A1',[[920,466],[1001,473],[907,484]],'32',[{'seconds':zero2,'text':'0'}])
add('C03-S16-A2',[[1086,390],[1170,391],[1078,415]],'0')
# One bound book, several repeated 32 entries. Lay out on the paper, never across fingers.
add('C03-S11-A1',[[993,454],[1183,504],[969,510]],'', [{'seconds':cue('C03-S11','마지막 장에는')+.15,'text':'32  32'}],color='#56442b',font=45)
add('C03-S11-A2-book',[], '') if False else None
layouts['c03-s11-a2']['extra_clues']=[{'quad':[[941,603],[1100,638],[910,650]],'initial':'','events':[{'seconds':cue('C03-S11','마지막 장에는')+.15,'text':'32  32'}],'color':'#56442b','font_size':45}]
add('C03-S12-A1',[[1070,422],[1266,470],[1051,474]],'32  32',color='#56442b',font=45)
(P/'01_script/diegetic-clue-layouts.json').write_text(json.dumps(layouts,ensure_ascii=False,indent=2)+'\n')
print('C03 reveals refined; 32/0 events locked at',zero,query,backzero,zero2)
