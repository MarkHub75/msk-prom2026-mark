import sys, io, numpy as np, cv2, PIL, yaml
from PIL import Image
out = sys.argv[1]
print("versions cv2", cv2.__version__, "PIL", PIL.__version__, "numpy", np.__version__, "yaml", yaml.__version__)
# 1) EXIF orientation=6 JPEG, stored size w=200,h=100
arr = np.zeros((100, 200, 3), np.uint8); arr[:, :100] = (255, 0, 0)  # left half red (RGB)
im = Image.fromarray(arr)
ex = Image.Exif(); ex[274] = 6
p = out + "/exif6.jpg"; im.save(p, exif=ex)
with Image.open(p) as i:
    print("PIL stored size (w,h):", i.size, "exif orientation:", i.getexif().get(274))
    s = i.size
    if i.getexif().get(274) in {5, 6, 7, 8}: s = s[::-1]
    print("exif_size-style (w,h) after swap logic:", s)
b = np.fromfile(p, np.uint8)
print("cv2.imdecode default (h,w,c):", cv2.imdecode(b, cv2.IMREAD_COLOR).shape)
print("cv2.imdecode IGNORE_ORIENTATION (h,w,c):", cv2.imdecode(b, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION).shape)
print("cv2.imread default (h,w,c):", cv2.imread(p).shape)
# 2) PNG with alpha, grayscale
rgba = np.zeros((50, 60, 4), np.uint8); rgba[..., 3] = 128
Image.fromarray(rgba, "RGBA").save(out + "/alpha.png")
print("PNG RGBA via imdecode COLOR shape:", cv2.imdecode(np.fromfile(out + "/alpha.png", np.uint8), cv2.IMREAD_COLOR).shape)
Image.fromarray(np.zeros((50, 60), np.uint8), "L").save(out + "/gray.jpg")
print("gray JPG via imdecode COLOR shape:", cv2.imdecode(np.fromfile(out + "/gray.jpg", np.uint8), cv2.IMREAD_COLOR).shape)
# 3) YAML 1.1 scalars as class names
for txt in ["names: [person, no, yes, on, off, y, n, null, 1, 1.0, '007', NO_helmet]",
            "names:\n  0: helmet\n  1: no\n  2: yes"]:
    d = yaml.safe_load(txt); n = d["names"]
    n = dict(enumerate(n)) if isinstance(n, list) else n
    print("YAML raw ->", d["names"], "| check_class_names-style str():", {int(k): str(v) for k, v in n.items()})
