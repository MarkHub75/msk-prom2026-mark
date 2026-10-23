# Known Pitfalls

In this file we document known problems and pitfalls. 

---

## 1. In the multi-view components, some segments end after the video does

**What you will see.** In `edf`, `cmdfall` and `mcfd`, a segment whose `end` lies
past the last frame of its video. Depending on your decoder you get fewer frames
than you asked for, or an error.

| Component | Segments affected | Videos affected | Largest overrun |
|---|---|---|---|
| mcfd | 85 / 1,352 | 71 / 192 | 1.19 s (`chute05/cam8`) |
| edf | 18 / 508 | 5 / 10 | 7.36 s (`jinhui/view2/rgb/...`) |
| cmdfall | 76 / 42,143 | 75 / 384 | 3.80 s (`colors/S22P36K6`) |

**Why.** These components are multi-camera, and one view was annotated, afterwards the labels were propagated to other views. 
To make sure the labels are still correct, each dataset carries per-camera synchronisation offsets; a
secondary view's segments are the reference view's segments shifted by that
offset. Where the offset is positive, or the secondary camera stopped recording
earlier than the reference, the shifted tail segment lands beyond the end of the video file.

---

## 2. Some config names are kept aliases

Config names have been revised, and the earlier spellings were kept working
rather than removed, so that code written against them does not break. Both
names load the same data.

| Old name | Current name |
|---|---|
| `cs-staged`, `cv-staged` | `of-sta-cs`, `of-sta-cv` |
| `cs-staged-wild`, `cv-staged-wild` | `of-sta-to-all-cs`, `of-sta-to-all-cv` |
| `of-sta-to-itw-*`, `of-sta-itw-*` | `of-sta-to-all-*` |
| `of-syn-to-itw`, `of-syn-itw` | `of-syn-to-all-cs` |
| `of-sta-syn-to-itw-*` | `of-sta-syn-to-all-*` |
| `OOPS` | `of-itw` |
| `caucafall`, `cmdfall`, `edf`, `gmdcsa24`, `le2i`, `mcfd`, `occu`, `up_fall` | the matching `-cs` config |

Two consequences worth knowing. A bare component name such as `le2i` is an alias
for `le2i-cs`, so it gives you the cross-subject split rather than "all of le2i"
--- if you want the cross-view split, ask for `le2i-cv` explicitly. And when you
report which configuration you trained on, prefer the current name, since the
aliases are the ones most likely to be retired later.

[CONFIGS.md](CONFIGS.md) carries the full list.
