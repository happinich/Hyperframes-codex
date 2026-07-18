# SNS 자동 게시 가이드

## 목적

YouTube 업로드 후 같은 홍보문을 Instagram, Threads, X에 자동 게시하기 위한 로컬 스크립트입니다.

기본값은 `dry-run`입니다. 실제 게시하려면 반드시 `--live`를 붙여야 합니다.

## 현재 지원

| 플랫폼 | 지원 상태 | 비고 |
| --- | --- | --- |
| Threads | 텍스트 게시 지원 | `THREADS_ACCESS_TOKEN`, `THREADS_USER_ID` 필요 |
| X | 텍스트 포스트 지원 | `tweet.write` 권한이 있는 `X_ACCESS_TOKEN` 필요 |
| Instagram | Reels 게시 컨테이너 지원 | 공개 HTTPS `video_url` 필요. 로컬 MP4 직접 업로드는 미지원 |

## 필요한 설정

토큰은 파일에 저장하지 않습니다. 환경 변수로만 넣습니다.

```bash
export THREADS_ACCESS_TOKEN="..."
export THREADS_USER_ID="..."
export X_ACCESS_TOKEN="..."
export INSTAGRAM_ACCESS_TOKEN="..."
export INSTAGRAM_USER_ID="..."
```

## 자동 게시를 위해 필요한 정보

### 공통

- 유튜브 영상 URL
- 유튜브 예약 공개 시간
- SNS에 올릴 문구는 프로젝트의 `07_publish/social/social-posts.json`에 저장

### Threads

- Meta 개발자 앱
- Threads 계정 ID: `THREADS_USER_ID`
- 게시 권한이 있는 액세스 토큰: `THREADS_ACCESS_TOKEN`

### X

- X Developer 앱
- OAuth 2.0 User Context에서 발급한 액세스 토큰: `X_ACCESS_TOKEN`
- 필요한 권한: `tweet.write`, 가능하면 `tweet.read`, `users.read`, `offline.access`
- 현재 스크립트는 텍스트 + 유튜브 링크 게시를 우선 지원

### Instagram

- Instagram Business 또는 Creator 계정
- Meta 개발자 앱과 연결된 Instagram 계정 ID: `INSTAGRAM_USER_ID`
- 게시 권한이 있는 액세스 토큰: `INSTAGRAM_ACCESS_TOKEN`
- Reels 자동 게시용 공개 HTTPS 영상 URL

Instagram API는 로컬 MP4 경로를 직접 받을 수 없습니다. 즉, 릴스까지 완전 자동 게시하려면 최종 MP4 또는 숏폼 파일이 외부에서 접근 가능한 HTTPS URL이어야 합니다.

설정 예시는 다음 파일에 있습니다.

```text
config/social-posting.example.json
```

## Dry-run

실제 게시 전에 반드시 먼저 확인합니다.

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID"
```

특정 플랫폼만 확인할 수도 있습니다.

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID" \
  --platform threads
```

예약 시간도 dry-run으로 먼저 확인할 수 있습니다.

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID" \
  --publish-at "2026-06-30 20:30" \
  --publish-delay-minutes 5
```

## 실제 게시

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID" \
  --platform threads \
  --live
```

## 유튜브 예약 공개 시간에 맞춰 게시

유튜브를 예약 공개로 올린 뒤, SNS를 같은 시간 또는 몇 분 뒤에 자동 게시할 수 있습니다.

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID" \
  --publish-at "2026-06-30 20:30" \
  --publish-delay-minutes 5 \
  --live
```

위 예시는 유튜브 공개 시간 5분 뒤에 SNS 게시를 실행합니다.

권장값:

- 유튜브 공개와 동시에 홍보: `--publish-delay-minutes 0`
- 유튜브 공개 후 안정적으로 홍보: `--publish-delay-minutes 5`
- 영상 처리나 공개 상태 반영이 느릴 때: `--publish-delay-minutes 10`

주의: 이 방식은 스크립트 프로세스가 예약 시간까지 켜져 있어야 합니다. 컴퓨터가 꺼지거나 잠자기 상태가 되면 게시되지 않습니다.

X도 같은 방식입니다.

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID" \
  --platform x \
  --live
```

Instagram Reels는 Meta API 특성상 공개 접근 가능한 영상 URL이 필요합니다.

```bash
python3 scripts/social_post.py \
  projects/2026-006-us-stock-gangnam-comeback \
  --youtube-url "https://youtu.be/VIDEO_ID" \
  --platform instagram \
  --instagram-media-url "https://example.com/reels-video.mp4" \
  --live
```

## 프로젝트별 게시문

게시문은 프로젝트 폴더 안에 저장합니다.

```text
projects/<PROJECT_ID>/07_publish/social/social-posts.json
```

`{youtube_url}` 자리에는 실행 시 넘긴 `--youtube-url` 값이 들어갑니다.

## 주의

- Instagram은 로컬 파일 경로를 받을 수 없습니다. 영상이 공개 URL로 접근 가능해야 합니다.
- X API는 개발자 앱 권한과 쓰기 권한이 필요합니다.
- Threads와 Instagram은 Meta 개발자 앱, 계정 연결, 적절한 권한이 필요합니다.
- 실제 게시 전에는 항상 dry-run 결과를 확인합니다.
