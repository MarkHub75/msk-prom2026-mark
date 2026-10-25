// HUD of Камера 1.3 drawn the way the АРГУС site draws it (components/Media.tsx + targeted-visual.css):
// white 2.5 px box with a dark outline, red for the object in a red rule, a dark label "человек #5".
// Data: window.HUD_CAM13 = [[ts_s, [[track_id, label, x1, y1, x2, y2, level], ...]], ...] from
// /api/videos/1/tracks (LinQ TPU analysis of argus-real, every 2nd frame). Everything is a function of t.
(function () {
  const RED = "#d64545";

  function frameAt(t) {
    const F = window.HUD_CAM13;
    let lo = 0, hi = F.length - 1;
    if (t <= F[0][0]) return { a: F[0], b: null, k: 0 };
    if (t >= F[hi][0]) return { a: F[hi], b: null, k: 0 };
    while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (F[mid][0] <= t) lo = mid; else hi = mid; }
    return { a: F[lo], b: F[lo + 1], k: (t - F[lo][0]) / (F[lo + 1][0] - F[lo][0]) };
  }

  // Objects at media time t, boxes interpolated between two analysed frames of the same track.
  function objectsAt(t) {
    const { a, b, k } = frameAt(t);
    return a[1].map((o) => {
      const n = b && b[1].find((p) => p[0] === o[0]);
      const box = n ? [2, 3, 4, 5].map((i) => o[i] + (n[i] - o[i]) * k) : o.slice(2, 6);
      return { id: o[0], label: o[1], box, level: o[6] };
    });
  }

  // host: a positioned element covering the video exactly. opts.stroke / opts.font in host px.
  function create(host, opts) {
    const o = Object.assign({ stroke: 2.5, font: 11, ids: null, hideLabelsOf: [] }, opts || {});
    const pool = new Map();
    function el(id) {
      if (pool.has(id)) return pool.get(id);
      const box = document.createElement("div");
      box.className = "hud-box";
      box.style.cssText = `position:absolute;box-sizing:border-box;border:${o.stroke}px solid #f8fcf8;` +
        `box-shadow:0 0 0 ${o.stroke * 0.7}px rgba(16,22,20,.85), inset 0 0 0 ${o.stroke * 0.7}px rgba(16,22,20,.55);`;
      const lab = document.createElement("div");
      lab.className = "hud-lab";
      lab.style.cssText = `position:absolute;transform:translateY(-100%);white-space:nowrap;color:#fff;` +
        `background:rgba(16,22,20,.96);border:1px solid #f8fcf8;font:600 ${o.font}px/1.25 'Source Sans Pro',sans-serif;` +
        `padding:${o.font * 0.36}px ${o.font * 0.55}px;`;
      host.appendChild(box); host.appendChild(lab);
      const rec = { box, lab };
      pool.set(id, rec);
      return rec;
    }
    return function draw(t) {
      const seen = new Set();
      for (const ob of objectsAt(t)) {
        if (o.ids && !o.ids.includes(ob.id)) continue;
        seen.add(ob.id);
        const r = el(ob.id);
        const [x1, y1, x2, y2] = ob.box;
        const red = ob.level === "red";
        Object.assign(r.box.style, { display: "block", left: x1 * 100 + "%", top: y1 * 100 + "%", width: (x2 - x1) * 100 + "%", height: (y2 - y1) * 100 + "%", borderColor: red ? RED : "#f8fcf8" });
        Object.assign(r.lab.style, { display: o.hideLabelsOf.includes(ob.id) ? "none" : "block", left: x1 * 100 + "%", top: `calc(${y1 * 100}% - ${o.stroke}px)`, borderColor: red ? RED : "#f8fcf8" });
        r.lab.innerHTML = `${ob.label}<span style="margin-left:${o.font * 0.5}px;color:#d3ddd7">#${ob.id}</span>`;
      }
      for (const [id, r] of pool) if (!seen.has(id)) { r.box.style.display = "none"; r.lab.style.display = "none"; }
    };
  }

  // A timecode the way the site stamps a recording: mm:ss.
  function mmss(s) { s = Math.max(0, Math.floor(s)); return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); }

  window.ArgusHud = { create, objectsAt, mmss };
})();
