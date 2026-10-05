from align_captions import character_coverage


def test_spoken_coverage_treats_digits_as_korean_spoken_forms():
    script = "백사 동 천사백일 호에서 세 시 십칠 분에 만났습니다."
    raw_words = [
        {"text": "104동"},
        {"text": "1401호에서"},
        {"text": "3시"},
        {"text": "17분에"},
        {"text": "만났습니다."},
    ]

    assert character_coverage(script, raw_words) == 1.0


def test_v4_performance_tags_are_excluded_from_spoken_alignment():
    assert character_coverage(
        "[quiet, measured narration] 문이 열렸어요. [whispering] 뒤에 있었죠.",
        [{"text": "문이 열렸어요."}, {"text": "뒤에 있었죠."}],
    ) == 1.0
