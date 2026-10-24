// Adapted from the OS cinematic-ppt-v1 image-slide export precedent.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const osRoot = process.env.SAFEWATCH_OS_ROOT || '/mnt/d/templates/frontend-hackathon-os';
const candidates = [
  process.env.SAFEWATCH_PPTXGENJS_MODULE,
  path.join(root, 'node_modules/pptxgenjs/dist/pptxgen.es.js'),
  path.join(osRoot, 'production/presentation_factory/jury-defense-v1/app/node_modules/pptxgenjs/dist/pptxgen.es.js'),
  path.join(osRoot, 'node_modules/pptxgenjs/dist/pptxgen.es.js'),
].filter(Boolean);
let modulePath;
for (const candidate of candidates) {
  try { await fs.access(candidate); modulePath = candidate; break; } catch {}
}
if (!modulePath) {
  const require = createRequire(import.meta.url);
  try { modulePath = require.resolve('pptxgenjs'); } catch {}
}
if (!modulePath) throw new Error('PptxGenJS not found. Set SAFEWATCH_PPTXGENJS_MODULE to an existing OS/toolchain module.');
const imported = await import(pathToFileURL(path.resolve(modulePath)).href);
const PptxGenJS = imported.default || imported;
const input = JSON.parse(await fs.readFile(path.join(root, 'speaker-notes.json'), 'utf8'));
const scenes = Array.isArray(input) ? input : input.slides;
if (!Array.isArray(scenes) || scenes.length !== 8) throw new Error('speaker-notes.json must contain exactly eight slides.');
const pptx = new PptxGenJS();
pptx.defineLayout({name: 'SAFEWATCH_16_9', width: 13.3333333333, height: 7.5});
pptx.layout = 'SAFEWATCH_16_9';
pptx.author = 'Команда продукта';
pptx.company = 'Команда продукта';
pptx.title = 'АРГУС — каркас финальной презентации';
pptx.subject = 'Восемь растровых слайдов с заметками докладчика';
pptx.lang = 'ru-RU';
for (let index = 0; index < scenes.length; index++) {
  const scene = scenes[index];
  const id = String(index + 1).padStart(2, '0');
  if (scene.id !== undefined && String(scene.id).padStart(2, '0') !== id) throw new Error('Slide order differs from notes: ' + id);
  if (typeof scene.title !== 'string' || typeof scene.speech !== 'string') throw new Error('Each slide needs title and speech: ' + id);
  const imagePath = path.join(root, 'slides', `slide-${id}.png`);
  const bytes = await fs.readFile(imagePath);
  if (bytes.subarray(1, 4).toString() !== 'PNG' || bytes.readUInt32BE(16) !== 1920 || bytes.readUInt32BE(20) !== 1080) throw new Error('Expected 1920×1080 PNG: ' + imagePath);
  const slide = pptx.addSlide();
  slide.addImage({path: imagePath, x: 0, y: 0, w: 13.3333333333, h: 7.5, altText: scene.title});
  const notes = [
    `СЛАЙД ${index + 1}/8 · ${scene.title}`,
    scene.duration ? `БЮДЖЕТ ВЫСТУПЛЕНИЯ: ${scene.duration} с (план, не измерение).` : '',
    '', 'ТЕКСТ', scene.speech,
    scene.notes ? '\nПРИМЕЧАНИЯ\n' + scene.notes : '',
    scene.sources ? '\nИСТОЧНИКИ\n' + (Array.isArray(scene.sources) ? scene.sources.join('\n') : scene.sources) : '',
    '\nФормат: один полноразмерный PNG на слайд. Изображение слайда не редактируется по отдельным объектам; заметки остаются текстовыми.',
  ].filter(Boolean).join('\n');
  slide.addNotes(notes);
}
await fs.mkdir(path.join(root, 'exports'), {recursive: true});
const output = path.join(root, 'exports', 'ARGUS_Final_Skeleton.pptx');
await pptx.writeFile({fileName: output});
console.log(JSON.stringify({status: 'WRITTEN', slides: 8, output, modulePath}));
