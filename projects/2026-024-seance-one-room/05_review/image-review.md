# 이미지 개별 검수 기록

본편 생성 이미지는 생성 직후 원본 해상도로 확인하고, 실제 대사와 앞뒤 장면에 대조했다. 렌더에 사용할 컷은 최종 크롭·모션을 다시 검수해야 한다. 이 문서는 아직 완료 기록이 아니다.

| 자산 | 생성 출처·해시 SHA-256 | 1차 원본 검수 | 2차 대본·인접 장면 검수 | 최종 판정 |
| --- | --- | --- | --- | --- |
| `04_composition/assets/references/apartment-location-v1.png` | built-in image_gen · `8223b7139337ad2ed2c973d0d80e2f9f767f1d69dbae495bc49067c30c384e1c` | 통과. 현관 왼쪽, 바로 옆 싱크대, 오른쪽 침대와 책상, 신발장·블라인드·편의점 흰빛이 읽힌다. 인물·문자 없음. | 통과. 원고의 좁은 원룸 지리와 일치. 컷 간 기준 이미지로 사용. | 기준 이미지 승인 |
| `04_composition/assets/references/entity-four-finger-v1.png` | built-in image_gen · `58c85518a7845b2a674acd7a5a09b415fcc42e8feaa060f68d452c42c3e1c77a` | 통과. 검고 차가운 표면, 손가락 총 네 개가 분명하다. 다른 손·얼굴·상처 오류 없음. | 통과. 원고의 네 줄 손목 자국과 카메라 속 네 손가락에 맞는 존재 기준. 초반에는 이 전체 이미지를 노출하지 않음. | 존재 기준 승인 |
| `04_composition/assets/visuals/shot-01-rejected-v1.png` | built-in image_gen · 현관·원룸 기준 참조 | **실패. 가운데 인물의 머리와 목이 사라진 듯한 비정상 신체.** | 사용 불가. 첫 장면의 세 사람을 물리적으로 납득하기 어렵게 함. | 렌더 제외, 새 구도로 재생성 |
| `04_composition/assets/visuals/shot-01.png` | built-in image_gen · `727b114f350439718596c4be37a452d96ade9fc1be1d9a06ce756e4e6b2ba9ca` | 통과. 탑다운 구도에서 가장자리의 세 사람 손·무릎만 보인다. 중앙 빈 자리, 팔다리 수와 접촉 자연스러움. 얼굴·문자 없음. | 통과. 첫 ‘셋인데 넷’ 훅을 직접 보여주되 존재의 형상은 미리 공개하지 않음. 다음 정상 원룸 장면과 조명·바닥 연결됨. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-04.png` | built-in image_gen · `ebc0806fdb35f4d34acf9522ada4f250fee8b77df5fcd1aeada20e1c70a9032e` | 통과. 포장된 수저 세트가 정확히 네 벌이며 각각 숟가락과 젓가락이 읽힌다. 글자·얼굴 없음. | 통과. 43.5초 첫 이상 징후에 수량 단서를 보여 주고 다음 신발장 컷의 여분 한 벌로 연결. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-05.png` | built-in image_gen · `b1d5dde866907888ccbb85c4a9b69d2988078964806df4853f901cea029782f4` | 통과. 신발장 위 포장 수저 한 벌, 동일한 현관문과 붉은 반사광. 사람·문자 없음. | 통과. 네 벌 중 남는 한 벌을 신발장에 둔 대사와 일치. 이후 포장지만 남는 장면을 제작할 때 같은 신발장 위치 유지. | 컷 승인, 출력 크롭 재검수 대기 |


| `04_composition/assets/visuals/shot-02.png` | built-in image_gen · `22e780a45f1bf58985a8c28a0e738c1ff968031862b6ff007450ef079d07dee2` | 통과. 세 명의 소매·무릎·손이 가장자리에서 들어오고 떡볶이를 먹는 정상적인 장면. 신체 수·접촉 자연스러움, 얼굴·글자 없음. | 통과. 첫 훅에서 정상적인 금요일 원룸으로 전환하고, 네 번째 수저는 아직 보여주지 않는다. 다음 공간 컷과 동일 위치·조명. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-03-rejected-v1.png` | built-in image_gen · 원룸 기준 참조 | **불확실. 오른쪽에 사람처럼 보일 수 있는 세운 천과 좌석이 있다.** | 사용하지 않음. ‘숨을 곳이 없는 빈 방’이라는 대사와 혼동된다. | 렌더 제외, 재생성 |
| `04_composition/assets/visuals/shot-03.png` | built-in image_gen · `03a14d67857c7784342d9c3f383281320ed9cb8a341022df0aaa039ad72e4bce` | 통과. 출입문·싱크대·침대·책상이 한눈에 들어오고 빈 바닥이 명확하다. 사람·그림자 오류 없음. | 통과. 좁아서 누가 서 있으면 보인다는 말과 일치. 다음 수저 네 벌 단서 전의 정상 공간이며 선공개 없음. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-16-rejected-v1.png` | built-in image_gen · 원룸 기준 참조 | 통과. 도어락 네 붉은 점과 수저 한 벌이 보인다. | **실패. 수저는 다음 날 아침에야 나오는 단서인데 밤의 도어락 컷에 함께 나타났다.** | 렌더 제외, 밤·아침 컷 분리 재생성 |
| `04_composition/assets/visuals/shot-16-night-lock.png` | built-in image_gen · `2fdc12943a2c0e155739cf51fb87cba62fd30171e9f99ee3c4037f00c6ba0099` | 통과. 도어락의 작은 붉은 표시 네 개, 비어 있는 바닥·신발장, 물리적으로 일관된 문 위치. | 통과. 네 번의 소리와 빈 복도에 맞고 다음 아침 수저를 미리 노출하지 않음. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-16-morning-utensil.png` | built-in image_gen · `317420feefef216f14abc8cd8524b5ca147ef776a8b55b5deaa1143b9b29a80f` | 통과. 아침 신발장 앞 바닥에 포장 없는 숟가락 한 개와 젓가락 한 쌍. 다른 세트·문자 없음. | 통과. 전날 수저 실종 뒤 재등장 대사 시점에 맞춘다. 밤 컷과 문·신발장 지리 연결됨. | 컷 승인, 출력 크롭 재검수 대기 |


| `04_composition/assets/visuals/shot-06.png` | built-in image_gen · `f788b802f349815e08d1d38023bf89b086b1e816489994dba26333655ea330d3` | 통과. 준호의 손과 검은 휴대폰 화면, 신발장 위 수저 한 벌. 손가락·기기 기하 자연스럽고 얼굴·글자 없음. | 통과. ‘손님 세기’ 글을 내미는 대사에 후반 그래픽으로만 정확한 제목을 붙일 수 있다. 수저가 아직 신발장 위인 전후 연속성 유지. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-07-rejected-v1.png` | built-in image_gen · 원룸·세 사람 참조 | 통과. 손 수는 대체로 자연스럽고 손전등은 꺼져 있다. | **실패. 세 사람 모두 연결된 원을 보여줘야 하는 넓은 구도에서 좌우 인물 사이 손 연결이 끊긴다.** | 렌더 제외, 접촉을 가까운 구도로 재생성 |
| `04_composition/assets/visuals/shot-07.png` | built-in image_gen · `bcbb1cf9d058a439d6bcbb0beef2248ac4d7cb04d311c603110a8a1748667d30` | 통과. 화자의 왼손·오른손이 각 친구의 손과 자연스럽게 맞잡혀 있고 미점등 손전등 한 개. 얼굴·여분 손 없음. | 통과. 셋이 손잡는 규칙의 화자 시점 일부만 보여줘 전체 원을 잘못 확정하지 않는다. 이후 왼손 은채·오른손 준호 접촉과 이어진다. | 컷 승인, 출력 크롭 재검수 대기 |

| `04_composition/assets/visuals/shot-09.png` | built-in image_gen · `1da7455ab935c0e5fc2a2ec65fbc4cbcfe7ddf9e982e8067e80c8dd2c9896142` | 통과. 소등된 원룸, 희미한 냉장고 빛과 블라인드 흰빛. 완전 검정 아님. | 통과. 손전등 의식 전의 소리·조도 묘사와 일치하고 존재의 모습을 선공개하지 않음. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-10.png` | built-in image_gen · `538be753bd51443057aeeb0c38a755df8a64933af1b3c518e89a57527b079eae` | 통과. 손을 잡은 인물 일부와 꺼진 손전등, 빈 러그의 어긋난 빛. 눈에 띄는 여분 손 없음. | 통과. 웃음이 멎고 적막이 길어지는 장면에 빈 자리만 보여준다. 넷째 목소리 전의 비노출 유지. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-11.png` | built-in image_gen · `2dcb7f0aa049c4b5417e3352213032c1b2a4e9fe5a499fbb2f090247aaf125a3` | 통과. 화자의 뒷어깨와 원룸의 빈 틈, 얼굴·귀 클로즈업 없음. | 통과. 오른쪽 귀 가까운 넷째 목소리는 공간감과 음향으로 전달하고 실제 형상은 아직 보이지 않음. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-12-wrapper.png` | built-in image_gen · `203d5869b59cb4e603f42e5a22f020229cccf7ffa07817dfafac4b861306b0ab` | 통과. 현관 신발장에 포장된 수저 한 벌. 문과 가구 위치 일관됨. | 통과. 바스락거리는 소리의 출처를 보여주되 수저는 아직 포장 안에 있어 이후 실종 시점과 맞음. | 컷 승인, 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-12-wrist-rejected-v1.png` | built-in image_gen · `70ad596cd5a684de8cafc9decd62cdeaac2dcfdfc2c4c8813a761bbc5c28b109` | 불확실. 맞잡은 두 손의 접촉 위치와 손 구조가 모호하다. | 실패. 준호는 손바닥을 잡고 보이지 않는 존재가 그 위 손목을 눌러야 하는데 분리 표현이 불명확하다. | 렌더 제외, 단일 손목 구도로 재생성 |
| `04_composition/assets/visuals/shot-12-wrist.png` | built-in image_gen · `86b5d9de1eebca73765f7f8bfb0c9d839ecbbdc0808cdb3a469c758b8ab6c77e` | 통과. 정상적인 단일 팔·손목, 러그와 꺼진 손전등 연속성. 손상·여분 손 없음. | 통과. 보이지 않는 압박은 음향·후반 그래픽으로 처리하고 이 이미지에 유령 손을 선공개하지 않음. | 컷 승인, 압박 효과 및 출력 크롭 재검수 대기 |
| `04_composition/assets/visuals/shot-13-rejected-v1.png` | built-in image_gen · `1b33984fae6e38ff1ab9b7187cc47f624ff268322a51b2a8f06ad80560c77168` | 불확실. 화자 시점 아래의 맞잡은 손이 누구의 것인지 모호하다. | 실패. 눈을 뜬 시점의 손 연결을 잘못 암시할 수 있다. | 렌더 제외, 손 없는 구도로 재생성 |
| `04_composition/assets/visuals/shot-13.png` | built-in image_gen · `b2c0e1aa54cf19942e6f9fc15025095ee6f8e7e3286f0f1224c3bc78ed6752cf` | 통과. 은채의 크림색 옷과 긴 머리, 준호의 검은 상의·짧은 머리가 뒷모습으로만 보인다. 얼굴·여분 인물 없음. | 통과. 화자가 눈을 뜬 뒤 두 친구와 빈 공간을 확인하는 대사에 맞는다. 손목은 별도 삽입 컷. | 컷 승인, 출력 크롭 재검수 대기 |

나머지 본편·쇼츠·썸네일 이미지는 생성 후 각 행에 두 차례 검수와 교체 이력을 추가한다. 승인되지 않은 자산은 렌더에 사용하지 않는다.

## 2026-10-01 추가 생성 이미지 개별·인접 장면 재검수

| 자산 | 출처·SHA-256 | 원본 1차 검수 | 원고·전후 장면 2차 검수 | 결정 |
|---|---|---|---|---|
| `04_composition/assets/visuals/shot-08.png` | built-in image_gen · `80a7b2230c11c16fee4e74cc0136dda3892500f9b574905107bddbc3d9e6e540` | 통과: 크림·검정·회색 소매의 세 사람, 꺼진 손전등, 빈자리. 손 수와 얼굴 노출 확인. | 통과: s07 손 연결에서 s09 암실로 이어지며 넷째 존재를 선공개하지 않음. | 승인 |
| `04_composition/assets/visuals/shot-14.png` | built-in image_gen · `45f037c1e0c1dd204371481289b461455e9a81e2c11f8536d3bfec218a4d0452` | 통과: 두 친구 뒷모습만 문밖으로 이동, 방 구조와 조명 일관. | 통과: s13 이후 이탈, s15의 빈 포장지 발견 전에는 수저 실종을 드러내지 않음. | 승인 |
| `04_composition/assets/visuals/shot-15.png` | built-in image_gen · `f2348b411680489733a4b2991d159b236b0e8519ae23b6667f72d60e2fb71dea` | 통과: 신발장 위 포장지만 남고 내부는 빈 상태, 실제 글자·얼굴 없음. | 통과: s14의 남겨진 수저에서 실종으로 변화, s16의 재등장과 위치 연결. | 승인 |
| `04_composition/assets/visuals/shot-17.png` | built-in image_gen · `fa491a8cd6cf217bc030f954294ad2622f3cf8d08b424ea031e555ef01814a91` | 통과: 정상 손과 빈 휴대전화 화면, 문·침대 지리 일치. | 통과: s17의 안 읽음 숫자는 후반 그래픽 대상이며 다음 편의점 장면으로 자연 전환. | 승인 |
| `04_composition/assets/visuals/shot-18.png` | built-in image_gen · `76e176680f7caa885a5c652e98fff093ab343eff5219a7761469ac2974cc1509` | 통과: 점원 뒷모습과 비어 있는 통로, 시선 방향과 계산대 지리 정상. | 통과: s18 질문의 보이지 않는 동행자를 암시하되 후반 정체를 드러내지 않음. | 승인 |
| `04_composition/assets/visuals/shot-19-rejected-v1.png` | built-in image_gen · `1eacefd4f46f60498fdbf2a5b159b24507acf2b5d8c57b379d5e2f2b77a6faf8` | 실패: 이불 주름이 네 손가락 압박 흔적으로 분명히 읽히지 않음. | s19의 네 자국 단서 불충족. | 렌더 제외 |
| `04_composition/assets/visuals/shot-19-rejected-v2.png` | built-in image_gen · `ae24441366a72de40a251dc29cfeea46f9e097d3bd10bbc4de5ea4e8e8538600` | 실패: 네 개의 솟은 천 돌출이 압박이 아닌 돌출로 보임. | s19의 눌린 자국 단서 불충족. | 렌더 제외 |
| `04_composition/assets/visuals/shot-19.png` | built-in image_gen 기초 컷 · `1eacefd4f46f60498fdbf2a5b159b24507acf2b5d8c57b379d5e2f2b77a6faf8` | 통과: 침대·원룸 지리와 천 질감 정상. 단독으로 네 자국이 약해 코드 기반 네 압박 그림자와 결합하도록 용도 제한. | 통과: `shot-19-composite-test.png` 완성 프레임에서 네 줄이 구분되고 s18의 흔적에서 s20의 전화로 연결. 유령 전체 미노출. | 합성 후 승인 |
| `04_composition/assets/visuals/shot-19-rejected-v3.png` | built-in image_gen · `14e6c4fc7265a480537ede3747a17d40f974e0c749a7c76c0e2d5c3da5986e4e` | 실패: 세 번째 재생성도 홈 개수가 모호함. | s19의 정확한 네 자국을 독립 이미지로 증명하지 못함. | 렌더 제외 |
| `04_composition/assets/visuals/shot-19-rejected-v4.png` | built-in image_gen · `4f93a3cd2822832bfd1bc138beb2c021e1b24e51ead91158f3414e1f2e380d52` | 실패: 네 번째 재생성도 세 개의 큰 홈처럼 보임. | s19의 정확한 네 자국을 독립 이미지로 증명하지 못함. | 렌더 제외 |
| `04_composition/assets/visuals/shot-20.png` | built-in image_gen · `574949559c532db0715725a42e006195cc90c809a0e1448e8dfbb8d1ab1246c4` | 통과: 준호의 검은 상의·뒷모습, 손과 문 구조 정상, 과거 색감 구별. | 통과: s20의 작년 기억을 현재 원룸과 구분하며 피해자나 결말 선공개 없음. | 승인 |
| `04_composition/assets/visuals/shot-21.png` | built-in image_gen · `ad5ea2211b7cc430a18213c6ad3b709a904455a0fe53a88531c0fb8eee7b2f7d` | 통과: 전화 화면과 양손 구조 자연, 문·침대 지리 유지, 글자·얼굴 없음. | 통과: s21 통화와 손목 시선, s22 연락처 망설임 사이 연결. | 승인 |
| `04_composition/assets/visuals/shot-22.png` | built-in image_gen · `10aff65781ae07bcebff5dc580108267e2d097ea82a040ea3475ba0eac2c6d74` | 통과: 정상 손과 연락처 행, 가짜 이름이나 글자 없음. | 통과: s22의 호출 망설임에서 s23 카메라 앱 장면으로 기기 동선 유지. | 승인 |
| `04_composition/assets/visuals/shot-23.png` | built-in image_gen · `39777a4c68eb2bc2729ebebc410e7e53350dfda5cc4af56ba833201cf58a47e2` | 통과: 휴대전화 화면 속 천장에만 검은 손가락 네 개, 실제 방에는 없음. 손·화면 기하 확인. | 통과: s23 부분 노출로 s24 실제 손목 접촉에 앞서 같은 표면·형태로 존재를 확인. | 승인 |
| `04_composition/assets/visuals/shot-24.png` | built-in image_gen · `ad1667d0310016ac5eb21fccfd38f3abbd5e121313cc9b6da130a48a64baf82e` | 통과: 화면 속 네 손가락과 실제 손목을 감싼 동일 질감의 손, 물리 접촉·팔 구조 확인. | 통과: s23 카메라 속 부분 노출에서 직접 접촉으로 진행, 과도한 상처 이미지는 없음. | 승인 |
| `04_composition/assets/visuals/shot-25.png` | built-in image_gen · `cf945bbf1019d880f409d40dd6e1d4805e32494cefbf21dc57b39c1d72eaa1e5` | 통과: 도어락 붉은 표시와 화자 뒷어깨 옆 빈 공간, 얼굴·여분 인물 없음. | 통과: s25 다섯 번째 소리는 음향·조명 펄스로 보강하고 오른쪽 엔드스크린 공간 유지. | 승인 |
| `04_composition/assets/shorts/short-01.png` | built-in image_gen · `767f7ce5e7d0550271e44850ba333e069cbe885c9c2e258a32195f217b831af2` | 통과: 별도 세로 생성, 정확히 세 사람과 큰 빈자리, 얼굴 없음. | 통과: 쇼츠 첫 장면 훅, 본편 첫 이미지와 다른 구도·해시. | 승인 |
| `04_composition/assets/shorts/short-02-rejected-v1.png` | built-in image_gen · `8cb3e75124d9031c04bf1454d93e90254b346bc59f38d8042b8474a352388c97` | 실패: 배경 인물 두 명의 얼굴이 보여 face-free 정책 위반. | 쇼츠 중간 내레이터 귀 뒤 공간도 흐려짐. | 렌더 제외 |
| `04_composition/assets/shorts/short-02.png` | built-in image_gen · `fe2225721ec66529c15ebc6fb80fa518b3ed68a7b444dee1e4f4277cef7f93ce` | 통과: 뒷머리·귀·어깨와 비어 있는 공간만 보이고 얼굴 없음. | 통과: 넷째 목소리 장면, 앞선 세 사람 구도와 다음 손목 그림자 사이 공포 단계. | 승인 |
| `04_composition/assets/shorts/short-03.png` | built-in image_gen · `7f6f13e396b818346076dbd4b1dc780b586f4b3bce72b608361086fcf2809eaa` | 통과: 정상 팔·손목, 네 줄 그림자, 상처·여분 손 없음. | 통과: 차가운 접촉을 암시하되 쇼츠에서 정체·결말을 공개하지 않음. | 승인 |
| `04_composition/assets/shorts/short-04.png` | built-in image_gen · `148647e927a0c00255d6f990d18616f91476a3e3054a5fe53a134291c27b72ca` | 통과: 네 개의 도어락 붉은 점과 빈 포장지, 글자·얼굴 없음. | 통과: 쇼츠 마지막 완결 문장과 일치, 본편 세로 자산과 다른 신규 생성 해시. | 승인 |
| `07_publish/youtube/thumbnail-a.png` | 승인 소스 이미지 + HTML/CSS 타이포 합성 · `41b67f8b2b3630e54d3bd8b691bc609856915636261f17815e74e3d310e55b21` | 통과: 1280×720. 수저 네 벌이 모두 보이고 제목 5음절이 모바일 크기로 읽힘. | 통과: 본편 s04 단서와 일치, 본편 제목과 역할이 중복되지 않음. | 승인 |
| `07_publish/youtube/thumbnail-b.png` | 승인 소스 이미지 + HTML/CSS 타이포 합성 · `6fc10a4de80a005238f6916c309466f44aae9a2544e16fdc2883af067e237090` | 통과: 1280×720. 카메라 속 네 손가락과 제목 5음절, 얼굴·문자 오류 없음. | 통과: 본편 s23 이미지 출처·부분 노출 시점과 일치, 결말 직접 공개 없음. | 승인 |

렌더 출력 크롭은 본편·쇼츠 완성본 프레임 검수에서 별도 확인한다. 쇼츠 승인 자산 4개는 본편 승인 이미지와 파일 경로·SHA-256이 모두 다르다.

## 완성본 크롭·움직임 재검수

- 본편 25개 씬의 시작 프레임을 `longform-scene-contact-sheet.png`로 훑고 s01·s19·s23·s24·s25 및 마지막 엔드스크린을 원본 출력 크기로 개별 확인했다. 중요한 단서가 크롭에 잘리거나 얼굴·문자가 새로 노출된 컷은 없다.
- s19 생성 원본들은 네 홈 수나 압박 방향이 모호해 단독 사용하지 않았다. 정상적인 침대 컷 위에 코드 기반 네 압박 그림자를 합성하고 `shot-19-final.png`에서 네 줄의 분리와 주변 천 접촉을 확인했다. 이 승인 판정은 이미지 단독이 아니라 최종 합성 컷에만 적용한다.
- 쇼츠 첫·중간·마지막 프레임을 각각 1080×1920으로 확인했다. 첫 프레임 세 사람·빈자리, 중간 정상 손목, 마지막 도어락 네 점과 하단 완결 문장이 모두 안전 영역에 들어온다. 재렌더는 BGM 소스만 교체했으며 최종 영상에도 동일한 크롭을 적용했다.
- 두 썸네일은 1280×720 원본으로 확인했고 네 벌 수저와 화면 속 네 손가락, 5음절 제목의 모바일 가독성을 확인했다.
