"""Export already recorded individual decisions; never infer approvals."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
j=json.loads((p/'05_review/generated-assets.json').read_text());out=[]
for a in j['assets']:
 out.append({**a,'relative_path':str(Path(a['path']).relative_to(p)),'decision':'approved' if a.get('render_approved') else 'rejected' if a.get('pass_1')=='rejected' or a.get('pass_2')=='rejected' else 'pending'})
(p/'05_review/image-review.json').write_text(json.dumps({'project_id':p.name,'status':'individual_reviews_in_progress','assets':out},ensure_ascii=False,indent=2)+'\n')
lines=['# 개별 이미지 두 차례 검수','', '접촉·해부·구도 검수와 원고·인접 장면 대조 검수를 각각 기록한다. 미검수/제외 자산은 렌더에 사용하지 않는다.','']
for a in out:
 lines.extend(['## '+a['asset_id'],'',f"- 파일: {a['relative_path']}",f"- SHA256: {a['sha256']}",f"- 1차: {a.get('pass_1')} — {a.get('pass_1_note','')}",f"- 2차: {a.get('pass_2')} — {a.get('pass_2_note','')}",f"- 결정: {a['decision']}",''])
(p/'05_review/image-review.md').write_text('\n'.join(lines))
