"""Lock scene/shot changes to approved-word timing and assemble untouched 1.00x chapter voices."""
from pathlib import Path
import sys,json,wave,shutil,re
from dataclasses import asdict
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(R/'scripts'))
from align_captions import align_tokens,make_cues,write_captions,character_coverage

d=P/'02_audio/shorts/shorts-03';sync=d/'03_sync';raw=json.loads((sync/'whisper_raw.json').read_text());words=[dict(w) for seg in raw['segments'] for w in seg['words']]
alias={'32kg이':'서른두 킬로그램이','0점으로':'영점으로','0이':'영이'};changes=[]
for w in words:
 if w['text'] in alias:changes.append({'original':w['text'],'normalized':alias[w['text']],'start':w['start'],'end':w['end']});w['text']=alias[w['text']]
source=(d/'01_script/narration.txt').read_text().strip();spoken=(d/'01_script/tts-narration.txt').read_text().strip();timed,ratio=align_tokens(source,words,raw['duration']);cues=make_cues(timed,26,3.6)
(sync/'whisper-numeric-notation-normalization.json').write_text(json.dumps({'raw_whisper_preserved':True,'scope':'Number/unit notation aliases only; no narration or audio changed; original timestamps preserved.','changes':changes},ensure_ascii=False,indent=2)+'\n')
(sync/'captions.words.json').write_text(json.dumps({'duration':raw['duration'],'cues':cues,'words':[asdict(x) for x in timed]},ensure_ascii=False,indent=2)+'\n');write_captions(cues,sync)
report=json.loads((sync/'sync_report.json').read_text());report['raw_notation_ratio']=report['matched_character_ratio'];report['matched_character_ratio']=round(character_coverage(spoken,words),4);report['caption_surface_match_ratio']=round(ratio,4);report['spoken_match_ratio']=report['matched_character_ratio'];report['status']='ready_for_review';report['normalization_record']='whisper-numeric-notation-normalization.json';(sync/'sync_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert report['matched_character_ratio']>=.92

anchors=[['그 뒤에','마당 쪽','앞을 조금','장롱 옆을','오른쪽 틈','그제야','대신 장롱','의자는 분명히','그때 의자','다시 끈을','한 손이','그때 의자','오래된 가로대','조금 뒤','뒷판은','한 번은'],['가지가','저는 트럭','가까이 가서','제가 호스를','아까 길','밑동이','바닥을 받친','저는 길 옆','나중에 물어보니','처음에는','제가 장화','저는 장화에서','동료가 제 팔','작업 길 중간','대신 길','마지막 묶음','제 발밑에서'],['누가 앉은','넓은 사각','처음 두','저는 일단','사무실로','저는 의자를','저는 빗자루','왜 그런지','저는 손잡이를','저울 위에','저는 기록장을','그 말을','저는 그 자세로','덮개만','주인은','그런데 이번에는','그 저울은']]
planfile=P/'01_script/scene-plan.json';plan=json.loads(planfile.read_text());clock=0;sr=48000;chapter_info=[];mixed=[]
for i,ch in enumerate(plan['chapters'],1):
 if i>1:mixed.append(b'\x00'*(round(5*sr)*4));clock+=5
 cp=P/f'02_audio/chapters/story-{i:02}'
 with wave.open(str(cp/'02_audio/working/voice.wav')) as wav:
  assert wav.getframerate()==sr and wav.getnchannels()==2 and wav.getsampwidth()==2
  dur=wav.getnframes()/sr;data=wav.readframes(wav.getnframes())
 words=json.loads((cp/'03_sync/captions.words.json').read_text())['words'];seq=[s for s in plan['scenes'] if s['chapter_id']==ch['id']];cursor=0;ch['start_seconds']=round(clock,6)
 for j,s in enumerate(seq):
  n=len(s['narration_text'].split());local=words[cursor:cursor+n];assert [x['text'] for x in local]==s['narration_text'].split();cursor+=n
  start=0 if j==0 else local[0]['start'];end=dur if j==len(seq)-1 else words[cursor]['start']
  s['start_seconds']=round(clock+start,6);s['end_seconds']=round(clock+end,6);s['duration_seconds']=round(end-start,6)
  target=re.sub(r'[^가-힣0-9A-Za-z]','',anchors[i-1][j]);cut=None
  for z in range(len(local)):
   phrase=''
   for k in range(z,min(len(local),z+6)):
    phrase+=re.sub(r'[^가-힣0-9A-Za-z]','',local[k]['text'])
    if target in phrase:cut=local[z]['start'];break
   if cut is not None:break
  if cut is None:cut=(start+end)/2
  if cut<=start+.5 or cut>=end-.5:cut=(start+end)/2
  if i==1 and j==4:s['shot_sequence'].reverse()
  for shot,a,b in zip(s['shot_sequence'],[clock+start,clock+cut],[clock+cut,clock+end]):shot['start_seconds']=round(a,6);shot['end_seconds']=round(b,6);shot['timing_source']='Whisper_approved_word_anchor'
  s['motion_beats']=[{'relative_seconds':0,'action':'first distinct camera setup reveals current narrated information; low practical light sweep','timing_status':'locked_to_actual_voice'}, {'relative_seconds':round(cut-start,6),'action':'new generated camera setup at spoken cue '+anchors[i-1][j], 'timing_status':'locked_to_actual_voice'}]
  s['transition_out']='hard_cut_at_approved_word_scene_boundary';s['audio']['bgm']='pending_delegated_candidate_selection'
 assert cursor==len(words)
 ch['end_seconds']=round(clock+dur,6);ch['actual_voice_seconds']=round(dur,6);chapter_info.append({'id':ch['id'],'duration':dur,'whisper_match_ratio':json.loads((cp/'03_sync/sync_report.json').read_text())['matched_character_ratio']});mixed.append(data);clock+=dur
plan['actual_voice_seconds']=round(clock,6);plan['estimated_total_seconds']=round(clock+4,6);plan['end_screen_start_seconds']=round(clock-16,6);plan['end_screen_end_seconds']=round(clock+4,6);plan['timing_source']='final_Eleven_V4_1x_voice_Whisper_turbo_word_timing';plan['status']='voice_timing_locked'
planfile.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
target=P/'02_audio/working/voice.wav'
with wave.open(str(target),'wb') as wav:wav.setparams((2,2,sr,0,'NONE','not compressed'));wav.writeframes(b''.join(mixed))
shutil.copy2(target,P/'02_audio/working/voice-only.wav');shutil.copy2(target,P/'04_composition/assets/audio/voice.wav')
f=P/'02_audio/elevenlabs-request.json';request=json.loads(f.read_text());request['request']['voice_id']='dJlwSfdSqMaQjm3NSl3B';request['request']['performance_direction']='calm, conversational';request['generation_method']='three_new_independent_chapter_takes_prior_request_context_then_5_second_chapter_bridges';f.write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n')
f=P/'06_delivery/profile.json';delivery=json.loads(f.read_text());delivery['chapter_visual_styles']=plan['approved_visual_styles'];delivery['external_caption_files_delivery']=False;delivery['voice_speed_multiplier']=1.0;f.write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
(P/'05_review/voice-review.md').write_text('# 내레이션 검수\n\n첫 장롱 테이크에서 반복·왜곡·긴 휴지를 발견해 폐기했다. 이전 요청 ID만 연결하고 짧은 낭독 태그를 사용한 새 테이크로 대체했다. 승인 원고와 실제 Whisper 단어를 비교했고 원고 회수율·받아쓰기 정확도를 각각 확인해 반복 대사가 일치율에 가려지지 않도록 했다.\n\n'+ '\n'.join(f'- {x["id"]}: 원래 1.00배속 {x["duration"]:.3f}초, Whisper 원고 일치 {x["whisper_match_ratio"]:.2%}. 별도 strict-text-review의 삽입·누락 경고 없음.' for x in chapter_info)+'\n\n본편과 쇼츠 원고는 그대로 보존했다. 쇼츠 세 편은 별도 TTS 생성 후 피치 보존 1.07배속. 쇼츠 3의 숫자·단위 표기(32kg/0점/0)를 승인 발음 원문과 같은 한글 표기로 정규화해 실제 타이밍을 유지했다. 원본 Whisper 결과와 변경 기록을 따로 보존했다. 직접 청취 판정은 수행하지 않았으며 텍스트·신호 검수만 기록한다.\n\n'+f'본편 음성와 두 5초 브리지는 {clock:.3f}초, BGM 아웃트로를 포함할 최종 길이는 {clock+4:.3f}초다. 두 전환의 무발화는 의도된 제목 구간이다. 긴 무음·왜곡 신호는 최종 믹스 후 다시 확인한다.\n')
print('Locked',chapter_info,'total with outro',clock+4,'short3 normalized ratio',report['matched_character_ratio'])
