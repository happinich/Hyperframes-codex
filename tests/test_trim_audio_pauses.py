from scripts.trim_audio_pauses import retained_intervals


def test_retained_intervals_keeps_requested_pause_around_each_cut():
    intervals, removed = retained_intervals(
        duration=10.0,
        silences=[(1.0, 2.0), (5.0, 6.2)],
        keep_pause=0.4,
    )

    assert intervals == [(0.0, 1.2), (1.8, 5.2), (6.0, 10.0)]
    assert round(removed, 3) == 1.4


def test_retained_intervals_does_not_cut_pause_shorter_than_keep_value():
    intervals, removed = retained_intervals(
        duration=4.0,
        silences=[(1.0, 1.3)],
        keep_pause=0.45,
    )

    assert intervals == [(0.0, 4.0)]
    assert removed == 0.0
