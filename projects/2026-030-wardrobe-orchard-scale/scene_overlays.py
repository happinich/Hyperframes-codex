"""Diegetic clues share image transforms; timed values never alter narration."""
import json,html
from pathlib import Path
P=Path(__file__).resolve().parent
def overlays_for_shot(item,offset_seconds,local_duration):
    f=P/'01_script/diegetic-clue-layouts.json'
    layouts=json.loads(f.read_text()) if f.exists() else {}
    row=layouts.get(item['asset'])
    if not row:return '',[]
    markup,cues=_one(row,item['id']+'-clue',item,offset_seconds,local_duration)
    for i,extra in enumerate(row.get('extra_clues',[])):
        more,events=_one(extra,item['id']+f'-clue-extra-{i}',item,offset_seconds,local_duration)
        markup+=more;cues.extend(events)
    return markup,cues
def _one(row,key,item,offset_seconds,local_duration):
    quad=row['quad'];tl,tr,bl=quad
    a=(tr[0]-tl[0])/340;b=(tr[1]-tl[1])/340;c=(bl[0]-tl[0])/90;d=(bl[1]-tl[1])/90
    initial=row.get('initial','');font=row.get('font_size',62)
    box=row.get('view_box',[1672,941])
    markup=f'<svg class="clue-layer" viewBox="0 0 {box[0]} {box[1]}"><g transform="matrix({a} {b} {c} {d} {tl[0]} {tl[1]})"><text id="{key}" x="170" y="67" text-anchor="middle" font-size="{font}" fill="{row.get("color","#b8d8a2")}" font-family="monospace">{html.escape(initial)}</text></g></svg>'
    start=max(0,item['startFrame']/60-offset_seconds);end=min(local_duration,item['endFrame']/60-offset_seconds)
    cues=[]
    for event in row.get('events',[]):
        time=event['seconds']-offset_seconds
        if start<=time<end:
            cues.append(f"tl.set('#{key}',{{textContent:{json.dumps(event['text'],ensure_ascii=False)}}}, {time});")
        elif time<start:initial=event['text']
    # Establish the correct prior value when a scene is rendered independently.
    cues.insert(0,f"tl.set('#{key}',{{textContent:{json.dumps(initial,ensure_ascii=False)}}}, {start});")
    return markup,cues
