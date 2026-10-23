import sys
from pathlib import Path
import numpy as np
from PIL import Image

root = Path(sys.argv[1])
rng = np.random.default_rng(0)


def img(p, w=320, h=240, mode="RGB", exif=None):
    p.parent.mkdir(parents=True, exist_ok=True)
    a = rng.integers(0, 255, (h, w, 3), dtype=np.uint8)
    im = Image.fromarray(a)
    if mode == "RGBA":
        im = im.convert("RGBA")
    if exif:
        e = Image.Exif()
        e[274] = exif
        im.save(p, exif=e)
    else:
        im.save(p)


def lab(split, stem, rows):
    p = root / "labels" / split / f"{stem}.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(rows) + ("\n" if rows else ""))


# ok images
for i in range(4):
    img(root / "images" / "train" / f"ok{i}.jpg")
    lab("train", f"ok{i}", [f"{i % 2} 0.5 0.5 0.2 0.3", f"{(i + 1) % 2} 0.3 0.3 0.1 0.1"])
img(root / "images" / "train" / "cls_eq_nc.jpg"); lab("train", "cls_eq_nc", ["3 0.5 0.5 0.2 0.2"])        # class == nc (nc=3 -> ids 0..2)
img(root / "images" / "train" / "six_cols.jpg"); lab("train", "six_cols", ["0 0.5 0.5 0.2 0.2 0.9"])      # 6 columns (e.g. confidence appended)
img(root / "images" / "train" / "abs_px.jpg"); lab("train", "abs_px", ["1 160 120 64 48"])                # absolute pixels
img(root / "images" / "train" / "tiny.jpg"); lab("train", "tiny", ["2 0.5 0.5 0.004 0.004"])              # ~1px box at 640
img(root / "images" / "train" / "duprows.jpg"); lab("train", "duprows", ["0 0.5 0.5 0.2 0.2", "0 0.5 0.5 0.2 0.2"])
img(root / "images" / "train" / "exif6.jpg", w=320, h=240, exif=6); lab("train", "exif6", ["0 0.5 0.5 0.2 0.2"])
img(root / "images" / "train" / "alpha.png", mode="RGBA"); lab("train", "alpha", ["1 0.5 0.5 0.2 0.2"])
img(root / "images" / "train" / "nolabel.jpg")                                                            # no label file -> background
# image outside an images/ dir -> label path cannot be derived
img(root / "pics" / "train" / "stray.jpg")
# val: includes a byte-identical copy of a train image (leakage)
img(root / "images" / "val" / "v0.jpg"); lab("val", "v0", ["0 0.5 0.5 0.2 0.2"])
(root / "images" / "val" / "leak.jpg").write_bytes((root / "images" / "train" / "ok0.jpg").read_bytes()); lab("val", "leak", ["0 0.5 0.5 0.2 0.3"])
# data.yaml with YAML 1.1 trap: class named `no`
(root / "data.yaml").write_text("path: " + str(root.resolve()).replace("\\", "/") + "\ntrain: [images/train, train_list.txt]\nval: images/val\nnames:\n  0: helmet\n  1: no\n  2: vest\n", encoding="utf-8")
# a second yaml with different class order, for --compare
(root / "other.yaml").write_text("train: images/train\nval: images/val\nnames:\n  0: vest\n  1: helmet\n  2: 'no'\n", encoding="utf-8")
# stray pics: also place under 'pics/' only (no 'images' in path) via train.txt list
(root / "train_list.txt").write_text(str((root / "pics" / "train" / "stray.jpg").resolve()) + "\n")
print("synthetic dataset written to", root)
