"""Record completed checks, never substitute planned checks for actual review."""
from pathlib import Path
import hashlib, json, re
P=Path(__file__).resolve().parent
def read(name):return json.loads((P/name).read_text())
def write(name,data):(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
probe=read('05_review/main-ffprobe.json')
v=next(s for s in probe['streams'] if s['codec_type']=='video')
a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],v['pix_fmt'])==(1920,1080,'60/1','h264','yuv420p')
assert a['codec_name']=='aac' and a['sample_rate']=='48000'
assert abs(float(v['duration'])-float(a['duration']))<.1
log=(P/'05_review/logs/main-detect.log').read_text()
assert 'video:' in log, 'Full master detector has not finished'
events=re.findall(r'(?:freeze_start|freeze_end|black_start|silence_start|silence_end):[^\r\n]*',log)
assert not events, events
visual=read('05_review/render-visual-review.json')
assert all(len(visual[k])==151 and all(r['decision']=='passed' for r in visual[k]) for k in ('main_first_pass','main_second_pass'))
assert read('05_review/shorts-output-review.json')['status']=='visual_two_pass_and_technical_review_passed'
main=P/f'06_delivery/youtube/{P.name}-youtube.mp4'
write('05_review/final-output-review.json',{
 'status':'verified','project_id':P.name,'main_file':str(main.relative_to(P)),
 'sha256':hashlib.sha256(main.read_bytes()).hexdigest(),
 'main':{'video_duration':float(v['duration']),'audio_duration':float(a['duration']),
 'dimensions':[1920,1080],'fps':60,'video_codec':'h264','audio_codec':'aac','sample_rate':48000,
 'visual_passes':2,'shots_reviewed_per_pass':151,'freeze_events_over_3s':0,'black_events_over_1s':0,
 'silence_events_over_0_8s_at_minus45db':0,'final_mux_extra_frame_times':[0,6.7,447.9,449.7,451.8,452.95,457,904.4,906.2,908.4,909.5,914,1359.9,1376.6,1380.3],
 'final_mux_transition_and_ending_decision':'passed','outro_seconds':4,'end_screen_reserve_seconds':20},
 'shorts_review':'shorts-output-review.json','thumbnail_review':'thumbnail-output-review.json',
 'image_review':'image-review.json','caption_delivery':'youtube_automatic_no_external_files',
 'audio_review_scope':'Whisper and independent Scribe text comparison plus PCM signal checks. Subjective ear-based naturalness and music judgment were not performed.',
 'render_lint':{'errors':0,'warnings':1,'mitigation':'Master heavy-overlay warning addressed in actual output by 69 scene/transition compositions, at most four images per part; all cache fingerprints and frame counts verified.'}})
visual['status']='main_visual_two_pass_passed';write('05_review/render-visual-review.json',visual)
manifest=read('04_composition/production-manifest.json');manifest['status']='rendered_and_verified';write('04_composition/production-manifest.json',manifest)
profile=read('06_delivery/profile.json');profile.update(script_mode='user_approved_three_story_anthology',chapter_visual_styles=manifest['chapter_styles']);write('06_delivery/profile.json',profile)
approvals=read('00_brief/approvals.json');approvals['production'].update(tts='generated_two_asr_signal_review_passed',images='individual_two_pass_review_passed',composition='implemented_and_verified',render='main_three_shorts_two_thumbnails_verified',publishing='package_prepared_upload_pending');write('00_brief/approvals.json',approvals)
planning=P.parents[1]/'planning'/P.name
(planning/'00_brief/approvals.json').write_text(json.dumps(approvals,ensure_ascii=False,indent=2)+'\n')
brief=(P/'00_brief/brief.md').read_text().replace('본편 마지막 구간 렌더 및 최종 검수 진행 중.','본편 151컷의 실제 출력 두 차례 검수 및 전체 규격·동결·검정·AV 길이 검사 완료. Drive 전달 준비 완료.')
(P/'00_brief/brief.md').write_text(brief);(planning/'00_brief/brief.md').write_text(brief)
(P/'05_review/editing-review.md').write_text('''# 028 편집·실제 출력 검수

승인 대본·편별 스타일을 유지했다. 본편 128개 고유 이미지로 151컷을 구성했다.
원본 개별 1차와 원고·인접 컷 대조 2차: `image-review.md/json`의 승인 146개 자산.
실제 출력 1차(컷 시작 부근)와 2차(컷 말미): `render-visual-review.json`의 151개 shot ID 각각에 실제 시각·파일·판정을 기록했다.

| 범위 | 구현·단서 | 실제 출력 검수 결과 |
| --- | --- | --- |
| C01-S01–S22, 0–447.84초 | 커튼 앞뒤 공간, 가림 레이어, 긴 흰 손등 자국, 손 접촉, 오른쪽 신발 분실 | 두 차례 통과. 발·손·줄·창고 방향과 확대 크롭 대조 |
| T01, 447.84–452.84초 | 단서 유지 암전, 다음 번호·제목, 냉동창고 입구로 전환, 밝아짐 | 수정된 출력에서 447.9/449.7/451.8/452.95초 확인. 완전 검정 없음 |
| C02-S01–S22, 452.84–904.36초 | 통로·운반대·상자 순서, 회색 존재 네 손가락, 오른쪽 안전화, 집 봉투의 서리 | 두 차례 통과. 마지막 안전화는 앞코 하향·측면 네 압흔·온전한 봉투 접힘으로 재생성 후 재검수 |
| T02, 904.36–909.36초 | 봉투 단서 유지, 다음 이야기, 정상 학교 공간 | 906.2/908.4/909.5초 및 다음 콜드 오픈 재검수 통과 |
| C03-S01–S23, 909.36–1376.55초 | 장비 숫자 2→3→4→1과 응답 기록, 의자 네 다리·현관→정문→상점 동선, 전화 거절, 아침 장비 | 두 차례 통과. 3/4/1 화면을 원해상도로 대조했고 숫자 1에는 ‘아무도 없어요’만 남음 |
| SH1/SH2/SH3 | 별도 대본·새 세로 13자산·14컷, 번인 자막 | 컷 중앙과 컷 말미·첫/끝 프레임 두 차례 통과. 19.60/19.00/18.78초, 1080×1920·60fps. 정체·결말 미공개 |
| 끝부분 1360.55–1380.55초 | 우측 엔드스크린 여백, 마지막 4초 음악·3초 감쇠 | 1359.9/1376.6/1380.3초 실제 최종 MP4 확인. 텍스트 잘림 없음 |

## 발견·수정

약 5ms의 부동소수 시간 겹침 때문에 다음 편 구간에 음수 전환 tween이 들어가 912.1초 화면에 암전과 전환 제목이 남았다.
전환 경계를 60fps 프레임으로 맞추고 parts 23/46/47을 다시 렌더했다. 거절한 프레임을 보존하고 교체 출력 두 번과 최종 합친 MP4를 확인했다.
69개 부분 파일의 HTML·GSAP·승인 이미지 해시 및 프레임 수를 다시 검증한 후 최종 합쳤다.

## 음성·음향 검수 범위

여성 Esther·eleven_v4·본편 1.00배속. 승인 원고를 Whisper 및 독립 Scribe 결과로 대조하고 타이밍·클리핑·말 간격을 검사했다.
cand-04, 별도 환경음·26개 사건 효과음, 덕킹·4초 여운을 적용했으며 음성 원본 해시는 유지했다.
최종 신호 −17.6 LUFS, −3.2dBFS true peak. 마지막 1초씩 RMS는 −30.74/−32.82/−37.53/−45.20dBFS로 감소한다.
주관적인 직접 청취를 수행했다고 주장하지 않는다. 음악의 취향·발음 자연스러움에 대한 귀로 듣는 판정은 이 검수 범위 밖이다.

전체 최종 MP4 동결(3초)·검정(1초)·신호 무음(−45dB, 0.8초) 이벤트 0. 규격·AV 길이는 `final-output-review.json` 참조.
외부 SRT/VTT 납품 없음. YouTube 자동 자막 사용, 쇼츠 자막은 영상에 포함.
''')
(P/'05_review/checklist.md').write_text('''# 028 완료 검수

- [x] 본편·쇼츠 대본, 세 스타일, Esther 승인 기록
- [x] 사용자 위임에 따라 BGM cand-04 적용, 원본 보존
- [x] V4 · 본편 1.00배속 · 쇼츠 생성 후 피치 보존 1.07배속
- [x] 대본·원본 이미지 개별·실제 출력 각각 두 차례 검토
- [x] 카메라 위치·각도 변화와 단서 반복 비교 구현
- [x] 5초 편 사이 전환, 첫 변칙 콜드 오픈, 선택적 제목·시간·단서 글자
- [x] 오류 이미지 제외 및 교체 이미지 두 차례 검수
- [x] 전환 시간 겹침 수정·재렌더·최종 MP4 재확인
- [x] 본편 1920×1080·60fps, 23:00.55, H264/AAC, AV 차이 0.005초
- [x] 독립 쇼츠 3편: 1080×1920·60fps·15–40초, 새 세로 이미지, 첫 훅·완결된 절벽 문장·스포일러 배제
- [x] 썸네일 1280×720 두 안 개별 출력 검토
- [x] 전체 최종 영상 동결·검정·무음 검사, 4초 음악 여운·3초 감쇠
- [x] 마지막 20초 엔드스크린 안전 영역
- [x] 본편/쇼츠 게시 전략, 제목·설명·타임스탬프·태그·댓글·일정·Related Video 대상
- [x] YouTube 자동 자막: 외부 SRT/VTT 납품 제외
- [ ] Drive 15개 업로드 및 실제 목록 확인 (완료 후 영수증에 기록)

직접 청취에 의한 주관적 발음/음악 판단은 수행하지 않았다. 두 ASR 원고 대조와 신호·타이밍 검증 결과만 보고한다.
''')
print('Final review recorded. Drive upload is still pending.')
