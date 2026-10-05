import pytest

from generate_elevenlabs_audio import build_audio_payload, split_text_chunks, validate_v4_spoken_source


def test_chunker_rebalances_a_tiny_final_prompt():
    text = " ".join(("가" * 100) + "." for _ in range(77))
    chunks = split_text_chunks(text, min_chars=1000, max_chars=1300)

    assert len(chunks) == 7
    assert all(1000 <= len(chunk) <= 1300 for chunk in chunks)
    assert " ".join(chunks) == text


def test_v4_strips_unsupported_settings_and_keeps_last_three_context_ids():
    payload = build_audio_payload(
        "문을 열었어요.",
        {"model_id": "eleven_v4", "voice_settings": {
            "stability": 0.5, "similarity_boost": 0.75,
            "style": 0.15, "speed": 1.1, "use_speaker_boost": True,
        }, "performance_direction": "quiet, measured narration"},
        request_history=["one", "two", "three", "four"],
        previous_text="이전 문장.", next_text="다음 문장.",
    )
    assert payload["voice_settings"] == {"stability": 0.5, "similarity_boost": 0.75}
    assert payload["text"] == "[quiet, measured narration] 문을 열었어요."
    assert payload["previous_request_ids"] == ["two", "three", "four"]
    assert "previous_text" not in payload
    assert payload["next_text"] == "다음 문장."


def test_v3_explicit_settings_remain_compatible_and_stitching_is_not_added():
    settings = {"stability": 0.5, "style": 0.15, "use_speaker_boost": True}
    payload = build_audio_payload("승인한 문장.", {"model_id": "eleven_v3", "voice_settings": settings},
                                  request_history=["old-id"], next_text="다음 문장.")
    assert payload["voice_settings"] == settings
    assert "previous_request_ids" not in payload
    assert "next_text" not in payload


def test_v4_spoken_source_allows_tags_and_number_normalization_but_rejects_rewrites():
    validate_v4_spoken_source("3시 17분이었어요.", "[quietly] 세 시 십칠 분이었어요.")
    with pytest.raises(ValueError, match="changed approved words"):
        validate_v4_spoken_source("문을 열었어요.", "[quietly] 문을 닫았어요.")


def test_v4_rejects_ssml_before_api_request():
    with pytest.raises(ValueError, match="does not support SSML"):
        build_audio_payload('문 앞에서 <break time="1s"/> 멈췄어요.', {"model_id": "eleven_v4"})
