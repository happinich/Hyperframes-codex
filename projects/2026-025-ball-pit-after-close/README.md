# 025 · 문 닫은 키즈카페, 볼풀에서 공이 하나씩 돌아왔다

창작 공포 한 편과 독립 쇼츠의 로컬 제작물이 완성됐다. ElevenLabs V4 / Esther, horror_cinematic_story_v1 / horror_cinematic. 본편 약7분49초, 쇼츠22.3초, 모두60fps.

## 결과물

- [본편 클린 MP4](06_delivery/youtube/2026-025-ball-pit-after-close-youtube.mp4)
- [독립 세로 쇼츠 MP4](06_delivery/shorts/2026-025-ball-pit-after-close-shorts.mp4)
- [본편 게시 도우미·썸네일·자막](07_publish/youtube/youtube-publish.html)
- [쇼츠 게시 도우미·자막](07_publish/shorts/shorts-publish.html)
- [최종 검수 기록](05_review/final-verification.md)

이미지별 원본/원고 대조 검수를 두 차례 수행하고 최종 렌더도 확인했다. 음성은 원본과 후처리 음성에 대해 두 차례 객관 분석했다. 직접 오디오 청취는 환경상 수행하지 못했고 발음·억양·믹스의 청취 통과를 주장하지 않는다. 공개 업로드/예약은 실행하지 않았다. 쇼츠 업로드 시 도우미에 기록한 정확한 본편을 Related Video로 지정한다.

승인 원고는 01_script/narration.txt와 shorts-narration.txt이며 원본 음성과 목소리 단독 마스터를 보존했다. scene-plan.json 및 04_composition/scene-data.json은 실제 음성 시점을 사용한다. 이미지 생성 출처/두 검수/해시는05_review/image-review.json에 기록했다. MP4·음성·렌더 캐시 등 큰 출력물은 .gitignore 정책에 따라 로컬에 보존한다.

## 기존 자산으로 재구성 및 확인

아래 명령은 저장된 자산을 사용하며 음성을 새로 생성하지 않는다. 로컬 음성/이미지 파일이 필요하다.

```bash
node projects/2026-025-ball-pit-after-close/build-composition.mjs
node projects/2026-025-ball-pit-after-close/build-shorts.mjs
.venv/bin/python projects/2026-025-ball-pit-after-close/render-segmented.py
.venv/bin/python projects/2026-025-ball-pit-after-close/verify-delivery.py
node projects/2026-025-ball-pit-after-close/review-publishing.mjs
```

render-segmented.py는 본편을 재출력한다. 쇼츠 재출력은 기존 variants/shorts.html을 Hyperframes에서 1080×1920/60fps로 별도 렌더한다.
