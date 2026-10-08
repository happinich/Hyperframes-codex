from pathlib import Path
import subprocess,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];J=P/'02_audio/shorts/shorts-03';A=J/'02_audio/working/voice.wav'
subprocess.run([str(R/'.venv/bin/python'),str(R/'scripts/generate_elevenlabs_audio.py'),str(J),'--replace','--postprocess'],check=True)
shutil.copy2(A,J/'02_audio/working/voice-original-speed.wav')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(J/'02_audio/working/voice-original-speed.wav'),'-af','atempo=1.07','-ar','48000','-ac','2',str(A)],check=True)
shutil.copy2(A,J/'04_composition/assets/audio/voice.wav')
subprocess.run([str(R/'.venv/bin/python'),str(R/'scripts/align_captions.py'),str(J),'--language','ko'],check=True)
subprocess.run([str(R/'.venv/bin/python'),str(P/'check-scribe.py'),str(A),str(P/'05_review/scribe-shorts03-final.json')],check=True)
