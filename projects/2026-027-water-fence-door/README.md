# 027 — 벽과 울타리로 막을 수 없었던 것들

2026-10-09 제작·시각/객관적 기술 검수·Google Drive 전달 완료.

- 여성 Esther / ElevenLabs eleven_v4 / 본편 원음 1.00배.
- 저수조(회화), 캠핑장(거친 2D), 배달된 문(종이 무대) 3편 합본.
- 본편 21분 11.97초, 1920×1080, 60fps, 화면 자막 없음.
- 별도 쇼츠 21.92·23.05·18.55초, 1080×1920, 60fps, 번인 자막, 1.07배.
- 5초 챕터 전환 2회 / 20초 엔드스크린 / 4초 BGM 아웃트로.
- 선택 이미지 51개 개별 2회 검수, 63개 인코딩 장면과 시작/전환/엔딩 검수.
- 최종 합본 전체 디코딩 통과, 3초 정지·1초 검정·예상하지 않은 무음 없음, 클리핑 0.

## 결과물

- [본편 MP4](06_delivery/youtube/2026-027-water-fence-door-youtube.mp4)
- [본편 게시 도우미](07_publish/youtube/youtube-publish.html)
- [쇼츠 3편 게시 도우미](07_publish/shorts/shorts-publish.html)
- [Drive 전달 폴더](https://drive.google.com/drive/folders/1tCnLGQh8YC62ObedEr0nJPGVpjfshAd8)
- [검수 체크리스트](05_review/checklist.md)
- [Drive 영수증](07_publish/drive-upload-receipt.json): 본편 MP4를 제외한 24개 파일, UI 완료 표시와 파일 목록 검증.

YouTube에는 업로드하지 않았습니다. 실제 본편 공개 후 쇼츠의 관련 동영상에서 027 본편을 선택합니다.

## 검수 범위와 한계

이미지 관찰·대본/타이밍 대조·파형 분석·Whisper와 독립 Scribe 검증을 수행했습니다. 귀로 듣는 주관적 발음·감정·음악 검수는 도구상 수행하지 못했습니다. 쇼츠 3 첫 단어 “이삿짐에”는 두 인식기의 표기 불일치가 남아 검수 기록에 보존했습니다.

## 재현

render-segmented.py는 HTML·원본 해시·프레임 수가 일치하는 완료 구간을 재사용합니다. 원본 음성·이미지·승인 기록은 이 프로젝트 안에 보관했습니다. 생성 음성·영상과 임시 검수 프레임은 로컬에 남고, 소스·승인 이미지·타이밍·전달 영수증을 Git에 기록합니다.
