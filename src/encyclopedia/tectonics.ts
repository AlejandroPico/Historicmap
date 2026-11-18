/* ---------- Tectónica de placas: cortes interactivos de los cinco tipos de límite ---------- */
// «:::componente tectonica-placas [dorsal|subduccion|colision|transformante|punto-caliente]».
// Todo se dibuja a la vez; el modo activo se elige con botones (data-tect-mode) y CSS oculta el resto.
import { tx } from '../i18n';
import { esc } from './markdown';

export const TECTONIC_MODES = ['dorsal', 'subduccion', 'colision', 'transformante', 'punto-caliente'] as const;
type Mode = typeof TECTONIC_MODES[number];

const label = (x: number, y: number, text: string, cls = '', anchor = 'start') => `<text x="${x}" y="${y}" class="tect-label ${cls}" text-anchor="${anchor}">${esc(text)}</text>`;
const arrow = (d: string, cls = '') => `<path d="${d}" class="tect-arrow ${cls}" marker-end="url(#tect-head)"/>`;
const flow = (d: string) => `<path d="${d}" class="tect-flow" marker-end="url(#tect-head-soft)"/>`;
const quakes = (pts: [number, number][]) => pts.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3.2" class="tect-quake"/>`).join('');
const mirror = (pts: string) => pts.split(' ').map(p => { const [x, y] = p.split(',').map(Number); return `${760 - x},${y}`; }).join(' ');

function names(mode: Mode) {
  return {
    dorsal: tx('tectonica.dorsal'), subduccion: tx('tectonica.subduccion'), colision: tx('tectonica.colision'),
    transformante: tx('tectonica.transformante'), 'punto-caliente': tx('tectonica.puntoCaliente')
  }[mode];
}
function captions(mode: Mode) {
  return {
    dorsal: [tx('tectonica.dorsalTexto'), tx('tectonica.dorsalEjemplos')],
    subduccion: [tx('tectonica.subduccionTexto'), tx('tectonica.subduccionEjemplos')],
    colision: [tx('tectonica.colisionTexto'), tx('tectonica.colisionEjemplos')],
    transformante: [tx('tectonica.transformanteTexto'), tx('tectonica.transformanteEjemplos')],
    'punto-caliente': [tx('tectonica.puntoCalienteTexto'), tx('tectonica.puntoCalienteEjemplos')]
  }[mode];
}

const defs = `<defs>
<linearGradient id="tect-asth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8612f"/><stop offset="1" stop-color="#6e2b17"/></linearGradient>
<linearGradient id="tect-magma" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff5a1f" stop-opacity=".95"/><stop offset="1" stop-color="#ffc35a" stop-opacity=".9"/></linearGradient>
<linearGradient id="tect-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f86b5"/><stop offset="1" stop-color="#1d4a6e"/></linearGradient>
<marker id="tect-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="tect-head"/></marker>
<marker id="tect-head-soft" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="tect-head-soft"/></marker>
</defs>`;
const mantle = `<rect x="0" y="150" width="760" height="190" fill="url(#tect-asth)"/>`;
const sea = (y = 40) => `<line x1="0" y1="${y}" x2="760" y2="${y}" class="tect-sea"/>`;

function dorsal() {
  const crust = '0,128 372,94 372,106 0,142', litho = '0,142 372,106 374,120 0,215';
  const stripes = [60, 36, 24, 44, 20, 30, 50].reduce<{ x: number; w: number; dark: boolean }[]>((acc, w, i) => { const x = (acc.at(-1)?.x ?? 380) - w; acc.push({ x, w, dark: i % 2 === 0 }); return acc; }, []);
  const band = stripes.map(s => `<rect x="${s.x}" y="6" width="${s.w}" height="14" class="${s.dark ? 'tect-mag-n' : 'tect-mag-r'}"/><rect x="${760 - s.x - s.w}" y="6" width="${s.w}" height="14" class="${s.dark ? 'tect-mag-n' : 'tect-mag-r'}"/>`).join('');
  return `${mantle}<rect x="0" y="40" width="760" height="110" fill="url(#tect-water)"/>${sea()}
<polygon points="0,215 374,120 386,120 760,215 760,340 0,340" fill="url(#tect-asth)"/>
<path d="M326,340 C350,250 366,170 374,104 L386,104 C394,170 410,250 434,340 Z" fill="url(#tect-magma)" class="tect-pulse"/>
<g class="tect-slide-l"><polygon points="${litho}" class="tect-litho"/><polygon points="${crust}" class="tect-ocrust"/></g>
<g class="tect-slide-r"><polygon points="${mirror(litho)}" class="tect-litho"/><polygon points="${mirror(crust)}" class="tect-ocrust"/></g>
<rect x="0" y="4" width="760" height="18" class="tect-band"/>${band}<rect x="378" y="4" width="4" height="18" class="tect-mag-n"/>
${flow('M380,322 C380,250 310,212 170,224')}${flow('M380,322 C380,250 450,212 590,224')}
${arrow('M332,66 L210,66')}${arrow('M428,66 L550,66')}
${label(380, 88, tx('tectonica.ejeDorsal'), 'tect-on-water', 'middle')}${label(12, 34, tx('tectonica.anomaliasMagneticas'), 'tect-small')}
${label(150, 58, tx('tectonica.placaOceanica'), 'tect-on-water')}${label(610, 58, tx('tectonica.placaOceanica'), 'tect-on-water', 'end')}
${label(14, 192, tx('tectonica.litosfera'), 'tect-on-rock')}${label(14, 322, tx('tectonica.astenosfera'), 'tect-on-rock')}
${label(446, 290, tx('tectonica.fusionDescompresion'), 'tect-on-rock')}`;
}

function subduccion() {
  const slab = 'M0,125 L360,125 Q420,150 470,190 L700,340 L620,340 L432,214 Q382,185 330,185 L0,185 Z';
  const crust = 'M0,125 L360,125 Q420,150 470,190 L700,340 L684,340 L462,200 Q414,163 358,138 L0,138 Z';
  const cont = '398,150 470,60 500,40 544,36 560,14 576,36 760,44 760,150 432,162';
  const contMantle = '432,162 760,150 760,222 528,224 470,190';
  return `${mantle}<polygon points="0,40 504,40 470,60 398,150 360,125 0,125" fill="url(#tect-water)"/>${sea()}
<path d="${slab}" class="tect-litho"/><path d="${crust}" class="tect-ocrust"/>
<polygon points="${contMantle}" class="tect-litho tect-litho-cont"/><polygon points="${cont}" class="tect-ccrust"/>
<ellipse cx="566" cy="246" rx="34" ry="17" fill="url(#tect-magma)" class="tect-pulse"/>
<path d="M562,232 C548,180 574,120 560,34" class="tect-rise"/>
${quakes([[424, 160], [462, 192], [500, 214], [540, 240], [584, 268], [628, 296], [668, 322]])}
${arrow('M120,104 L262,104')}${flow('M486,214 L628,306')}
${label(60, 92, tx('tectonica.placaOceanica'), 'tect-on-water')}${label(394, 114, tx('tectonica.fosa'), 'tect-on-water', 'end')}
${label(752, 108, tx('tectonica.placaContinental'), 'tect-on-crust', 'end')}${label(590, 26, tx('tectonica.arcoVolcanico'), 'tect-strong')}
${label(606, 252, tx('tectonica.fusionHidratacion'), 'tect-on-rock')}${label(470, 330, tx('tectonica.wadatiBenioff'), 'tect-on-rock', 'end')}
${label(14, 168, tx('tectonica.litosfera'), 'tect-on-rock')}${label(14, 322, tx('tectonica.astenosfera'), 'tect-on-rock')}`;
}

function colision() {
  const left = '0,60 250,58 320,40 360,8 386,5 400,120 430,236 300,152 0,140';
  const right = '386,5 400,4 440,14 500,44 760,58 760,140 560,150 470,230 430,236 400,120';
  const leftMantle = '0,140 300,152 430,236 524,302 474,322 262,216 0,210', rightMantle = '760,140 760,212 602,216 506,282 470,230 560,150';
  return `${mantle}<rect x="0" y="0" width="760" height="150" class="tect-sky"/>
<polygon points="${leftMantle}" class="tect-litho"/><polygon points="${rightMantle}" class="tect-litho tect-litho-cont"/>
<polygon points="${left}" class="tect-ccrust"/><polygon points="${right}" class="tect-ccrust tect-ccrust-b"/>
<path d="M386,6 L400,120 L430,236" class="tect-suture"/>
${quakes([[372, 60], [396, 100], [410, 150], [300, 120], [460, 110], [440, 200]])}
${arrow('M30,26 L160,26')}${arrow('M730,26 L600,26')}${flow('M440,250 L520,306')}
${label(40, 104, tx('tectonica.placaContinental'), 'tect-on-crust')}${label(720, 104, tx('tectonica.placaContinental'), 'tect-on-crust', 'end')}
${label(330, 30, tx('tectonica.cordillera'), 'tect-strong', 'end')}${label(436, 186, tx('tectonica.sutura'), 'tect-on-crust')}
${label(520, 214, tx('tectonica.raizCortical'), 'tect-on-rock')}${label(14, 322, tx('tectonica.astenosfera'), 'tect-on-rock')}`;
}

function transformante() {
  const iso = (x: number, y1: number, y2: number) => [-48, -28, 28, 48].map(d => `<line x1="${x + d}" y1="${y1}" x2="${x + d}" y2="${y2}" class="tect-iso"/>`).join('');
  return `<rect x="0" y="0" width="760" height="340" class="tect-floor"/>
${iso(250, 14, 168)}${iso(510, 172, 326)}
<line x1="0" y1="170" x2="250" y2="170" class="tect-fracture"/><line x1="510" y1="170" x2="760" y2="170" class="tect-fracture"/>
<line x1="250" y1="170" x2="510" y2="170" class="tect-transform"/>
<path d="M246,14 L246,170 M254,14 L254,170" class="tect-ridge"/><path d="M506,170 L506,326 M514,170 L514,326" class="tect-ridge"/>
${quakes([[280, 170], [322, 170], [366, 170], [410, 170], [452, 170], [492, 170]])}
${arrow('M170,96 L70,96')}${arrow('M330,132 L440,132')}${arrow('M440,212 L330,212')}${arrow('M590,252 L690,252')}
${arrow('M190,150 L120,150', 'tect-arrow-faint')}${arrow('M190,192 L120,192', 'tect-arrow-faint')}${arrow('M570,150 L640,150', 'tect-arrow-faint')}${arrow('M570,192 L640,192', 'tect-arrow-faint')}
${label(380, 162, tx('tectonica.fallaActiva'), 'tect-strong', 'middle')}${label(10, 232, tx('tectonica.zonaFractura'), 'tect-small')}${label(750, 120, tx('tectonica.zonaFractura'), 'tect-small', 'end')}
${label(262, 30, tx('tectonica.ejeDorsal'), 'tect-small')}${label(498, 318, tx('tectonica.ejeDorsal'), 'tect-small', 'end')}
${label(10, 330, tx('tectonica.vistaEnPlanta'), 'tect-small')}`;
}

function puntoCaliente() {
  const islands: [number, number, number][] = [[580, 18, 0], [496, 24, 1], [412, 30, 3], [328, 36, 5], [226, 46, 28], [112, 78, 47]];
  const cones = islands.map(([x, peak, age]) => `<path d="M${x - 46},122 Q${x - 16},${peak + 8} ${x},${peak} Q${x + 16},${peak + 8} ${x + 46},122 Z" class="${age ? 'tect-old' : 'tect-active'}"/>${label(x, peak - 7, tx('tectonica.edadMa', { v: age }), age ? 'tect-small tect-on-water' : 'tect-strong', 'middle')}`).join('');
  return `${mantle}<rect x="0" y="40" width="760" height="82" fill="url(#tect-water)"/>${sea()}
<path d="M532,340 C556,280 562,240 568,192 L592,192 C598,240 604,280 628,340 Z" fill="url(#tect-magma)" class="tect-pulse"/>
<polygon points="0,120 760,120 760,190 0,190" class="tect-litho"/><polygon points="0,120 760,120 760,132 0,132" class="tect-ocrust"/>
<path d="M580,192 L580,126" class="tect-rise"/>${cones}
${arrow('M360,162 L220,162', 'tect-arrow-light')}
${label(632, 300, tx('tectonica.plumaManto'), 'tect-on-rock')}${label(636, 104, tx('tectonica.volcanActivo'), 'tect-on-water')}
${label(160, 182, tx('tectonica.movimientoPlaca'), 'tect-on-rock')}${label(14, 322, tx('tectonica.astenosfera'), 'tect-on-rock')}`;
}

const DRAW: Record<Mode, () => string> = { dorsal, subduccion, colision, transformante, 'punto-caliente': puntoCaliente };

export function tectonicPlates(args: string) {
  const first = (TECTONIC_MODES as readonly string[]).includes(args.trim()) ? args.trim() as Mode : 'dorsal';
  const buttons = TECTONIC_MODES.map(m => `<button type="button" data-tect-mode="${m}" aria-pressed="${m === first}">${esc(names(m))}</button>`).join('');
  const scenes = TECTONIC_MODES.map(m => `<g data-tect="${m}">${DRAW[m]()}</g>`).join('');
  const text = TECTONIC_MODES.map(m => { const [what, where] = captions(m); return `<div data-tect-caption="${m}"><p>${esc(what)}</p><p class="tect-examples">${esc(where)}</p></div>`; }).join('');
  return `<figure class="enc-component enc-tectonics" data-mode="${first}"><strong class="enc-chart-title">${esc(tx('tectonica.titulo'))}</strong>
<div class="tect-modes" role="group" aria-label="${esc(tx('tectonica.tiposDeLimite'))}">${buttons}</div>
<svg viewBox="0 0 760 340" role="img" aria-label="${esc(tx('tectonica.titulo'))}">${defs}${scenes}</svg>
<figcaption>${text}<span class="tect-note">${esc(tx('tectonica.nota'))}</span></figcaption></figure>`;
}

/** Cambia el modo del corte; devuelve true si el clic era suyo. */
export function handleTectonicsClick(target: Element) {
  const button = target.closest<HTMLElement>('[data-tect-mode]'); if (!button) return false;
  const fig = button.closest<HTMLElement>('.enc-tectonics'); if (!fig) return false;
  fig.dataset.mode = button.dataset.tectMode;
  fig.querySelectorAll('[data-tect-mode]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  return true;
}
