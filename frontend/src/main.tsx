import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, HashRouter } from "react-router-dom";
import { App } from "./App";
import "./theme.css";
import "./styles/mobile-timeline.css";
import "./styles/control-room.css";
import "./styles/pro-skin.css";
import "./styles/ops.css";
import "./styles/ds.css";
import "@fontsource/source-sans-3/cyrillic-400.css";
import "@fontsource/source-sans-3/cyrillic-500.css";
import "@fontsource/source-sans-3/cyrillic-600.css";
import "@fontsource/source-sans-3/cyrillic-700.css";
import "@fontsource/source-sans-3/latin-400.css";
import "@fontsource/source-sans-3/latin-500.css";
import "@fontsource/source-sans-3/latin-600.css";
import "@fontsource/source-sans-3/latin-700.css";
import "@fontsource/source-code-pro/cyrillic-400.css";
import "@fontsource/source-code-pro/latin-400.css";
import "@fontsource/source-code-pro/latin-500.css";
import "@fontsource/source-code-pro/cyrillic-500.css";


async function start() {
  const staticDemo = import.meta.env.VITE_STATIC_DEMO === "1";
  const demo = staticDemo ? await import("./static-demo/index.mjs") : undefined;
  demo?.installStaticDemo();
  const Controls = staticDemo ? (await import("./static-demo/Controls")).DemoControls : undefined;
  const Router = staticDemo ? HashRouter : BrowserRouter;
  createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Router>
      <App />
      {Controls && <Controls />}
    </Router>
  </StrictMode>,
  );
}
void start();
