"""Derives compositions/v-finale.html (1080×1920) from the landscape finale: same slam, light and order."""
import pathlib

C = pathlib.Path(__file__).resolve().parents[2] / "composition" / "compositions"
s = (C / "finale.html").read_text(encoding="utf-8")
pairs = [
    ('data-composition-id="finale" data-width="1920" data-height="1080"', 'data-composition-id="v-finale" data-width="1080" data-height="1920"'),
    ('window.__timelines["finale"]', 'window.__timelines["v-finale"]'),
    # glow and light around the word, which sits right-aligned around y≈900
    ("#fin-glow { position: absolute; left: 560px; top: 90px; width: 1400px; height: 900px;",
     "#fin-glow { position: absolute; left: -200px; top: 440px; width: 1400px; height: 900px;"),
    ("#fin-glow-audio { position: absolute; left: 760px; top: 250px; width: 1100px; height: 580px;",
     "#fin-glow-audio { position: absolute; left: -10px; top: 610px; width: 1100px; height: 580px;"),
    ("#fin-burst { position: absolute; left: 610px; top: 240px; width: 1300px; height: 600px;",
     "#fin-burst { position: absolute; left: -110px; top: 600px; width: 1300px; height: 600px;"),
    ("#fin-row { position: absolute; left: 150px; right: 140px; top: 0; bottom: 0; display: flex; align-items: center; }",
     "#fin-row { position: absolute; left: 96px; right: 90px; top: 740px; }"),
    ("#fin-inner { width: 100%; display: flex; justify-content: space-between; align-items: baseline; }",
     "#fin-inner { width: 100%; display: flex; flex-direction: column-reverse; align-items: stretch; gap: 64px; }"),
    ("#fin-sub { font-weight: 600; font-size: 38px; letter-spacing: .34em;", "#fin-sub { align-self: flex-start; font-weight: 600; font-size: 40px; letter-spacing: .34em;"),
    ("font-weight: 900; font-size: 360px; line-height: 1;", "align-self: flex-end; font-weight: 900; font-size: 280px; line-height: 1;"),
    ("#fin-line { position: absolute; left: 600px; top: 712px; width: 1220px;", "#fin-line { position: absolute; left: 60px; top: 1010px; width: 960px;"),
]
for a, b in pairs:
    assert a in s, a[:60]
    s = s.replace(a, b)
(C / "v-finale.html").write_text(s, encoding="utf-8")
print("ok")
