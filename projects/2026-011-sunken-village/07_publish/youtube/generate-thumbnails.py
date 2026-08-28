#!/usr/bin/env python3
"""Overlay Korean thumbnail headlines onto 1280x720 backgrounds."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WIDTH = 1280
HEIGHT = 720
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

VARIANTS = [
    {
        "source": "thumbnail-a-background.png",
        "output": "thumbnail-a.png",
        "side": "left",
        "size": 80,
        "lines": [("철거된 종탑", "#ffffff"), ("종이 울렸다", "#ff4d5f")],
    },
    {
        "source": "thumbnail-b-background.png",
        "output": "thumbnail-b.png",
        "side": "right",
        "size": 76,
        "lines": [("42가구 이주", "#ffffff"), ("마을은 그대로", "#ff4d5f")],
    },
]


def load_font(size):
    for index in (7, 6, 0):
        try:
            return ImageFont.truetype(FONT_PATH, size, index=index)
        except OSError:
            continue
    raise FileNotFoundError(FONT_PATH)


def cover(path):
    image = Image.open(path).convert("RGB")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    resized = image.resize(
        (int(image.width * scale), int(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - WIDTH) // 2
    top = (resized.height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def render(variant):
    canvas = cover(HERE / variant["source"])
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    is_left = variant["side"] == "left"
    panel_x = 28 if is_left else 690
    for index in range(562):
        t = index / 561
        alpha = int(210 * (1 - 0.62 * t)) if is_left else int(210 * (0.28 + 0.62 * t))
        draw.line(
            [(panel_x + index, 145), (panel_x + index, 470)],
            fill=(0, 0, 0, alpha),
        )
    accent_x = 52 if is_left else 1198
    draw.rectangle([accent_x, 176, accent_x + 9, 414], fill=(227, 27, 54, 255))
    font = load_font(variant["size"])
    x = 82 if is_left else 1170
    for (text, color), y in zip(variant["lines"], (250, 370)):
        box = draw.textbbox((0, 0), text, font=font)
        text_w = box[2] - box[0]
        text_h = box[3] - box[1]
        tx = x if is_left else x - text_w
        ty = y - text_h // 2
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                if dx * dx + dy * dy <= 36:
                    draw.text((tx + dx, ty + dy), text, font=font, fill=(0, 0, 0, 250))
        draw.text((tx, ty), text, font=font, fill=color)
    out = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    out.save(HERE / variant["output"], "PNG")
    print(f"Created {variant['output']}")


if __name__ == "__main__":
    for variant in VARIANTS:
        render(variant)
