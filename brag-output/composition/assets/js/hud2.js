// HUD for the depot clips, in the АРГУС site style (components/Media.tsx, ds.css): white box with a dark outline,
// amber / red for rule levels, a dark label chip, muted pose skeleton, dashed danger zone.
// Data: window.HUD[clip] = {fps, zone: {name, poly} | null, frames: [[t, [[id, kind, x1, y1, x2, y2, level, label, kp], ...]], ...]}
// produced by capture/scripts/depot_hud.py from YOLOv8 detections (not LinQ). Everything is a function of media time.
(function () {
  const COL = { "": "#f8fcf8", amber: "#c99a3a", red: "#d64545" };
  const BONES = [[5, 7], [7, 9], [6, 8], [8, 10], [5, 6], [5, 11], [6, 12], [11, 12], [11, 13], [13, 15], [12, 14], [14, 16]];
  const SVG = "http://www.w3.org/2000/svg";

  function create(host, clip, opts) {
    const o = Object.assign({ stroke: 2.5, font: 12, pose: false, zone: false, labels: true, ids: null, hide: [], trains: true }, opts || {});
    const data = window.HUD[clip];
    const svg = document.createElementNS(SVG, "svg");
    svg.setAttribute("viewBox", "0 0 1000 1000");
    svg.setAttribute("preserveAspectRatio", "none");
    svg.style.cssText = "position:absolute;inset:0;width:100%;height:100%;overflow:visible";
    host.appendChild(svg);
    if (o.zone && data.zone) {
      const poly = document.createElementNS(SVG, "polygon");
      poly.setAttribute("points", data.zone.poly.map(([x, y]) => `${x * 1000},${y * 1000}`).join(" "));
      poly.setAttribute("fill", "rgba(214,69,69,.12)");
      poly.setAttribute("stroke", "rgba(214,69,69,.85)");
      poly.setAttribute("stroke-width", o.stroke * 0.8);
      poly.setAttribute("stroke-dasharray", `${o.stroke * 4} ${o.stroke * 3}`);
      poly.setAttribute("vector-effect", "non-scaling-stroke");
      poly.classList.add("hud2-zone");
      svg.appendChild(poly);
    }
    const bones = document.createElementNS(SVG, "g");
    svg.appendChild(bones);
    const pool = new Map();
    function el(id) {
      if (pool.has(id)) return pool.get(id);
      const box = document.createElement("div");
      box.style.cssText = `position:absolute;box-sizing:border-box;border:${o.stroke}px solid #f8fcf8;` +
        `box-shadow:0 0 0 ${o.stroke * 0.7}px rgba(16,22,20,.85), inset 0 0 0 ${o.stroke * 0.7}px rgba(16,22,20,.5);`;
      const lab = document.createElement("div");
      lab.style.cssText = `position:absolute;transform:translateY(-100%);white-space:nowrap;color:#fff;background:rgba(16,22,20,.95);` +
        `border:1px solid #f8fcf8;font:600 ${o.font}px/1.25 'Source Sans Pro',sans-serif;padding:${o.font * 0.32}px ${o.font * 0.5}px;`;
      host.appendChild(box);
      host.appendChild(lab);
      const r = { box, lab };
      pool.set(id, r);
      return r;
    }
    const lines = [];
    function line(i) {
      while (lines.length <= i) {
        const l = document.createElementNS(SVG, "line");
        l.setAttribute("stroke", "rgba(236,238,241,.7)");
        l.setAttribute("stroke-width", o.stroke * 0.7);
        l.setAttribute("stroke-linecap", "round");
        l.setAttribute("vector-effect", "non-scaling-stroke");
        bones.appendChild(l);
        lines.push(l);
      }
      return lines[i];
    }
    return function draw(t) {
      const F = data.frames;
      const i = Math.max(0, Math.min(F.length - 1, Math.round(t * data.fps)));
      const seen = new Set();
      let li = 0;
      for (const ob of F[i][1]) {
        const [id, kind, x1, y1, x2, y2, level, label, kp] = ob;
        if (o.ids && !o.ids.includes(id)) continue;
        if (o.hide.includes(id) || (kind === "train" && !o.trains)) continue;
        seen.add(id);
        const r = el(id);
        const c = COL[level] || COL[""];
        Object.assign(r.box.style, { display: "block", left: x1 * 100 + "%", top: y1 * 100 + "%", width: (x2 - x1) * 100 + "%", height: (y2 - y1) * 100 + "%", borderColor: c });
        Object.assign(r.lab.style, { display: o.labels ? "block" : "none", left: x1 * 100 + "%", top: `calc(${y1 * 100}% - ${o.stroke}px)`, borderColor: c });
        r.lab.textContent = label;
        if (o.pose && kp) {
          for (const [a, b] of BONES) {
            if (kp[a][2] < 0.3 || kp[b][2] < 0.3) continue;
            const l = line(li++);
            l.setAttribute("x1", kp[a][0] * 1000); l.setAttribute("y1", kp[a][1] * 1000);
            l.setAttribute("x2", kp[b][0] * 1000); l.setAttribute("y2", kp[b][1] * 1000);
            l.style.display = "";
          }
        }
      }
      for (let k = li; k < lines.length; k++) lines[k].style.display = "none";
      for (const [id, r] of pool) if (!seen.has(id)) { r.box.style.display = "none"; r.lab.style.display = "none"; }
    };
  }

  window.ArgusHud2 = { create };
})();
