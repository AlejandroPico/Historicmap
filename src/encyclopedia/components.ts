// Componentes visuales invocables desde las páginas con «:::componente nombre argumentos».
// P01 incluye los básicos; P02 amplía la biblioteca (series, líneas de tiempo, mapas, árboles).
import { geologicalUnits, geologicalAgeLabel, type GeologicalUnit } from '../earth-chronology';
import { scientificDiagram } from '../encyclopedia-diagrams';
import { esc } from './markdown';

interface Context { year: number }
type Component = (args: string, ctx: Context) => string;

const LEVELS: GeologicalUnit['rank'][] = ['eon', 'era', 'period', 'epoch'];
const LEVEL_LABEL: Record<string, string> = { eon: 'Eones', era: 'Eras', period: 'Periodos', epoch: 'Épocas' };

/** Escala temporal en bandas proporcionales. Argumento opcional: id ICS raíz (p. ej. «Phanerozoic»). */
function scale(args: string): string {
  const rootId = args.trim();
  const root = rootId ? geologicalUnits.find(u => u.id === rootId) : undefined;
  const oldest = root ? root.oldestMa : Math.max(...geologicalUnits.map(u => u.oldestMa));
  const youngest = root ? root.youngestMa : 0;
  const inside = (u: GeologicalUnit) => u.oldestMa <= oldest + 1e-9 && u.youngestMa >= youngest - 1e-9;
  const span = oldest - youngest, W = 1000, rowH = 34, label = 92;
  const levels = LEVELS.filter(l => geologicalUnits.some(u => u.rank === l && inside(u) && (!root || u.id !== root.id || true)));
  const rows = levels.map((level, r) => {
    const units = geologicalUnits.filter(u => u.rank === level && inside(u));
    return `<text x="0" y="${r * rowH + 21}" class="enc-scale-label">${LEVEL_LABEL[level]}</text>` + units.map(u => {
      const x = label + (oldest - u.oldestMa) / span * (W - label), w = Math.max(.6, (u.oldestMa - u.youngestMa) / span * (W - label));
      const name = w > u.name.length * 6.4 ? u.name : w > 26 ? u.name.slice(0, Math.max(1, Math.floor(w / 7))) + '.' : '';
      return `<g class="enc-scale-unit" data-encyclopedia-entry="geo-${u.id}" role="link" tabindex="0" aria-label="${esc(u.name)} · ${esc(geologicalAgeLabel(u.oldestMa))}"><rect x="${x.toFixed(2)}" y="${r * rowH + 2}" width="${w.toFixed(2)}" height="${rowH - 4}" fill="${esc(u.color)}"><title>${esc(u.name)} · ${esc(geologicalAgeLabel(u.oldestMa))} – ${esc(u.youngestMa ? geologicalAgeLabel(u.youngestMa) : 'hoy')}</title></rect>${name ? `<text x="${(x + w / 2).toFixed(2)}" y="${r * rowH + 21}" text-anchor="middle">${esc(name)}</text>` : ''}</g>`;
    }).join('');
  }).join('');
  const ticks = Array.from({ length: 6 }, (_, i) => oldest - span * i / 5);
  const axisY = levels.length * rowH + 16;
  const axis = ticks.map(t => { const x = label + (oldest - t) / span * (W - label); return `<text x="${x.toFixed(1)}" y="${axisY}" text-anchor="${t <= 0.0001 ? 'end' : 'middle'}" class="enc-scale-tick">${esc(t <= 0.0001 ? 'hoy' : geologicalAgeLabel(t))}</text>`; }).join('');
  return `<figure class="enc-component enc-scale"><svg viewBox="0 0 ${W} ${axisY + 8}" role="img" aria-label="Escala temporal geológica${root ? ' del ' + esc(root.name) : ''}">${rows}${axis}</svg><figcaption>Escala proporcional al tiempo${root ? ` del ${esc(root.name)}` : ''} según la carta ICS 2026/06. Pulsa cualquier unidad para abrir su página.</figcaption></figure>`;
}

/** Comparación de duraciones: cuánto ocupa cada eón si la historia de la Tierra fuera un día de 24 horas. */
function clock(): string {
  const eons = geologicalUnits.filter(u => u.rank === 'eon').sort((a, b) => b.oldestMa - a.oldestMa);
  const total = 4540;let acc = 0;
  const rows = eons.map(u => {
    const start = Math.max(0, (total - Math.min(u.oldestMa, total)) / total * 24), end = (total - u.youngestMa) / total * 24;
    const hm = (h: number) => `${String(Math.floor(h)).padStart(2, '0')}:${String(Math.floor((h % 1) * 60)).padStart(2, '0')}`;
    return `<tr><td><span class="enc-swatch" style="background:${esc(u.color)}"></span> <a href="#" class="enc-link" data-encyclopedia-entry="geo-${u.id}">${esc(u.name)}</a></td><td>${hm(start)}</td><td>${hm(Math.min(24, end))}</td></tr>`;
  }).join('');
  const sec = (ka: number) => (ka * 1000 / (total * 1e6) * 86400).toLocaleString('es', { maximumFractionDigits: 2 });
  return `<div class="enc-table enc-clock"><table><thead><tr><th>Eón</th><th>Empieza</th><th>Termina</th></tr></thead><tbody>${rows}</tbody></table><p class="enc-muted">En esa escala, los dinosaurios no avianos se extinguen a las 23:39; el género <em>Homo</em> aparece unos ${(2.8e6 / (total * 1e6) * 1440).toLocaleString('es', { maximumFractionDigits: 1 })} minutos antes de medianoche; la agricultura, hace ${sec(12)} segundos, y los últimos 2.000 años ocupan ${sec(2)} segundos.</p></div>`;
}

function phanda(_args: string, ctx: Context) {
  return scientificDiagram({ id: 'phanda', title: 'Temperatura global del Fanerozoico', summary: '', sections: [], sourceIds: [], related: [], diagram: 'climate', year: ctx.year });
}

const registry: Record<string, Component> = { 'escala-geologica': scale, 'reloj-geologico': clock, 'curva-temperatura-fanerozoico': phanda };

export function component(name: string, args: string, ctx: Context) {
  const fn = registry[name];
  return fn ? fn(args, ctx) : `<p class="enc-muted">[Componente «${esc(name)}» no disponible]</p>`;
}
export const componentNames = Object.keys(registry);
