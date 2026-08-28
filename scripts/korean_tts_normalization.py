#!/usr/bin/env python3
"""Convert digits in Korean narration into deterministic spoken forms."""

from __future__ import annotations

import re


SINO_DIGITS = ["영", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
SMALL_UNITS = [(1000, "천"), (100, "백"), (10, "십")]
NATIVE_ONES = {
    1: "한",
    2: "두",
    3: "세",
    4: "네",
    5: "다섯",
    6: "여섯",
    7: "일곱",
    8: "여덟",
    9: "아홉",
    10: "열",
    11: "열한",
    12: "열두",
    13: "열세",
    14: "열네",
    15: "열다섯",
    16: "열여섯",
    17: "열일곱",
    18: "열여덟",
    19: "열아홉",
    20: "스무",
}


def sino_number(value: int) -> str:
    """Read a non-negative integer with Korean Sino-number words."""
    if value == 0:
        return SINO_DIGITS[0]
    if value < 0:
        return "마이너스 " + sino_number(abs(value))
    if value >= 10_000:
        high, low = divmod(value, 10_000)
        result = sino_number(high) + "만"
        return result + (sino_number(low) if low else "")

    remainder = value
    parts: list[str] = []
    for unit, label in SMALL_UNITS:
        digit, remainder = divmod(remainder, unit)
        if digit:
            if digit > 1:
                parts.append(SINO_DIGITS[digit])
            parts.append(label)
    if remainder:
        parts.append(SINO_DIGITS[remainder])
    return "".join(parts)


def native_number(value: int) -> str:
    """Read common Korean counters naturally for values used in narration."""
    if value in NATIVE_ONES:
        return NATIVE_ONES[value]
    if 21 <= value < 100:
        tens, ones = divmod(value, 10)
        tens_word = {2: "스물", 3: "서른", 4: "마흔", 5: "쉰", 6: "예순", 7: "일흔", 8: "여든", 9: "아흔"}[tens]
        return tens_word + (NATIVE_ONES[ones] if ones else "")
    return sino_number(value)


def _replace_counter(text: str, counter: str, reader) -> str:
    pattern = re.compile(rf"(?<!\d)(\d+)\s*{re.escape(counter)}")
    return pattern.sub(lambda match: f"{reader(int(match.group(1)))} {counter}", text)


def normalize_korean_tts_text(text: str) -> str:
    """Expand every digit sequence while preserving the authored display script separately."""
    normalized = text

    # Clock notation is ambiguous without context, so resolve it before generic counters.
    normalized = re.sub(
        r"(?<!\d)(\d{1,2}):(\d{2})(?!\d)",
        lambda match: f"{native_number(int(match.group(1)))} 시 {sino_number(int(match.group(2)))} 분",
        normalized,
    )

    # Apartment identifiers need cardinal readings, not digit-by-digit readings.
    normalized = re.sub(
        r"(?<!\d)(\d{3,4})\s*호",
        lambda match: f"{sino_number(int(match.group(1)))} 호",
        normalized,
    )
    normalized = re.sub(
        r"(?<!\d)(\d{2,3})\s*동",
        lambda match: f"{sino_number(int(match.group(1)))} 동",
        normalized,
    )
    # Four-digit apartment numbers also appear without 호 in call panels and status messages.
    normalized = re.sub(
        r"(?<!\d)(1[0-5]\d{2})(?=\s*(?:[.,]|세대|였|입|재배정|$))",
        lambda match: f"{sino_number(int(match.group(1)))} 호",
        normalized,
    )

    # Calendar and clock expressions use Sino numbers except for Korean hour counters.
    normalized = _replace_counter(normalized, "년", sino_number)
    normalized = re.sub(
        r"(?<!\d)(\d+)\s*월",
        lambda match: f"{'시월' if int(match.group(1)) == 10 else sino_number(int(match.group(1))) + ' 월'}",
        normalized,
    )
    normalized = _replace_counter(normalized, "일", sino_number)
    normalized = _replace_counter(normalized, "시", native_number)
    normalized = _replace_counter(normalized, "분", sino_number)
    normalized = _replace_counter(normalized, "초", sino_number)

    # Device labels are read more naturally with an explicit ordinal-like counter.
    normalized = re.sub(
        r"카메라\s*(\d+)",
        lambda match: f"카메라 {sino_number(int(match.group(1)))} 번",
        normalized,
    )

    # Building floors use Sino numbers; object counters use native Korean forms.
    normalized = _replace_counter(normalized, "층", sino_number)
    for counter in ("세대", "번", "통", "배", "장", "줄"):
        normalized = _replace_counter(normalized, counter, native_number)

    # Any remaining digits are labels or counts without an explicit counter.
    normalized = re.sub(r"\d+", lambda match: sino_number(int(match.group(0))), normalized)
    return normalized
