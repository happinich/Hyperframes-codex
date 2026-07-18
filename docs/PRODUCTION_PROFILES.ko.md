# Hyperframes 제작 프로필

제작 프로필은 색상만 정하는 비주얼 스타일보다 상위 개념입니다. 레이아웃 밀도, 화면 변화 속도, 목표 낭독 속도, 자막 적용 방식과 납품 파일을 함께 정의합니다.

설정 파일은 [`config/production-profiles.json`](../config/production-profiles.json)입니다.

## 프로필 구분

| 프로필 ID | 이름 | 용도 | 상태 |
| --- | --- | --- | --- |
| `minimal_dark_tech_v1` | 미니멀 다크 테크형 | AI, 개발 도구, 워크플로, 단계별 설명 | 앞으로의 기본 권장 |
| `classic_rich_motion_v1` | 기존 리치 모션형 | 부동산, 경제, 정책, 다층 데이터 설명 | 기존 방식 보존 |

두 방식의 시작 템플릿도 각각 `templates/composition-profiles/<profile-id>/index.html`에 따로 저장합니다. 한 프로필의 화면 문법을 수정해도 다른 프로필 원본은 바뀌지 않습니다.

## 미니멀 다크 테크형

- 순수 검정 캔버스와 넓은 여백을 사용합니다.
- 흰색을 기본 글자로 쓰고 핵심 요소만 네온 초록으로 강조합니다.
- 화면 중앙 960~1200px 안에 한 번에 하나의 개념만 배치합니다.
- 카드 추가, 선 연결, 진행바 채움, 숫자 및 막대 성장을 1~3초마다 실행합니다.
- 완전 정지 상태가 3초 이상 지속되지 않게 미세한 글로우와 진행 움직임을 유지합니다.
- 목표 낭독 속도는 145~165WPM입니다.
- 승인된 클린 마스터를 먼저 만들고, 이후 `scripts/burn_phrase_captions.mjs`로 한 줄 흰색 문장 자막 버전을 만듭니다.
- 자막본 파일명은 `<project-id>-youtube-captioned-minimal.mp4`입니다.

주요 화면 컴포넌트:

- 아이콘 또는 로고 2개 조합
- 단계별 진행선
- 2열 비교 카드
- 비용 비교 막대
- 구조·구조 요청·검토 흐름 도식
- 명령어 또는 코드 박스
- 질문·경고·CTA 카드

## 기존 리치 모션형

- 밝은 카드, 대형 패널, 지도, 표, 허브, 차트를 장면별로 교차합니다.
- `config/visual-styles.json`의 기존 8개 스타일을 그대로 사용할 수 있습니다.
- 목표 낭독 속도는 95~135WPM입니다.
- 기존 가라오케 자막은 `scripts/burn_karaoke_captions.mjs`로 생성합니다.
- 자막본 파일명은 `<project-id>-youtube-captioned.mp4`입니다.

## 프로젝트 생성

앞으로 기본 권장 프로필은 `minimal_dark_tech_v1`입니다.

```bash
python3 scripts/new_project.py --list-production-profiles
python3 scripts/new_project.py --list-visual-styles
python3 scripts/new_project.py 2026-010-topic \
  --title "영상 제목" \
  --production-profile minimal_dark_tech_v1 \
  --visual-style minimal_dark_tech
```

기존 방식으로 만들 때는 프로필을 명시합니다.

```bash
python3 scripts/new_project.py 2026-010-topic \
  --title "영상 제목" \
  --production-profile classic_rich_motion_v1 \
  --visual-style adaptive_mix
```

프로필 ID는 아래 파일에 함께 저장됩니다.

- `00_brief/brief.md`
- `01_script/scene-plan.json`
- `01_script/production-notes.md`
- `04_composition/profile.json`
- `06_delivery/profile.json`

완료된 기존 프로젝트의 파일명과 영상은 변경하지 않습니다.
