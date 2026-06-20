#!/usr/bin/env python3
"""Create YouTube thumbnail options for the WWDC 2026 video."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT_DIR = Path(__file__).resolve().parent
W, H = 1280, 720

INK = (15, 28, 55)
MUTED = (89, 107, 132)
BLUE = (59, 130, 246)
MINT = (45, 212, 191)
GREEN = (34, 197, 94)
YELLOW = (245, 183, 0)
RED = (239, 68, 68)
WHITE = (255, 255, 255)

FONT_KR = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_EN = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size: int, *, english: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_EN if english else FONT_KR, size=size)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient_bg() -> Image.Image:
    img = Image.new("RGB", (W, H), (246, 251, 255))
    px = img.load()
    for y in range(H):
        for x in range(W):
            nx = x / W
            ny = y / H
            r = int(255 - 13 * ny - 7 * nx)
            g = int(255 - 22 * ny + 8 * nx)
            b = int(255 - 42 * ny + 16 * nx)
            px[x, y] = (max(235, r), max(238, g), min(255, b))
    return img


def glow_layer(circles: list[tuple[int, int, int, tuple[int, int, int, int]]]) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for cx, cy, radius, color in circles:
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
    return layer.filter(ImageFilter.GaussianBlur(48))


def add_common(img: Image.Image, label: str) -> ImageDraw.ImageDraw:
    img.alpha_composite(glow_layer([
        (1050, 95, 260, (*BLUE, 58)),
        (105, 610, 300, (*MINT, 64)),
        (760, 655, 190, (*YELLOW, 34)),
    ]))
    draw = ImageDraw.Draw(img)
    for offset in range(-500, 1320, 190):
        draw.line((offset, -40, offset + 520, 760), fill=(80, 180, 210, 24), width=10)
    rounded(draw, (42, 38, 1238, 682), 42, (255, 255, 255, 142), (20, 33, 61, 36), 2)
    for i, color in enumerate([BLUE, MINT, YELLOW, GREEN]):
        draw.ellipse((74 + i * 20, 70, 84 + i * 20, 80), fill=color)
    draw.text((168, 60), "WWDC 2026", fill=INK, font=font(30, english=True))
    draw.text((1035, 62), label, fill=MUTED, font=font(23, english=True), anchor="ra")
    return draw


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill, fnt, spacing: int = 0) -> None:
    draw.multiline_text(xy, text, fill=fill, font=fnt, anchor="mm", align="center", spacing=spacing)


def draw_option_a() -> None:
    img = gradient_bg().convert("RGBA")
    draw = add_common(img, "KEYNOTE PREVIEW")

    rounded(draw, (118, 146, 780, 604), 36, (255, 255, 255, 185), (20, 33, 61, 35), 2)
    draw.text((164, 196), "APPLE AI", fill=MINT, font=font(34, english=True))
    draw.multiline_text((160, 248), "이번엔\n진짜 쓸만할까?", fill=INK, font=font(78), spacing=2)
    rounded(draw, (162, 515, 650, 585), 24, INK)
    text_center(draw, (406, 551), "예쁜 데모 말고, 실제 사용?", WHITE, font(34), 0)

    rounded(draw, (840, 170, 1145, 485), 42, (255, 255, 255, 210), (59, 130, 246, 62), 3)
    draw.ellipse((930, 220, 1055, 345), fill=(45, 212, 191, 45), outline=(45, 212, 191, 120), width=5)
    draw.arc((902, 192, 1083, 373), 28, 332, fill=BLUE, width=12)
    text_center(draw, (994, 407), "Siri\nApple Intelligence", INK, font(35, english=True), 8)
    rounded(draw, (855, 510, 1130, 582), 22, (255, 255, 255, 220), (245, 183, 0, 95), 3)
    text_center(draw, (992, 546), "6월 8일 공개", INK, font(34), 0)

    img.convert("RGB").save(OUT_DIR / "wwdc-2026-thumbnail-a.png", quality=95)


def draw_option_b() -> None:
    img = gradient_bg().convert("RGBA")
    draw = add_common(img, "PROOF OR DELAY")

    rounded(draw, (104, 136, 1176, 604), 42, (255, 255, 255, 170), (20, 33, 61, 34), 2)
    draw.text((160, 190), "SIRI TEST", fill=MINT, font=font(34, english=True))
    draw.multiline_text((154, 246), "Siri,\n드디어 바뀌나?", fill=INK, font=font(83), spacing=-6)
    draw.text((164, 498), "WWDC 2026에서 봐야 할 진짜 질문", fill=MUTED, font=font(36))

    rounded(draw, (792, 208, 1088, 336), 28, (236, 253, 245, 230), (34, 197, 94, 105), 4)
    text_center(draw, (940, 272), "PROOF", INK, font(50, english=True), 0)
    rounded(draw, (792, 374, 1088, 502), 28, (255, 246, 246, 230), (239, 68, 68, 82), 4)
    text_center(draw, (940, 438), "DELAY", INK, font(50, english=True), 0)

    draw.line((737, 210, 737, 502), fill=(20, 33, 61, 42), width=4)
    draw.polygon([(704, 342), (770, 342), (737, 388)], fill=YELLOW)
    rounded(draw, (156, 586, 592, 646), 22, INK)
    text_center(draw, (374, 616), "6월 8일 키노트", WHITE, font(32), 0)

    img.convert("RGB").save(OUT_DIR / "wwdc-2026-thumbnail-b.png", quality=95)


def main() -> None:
    draw_option_a()
    draw_option_b()
    print(OUT_DIR / "wwdc-2026-thumbnail-a.png")
    print(OUT_DIR / "wwdc-2026-thumbnail-b.png")


if __name__ == "__main__":
    main()
