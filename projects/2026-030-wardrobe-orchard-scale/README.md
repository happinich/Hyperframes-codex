# 030 · 빈집·과수원·고물상의 밤

독립적인 창작 공포 세 이야기, 본편 25분 58초. 본편 1920×1080 60fps, 쇼츠 3편 각각 1080×1920 60fps. 원래 본편 음성 1.00x, 쇼츠 별도 음성 1.07x 피치 보존 후처리.

## 결과

- `06_delivery/youtube/2026-030-wardrobe-orchard-scale-youtube.mp4`
- `06_delivery/shorts/2026-030-wardrobe-orchard-scale-shorts-01.mp4` ~ `03.mp4`
- `07_publish/youtube/youtube-publish.html` 및 MD, 썸네일 A/B
- `07_publish/shorts/shorts-publish.html` 및 각 쇼츠 게시 도우미

YouTube 자동 자막. 본편 연속 번인 자막 없음, 쇼츠 번인 자막 포함. 외부 SRT/VTT 납품 없음. YouTube 업로드는 수행하지 않음. Drive 결과는 `07_publish/drive-upload-receipt.json`을 확인.

## 실제 검수와 한계

선택 이미지 117장 각각 두 번, 실제 본편 108숏의 원본 프레임, 쇼츠의 모든 자막 큐와 첫/마지막 프레임, 썸네일 2안 확인. 4개 최종 MP4의 ffprobe·전체 동결/검정 검사·오디오 길이·클리핑·Whisper 대조 수행. 직접 청취 및 정상 속도 연속 시청 검수는 도구 지원 한계로 미실시이며 전체 시청·청취까지 완료했다고 간주하지 않음. 구체적 근거는 `05_review/`에 기록.

## 재구성

최종 계획과 음성·이미지가 존재하는 상태에서 `build-composition.py`, `render-segmented.py`, `build-shorts.py`, `render-shorts.py`로 재구성할 수 있음. 선택 이미지의 승인 해시를 렌더 전에 검사하고 본편은 54분절 렌더 후 합침. 음성 원본 유지, BGM 적용은 TTS를 다시 생성하지 않음.

`finalize-review.py`, `prepare-project.py`, `lock-timing.py`, `lock-scale-clues.py`, `repair-orchard-plan.py`, `refine-*`, `correct-*`, `restore-cart-shot.py`는 제작 중 사용한 일회성 수정 이력이며 최종 계획에 다시 실행하면 안 됨. `prepare-publishing.py`도 게시자료/썸네일 HTML을 덮어쓰므로 승인된 수정 뒤에는 주의할 것. 원본·이전 제외 이미지·음성·렌더 결과는 로컬에 보존하며 Git에서는 제외.
