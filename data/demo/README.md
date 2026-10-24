# data/demo

Демо-пакеты Argus (tech.md 8.19): `data/demo/<name>/` с `manifest.json`, `videos/` и `artifacts/`. Содержимое папки, кроме этого файла, в git не попадает.

Сборка на LinQ (туннель поднят, `INFERENCE_BACKEND=linq`, без фейка):

```
uv run safewatch demo build config/demo.example.yaml --videos data/videos --out data/demo/argus
```

Без LinQ: `SAFEWATCH_FAKE=1` и `--allow-fake`, пакет подписан как фейк (`DemoPack.fake`).

Импорт: `uv run safewatch demo import data/demo/argus` или `uv run safewatch serve --seed` при `demo.autoload: true` (пакет из `demo.pack`). Повторный импорт пакета с тем же `name` ничего не меняет.
