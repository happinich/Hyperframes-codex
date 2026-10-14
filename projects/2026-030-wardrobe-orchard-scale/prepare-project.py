"""Story-specific source, approvals, shot plans and production setup."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
TITLE='빈집·과수원·고물상의 밤 | 창작 공포 3편'
chapters=[
('C01','장롱 뒤에 서 있던 여자','explicit_ghost','horror_painterly','space_clue_action','닫힌 공간 밖에서 안으로 향하는 먼지와 작은 의자',[
('장롱과 벽 사이 압박','side profile cropped below protagonist shoulders, the brown wardrobe presses her navy jacket chest against the wall, ordinary grey ghost hand pushes from its far rear, no face','low oblique view between wardrobe and wall, moving dolly wheels point toward the protagonist, tight gap readable, grey skirt edge only'),
('빈집 정리와 안방 동선','wide bedroom from entry: brown closed wardrobe at north wall, window left, exit right, bare wooden floor, worker seen from back','exterior of modest Korean house and white moving pickup at courtyard, dusk, no people faces, worker returns from front gate'),
('빈 장롱과 운반판','front oblique view of OPEN two-door wardrobe completely EMPTY except upper shelf, no chair no ghost, flashlight illuminates clear rear wood','floor-height view brown gloved worker hand sliding flat wheeled dolly under wardrobe front edge, empty interior visible above, no ghost'),
('벽을 향한 먼지와 응답','close low view narrow gap behind wardrobe, fine parallel finger-like trails in dust point TOWARD wall, empty space, no body','over-shoulder back view worker taps solid wardrobe side with brown glove, narrow rear gap and left window visible, no ghost'),
('마른 발소리와 양말 끝','floor-level close view a pale-grey SOCK toe barely emerges at wardrobe right rear gap, only ONE partial foot, no body','kneeling back-view worker flashlight directed into empty rear gap, glove holds moving strap, dusty wood floor, faint erased foot trail'),
('빈 틈과 밖으로 건 전화','eye-level shot from right doorway looking along narrow rear gap, no person or chair in gap, dust mark toward wall','courtyard view worker from back holding phone with BLANK screen, bedroom light through left window, dusk'),
('창밖에서 보인 의자','exterior through left window, open wardrobe interior contains ONE small old wooden chair with BACKREST facing camera and seat toward rear panel, no body yet','new camera from right side of exterior window, wardrobe doors partially closing around same chair, all geometry retained, no body'),
('충전기를 뽑고 다시 확인','close low side view brown glove pulls charging plug from bedroom wall socket, navy sleeve, wardrobe blurred in background','eye-level from doorway same small chair in wardrobe facing BACK PANEL, folded grey skirt hem visible ahead of chair, no torso no face'),
('공간 없는 의자 아래 두 발','low frontal close view exactly TWO pale-grey socked feet under same chair, folded grey skirt hem cropped at top, no torso, coherent knees hidden','high oblique view chair inside wardrobe, front chair leg drags short track toward doorway, feet still below chair, ghost upper body hidden'),
('출입구를 가린 장롱','high corner view shifted wardrobe and dolly partially block RIGHT room exit, left window unobstructed, worker back holds strap','eye-level from left window worker rotates wardrobe toward window using moving strap, chair legs visible through open wardrobe door, no full ghost'),
('좁은 틈에 선 여자','side oblique view wardrobe rear: ghost woman upright pressed close to wall, grey blouse skirt socks, HEAD AND FACE completely out of frame above upper border, normal pale hand rests on wardrobe top','low close view ghost pale normal hand physically depresses dark brown top edge, grey sleeve intact, one ordinary hand, no face no extra fingers'),
('벽에 눌린 가슴과 다가오는 의자','side view shoulders-to-knees only protagonist navy jacket chest against wardrobe edge, back against wall, hands try push, no faces no gore','low first-person view small chair front leg coming out of wardrobe near worker brown boots, grey socked feet behind chair, dust displaced'),
('의자를 끌자 풀린 압박','medium side close shot worker two brown gloved hands pull chair BACKREST sideways out of wardrobe, normal contact and coherent arms, grey sock feet lift behind it','low detail of chair broken horizontal crossbar and splintered joint, same TWO grey sock feet lifted slightly above wood floor, no gore'),
('창문 탈출과 원래 자리','courtyard low view worker legs and navy torso climb out open LEFT bedroom window, face out of frame, intact anatomy','courtyard view coworker back and worker back flashlights through window at wardrobe now back at north wall, doors OPEN, interior EMPTY with no chair no ghost'),
('낮에 남은 자국','daylight high oblique bedroom floor with dolly rolling tracks from wall toward room, open empty wardrobe, no entity','close wardrobe solid back panel and intact wall behind it, no hole, daylight glove inspects joinery, no ghost no chair'),
('벽에 등을 기대지 않는다','back-view worker sits on a low stool outdoors away from blank concrete wall, clearly visible air gap between her back and wall, no wardrobe no ghost','close oblique blank concrete wall and worker navy-jacket back separated by narrow gap, readable local light, no figure or face')]),
('C02','폐원한 과수원의 나무가 따라왔어요','creature_or_unknown_entity','horror_paper_stage','space_clue_action','바람을 따르지 않는 가지와 소리에 반응하는 뿌리',[
('발등을 조이는 뿌리','close ground-level view one thick woody root bends around dark GREEN RUBBER BOOT over black irrigation hose, boot leather compresses, root is bark not a human hand, no gore no face','side low close view same boot pinned to soil by root, olive work trousers above, folded woody roots in background but no full tree reveal'),
('과수원 작업 길','high oblique overview orchard with central dirt work lane, low shed at upper end yellow lamp, lower wire gate and white pickup, pear trees and support poles','back-view olive-jacket woman coils black irrigation hose beside pickup at lower gate, tan-jacket coworker far at shed, no faces'),
('바람에 멈춘 나무','wide eye-level view ordinary orchard trees with leaves leaning with breeze, ONE short bare gnarled tree motionless at lane edge, planted in soil, NO root limbs revealed','medium view from lane at dusk the same short tree with two main branching boughs, no support ribbon, ground smooth and roots hidden, shed yellow light behind'),
('호스에 걸린 거꾸로 된 뿌리','low close shot gloved hand lifts black hose slightly and narrow woody root points inward toward short tree, soil rising under it, no creature body','macro-oblique close bark fissure of that root with smaller woody root folding out, unmistakable layered cut cardstock, no flesh no fingers'),
('전화와 이동한 위치','over-shoulder back worker holding phone BLANK display, shed upper lane and coworker back far away, no face','fixed-support-pole reference medium view same short tree now protrudes toward lane relative to metal support pole behind it, broken soil at its base, no eyes'),
('들린 밑동','low view dirt lane leaves beneath worker green boot, slight soil mound near tree, planted support poles unchanged','ground level view short tree base lifted 20 cm above soil by multiple thick folded woody roots, visible air gap, no human anatomy, two main branches above cropped'),
('빈 줄기 안쪽','medium oblique close short tree hollow vertical bark fissure, interlocking small woody roots inside, absolutely NO eyes mouth face or flesh','low three-quarter view folded roots support trunk and shift toward worker, consistent tree hollow and main branches, worker excluded'),
('천천히 물러난다','back-view olive worker steps down central lane toward lower gate while root-supported tree follows from behind, distance visible, no human face','close glove on rusty support pole after being thrown, tree in distant background turning toward pole, paper layers stay planar'),
('동료와 울타리 철사','wide shot coworker back at upper shed doorway and protagonist back lower lane, root tree between them turning toward shed, clear geography','low side detail main branch caught on tensioned wire fence, bark hinge bends without eyes, roots below visible'),
('장화를 붙잡는다','floor close woody root emerging under black hose and folding over GREEN boot, clear physical contact, no gore','higher oblique view root band compresses green boot toe and upper, worker brown trousers intact, tree base approaches from left'),
('호스와 머리 위 가지','shoulders-down olive worker bent by fence, brown gloved hand pulls black hose while root holds boot, one coherent person','side view branch passes above back-view workers head, hair tied low, face hidden, folded bark plates articulate instead of human joints'),
('쇠막대 소리와 빈 장화','back-view tan coworker strikes SHED metal post with long grey rod, intact hands, protagonist only distant below','low close released worker sock foot just outside boot, woody root crushes now EMPTY green rubber boot flat, no foot inside, no gore'),
('나무의 몸과 탈출','wide low tree creature entirely lifted on folded woody roots crawling sideways toward fallen metal poles, two main branches and hollow trunk, no human face','back view tan coworker supports olive worker arm while both move down central lane toward white pickup, worker one green boot one sock, intact anatomy'),
('트럭에서 멈춘 나무','pickup cabin from rear two adults back views with faces completely concealed, dark orchard through front windshield, no readable dash','view through pickup side window root tree now planted-looking motionless halfway up dirt lane, yellow shed lamp above, gate foreground'),
('낮에 확인한 흔적','daylight close flattened empty green boot on dirt work lane beside hose marks, no foot no gore','high oblique daylight orchard lane with broad dragged soil trail toward fence, tree spot smooth with NO stump hole, support poles and shed same'),
('호스 묶음 안 뿌리','day exterior workshop yard black hose unrolled beside white pickup, brown glove holds final coil, no faces','close ONE short bent woody root caught within black hose coil, dry bark, no hand shape, daylight cardstock textures'),
('뒤에서 난 껍질 소리','low view short woody root on yard ground behind two workers backs turning away, pickup wheel at edge, no new monster','ground-level close worker sock foot presses dry fallen leaf, short root behind across visible ground, deliberately no movement lines or supernatural face')]),
('C03','빈 저울의 영점을 맞추지 마세요','modern_rule_horror','horror_retro_3d','return_with_changed_clue','빈 철판의 32kg과 저울 밖에서 물건을 누르는 압력',[
('빈 의자 좌판이 내려앉는다','low oblique empty wooden chair seat bends visibly downward at center with no body on it, same chair by warehouse office, no ghost or human','wide warehouse scale platform empty at left, blank scale display at right, empty chair lowered at center by office, corrugated exit rear left, no entity'),
('고물상 야간 업무','high corner warehouse overview same low square scale foreground left and display right, office rear right, metal exit rear left, blue empty handcart beside exit','back view navy vest woman clerk near office doorway looking toward low steel platform, no face, angular low-poly limbs'),
('테이프 아래 영점 단추','medium close same control panel blank green display and clear protective lid, plain yellow tape across left button, no text or number','new side view empty blue handcart rolling onto square scale plate, navy grey-sleeve clerk back, normal geometry no threat yet'),
('빈 저울의 32킬로그램','front slight high view EMPTY steel scale and blank rectangular display clearly readable left-center for later 32 editorial overlay, no numbers generated','top view simple ruled notebook on desk and ordinary pen, book pages BLANK no letters, navy sleeve at corner, no invisible body'),
('영점 단추와 의자 압박','close ordinary bare index finger of grey sleeve presses taped left button under clear lid, display BLANK, no extra fingers','new low camera empty chair beside office with seat depressed center and legs strained, dusty floor, no body'),
('먼지의 둥근 압박','top-down empty bent chair, two smooth shallow OVAL dust pressure marks on floor just in front, no footprints no ghost','side view ordinary hand tries lift empty chair back but chair scrapes away from scale across dust line, no entity'),
('빗자루가 바닥에 붙는다','low view broad pressed smooth dust line from scale edge toward chair, empty warehouse, no figure','close broom bristles pinned flat to dusty floor and wood handle bending under clerk hand pull, no ghost hand, ordinary fingers'),
('전화와 휘는 창고문','shoulder cropped shot grey sleeve holding phone with BLANK screen next to office outside doorway, face excluded','low frontal corrugated exit door lower edge bends INWARD, pressure dust line from chair toward it, no monster'),
('빈 손수레의 무게','low side empty blue handcart tires flatten on dusty floor under invisible pressure, handcart tray obviously empty','medium back view navy vest clerk releases handcart handle and steps back, wheels compressed, face excluded'),
('들린 철판과 위로 간 먼지','ground-level platform corner raised several centimeters, one support lifted above floor, dust suspended beneath, display blank behind','new side close gap under empty platform showing intact support mounts and dusty particles lifted, no visible entity no human'),
('기록장과 휘는 책상','overhead desk notebook open blank ruled pages, simple pen, bare ordinary fingers at edge, tabletop mildly bent downward','side desk view notebook stays on tabletop while grey-sleeve clerk hand opens it, pen stops on bowed desk, no text generated'),
('같은 값과 손등의 압박','overhead close open BLANK notebook with three ruled rows suitable for editorial repeated 32 overlay, no letters','close one ordinary clerk hand pressed flat downward on desk by unseen force, grey cuff, no external hand no gore'),
('조회하는 동안 잠깐 풀린다','close TWO ordinary hands one supports the other above desk, both wrists coherent, flat pressure on upper hand, no third hand','side close coherent index finger presses center query button on blank scale panel, clear lid open, no numbers'),
('무게를 돌려놓고 탈출','low scale plate now rests flat on its supports again, blank display behind, dust falls, all visible bodies absent','wide navy vest woman from back walking out through slightly bent corrugated door, empty chair now normal, no faces'),
('낮에도 같은 빈 값','daylight wide warehouse scale still empty, anonymous repair worker from back inspects blank display, no danger instructions no faces','close scale control protective lid shut with fresh plain tape covering left button, blank display has room for editorial 32 overlay'),
('새 직원과 전자음','wide warehouse from exit, anonymous new employee grey jacket back enters small office rear right, scale empty and display BLANK','new medium frontal scale blank display foreground, empty chair and handcart unchanged upright, office doorway beyond, no person body revealed'),
('문턱에 붙은 신발','low floor angle TWO brown worker shoes at office threshold compressed into shallow matching dents, grey pants legs above, no person face no gore','close final protective lid completely wrapped by plain adhesive tape over buttons, display dark BLANK, office threshold with dents soft background')])]

for i,text in enumerate([
'장롱 뒤에는 사람이 설 틈이 없었어요. 그런데 가구를 당길 때마다, 그 틈에서 의자를 끄는 소리가 났습니다. 창밖에서 다시 봤어요. 아까 비어 있던 장롱 안에 작은 의자가 놓여 있었습니다. 의자는 저를 보고 있지 않았어요.',
'그 과수원에는 바람에 흔들리지 않는 나무가 하나 있었어요. 가까이 갔더니, 제 발밑 흙이 움직였습니다. 저는 길 쪽으로 물러났어요. 그러자 고정된 지지대와 나무 사이의 거리가 달라져 있었습니다. 그 나무만 앞으로 나와 있었어요.',
'빈 저울에 서른두 킬로그램이 남아 있었어요. 영점으로 맞추지 말라는 말을 들었는데, 저는 단추를 눌렀습니다. 저울은 영이 됐어요. 그 순간, 아무도 앉지 않은 의자가 내려앉았습니다. 바닥의 먼지에도 새 자국이 생겼어요.'],1):
 (P/f'01_script/shorts-{i:02}-narration.txt').write_text(text+'\n')

styles=json.loads((ROOT/'config/visual-styles.json').read_text())['styles']
sceneplan={'project_id':P.name,'title':TITLE,'status':'approved_by_explicit_user_selection_delegation','content_nature':'fiction','production_profile_id':'horror_cinematic_story_v1','production_profile_status':'approved_by_user_delegation','format':{'type':'three_story_anthology','duration_minutes_range':[20,40],'voice_speed_multiplier':1.0,'automatic_speedup':False,'screen_text_mode':'short_story_titles_and_diegetic_clues_no_continuous_narration_captions','youtube':{'width':1920,'height':1080,'fps':60},'shorts':{'count_planned':3,'width':1080,'height':1920,'fps':60,'duration_seconds_range':[15,40],'voice_speed_multiplier':1.07}},'timing_source':'draft_character_estimate_replace_with_actual_Whisper','chapter_transition_seconds':5,'chapters':[],'scenes':[]}
assets=[];alltext=[];clock=0
for i,(cid,title,kind,style,primary,clue,details) in enumerate(chapters,1):
 raw=(P/f'01_script/story-{i:02}-narration.txt').read_text().strip();pars=raw.split('\n\n');assert len(pars)==len(details)
 alltext.append(raw)
 if i>1:clock+=5
 start=clock
 for j,(par,(purpose,a,b)) in enumerate(zip(pars,details),1):
  sid=f'{cid}-S{j:02}';duration=round(len(par)*.129,3);end=round(clock+duration,3)
  stage='cold_open' if j==1 else 'normal' if j<4 else 'anomaly' if j<7 else 'escalation' if j<11 else 'interaction' if j<15 else 'aftermath'
  shots=[]
  for k,description in enumerate([a,b],1):
   aid=f'{sid}-A{k}';path=P/f'04_composition/assets/visuals/{aid.lower()}.png'
   shot={'shot_id':f'{sid}-SH{k}','location_id':['empty_house','orchard','warehouse'][i-1],'camera_position':description.split(',')[0],'camera_angle':'story_specific_as_described','camera_height':'floor_level' if 'low ' in description or 'floor' in description[:30] else 'high_angle' if 'high' in description[:35] or 'overhead' in description[:30] else 'eye_level','shot_size':'detail' if 'close' in description[:40] else 'wide' if 'wide' in description[:30] or 'overview' in description[:35] else 'medium','subject_focus':purpose,'spatial_anchors':'Fixed chapter-specific geography and entity design in reference sheet; preserve action axis.','asset_id':aid,'new_information':description,'reuse_reason':None}
   shots.append(shot)
   prefix=styles[style].get('image_prompt_cues',style)
   prompt=f'Use case: illustration-story. Generate ONE new standalone full-bleed landscape film frame in 16:9 aspect ratio, intended for 1920x1080 video. Reference sheet is ONLY a guide to material, palette, character clothes, recurring objects and fixed geography. Do NOT copy its panel layout: NO panels, NO collage, NO borders. Style: {prefix}. Specific shot: {description}. Narrated purpose: {purpose}. Keep the decisive clue near central 70 percent, readable on a phone, with intact natural anatomy and coherent object geometry. Only show the exact people or threat portions described for this shot; do not insert reference entities into earlier empty scenes. Human faces fully hidden by back view or framing. No gore, logos, text, captions, lettering, numbers or watermark. Device displays and notebook pages remain BLANK for precise editorial overlays. Lighting low but clue edges readable. Preserve consistent wardrobe doors/dolly or orchard lane/pickup or platform/display/office relationships from reference.'
   assets.append({'asset_id':aid,'scene_id':sid,'chapter_id':cid,'output_path':str(path),'reference_path':str(P/f'04_composition/assets/references/{cid.lower()}-reference.png'),'prompt':prompt,'status':'planned','camera':shot})
  sceneplan['scenes'].append({'id':sid,'chapter_id':cid,'type':stage,'start_seconds':clock,'end_seconds':end,'duration_seconds':duration,'purpose':purpose,'narration_text':par,'caption_text':par,'visual':purpose,'motion':'clue-focused camera plus practical-light change; distinct generated view at narration beat','motion_beats':[{'relative_seconds':0,'action':'first camera setup slowly approaches narrated clue','timing_status':'draft_retime_after_voice'},{'relative_seconds':round(duration/2,3),'action':'cut to second new camera setup exposing new detail','timing_status':'draft_retime_after_voice'}],'audio':{'narration':'voice_only_master','room_ambience':'separate_original_room_tone','event_foley':'separate_at_spoken_object_action','bgm':'select_after_voice_review_by_user_delegation','intentional_silence_seconds':0},'transition_out':'cut_on_narrated_discovery_or_action','shorts_adaptation':f'separate_approved_short_{i:02}_fresh_portrait_images','editing':{'technique_ids':[primary,'clue_directed_motion'] if j>1 else ['space_clue_action'],'clue':purpose,'tension_stage':stage,'shot_scale':'two_distinct_generated_camera_setups','baseline_scene_id':f'{cid}-S03' if primary=='return_with_changed_clue' and j>3 else None,'selection_reason':'Keep spatial relation and narrated clue legible; reveal only the current beat.'},'shot_sequence':shots})
  clock=end
 sceneplan['chapters'].append({'id':cid,'title':title,'content_nature':'fiction','horror_type':kind,'visual_style_id':style,'start_seconds':start,'end_seconds':clock,'estimated_seconds':round(clock-start,3),'voice_speed_multiplier':1.0})
sceneplan['estimated_total_seconds']=round(clock+4,3);sceneplan['end_screen_start_seconds']=round(clock-16,3);sceneplan['end_screen_end_seconds']=round(clock+4,3)
sceneplan['approved_visual_styles']={x[0]:x[3] for x in chapters}
(P/'01_script/narration.txt').write_text('\n\n'.join(alltext)+'\n')
def dump(path,d):path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
dump(P/'01_script/scene-plan.json',sceneplan)
dump(P/'01_script/image-generation-plan.json',{'project_id':P.name,'generation_tool':'built_in_image_gen','assets':assets})
short_assets=[]
short_specs=[['exterior through left window, empty wardrobe doors open; no person inside','low close narrow empty gap behind wardrobe, fine dust trails toward wall','courtyard back-view navy worker holding phone, bedroom window behind','frontal close one small chair backrest inside wardrobe facing rear panel, NO ghost no feet'],['wide central orchard dirt lane toward yellow shed, ordinary trees, one still bare short tree','low worker green boot beside black hose and slightly raised dirt, NO revealed creature','fixed pole comparison short ordinary tree now closer to lane, root limbs completely HIDDEN','back-view olive worker halts on lane looking at misplaced tree and gate beyond, no creature reveal'],['low empty square steel scale and BLANK panel, no person or pressure yet','close grey sleeve finger near taped left button under lid, panel blank','empty chair seat begins to bow downward, NO body','low dust floor with smooth new oval pressure marks between chair and scale, no figure']]
for i,specs in enumerate(short_specs,1):
 for j,desc in enumerate(specs,1):
  cid=f'C{i:02}';style=chapters[i-1][3];aid=f'SH{i:02}-{j:02}';prompt=f'Use case: illustration-story. Generate ONE freshly composed full-bleed PORTRAIT image for a 9:16, 1080x1920 Short. New independent asset, never crop the reference sheet or a longform frame. Reference ONLY for consistent material, props, clothes and geography. Style: {styles[style]["image_prompt_cues"]}. Shot: {desc}. Clear central mobile clue with safe lower third for captions. No panels, borders, collage, text, numbers, logos, gore, watermark or human face. NO identity, full ghost, root creature body or ending. Scale display stays blank.'
  short_assets.append({'asset_id':aid,'chapter_id':cid,'output_path':str(P/f'04_composition/assets/visuals/{aid.lower()}.png'),'reference_path':str(P/f'04_composition/assets/references/{cid.lower()}-reference.png'),'prompt':prompt,'status':'planned'})
dump(P/'01_script/shorts-image-generation-plan.json',{'project_id':P.name,'generation_tool':'built_in_image_gen','fresh_portrait_required':True,'assets':short_assets})
approval={'recorded_date_kst':'2026-10-14','user_instruction':'오늘 이야기 시작하자. 지금 작업 지시하고 자러 갈거야. 다음 작업 지시 안되니까 모든 내용 추천으로 하고 끝까지 진행해줘.','scope':'Explicit advance approval and selection delegation for this new anthology: all three complete scripts, separate Shorts scripts, production profile, story-specific recommended visual styles, narrator casting, editing, BGM selection after voice review, reviewed Drive delivery and relevant commit/push.','script':'approved_by_explicit_user_delegation','shorts_script':'approved_by_explicit_user_delegation','visual_styles':sceneplan['approved_visual_styles'],'voice':'Esther_eleven_v4_recommended_selected_by_delegation','bgm':'delegated_selection_after_voice_review_not_yet_selected'}
dump(P/'00_brief/approvals.json',approval)
config=json.loads((ROOT/'config/success-rules.json').read_text())
for kind,count in [('chapters',3),('shorts',3)]:
 for i in range(1,count+1):
  stem=f'story-{i:02}' if kind=='chapters' else f'shorts-{i:02}'
  d=P/f'02_audio/{kind}/{stem}'
  for sub in ['01_script','02_audio/inbox','02_audio/working','03_sync','04_composition/assets/audio']: (d/sub).mkdir(parents=True,exist_ok=True)
  shutil.copy2(P/f'01_script/{stem}-narration.txt',d/'01_script/narration.txt')
  req=json.loads((ROOT/'projects/2026-029-three-unreturned-items/02_audio/chapters/story-01/02_audio/elevenlabs-request.json').read_text())
  req['target_audio']=f'inbox/{stem}-narration.mp3';req['request']['performance_direction']='Restrained conversational Korean female storytelling. Natural original pace, gradual emotional arc, no duplicated words, no non-speech sounds, voice only. Quiet observations to urgent contact then subdued aftermath.'
  req['postprocess']['voice_speed_multiplier']=1.0 if kind=='chapters' else 1.07
  dump(d/'02_audio/elevenlabs-request.json',req)
(P/'04_composition/assets/visuals').mkdir(exist_ok=True)
shutil.copy2(ROOT/'projects/2026-029-three-unreturned-items/04_composition/assets/gsap.min.js',P/'04_composition/assets/gsap.min.js')
editing={'project_id':P.name,'status':'planned_approved_by_explicit_delegation','catalog':'config/horror-editing-techniques.json','reference_report':'planning/horror-reference-monitoring/2026-10-12/report.ko.md','chapters':[{'id':c[0],'primary_technique_id':c[4],'support_technique_ids':['clue_directed_motion','foreground_depth','tension_driven_transition'],'clue':c[5],'visual_style_id':c[3],'reason':'New geometry and physical clue determine camera distance and timing. 32kg comparisons use a fixed display baseline; wardrobe gap and root lift use high/low new assets.','excluded':['random_glitches','same_image_crop_as_new_view','unmotivated_early_full_entity_reveal'],'reference_application':'2026-10-12 camera-height contrast candidate applies only to actual floor/gap information, not to numerical baseline comparison.','shorts_application':'standalone spoiler-free portrait clue sequence with separately generated images'} for c in chapters], 'review':{'plan_and_assets':'pending','rendered_output':'pending','record_path':'05_review/editing-review.md'}}
dump(P/'01_script/editing-plan.json',editing)
brief=f'''# 030 제작 브리프 — {TITLE}

작성일: 2026-10-14 KST. 세 편 모두 독립적인 오리지널 창작 공포(`fiction`). 가상의 장소와 인물이며 실화·제보로 표시하지 않는다.

사용자가 이번 회차의 모든 추천 선택과 완료까지의 진행을 명시적으로 위임했다. 원고·쇼츠 원고·프로필·편별 비주얼·음성 선택을 각각 이 근거로 승인 기록했고, BGM은 음성 검수 후 새 후보를 만들어 선택한다. 인용 지시는 `approvals.json`에 보존했다.

전체 20~40분, 기본 세 편. 원고 {sum(len(s) for s in alltext):,}자, 최근 원래 1.00배속 낭독 기준 약 {clock/60:.1f}분 추정. 실제 음성으로 확정한다. 본편 1920×1080 60fps, 별도 쇼츠 세 편 1080×1920 60fps 15~40초. 본편 연속 나레이션 자막 없음, 필요한 제목·저울 숫자·기록장 값만 화면 글자로 편집. YouTube 자동 자막, 외부 SRT/VTT 납품 없음. 쇼츠는 1.07배속 후처리와 번인 자막, 새 세로 자산.

## 이야기와 선정 이유

1. **장롱 뒤에 서 있던 여자**: 빈집 정리 작업에서 장롱 밖의 좁은 틈에 여자가 서 있고 가구를 밀어 화자를 압박한다. 먼지→양말과 치맛자락→손과 몸을 통한 압박으로 귀신의 실재를 확인한다. `horror_painterly` 우선: 갈색 나무·회색 옷·황색 창빛의 무광 붓질, 단서는 밝은 윤곽으로 남긴다. 대안 먹·목탄(빈틈 명암)과 인형극(목재·의자 촉감). 실제 깊이와 좁아지는 동선이 중요해 회화풍 선정. 공간→단서→행동 중심, 창문 왼쪽/방 문 오른쪽/장롱 뒤 벽 기준. 평소 장롱 안은 비워 두고 존재 공개를 앞당기지 않는다.
2. **폐원한 과수원의 나무가 따라왔어요**: 호스 철수 작업 중 바람을 따르지 않는 줄기가 뿌리 위에 올라 소리를 향해 이동한다. 바닥의 움직임→빈 줄기와 받친 뿌리→장화 압박으로 한 나무형 존재를 확인한다. `horror_paper_stage` 우선: 카드지 껍질·가지·뿌리의 겹침으로 접히는 몸을 구분하고 남색 하늘·올리브 작업복·황색 창고 빛을 유지한다. 대안 거친 2D(동선)와 회화(수목 질감). 새 카메라 높이에 따라 뿌리와 흙의 틈을 읽힐 수 있는 종이층 선정. 낮은 대문·트럭→상부 창고의 중앙 길을 유지. 눈·입·인간 손이 없는 줄기와 두 주 가지, 접힌 목재 뿌리를 고정한다.
3. **빈 저울의 영점을 맞추지 마세요**: 남아 있는 32kg을 지우면 보이지 않는 압력이 의자·손수레·사람이 닿은 물체로 이동한다. 값 복구로 탈출하나 다음 작업자가 같은 단추를 누르는 잔상을 남긴다. `horror_retro_3d` 우선: 빈 철판·사무실·표시기 위치와 구식 기기 금기를 각진 공간·거친 텍스처로 읽힌다. 대안 픽셀(수치)과 거친 2D(손 접촉). 표면 미세사진 질감과 매끈한 최신 CGI를 제외한 낮은 폴리곤 선정. 숫자는 이미지 생성에 맡기지 않고 실제 발화에 맞춰 편집한다. 위협의 눈에 보이는 몸을 추가하지 않는다.

보이스: Esther 여성 보이스 우선, V4 1.00x. 세 일인칭의 성별은 원고상 고정하지 않는다. 관찰 문장과 후반 압박의 거리 변화에 적합하며 최근 동일 모델의 한국어 정렬이 안정적이었다. 남성 보이스는 현장감 대안이지만 별도 새 테이크 품질을 확인해야 하므로 이번에는 검증된 여성 보이스를 추천 선택한다. 이전 프로젝트의 테이크·BGM·이미지는 재사용하지 않는다.

## 참고 근거와 독립성

최신 [2026-10-12 보고서](../../../planning/horror-reference-monitoring/2026-10-12/report.ko.md)와 아이디어 라이브러리를 확인했다. [높은 도시 시점·낮은 철길 표본](https://www.youtube.com/watch?v=Kyjxoqovpyw&t=35s), [눈높이·상부 삽화 표본](https://www.youtube.com/watch?v=qfBDx-TeBaQ&t=935s)의 카메라 높이 정보 차이를 장롱 뒤 바닥, 들린 밑동, 저울 받침 틈의 새 시점에 연결한다. 원 영상은 정지 화면 표본만 확인된 자료이며 음향·컷 속도·전체 줄거리·결말을 차용하거나 검증했다고 주장하지 않는다. 라이브러리의 수선실·잔교·펜션 소재는 029에서 이미 제작했으므로 사용하지 않는다.

029와 장소·직업·반복 물건·위협 해결 구조를 대조했다. 수선사의 소매·실 자르기→빈집의 장롱·의자 가로대; 잔교 정비·마른 손·잠금 핀→과수원 호스 철수·뿌리·소리 유도; 철거 펜션·키 반납·구역 등록→고물상 계량·영점·물리 압력. 네 요소가 각각 다르다. 장롱 이야기는 의복 물건 이동과 구별하고 019 초상·028 커튼·냉장실·방송 사건도 사용하지 않는다.

## 사운드와 납품

새 BGM 후보 선정과 내레이션·원본 공간음·사건 효과음을 분리한다. 0.8초가 넘는 적막은 실제 타이밍에 기록한다. 본편 마지막 20초에 공개된 029 합본 또는 창작 공포 재생목록을 연결한다. 공개 전 실제 채널에서 선택한다. Drive에는 게시 MD/HTML·최종 썸네일 두 장·쇼츠 세 편과 각 게시 전략을 전달하고 본편 MP4는 로컬에 둔다. 검수 후 관련 텍스트 소스만 커밋·푸시한다.
'''
(P/'00_brief/brief.md').write_text(brief)
(P/'01_script/script-review.md').write_text('# 원고 검토\n\n사용자 추천 선택 위임에 따라 세 본편과 세 독립 쇼츠 원고를 승인 기록했다. 초반 정상 동선과 첫 불일치, 확인 행동, 직접 압박·접촉, 결정적 선택, 잔상 결말을 각각 점검했다. 모든 문장은 자연스러운 존댓말 구술형이며 대사와 문어식 설명을 구분했다. 실제 콜드오픈과 첫 이상 시점은 음성 생성 뒤 Whisper로 확인하고 늦으면 초반 구성을 보정한다. 원고는 최종 음성 이전까지 단일 기준으로 유지한다.\n')
(P/'01_script/production-notes.md').write_text('# 제작 노트\n\n프로필 horror_cinematic_story_v1. 편별 스타일: 회화/종이 무대/초기 3D. 원래 음성 1.00x, 쇼츠 후처리 1.07x. 50개 장면, 100개 본편 컷·12개 새 세로 컷을 계획했고 장면별 두 카메라의 목적을 shot_sequence에 적었다. 모션·효과음·컷은 최종 Whisper 발화 시점으로 재계산한다. 의도하지 않은 손·공간·글자와 이미지 스타일 이탈은 수정한다.\n')
print('project prepared',len(sceneplan['scenes']),'scenes',len(assets),'landscape shots',len(short_assets),'portrait shots',sceneplan['estimated_total_seconds']/60,'estimated minutes')
