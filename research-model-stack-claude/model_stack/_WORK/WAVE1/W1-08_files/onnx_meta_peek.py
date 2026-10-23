import sys, re
# READ-ONLY byte scan of a (neighbour-produced) ONNX file: print the ModelProto.metadata_props key/value pairs without importing onnx.
# metadata_props is field 14 (length-delimited) of ModelProto; each entry = StringStringEntryProto{1:key,2:value}.
b = open(sys.argv[1], "rb").read()
def varint(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1; r |= (c & 0x7F) << s; s += 7
        if not c & 0x80: return r, i
i = 0; n = len(b); out = {}
while i < n:
    tag, i = varint(b, i); f, wt = tag >> 3, tag & 7
    if wt == 0: _, i = varint(b, i)
    elif wt == 1: i += 8
    elif wt == 5: i += 4
    elif wt == 2:
        L, i = varint(b, i)
        if f == 14:
            e = b[i:i+L]; j = 0; kv = {}
            while j < len(e):
                t, j = varint(e, j); ff = t >> 3
                l2, j = varint(e, j); kv[ff] = e[j:j+l2].decode("utf8", "replace"); j += l2
            out[kv.get(1)] = kv.get(2)
        i += L
    else: raise SystemExit(f"unexpected wire type {wt}")
for k, v in out.items(): print(f"{k}: {v[:230]}{'...' if len(v) > 230 else ''}")
