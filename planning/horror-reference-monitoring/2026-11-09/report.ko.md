# 공포 채널 주간 조사 — 2026-11-09 · 목록 확인, 화면 검토 보류

예약 작업 `automation-3` · 시작 2026-11-09 09:56:12 KST.
기록 시각 10:03:37 KST · 시작 브랜치 `main`, HEAD `ad4592a`.

## 결과

네 채널의 현재 최근 목록을 앱 내 브라우저에서 확인했다. 새 ID 16개 중
일반 공개 표시 9개를 검토 대기에, 회원/회원 우선 공개 4개와 대형 합본 3개를
제외 목록에 추가했다. 이전 회원 우선 공개 3개는 현재 목록 배지가 사라져
일반 플레이어 확인 대기로 옮겼으며 이전 제외 이력을 각 항목 안에 보존했다.
**배지 변화만으로 일반 재생 가능 또는 내용 검토 완료를 확정하지 않는다.**

Chrome 조사 탭 생성과 앱 내 브라우저의 영상 화면 캡처가 실패하여 새 내용 분석은
0편이다. 편집·소재 후보를 추가하지 않았다. 누적 검토 26개는 그대로이며,
대기 47개·제외 18개다. [아이디어 목록](../ideas.json)의 11개 항목은 바이트 단위로
보존했다. 마지막 실제 화면 내용 보고서는 [2026-11-02](../2026-11-02/report.ko.md)다.

## 접근 방법과 실제 확인 범위

| 대상 | 현재 목록 확인 방법·범위 | 내용 검토 |
| --- | --- | --- |
| [Mr. Nightmare](https://www.youtube.com/@MrNightmare/videos) | 앱 내 브라우저 최근 4항목 | 프레임 0, 청취 없음 |
| [돌비공포라디오](https://www.youtube.com/@돌비공포라디오/videos) | 앱 내 브라우저 최근 8항목 | 프레임 0, 청취 없음 |
| [왓섭](https://www.youtube.com/@왓섭/videos) | 앱 내 브라우저 최근 9항목 | 프레임 0, 청취 없음 |
| [괴들남](https://www.youtube.com/@괴들남/videos) | 앱 내 브라우저 최근 4항목 | 프레임 0, 청취 없음 |

웹 열람은 Mr·돌비·괴들남에서 오래된 저작권 푸터만, 왓섭에서 조회 제한을 반환했다.
이를 최신 목록이나 신작 부재의 근거로 쓰지 않았다. Chrome 인벤토리는 응답했지만
문서화된 탭 생성 API는 `timeoutMs` 속성 오류로 실패했다. 문제 해결 문서를 읽고
CUA 세션을 한 번 초기화한 뒤 재시도해도 같은 결과였다. 사용자 탭은 조작하지 않았다.

앱 내 브라우저는 네 목록의 제목·링크·게시 표시·회원 배지를 정상 반환했다.
의도한 기록 범위는 위 표의 최근 25항목이며 전체 카탈로그를 따로 수집하거나
스크롤하지 않았다. 최초 DOM 응답에 이 범위 밖 제목도 포함됐으나 분석·상태 수집에서
제외했다. 조회수는 성과나 유지율 판단에 사용하지 않았다.

Mr의 [미검토 영상](https://www.youtube.com/watch?v=6aZH2a40BCU)을 열어 58초 스폰서
광고를 건너뛴 뒤 원 영상 길이 **1574.621초**를 확인했다. 일시정지·음소거 후
키 탐색으로 5초에 놓았으며 `paused=true`, `muted=true`, `readyState=4`까지 확인했다.
그러나 `screenshot`과 대체 `getScreenshot` 모두 `Page.captureScreenshot` 시간 초과로
실패했다. **5초의 실제 영상 프레임은 보지 못했다.** 준비 상태·시각만으로 장면을
추정하지 않았으며 `observed_segments=[]`로 남겼다. 다른 세 채널의 원 영상 플레이어는
열지 않았다. 조사 전용 앱 내 탭은 닫았다.

초반·중반·후반·전환 주변 화면, 컷 속도, 모션, 첫 문장 훅, 단서 공개 순서,
소리·BGM, 실제 썸네일 이미지, Shorts 연결은 이번에 검증하지 못했다.
챕터는 `not_inspected`다. 브라우저 자막·오버레이도 원본 번인 편집으로 귀속하지 않았다.
이는 조사 도구의 오류이며 YouTube나 채널 자체 장애라는 뜻은 아니다.

## 새로 식별한 일반 공개 표시 ID — 내용 검토 대기

게시 표시는 현재 목록의 상대 날짜다. 제목은 식별용 축약이며 원 채널의 실화·범죄
주장을 검증한 기록이 아니다. 링크·표시·분류 원본은 [state.json](../state.json)의
이번 `listing_observations`에 있다.

| 채널 | ID·식별 제목 | 게시 표시 | 목록 길이 |
| --- | --- | --- | --- |
| Mr | [6aZH2a40BCU · October Horror Stories](https://www.youtube.com/watch?v=6aZH2a40BCU) | 3일 전 | 26분 |
| 돌비 | [mD_3uqR6au8 · 시골 미친 언니](https://www.youtube.com/watch?v=mD_3uqR6au8) | 2시간 전 | 29분 |
| 돌비 | [JtQEB6jJmzU · 유럽 도살자](https://www.youtube.com/watch?v=JtQEB6jJmzU) | 2일 전 | 44분 |
| 돌비 | [XKQ9HjoD2Cs · 피원하모니](https://www.youtube.com/watch?v=XKQ9HjoD2Cs) | 3일 전 | 47분 |
| 돌비 | [nWMIeHee4nM · 셰어하우스](https://www.youtube.com/watch?v=nWMIeHee4nM) | 4일 전 | 57분 |
| 돌비 | [DgHBihNQ1K8 · 자수하고 싶은 건달](https://www.youtube.com/watch?v=DgHBihNQ1K8) | 5일 전 | 37분 |
| 돌비 | [F5R_kkGJpvk · VIP 금기사항](https://www.youtube.com/watch?v=F5R_kkGJpvk) | 6일 전 | 34분 |
| 왓섭 | [w2V1rVb-Yq4 · 우리 춘천 이모 08화](https://www.youtube.com/watch?v=w2V1rVb-Yq4) | 1일 전 | 17분 |
| 괴들남 | [GquaSi147EY · 출장 알바](https://www.youtube.com/watch?v=GquaSi147EY) | 6일 전 | 14분 10초 |

Mr의 새 ID `6aZH2a40BCU`는 이전 제외 ID `V-JNxhZya-w`와 제목이 같지만
동일 콘텐츠·교체 업로드인지 확인하지 않았다. ID가 다르므로 이전 이력을 덮어쓰지 않았다.

### 이전 회원 우선 공개 → 현재 목록 배지 없음

- [3InoqTW0IpI · 동물병원의 악몽](https://www.youtube.com/watch?v=3InoqTW0IpI): 3시간 전, 32분.
- [P-v1VYKKBXU · 악귀](https://www.youtube.com/watch?v=P-v1VYKKBXU): 5일 전, 20분.
- [QgMgpOOHLq4 · 오피스 괴담](https://www.youtube.com/watch?v=QgMgpOOHLq4): 6일 전, 52분.

세 항목 모두 `public_listing_player_unverified`로 대기한다. 원래 제외 행 전체를
`prior_exclusion_record`로 보존했다. 그 외 과거 제외 영상의 현재 공개 상태는 재확인하지 않았다.

### 이번에 새로 제외한 ID

| 이유 | ID·현재 목록 표시 |
| --- | --- |
| 회원 전용 | [oulccPTl3pg](https://www.youtube.com/watch?v=oulccPTl3pg) Cold Night, 3일 전·24분; [sZntZ2HASEI](https://www.youtube.com/watch?v=sZntZ2HASEI) Bonus Halloween, 5일 전·13분 |
| 회원 우선 공개 | [E93oad0FFr4](https://www.youtube.com/watch?v=E93oad0FFr4) 연쇄 살인귀, 3일 전·51분; [mRrFQ54ULWk](https://www.youtube.com/watch?v=mRrFQ54ULWk) 일본 연수, 5일 전·17분 |
| 대형 모음·통합본 | [9Y343tTfcEk](https://www.youtube.com/watch?v=9Y343tTfcEk) 팔자 모음, 1일 전·2시간 1분; [IH1HfrLHwr0](https://www.youtube.com/watch?v=IH1HfrLHwr0) 지배 통합본, 3일 전·3시간 4분; [B9k5m55BSeg](https://www.youtube.com/watch?v=B9k5m55BSeg) 괴담 모음, 3일 전·1시간 4분 |

제외는 목록 표시와 제목을 근거로 하며 내용 분석은 아니다. 긴 단일 사연을 길이만으로
합본으로 분류하지 않았다. 기존 검토 ID가 목록에 다시 보여도 내용 분석을 반복하지 않았다.

## 두 차례 검토와 다음 기획 연결

1. **출처·관찰 정확성:** 현재 DOM 목록·과거 웹 푸터·광고 길이·원 영상 길이·캡처 실패를
   분리했다. 새 ID 16개와 배지 변화 3개를 기존 ID 집합과 대조하고, 영상 프레임·음향을
   확인한 것으로 승격하지 않았다. 채널별 상세 검토 0편으로 상한 3편을 지킨다.
2. **이야기·스타일·모바일 적용:** 실제 화면 근거가 없어 신규 기법·소재 추천을 보류한다.
   기존 7기법과 아이디어 11개를 유지하며 새 프로젝트의 브리프·편집 계획에 적합한 후보를
   연결하는 기존 절차를 따른다. 이번 감시로 제작을 시작하거나 완료 작품을 수정하지 않는다.

다음 예약에서는 대기 ID의 정상 원 영상과 화면 캡처부터 확인한다. 특히 배지가 사라진
3편은 일반 플레이어 접근 검증을 먼저 거친다. 연결이 계속 실패하면 Chrome의 Codex
브라우저 연결 상태와 앱 내 브라우저 화면 캡처 기능 확인이 필요하다.

## 저장·검증

이번 변경은 보고서와 `state.json` 두 파일이다. `latest_report`는 이번 목록/오류 기록을,
`latest_successful_content_report`는 11월 2일을 유지한다. 네 채널의 내용 검토 대기를
`pending_channel_checks`에 남겼으며 현재 목록까지 미확인인 것으로 기록하지 않았다.

검증 **PASS**: JSON, ID 집합 중복·상호 배타성, 이전 검토 26개·기존 대기 35개·기존 실행
이력 보존, 이전 제외 14개 중 3개 이력 보존 이동, 새 대기 9개·제외 7개, 아이디어 바이트
동일성, 채널 URL·회차 상한·보고서 링크를 대조했다. 기존 관련 없는 Git 상태 526항목과
완료 프로젝트·원고·생성 미디어를 보존한다. 관련 두 파일만 커밋하고 현재 브랜치에 푸시한다.
