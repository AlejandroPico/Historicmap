/* ---------- Árbol evolutivo de los homininos: 39 linajes sobre un eje temporal ---------- */
// «:::componente arbol-homininos [clave]»: barras con el rango de cada linaje (public/data/human-lineages.json),
// agrupadas por género, flujos génicos documentados y enlace a la ficha de cada uno. Los botones cambian la escala
// (logarítmica o lineal) y muestran u ocultan las propuestas discutidas; el SVG se vuelve a dibujar en el sitio.
import catalogue from '../../public/data/human-lineages.json' with { type: 'json' };
import { tx, language } from '../i18n';
import { esc } from './markdown';

type Taxon = { key: string; name: string; group: string; color: string; oldestKa: number; youngestKa: number; classification: string };
const taxa = catalogue.taxa as Taxon[];
const REFERENCE = new Set(['especie de referencia', 'linaje genético']);
export const isReference = (t: Taxon) => REFERENCE.has(t.classification);
/** Claves de los 39 linajes, del más antiguo al más reciente. */
export const lineageKeysByAge = () => [...taxa].sort((a, b) => b.oldestKa - a.oldestKa || b.youngestKa - a.youngestKa).map(t => t.key);

function groups(): [string, string][] {
  return [
    ['early', tx('arbolHomininos.grupoPrimeros')], ['australopith', tx('arbolHomininos.grupoAustralopitecos')], ['paranthropus', tx('arbolHomininos.grupoParantropos')],
    ['early-homo', tx('arbolHomininos.grupoHomoTemprano')], ['erectus', tx('arbolHomininos.grupoErectus')], ['archaic-homo', tx('arbolHomininos.grupoArcaicos')],
    ['island', tx('arbolHomininos.grupoIslas')], ['late', tx('arbolHomininos.grupoTardios')], ['unassigned', tx('arbolHomininos.grupoDiscutidas')]
  ];
}
// Los linajes tardíos y los insulares se reúnen en dos bloques; las propuestas discutidas van al final.
const blockOf = (t: Taxon) => !isReference(t) && t.group !== 'early-homo' && t.group !== 'australopith' ? 'unassigned'
  : ['flores', 'luzon', 'naledi'].includes(t.group) ? 'island' : ['neanderthal', 'denisovan', 'sapiens'].includes(t.group) ? 'late' : t.group;

const W = 760, LEFT = 236, RIGHT = 744, ROW = 17, TOP = 40, MAX_KA = 7200;
const LOG_TICKS = [7000, 4000, 2000, 1000, 500, 300, 100, 50, 10, 0];
const LIN_TICKS = [7000, 6000, 5000, 4000, 3000, 2000, 1000, 0];
function xOf(ka: number, log: boolean) {
  const f = log ? (Math.log10(MAX_KA + 10) - Math.log10(Math.max(0, ka) + 10)) / (Math.log10(MAX_KA + 10) - 1) : (MAX_KA - ka) / MAX_KA;
  return LEFT + f * (RIGHT - LEFT);
}
const fmtKa = (ka: number) => ka >= 1000 ? tx('arbolHomininos.ma', { v: (ka / 1000).toLocaleString(language, { maximumFractionDigits: 2 }) }) : ka === 0 ? tx('arbolHomininos.hoy') : tx('arbolHomininos.ka', { v: ka.toLocaleString(language) });

/** Flujos génicos documentados por ADN antiguo: de, a, edad aproximada en ka, clave de la etiqueta. */
function flows(): [string, string, number, string][] {
  return [
    ['neanderthal', 'sapiens', 50, tx('arbolHomininos.flujoNeandertalSapiens')],
    ['denisovan', 'sapiens', 45, tx('arbolHomininos.flujoDenisovanoSapiens')],
    ['neanderthal', 'denisovan', 90, tx('arbolHomininos.flujoDenny')],
    ['sapiens', 'neanderthal', 250, tx('arbolHomininos.flujoSapiensNeandertal')]
  ];
}

export function homininTreeSvg(opts: { log: boolean; all: boolean; focus?: string }) {
  const rows: (Taxon | string)[] = [];
  for (const [g, label] of groups()) {
    const list = taxa.filter(t => blockOf(t) === g && (opts.all || isReference(t))).sort((a, b) => b.oldestKa - a.oldestKa || b.youngestKa - a.youngestKa);
    if (list.length) rows.push(label, ...list);
  }
  const H = TOP + rows.length * ROW + 28, yOf = new Map<string, number>();
  const ticks = (opts.log ? LOG_TICKS : LIN_TICKS).map(ka => { const x = xOf(ka, opts.log); return `<line x1="${x}" y1="${TOP - 8}" x2="${x}" y2="${H - 24}" class="htree-grid"/><text x="${x}" y="${TOP - 14}" class="htree-tick" text-anchor="middle">${esc(fmtKa(ka))}</text>`; }).join('');
  const body = rows.map((r, i) => {
    const y = TOP + i * ROW;
    if (typeof r === 'string') return `<text x="8" y="${y + 13}" class="htree-group">${esc(r)}</text><line x1="8" y1="${y + 16}" x2="${RIGHT}" y2="${y + 16}" class="htree-rule"/>`;
    yOf.set(r.key, y + ROW / 2);
    const x1 = xOf(r.oldestKa, opts.log), x2 = Math.max(xOf(r.youngestKa, opts.log), x1 + 4), ref = isReference(r);
    const tip = `${r.name} · ${fmtKa(r.oldestKa)} – ${fmtKa(r.youngestKa)} · ${r.classification}`;
    return `<g class="htree-row${opts.focus === r.key ? ' is-focus' : ''}${ref ? '' : ' is-alt'}" data-encyclopedia-entry="hominin-${esc(r.key)}" role="link" tabindex="0" aria-label="${esc(tip)}"><title>${esc(tip)}</title>
<rect x="0" y="${y}" width="${W}" height="${ROW}" class="htree-hit"/><text x="${LEFT - 8}" y="${y + 12.5}" class="htree-name" text-anchor="end">${esc(r.name)}</text>
<rect x="${x1}" y="${y + 3.5}" width="${x2 - x1}" height="${ROW - 7}" rx="4" fill="${esc(r.color)}" class="htree-bar"/></g>`;
  }).join('');
  const arrows = !opts.log ? '' : flows().filter(([a, b]) => yOf.has(a) && yOf.has(b)).map(([a, b, ka, label]) => {
    const x = xOf(ka, opts.log), y1 = yOf.get(a)! + (yOf.get(b)! > yOf.get(a)! ? 4 : -4), y2 = yOf.get(b)! + (yOf.get(b)! > yOf.get(a)! ? -5 : 5);
    const d = `M${x},${y1} L${x},${y2}`;
    return `<g class="htree-flow-g"><title>${esc(label)}</title><path d="${d}" class="htree-flow-under"/><path d="${d}" class="htree-flow" marker-end="url(#htree-head)"/><circle cx="${x}" cy="${y1}" r="2.6" class="htree-head"/></g>`;
  }).join('');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(tx('arbolHomininos.titulo'))}"><defs><marker id="htree-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="htree-head"/></marker></defs>
${ticks}${body}${arrows}<text x="${RIGHT}" y="${H - 6}" class="htree-tick" text-anchor="end">${esc(opts.log ? tx('arbolHomininos.notaLog') : tx('arbolHomininos.notaLineal'))}</text></svg>`;
}

/** Franja compacta para las fichas de especie: sitúa el linaje en el eje de 7 Ma a hoy frente a los demás (en gris). */
export function homininStrip(key: string) {
  const t = taxa.find(x => x.key === key); if (!t) return '';
  const H = 62, y = 24, ticks = LOG_TICKS.filter(k => k !== 4000).map(ka => `<text x="${xOf(ka, true)}" y="14" class="htree-tick" text-anchor="middle">${esc(fmtKa(ka))}</text>`).join('');
  const others = taxa.filter(x => x.key !== key).map(x => { const x1 = xOf(x.oldestKa, true), x2 = Math.max(xOf(x.youngestKa, true), x1 + 3); return `<rect x="${x1}" y="${y + 4}" width="${x2 - x1}" height="6" rx="3" class="hstrip-other"/>`; }).join('');
  const x1 = xOf(t.oldestKa, true), x2 = Math.max(xOf(t.youngestKa, true), x1 + 5);
  return `<figure class="enc-component enc-hstrip"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(`${t.name} · ${fmtKa(t.oldestKa)} – ${fmtKa(t.youngestKa)}`)}">${ticks}<line x1="${LEFT}" y1="${y + 7}" x2="${RIGHT}" y2="${y + 7}" class="htree-rule"/>${others}<rect x="${x1}" y="${y}" width="${x2 - x1}" height="14" rx="5" fill="${esc(t.color)}" class="hstrip-this"/><text x="${LEFT - 8}" y="${y + 11}" class="htree-name" text-anchor="end">${esc(t.name)}</text><text x="${LEFT - 8}" y="${y + 28}" class="htree-tick" text-anchor="end">${esc(`${fmtKa(t.oldestKa)} – ${fmtKa(t.youngestKa)}`)}</text></svg><figcaption>${esc(tx('arbolHomininos.franja'))}</figcaption></figure>`;
}

export function homininTree(args: string) {
  const focus = args.trim() || undefined;
  return `<figure class="enc-component enc-htree" data-log="true" data-all="true"${focus ? ` data-focus="${esc(focus)}"` : ''}><strong class="enc-chart-title">${esc(tx('arbolHomininos.titulo'))}</strong>
<div class="htree-controls"><button type="button" data-htree="log" aria-pressed="true">${esc(tx('arbolHomininos.escalaLog'))}</button><button type="button" data-htree="lin" aria-pressed="false">${esc(tx('arbolHomininos.escalaLineal'))}</button><button type="button" data-htree="all" aria-pressed="true">${esc(tx('arbolHomininos.verDiscutidas'))}</button></div>
<div class="htree-canvas">${homininTreeSvg({ log: true, all: true, focus })}</div>
<figcaption>${esc(tx('arbolHomininos.leyenda'))}<span class="htree-key"><i class="htree-swatch"></i>${esc(tx('arbolHomininos.leyendaFlujo'))}</span></figcaption></figure>`;
}

/** Botones del árbol; devuelve true si el clic era suyo. */
export function handleHomininTreeClick(target: Element) {
  const button = target.closest<HTMLElement>('[data-htree]'); if (!button) return false;
  const fig = button.closest<HTMLElement>('.enc-htree'); if (!fig) return false;
  const what = button.dataset.htree;
  if (what === 'all') fig.dataset.all = String(fig.dataset.all !== 'true'); else fig.dataset.log = String(what === 'log');
  const log = fig.dataset.log === 'true', all = fig.dataset.all === 'true';
  fig.querySelector('[data-htree="log"]')?.setAttribute('aria-pressed', String(log));
  fig.querySelector('[data-htree="lin"]')?.setAttribute('aria-pressed', String(!log));
  fig.querySelector('[data-htree="all"]')?.setAttribute('aria-pressed', String(all));
  fig.querySelector('.htree-canvas')!.innerHTML = homininTreeSvg({ log, all, focus: fig.dataset.focus });
  return true;
}
