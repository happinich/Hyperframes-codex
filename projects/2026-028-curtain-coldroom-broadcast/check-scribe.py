"""Independent speech QA; does not change approved captions or narration."""
from pathlib import Path
import sys, json, os, urllib.request, uuid
from dotenv import load_dotenv

P = Path(__file__).resolve().parent
load_dotenv(P.parents[1] / '.env')
src = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve()
boundary = 'qa-' + uuid.uuid4().hex
parts = []
for key, value in {'model_id': 'scribe_v2', 'tag_audio_events': 'true', 'diarize': 'false'}.items():
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{src.name}"\r\nContent-Type: audio/wav\r\n\r\n'.encode() + src.read_bytes() + b'\r\n')
parts.append(f'--{boundary}--\r\n'.encode())
request = urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text', data=b''.join(parts), headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'multipart/form-data; boundary=' + boundary}, method='POST')
with urllib.request.urlopen(request, timeout=240) as response:
    result = json.load(response)
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'file': src.name, 'model': 'scribe_v2', 'text_characters': len(result.get('text', '')), 'words': len(result.get('words', [])), 'events': [w for w in result.get('words', []) if w.get('type') == 'audio_event']}, ensure_ascii=False))
