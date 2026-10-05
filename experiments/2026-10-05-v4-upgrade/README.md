# V4 / 제작 환경 업데이트 검증

2026-10-05, macOS arm64. 게시용 에피소드가 아닌 도구 호환성 실험입니다.

- `comparison.html`: 같은 승인 원고와 Esther 목소리로 생성한 V3/V4 비교. 오디오는 로컬에만 보관합니다.
- `comparison-metrics.json`: 실제 MP3 길이, 해시, Whisper 정렬 및 호흡 수치.
- `eleven_v3`, `eleven_v4`: 실험 요청, 원고, 자막 및 정렬 결과. V4에는 절제된 한국어 연기 지시를 넣었습니다.
- `stitching-smoke`: 앞뒤 문맥과 이전 요청 ID를 전달한 V4 2청크 실험. MP3 파일과 원본 WAV는 로컬에만 보관합니다.
- `render-smoke`: 별도 가로/세로 3초 60fps 테스트. 각 폴더의 `ffprobe.json`은 180프레임과 H.264/AAC, 3초 A/V 일치를 기록합니다.

GSAP 3.12.5는 https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js 에서 각 렌더 폴더의 `assets/gsap.min.js`로 준비했습니다. 테스트 음성은 `eleven_v4/02_audio/working/voice.wav`를 각 폴더의 `assets/voice.wav`로 복사했습니다. 생성 미디어 및 프레임은 Git에서 제외됩니다.

자막 테스트를 재실행할 때는 로컬 `06_delivery/youtube/2026-10-05-v4-upgrade-youtube.mp4`와 `03_sync/captions.words.json`을 사용합니다:

```bash
node scripts/burn_story_captions.mjs experiments/2026-10-05-v4-upgrade --sample-duration 3
```

자동 검증은 원고·타이밍·미디어 구조를 확인합니다. 주관적인 음색 평가나 배경음 혼입 청취 판정은 완료했다고 주장하지 않습니다. 자세한 기록은 `docs/reviews/2026-10-05-toolchain-v4-upgrade.md`에 있습니다.
