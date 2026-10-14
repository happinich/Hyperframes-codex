"""Historical one-time record of views actually reviewed for 030.
Do not rerun after any media change: this is not an automated approval system.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,subprocess
import numpy as np
P=Path(__file__).resolve().parent;R=P/'05_review';S=P/'01_script';now=datetime.now(timezone.utc).isoformat()
def read(f):return json.loads((P/f).read_text())
def save(f,j):(P/f).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
images=read('05_review/image-review.json');assert len(images['assets'])==117
for a in images['assets']:
 assert a['decision']=='approved' and a['first_full_resolution_review']=='approved' and a['second_full_resolution_and_adjacent_review']=='approved'
 assert hashlib.sha256((P/a['relative_path']).read_bytes()).hexdigest()==a['sha256']
images['status']='all_117_selected_images_two_pass_approved';images['finalized_at']=now;save('05_review/image-review.json',images)
md=['# 030 이미지 검수','', '선택 이미지 117장(본편 103·쇼츠 12·썸네일 배경 2)을 원본 크기로 각각 두 번 확인했습니다. 두 번째는 원고·인접 컷과 대조했습니다. 출력 크롭은 별도 `rendered-shot-review.json`과 `final-extra-frames.json`에 기록합니다.','', '| 이미지 | 해시 | 생성 직후 | 원고·인접 대조 | 제외한 이전 버전 |','|---|---|---|---|---|']
for a in images['assets']:
 md.append(f"| {a['asset_id']} | {a['sha256']} | 승인 | 승인 | {', '.join(str(v) for v in a.get('rejected_versions',[])) or '없음'} |")
 md.extend(['',f"## {a['asset_id']} 판정 근거",'']+[f"- {x['pass']}: {x['note']}" for x in a['reviews']])
(R/'image-review.md').write_text('\n'.join(md)+'\n')
refs=[]
for name,note in [('c01-reference','회화풍 방/작업자/회색 치마와 양말 존재, 왼쪽 창/오른쪽 문, 의자 소품 기준. 실제 선택 컷과 대조.'),('c02-reference','종이 무대풍 입구→창고 축, 올리브 작업복/갈색 동료, 두 주요 가지/수피/뿌리 기준.'),('c02-yard-reference','후일 별도 콘크리트 장비 야적장. 과수원과 구별되는 흰 벽/회색 셔터/호스/트럭.'),('c03-reference','저해상도 3D/픽셀 표면, 고물상 한 사무실/출구/세 버튼 계기/작업자/빈 의자. 실사풍 이전 버전 제외.')]:
 q=P/f'04_composition/assets/references/{name}.png';refs.append(dict(name=name,sha256=hashlib.sha256(q.read_bytes()).hexdigest(),generation_review='previously_individually_viewed',final_original_reference_comparison='approved',note=note,reviewed_at=now))
save('05_review/reference-review.json',refs)
extra=read('05_review/final-extra-frames.json')
for x in extra:
 assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']
 x.update(review='approved_individually_viewed',reviewed_at=now,note='실제 최종 MP4 원본 크기 개별 확인. 자막 문구/안전 영역/결말 비공개, 숫자 면 정합성, 첫·마지막 화면 및 브리지/끝화면 영역 통과.' if x['kind']!='long' else '실제 최종 본편 원본 크기 확인. 첫 훅, 두 브리지 제목 한글, 신발형 홈 공개 시점, 마지막 단서/오른쪽 끝화면 예약 영역 통과.')
save('05_review/final-extra-frames.json',extra)
cap=read('01_script/shorts-caption-plan.json')
for x in cap:x['status']='output_cues_individually_reviewed_against_unchanged_Whisper_words'
save('01_script/shorts-caption-plan.json',cap)
shots=read('05_review/rendered-shot-review.json')['shots'];assert len(shots)==108 and all(x['manual_frame_review']=='approved_individually_viewed' for x in shots)
plan=read('01_script/scene-plan.json');edit=read('01_script/editing-plan.json')
reasons={
'C01':'장롱 뒤의 좁은 틈과 안쪽을 향한 의자를 공간→단서→압박 순서로 보여준다. 바닥 먼지는 낮은 시점, 장롱 내부는 정면, 뒤의 존재는 새 측면으로 공개한다. 좌창/우문 축을 유지한 컷과 가구 끌림 효과를 연결한다.',
'C02':'정상 입구→창고 작업축을 먼저 고정한 뒤, 호스와 뿌리를 낮은 접촉 숏으로 확인한다. 올라간 뿌리와 수피 내부는 별도의 시점에서 단계적으로 공개하고 철기둥 타격 뒤 장화 탈출로 긴장을 해소한다.',
'C03':'C03-S03 봉인 계기 기준 숏으로 C03-S04에서 같은 구도의 32를 비교한다. 영점 뒤 의자/둥근 자국/카트/받침의 변화를 새 접촉 숏으로 보여 주고 버튼 색별 상태를 실제 단어와 연결한다. 복구 뒤 휜 출입문은 남긴다.'}
for ch in edit['chapters']:ch['reason']=reasons[ch['id']];ch['status']='implemented_and_frame_reviewed';ch['rendered_shot_ids']=[x['shot_id'] for x in shots if x['scene_id'].startswith(ch['id'])]
edit.update(status='implemented_asset_and_rendered_frame_reviewed',final_output_shot_count=108,selected_landscape_image_count=103,review_limitations=['직접 청취 및 정상 속도의 연속 시청 검수 미실시; 프레임 순서 대조/대표 모션 쌍/전체 기술 검사까지 수행'])
save('01_script/editing-plan.json',edit)
for scene in plan['scenes']:
 assert scene['narration_text']==scene['caption_text']
 scene['editing']['selection_reason']=reasons[scene['chapter_id']]+' 이 장면의 초점: '+scene['purpose']
 if scene['id']=='C03-S04':scene['editing']['baseline_scene_id']='C03-S03'
 if scene['id']=='C02-S11':scene['editing']['baseline_scene_id']='C02-S10'
 if scene['id']=='C03-S01':
  scene['shot_sequence'][1]['camera_position']='low wide showing empty platform, controller at left and bowed empty chair outside rear-right office'
plan.update(status='rendered_technical_and_individual_frame_reviewed',actual_render_seconds=1558.137187,public_title='빈 저울의 영점을 맞췄더니 옆 의자가 눌렸어요 | 창작 공포 3편',review_limitations=edit['review_limitations'])
save('01_script/scene-plan.json',plan)
md=['# 030 편집 검수','', '## 계획·자산 대조','', '117장 두 차례 개별 검수. C01 의자 등받이 방향/회색 존재의 밑단과 압박, C02 발→빈 장화/뿌리와 철기둥 접촉/차량 시선/별도 야적장, C03 둥근 초기 자국과 신발형 후기 홈/빈 카트 타이어/정상화 후 휜 문을 수정·대조했다. 결함 있는 이전 컷은 제외했다.','']
for ch in edit['chapters']:md.extend([f"### {ch['id']} · {ch['primary_technique_id']}",'',ch['reason'],'',f"보조: {', '.join(ch['support_technique_ids'])}. 제외: {', '.join(ch['excluded'])}.",''])
md.extend(['## 실제 출력 검수','', '108개의 실제 출력 중간 프레임을 원본 크기로 각각 확인하고 인접 순서와 대사를 대조했다. 108개 시작/끝 모션 쌍의 캡처 변화량은 모두 0보다 크며, 최소 '+str(min(x['mean_rgb_capture_difference'] for x in shots))+'. 대표 4쌍을 개별 시각 대조했다. 전체 영상 동결/검정 검사는 허용 한계를 넘는 구간 0개다.','', '| 출력 숏 | 장면 | 실제 초 | 이미지 | 개별 판정 |','|---|---|---:|---|---|'])
for x in shots:md.append(f"| {x['shot_id']} | {x['scene_id']} | {x['output_seconds']:.3f} | {x['asset']} | 승인 |")
md.extend(['','## 대표 모션 쌍',''])
for i in [12,54,79,106]:
 x=shots[i];md.append(f"- {x['scene_id']} {x['motion_start_seconds']}–{x['motion_end_seconds']}초: 원본 시작/끝 프레임 개별 확인, 줌/팬 후 단서와 화면 숫자 정합성 통과.")
md.extend(['','## 쇼츠·브리지·끝화면','', '별도 세로 이미지/별도 음성의 쇼츠 3편을 첫 프레임, 모든 의미 단위 자막 큐 7/8/7개, 마지막 프레임까지 개별 확인했다. 의자 등받이/바람을 따르지 않는 나무의 위치/32→0와 빈 의자의 압박까지이며 정체·탈출·복구·결말은 제외했다. 마지막 말은 각 완전한 문장으로 끝난다. 본편 0/472.5/1005.5/1539/1545/1557.9초도 확인. 두 제목과 우측 20초 끝화면 예약 영역 통과.','', '## 검수 한계','', '이 환경의 오디오 입력 도구는 audio input을 지원하지 않는다고 반환했다. 직접 청취, 믹스의 귀로 듣는 평가 및 정상 속도 연속 시청은 미실시이다. 음성은 Whisper 텍스트 대조·단어 타이밍·긴 공백·피크·클리핑·오디오 길이와 출력 프레임의 연결까지 검사했다. 이 기록은 청취 또는 전체 재생 검수의 통과로 간주하지 않는다.'])
(R/'editing-review.md').write_text('\n'.join(md)+'\n')
# Keep the canonical Shorts entrypoint tied to the actual first separate composition.
shutil.copy2(P/'04_composition/shorts-01/index.html',P/'04_composition/variants/shorts.html') if (P/'04_composition/shorts-01/index.html').exists() else None
# Measure encoded first audio and outro tail; no listening claim.
rows=[]
for n,video in enumerate([P/f'06_delivery/youtube/{P.name}-youtube.mp4']+[P/f'06_delivery/shorts/{P.name}-shorts-{i:02}.mp4' for i in range(1,4)]):
 a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-t','0.5','-f','f32le','-ac','1','-ar','48000','pipe:1']),dtype='<f4')
 idx=np.flatnonzero(abs(a)>.0001);rows.append(dict(file=video.name,first_half_second_peak=float(abs(a).max()),first_signal_above_minus80db_seconds=float(idx[0]/48000) if len(idx) else None,method='encoded_PCM_signal_not_listening'))
master=P/f'06_delivery/youtube/{P.name}-youtube.mp4'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-sseof','-4','-i',str(master),'-f','f32le','-ac','1','-ar','48000','pipe:1']),dtype='<f4')
fade=[float(20*np.log10(max(1e-12,np.sqrt(np.mean(x*x))))) for x in np.array_split(a,8)]
save('05_review/boundary-audio-review.json',dict(first_audio_samples=rows,last_four_second_half_second_rms_db=fade,configured_outro_seconds=4,configured_fade_seconds=3,listening_performed=False))
(P/'README.md').write_text('''# 030 · 빈집·과수원·고물상의 밤

독립적인 창작 공포 세 이야기, 본편 25분 58초. 본편 1920×1080 60fps, 쇼츠 3편 각각 1080×1920 60fps. 원래 본편 음성 1.00x, 쇼츠 별도 음성 1.07x 피치 보존 후처리.

## 결과

- `06_delivery/youtube/2026-030-wardrobe-orchard-scale-youtube.mp4`
- `06_delivery/shorts/2026-030-wardrobe-orchard-scale-shorts-01.mp4` ~ `03.mp4`
- `07_publish/youtube/youtube-publish.html` 및 MD, 썸네일 A/B
- `07_publish/shorts/shorts-publish.html` 및 각 쇼츠 게시 도우미

YouTube 자동 자막. 본편 연속 번인 자막 없음, 쇼츠 번인 자막 포함. 외부 SRT/VTT 납품 없음. YouTube 업로드는 수행하지 않음. Drive 결과는 `07_publish/drive-upload-receipt.json`을 확인.

## 실제 검수와 한계

선택 이미지 117장 각각 두 번, 실제 본편 108숏의 원본 프레임, 쇼츠의 모든 자막 큐와 첫/마지막 프레임, 썸네일 2안 확인. 4개 최종 MP4의 ffprobe·전체 동결/검정 검사·오디오 길이·클리핑·Whisper 대조 수행. 직접 청취 및 정상 속도 연속 시청 검수는 도구 지원 한계로 미실시이며 전체 시청·청취까지 완료했다고 간주하지 않음. 구체적 근거는 `05_review/`에 기록.

## 재구성

최종 계획과 음성·이미지가 존재하는 상태에서 `build-composition.py`, `render-segmented.py`, `build-shorts.py`, `render-shorts.py`로 재구성할 수 있음. 선택 이미지의 승인 해시를 렌더 전에 검사하고 본편은 54분절 렌더 후 합침. 음성 원본 유지, BGM 적용은 TTS를 다시 생성하지 않음.

`prepare-project.py`, `lock-timing.py`, `lock-scale-clues.py`, `repair-orchard-plan.py`, `refine-*`, `correct-*`, `restore-cart-shot.py`는 제작 중 사용한 일회성 수정 이력이며 최종 계획에 다시 실행하면 안 됨. `prepare-publishing.py`도 게시자료/썸네일 HTML을 덮어쓰므로 승인된 수정 뒤에는 주의할 것. 원본·이전 제외 이미지·음성·렌더 결과는 로컬에 보존하며 Git에서는 제외.
''')
brief=P/'00_brief/brief.md';brief.write_text(brief.read_text()+'\n## 최종 출력 기록\n\n본편 실제 1558.137초(25:58), 51장면·108숏·선택 본편 이미지 103장. 독립 쇼츠 3편(15.933/16.467/15.800초), 새 세로 이미지 12장. 썸네일 배경 2장/최종 1280×720 2안. 공개 메인 제목: '+plan['public_title']+'\n\n이미지 두 차례·출력 개별 프레임·전체 기술 검수 수행. 직접 청취/정상 속도 연속 시청은 도구 미지원으로 미실시. YouTube 게시 미수행. Drive 전달 결과는 영수증에 따로 기록.\n')
print('Final evidence recorded: 117 selected images, 108 shots, 34 extra frames, 4 original references; auditory limits explicit.')
print('Audio boundary evidence:',rows,'outro',fade)
