# 공포 영상 비실사 스타일 제안
상태: 비교 검토 완료 후 사용자 선택 대기. 기존 025 영상과 드라이브 파일은 이번 검토에서 수정하지 않는다.

## 현재 화면이 선명하게 느껴지는 원인
025 이미지 프롬프트는 photorealistic-natural, photograph, photographic natural detail, crisp mobile-readable focal clue를 명시한다. 넓은 천장 형광등과 바닥 반사, 사실적인 재질이 공간 전체를 설명한다. 합성의 밝기 변화(1.04→0.96)는 이 실사 성격을 크게 바꾸지 않는다. 실제 원본 shot-03과 생성 프롬프트/합성 소스를 확인했다.

## 추천
A: 어두운 회화풍. 거친 과슈·유화 붓질과 단순한 명암 덩어리, 그림자에 일부 녹는 윤곽, 탁한 청록/먹색/갈색, 작은 붉은 단서. 사람이 그린 공포 삽화처럼 인상을 남기면서 손·물체 접촉·공간 관계도 읽을 수 있는 방향이다. 이 판단은 채널 영상 문법과 사용자의 미감 요청에 따른 연출 제안이며 조회수 개선이 검증된 결과는 아니다.

B: 먹·목탄풍. 거의 흑백, 문지른 목탄과 불규칙한 검은 면. 악몽·심리·귀신 이야기의 특집에 어울리지만 물체 색이나 접촉 관계가 단서일 때 구분이 어려울 수 있다.

C: 거친 2D 애니메이션 배경풍. 단순한 외곽선과 명암 블록, 손으로 칠한 배경. 긴 이야기의 공간/인물 연속성을 표현하기 편리한 방향이지만 매끈한 웹툰·귀여운 그림체는 피한다.

## 생성할 때
- nonphotographic hand-painted horror illustration, broad matte pigment masses, simplified material detail, irregular soft/lost edges, selective low-key lighting를 기본으로 제안.
- photographic, crisp microdetail, glossy CGI, HDR, bright even lighting 같은 실사/선명도 지시는 제외.
- 단서를 제외한 배경의 세부 묘사와 채도를 줄이고 국소 조명만 둔다.
- 원본 공간은 정상적인 장소다. 그림의 거친 질감을 실제 벽 파손·곰팡이·폐건물로 바꾸지 않는다.
- 사람의 손과 물체 접촉, 귀신/생물의 정체 확인은 대사 순서에 맞게 읽혀야 한다. 의도적으로 거친 화법과 생성 오류를 구분한다.

## 영상으로 만들 때
배경/중경/단서를 나누어 느린 팬·접근·약한 시차를 적용하고 불빛과 그림자가 대사에 반응하도록 한다. 화면 전체의 과한 흐림 대신 배경 윤곽만 부드럽게 처리한다. 채도 낮은 그림, 절제한 입자·종이 질감, 간헐적인 국소 조명 변화를 유지한다. 완전한 검정이나 뿌연 안개로 단서를 가리지 않는다. 1–3초의 의미 있는 변화, 모바일 단서, 마지막 15–20초 엔드스크린 공간 같은 기존 제작 기준은 지킨다.

## 참고
- Adobe, Low-key vs high-key lighting: https://www.adobe.com/creativecloud/video/discover/low-key-vs-high-key-lighting.html — 주변광을 제한하고 조명을 통제해 강한 명암 대비와 시선 집중을 만드는 원리.
- BFI, 10 great German expressionist films: https://www.bfi.org.uk/lists/10-great-german-expressionist-films — 그림자와 악몽 같은 공간의 표현을 공포 시각 언어의 참고로 사용.

## 범위
시안은 내장 image_gen으로 새로 만든 비교 이미지이며 제작 영상에 적용된 최종 자산이 아니다. 기존 프로젝트의 장소 사진을 구도 참고로 사용했다. 추천 스타일의 영구 기본값 변경과 기존 본편/쇼츠 재제작은 선택 이후 진행한다.

## 비교 시안과 생성 기록

[최종 A/B/C 비교 이미지](style-comparison.png). 위부터 A 회화풍, B 먹·목탄풍, C 거친 2D 애니메이션 배경풍입니다. 내장 image_gen으로 생성하고 세부 묘사를 줄이는 한 차례 수정 후 원본 크기 검수와 기준 구도/서사 대조 검수를 완료했습니다. 첫 시안은 사진처럼 세부가 많이 남아 비교 최종본에서 제외했습니다. 프롬프트 전문은 [prompts.json](prompts.json), 검수/해시는 [review.json](review.json)에 보관합니다. 최종 제작 스타일 승인과 기존 영상의 재제작 승인은 아직 요청받지 않았습니다.
