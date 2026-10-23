# OmniFall Configuration Reference

All configurations are loaded via:

```python
from datasets import load_dataset
ds = load_dataset("simplexsigil2/omnifall", "<config_name>")
```

## Labels (no train/val/test splits)

| Config | Description |
|---|---|
| `labels` (default) | All staged + OOPS labels (52,618 segments, 7 columns) |
| `labels-syn` | OF-Syn labels with demographic metadata (19,228 segments, 19 columns) |
| `metadata-syn` | OF-Syn video-level metadata (12,000 videos) |
| `framewise-syn` | OF-Syn frame-wise labels (81 labels per video) |

`labels` and `labels-syn` are per-segment tables with `start`/`end` in seconds.
`metadata-syn` describes whole videos and `framewise-syn` holds per-frame label
arrays, so neither has segment bounds and neither can be given a video clip;
`omnifall.load(..., video=True)` rejects them for that reason. All other configs
are per-segment tables.

## Same-Domain Configs

### OF-Staged

| Config | Description |
|---|---|
| `of-sta-cs` | 8 staged datasets, cross-subject splits |
| `of-sta-cv` | 8 staged datasets, cross-view splits |

### OF-ItW

| Config | Description |
|---|---|
| `of-itw` | OOPS-Fall in-the-wild genuine accidents |

Video loading requires the `omnifall` companion package (`pip install omnifall`).

### OF-Syn

| Config | Description |
|---|---|
| `of-syn` | Random 80/10/10 split |
| `of-syn-cross-age` | Cross-age split (train: adults, test: children/elderly) |
| `of-syn-cross-ethnicity` | Cross-ethnicity split |
| `of-syn-cross-bmi` | Cross-BMI split (train: normal/underweight, test: obese) |

Video loading requires the `omnifall` companion package.

## Cross-Domain Evaluation (to-all)

Train/val from a specific source, test on **all** datasets (staged test + ItW test + Syn random test). The `-cs`/`-cv` suffix controls how the staged portion of the test set is split.

### Combined source configs

| Config | Train/val source | Test |
|---|---|---|
| `of-sta-to-all-cs` | All 8 staged (CS) | All datasets (staged CS + ItW + Syn) |
| `of-sta-to-all-cv` | All 8 staged (CV) | All datasets (staged CV + ItW + Syn) |
| `of-syn-to-all-cs` | OF-Syn random | All datasets (staged CS + ItW + Syn) |
| `of-syn-to-all-cv` | OF-Syn random | All datasets (staged CV + ItW + Syn) |
| `of-sta-syn-to-all-cs` | Staged CS + OF-Syn | All datasets (staged CS + ItW + Syn) |
| `of-sta-syn-to-all-cv` | Staged CV + OF-Syn | All datasets (staged CV + ItW + Syn) |

### Individual staged dataset configs

| Config pattern | Train/val source |
|---|---|
| `{dataset}-to-all-cs` | Individual staged dataset (CS split) |
| `{dataset}-to-all-cv` | Individual staged dataset (CV split) |

Available for: `caucafall`, `cmdfall`, `edf`, `gmdcsa24`, `le2i`, `mcfd`, `occu`, `up_fall`.

Note: `mcfd-to-all-cs` has train only (1 subject, CS val is empty). `caucafall-to-all-cv` has train only (1 room, CV val is empty).

## Aggregate Configs (staged + OOPS combined)

| Config | Description |
|---|---|
| `cs` | Cross-subject splits for all staged + OOPS |
| `cv` | Cross-view splits for all staged + OOPS |

## Individual Dataset Configs

Each staged dataset with both cross-subject (`-cs`) and cross-view (`-cv`) splits:

| CS | CV |
|---|---|
| `caucafall-cs` | `caucafall-cv` |
| `cmdfall-cs` | `cmdfall-cv` |
| `edf-cs` | `edf-cv` |
| `gmdcsa24-cs` | `gmdcsa24-cv` |
| `le2i-cs` | `le2i-cv` |
| `mcfd-cs` | `mcfd-cv` |
| `occu-cs` | `occu-cv` |
| `up_fall-cs` | `up_fall-cv` |

Note: `mcfd-cs` has train only (1 subject). `caucafall-cv` has train only (1 room).

## Deprecated Config Names

The following old config names still work but may be removed in a future version:

| Old Name | Use Instead |
|---|---|
| `cs-staged` | `of-sta-cs` |
| `cv-staged` | `of-sta-cv` |
| `cs-staged-wild` | `of-sta-to-all-cs` |
| `cv-staged-wild` | `of-sta-to-all-cv` |
| `of-sta-to-itw-cs` | `of-sta-to-all-cs` |
| `of-sta-to-itw-cv` | `of-sta-to-all-cv` |
| `of-sta-itw-cs` | `of-sta-to-all-cs` |
| `of-sta-itw-cv` | `of-sta-to-all-cv` |
| `of-syn-to-itw` | `of-syn-to-all-cs` |
| `of-syn-itw` | `of-syn-to-all-cs` |
| `of-sta-syn-to-itw-cs` | `of-sta-syn-to-all-cs` |
| `of-sta-syn-to-itw-cv` | `of-sta-syn-to-all-cv` |
| `OOPS` | `of-itw` |
| `caucafall` | `caucafall-cs` |
| `cmdfall` | `cmdfall-cs` |
| `edf` | `edf-cs` |
| `gmdcsa24` | `gmdcsa24-cs` |
| `le2i` | `le2i-cs` |
| `mcfd` | `mcfd-cs` |
| `occu` | `occu-cs` |
| `up_fall` | `up_fall-cs` |
