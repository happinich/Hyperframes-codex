from pathlib import Path
import json,sys,hashlib,datetime
P=Path(__file__).resolve().parent;f=P/'05_review/rendered-shot-review.json';d=json.loads(f.read_text());start,end=map(int,sys.argv[1:3]);note=sys.argv[3]
for row in d['shots'][start:end]:
 row.update(manual_frame_review='approved_individually_viewed',frame_sha256=hashlib.sha256(Path(row['frame_path']).read_bytes()).hexdigest(),review_note=note,reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('Recorded output frames',start,'through',end-1)
