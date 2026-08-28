# 썸네일 생성 프롬프트

한글 문구는 Imagine에 넣지 않는다. 배경만 생성한 뒤 `generate-thumbnails.py`로 1280x720 헤드라인을 올린다.

## A안: 철거된 종탑 (1순위)

- 문구: `철거된 종탑` / `종이 울렸다`
- 구도: 왼쪽 문구, 오른쪽 빈 종탑 기단
- 핵심 오브젝트: 물이 빠진 저수지, 진흙 위 기와집, 종이 없는 종탑, 외등 하나
- 색상: 딥 네이비, 진흙 브라운, 보랏빛 저녁, 앰버 등불

```text
Cinematic Korean horror YouTube thumbnail background. A drought-drained reservoir at dusk has revealed a preserved rural Korean village sitting in dark wet mud. On the right, a demolished church bell-tower foundation stands empty—wet concrete, no bell, one distant hanging paper lantern glowing dull amber. Keep the entire left third very dark, simple, and uncluttered so large headline text can sit there later. Photorealistic, high contrast, deep navy water, mud-brown roofs, cold fog, restrained amber light. No text, letters, numbers, logo, watermark, gore, people, or visible faces.
```

## B안: 붉은 수첩과 등불 (A/B 테스트)

- 문구: `42가구 이주` / `마을은 그대로`
- 구도: 왼쪽 수첩·대장, 오른쪽 문구
- 핵심 오브젝트: 붉은 표지 수첩, 글자 없는 젖은 서류, 인주, 물에 잠긴 마당의 등불
- 색상: 차콜 블랙, 탁한 앰버, 인주 빨강

```text
Photorealistic Korean supernatural-thriller YouTube thumbnail background. Night close-up of a wet wooden table: a closed red cloth-bound notebook with a thread tie, a mud-stained ledger, and one wet red ink stamp pad. Behind the table, many small amber paper lanterns glow across a flooded village courtyard in the mist. Keep the entire right third very dark, simple, and uncluttered so large headline text can sit there later. High contrast, charcoal black, dull amber, a thin wet sheen. No readable writing, letters, numbers, logo, watermark, gore, people, or visible faces.
```

## 재생성

```bash
python3 generate-thumbnails.py
```
