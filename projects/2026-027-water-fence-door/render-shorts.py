"""Render each independent, reviewed portrait composition with its own audio."""
import hashlib
import json
import re
import sys
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent
C = P / '04_composition'
checks = {a['relative_path']: a for a in json.loads((P / '05_review/image-review.json').read_text())['assets']}
for number in (list(map(int,sys.argv[1:])) or range(1, 4)):
    composition = C / f'shorts-{number:02}'
    text = (composition / 'index.html').read_text()
    for name in sorted(set(re.findall(r'assets/visuals/([^"<>]+\.png)', text))):
        path = C / 'assets/visuals' / name
        check = checks['04_composition/assets/visuals/' + name]
        if check['decision'] != 'approved' or hashlib.sha256(path.read_bytes()).hexdigest() != check['sha256']:
            raise SystemExit('Unreviewed or changed portrait asset: ' + name)
    output = P / f'06_delivery/shorts/{P.name}-shorts-{number:02}.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    log = P / f'05_review/logs/render-shorts-{number:02}.log'
    with log.open('w') as stream:
        result = subprocess.run(['npx', '--no-install', 'hyperframes', 'render', str(composition),
                                 '--output', str(output), '--fps', '60', '--workers', '2', '--strict', '--crf', '20'],
                                stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise SystemExit(f'Short {number} failed: {log}')
    print(f'Short {number}/3 rendered: {output}', flush=True)
