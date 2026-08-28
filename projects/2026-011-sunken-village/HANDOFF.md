# 인수인계: 2026-011 「소흔리에서 종이 울렸다」

이 문서만 읽으면 이어서 작업할 수 있게 정리한 것이다.
작업 위치는 `/Users/happinich/Documents/Hyperframes-codex/projects/2026-011-sunken-village`.

---

## 1. 지금 어디까지 왔나

**오디오와 대본은 완성됐고, 화면 제작만 남았다.**

| 단계 | 상태 |
| --- | --- |
| 주제 선정 | 완료 — 저수지 수몰 마을 괴담 |
| 대본 작성 | 완료 |
| **대본 승인** | **완료 (2026-08-18)** |
| **비주얼 스타일 승인** | **완료 (2026-08-18)** — `classic_rich_motion_v1` + `dark_cinematic` |
| 음성 생성 | 완료 — ElevenLabs Bin |
| 음성 검수 | 완료 — 통과 |
| **BGM 승인** | **완료 (2026-08-18)** — cand-03 적용됨 |
| 비주얼 레퍼런스 기준 | 완료 |
| 장면 이미지 생성 | **미완 — 20종 필요. 여기서 막혔다** |
| 컴포지션 제작 | 미착수 |
| 렌더 / 검수 / 게시 | 미착수 |

**막힌 이유:** 이전 작업 환경에 이미지 생성 도구가 없었다. 프롬프트는 전부 써뒀다.

---

## 2. 확정된 사실 (바꾸지 말 것)

- **제목:** 소흔리에서 종이 울렸다
- **길이:** 17분 09.8초 (음성 17분 05.8초 + BGM 아웃트로 4초)
- **포맷:** 1920x1080, 16:9, 60fps
- **제작 프로필:** `classic_rich_motion_v1`
- **비주얼 스타일:** `dark_cinematic`
- **장면 수:** 35개
- **얼굴 노출 금지** (프로젝트 기본값)
- **자막은 영상에 굽지 않는다.** SRT/VTT로 별도 납품. 검수 통과 후 별도 자막본을 따로 만든다
- 창작 괴담이며 실존 수몰 마을·댐·인물과 무관하다는 고지를 설명란에 넣는다

### 오디오 (완성, 재생성 금지)

- `02_audio/working/voice.wav` — **voice-only 마스터. 절대 덮어쓰지 말 것** (17분 05.8초, 48kHz)
- `04_composition/assets/audio/voice.wav` — **컴포지션이 쓸 파일. BGM 믹스본** (17분 09.8초, 48kHz)
- 자막 정렬률 97.3%, 313큐. 자막은 1025.8초에 끝나므로 마지막 4초 아웃트로에는 자막이 없다

**음성을 다시 만들면 안 된다.** 자막 타이밍이 전부 무효가 되고, 무음 정리 작업(19분 36초 → 17분 05.8초)을 다시 해야 한다.

---

## 3. 이야기 요약

**훅:** "30년 만에 저수지 물이 빠졌습니다. 그리고 물속에서 종이 울렸습니다. 문제는 그 종탑이 30년 전에 철거됐다는 겁니다."

화자의 어머니 정혜숙은 1996년 수몰된 소흔리 출신이다. 평생 고향 이야기를 하지 않았고, 물을 무서워했고, 8월에 비가 오면 잠을 못 잤다. 올해 5월 사망 후 유품에서 이름 42개가 적힌 붉은 수첩이 나온다.

가뭄으로 마을이 드러나자 화자는 유골을 뿌리러 간다. 그런데 이주했다는 마을에 세간이 그대로 있다 — 항아리, 정미소 기계, 8월 14일까지 찍힌 출석부, 안쪽에서 잠긴 우물, 8월 14일에 멈춘 달력.

마을회관에서 「소흔리 이주 처리 대장」을 찾는다. 42가구 전원 이주 완료 도장. **그런데 날짜가 전부 담수 당일인 8월 15일 하루에 몰려 있다.** 이장 배진구가 혼자 앉아 42번 찍은 것이다.

**반전:** 주민들은 이주하지 않았다. **이주한 것은 사람이 아니라 서류였다.** 담수 전날 밤 종을 울리며 남기로 했고, 서류상 전원 이주 처리됐기에 아무도 실종 신고를 하지 않았다. 어머니만 혼자 나왔고, 마을은 30년간 그 한 자리를 비워두고 기다렸다.

화자가 유골을 뿌린다. 등불이 물속에서 켜진다. 세어보니 **42개. 그리고 잠시 뒤 하나 더 켜져 43개**가 된다. 차로 돌아오니 가방에 넣었던 수첩이 조수석에 펼쳐져 있고, 어머니 글씨 아래 젖은 글씨로 한 줄이 더 있다 — "자리는 비워두마."

---

## 4. 지금 해야 할 일

### 4-1. 장면 이미지 20종 생성 ← 여기서 시작

**읽을 파일 (필수, 순서대로):**
1. `01_script/visual-reference.md` — 인물·장소·시대·팔레트·조명·공포강도 기준. **모든 이미지가 여기 종속된다**
2. `04_composition/assets/visuals/image-prompts.md` — 20종의 영문 프롬프트와 파일명

**생성 규칙:**
- 1920x1080 이상, 16:9, PNG
- 저장: `04_composition/assets/visuals/` 에 지정된 파일명 그대로
- 이미지에 **문자를 넣지 않는다.** 수치·표·라벨은 컴포지션에서 HTML로 얹는다
- 사람 얼굴 없음, 유혈 없음, 워터마크 없음
- **마을은 폐허가 아니다.** 무너진 지붕·잔해 금지. "30년간 물속에 있었지만 정돈된" 상태가 핵심
- 좌우 하단은 자막 안전 영역이므로 핵심 피사체를 두지 않는다

**팔레트 (엄수):**
`#05070d` 최심부 / `#0b1730` 딥네이비 / `#172b4d` 중간톤 / `#f5f7ff` 밝은 글자 / `#ff4d5f` 경고 강조 / `#3a3128` 진흙 갈색 / `#e8a33d` 등불 호박색

**호박색 `#e8a33d`는 마지막 등불 장면(`lanterns-under-water.png`)에서만 쓴다.** 앞 장면에 한 번이라도 등장하면 반전의 의미가 죽는다.

### 4-2. 컴포지션 제작

`04_composition/index.html`을 만든다. 현재는 템플릿 상태다.

- 참조 템플릿: `templates/composition-profiles/classic_rich_motion_v1/index.html`
- 장면 정의: `01_script/scene-plan.json`의 `scenes` 배열 35개.
  각 장면에 `start_seconds`, `end_seconds`, `narration_text`, `visual`, `motion`, `motion_beats`, `audio`, `transition_out`이 이미 들어 있다
- 오디오: `assets/audio/voice.wav` (1029.819초). `index.html`의 `data-duration`은 이미 갱신돼 있다
- **13개 장면은 이미지 없이 코드로 만든다** — `image-prompts.md` 하단 표 참조.
  저수율 그래프, 지적도 침수, 달력 3개 겹침, 도장 42개 그리드, 허브 다이어그램, 42가구 배치도,
  출석부, 철거 확인서, 이주 대장 표, 버스 시간표, 수문 파형 등
- **모션 규칙:** 최소 3초마다 의미 있는 정보 변화. 3초 이상 완전 정지 금지. 배경 미세 움직임 유지
- **화면에 총 러닝타임 배지를 넣지 않는다**
- 상시 장면 제목과 좌우 하단 정보 박스를 쓰지 않는다 (2026-010에서 이 방식이 승인됐다)
- **아웃트로를 4초 연장한다.** BGM이 음성 종료 후 4초 더 이어지므로 마지막 장면을 그만큼 늘려야 한다

### 4-3. 이후 순서

```bash
npm run hf:lint -- projects/2026-011-sunken-village/04_composition
python3 scripts/render_project.py projects/2026-011-sunken-village --format youtube --dry-run
python3 scripts/render_project.py projects/2026-011-sunken-village --format youtube
```

렌더 후 검수(ffprobe로 해상도·fps·코덱·길이, freeze detection, 프레임 확인) → 통과하면 자막본 생성:

```bash
node scripts/burn_karaoke_captions.mjs projects/2026-011-sunken-village
```

그다음 게시 패키지: 썸네일 2종(1280x720), 제목 6개, 설명란, 태그, 고정 댓글, SNS 문구.

---

## 5. 이번에 걸린 함정들 (반복 주의)

1. **`new_project.py`가 만드는 `elevenlabs-request.json`은 템플릿 기본값을 쓴다.**
   보이스가 다른 사람(`syYMPZoPqpHXYytuWMFR`)으로 들어가 있었고, BGM도 무관한 곡이 지정돼 있었다.
   그대로 돌렸으면 엉뚱한 목소리로 17분을 생성하고 BGM 승인 게이트를 건너뛸 뻔했다.
   → 이번 프로젝트는 Bin(`jB1Cifc2UQbq1gR3wnb0`)으로 교정 완료.

2. **`trim_audio_pauses.py`의 인자 이름이 실제 동작과 다르다.**
   ffmpeg `silenceremove`는 `stop_duration + stop_silence`의 합만큼 무음을 남긴다.
   `--min-pause 0.8 --keep-pause 0.7`은 1.5초를 남겨 아무것도 트림하지 않는다.
   이번엔 `--min-pause 0.4 --keep-pause 0.3`(합 0.7초)으로 처리했다. 스크립트 수정은 미완.

3. **BGM 후보는 고역이 거의 없다.** `dark_cinematic` 프리셋의 `base_prompt`가
   "보컬 없음, 스팅어 없음, 드럼 없음"으로 고역 요소를 전부 배제한 탓에 2kHz 이상이 -46~-53dB다.
   목소리 밑에 깔면 잘 안 들린다. 프리셋 보강은 미완.

4. **`generate_bgm_candidates.py`의 `--content-hint` 자동 추출이 쓸모없다.**
   브리프 첫 문단이 메타데이터 목록이라 "상태: 음성 검수 통과…"가 프롬프트로 들어간다.
   항상 `--content-hint`를 직접 지정할 것. 수정은 미완.

5. **`mix_bgm_with_voice()`가 48kHz를 44.1kHz로 다운샘플하던 버그는 수정 완료.**
   `audio_mixing.py`에 `OUTPUT_SAMPLE_RATE = 48000` 추가하고 회귀 테스트도 넣었다(46개 통과).

---

## 6. 가져갈 파일

**필수:**
- `01_script/narration.txt` — 승인된 대본. **한 글자도 바꾸지 말 것**
- `01_script/scene-plan.json` — 35장면 정의, 타이밍 포함
- `01_script/visual-reference.md` — 비주얼 기준
- `04_composition/assets/visuals/image-prompts.md` — 이미지 20종 프롬프트
- `00_brief/brief.md` — 기획 브리프
- `05_review/audio-review.md` — 오디오 검수 기록

**참고:**
- `03_sync/captions.srt` — 최종 자막 313큐
- `templates/composition-profiles/classic_rich_motion_v1/index.html` — 컴포지션 템플릿
- `projects/2026-010-sixth-guest/04_composition/index.html` — 같은 프로필로 만든 완성 사례
- `config/success-rules.json`, `config/production-profiles.json`, `config/visual-styles.json`
- `AGENTS.md` — 저장소 전체 작업 규칙

**오디오는 그대로 두고 쓴다:** `04_composition/assets/audio/voice.wav` (BGM 믹스 완료본)
