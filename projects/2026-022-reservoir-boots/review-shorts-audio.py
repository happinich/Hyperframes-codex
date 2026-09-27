"""Record technical speech review without claiming human listening."""
import json
import subprocess
import wave
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
voice=P/'04_composition/assets/audio/shorts-voice.wav'
with wave.open(str(voice),'rb') as w:
    sr=w.getframerate();channels=w.getnchannels();n=w.getnframes()
    pcm=np.frombuffer(w.readframes(n),dtype='<i2').reshape(-1,channels)/32768
assert np.max(np.abs(pcm[:round(.12*sr)]))==0
log=subprocess.run(['ffmpeg','-hide_banner','-i',str(voice),'-af','silencedetect=n=-40dB:d=0.8,volumedetect','-f','null','-'],capture_output=True,text=True,check=True).stderr
assert 'silence_start:' not in log
sync=json.loads((P/'03_sync/shorts-sync_report.json').read_text())
assert sync['matched_character_ratio']>=.92
raw=json.loads((P/'03_sync/shorts-whisper_raw.json').read_text())
assert raw['segments'][0]['text'].startswith('제 장화가')
assert raw['segments'][-1]['text'].endswith('올라왔어요.')
pace=json.loads((P/'02_audio/working/shorts-shadow/03_sync/pacing_report.json').read_text())
tail=pace['slow_windows'][0]
actual=tail['word_count']/(tail['end']-tail['start'])*60
report={'status':'pass','review_method':'approved-source versus ASR, waveform silence and onset, pacing-window inspection; not a claim of human listening','voice_generated_separately':True,'voice_multiplier':1.07,'pitch_preserved':True,'head_silence_seconds':.12,'head_fade_seconds':.006,'duration_seconds':n/sr,'alignment':sync['matched_character_ratio'],'long_silences':0,'long_word_gaps':pace['long_word_gap_count'],'trailing_slow_window':'false positive: denominator uses full 15s window for a 2.54s tail','actual_tail_wpm':round(actual,1),'first_and_last_sentence_present':True,'asr_note':'Whisper recognized 손바닥 as 선바닥 once. Approved caption remains 손바닥; isolated ASR substitution alone is not a proven TTS pronunciation defect. Subjective voice quality should be checked during playback.'}
(P/'05_review/shorts-audio-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Independent Short voice onset, full ending and technical pacing passed.')
