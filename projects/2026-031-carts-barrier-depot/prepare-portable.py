"""Copy only verified final publishing outputs to the portable multi-Short package."""
import json,shutil,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;O=P/'07_publish/drive-upload';O.mkdir(exist_ok=True)
lf=json.loads((P/'05_review/longform-technical-review.json').read_text())[0];shorts=json.loads((P/'05_review/shorts-technical-review.json').read_text());assert lf['full_decode']=='passed' and not lf['freeze_intervals_over_3s'] and not lf['black_intervals_over_1s']
for r in shorts:assert r['full_decode']=='passed' and not r['freeze_intervals_over_3s'] and not r['black_intervals_over_1s']
for name,src in {'longform-publish.md':'07_publish/youtube/youtube-publish.md','longform-publish.html':'07_publish/youtube/youtube-publish.html','thumbnail-a.png':'07_publish/thumbnail-a.png','thumbnail-b.png':'07_publish/thumbnail-b.png'}.items():
 f=P/src;dst=O/name
 if f.suffix=='.html':dst.write_text(f.read_text().replace('../../06_delivery/youtube/',''))
 else:shutil.copy2(f,dst)
for n in range(1,4):
 sid=f'shorts-{n:02}';shutil.copy2(P/f'06_delivery/shorts/{P.name}-{sid}.mp4',O/f'{P.name}-{sid}.mp4');shutil.copy2(P/f'07_publish/shorts/{sid}-publish.md',O/f'{sid}-publish.md');(O/f'{sid}-publish.html').write_text((P/f'07_publish/shorts/{sid}-publish.html').read_text().replace('../../06_delivery/shorts/',''))
shutil.copy2(P/f'06_delivery/youtube/{P.name}-youtube.mp4',O/f'{P.name}-youtube.mp4')
(O/'README.md').write_text(f'''# 031 · 최종 전달

본편: {P.name}-youtube.mp4 (20분 50초, 1920×1080, 60fps)
쇼츠: {P.name}-shorts-01~03.mp4 (각 약 20.5초, 1080×1920, 60fps)
썸네일: thumbnail-a.png / thumbnail-b.png
본편 게시 도우미: longform-publish.html / longform-publish.md
쇼츠 게시 도우미: shorts-01~03-publish.html / .md

폴더 전체를 내려받아 HTML을 브라우저에서 열면 MP4 미리보기와 복사 버튼을 사용할 수 있습니다.
본편 자막은 YouTube 자동 자막을 사용하며 쇼츠 자막은 번인했습니다. 외부 SRT/VTT는 포함하지 않습니다.

창작 공포이며 검증된 실화가 아닙니다. 추천 게시 시간은 자료에 있는 기본 일정 제안입니다. YouTube 게시와 관련 동영상·엔드스크린 지정은 아직 수행하지 않았습니다.
검수: 개별 원본·출력 프레임·전체 디코딩·음성 텍스트/신호 대조. 직접 청취와 정상 속도 전체 육안 시청 판정은 미실시입니다.
''')
files=[{'filename':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(O.iterdir()) if f.is_file() and f.name!='delivery-manifest.json']
(O/'delivery-manifest.json').write_text(json.dumps({'project_id':P.name,'longform_mp4_included':True,'external_caption_files_included':False,'shorts_count':3,'files':files},ensure_ascii=False,indent=2)+'\n');print(len(files),'portable files prepared')
