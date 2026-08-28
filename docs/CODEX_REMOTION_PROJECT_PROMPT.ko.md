# Codex용 Remotion 자동 영상 제작 프로젝트 프롬프트

아래 프롬프트 전체를 새 Codex 작업에 한 번에 입력합니다. 가능하면 `Hyperframes-codex`와 같은 상위 폴더에서 작업을 시작합니다.

```text
당신은 TypeScript, React, Remotion, FFmpeg 기반 자동 영상 제작 시스템을 구축하는 시니어 엔지니어입니다.

현재 다음 소스 프로젝트가 있습니다.

- 기준 프로젝트: /Users/happinich/Documents/Hyperframes-codex
- 새 프로젝트 목표 경로: /Users/happinich/Documents/Remotion-codex

이번 작업의 목적은 기존 Hyperframes 프로젝트에서 확립한 제작 규칙을 Remotion 기반의 독립적인 자동 영상 제작 시스템으로 옮기는 것입니다.

중요:

1. 기존 Hyperframes-codex는 읽기 전용 참고 자료로 사용하세요.
2. 기존 프로젝트, 완성 영상, 대본, 자막, 게시 패키지를 수정하거나 삭제하지 마세요.
3. 새 구현은 반드시 Remotion-codex 폴더 안에 만드세요.
4. 설명이나 계획만 제시하고 멈추지 말고, 구현·테스트·샘플 렌더·문서화까지 완료하세요.
5. 진행 중 합리적으로 판단할 수 있는 세부 사항은 직접 결정하세요. 파괴적인 선택이나 계정·결제 정보가 필요한 경우에만 질문하세요.
6. API 키, SNS 토큰, 비밀번호를 코드나 JSON에 저장하지 마세요. 환경 변수 이름과 .env.example만 제공하세요.

## 1. 시작 전 조사

먼저 아래 파일을 읽고 기존 시스템의 실제 규칙과 데이터 형식을 파악하세요.

- Hyperframes-codex/README.md
- Hyperframes-codex/config/success-rules.json
- Hyperframes-codex/config/production-profiles.json
- Hyperframes-codex/config/visual-styles.json
- Hyperframes-codex/docs/WORKFLOW.ko.md
- Hyperframes-codex/docs/PRODUCTION_PROFILES.ko.md
- Hyperframes-codex/docs/SCENE_PLANNING.ko.md
- Hyperframes-codex/scripts/new_project.py
- Hyperframes-codex/scripts/generate_elevenlabs_audio.py
- Hyperframes-codex/scripts/align_captions.py
- Hyperframes-codex/scripts/analyze_audio_pacing.py
- Hyperframes-codex/scripts/burn_story_captions.mjs
- Hyperframes-codex/projects/2026-009-wealth-exit-core-assets

Remotion은 구현 시점의 npm 최신 안정 버전을 확인해 사용하세요. `remotion`과 모든 `@remotion/*` 패키지는 정확히 같은 버전으로 고정하세요. 현재 공식 문서를 우선 기준으로 삼고, 폐기 예정 API나 과거 예제는 사용하지 마세요.

Remotion 라이선스 조건도 확인하여 `docs/REMOTION_LICENSE.ko.md`에 개인 제작, 팀 사용, 대량 자동 렌더 시 확인해야 할 사항을 간단히 기록하세요. 라이선스 판단을 코드로 강제하지는 마세요.

## 2. 기술 기준

- TypeScript strict mode
- React
- Remotion
- Zod 기반 입력 데이터 검증
- ESLint와 Prettier
- Vitest 또는 현재 코드베이스에 적합한 테스트 도구
- 60fps
- YouTube: 1920x1080, 16:9
- Shorts: 1080x1920, 9:16
- 출력 코덱: H.264
- 픽셀 포맷: yuv420p
- 오디오 포함
- macOS Apple Silicon 로컬 렌더 우선

모든 애니메이션은 Remotion의 프레임을 기준으로 결정적이어야 합니다.

- `useCurrentFrame()`
- `useVideoConfig()`
- `interpolate()`
- `spring()`
- `<Sequence>`
- `<Series>`
- `<Audio>` 또는 현재 권장 미디어 컴포넌트

CSS transition, setTimeout, 실시간 Date, Math.random, GSAP 타임라인처럼 렌더마다 결과가 달라질 수 있는 방식은 사용하지 마세요. 난수가 필요하면 프로젝트 ID와 씬 ID를 시드로 사용하세요.

렌더 중 외부 URL에 의존하지 마세요. 폰트, 이미지, 오디오, 영상은 프로젝트 로컬 자산으로 정규화하고 `staticFile()` 또는 현재 공식 권장 방식으로 읽으세요.

## 3. 프로젝트 구조

다음 구조를 기준으로 더 나은 세부 구조가 있으면 보완하세요.

Remotion-codex/
  README.md
  package.json
  remotion.config.ts
  .env.example
  config/
    production-profiles.json
    visual-styles.json
    success-rules.json
  docs/
    WORKFLOW.ko.md
    DATA_SCHEMA.ko.md
    PRODUCTION_PROFILES.ko.md
    REMOTION_LICENSE.ko.md
  src/
    index.ts
    Root.tsx
    schemas/
    compositions/
      LongformClean.tsx
      LongformCaptionedMinimal.tsx
      LongformCaptionedKaraoke.tsx
      ShortsClean.tsx
      ThumbnailStill.tsx
    profiles/
      minimal-dark-tech/
      classic-rich-motion/
    components/
      typography/
      diagrams/
      charts/
      captions/
      backgrounds/
      transitions/
    lib/
      timing/
      captions/
      project-loader/
      validation/
  scripts/
    create-project.ts
    prepare-assets.ts
    generate-audio.ts
    align-captions.ts
    render-project.ts
    verify-render.ts
    create-publish-package.ts
  projects/
    <project-id>/
      00_brief/
      01_script/
      02_audio/
      03_sync/
      04_remotion/
      05_review/
      06_delivery/
      07_publish/
  public/
    projects/
  tests/

프로젝트 데이터와 미디어를 중복 저장하지 않도록 `prepare-assets.ts`가 렌더 직전에 필요한 파일만 `public/projects/<project-id>/`로 복사하거나 안전한 방식으로 준비하게 하세요.

## 4. 데이터 모델

기존 `scene-plan.json`을 그대로 버리지 말고 Zod 스키마로 공식화하세요.

최소 데이터:

- project ID와 제목
- production profile ID
- visual style ID
- fps, width, height
- 실제 오디오 길이
- 씬 목록
- 씬 시작·종료 초
- 씬 시작·종료 프레임
- narration_text
- caption_text
- visual type
- motion beats
- 강조 단어와 색상
- Shorts 재배치 지침
- 자막 cue
- 단어별 start/end 타이밍

필수 규칙:

1. `narration.txt`가 발화 문구의 단일 기준 원문입니다.
2. `caption_text`는 `narration_text`와 정확히 일치해야 합니다.
3. Whisper 인식문은 자막 문구를 새로 쓰는 데 사용하지 않고 실제 발화 시간 보정에만 사용합니다.
4. 씬 시간은 최종 음성의 단어 타이밍으로 다시 계산합니다.
5. 초를 프레임으로 바꿀 때 하나의 공통 함수만 사용해 반올림 오차를 통제하세요.
6. 앞 씬 종료 프레임과 다음 씬 시작 프레임 사이에 의도하지 않은 공백이나 중첩이 없어야 합니다.
7. Remotion의 `calculateMetadata()`를 사용해 최종 오디오와 씬 종료 시점으로 `durationInFrames`를 계산하세요.
8. 입력 props는 JSON 직렬화 가능한 값만 사용하고 Zod로 검증하세요.

## 5. 제작 프로필 두 가지

### A. 신규 기본 프로필

ID: `minimal_dark_tech_v1`

이 프로필을 앞으로 신규 프로젝트의 기본 권장값으로 만드세요.

- 순수 검정 배경
- 흰색 메인 타이포
- 제한적인 회색 보조 텍스트
- 네온 초록 강조
- 화면 중앙 960~1200px 정보 영역
- 한 화면에 핵심 개념 하나
- 카드 추가, 선 연결, 진행바, 숫자 변화, 막대 성장, 터미널 코드, 단계 도식
- 의미 있는 화면 변화가 1~3초마다 발생
- 본문 애니메이션 없이 자막만 바뀌는 구간 금지
- 3초 이상 완전 정지 금지
- 미세한 글로우·진행 움직임은 보조 수단일 뿐이며 핵심 정보 변화로 계산하지 않음
- 큰 패널, 과도한 글래스 효과, 복잡한 대시보드, 무관한 스톡 이미지는 사용하지 않음
- 목표 낭독 속도 145~165 WPM

### B. 기존 보존 프로필

ID: `classic_rich_motion_v1`

- 기존 Hyperframes 방식의 밝은 에디토리얼, 다크 시네마틱, 명암 분할, 따뜻한 다큐멘터리, 프리미엄 금융, 네온 테크, 종이 콜라주, 주제 혼합형을 보존
- 카드, 지도, 표, 허브, 차트, 대형 타이포를 장면별로 교차
- 최소 3초마다 의미 있는 정보 변화
- 목표 낭독 속도 95~135 WPM

두 프로필은 색상 변수만 다르게 한 동일 컴포넌트가 아니라, 독립된 레이아웃·모션 문법을 가진 구현으로 분리하세요. 공통 저수준 컴포넌트는 공유해도 되지만 프로필별 scene renderer와 design token은 분리하세요.

완료된 기존 프로젝트를 새 프로필로 자동 변환하거나 덮어쓰지 마세요.

## 6. 자동 씬 렌더러

씬 플랜의 `visual.type`에 따라 아래 시각 장치를 자동 선택할 수 있게 만드세요.

- `headline`
- `question`
- `stat`
- `comparison`
- `flow`
- `timeline`
- `bar-chart`
- `table`
- `hub`
- `map`
- `code`
- `quote`
- `warning`
- `cta`

각 장치는 다음을 만족해야 합니다.

- 긴 한국어 제목의 동적 폰트 크기 조절
- 한 글자만 다음 줄에 남는 고아 줄 방지
- 도형과 글자 겹침 방지
- 좌우 120px 안전 영역
- 자막용 하단 안전 영역 확보
- 화면 오른쪽 위 총 영상 시간 표시 금지
- 표는 행 순차 등장, 값 강조, 마커 이동
- 흐름도는 노드 등장 후 연결선 드로잉
- 허브는 중심 노드와 외부 노드를 순서대로 연결
- 그래프는 막대·숫자가 실제 프레임에 따라 성장
- 내레이션보다 화면이 약 0.35초 먼저 준비되도록 시각 리드 적용

씬마다 동일한 2열 카드 레이아웃만 반복하지 말고 정보 구조에 따라 시각 장치를 바꾸세요.

## 7. 오디오 파이프라인

기존 기능을 독립 프로젝트 안에서 계속 사용할 수 있게 구현하세요.

ElevenLabs:

- 모델 ID: `eleven_v3`
- voice ID는 환경 변수 또는 프로젝트 요청 JSON에서 받음
- API 키는 `ELEVENLABS_API_KEY` 환경 변수로만 받음
- language code: `ko`
- stability: 0.50
- similarity_boost: 0.75
- style: 0.15
- use_speaker_boost: true
- 공백 포함 약 1,000~1,300자 단위로 문장 기반 청크 분할
- 마침표, 물음표, 느낌표, 줄바꿈 우선
- 문장 중간 분할 금지
- 청크 순차 생성
- 청크별 재시도와 오류 메시지
- 모든 청크를 최종 voice-only 오디오로 병합

BGM:

- BGM이 짧으면 최종 길이까지 반복
- 목소리 구간 BGM 기본 -18dB
- 허용 범위 -20~-15dB
- 목소리 종료 후 기본 4초 아웃트로
- 아웃트로에서 BGM을 약간 올릴 수 있음
- 마지막 3초 페이드아웃
- 최종 길이: 목소리 길이 + 아웃트로
- voice-only 파일과 mixed 파일 모두 보존

Remotion 컴포지션은 최종 mixed 오디오를 사용하되, 오디오 생성·분석 단계와 영상 렌더 단계를 분리하세요.

## 8. Whisper와 자막

기본 정렬 모델:

`mlx-community/whisper-large-v3-turbo`

기존 Python MLX Whisper 구현을 안전하게 재사용하거나 독립 도구로 이식해도 됩니다. 단, Remotion 내부에서 Whisper를 실행하지 말고 렌더 전 전처리 단계에서 아래 파일을 완성하세요.

- captions.srt
- captions.vtt
- captions.words.json
- sync_report.json
- pacing_report.json

품질 기준:

- 원문과 정렬 일치율 0.92 이상
- 긴 무음 0.8초 이상 검출
- 긴 단어 간격 0.8초 이상 검출
- 느려지는 구간과 지나치게 빠른 구간 보고
- 검수 상태가 실패면 렌더 중단

Remotion에서 다음 두 가지 영상 컴포지션을 제공하세요.

1. `LongformClean`
   - 번인 자막 없음
   - 외부 SRT/VTT 업로드용

2. `LongformCaptionedStory`
   - 두 롱폼 프로필 공통
   - 하단 중앙의 읽기 좋은 짧은 구문
   - 44px, 굵기 700의 흰색 글자
   - 6px 검정 외곽선과 그림자
   - 현재 단어 색상 추적과 이동 효과 없음
   - 파일명: `<project-id>-youtube-captioned-story.mp4`

`@remotion/captions`의 현재 공식 타입과 도구를 활용하되 기존 `captions.words.json`을 어댑터로 변환하세요. 자막 한 줄의 폭을 측정해 화면 밖으로 나가지 않게 하고, 긴 문장은 cue 또는 phrase 단위로 나누세요.

## 9. Remotion 컴포지션

`Root.tsx`에서 최소 다음 항목을 등록하세요.

- `Longform-Clean`
- `Longform-Captioned-Story`
- `Shorts-Clean`
- `Thumbnail-Still`

각 Composition은 Zod schema와 기본 props를 가져야 합니다.

`Longform-*`:

- 1920x1080
- 60fps
- 동적 durationInFrames

`Shorts-Clean`:

- 1080x1920
- 60fps
- 단순 좌우 크롭 금지
- 씬 플랜의 shorts_adaptation을 사용해 중앙 집중형으로 재배치

`Thumbnail-Still`:

- 1280x720
- 얼굴 없는 자극적 썸네일
- 큰 한국어 후킹 문구
- 핵심 숫자 또는 대비
- 작은 글자, 워터마크, 잘못된 한글 금지

## 10. 프로젝트 명령

다음과 유사한 명령을 구현하세요. 정확한 명령명은 일관성이 더 좋아진다면 조정할 수 있습니다.

- `npm run studio`
- `npm run typecheck`
- `npm run lint`
- `npm test`
- `npm run project:new -- <project-id> --title "제목" --profile minimal_dark_tech_v1 --style minimal_dark_tech`
- `npm run project:validate -- <project-id>`
- `npm run audio:generate -- <project-id>`
- `npm run captions:align -- <project-id>`
- `npm run render:clean -- <project-id>`
- `npm run render:captioned -- <project-id>`
- `npm run render:shorts -- <project-id>`
- `npm run render:thumbnail -- <project-id>`
- `npm run verify -- <project-id>`
- `npm run publish:package -- <project-id>`

렌더 자동화는 공식 방식 중 하나로 구현하세요.

- CLI: `npx remotion render`와 JSON props 파일
- 프로그램 방식: `bundle()`을 소스 변경 시 한 번 실행하고, `selectComposition()`과 `renderMedia()`를 사용해 여러 프로젝트를 렌더

여러 영상을 연속 렌더할 때 매번 새로 bundle하지 마세요. 동일 소스 번들을 재사용하고 프로젝트 props만 바꾸세요.

## 11. 출력 파일

프로젝트별 출력:

- `06_delivery/youtube/<project-id>-youtube.mp4`
- `06_delivery/youtube/<project-id>-youtube-captioned-story.mp4`
- `06_delivery/shorts/<project-id>-shorts.mp4`
- `03_sync/captions.srt`
- `03_sync/captions.vtt`
- 썸네일 2개
- `07_publish/youtube/youtube-publish.html`
- `07_publish/youtube/youtube-publish.md`

YouTube 게시 도우미에는 다음을 포함하세요.

- 메인 제목
- 추천 제목 5개
- 한 번에 복사 가능한 설명란
- 실제 영상 길이에 맞는 타임스탬프
- 태그
- 해시태그
- 고정 댓글
- X, Threads, Instagram 홍보 문구
- 추천 게시 시간
- 각 영역 복사 버튼

HTML이 지원되지 않는 Markdown 미리보기에서 `<style>`이나 `<button>` 코드가 그대로 노출되지 않게 하세요. 복사 기능은 HTML 파일에서 제공하고 Markdown은 순수 문서로 유지하세요.

## 12. 검증

다음 테스트를 반드시 구현하고 실행하세요.

단위 테스트:

- 초→프레임 변환
- 씬 경계 연속성
- 동적 영상 길이 계산
- 프로필 선택
- 긴 제목 폰트 축소
- 자막 cue 선택
- 현재 단어 하이라이트
- caption_text와 narration_text 일치
- 출력 파일명

통합 테스트:

- 최소 8초짜리 `minimal_dark_tech_v1` 샘플 프로젝트
- 최소 8초짜리 `classic_rich_motion_v1` 샘플 프로젝트
- 클린 렌더
- 스토리 구문 자막 렌더
- 16:9와 9:16 컴포지션 확인

렌더 QA:

- ffprobe로 해상도, fps, 코덱, 오디오 스트림, 길이 확인
- 영상과 오디오 길이 오차 확인
- 첫 장면, 중간 장면, 마지막 장면 프레임 추출
- 텍스트 잘림과 도형 겹침 확인
- 3초 이상 정지 화면 탐지
- 마지막 프레임이 의도치 않은 검정 화면인지 확인

실제 샘플 렌더를 만들기 전에는 기존 2026-009 프로젝트의 텍스트·씬 구조만 참고하세요. 기존 파일을 이동하거나 수정하지 마세요.

## 13. 완료 조건

아래 조건을 모두 만족할 때만 완료라고 보고하세요.

1. Remotion-codex가 독립적으로 설치됩니다.
2. `npm run studio`가 실행됩니다.
3. TypeScript, lint, test가 통과합니다.
4. 두 제작 프로필이 코드와 설정에서 분리되어 있습니다.
5. 샘플 클린 영상이 실제로 렌더됩니다.
6. 작은 고정형 스토리 구문 자막본이 렌더됩니다.
7. ffprobe 검수가 통과합니다.
8. API 키가 저장소에 없습니다.
9. README에 전체 사용 순서가 한국어로 정리되어 있습니다.
10. 기존 Hyperframes-codex에는 변경이 없습니다.

마지막 보고에는 다음만 간결하게 포함하세요.

- 생성된 프로젝트 경로
- 사용한 Remotion 버전
- 주요 구조
- 실행 명령
- 테스트 및 샘플 렌더 결과
- 남은 제한 사항
- Remotion 라이선스 확인 필요 사항
```

## 공식 참고 문서

- [Remotion 공식 사이트](https://www.remotion.dev/)
- [Composition](https://www.remotion.dev/docs/composition)
- [Parameterized rendering](https://www.remotion.dev/docs/parameterized-rendering)
- [Captions](https://www.remotion.dev/docs/captions)
- [CLI render](https://www.remotion.dev/docs/cli/render)
- [bundle()](https://www.remotion.dev/docs/bundle)
- [renderMedia()](https://www.remotion.dev/docs/renderer/render-media)
