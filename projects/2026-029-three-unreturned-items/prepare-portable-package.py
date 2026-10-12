"""Package the reviewed episode's requested Drive deliverables only."""
from pathlib import Path
import json, hashlib, shutil
P=Path(__file__).resolve().parent
review=json.loads((P/'05_review/final-output-review.json').read_text())
assert review['status']=='verified', 'Finish final output review before packaging.'
O=P/'07_publish/drive-upload';O.mkdir(parents=True,exist_ok=True)
sources={'longform-publish.md':P/'07_publish/youtube/youtube-publish.md',
         'longform-publish.html':P/'07_publish/youtube/youtube-publish.html',
         **{f'thumbnail-{a}.png':P/f'07_publish/youtube/thumbnail-{a}.png' for a in 'ab'}}
for i in range(1,4):
    sid=f'shorts-{i:02}'
    sources[f'{P.name}-{sid}.mp4']=P/f'06_delivery/shorts/{P.name}-{sid}.mp4'
    for ext in ('md','html'):sources[f'{sid}-publish.{ext}']=P/f'07_publish/shorts/{sid}-publish.{ext}'
allowed=set(sources)|{'README.md','delivery-manifest.json'}
assert not {f.name for f in O.iterdir() if f.is_file()}-allowed, 'Unexpected file in delivery folder.'
for name,src in sources.items():
    assert src.is_file() and src.stat().st_size>0
    if src.suffix=='.html':
        body=src.read_text()
        for i in range(1,4):
            name_video=f'{P.name}-shorts-{i:02}.mp4'
            body=body.replace('../../06_delivery/shorts/'+name_video,name_video)
        (O/name).write_text(body)
    else:shutil.copy2(src,O/name)
(O/'README.md').write_text('''# 029 · 돌아오지 말아야 할 것들

본편 게시 전략: longform-publish.md / longform-publish.html
썸네일 두 안: thumbnail-a.png / thumbnail-b.png
쇼츠 세 편: 프로젝트 ID 뒤 shorts-01 / shorts-02 / shorts-03인 MP4
쇼츠별 게시 전략: shorts-01 / shorts-02 / shorts-03-publish의 MD 및 HTML

HTML 미리보기와 복사 버튼을 사용하려면 폴더 전체를 내려받아 같은 폴더에서 여세요.
본편을 채널에 업로드한 뒤 각 쇼츠의 YouTube Studio 관련 동영상에서
「돌아오지 말아야 할 것들 | 창작 공포 3편」을 지정하세요.

창작 공포 3편 합본. 여성 Esther · ElevenLabs V4 · 본편 1.00배속.
인형 스톱모션풍 / 거친 2D 애니메이션풍 / 먹·목탄풍. 쇼츠는 별도 원고·새 세로 이미지·1.07배속.
롱폼 MP4는 로컬에 보관하며 이 Drive 전달 폴더에는 포함하지 않았습니다.
YouTube 자동 자막을 사용하므로 외부 SRT/VTT는 전달하지 않습니다.
쇼츠의 자막은 영상에 포함되어 있습니다.

검수: 원본 이미지 개별 2회, 실제 영상 화면 2회 및 규격·동결·검정·신호 확인.
음성은 승인 원고와 두 ASR 결과 및 신호로 검증했으며 주관적인 청취 판정을 주장하지 않습니다.
''')
files=[]
for f in sorted(O.iterdir()):
    if f.name=='delivery-manifest.json':continue
    files.append({'filename':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(O/'delivery-manifest.json').write_text(json.dumps({'project_id':P.name,'status':'locally_verified','longform_mp4_included':False,'external_caption_files_included':False,'files':files},ensure_ascii=False,indent=2)+'\n')
print(f'{len(files)+1} portable files prepared. Upload remains separate.')
