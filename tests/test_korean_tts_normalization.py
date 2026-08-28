from korean_tts_normalization import normalize_korean_tts_text, sino_number


def test_sino_number_for_apartment_units():
    assert sino_number(104) == "백사"
    assert sino_number(1401) == "천사백일"
    assert sino_number(1502) == "천오백이"
    assert sino_number(2006) == "이천육"


def test_normalizes_apartment_numbers_and_display_labels():
    source = "104동 1401호. 1402호. 1403호. 1404호. 발신 번호는 1402였습니다."
    assert normalize_korean_tts_text(source) == (
        "백사 동 천사백일 호. 천사백이 호. 천사백삼 호. 천사백사 호. "
        "발신 번호는 천사백이 호였습니다."
    )


def test_normalizes_korean_dates_times_and_counters():
    source = "2006년 10월 17일 03:17. 밤 11시 42분. 대피 완료 4세대. 7통. 15줄."
    assert normalize_korean_tts_text(source) == (
        "이천육 년 시월 십칠 일 세 시 십칠 분. 밤 열한 시 사십이 분. "
        "대피 완료 네 세대. 일곱 통. 열다섯 줄."
    )


def test_normalizes_every_digit_in_realistic_sentence():
    source = "1층부터 15층까지, 13층 다음은 14층이고 104동 1502호에서 3시 31분에 만났다."
    result = normalize_korean_tts_text(source)
    assert result == "일 층부터 십오 층까지, 십삼 층 다음은 십사 층이고 백사 동 천오백이 호에서 세 시 삼십일 분에 만났다."
    assert not any(char.isdigit() for char in result)


def test_normalizes_seconds_and_camera_labels_naturally():
    source = "카메라 2. 영상은 실제보다 1초 먼저 움직였다."
    assert normalize_korean_tts_text(source) == "카메라 이 번. 영상은 실제보다 일 초 먼저 움직였다."
