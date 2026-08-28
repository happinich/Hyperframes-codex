#!/usr/bin/env python3
"""Render exact Korean thumbnail copy over generated horror backgrounds."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT = 1280, 720
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

VARIANTS = [
    {
        "source": "thumbnail-a-background.png",
        "output": "thumbnail-a.png",
        "side": "left",
        "size": 78,
        "lines": [("14층은 없다", "#ffffff"), ("그런데 내가 있다", "#ff4055")],
    },
    {
        "source": "thumbnail-b-background.png",
        "output": "thumbnail-b.png",
        "side": "right",
        "size": 80,
        "lines": [("03:17 경고", "#ffffff"), ("문을 열지 마", "#ff4055")],
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
    if is_left:
        draw.rectangle([24, 150, 660, 505], fill=(0, 0, 0, 188))
        accent_x = 52
    else:
        draw.rectangle([640, 150, 1256, 505], fill=(0, 0, 0, 188))
        accent_x = 1204
    draw.rectangle([accent_x, 180, accent_x + 10, 443], fill=(255, 64, 85, 255))

    font = load_font(variant["size"])
    for (text, color), y in zip(variant["lines"], (260, 390)):
        box = draw.textbbox((0, 0), text, font=font)
        text_w = box[2] - box[0]
        text_h = box[3] - box[1]
        x = 86 if is_left else 1168 - text_w
        top = y - text_h // 2
        draw.text((x, top), text, font=font, fill=color, stroke_width=7, stroke_fill="#000000")

    output = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    output.save(HERE / variant["output"], "PNG")
    print(f"Created {variant['output']}")


if __name__ == "__main__":
    for variant in VARIANTS:
        render(variant)
