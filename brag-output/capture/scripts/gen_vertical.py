"""Writes the 1080×1920 scenes of the vertical cut into composition/compositions/v-*.html."""
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[2] / "composition" / "compositions"
FONTS = """    @font-face { font-family: "Source Sans Pro"; font-weight: 900; src: url("assets/fonts/SourceSansPro-Black.ttf"); }
    @font-face { font-family: "Source Sans Pro"; font-weight: 700; src: url("assets/fonts/SourceSansPro-Bold.ttf"); }
    @font-face { font-family: "Source Sans Pro"; font-weight: 600; src: url("assets/fonts/SourceSansPro-Semibold.ttf"); }
"""


def scene(cid, css, html, js, head=""):
    return f"""<template>
  <style>
{FONTS}    #root {{ position: absolute; inset: 0; overflow: hidden; background: #111214; font-family: "Source Sans Pro", sans-serif; color: #eceef1; }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{html}
  </div>
{head}  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""


FILES = {}

FILES["v-hook"] = scene("v-hook", """    #vh-move { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 0 0; }
    #vh-video { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: fill; }
    #vh-scrim { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(17,18,20,.55) 0%, rgba(17,18,20,.9) 30%, rgba(17,18,20,.94) 62%, rgba(17,18,20,.75) 100%); }
    #vh-copy { position: absolute; left: 96px; top: 560px; width: 900px; }
    #vh-num { font-weight: 900; font-size: 290px; line-height: .86; font-variant-numeric: tabular-nums; }
    #vh-line { margin-top: 30px; font-weight: 600; font-size: 60px; line-height: 1.15; color: #c8ccd2; }
    #vh-line span, #vh-punch span { display: inline-block; margin-right: .25em; }
    #vh-punch { margin-top: 90px; font-weight: 700; font-size: 88px; line-height: 1.08; }
    #vh-punch .red { color: #d64545; }
    #vh-src { position: absolute; left: 96px; top: 1640px; font-weight: 600; font-size: 32px; color: #8a909a; }""",
"""    <div id="vh-move"><video id="vh-video" class="clip" data-start="0" data-duration="4.2" data-media-start="0.6" data-track-index="0" muted playsinline src="assets/media/cam13.mp4"></video></div>
    <div id="vh-scrim"></div>
    <div id="vh-copy">
      <div id="vh-num">1,17</div>
      <div id="vh-line"><span>пострадавших</span><span>на</span><span>1000</span><span>работников</span><span>в</span><span>год</span></div>
      <div id="vh-punch"><span>Мастер</span><span>не</span><span>может</span><span>видеть</span><span class="red">всё.</span></div>
    </div>
    <div id="vh-src">Росстат, 2025</div>""",
"""      const at = (cx, cy, s) => ({ scale: s, x: 540 - cx * s, y: 960 - cy * s });
      tl.fromTo("#vh-move", at(1380, 540, 1.78), { ...at(1360, 520, 1.9), duration: 4.2, ease: "none" }, 0);
      const num = document.getElementById("vh-num"), c = { v: 0 };
      tl.fromTo("#vh-num", { opacity: 0, filter: "blur(14px)", y: 18 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.45, ease: "expo.out" }, 0.15);
      tl.fromTo(c, { v: 0 }, { v: 1.17, duration: 0.75, ease: "power3.out", onUpdate: () => { num.textContent = c.v.toFixed(2).replace(".", ","); } }, 0.15);
      tl.fromTo("#vh-line span", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, stagger: 0.075, ease: "power2.out" }, 0.62);
      tl.fromTo("#vh-src", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.9);
      tl.fromTo("#vh-punch span", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, stagger: 0.08, ease: "power2.out" }, 1.85);
      tl.to("#vh-copy, #vh-src", { y: -120, opacity: 0, filter: "blur(16px)", duration: 0.24, ease: "power3.in" }, 3.78);""")

FILES["v-cam"] = scene("v-cam", """    #vc-move { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 0 0; }
    #vc-video { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: fill; }
    #vc-hud { position: absolute; inset: 0; }
    #vc-zone { position: absolute; left: 1152px; top: 486px; width: 422.4px; height: 486px; border: 2px dashed rgba(214,69,69,.8); background: rgba(214,69,69,.08); }
    #vc-zone-fill { position: absolute; inset: 0; background: rgba(214,69,69,.16); opacity: 0; }
    #vc-zone-lab { position: absolute; left: -2px; top: -2px; transform: translateY(-100%); padding: 3px 7px; background: rgba(16,22,20,.92); border: 1px solid rgba(214,69,69,.9); color: #f0d0d0; font-weight: 600; font-size: 12px; white-space: nowrap; }
    #vc-stamp { position: absolute; right: 96px; top: 200px; display: flex; flex-direction: column; align-items: flex-end; gap: 2px; padding: 10px 16px; border-radius: 4px; background: rgba(0,0,0,.62); color: rgba(255,255,255,.82); font-weight: 600; font-size: 30px; line-height: 1.3; }
    #vc-stamp b { font: 500 36px/1.25 "Source Code Pro", monospace; color: #fff; letter-spacing: .02em; }
    #vc-reason { position: absolute; left: 96px; right: 96px; top: 1460px; padding: 22px 28px; background: #d64545; color: #fff; font-weight: 700; font-size: 52px; line-height: 1.15; opacity: 0; }
    #vc-reason small { display: block; font-weight: 600; font-size: 34px; opacity: .9; margin-bottom: 6px; }
    #vc-kick { position: absolute; left: 96px; top: 200px; padding: 14px 22px 14px 18px; background: rgba(17,18,20,.9); border-left: 4px solid #3d84f0; font-weight: 700; font-size: 44px; }
    #vc-flash { position: absolute; inset: 0; box-shadow: inset 0 0 0 0 rgba(214,69,69,0); }""",
"""    <div id="vc-move">
      <video id="vc-video" class="clip" data-start="0" data-duration="6.2" data-media-start="11.397" data-track-index="0" muted playsinline src="assets/media/cam13.mp4"></video>
      <div id="vc-zone"><div id="vc-zone-fill"></div><div id="vc-zone-lab">Проезд погрузчиков</div></div>
      <div id="vc-hud"></div>
    </div>
    <div id="vc-kick">Диспетчерская · Камера 1.3</div>
    <div id="vc-stamp">Камера 1.3 · Проход у пресса<b id="vc-tc">00:11 · кадр 285</b></div>
    <div id="vc-reason"><small>Опасное сближение с техникой</small>Человек в зоне «Проезд погрузчиков»</div>
    <div id="vc-flash"></div>""",
"""      const MEDIA = 11.397, DUR = 6.2, FPS = 25.05, RED_AT = 16.687 - MEDIA;
      const draw = window.ArgusHud.create(document.getElementById("vc-hud"), { stroke: 1.6, font: 9, hideLabelsOf: [1, 2, 3, 4, 6] });
      const tc = document.getElementById("vc-tc");
      const render = (t) => { const m = MEDIA + t; draw(m); tc.textContent = window.ArgusHud.mmss(m) + " · кадр " + Math.floor(m * FPS); };
      const p = { t: 0 };
      tl.fromTo(p, { t: 0 }, { t: DUR, duration: DUR, ease: "none", onUpdate: () => render(p.t) }, 0);
      render(0);
      const at = (cx, cy, s) => ({ scale: s, x: 540 - cx * s, y: 960 - cy * s });
      tl.fromTo("#vc-move", { ...at(1300, 540, 1.7778), filter: "blur(10px)" }, { ...at(1300, 540, 1.7778), filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, 0);
      tl.to("#vc-move", { ...at(1350, 400, 2.4), duration: RED_AT - 0.3, ease: "power1.inOut" }, 0.3);
      tl.to("#vc-move", { ...at(1352, 405, 2.48), duration: 0.18, ease: "expo.out" }, RED_AT);
      tl.fromTo("#vc-kick", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, 0.2);
      tl.to("#vc-kick", { opacity: 0, duration: 0.25 }, 2.2);
      tl.fromTo("#vc-stamp", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 2.3);
      tl.fromTo("#vc-zone-fill", { opacity: 0 }, { opacity: 1, duration: 0.12 }, RED_AT);
      tl.fromTo("#vc-reason", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: "expo.out" }, RED_AT + 0.04);
      tl.fromTo("#vc-flash", { boxShadow: "inset 0 0 0 0px rgba(214,69,69,0)" }, { boxShadow: "inset 0 0 0 30px rgba(214,69,69,.85)", duration: 0.1, ease: "power2.out" }, RED_AT);
      tl.to("#vc-flash", { boxShadow: "inset 0 0 0 12px rgba(214,69,69,.7)", duration: 0.35, ease: "power2.out" }, RED_AT + 0.1);""",
"""  <script src="assets/js/hud-cam13.js"></script>
  <script src="assets/js/hud.js"></script>
""")

# Phone screenshots 1170×2532 shown at 840×1818 (scale 0.718 of pixels, 2.154 of points), screen at (120, 51).
FILES["v-oper"] = scene("v-oper", """    #vo-screen { position: absolute; left: 120px; top: 51px; width: 840px; height: 1818px; border-radius: 64px; overflow: hidden; box-shadow: 0 0 0 3px #2f3238, 0 40px 90px rgba(0,0,0,.6); }
    #vo-screen img { position: absolute; left: 0; top: 0; width: 840px; height: 1818px; }
    /* the takeover screen below its evidence thumbnail (pt 272..844), 960 px wide: 0.8205 px per screenshot px */
    #vo-crop { position: absolute; left: 60px; top: 256px; width: 960px; height: 1407px; border-radius: 40px; overflow: hidden; background: #18191c; box-shadow: 0 0 0 3px #d64545, 0 40px 90px rgba(0,0,0,.6); opacity: 0; }
    #vo-crop img { position: absolute; left: 0; top: -670px; width: 960px; height: 2077px; }
    #vo-press { position: absolute; left: 42px; top: 955px; width: 876px; height: 128px; border-radius: 6px; background: rgba(0,0,0,.26); opacity: 0; }
    .vo-dot { position: absolute; width: 84px; height: 84px; margin: -42px 0 0 -42px; border-radius: 50%; background: rgba(236,238,241,.42); border: 3px solid rgba(236,238,241,.75); opacity: 0; }
    #vo-dot1 { left: 540px; top: 1063px; }
    #vo-dot2 { left: 540px; top: 1275px; }
    #vo-red { position: absolute; inset: 0; background: #d64545; opacity: 0; }""",
"""    <div id="vo-screen"><img src="assets/media/ph-op-feed.jpg" alt="" /></div>
    <div id="vo-crop"><img src="assets/media/ph-op-red.jpg" alt="" /><div id="vo-press"></div></div>
    <div class="vo-dot" id="vo-dot1"></div>
    <div class="vo-dot" id="vo-dot2"></div>
    <div id="vo-red"></div>""",
"""      tl.fromTo("#vo-red", { opacity: 0.55 }, { opacity: 0, duration: 0.32, ease: "power2.out" }, 0);
      tl.fromTo("#vo-screen", { scale: 1.06, y: 30 }, { scale: 1, y: 0, duration: 0.45, ease: "expo.out" }, 0);
      // tap the red card in the operator's phone feed
      tl.fromTo("#vo-dot1", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.1, ease: "power2.out" }, 0.8);
      tl.to("#vo-dot1", { opacity: 0, duration: 0.14 }, 0.96);
      tl.to("#vo-screen", { opacity: 0.25, scale: 0.96, duration: 0.3, ease: "power2.inOut" }, 1.0);
      tl.fromTo("#vo-crop", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.32, ease: "expo.out" }, 1.02);
      // «Подтверждаю»
      tl.fromTo("#vo-dot2", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.1, ease: "power2.out" }, 1.82);
      tl.fromTo("#vo-press", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 1.9);
      tl.to("#vo-dot2, #vo-press", { opacity: 0, duration: 0.14 }, 2.06);
      tl.to("#vo-crop, #vo-screen", { opacity: 0, filter: "blur(8px)", duration: 0.25, ease: "power3.in" }, 2.15);""")

FILES["v-card"] = scene("v-card", """    #vk-stage { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 0 0; }
    #vk-stage img { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
    #vk-mask { position: absolute; left: 0; top: 0; width: 1446px; height: 1080px; background: #111214; }
    #vk-ring { position: absolute; left: 1449px; top: 401px; width: 466px; height: 40px; border: 2px solid #3d84f0; border-radius: 3px; opacity: 0; }
    #vk-kick { position: absolute; left: 96px; top: 1640px; padding: 14px 22px 14px 18px; background: rgba(17,18,20,.92); border-left: 4px solid #3d84f0; font-weight: 700; font-size: 46px; }""",
"""    <div id="vk-stage"><img src="assets/media/confirmed.jpg" alt="" /><div id="vk-mask"></div><div id="vk-ring"></div></div>
""",
"""      const at = (cx, cy, s) => ({ scale: s, x: -cx * s, y: -cy * s });
      tl.fromTo("#vk-stage", { ...at(1440, 80, 2.25), opacity: 0, filter: "blur(8px)" }, { ...at(1440, 90, 2.25), opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out" }, 0);
      tl.to("#vk-stage", { ...at(1440, 190, 2.25), duration: 1.85, ease: "power1.inOut" }, 0.35);
      tl.fromTo("#vk-ring", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0.5);""")

FILES["v-master"] = scene("v-master", """    #vm-screen { position: absolute; left: 120px; top: 51px; width: 840px; height: 1818px; border-radius: 64px; overflow: hidden; box-shadow: 0 0 0 3px #2f3238, 0 40px 90px rgba(0,0,0,.6); }
    #vm-screen img { position: absolute; left: 0; top: 0; width: 840px; height: 1818px; }
    #vm-measures, #vm-resolved { opacity: 0; }
    .vm-press { position: absolute; border-radius: 8px; background: rgba(0,0,0,.28); opacity: 0; }
    #vm-p1 { left: 67px; top: 1120px; width: 396px; height: 102px; }
    #vm-p2 { left: 37px; top: 1686px; width: 768px; height: 108px; }
    .vm-dot { position: absolute; width: 84px; height: 84px; margin: -42px 0 0 -42px; border-radius: 50%; background: rgba(236,238,241,.42); border: 3px solid rgba(236,238,241,.75); opacity: 0; }
    #vm-d1 { left: 265px; top: 1170px; }
    #vm-d2 { left: 420px; top: 1740px; }""",
"""    <div id="vm-screen">
      <img id="vm-inbox" src="assets/media/ph-inbox.jpg" alt="" />
      <img id="vm-measures" src="assets/media/ph-measures.jpg" alt="" />
      <img id="vm-resolved" src="assets/media/ph-resolved.jpg" alt="" />
      <div class="vm-press" id="vm-p1"></div><div class="vm-press" id="vm-p2"></div>
      <div class="vm-dot" id="vm-d1"></div><div class="vm-dot" id="vm-d2"></div>
    </div>""",
"""      tl.fromTo("#vm-screen", { y: 120, opacity: 0, filter: "blur(10px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 0);
      tl.fromTo("#vm-d1", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.1, ease: "power2.out" }, 0.86);
      tl.fromTo("#vm-p1", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 0.92);
      tl.to("#vm-d1, #vm-p1", { opacity: 0, duration: 0.14 }, 1.06);
      tl.fromTo("#vm-inbox", { x: 0 }, { x: -270, duration: 0.32, ease: "power3.inOut" }, 1.12);
      tl.fromTo("#vm-measures", { x: 840, opacity: 1 }, { x: 0, opacity: 1, duration: 0.32, ease: "power3.inOut" }, 1.12);
      tl.fromTo("#vm-d2", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.1, ease: "power2.out" }, 2.02);
      tl.fromTo("#vm-p2", { opacity: 0 }, { opacity: 1, duration: 0.05 }, 2.08);
      tl.to("#vm-d2, #vm-p2", { opacity: 0, duration: 0.14 }, 2.22);
      tl.fromTo("#vm-resolved", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.24, ease: "power3.out" }, 2.28);""")

FILES["v-linq"] = scene("v-linq", """    #vl-chip { position: absolute; left: 96px; top: 470px; width: 330px; height: 109px; }
    #vl-head { position: absolute; left: 96px; top: 620px; font-weight: 700; font-size: 92px; line-height: 1.05; }
    .vl-fig { position: absolute; left: 96px; }
    #vl-f1 { top: 900px; }
    #vl-f2 { top: 1240px; }
    .vl-num { font-weight: 900; font-size: 220px; line-height: .9; }
    .vl-num small { font-weight: 700; font-size: 72px; margin-left: 20px; color: #c8ccd2; }
    .vl-lab { margin-top: 18px; font-weight: 600; font-size: 44px; color: #a1a7b0; }""",
"""    <img id="vl-chip" src="assets/media/chip-linq.png" alt="" />
    <div id="vl-head">Детекции —<br />на LinQ TPU</div>
    <div class="vl-fig" id="vl-f1"><div class="vl-num">10,6<small>кадр/с</small></div><div class="vl-lab">детектор на ускорителе</div></div>
    <div class="vl-fig" id="vl-f2"><div class="vl-num">308<small>мс</small></div><div class="vl-lab">задержка, медиана</div></div>""",
"""      tl.fromTo("#vl-chip", { opacity: 0, scale: 0.86, transformOrigin: "0 50%" }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, 0.02);
      tl.fromTo("#vl-head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power2.out" }, 0.1);
      tl.fromTo(".vl-fig", { opacity: 0, y: 30, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, stagger: 0.12, ease: "expo.out" }, 0.3);""")

FILES["v-phrase"] = scene("v-phrase", """    #vp { position: absolute; left: 96px; top: 0; bottom: 0; display: flex; flex-direction: column; justify-content: center; }
    .vp-line { font-weight: 700; font-size: 92px; line-height: 1.1; white-space: nowrap; }
    .vp-line span { display: inline-block; margin-right: .22em; }
    .vp-line span:last-child { margin-right: 0; }
    #vp-l1 { color: #a1a7b0; }
    #vp-l3 { margin-top: 70px; margin-left: 22px; }
    #vp-target { position: relative; display: inline-block; }
    #vp-box { position: absolute; left: -22px; top: 6px; right: -22px; bottom: -6px; border: 6px solid #d64545; box-shadow: 0 0 0 3px rgba(16,22,20,.9), inset 0 0 0 3px rgba(16,22,20,.6); }
    #vp-lab { position: absolute; left: -22px; top: 8px; transform: translateY(-100%); padding: 6px 12px; background: rgba(16,22,20,.96); border: 2px solid #d64545; font-weight: 600; font-size: 32px; color: #fff; white-space: nowrap; }""",
"""    <div id="vp">
      <div class="vp-line" id="vp-l1"><span>Точность</span><span>там,</span></div>
      <div class="vp-line" id="vp-l2"><span>где</span></div>
      <div class="vp-line" id="vp-l3"><span id="vp-target"><span>что-то</span><span>происходит.</span><i id="vp-box"></i><b id="vp-lab">событие</b></span></div>
    </div>""",
"""      tl.fromTo("#vp-l1 span, #vp-l2 span, #vp-target > span", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, stagger: 0.09, ease: "power2.out" }, 0.15);
      tl.fromTo("#vp-box", { opacity: 0, scaleX: 1.12, scaleY: 1.5 }, { opacity: 1, scaleX: 1, scaleY: 1, duration: 0.26, ease: "expo.out" }, 0.86);
      tl.fromTo("#vp-lab", { opacity: 0 }, { opacity: 1, duration: 0.12 }, 1.0);
      tl.to("#vp", { opacity: 0, filter: "blur(10px)", duration: 0.22, ease: "power2.in" }, 3.95);""")

for name, text in FILES.items():
    (OUT / f"{name}.html").write_text(text, encoding="utf-8")
print(sorted(FILES))
