"""Prepare the 030 flat multi-Short package for canonical validation, no upload."""
from pathlib import Path
import json,shutil,hashlib
P=Path(__file__).resolve().parent;D=P/'07_publish/drive-upload';D.mkdir(parents=True,exist_ok=True)
sources={'longform-publish.md':P/'07_publish/youtube/youtube-publish.md','longform-publish.html':P/'07_publish/youtube/youtube-publish.html','thumbnail-a.png':P/'07_publish/youtube/thumbnail-a.png','thumbnail-b.png':P/'07_publish/youtube/thumbnail-b.png','shorts-publish.md':P/'07_publish/shorts/shorts-publish.md','shorts-publish.html':P/'07_publish/shorts/shorts-publish.html'}
for n in range(1,4):
 sid=f'shorts-{n:02}';stem=f'{P.name}-{sid}'
 sources[f'{stem}.mp4']=P/f'06_delivery/shorts/{stem}.mp4'
 for ext in ['md','html']:sources[f'{sid}-publish.{ext}']=P/f'07_publish/shorts/{sid}-publish.{ext}'
for name,src in sources.items():
 if src.suffix=='.html':
  text=src.read_text().replace('../../06_delivery/shorts/','');(D/name).write_text(text)
 else:shutil.copy2(src,D/name)
(D/'README.md').write_text('''# 030 전달 자료

독립적인 창작 공포 3편 합본 약 25분 58초. 롱폼 게시 전략, 썸네일 2안, 쇼츠 3편과 각각의 게시 전략/복사 도우미가 포함됩니다. 본편 MP4는 로컬 제작 폴더에 보관합니다.

- longform-publish.md / longform-publish.html
- thumbnail-a.png / thumbnail-b.png
- shorts-publish.md / shorts-publish.html
- shorts-01/02/03-publish.md / .html
- 프로젝트 ID가 붙은 shorts-01/02/03.mp4

HTML 복사 버튼과 미리보기를 쓰려면 폴더 전체를 내려받아 같은 폴더에서 여세요. YouTube 자동 자막, 쇼츠 영상 내 자막. 외부 SRT/VTT는 납품하지 않습니다.

쇼츠의 관련 동영상은 본편 「빈 저울의 영점을 맞췄더니 옆 의자가 눌렸어요 | 창작 공포 3편」을 실제 업로드 후 정확히 지정해야 합니다. YouTube 업로드/예약 자체는 수행하지 않았습니다.

선택 이미지 각각 두 번 및 실제 장면별 출력/쇼츠 모든 자막 큐/전체 기술 검사를 수행했습니다. 직접 청취 및 정상 속도 연속 시청 검수는 오디오 입력 도구 미지원으로 미실시입니다. 제작 파일과 검수 증거는 로컬 프로젝트 05_review에 보존했습니다.
''')
files=[dict(filename=q.name,bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()) for q in sorted(D.iterdir()) if q.is_file() and q.name!='delivery-manifest.json']
(D/'delivery-manifest.json').write_text(json.dumps(dict(project_id=P.name,files=files,longform_mp4_included=False,external_captions_included=False,review_scope='technical_and_individual_frames_passed; direct_listening_and_continuous_playback_not_performed'),ensure_ascii=False,indent=2)+'\n')
print('Portable package prepared:',len(files)+1,'files')
