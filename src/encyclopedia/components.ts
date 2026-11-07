// Biblioteca de componentes visuales de la enciclopedia (P02).
// Desde Markdown:  «:::componente nombre argumentos» + «:::» (sin datos)
//                  «:::grafico …», «:::linea-tiempo …», «:::mapa …», «:::galeria …» (con datos en el bloque)
// Los componentes devuelven HTML; los interactivos se activan con hydrateComponents() tras pintar la página.
import { geologicalUnits, geologicalAgeLabel, rankLabels, type GeologicalUnit } from '../earth-chronology';
import { scientificDiagram } from '../encyclopedia-diagrams';
import { planetRecordFor, planetValue, type PlanetField } from '../planet';
import { formatYear } from '../time';
import { esc, inline } from './markdown';
import { civilYear } from '../../scripts/lib/encyclopedia-format.mjs';

export interface ComponentContext { year: number; media?: (path: string) => string | undefined; credit?: (path: string) => string | undefined }
type Component = (args: string, ctx: ComponentContext, content: string) => string;

const PALETTE = ['#d4b06a', '#6fa8bd', '#c97b63', '#8fb27a', '#b08cc4', '#e0d38a', '#7c94c9', '#d18aa8'];
const num = (s: string) => Number(String(s).trim().replace(/\s/g, '').replace(',', '.'));
const fmt = (n: number) => Math.abs(n) >= 1e4 ? n.toLocaleString('es', { maximumFractionDigits: 0 }) : n.toLocaleString('es', { maximumFractionDigits: 2 });
function niceTicks(min: number, max: number, count = 5) {
  if (min === max) { min -= 1; max += 1; }
  const step0 = (max - min) / count, mag = 10 ** Math.floor(Math.log10(Math.abs(step0))), norm = step0 / mag;
  const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
  const out: number[] = []; for (let v = Math.ceil(min / step) * step; v <= max + step * 1e-9; v += step) out.push(Number(v.toPrecision(12)));
  return out;
}

/* ---------- Escala geológica interactiva: zoom por unidad ---------- */
const RANKS: GeologicalUnit['rank'][] = ['eon', 'era', 'period', 'epoch', 'age'];
const RANK_PLURAL: Record<string, string> = { eon: 'Eones', era: 'Eras', period: 'Periodos', epoch: 'Épocas', age: 'Edades' };
const unit = (id: string) => geologicalUnits.find(u => u.id === id);

/** SVG y cabecera de la escala centrada en una unidad (vacío = toda la historia). */
export function scaleView(focusId: string) {
  const focus = focusId ? unit(focusId) : undefined;
  const oldest = focus ? focus.oldestMa : 4567, youngest = focus ? focus.youngestMa : 0, span = oldest - youngest;
  const inside = (u: GeologicalUnit) => u.oldestMa <= oldest + 1e-6 && u.youngestMa >= youngest - 1e-6 && u.id !== focus?.id;
  const startRank = focus ? Math.max(0, RANKS.indexOf(focus.rank as GeologicalUnit['rank']) + 1) : 0;
  const levels = RANKS.slice(startRank).filter(r => geologicalUnits.some(u => u.rank === r && inside(u))).slice(0, 3);
  const W = 1000, rowH = 42, label = 78;
  const rows = levels.map((rank, r) => `<text x="0" y="${r * rowH + 25}" class="enc-scale-label">${RANK_PLURAL[rank]}</text>` + geologicalUnits.filter(u => u.rank === rank && inside(u)).map(u => {
    const x = label + (oldest - u.oldestMa) / span * (W - label), w = Math.max(.8, (u.oldestMa - u.youngestMa) / span * (W - label));
    const kids = geologicalUnits.some(c => c.parent === u.id);
    const name = w > u.name.length * 7.6 + 8 ? u.name : w > 36 ? u.name.slice(0, Math.max(2, Math.floor((w - 8) / 7.8))) + '.' : '';
    const title = `${u.name} · ${geologicalAgeLabel(u.oldestMa)} – ${u.youngestMa ? geologicalAgeLabel(u.youngestMa) : 'hoy'}${kids ? ' · pulsa para ampliar' : ' · pulsa para abrir'}`;
    return `<g class="enc-scale-unit" ${kids ? `data-scale-zoom="${u.id}"` : `data-encyclopedia-entry="geo-${u.id}"`} role="button" tabindex="0" aria-label="${esc(title)}"><rect x="${x.toFixed(2)}" y="${r * rowH + 3}" width="${w.toFixed(2)}" height="${rowH - 6}" rx="2" fill="${esc(u.color)}"><title>${esc(title)}</title></rect>${name ? `<text x="${(x + w / 2).toFixed(2)}" y="${r * rowH + 25}" text-anchor="middle">${esc(name)}</text>` : ''}</g>`;
  }).join('')).join('');
  const axisY = levels.length * rowH + 20;
  const axis = niceTicks(youngest, oldest, 7).map(t => { const x = label + (oldest - t) / span * (W - label); return `<line x1="${x.toFixed(1)}" x2="${x.toFixed(1)}" y1="${axisY - 14}" y2="${axisY - 9}" class="enc-axis"/><text x="${x.toFixed(1)}" y="${axisY + 2}" text-anchor="middle" class="enc-scale-tick">${esc(t <= 1e-9 ? 'hoy' : geologicalAgeLabel(t))}</text>`; }).join('');
  const trail: GeologicalUnit[] = []; let p = focus; while (p) { trail.unshift(p); p = p.parent ? unit(p.parent) : undefined; }
  const crumbs = [`<button data-scale-zoom="">Toda la historia</button>`, ...trail.filter(t => t.rank !== 'group').map(t => `<button data-scale-zoom="${t.id}">${esc(t.name)}</button>`)].join('<span>›</span>');
  const head = `<div class="enc-scale-head"><nav aria-label="Nivel de la escala">${crumbs}</nav>${focus ? `<a href="#" class="enc-link" data-encyclopedia-entry="geo-${focus.id}">Abrir ${esc(focus.name)} →</a>` : ''}</div>`;
  const info = focus ? `<p class="enc-scale-info">${esc(rankLabels[focus.rank])} · ${esc(geologicalAgeLabel(focus.oldestMa))} – ${esc(focus.youngestMa ? geologicalAgeLabel(focus.youngestMa) : 'hoy')} · duración ≈ ${esc(geologicalAgeLabel(span))}</p>` : '';
  return `${head}${info}<div class="enc-scale-scroll"><svg viewBox="0 0 ${W} ${axisY + 10}" role="img" aria-label="Escala temporal geológica${focus ? ' · ' + esc(focus.name) : ''}">${rows}${axis}</svg></div>`;
}
function scale(args: string) {
  return `<figure class="enc-component enc-scale" data-scale-root="${esc(args.trim())}">${scaleView(args.trim())}<figcaption>Escala proporcional según la carta ICS 2026/06. Pulsa una unidad para ampliarla y ver sus subdivisiones; las unidades sin subdivisiones abren su página. Desliza horizontalmente en pantallas estrechas.</figcaption></figure>`;
}

/* ---------- Reloj geológico ---------- */
function clock(): string {
  const eons = geologicalUnits.filter(u => u.rank === 'eon').sort((a, b) => b.oldestMa - a.oldestMa), total = 4540;
  const hm = (h: number) => `${String(Math.floor(h)).padStart(2, '0')}:${String(Math.floor((h % 1) * 60)).padStart(2, '0')}`;
  const pos = (ma: number) => Math.max(0, (total - Math.min(ma, total)) / total * 24);
  const rows = eons.map(u => `<tr><td><span class="enc-swatch" style="background:${esc(u.color)}"></span> <a href="#" class="enc-link" data-encyclopedia-entry="geo-${u.id}">${esc(u.name)}</a></td><td>${hm(pos(u.oldestMa))}</td><td>${hm(Math.min(24, pos(u.youngestMa)))}</td></tr>`).join('');
  const bar = eons.map(u => `<span style="flex:${Math.min(u.oldestMa, total) - u.youngestMa};background:${esc(u.color)}" title="${esc(u.name)}"></span>`).join('');
  const sec = (ka: number) => (ka * 1000 / (total * 1e6) * 86400).toLocaleString('es', { maximumFractionDigits: 2 });
  return `<div class="enc-clock"><div class="enc-clock-bar">${bar}</div><div class="enc-clock-hours"><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div><div class="enc-table"><table><thead><tr><th>Eón</th><th>Empieza</th><th>Termina</th></tr></thead><tbody>${rows}</tbody></table></div><p class="enc-muted">En esa escala, los dinosaurios no avianos se extinguen a las 23:39; el género <em>Homo</em> aparece unos ${(2.8e6 / (total * 1e6) * 1440).toLocaleString('es', { maximumFractionDigits: 1 })} minutos antes de medianoche; la agricultura, ${sec(12)} segundos antes, y los últimos 2.000 años ocupan ${sec(2)} segundos.</p></div>`;
}

function phanda(_args: string, ctx: ComponentContext) {
  return scientificDiagram({ id: 'phanda', title: 'Temperatura global del Fanerozoico', summary: '', sections: [], sourceIds: [], related: [], diagram: 'climate', year: ctx.year });
}

/* ---------- Composición atmosférica y indicadores en una fecha ---------- */
function atmosphere(args: string, ctx: ComponentContext) {
  const year = args.trim() ? civilYear(args.trim()) ?? ctx.year : ctx.year;
  const gases: [PlanetField, string, string][] = [['nitrogen', 'N₂', '#7c94c9'], ['oxygen', 'O₂', '#6fa8bd'], ['argon', 'Ar', '#b08cc4'], ['carbonDioxide', 'CO₂', '#c97b63'], ['methane', 'CH₄', '#8fb27a'], ['waterVapor', 'H₂O', '#e0d38a']];
  const rows = gases.map(([f, label, color]) => { const r = planetRecordFor(f, year); return r ? { label, color, value: planetValue(r), share: r.value === null ? 0 : typeof r.value === 'number' ? r.value : (r.value.min + r.value.max) / 2, unit: r.unit } : null; }).filter((r): r is NonNullable<typeof r> => !!r);
  if (!rows.length) return `<p class="enc-muted">Sin datos de composición atmosférica para ${esc(formatYear(year))}.</p>`;
  const total = rows.reduce((n, r) => n + (Number.isFinite(r.share) ? r.share : 0), 0) || 1;
  return `<figure class="enc-component enc-atmo"><div class="enc-atmo-bar">${rows.map(r => `<span style="flex:${Math.max(.004, r.share / total)};background:${r.color}" title="${esc(r.label)} · ${esc(r.value)}"></span>`).join('')}</div><dl>${rows.map(r => `<div><dt><i style="background:${r.color}"></i>${esc(r.label)}</dt><dd>${esc(r.value)}</dd></div>`).join('')}</dl><figcaption>Composición de referencia de la atmósfera en ${esc(formatYear(year))} según los registros del panel Planeta. Los gases traza se exageran para ser visibles.</figcaption></figure>`;
}

/* ---------- Gráfico de series a partir de datos del bloque ---------- */
/** «:::grafico linea|area|barras | Título | unidad del eje Y | unidad del eje X»; primera línea: cabecera «x; serie 1; serie 2». */
function chart(args: string, _ctx: ComponentContext, content: string) {
  const [kindRaw, title = '', yUnit = '', xUnit = ''] = args.split('|').map(s => s.trim());
  const kind = ['linea', 'area', 'barras'].includes(kindRaw) ? kindRaw : 'linea';
  const lines = content.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
  if (lines.length < 2) return '';
  const sep = lines[0].includes(';') ? ';' : lines[0].includes('\t') ? '\t' : ',';
  const head = lines[0].split(sep).map(s => s.trim()), rows = lines.slice(1).map(l => l.split(sep).map(s => s.trim()));
  const series = head.slice(1);
  const W = 720, H = 300, L = 62, R = 18, T = 20, B = 46;
  const values = rows.flatMap(r => r.slice(1).map(num)).filter(Number.isFinite);
  const yMin = Math.min(0, ...values), yMax = Math.max(...values);
  const yt = niceTicks(yMin, yMax), y0 = yt[0], y1 = yt[yt.length - 1];
  const Y = (v: number) => T + (H - T - B) * (1 - (v - y0) / (y1 - y0 || 1));
  const categorical = kind === 'barras' || rows.some(r => !Number.isFinite(num(r[0])));
  const xs = rows.map(r => num(r[0])), xMin = Math.min(...xs), xMax = Math.max(...xs);
  const reversed = !categorical && xs[0] > xs[xs.length - 1];
  const fx = (v: number) => (reversed ? xMax - v : v - xMin) / (xMax - xMin || 1);
  const X = (i: number) => categorical ? L + (W - L - R) * (i + .5) / rows.length : L + (W - L - R) * fx(xs[i]);
  const grid = yt.map(v => `<line x1="${L}" x2="${W - R}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}" class="enc-grid"/><text x="${L - 8}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end" class="enc-tick">${esc(fmt(v))}</text>`).join('');
  const every = Math.max(1, Math.ceil(rows.length / 10));
  const xlabels = categorical ? rows.map((r, i) => i % every ? '' : `<text x="${X(i).toFixed(1)}" y="${H - B + 18}" text-anchor="middle" class="enc-tick">${esc(r[0])}</text>`).join('')
    : niceTicks(xMin, xMax, 6).map(v => { const x = L + (W - L - R) * fx(v); return `<text x="${x.toFixed(1)}" y="${H - B + 18}" text-anchor="middle" class="enc-tick">${esc(fmt(v))}</text>`; }).join('');
  let marks = '';
  series.forEach((name, s) => {
    const color = PALETTE[s % PALETTE.length];
    if (kind === 'barras') {
      const bw = (W - L - R) / rows.length / (series.length + .6);
      marks += rows.map((r, i) => { const v = num(r[s + 1]); if (!Number.isFinite(v)) return ''; const x = X(i) - bw * series.length / 2 + bw * s; return `<rect x="${x.toFixed(1)}" y="${Math.min(Y(v), Y(0)).toFixed(1)}" width="${(bw * .92).toFixed(1)}" height="${Math.abs(Y(0) - Y(v)).toFixed(1)}" fill="${color}"><title>${esc(r[0])} · ${esc(name)}: ${esc(fmt(v))} ${esc(yUnit)}</title></rect>`; }).join('');
    } else {
      const pts = rows.map((r, i) => [X(i), num(r[s + 1]), r[0]] as const).filter(p => Number.isFinite(p[1]));
      const d = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)} ${Y(p[1]).toFixed(1)}`).join(' ');
      if (kind === 'area' && pts.length) marks += `<path d="${d} L${pts[pts.length - 1][0].toFixed(1)} ${Y(Math.max(0, y0)).toFixed(1)} L${pts[0][0].toFixed(1)} ${Y(Math.max(0, y0)).toFixed(1)}Z" fill="${color}" opacity=".22"/>`;
      marks += `<path d="${d}" fill="none" stroke="${color}" stroke-width="2.2"/>` + pts.map(p => `<circle cx="${p[0].toFixed(1)}" cy="${Y(p[1]).toFixed(1)}" r="3.4" fill="${color}"><title>${esc(p[2])} · ${esc(name)}: ${esc(fmt(p[1]))} ${esc(yUnit)}</title></circle>`).join('');
    }
  });
  const legend = series.length > 1 ? `<div class="enc-legend">${series.map((n, s) => `<span><i style="background:${PALETTE[s % PALETTE.length]}"></i>${esc(n)}</span>`).join('')}</div>` : '';
  return `<figure class="enc-component enc-chart">${title ? `<strong class="enc-chart-title">${inline(title)}</strong>` : ''}${legend}<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title || 'Gráfico')}">${grid}<line x1="${L}" x2="${W - R}" y1="${Y(Math.max(0, y0)).toFixed(1)}" y2="${Y(Math.max(0, y0)).toFixed(1)}" class="enc-axis"/>${marks}${xlabels}${yUnit ? `<text x="${L}" y="12" class="enc-tick">${esc(yUnit)}</text>` : ''}${xUnit ? `<text x="${W - R}" y="${H - 6}" text-anchor="end" class="enc-tick">${esc(xUnit)}</text>` : ''}</svg><details class="enc-data-table"><summary>Ver los datos</summary><div class="enc-table"><table><thead><tr>${head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details></figure>`;
}

/* ---------- Línea de tiempo proporcional ---------- */
/** «:::linea-tiempo Título»; líneas «inicio[ / fin] | etiqueta | texto opcional». Fechas civiles o edades (Ma, Ga, ka). */
function timeline(args: string, _ctx: ComponentContext, content: string) {
  const items = content.split('\n').map(l => l.trim()).filter(Boolean).map(l => {
    const [when, label = '', text = ''] = l.replace(/^[-*]\s*/, '').split('|').map(s => s.trim());
    const [a, b] = when.split(/\s+\/\s+/);
    try { return { start: civilYear(a)!, end: b ? civilYear(b)! : null, when, label, text }; } catch { return null; }
  }).filter((x): x is NonNullable<typeof x> => !!x && x.start !== null).sort((x, y) => x.start - y.start);
  if (!items.length) return '';
  const min = Math.min(...items.map(i => i.start)), max = Math.max(...items.map(i => i.end ?? i.start));
  const W = Math.max(900, items.length * 70), lanes: number[] = [], H0 = 34, laneH = 30, RIGHT = 190;
  const X = (y: number) => 30 + (W - 30 - RIGHT) * ((y - min) / (max - min || 1));
  const placed = items.map(it => { const x1 = X(it.start), x2 = it.end ? X(it.end) : x1, need = x2 + Math.max(90, it.label.length * 6.6); let lane = lanes.findIndex(e => e < x1 - 6); if (lane < 0) { lane = lanes.length; lanes.push(0); } lanes[lane] = need; return { ...it, x1, x2, lane }; });
  const H = H0 + lanes.length * laneH + 10;
  const marks = placed.map(p => `<g class="enc-tl-item" tabindex="0"><title>${esc(p.when)} · ${esc(p.label)}${p.text ? ' — ' + esc(p.text.replace(/\[\[[^|\]]+\|?([^\]]*)\]\]/g, '$1')) : ''}</title>${p.end ? `<rect x="${p.x1.toFixed(1)}" y="${H0 + p.lane * laneH - 4}" width="${Math.max(3, p.x2 - p.x1).toFixed(1)}" height="8" rx="4"/>` : `<circle cx="${p.x1.toFixed(1)}" cy="${H0 + p.lane * laneH}" r="5"/>`}<text x="${(p.x1 + 9).toFixed(1)}" y="${H0 + p.lane * laneH + 14}">${esc(p.label)}</text></g>`).join('');
  const ticks = niceTicks(min, max, 8).filter(t => t >= min && t <= max).map(t => { const x = X(t), label = Math.abs(t) >= 1e6 ? geologicalAgeLabel(Number(((1950 - t) / 1e6).toPrecision(3))) : formatYear(Math.round(t) || 1); return `<line x1="${x.toFixed(1)}" x2="${x.toFixed(1)}" y1="14" y2="22" class="enc-axis"/><text x="${x.toFixed(1)}" y="11" text-anchor="middle" class="enc-tick">${esc(label)}</text>`; }).join('');
  const list = `<ol class="enc-timeline">${items.map(i => `<li><time>${inline(i.when)}</time><span><strong>${inline(i.label)}</strong>${i.text ? ' — ' + inline(i.text) : ''}</span></li>`).join('')}</ol>`;
  return `<figure class="enc-component enc-tl">${args ? `<strong class="enc-chart-title">${inline(args)}</strong>` : ''}<div class="enc-scale-scroll"><svg viewBox="0 0 ${W} ${H}" style="min-width:${Math.min(W, 900)}px" role="img" aria-label="${esc(args || 'Línea de tiempo')}"><line x1="30" x2="${W - RIGHT}" y1="22" y2="22" class="enc-axis"/>${ticks}${marks}</svg></div><details class="enc-data-table"><summary>Ver como lista</summary>${list}</details></figure>`;
}

/* ---------- Mapa de localización (se completa al hidratar) ---------- */
/** «:::mapa Título»; líneas «lat, lon | etiqueta» y opcionalmente «países: ESP, FRA» y «encuadre: lonMin, latMin, lonMax, latMax». */
function locator(args: string, _ctx: ComponentContext, content: string) {
  const points: [number, number, string][] = [], countries: string[] = []; let bbox: number[] | null = null;
  for (const raw of content.split('\n').map(l => l.trim()).filter(Boolean)) {
    const m = /^(pa[ií]ses|encuadre)\s*:\s*(.+)$/i.exec(raw);
    if (m) { if (/^pa/i.test(m[1])) countries.push(...m[2].split(',').map(s => s.trim().toUpperCase())); else bbox = m[2].split(',').map(num); continue; }
    const [coords, label = ''] = raw.split('|').map(s => s.trim()); const [lat, lon] = coords.split(',').map(num);
    if (Number.isFinite(lat) && Number.isFinite(lon)) points.push([lat, lon, label]);
  }
  const spec = esc(JSON.stringify({ points, countries, bbox }));
  return `<figure class="enc-component enc-map" data-enc-map="${spec}"><div class="enc-map-canvas"><p class="enc-muted">Cargando mapa…</p></div><figcaption>${args ? inline(args) + ' · ' : ''}Mapa de localización sobre las fronteras actuales (Natural Earth, dominio público).</figcaption></figure>`;
}
export function mapSvg(world: Record<string, string>, spec: { points: [number, number, string][]; countries: string[]; bbox: number[] | null }) {
  const pad = 8;
  let [x0, y0, x1, y1] = spec.bbox ?? [-180, -60, 180, 84];
  if (!spec.bbox && spec.points.length) {
    const lons = spec.points.map(p => p[1]), lats = spec.points.map(p => p[0]);
    const dx = Math.max(24, Math.max(...lons) - Math.min(...lons)), dy = Math.max(16, Math.max(...lats) - Math.min(...lats));
    x0 = Math.max(-180, Math.min(...lons) - dx * .6); x1 = Math.min(180, Math.max(...lons) + dx * .6); y0 = Math.max(-85, Math.min(...lats) - dy * .6); y1 = Math.min(85, Math.max(...lats) + dy * .6);
  }
  const w = x1 - x0, h = y1 - y0, scale = 720 / w, H = Math.round(h * scale);
  const paths = Object.entries(world).map(([code, d]) => `<path d="${d}" class="${spec.countries.includes(code) ? 'enc-map-hi' : ''}"/>`).join('');
  const r = 4 / scale, fs = 11 / scale;
  const pts = spec.points.map(([lat, lon, label]) => `<g><circle cx="${lon}" cy="${-lat}" r="${r}"/>${label ? `<text x="${lon + r * 1.6}" y="${-lat + fs * .35}" font-size="${fs}">${esc(label)}</text>` : ''}</g>`).join('');
  return `<svg viewBox="${x0 - pad / scale} ${-y1 - pad / scale} ${w + 2 * pad / scale} ${h + 2 * pad / scale}" style="aspect-ratio:${720}/${H}" role="img" aria-label="Mapa de localización"><g class="enc-map-land" stroke-width="${.6 / scale}">${paths}</g><g class="enc-map-points">${pts}</g></svg>`;
}

/* ---------- Galería ---------- */
/** «:::galeria Título»; líneas «medios/ruta.jpg | pie». El crédito se toma de medios/creditos.json si existe. */
function gallery(args: string, ctx: ComponentContext, content: string) {
  const items = content.split('\n').map(l => l.trim()).filter(Boolean).map(l => { const [path, caption = ''] = l.split('|').map(s => s.trim()); return { src: /^https?:/.test(path) ? path : ctx.media?.(path), caption, credit: ctx.credit?.(path) }; }).filter(i => i.src);
  if (!items.length) return '';
  return `<figure class="enc-component enc-gallery">${args ? `<strong class="enc-chart-title">${inline(args)}</strong>` : ''}<div>${items.map(i => `<figure><img src="${esc(i.src)}" alt="${esc(i.caption)}" loading="lazy"><figcaption>${inline(i.caption)}${i.credit ? ` <span class="enc-credit">${i.credit}</span>` : ''}</figcaption></figure>`).join('')}</div></figure>`;
}

export const registry: Record<string, Component> = {
  'escala-geologica': scale, 'reloj-geologico': clock, 'curva-temperatura-fanerozoico': phanda, 'atmosfera': atmosphere,
  'grafico': chart, 'linea-tiempo': timeline, 'mapa': locator, 'galeria': gallery
};
/** Bloques de Markdown que llevan datos y se resuelven como componentes. */
export const BLOCK_COMPONENTS = ['grafico', 'linea-tiempo', 'mapa', 'galeria'];
export function component(name: string, args: string, ctx: ComponentContext, content = '') {
  const fn = registry[name];
  try { return fn ? fn(args, ctx, content) : `<p class="enc-muted">[Componente «${esc(name)}» no disponible]</p>`; }
  catch { return `<p class="enc-muted">[No se pudo dibujar «${esc(name)}»]</p>`; }
}
export const componentNames = Object.keys(registry);

/* ---------- Sucesión de mandatos (diagrama de barras temporales) ---------- */
export function successionChart(rows: { id: string; name: string; role: string; start: number; end: number }[], title: string) {
  if (rows.length < 2) return '';
  const min = Math.min(...rows.map(r => r.start)), max = Math.max(...rows.map(r => r.end));
  const roles = [...new Set(rows.map(r => r.role))].slice(0, 8);
  const lanes = roles.map(() => [] as number[]), laneH = 22, W = Math.min(2400, Math.max(900, rows.length * 16)), L = 10;
  const X = (y: number) => L + (W - 2 * L) * ((y - min) / (max - min || 1));
  const placed = rows.map(r => { const role = Math.max(0, roles.indexOf(r.role)), track = lanes[role]; let sub = track.findIndex(e => e < r.start); if (sub < 0) { sub = track.length; track.push(0); } track[sub] = r.end; return { ...r, role, sub }; });
  const offsets: number[] = []; let acc = 30; roles.forEach((_, i) => { offsets[i] = acc; acc += Math.max(1, lanes[i].length) * laneH + 22; });
  const H = acc;
  const bars = placed.filter(p => p.role < roles.length).map(p => { const x = X(p.start), w = Math.max(2, X(p.end + 1) - x), y = offsets[p.role] + p.sub * laneH; return `<g class="enc-succ" data-encyclopedia-entry="${esc(p.id)}" role="link" tabindex="0"><title>${esc(p.name)} · ${esc(formatYear(p.start))} – ${esc(formatYear(p.end))}</title><rect x="${x.toFixed(1)}" y="${y}" width="${w.toFixed(1)}" height="${laneH - 6}" rx="2" fill="${PALETTE[p.role % PALETTE.length]}"/>${w > p.name.length * 6 + 6 ? `<text x="${(x + 4).toFixed(1)}" y="${y + 12}">${esc(p.name)}</text>` : ''}</g>`; }).join('');
  const roleLabels = roles.map((r, i) => `<text x="${L}" y="${offsets[i] - 6}" class="enc-tick">${esc(r)}</text>`).join('');
  const ticks = niceTicks(min, max, 8).filter(t => t >= min && t <= max).map(t => `<text x="${X(t).toFixed(1)}" y="12" text-anchor="middle" class="enc-tick">${esc(formatYear(Math.round(t) || 1))}</text>`).join('');
  return `<figure class="enc-component enc-succession"><strong class="enc-chart-title">${esc(title)}</strong><div class="enc-scale-scroll"><svg viewBox="0 0 ${W} ${H}" style="width:${W}px;max-width:none" role="img" aria-label="${esc(title)}">${ticks}${roleLabels}${bars}</svg></div><figcaption>Cada barra es un mandato registrado en el atlas; pulsa una para abrir la ficha de la persona.</figcaption></figure>`;
}
