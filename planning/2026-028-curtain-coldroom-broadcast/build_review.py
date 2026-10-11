"""Build this episode's planning artifacts; no TTS, images or renders are generated."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "01_script"
BRIEF = ROOT / "00_brief"
REVIEW = ROOT / "05_review"
for directory in (BRIEF, REVIEW):
    directory.mkdir(exist_ok=True)
PROJECT = ROOT.name
REPO = ROOT.parents[1]
RULES = json.loads((REPO / "config/success-rules.json").read_text())

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

CAMERAS = {
    "T-W": ("극장", "객석 뒤 중앙", "무대 정면", "눈높이", "wide"),
    "T-O": ("극장", "객석 왼쪽 통로", "무대 오른쪽을 향한 사선", "눈높이", "medium"),
    "T-L": ("극장", "무대 앞 왼쪽 바닥", "커튼 밑을 향한 낮은 사선", "바닥 높이", "detail"),
    "T-S": ("극장", "무대 중앙 옆", "왼쪽 줄과 커튼을 향한 측면", "가슴 높이", "medium"),
    "T-P": ("극장", "무대 왼쪽 점검자 위치", "줄을 잡는 손을 내려다보는 일인칭", "어깨 높이", "detail"),
    "T-B": ("극장", "무대 뒤 통로 오른쪽 끝", "점검등 아래 통로를 향한 사선", "눈높이", "wide"),
    "T-D": ("창고", "창고 출입문 안쪽", "문턱에서 왼쪽 무대를 보는 역방향 사선", "바닥 높이", "medium"),
    "T-H": ("극장", "무대 오른쪽 창고문 옆", "스위치와 붙잡힌 발을 향한 측면", "무릎 높이", "detail"),
    "T-X": ("극장 밖", "건물 앞 보도", "출입문을 향한 사선", "눈높이", "wide"),
    "T-R": ("집", "책상 옆", "휴대전화와 오른손을 내려다보는 일인칭", "어깨 높이", "detail"),
    "F-W": ("냉동창고", "입구 안쪽", "왼쪽 운반대와 오른쪽 선반을 향한 정면", "눈높이", "wide"),
    "F-O": ("냉동창고", "오른쪽 선반 옆", "비닐막과 입구를 함께 보는 사선", "눈높이", "medium"),
    "F-L": ("냉동창고", "운반대 옆 바닥", "바퀴와 서리 흔적을 향한 사선", "바닥 높이", "detail"),
    "F-P": ("냉동창고", "작업자 위치", "장갑·확인표·무전기를 내려다보는 일인칭", "어깨 높이", "detail"),
    "F-C": ("냉동창고", "비닐막 앞 오른쪽", "비닐막 하단을 향한 사선", "무릎 높이", "medium"),
    "F-S": ("냉동창고", "옆 통로 끝", "선반을 따라 입구를 보는 측면", "눈높이", "wide"),
    "F-A": ("냉동창고", "왼쪽 벽 가까운 작업자 위치", "안전화와 손의 접촉을 내려다보는 일인칭", "허리 높이", "detail"),
    "F-D": ("포장 구역", "출입문 바깥 왼쪽", "냉동 구역 문턱을 향한 사선", "무릎 높이", "medium"),
    "F-R": ("집", "책상 옆", "신발과 종이봉투를 보는 사선", "탁자 높이", "detail"),
    "F-X": ("포장 구역", "냉동창고 문에서 떨어진 통로", "잠긴 큰 문을 향한 정면", "눈높이", "wide"),
    "S-W": ("학교 일층", "현관 안쪽", "왼쪽 경비실과 맞은편 방송실을 향한 사선", "눈높이", "wide"),
    "S-B": ("방송실", "장비 왼쪽 옆", "마이크·화면을 향한 사선", "가슴 높이", "medium"),
    "S-P": ("방송실", "장비 정면", "잔류 인원 화면 정면", "화면 높이", "detail"),
    "S-N": ("경비실", "책상 옆", "안내 책자를 향한 일인칭", "어깨 높이", "detail"),
    "S-H": ("학교 이층", "계단 위 복도 입구", "삼 반과 다음 교실 문을 함께 보는 사선", "눈높이", "wide"),
    "S-D": ("학교 이층", "삼 반 문밖", "문 유리 너머 앞줄 책상·의자를 보는 사선", "눈높이", "medium"),
    "S-L": ("학교 이층", "삼 반 문 안쪽", "앞줄 의자 다리를 향한 낮은 사선", "바닥 높이", "detail"),
    "S-O": ("학교 밖", "현관 바깥 계단", "유리문 안 의자와 방송실을 보는 사선", "눈높이", "wide"),
    "S-G": ("학교 정문", "정문 바깥 보도", "화단과 안내 스피커를 향한 사선", "눈높이", "medium"),
    "S-F": ("학교 정문", "화단 옆", "흙에 박힌 의자 다리를 향한 사선", "바닥 높이", "detail"),
    "S-C": ("편의점", "문에서 떨어진 실내", "출입문 너머 의자와 학교 방향을 보는 사선", "눈높이", "wide"),
    "S-T": ("편의점", "문 옆 실내", "유리와 의자 등받이 접촉을 보는 측면", "가슴 높이", "detail"),
    "S-M": ("편의점", "계산대 옆", "수신 중 휴대전화를 내려다보는 일인칭", "어깨 높이", "detail"),
    "S-R": ("집", "책상 옆", "음성 메시지 화면을 향한 사선", "탁자 높이", "detail"),
}

# Each row corresponds exactly to one narration paragraph, in spoken order.
BEATS = [
 [
  ("interaction","T-P","줄을 쥔 인간 장갑 위의 흰 자국 있는 손","T-S","커튼 틈·줄·두 손만, 귀신 얼굴과 전체 몸은 가림"),
  ("normal","T-W","공연 뒤 비어 있는 객석과 무대","T-O","철수 상자를 옮기는 사람의 뒷모습"),
  ("normal","T-S","왼쪽 줄과 오른쪽 창고문","T-B","점검등 아래 폭 좁은 빈 통로"),
  ("trace","T-B","처음 확인한 빈 통로","T-L","커튼 밑 작업화처럼 보이는 검은 앞코"),
  ("trace","T-B","커튼 뒤에는 신발도 사람도 없음","T-O","객석에서 다시 보이는 같은 앞코"),
  ("trace","T-O","옮겨지는 이동식 조명","T-L","사람 그림자와 반대 방향으로 남은 발 그림자"),
  ("trace","T-L","끈과 밑창 없는 검은 발 모양","T-S","천에 손을 대지 않고 멈춘 점검자"),
  ("normal","T-S","실장과 커튼을 걷는 두 손","T-B","걷힌 커튼 뒤 빈 통로, 앞코 사라짐"),
  ("normal","T-O","조명을 원래 자리로 돌려 둠","T-S","실장이 나간 뒤 왼쪽 줄 앞 점검자"),
  ("trace","T-P","줄을 당기고 멈추는 장갑","T-L","닫히는 커튼 아래 소리의 위치"),
  ("partial","T-S","가운데 틈을 보는 점검자의 옆·뒷모습","T-B","검은 조끼 어깨와 아래로 내려온 팔, 머리 가림"),
  ("interaction","T-S","흰 손등 자국이 커튼 틈에서 나타남","T-P","그 손이 오른손 장갑 위를 덮음"),
  ("interaction","T-P","서로 구별되는 인간 장갑과 귀신 손가락 다섯","T-S","멀리 남아 있는 어깨와 가려진 팔"),
  ("interaction","T-P","왼손이 손가락을 떼려는 접촉","T-S","줄이 내려가며 닫히는 커튼과 위쪽 고리"),
  ("interaction","T-L","커튼 밖으로 옮겨 오는 검은 발","T-O","왼쪽에 선 검은 조끼 몸, 목 위는 어둠"),
  ("interaction","T-S","줄을 놓고 오른쪽 창고로 이동","T-D","문턱에서 발목을 잡은 흰 자국 손"),
  ("interaction","T-D","선반을 잡은 인간과 바닥의 발목 접촉","T-O","무대 왼쪽 몸 위치 유지, 길어진 팔은 커튼에 가림"),
  ("interaction","T-H","켜지는 점검등 스위치","T-D","빛에 얇아진 손과 신발에서 빠져나오는 발"),
  ("aftermath","T-X","건물 앞 맨발 점검자와 실장","T-B","불 켜진 빈 통로와 닫힌 막"),
  ("aftermath","T-L","줄 아래 돌아온 신발","T-P","줄에 끼워진 장갑과 실장의 멈춘 손"),
  ("aftermath","T-R","인간 손등과 발목에 남은 압박 흔적","T-R","답장 속 뒤 통로 점검등 문구, 앵글은 옆쪽으로 변경"),
  ("aftermath","T-R","휴대전화 속 새 공연 사진","T-P","사진 속 줄을 잡은 흰 자국 손, 새 사진 구도로 생성"),
 ],
 [
  ("interaction","F-A","안전화 위를 덮는 네 손가락 손","F-C","비닐막 하단과 큰 손, 몸 전체는 가림"),
  ("normal","F-D","포장 구역과 방한복을 입는 뒷모습","F-P","주황 장갑과 확인표"),
  ("normal","F-W","왼쪽 운반대·오른쪽 선반·끝 비닐막","F-S","돌아 나오는 옆 통로와 입구 비상 손잡이"),
  ("trace","F-O","비닐막 쪽에서 미끄러지는 상자","F-L","멈춘 상자와 바닥, 작업자·차량 없음"),
  ("trace","F-P","빈 상자 안쪽","F-L","바퀴 자국 사이 서리가 벗겨진 넓은 흔적"),
  ("normal","F-P","포장팀과 무전 확인","F-O","왼쪽 운반대 위에 놓은 빈 상자"),
  ("partial","F-C","가운데 두 장만 부푼 비닐막","F-O","작업복처럼 보이는 회색 등 일부"),
  ("trace","F-O","형태가 사라진 선반 틈","F-P","무전 호출과 입구로 물러서는 주황 장갑"),
  ("trace","F-W","통로를 막도록 이동한 운반대","F-L","네 갈래 홈 있는 서리 자국"),
  ("trace","F-L","자국 옆에 벗어 놓은 주황 장갑","F-P","장갑을 다시 낀 손과 움직이지 않는 운반대"),
  ("partial","F-L","바퀴 앞에서 바닥을 짚는 네 갈래 손","F-C","선반 뒤로 이어진 봉제선 없는 회색 표면"),
  ("escalation","F-P","무전 호출 버튼","F-O","작업자의 진로에 따라 옮겨지는 두 번째 상자"),
  ("interaction","F-S","옆 통로로 물러서는 작업자","F-A","비닐막 아래 손이 오른쪽 안전화를 감쌈"),
  ("interaction","F-A","신발 앞코를 누르는 네 손가락","F-C","올라간 바짓단과 비닐막의 접촉"),
  ("partial","F-O","아랫단을 채운 단일 회색 몸","F-C","넓은 머리의 가로 틈과 상자를 미는 다른 손"),
  ("escalation","F-P","살려 달라는 무전과 열린 문 쪽 빛","F-W","입구 노란 빛에 물러나는 몸 일부"),
  ("interaction","F-A","다른 발로 뒤축을 눌러 발을 뺌","F-C","회색 머리 쪽으로 밀려 가는 빈 상자"),
  ("interaction","F-O","비닐막 앞을 막도록 미는 운반대","F-S","왼쪽 벽을 따라 입구로 이어지는 탈출 동선"),
  ("aftermath","F-D","문턱 바깥으로 작업자를 당기는 직원","F-X","직원이 닫은 문과 금속 충격 위치"),
  ("aftermath","F-X","바깥에서만 점검하는 직원들","F-P","문 열림 경고 기록, 별도 정확한 글자로 편집"),
  ("aftermath","F-D","아침에 돌아온 눌린 안전화","F-R","신발의 네 줄 홈과 종이봉투"),
  ("aftermath","F-R","봉투 바닥 흰 서리","F-R","신발 홈에서 올라오는 냉기와 긁힌 종이, 반대 사선 새 이미지"),
 ],
 [
  ("trace","S-B","첫 응답 뒤 장비의 초록 빛","S-H","교실 불이 켜지는 변화, 형체·의자 이동은 숨김"),
  ("normal","S-W","마지막 선생님이 나간 현관","S-N","임시 야간 경비원의 근무표"),
  ("normal","S-W","현관 옆 경비실과 맞은편 방송실","S-N","마지막 안내에는 응답하지 말 것이라는 필기"),
  ("trace","S-B","꺼진 마이크와 안내 중 표시등","S-P","첫 응답 뒤 잔류 인원 2"),
  ("trace","S-P","숫자 2와 꺼진 마이크","S-H","계단 위에서 밝아지는 이층 복도"),
  ("trace","S-D","삼 반의 빈 책상·의자","S-H","다음 교실 불빛과 다시 들리는 의자 소리"),
  ("trace","S-L","책상에서 나온 앞줄 의자","S-H","스피커 아래 멈춘 경비원의 뒷모습"),
  ("trace","S-D","빈 교실에서 대답이 들리는 위치","S-H","문을 닫고 계단으로 내려가는 동선"),
  ("escalation","S-P","잔류 인원 3, 정상 기준과 의도적 비교","S-B","꺼진 마이크와 최근 응답 기록"),
  ("escalation","S-M","학교 근무자와 통화 화면, 학교 복도로 재배치","S-W","교실 대신 현관 바깥으로 이동할 계획"),
  ("escalation","S-P","두 대답 뒤 잔류 인원 4","S-B","전화기를 내린 인간과 방송 표시등"),
  ("escalation","S-O","열린 현관과 밖으로 나온 경비원","S-W","의자 소리가 난 빈 일층 복도"),
  ("escalation","S-O","유리문 너머 현관에 나타난 의자","S-G","정문 쪽으로 이동하며 택시 호출"),
  ("escalation","S-M","수신 중 경비실 번호, 정문 위치로 재배치","S-G","정문 안내 스피커"),
  ("escalation","S-G","화단 뒤 작은 의자","S-F","흙에 박힌 다리 네 개"),
  ("escalation","S-G","정문 밖과 길 건너 편의점","S-M","받지 않은 수신 전화와 자기 이름 안내"),
  ("escalation","S-C","편의점 안에서 보는 바깥 보도","S-M","학교 문제를 문자로 보여 줌"),
  ("escalation","S-C","문 밖에 멈춘 의자","S-M","직원에게 보여 주는 문자와 새 수신 화면"),
  ("interaction","S-M","미수신 화면에서 들리는 소리와 종료 버튼","S-T","문 유리의 의자 등받이와 잠금쇠"),
  ("aftermath","S-C","날이 밝아오며 도착한 근무자","S-M","말없이 보여 주는 마지막 안내 문구"),
  ("aftermath","S-T","마지막 안내를 기다리는 닫힌 유리문","S-C","학교 쪽으로 멀어지는 의자"),
  ("aftermath","S-O","아침 현관 밖 경비원","S-P","방송실에 남은 잔류 인원 1"),
  ("aftermath","S-R","한 달 뒤 음성 메시지 화면","S-R","자기 목소리를 듣고 멈춘 손, 옆쪽 사선 새 이미지"),
 ],
]

ANCHORS = [
 ["객석 시점 무대 왼쪽 줄", "무대 오른쪽 창고문", "무대 뒤 점검 통로", "귀신의 흰 손등 자국"],
 ["입구를 등지고 왼쪽 낮은 운반대", "오른쪽 높은 선반", "끝 비닐막", "오른쪽 옆 통로", "주황 장갑", "오른쪽 안전화"],
 ["현관 옆 경비실", "맞은편 방송실", "이층 삼 반과 다음 교실", "정문 화단", "길 건너 편의점", "같은 갈색 교실 의자"],
]
TITLES = ["객석은 비었는데, 커튼을 잡은 손이 있었다", "냉동창고 비닐막 뒤에서 상자가 움직였다", "마지막 퇴실 방송에는 대답하지 마세요"]
STYLES = ["horror_shadow_theatre", "horror_retro_3d", "horror_pixel"]
LABELS = ["그림자극", "초기 3D 공포게임풍", "픽셀아트 공포풍"]
ALTERNATIVES = [["horror_ink_charcoal"], ["horror_painterly"], ["horror_rough_2d"]]
PRIMARY = ["foreground_depth", "space_clue_action", "return_with_changed_clue"]
SUPPORT = [["clue_directed_motion", "tension_driven_transition"], ["local_darkness_texture", "tension_driven_transition"], ["space_clue_action", "sound_bridge_silence"]]
THREATS = ["explicit_ghost", "creature_or_unknown_entity", "modern_rule_horror"]
COLOR = ["검붉은 커튼·먹색 무대·약한 호박색 측광 / 종이 실루엣", "청회색 냉기·회색 존재·주황 장갑·출입문 노란 빛 / 거친 저해상도 3D 재료", "남색 복도·녹색 장비·황색 교실 빛 / 정사각 픽셀·디더링"]
REASONS = ["커튼의 가림과 손의 물리 접촉을 분리된 레이어와 새 각도 컷으로 보여 준다.", "출구가 보이는 공간에서 진로가 막히는 행동을 큰 형태와 고정 지형으로 전달한다.", "잔류 숫자와 교실 불빛의 변화를 큰 픽셀 형태로 비교하고 다른 공간 컷으로 반복감을 줄인다."]
SOURCES = ["https://www.youtube.com/watch?v=YSeyM7NUuYA&t=791s", "https://www.youtube.com/watch?v=InOPPY7IofY&t=1281s", "https://www.youtube.com/watch?v=uuKxKE_PdNA&t=1410s"]

plan = {
 "project_id": PROJECT, "title": "마지막까지 남아 있던 것들 | 창작 공포 3편",
 "status": "draft_pending_user_narration_and_direction_review", "content_nature": "fiction",
 "production_profile_id": "horror_cinematic_story_v1",
 "format_override": {"type": "three_story_anthology", "approval": "explicit_user_request_2026_10_11", "scope": "this_episode"},
 "voice_speed_multiplier": RULES['audio_rules']['longform_voice_speed']['default_multiplier'],
 "automatic_speedup": False, "timing_source": "draft_word_count_120_wpm_retime_after_actual_original_speed_tts",
 "master_format": {"width":1920,"height":1080,"fps":60,"burned_narration_captions":False},
 "shorts_format": {"width":1080,"height":1920,"fps":60,"count":3,"burned_captions":True,"voice_speed_multiplier":1.07,"fresh_portrait_assets":True},
 "screen_text_plan": {"mode":"brief_story_relevant_titles_times_and_clues", "basis":"user_requested_changed_approach_2026_10_11", "narration_burn_in_approved":False, "render_text_separately_from_generated_images":True},
 "chapters": [], "scenes": [], "transition_policy": {"narration_gap_seconds":5,"fade_to_dim_seconds":1.5,"new_chapter_cue_at":1.4,"new_location_at":2.5,"fade_up_start":3,"new_narration_at":5,"retain_visible_clue":True},
 "outro_seconds": RULES['audio_rules']['bgm']['outro_delay_seconds'], "end_screen_reserve_seconds":20,
}
cursor = 0.0
texts = []
asset_plan = []
for ci, rows in enumerate(BEATS, 1):
    cid=f"C{ci:02d}"
    text=(SCRIPT/f"story-{ci:02d}-narration.txt").read_text().strip()
    paragraphs=text.split("\n\n")
    assert len(rows)==len(paragraphs), (ci,len(rows),len(paragraphs))
    texts.append(text)
    start=cursor
    ids=[]
    for pi, (paragraph, row) in enumerate(zip(paragraphs,rows),1):
        stage,camera_a,focus_a,camera_b,focus_b=row
        sid=f"{cid}-S{pi:02d}"
        ids.append(sid)
        duration=max(5.0, round(len(paragraph.split())*.5,2))
        shots=[]
        for si,(camera,focus) in enumerate(((camera_a,focus_a),(camera_b,focus_b))):
            shot_id=f"{sid}-{'AB'[si]}"
            location,position,angle,height,size=CAMERAS[camera]
            # A new narrative image is required for each planned camera/state combination.
            reuse_reason=""
            baseline=None
            if ci==3 and camera=="S-P" and pi>4:
                baseline="C03-S04-B"
                reuse_reason="잔류 숫자 변화만 비교하는 의도된 동일 촬영 위치; 변화한 숫자는 별도 편집"
            if camera_a==camera_b and si==1:
                position += "의 반대 옆쪽"
                angle += "에서 측면 사선으로 변경"
            # Set cameras placed in different story locations explicitly.
            if ci==3 and camera=="S-M" and pi<12:
                location="학교 일층"
                position="방송실 밖 복도"
            elif ci==3 and camera=="S-M" and pi in (14,16):
                location="학교 정문"
                position="정문 밖 보도"
            if ci==2 and camera=="F-P" and pi==20:
                location="포장 구역"
                position="바깥 기록 단말 앞"
            if ci==1 and pi==22 and camera=="T-P":
                location="집에서 보는 공연 사진"
                position="사진 속 무대 왼쪽 줄을 보는 확대 삽입 컷"
                angle="새 공연 사진의 사선 관찰"
            shot={"shot_id":shot_id,"location_id":location,"start_seconds":round(cursor+duration*si/2,2),"end_seconds":round(cursor+duration*(si+1)/2,2),"camera_position":position,"camera_angle":angle,"camera_height":height,"shot_size":size,"subject_focus":focus,"spatial_anchors":ANCHORS[ci-1],"asset_id":shot_id,"new_information":focus,"reuse_reason":reuse_reason,"baseline_shot_id":baseline,"screen_text":[]}
            if ci==3 and camera=="S-P":
                shot['screen_text']=[{"role":"device_clue","text":{4:"잔류 인원 2",5:"잔류 인원 2",9:"잔류 인원 3",11:"잔류 인원 4",22:"잔류 인원 1"}.get(pi,"잔류 인원"),"method":"edited_device_text_after_image_generation","timing":"actual_spoken_point"}]
            if pi==2 and si==0:
                shot['screen_text']=[{"role":"story_title","text":TITLES[ci-1],"timing":"after_cold_open_when_setting_is_established"}]
            shots.append(shot)
            asset_plan.append({"asset_id":shot_id,"output":"longform","generation_status":"not_generated","approval_status":"pending","visual_style_id":STYLES[ci-1],"camera":shot,"entity_reveal_stage":stage,"prompt_constraint":"새 카메라 시점과 현재 사건 상태를 생성. 공간·인물·존재 기준 유지. 정확한 문자는 생성하지 않고 편집에서 구현. 귀신·괴물의 얼굴·정체를 대사보다 먼저 공개하지 않음."})
        techniques=['space_clue_action']
        if ci==1 and pi in (4,5,6,7,10,11,12,13,14,15,16,17,18):
            techniques=['foreground_depth']
            if stage in ('trace','partial'):techniques.append('clue_directed_motion')
        if ci==2 and pi in (4,6,10,12,14):techniques.append('local_darkness_texture')
        if stage in ('partial','interaction'):techniques.append('tension_driven_transition')
        if ci==3 and pi in (5,9,11,22):techniques=['return_with_changed_clue']
        if ci==3 and pi in (4,7,8,11,12,14,16,18,21):techniques.append('sound_bridge_silence')
        event_sounds = {
          1:{10:'커튼 줄·고리와 바닥 긁힘',14:'닫히는 커튼의 금속 고리',16:'넘어지며 바닥을 짚는 소리',18:'점검등 스위치',20:'줄 고리와 멈추는 바닥 긁힘'},
          2:{4:'미끄러지는 빈 상자',6:'비닐막 일부의 마찰',9:'빈 상자 안 긁힘',12:'비닐막 아래 손 마찰',13:'눌리는 안전화 앞코',17:'찢어지는 골판지와 운반대 금속',18:'큰 출입문과 안쪽 금속 충격',22:'종이봉투 내부 긁힘'},
          3:{4:'별도 퇴실 방송',6:'교실 의자 마찰',8:'별도 짧은 응답',11:'별도 두 응답',12:'현관 안 의자 마찰',14:'경비실 수신 진동과 정문 방송',16:'별도 자기 이름 안내',17:'보도 위 의자 다리 마찰',19:'유리문과 의자 접촉',21:'멀어지는 의자 다리 마찰'}
        }[ci].get(pi)
        plan['scenes'].append({"id":sid,"type":"hook" if pi==1 else stage,"start_seconds":round(cursor,2),"end_seconds":round(cursor+duration,2),"duration_seconds":duration,"purpose":focus_a+" → "+focus_b,"narration_text":paragraph,"caption_text":paragraph,"visual":shots[0]['subject_focus'],"entity_reveal_stage":stage,"shot_sequence":shots,
          "editing":{"technique_ids":techniques,"clue":focus_b,"tension_stage":{"trace":"anomaly","partial":"escalation"}.get(stage,stage),"shot_scale":shots[0]['shot_size']+"_to_"+shots[1]['shot_size'],"baseline_scene_id":"C03-S04" if ci==3 and pi in (5,9,11,22) else None,"selection_reason":REASONS[ci-1]},
          "motion":"두 새 시점 컷과 관련 단서의 가림·빛·초점을 결합. 작은 흔들림만 반복하지 않음.",
          "motion_beats":[{"at":0,"action":"첫 촬영 위치에서 공간·단서 기준을 앉힘"},{"at":round(duration/2,2),"action":"관련 대사 시점에 두 번째 촬영 위치·초점 대상으로 컷; 실제 음성 후 다시 맞춤"}],
          "motion_detail_policy":"각 컷 안의 의미 있는 가림·조명·초점·단서 공개를 1–3초 기준으로 계획하되 해당 문장의 실제 단어 타이밍으로 세분화. 장식적 흔들림은 정보 변화로 세지 않음.",
          "audio":{"narration":"approved_narration_after_review","ambience":["극장 환기와 빈 무대","냉동기와 비닐막","학교 공간음과 별도 방송"][ci-1],"foley":[{"event":event_sounds,"timing":"retime_to_actual_narration_word_or_action","status":"not_generated"}] if event_sounds else [],"bgm":"pending_voice_review_then_separate_candidate_approval","intentional_silence":None},"transition_out":"discovery_or_contact_cut" if stage in ('partial','interaction') else "motivated_cut","shorts_adaptation":"별도 원고·새 세로 자산에서 독립 재구성"})
        cursor+=duration
    chapter={"id":cid,"title":TITLES[ci-1],"narration_source":f"01_script/story-{ci:02d}-narration.txt","shorts_source":f"01_script/shorts-{ci:02d}-narration.txt","start_seconds":round(start,2),"end_seconds":round(cursor,2),"estimated_duration_seconds":round(cursor-start,2),"estimated_first_anomaly_relative_seconds":round(sum(len(p.split())*.5 for p in paragraphs[:3]),2),"scene_ids":ids,"threat_type":THREATS[ci-1],"visual_style_recommendation":{"id":STYLES[ci-1],"label_ko":LABELS[ci-1],"alternatives":ALTERNATIVES[ci-1],"approval":"pending_confirmation_with_review","brightness_palette_texture":COLOR[ci-1],"reason":REASONS[ci-1]},"reference":{"url":SOURCES[ci-1],"scope":"2026-10-05 recorded still-frame observations; not audio or current performance analysis"}}
    plan['chapters'].append(chapter)
    if ci<3:
        plan['scenes'].append({"id":f"T{ci:02d}","type":"chapter_transition","start_seconds":round(cursor,2),"end_seconds":round(cursor+5,2),"duration_seconds":5,"purpose":"낭독 쉼·국소 암전·다음 편 제목·새 공간 밝아짐","narration_text":"","caption_text":"","visual":"앞 편 단서와 다음 편 정상 공간","motion_beats":[{"at":0,"action":"1.5초 동안 단서를 남기며 어둡게"},{"at":1.4,"action":"다음 편 번호·제목"},{"at":2.5,"action":"새 편 정상 공간으로 변경"},{"at":3,"action":"5초까지 서서히 밝아짐"}],"audio":{"narration":None,"ambience":"두 공간음 교차","bgm":"approved_candidate_only","intentional_silence":{"narration_gap_seconds":5,"full_audio_silence":False}},"transition_out":"fade_up_to_next_cold_open"})
        cursor+=5
plan['narration_duration_estimate_seconds']=round(sum(c['estimated_duration_seconds'] for c in plan['chapters']),2)
plan['duration_seconds']=round(cursor+plan['outro_seconds'],2)
write_json(SCRIPT/'scene-plan.json',plan)
(SCRIPT/'narration.txt').write_text("\n\n".join(texts)+"\n")
write_json(SCRIPT/'image-generation-plan.json',{"project_id":PROJECT,"status":"planning_only_not_generated","longform_assets":asset_plan,"numeric_rules_source":"config/success-rules.json#motion_rules.horror_visuals.camera_coverage","review":"Individual full-resolution pass plus narration/adjacent-shot pass after each image is actually generated; no pass granted here."})

shorts=[]
for ci in range(1,4):
    text=(SCRIPT/f'shorts-{ci:02d}-narration.txt').read_text().strip()
    shorts.append({"id":f"SH{ci}","narration_text":text,"caption_text":text,"estimated_duration_seconds":round(len(text.split())*.5/1.07,2),"voice_speed_multiplier":1.07,"source":f"01_script/shorts-{ci:02d}-narration.txt","visual_style_id":STYLES[ci-1],"assets":[{"asset_id":f"SH{ci}-{si:02d}","generation_status":"not_generated","fresh_portrait":True,"reuse_longform":False} for si in range(1,4)],"camera_direction":["전체 장소를 세로로 읽히게 하는 새 구도","단서를 크게 보는 다른 위치·각도","정체 공개 직전의 새 관찰 시점"],"spoiler_policy":"귀신·괴물의 직접 접촉·전체 모습, 탈출 방법, 잔상 결말은 공개하지 않음.","review_status":"script_review_only_assets_and_audio_pending"})
write_json(SCRIPT/'shorts-scene-plans.json',{"project_id":PROJECT,"shorts":shorts})
editing={"project_id":PROJECT,"production_profile_id":"horror_cinematic_story_v1","status":"planned_pending_direction_review","chapters":[{"id":f"C{ci:02d}","visual_style_id":STYLES[ci-1],"primary_technique_id":PRIMARY[ci-1],"support_technique_ids":SUPPORT[ci-1],"reason":REASONS[ci-1],"excluded":["uniform shake","automatic glitch","unmotivated angle rotation"],"applied_scene_ids":plan['chapters'][ci-1]['scene_ids']} for ci in range(1,4)],"camera_coverage":{"rules_source":"config/success-rules.json#motion_rules.horror_visuals.camera_coverage","planned_shot_count":len(asset_plan),"distinct_camera_setup_ids":list(CAMERAS),"all_new_view_assets_pending":True,"same_camera_comparison_exception":"학교 잔류 인원 숫자 비교 컷만 기준 촬영 위치 유지. 이외 긴 같은 공간도 다른 시점 컷으로 전개.","plan_review":"reviewed_twice_as_text_plan_only","asset_review":"pending_generation","rendered_sequence_review":"pending_render"},"shorts":{"scene_plan_path":"01_script/shorts-scene-plans.json","new_portrait_asset_count":9,"selection":"각 위협 단서에 맞게 독립 적용"},"review":{"record_path":"05_review/editing-review.md","rendered_output":"pending"}}
write_json(SCRIPT/'editing-plan.json',editing)
approval={"project_id":PROJECT,"recorded_on":"2026-10-11","user_request":"좋아 3편 합본으로 바뀐 내용 적용해서 진행해줘.","topic_selection":{"status":"approved","chapters":["C01","C02","C03"]},"format":{"status":"approved","type":"three_story_anthology","scope":"this_episode"},"camera_variation":{"status":"approved","basis":"same_scene_new_camera_positions_and_angles_requested"},"screen_text":{"status":"planned_recommended_selective_text","narration_burn_in":False},"narration":{"status":"pending","source":"01_script/narration.txt"},"shorts_scripts":{"status":"pending"},"visual_style":{"status":"pending_confirmation","recommendations":dict(zip(('C01','C02','C03'),STYLES))},"voice":{"status":"pending_confirmation","recommendation":"female_Esther","alternative":"male_distant_documentary_delivery","model_id":"eleven_v4","speed_multiplier":1.0},"bgm":{"status":"pending_after_voice_review"},"production":{"tts":"not_started","images":"not_started","composition":"not_started","render":"not_started"}}
write_json(BRIEF/'approvals.json',approval)
write_json(BRIEF/'voice-plan.json',{"project_id":PROJECT,"status":"recommendation_pending_confirmation","primary":{"gender":"female","voice":"Esther","reason":"앞선 여성 보이스 선호를 참고한 추천. 서로 다른 세 직업의 일인칭 화자를 담담한 구술에서 불안으로 연결한다. 서사상 성별은 고정되지 않는다."},"alternative":{"gender":"male","tradeoff":"더 거리감 있는 경험담 전달; 같은 편에서도 기존 여성 보이스와 음색 대비가 커짐"},"request":{"model_id":"eleven_v4","voice_settings":RULES['audio_rules']['elevenlabs']['voice_settings'],"performance_direction":"담담한 자연스러운 존댓말 구술. 대답·괴물 소리 등은 음성 마스터에 넣지 않고 별도 연출 층으로 계획. sparse tags only in TTS source."},"postprocess":{"voice_speed_multiplier":1.0,"automatic_speedup":False,"preserve_pitch":True}})

# The entire narration is presented, rather than a synopsis, in the review page.
css="""*{box-sizing:border-box}body{margin:0;background:#11171b;color:#eee9df;font:18px/1.9 system-ui,-apple-system,sans-serif}main{max-width:920px;margin:auto;padding:40px 24px 80px}h1,h2,h3{line-height:1.45}h1{font-size:31px}h2{margin-top:45px;font-size:25px}h3{font-size:20px}a{color:#a9d7ca}nav{display:flex;flex-wrap:wrap;gap:15px}.note,.short{padding:18px 22px;background:#1c2a30;border-left:3px solid #bdafa0;margin:25px 0}.meta{color:#bcc6c9;font-size:15px}p{margin:0 0 22px;word-break:keep-all}article{border-top:1px solid #43535b;margin-top:40px;padding-top:10px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.6}th,td{border-bottom:1px solid #43535b;padding:9px;text-align:left;vertical-align:top}.table-wrap{overflow-x:auto}button{background:#243f45;color:#fff;border:1px solid #799a99;padding:8px 14px;border-radius:4px;cursor:pointer}@media(max-width:600px){body{font-size:17px}main{padding:24px 16px}h1{font-size:26px}}@media print{body{background:white;color:black}nav,button{display:none}.note,.short{background:#eee}article{break-before:page}}"""
parts=[f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>028 · 세 편 합본 대본·카메라 구성</title><style>{css}</style></head><body><main><h1>{html.escape(plan["title"])}</h1><p class="meta">창작 공포 · 총 약 {plan["duration_seconds"]/60:.1f}분 예상 · V4 · 본편 1.00배속 · 여성 Esther 추천</p><div class="note">세 편의 전체 본편 원고와 별도 쇼츠 원고, 새로운 카메라 구성입니다. 대본·동선·연출 계획을 두 차례 검토했습니다. 음성·이미지·영상은 아직 만들지 않았습니다. 길이는 추정이며 실제 원속도 낭독 후 보정합니다.</div><nav><a href="#story-1">1편 · 커튼</a><a href="#story-2">2편 · 냉동창고</a><a href="#story-3">3편 · 방송</a><a href="#direction">글자·스타일·목소리</a><a href="#shots">컷 구성</a></nav>']
for ci in range(1,4):
    chapter=plan['chapters'][ci-1]
    parts.append(f'<article id="story-{ci}"><h2>{ci}. {TITLES[ci-1]}</h2><p class="meta">약 {chapter["estimated_duration_seconds"]/60:.1f}분 · {LABELS[ci-1]} 추천</p><div id="narration-{ci}">')
    parts += ['<p>'+html.escape(p)+'</p>' for p in texts[ci-1].split('\n\n')]
    parts.append(f'</div><button onclick="copyText(\'narration-{ci}\',this)">본편 원고 복사</button><section class="short"><h3>별도 쇼츠 {ci} 전체 원고</h3><p>{html.escape(shorts[ci-1]["narration_text"])}</p><p class="meta">약 {shorts[ci-1]["estimated_duration_seconds"]:.1f}초 추정 · 새 세로 이미지 3장 계획 · 별도 음성·자막 · 정체·접촉·결말 제외</p></section></article>')
parts.append('<article id="direction"><h2>화면 글자·스타일·목소리</h2><p>나레이션 전체 번인 자막은 기본 미생성입니다. 콜드 오픈 뒤 이야기 제목, 필요한 시간·장소, 핵심 규칙·숫자·단서만 짧게 표시합니다. 정확한 글자는 이미지 생성에 맡기지 않고 편집에서 넣습니다.</p><ul>')
for ci in range(1,4):
    parts.append(f'<li><strong>{ci}편 · {LABELS[ci-1]}</strong><p>{COLOR[ci-1]}. {REASONS[ci-1]} 단서가 어둠에 묻히지 않게 국소 명암을 유지합니다. 대안: {", ".join(ALTERNATIVES[ci-1])}.</p></li>')
parts.append('</ul><p>여성 Esther를 우선 추천합니다. 주인공 성별은 서사상 고정되지 않으며, 남성 보이스를 선택하면 더 거리감 있는 경험담으로 전달할 수 있습니다. 본편은 V4 원본 1.00배속, 쇼츠는 별도 생성 후 피치 보존 1.07배속을 계획합니다.</p><p>편 사이에는 5초 낭독 쉼을 둡니다. 앞 편의 읽을 수 있는 단서를 남기며 어두워지고, 다음 편 번호와 제목이 나온 뒤 새 공간이 서서히 밝아집니다. 완전 검정 5초나 전체 무음 5초가 아닙니다.</p><p>BGM은 음성 검수 이후 후보를 별도로 제시합니다. 현재 대본·편별 스타일·목소리는 검토 후 확정할 추천안입니다.</p></article><article id="shots"><h2>같은 공간의 카메라·컷 구성</h2><p>아래는 생성 전 계획입니다. 다른 시점은 새 이미지로 제작하며 단순 크롭·줌·흔들림으로 대체하지 않습니다. 컷 시각은 현재 추정값이며 실제 나레이션 후 대사에 맞게 다시 정합니다.</p>')
for ci in range(1,4):
    parts.append(f'<h3>{ci}편 · {TITLES[ci-1]}</h3><div class="table-wrap"><table><thead><tr><th>장면</th><th>첫 시점·단서</th><th>다음 시점·단서</th></tr></thead><tbody>')
    for scene in plan['scenes']:
        if not scene['id'].startswith(f'C{ci:02d}-'):continue
        a,b=scene['shot_sequence']
        parts.append(f'<tr><td>{scene["id"]}</td><td>{html.escape(a["camera_position"])} · {html.escape(a["camera_height"])}<br>{html.escape(a["subject_focus"])}</td><td>{html.escape(b["camera_position"])} · {html.escape(b["camera_height"])}<br>{html.escape(b["subject_focus"])}</td></tr>')
    parts.append('</tbody></table></div>')
parts.append('</article><p><a href="../05_review/planning-validation.json">계획 확인 결과</a> · <a href="script-review.md">두 차례 대본 검토 기록</a></p></main><script>async function copyText(id,b){try{await navigator.clipboard.writeText(document.getElementById(id).innerText);b.textContent="복사 완료"}catch(e){b.textContent="본문을 선택해 복사해 주세요"}}</script></body></html>')
(SCRIPT/'script-review.html').write_text(''.join(parts))
print(json.dumps({"project_id":PROJECT,"stories":len(plan['chapters']),"scenes":len(plan['scenes']),"planned_longform_shots":len(asset_plan),"planned_short_assets":9,"duration_estimate_seconds":plan['duration_seconds'],"status":"planning_only"},ensure_ascii=False))
