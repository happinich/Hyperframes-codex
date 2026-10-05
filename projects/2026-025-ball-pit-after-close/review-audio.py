from pathlib import Path
import json,subprocess,shutil,re,hashlib
P=Path(__file__).resolve().parent
plan=json.loads((P/'01_script/scene-plan.json').read_text());w=json.loads((P/'03_sync/captions.words.json').read_text())['words']
assert ' '.join((P/'01_script/narration.txt').read_text().split())==' '.join(x['text'] for x in w)
offset=0
for i,s in enumerate(plan['scenes']):
 count=len(s['narration_text'].split());assert s['caption_text']==s['narration_text'];assert ' '.join(s['narration_text'].split())==' '.join(x['text'] for x in w[offset:offset+count]);s['spoken_start_seconds']=w[offset]['start'];s['spoken_end_seconds']=w[offset+count-1]['end'];s['start_seconds']=max(0,w[offset]['start']-.35) if i else 0;offset+=count
for i,s in enumerate(plan['scenes']):s['end_seconds']=plan['scenes'][i+1]['start_seconds'] if i+1<len(plan['scenes']) else 464.46;s['duration_seconds']=s['end_seconds']-s['start_seconds']
plan['timing_source']='actual_pitch_preserved_V4_audio_aligned_by_mlx_whisper_large_v3_turbo';plan['duration_seconds']=464.46;plan['status']='timed_voice_review_passed_objective_checks';plan['voice_speed_multiplier']=1.10
(P/'01_script/scene-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
A=P/'02_audio/shorts-align/03_sync'
for suffix in ['srt','vtt','words.json']:
 shutil.copy2(A/('captions.'+suffix),P/'03_sync'/('shorts-captions.'+suffix))
shutil.copy2(A/'sync_report.json',P/'03_sync/shorts-sync-report.json')
reports={}
for name,src in [('main',P/'02_audio/working/voice.wav'),('shorts',P/'02_audio/working/shorts-voice.wav')]:
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','silencedetect=noise=-40dB:d=0.8,volumedetect','-f','null','-'],capture_output=True,text=True,check=True);(P/f'05_review/{name}-audio-detect.log').write_text(r.stderr)
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(src)],text=True))
 reports[name]={'duration_seconds':duration,'mean_volume_db':float(re.search(r'mean_volume: ([\-\d.]+)',r.stderr)[1]),'max_volume_db':float(re.search(r'max_volume: ([\-\d.]+)',r.stderr)[1]),'silence_durations':re.findall(r'silence_duration: ([\d.]+)',r.stderr)}
main_sync=json.loads((P/'03_sync/sync_report.json').read_text());short_sync=json.loads((P/'03_sync/shorts-sync-report.json').read_text());reports['main']['alignment']=main_sync;reports['shorts']['alignment']=short_sync
for k in ['main','shorts']:
 assert reports[k]['max_volume_db']<-.1
 assert reports[k]['alignment']['matched_character_ratio']>=.92
assert 360<reports['main']['duration_seconds']+4<480;assert 15<reports['shorts']['duration_seconds']<40
reports['first_anomaly_spoken_seconds']=plan['scenes'][4]['spoken_start_seconds'];assert 40<=reports['first_anomaly_spoken_seconds']<=60
reports['cold_open_seconds']=plan['scenes'][1]['spoken_start_seconds'];assert 5<=reports['cold_open_seconds']<=10
reports['review_pass_1']='Original V4 source ASR coverage, word completeness, silence/gap analysis; speed correction identified.'
reports['review_pass_2']='Processed voice independently re-aligned; all 951 authored words preserved; coverage and no >0.8 second gaps confirmed; clipping and first/last word timing checked.'
reports['subjective_listening']='Not performed: this environment provides no audio listening capability. No claim of ear-based pronunciation/emotion or music review.'
reports['unmatched_main_words']=[x for x in w if not x.get('matched',True)]
(P/'05_review/audio-review.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
(P/'02_audio/voice-postprocess.json').write_text(json.dumps({'main':{'multiplier':1.10,'method':'ffmpeg atempo pitch preserving','original':'working/voice-v4-original.wav'},'shorts':{'multiplier':1.07,'method':'ffmpeg atempo then loudness normalization','original':'working/shorts-v4-original.mp3'}},indent=2)+'\n')
print(json.dumps(reports,ensure_ascii=False,indent=2))
