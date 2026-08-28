from generate_elevenlabs_audio import split_text_chunks


def test_chunker_rebalances_a_tiny_final_prompt():
    text = " ".join(("가" * 100) + "." for _ in range(77))
    chunks = split_text_chunks(text, min_chars=1000, max_chars=1300)

    assert len(chunks) == 7
    assert all(1000 <= len(chunk) <= 1300 for chunk in chunks)
    assert " ".join(chunks) == text
