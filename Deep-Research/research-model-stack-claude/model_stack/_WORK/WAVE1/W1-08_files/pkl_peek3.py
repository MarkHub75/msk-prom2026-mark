import sys, zipfile, pickletools, io, re
z = zipfile.ZipFile(sys.argv[1])
data = z.read([n for n in z.namelist() if n.endswith("data.pkl")][0])
out = io.StringIO(); pickletools.dis(data, out)
txt = out.getvalue()
strs = [m.group(2).strip().strip("'") for m in (re.search(r"(SHORT_BINUNICODE|BINUNICODE)\s+(.*)$", l) for l in txt.splitlines()) if m]
print("n strings:", len(strs))
print("top-level keys region (first 14):", strs[:14])
for key in ("names", "train_args", "nc", "task", "ema", "optimizer", "stride", "yaml"):
    print(key, "idx:", [i for i, s in enumerate(strs) if s == key][:6])
i = strs.index("names"); print("after first 'names':", strs[i:i+90])
print("globals:", sorted(set(re.findall(r"GLOBAL\s+'([^']+)'", txt)))[:25])
