"""Synthetic evidence placeholders: yellow.jpg and red.jpg (1280x720, 16:9).

Each frame says in large letters that it is synthetic and draws the box exactly by the bbox
of evidence.json (normalized 0..1). Run: py -3.12 evidence/make_placeholders.py
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1280, 720
COLORS = {"yellow": (255, 196, 0), "red": (255, 59, 48)}
CAPTIONS = {
    "yellow": "Жёлтая опасность · Сектор 1 · Бег 2,4 роста/с",
    "red": "Красная опасность · Сектор 1 · Зафиксировано падение",
}
FONTS = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans-Bold.ttf"]


def font(size: int) -> ImageFont.FreeTypeFont:
    for name in FONTS:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    sys.exit("нет шрифта с кириллицей: укажите путь в FONTS")


def make(key: str, item: dict) -> None:
    img = Image.new("RGB", (W, H), (28, 34, 44))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 80):  # floor grid, only to show it is a drawing
        d.line([(x, 0), (x, H)], fill=(40, 48, 60))
    for y in range(0, H, 80):
        d.line([(0, y), (W, y)], fill=(40, 48, 60))
    d.text((W // 2, 150), "СИНТЕТИЧЕСКИЙ КАДР", font=font(78), fill=(230, 237, 243), anchor="mm")
    d.text((W // 2, 235), "не результат нейросети", font=font(48), fill=(230, 237, 243), anchor="mm")
    d.text((W // 2, H - 40), CAPTIONS[key], font=font(30), fill=COLORS[key], anchor="mm")
    for obj in item["objects"]:
        x1, y1, x2, y2 = obj["bbox"]
        box = [round(x1 * W), round(y1 * H), round(x2 * W), round(y2 * H)]
        d.rectangle(box, outline=COLORS[key], width=6)
        d.text((box[0], box[1] - 8), "ручная разметка", font=font(26), fill=COLORS[key], anchor="ld")
    img.save(HERE / item["file"], "JPEG", quality=88)
    print(f"{item['file']}: bbox {obj['bbox']}")


def main() -> None:
    conf = json.loads((HERE / "evidence.json").read_text(encoding="utf-8"))
    for key in ("yellow", "red"):
        make(key, conf[key])


if __name__ == "__main__":
    main()
