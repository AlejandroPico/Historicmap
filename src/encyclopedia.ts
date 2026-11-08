// Lector de la enciclopedia (P01): índice por ramas, búsqueda unificada, composición jerárquica,
// ficha lateral, historial, panorama por fecha y fichas generadas de dirigentes y entidades.
// Fuentes de contenido, por prioridad: páginas de enciclopedia/ → contenido heredado de Tierra/ → fichas generadas.
import { encyclopediaArticle, encyclopediaForYear, encyclopediaReferenceYear, searchEncyclopedia, encyclopediaSources, curatedArticles, curatedGroups, reviewedEvents, type EncyclopediaArticle } from './encyclopedia-model';
import { geologicalUnits, humanUnits, humanChronologySources, geologicalAt, humanAt, rankLabels, geologicalRangeLabel, geologicalAgeLabel, type GeologicalUnit } from './earth-chronology';
import { scientificDiagram } from './encyclopedia-diagrams';
import { humanDiagram, handleHumanInput } from './human-encyclopedia';
import { humanPhoto, humanKnowledge } from './human-knowledge';
import { planetRecordFor, planetValue, planetSources } from './planet';
import { formatYear } from './time';
import { formatEventDate } from './dates';
import media from '../Tierra/Precambrico/medios.json' with { type: 'json' };
import phanerozoicMedia from '../Tierra/Fanerozoico/medios.json' with { type: 'json' };
import { render as renderMarkdown, esc, type Heading } from './encyclopedia/markdown';
import { loadIndex, loadSource, loadPerson, loadEntity, loadCentury, loadNames, loadWorld, mediaUrl, mediaCredit, activeIn, dateYearOf, normalizeText, type IndexPage, type EncyclopediaIndexFile } from './encyclopedia/store';
import { component, scaleView, mapSvg, successionChart } from './encyclopedia/components';
import { handleSpeechChange, handleSpeechClick, playerMarkup, resetSpeech, stopSpeech } from './encyclopedia/speech';

interface Source { title: string; url: string }
interface Page {
  id: string; kind: string; title: string; summary: string; year: number;
  html: string; headings: Heading[]; infobox: [string, string][]; breadcrumb: { id: string; title: string }[];
  children: { id: string; title: string; summary: string; meta: string }[]; related: string[]; sources: Source[];
  top: string; note?: string; legacy?: EncyclopediaArticle; portrait?: string;
}

let dialog: HTMLDialogElement, history: string[] = [], cursor = -1, consultedYear = 2026, onMap: (year: number) => void, returnFocus: HTMLElement;
let index: EncyclopediaIndexFile | null = null, renderToken = 0, replacedBy = new Map<string, string>();
const isReplaced = (id: string) => replacedBy.has(id);
const byId = (id: string) => document.getElementById(id)!;
const BASE = import.meta.env.BASE_URL;
const pageById = (id: string) => index?.paginas.find(p => p.id === id);
const unitById = (id: string) => geologicalUnits.find(u => u.id === id);
const personKey = (id: string) => id.slice('persona-'.length);
const entityKey = (id: string) => id.slice('entidad-'.length);
const dateLabel = (d: string, precision = 9) => { try { return formatEventDate(d, precision >= 11 ? 11 : 9); } catch { return d; } };
const yearLabel = (y: number | null | undefined) => y === null || y === undefined ? '—' : formatYear(y);

/** Título conocido para un identificador, sin cargar la página. */
function knownTitle(id: string) {
  const p = pageById(id); if (p) return p.titulo;
  if (id.startsWith('geo-')) return unitById(id.slice(4))?.name;
  if (id.startsWith('fecha-')) { const y = Number(id.slice(6)); return (y <= -1000000 ? 'La Tierra hace ' : 'El mundo en ') + formatYear(y); }
  return encyclopediaArticle(id)?.title;
}
const renderOptions = (extra = {}) => ({ title: knownTitle, media: mediaUrl, credit: mediaCredit, component: (name: string, args: string, content = '') => component(name, args, { year: consultedYear, media: mediaUrl, credit: mediaCredit }, content), ...extra });

/* ---------- Esquemas heredados (conservados de las versiones 0.53–0.56) ---------- */
function legacyDiagram(a: EncyclopediaArticle) {
  const human = humanDiagram(a); if (human) return human;
  const scientific = scientificDiagram(a); if (scientific) return scientific;
  if (!['interior', 'impact', 'albedo', 'photosynthesis'].includes(a.diagram)) return '';
  const interior = a.diagram === 'interior', impact = a.diagram === 'impact', albedo = a.diagram === 'albedo';
  const core = interior ? `<circle cx="260" cy="130" r="105" fill="#9b6943"/><circle cx="260" cy="130" r="91" fill="#b48a55"/><circle cx="260" cy="130" r="56" fill="#c6683b"/><circle cx="260" cy="130" r="28" fill="#efbd70"/><text x="410" y="74">Corteza</text><text x="410" y="114">Manto</text><text x="410" y="154">Núcleo externo</text><text x="410" y="194">Núcleo interno</text><path d="M350 65H400M330 105H400M300 145H400M270 185H400"/>`
    : impact ? `<circle cx="280" cy="130" r="80" fill="#d1783d"/><g class="impact-body"><circle cx="90" cy="105" r="32" fill="#8b8178"/><path d="M30 105H48M8 118H42M20 90H42"/></g><ellipse cx="290" cy="130" rx="145" ry="28" fill="none" stroke-dasharray="4 9"/><text x="460" y="120">Colisión</text><text x="460" y="154">Material expulsado</text><text x="460" y="188">Reorganización</text>`
    : `<rect x="35" y="70" width="170" height="115" rx="4" fill="#3f7581"/><rect x="245" y="70" width="170" height="115" rx="4" fill="#8e7959"/><rect x="455" y="70" width="170" height="115" rx="4" fill="#60765c"/><path d="M210 126H239M420 126H449"/><text x="120" y="125" text-anchor="middle">${albedo ? 'Luz solar' : 'Luz y agua'}</text><text x="330" y="125" text-anchor="middle">${albedo ? 'Reflexión' : 'Microorganismos'}</text><text x="540" y="125" text-anchor="middle">${albedo ? 'Absorción' : 'Materia y gases'}</text>`;
  return `<figure class="encyclopedia-diagram" data-diagram="${a.diagram}"><svg viewBox="0 0 660 255" role="img" aria-label="Esquema didáctico: ${esc(a.title)}">${core}</svg><figcaption>Esquema propio, sin escala.</figcaption>${albedo ? '<label>Fracción reflejada <input id="encyclopedia-lab" type="range" min="0" max="90" value="30" aria-label="Porcentaje de luz reflejada"></label><output id="encyclopedia-lab-output">70 % de luz absorbida</output><progress id="encyclopedia-energy" max="100" value="70"></progress>' : impact ? '<label>Recorrer las etapas <input id="encyclopedia-lab" type="range" min="0" max="100" value="0" aria-label="Etapa del esquema de impacto"></label><output id="encyclopedia-lab-output">Acercamiento · esquema sin escala temporal</output>' : ''}</figure>`;
}
function planetFacts(year: number) {
  if (year >= -10000) return '';
  const rows = (['meanTemperature', 'solarDay', 'carbonDioxide'] as const).map(field => {
    const r = planetRecordFor(field, year); if (!r) return '';
    const label = field === 'meanTemperature' ? 'Temperatura global' : field === 'solarDay' ? 'Día solar' : 'CO₂ atmosférico';
    const kind = r.evidence === 'illustrative-scenario' ? 'Escenario audiovisual' : r.evidence === 'model' ? 'Reconstrucción publicada' : 'Estimación publicada';
    return `<div><span>${label}</span><strong>${esc(planetValue(r))}</strong><a href="${planetSources[r.sourceId].url}" target="_blank" rel="noopener">${kind} ↗</a></div>`;
  }).join('');
  return rows ? `<aside class="encyclopedia-facts" aria-label="Indicadores de referencia"><small>Indicadores del planeta · ${formatYear(year)}</small>${rows}</aside>` : '';
}
function legacyImage(a: EncyclopediaArticle) {
  const image = [...phanerozoicMedia.images, ...media.images].find(m => m.articleIds.includes(a.themeId ?? a.id));
  return image ? `<figure class="encyclopedia-photo"><img src="${BASE + image.file}" alt="${esc(image.alt)}" loading="lazy"><figcaption>${esc(image.caption)} <a href="${image.page}" target="_blank" rel="noopener">${esc(image.credit)} ↗</a></figcaption></figure>` : '';
}
function legacySources(a: EncyclopediaArticle): Source[] {
  return a.sourceIds.map(id => encyclopediaSources[id as keyof typeof encyclopediaSources] as { name?: string; title?: string; url: string } | undefined).filter((s): s is { name?: string; title?: string; url: string } => !!s).map(s => ({ title: s.name ?? s.title ?? s.url, url: s.url }));
}
function legacyBody(a: EncyclopediaArticle, year: number) {
  const headings: Heading[] = [];
  const html = a.sections.map((s, i) => { const anchor = 'encyclopedia-section-' + i; headings.push({ level: 2, text: s.title, anchor }); return `<section id="${anchor}"><h2>${esc(s.title)}</h2><p>${esc(s.text)}</p></section>${i === 0 ? legacyDiagram({ ...a, year }) : ''}`; }).join('');
  const video = a.id === 'theia' ? `<section class="encyclopedia-video"><h2>Simular una colisión</h2><p>NASA: visualización de una simulación del impacto formador de la Luna.</p><button data-video-id="kRlhlCWplqk">Cargar animación de NASA</button><div id="encyclopedia-video-frame"></div><a href="https://www.nasa.gov/solar-system/nasa-finds-moon-may-have-formed-in-hours-instead-of-years/" target="_blank" rel="noopener">Contexto científico de la simulación ↗</a></section>`
    : a.id.startsWith('video-') ? `<section class="encyclopedia-video"><h2>Archivo de la referencia inicial</h2><a href="https://www.youtube.com/watch?v=Q1OreyX0-fw&t=${a.videoStart ?? 0}s" target="_blank" rel="noopener">Consultar segmento original ↗</a></section>` : '';
  return { html: html + video, headings };
}

/* ---------- Constructores de páginas ---------- */
/** Artículos temáticos que cuelgan de una página (campo «padre»), en su orden. */
function topicsOf(id: string) {
  return (index?.paginas ?? []).filter(c => c.padre === id).sort((a, b) => (a.orden ?? 1e9) - (b.orden ?? 1e9) || a.titulo.localeCompare(b.titulo, 'es'))
    .map(c => ({ id: c.id, title: c.titulo, summary: c.resumen, meta: c.inicio !== null && !c.id.startsWith('geo-') ? (Math.abs(c.inicio) >= 1e6 ? `${yearLabel(c.inicio)} — ${yearLabel(c.fin)}` : '') : '' }));
}
/** Elementos interactivos de un artículo heredado que se conservan al sustituir su texto. */
function legacyExtras(a: EncyclopediaArticle, year: number) {
  const diagram = legacyDiagram({ ...a, year });
  const video = a.id === 'theia' ? `<section class="encyclopedia-video"><h2 id="enc-simulacion">Simular una colisión</h2><p>NASA: visualización de una simulación del impacto formador de la Luna.</p><button data-video-id="kRlhlCWplqk">Cargar animación de NASA</button><div id="encyclopedia-video-frame"></div><a href="https://www.nasa.gov/solar-system/nasa-finds-moon-may-have-formed-in-hours-instead-of-years/" target="_blank" rel="noopener">Contexto científico de la simulación ↗</a></section>` : '';
  return { top: humanPhoto(a.themeId ?? a.id) + legacyImage(a), html: diagram + video };
}
function unitChildren(u: GeologicalUnit) { return geologicalUnits.filter(c => c.parent === u.id).sort((a, b) => b.oldestMa - a.oldestMa); }
function unitTrail(u: GeologicalUnit) { const out: GeologicalUnit[] = []; let p = u.parent ? unitById(u.parent) : undefined; while (p) { out.unshift(p); p = p.parent ? unitById(p.parent) : undefined; } return out; }
const duration = (u: GeologicalUnit) => geologicalAgeLabel(Math.max(0, u.oldestMa - u.youngestMa));
const RANK_PLURAL: Record<string, string> = { eon: 'eones', era: 'eras', period: 'periodos', subperiod: 'subperiodos', epoch: 'épocas', age: 'edades', group: 'agrupaciones' };

function unitInfobox(u: GeologicalUnit): [string, string][] {
  const parent = u.parent ? unitById(u.parent) : undefined;
  return [
    ['Rango', esc(rankLabels[u.rank])],
    ...(parent ? [['Forma parte de', `<a href="#" class="enc-link" data-encyclopedia-entry="geo-${parent.id}">${esc(parent.name)}</a>`] as [string, string]] : []),
    ['Intervalo', esc(geologicalRangeLabel(u))],
    ['Duración', '≈ ' + esc(duration(u))],
    ['Límite inferior', u.gsspRatified ? 'Definido por un GSSP ratificado' : u.formal ? 'Sin GSSP ratificado' : 'Unidad informal'],
    ['Color ICS', `<span class="enc-swatch" style="background:${esc(u.color)}"></span> ${esc(u.color)}`]
  ];
}
/** Fase del plan en la que se redacta la monografía de una unidad. */
function unitPhase(u: GeologicalUnit) {
  const ids = [u.id, ...unitTrail(u).map(t => t.id)];
  return ids.includes('Proterozoic') ? 'P04 · Proterozoico' : ids.includes('Paleozoic') ? 'P05 · Paleozoico' : ids.includes('Mesozoic') ? 'P06 · Mesozoico' : ids.includes('Cenozoic') ? 'P07 · Cenozoico' : 'P03 · Hádico y Arcaico';
}
/** Unidad todavía sin monografía: solo un aviso; los datos están en la ficha y la escala. */
function unitPendingNote(u: GeologicalUnit) {
  return `<p class="enc-pending">La monografía de ${esc(u.name)} se redacta en la fase ${esc(unitPhase(u))} del plan de la enciclopedia. Mientras tanto, la ficha recoge sus datos oficiales y la escala permite situarla.</p>`;
}

async function geologicalPage(u: GeologicalUnit, md: Awaited<ReturnType<typeof loadSource>>, idx?: IndexPage, compact = false): Promise<Page> {
  const id = 'geo-' + u.id, legacy = encyclopediaArticle(id)!, trail = unitTrail(u);
  const parentLegacy = u.parent ? encyclopediaArticle('geo-' + u.parent) : undefined;
  const ownTheme = legacy.themeId && parentLegacy?.themeId !== legacy.themeId;
  const year = encyclopediaReferenceYear(legacy, consultedYear);
  let html: string, headings: Heading[];
  if (md) ({ html, headings } = renderMarkdown(md.body, renderOptions()));
  else if (ownTheme && !compact) { ({ html, headings } = legacyBody(legacy, year)); html = unitPendingNote(u) + html; }
  else if (compact) { html = `<p class="enc-pending">Monografía pendiente · fase ${esc(unitPhase(u))}.</p>`; headings = []; }
  else {
    const theme = legacy.themeId ? curatedArticles.find(a => a.id === legacy.themeId) : undefined;
    html = unitPendingNote(u) + `<figure class="enc-component enc-scale" data-scale-root="${esc(u.id)}">${scaleView(unitChildren(u).length ? u.id : u.parent ?? '')}</figure>` + (theme ? `<p class="enc-see">Lectura provisional relacionada: <a href="#" class="enc-link" data-encyclopedia-entry="${theme.id}">${esc(theme.title)}</a>.</p>` : '');
    headings = [];
  }
  return {
    id, kind: rankLabels[u.rank] + ' · escala geológica ICS', title: md?.meta.titulo ?? u.name,
    summary: idx?.resumen && md ? geologicalRangeLabel(u) + '. ' + idx.resumen : geologicalRangeLabel(u) + '.',
    year, html, headings, infobox: mergeInfobox(unitInfobox(u), infoboxFromMeta(md?.meta)),
    breadcrumb: trail.map(t => ({ id: 'geo-' + t.id, title: t.name })),
    children: [...topicsOf(id), ...unitChildren(u).map(c => ({ id: 'geo-' + c.id, title: c.name, summary: pageById('geo-' + c.id)?.resumen ?? '', meta: geologicalRangeLabel(c) }))],
    related: (md?.meta.relacionados as string[] | undefined) ?? (ownTheme ? legacy.related.filter(r => !r.startsWith('geo-')) : []),
    sources: [...sourcesFromMeta(md?.meta), { title: 'Comisión Internacional de Estratigrafía · Carta cronoestratigráfica 2026/06', url: u.source }, ...(ownTheme && !md ? legacySources(legacy) : [])],
    top: legacyImage(legacy) + planetFacts(year), legacy
  };
}

function mergeInfobox(base: [string, string][], extra: [string, string][]) { const keys = new Set(extra.map(e => e[0])); return [...base.filter(b => !keys.has(b[0])), ...extra]; }
function infoboxFromMeta(meta?: Record<string, unknown>): [string, string][] {
  const f = meta?.ficha as Record<string, unknown> | undefined;
  if (!f) return [];
  return Object.entries(f).map(([k, v]) => [esc(k), renderMarkdown(String(Array.isArray(v) ? v.join(', ') : v), renderOptions()).html.replace(/^<p>|<\/p>$/g, '')]);
}
function sourcesFromMeta(meta?: Record<string, unknown>): Source[] {
  return ((meta?.fuentes as { titulo?: string; url?: string }[] | undefined) ?? []).filter(s => s && s.url).map(s => ({ title: s.titulo ?? s.url!, url: s.url! }));
}

async function markdownPage(p: IndexPage): Promise<Page | undefined> {
  const md = await loadSource(p); if (!md) return;
  const { html, headings } = renderMarkdown(md.body, renderOptions());
  const trail: { id: string; title: string }[] = []; let parent = p.padre;
  while (parent) { trail.unshift({ id: parent, title: knownTitle(parent) ?? parent }); parent = pageById(parent)?.padre ?? (parent.startsWith('geo-') ? (unitById(parent.slice(4))?.parent ? 'geo-' + unitById(parent.slice(4))!.parent : null) : null); }
  const legacy = encyclopediaArticle(p.id);
  const kids = index!.paginas.filter(c => c.padre === p.id).sort((a, b) => (a.orden ?? 1e9) - (b.orden ?? 1e9) || (a.inicio ?? 0) - (b.inicio ?? 0) || a.titulo.localeCompare(b.titulo, 'es'));
  const year = p.ancla ?? (p.inicio !== null && p.fin !== null && consultedYear >= p.inicio && consultedYear <= p.fin ? consultedYear : p.inicio) ?? consultedYear;
  const KIND: Record<string, string> = { portada: 'Enciclopedia', guia: 'Guía', geologia: 'Escala geológica', tierra: 'Planeta Tierra', clima: 'Clima', vida: 'Vida', especie: 'Especie', humanidad: 'Humanidad', cultura: 'Cultura', contexto: 'Contexto histórico', entidad: 'Entidad política', persona: 'Biografía', evento: 'Acontecimiento', obra: 'Obra y monumento', tema: 'Tema', lista: 'Listado' };
  return {
    id: p.id, kind: KIND[p.tipo] ?? p.tipo, title: p.titulo, summary: (md.meta.resumen as string) ?? '', year,
    html: html + (legacy ? legacyExtras(legacy, year).html : ''), headings, infobox: infoboxFromMeta(md.meta), breadcrumb: trail,
    children: kids.map(c => ({ id: c.id, title: c.titulo, summary: c.resumen, meta: c.inicio !== null ? `${yearLabel(c.inicio)} — ${yearLabel(c.fin)}` : '' })),
    related: (md.meta.relacionados as string[] | undefined) ?? [], sources: sourcesFromMeta(md.meta), top: legacy ? legacyExtras(legacy, year).top : ''
  };
}

async function personPage(id: string, md?: Page): Promise<Page | undefined> {
  const person = await loadPerson(personKey(id)); if (!person && !md) return;
  const rows = person ? await Promise.all(person.m.map(async m => { const e = await loadEntity(m[0]); return `<tr><td><a href="#" class="enc-link" data-encyclopedia-entry="entidad-${esc(m[0])}">${esc(e?.n ?? m[0])}</a></td><td>${esc(m[1])}</td><td>${esc(dateLabel(m[2], m[4]))}</td><td>${esc(dateLabel(m[3], m[4]))}</td></tr>`; })) : [];
  const first = person?.m[0], active = person?.m.find(m => activeIn(consultedYear, m[2], m[3])), firstYear = active ? consultedYear : first ? dateYearOf(first[2]) ?? consultedYear : consultedYear;
  const firstEntity = first ? await loadEntity(first[0]) : undefined;
  const portrait = person?.p ? `<figure class="enc-portrait"><img src="${BASE + person.p.f}" alt="Retrato de ${esc(person.n)}" loading="lazy"><figcaption>${esc(person.p.a)}${person.p.l ? ' · ' + esc(person.p.l) : ''}${person.p.u ? ` · <a href="${esc(person.p.u)}" target="_blank" rel="noopener">Commons ↗</a>` : ''}</figcaption></figure>` : '';
  const table = rows.length ? `<h2 id="enc-cargos">Cargos registrados en el atlas</h2><div class="enc-table"><table><thead><tr><th>Entidad</th><th>Cargo</th><th>Desde</th><th>Hasta</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>` : '';
  const base: Page = md ?? {
    id, kind: 'Dirigente · ficha del atlas', title: person!.n,
    summary: first ? `${first[1]} de ${firstEntity?.n ?? first[0]}${person!.m.length > 1 ? ` y otros ${person!.m.length - 1} cargos registrados` : ''}.` : '',
    year: firstYear, html: `<p class="enc-pending">La biografía completa de ${esc(person!.n)} se está redactando. Mientras tanto, esta ficha reúne los cargos que el atlas tiene documentados.</p>`,
    headings: [], infobox: [], breadcrumb: [], children: [], related: [], sources: [], top: '', note: 'Ficha generada a partir de los datos de autoridades del atlas.'
  };
  return {
    ...base, portrait, year: md ? base.year : firstYear,
    html: base.html + table, headings: [...base.headings, ...(table ? [{ level: 2, text: 'Cargos registrados en el atlas', anchor: 'enc-cargos' }] : [])],
    infobox: [...base.infobox, ...(person ? [['Primer cargo', first ? esc(dateLabel(first[2], first[4])) : '—'], ['Cargos en el atlas', String(person.m.length)]] as [string, string][] : [])],
    sources: [...base.sources, ...(person?.w ? [{ title: 'Wikipedia', url: person.w }] : []), ...(/^Q\d+$/.test(personKey(id)) ? [{ title: 'Wikidata · ' + personKey(id), url: 'https://www.wikidata.org/wiki/' + personKey(id) }] : [])]
  };
}

async function entityPage(id: string, md?: Page): Promise<Page | undefined> {
  const e = await loadEntity(entityKey(id)); if (!e && !md) return;
  const rows = e ? e.m.map(m => `<tr><td><a href="#" class="enc-link" data-encyclopedia-entry="persona-${esc(m[0])}">${esc(m[1])}</a></td><td>${esc(m[2])}</td><td>${esc(dateLabel(m[3]))}</td><td>${esc(dateLabel(m[4]))}</td></tr>`) : [];
  const bars = e ? e.m.map(m => ({ id: 'persona-' + m[0], name: m[1], role: m[2], start: dateYearOf(m[3]) ?? 0, end: dateYearOf(m[4]) ?? dateYearOf(m[3]) ?? 0 })).filter(b => b.start) : [];
  const chart = successionChart(bars, 'Sucesión en el tiempo');
  const table = rows.length ? `<h2 id="enc-sucesion">Sucesión de dirigentes registrada</h2><div class="enc-table"><table><thead><tr><th>Dirigente</th><th>Cargo</th><th>Desde</th><th>Hasta</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>` : '';
  const year = e?.a ?? consultedYear;
  const base: Page = md ?? {
    id, kind: 'Entidad política · ficha del atlas', title: e!.n,
    summary: e!.a !== null ? `Dirigentes registrados entre ${yearLabel(e!.a)} y ${yearLabel(e!.b)}.` : '',
    year: e && e.a !== null && consultedYear >= e.a && consultedYear <= (e.b ?? e.a) ? consultedYear : year,
    html: `<p class="enc-pending">El artículo histórico de ${esc(e!.n)} está en preparación. Esta ficha muestra la sucesión de dirigentes que el atlas tiene documentada.</p>`,
    headings: [], infobox: [], breadcrumb: [], children: [], related: [], sources: [], top: '', note: 'Ficha generada a partir de los datos de autoridades del atlas.'
  };
  return {
    ...base, html: base.html + chart + table, headings: [...base.headings, ...(table ? [{ level: 2, text: 'Sucesión de dirigentes registrada', anchor: 'enc-sucesion' }] : [])],
    infobox: [...base.infobox, ...(e ? [['Registros', `${yearLabel(e.a)} — ${yearLabel(e.b)}`], ['Mandatos', String(e.m.length)]] as [string, string][] : [])],
    sources: [...base.sources, ...(e?.q ? [{ title: 'Wikidata · ' + e.q, url: 'https://www.wikidata.org/wiki/' + e.q }] : [])]
  };
}

async function datePage(year: number): Promise<Page> {
  const units = geologicalAt(year), humans = humanAt(year), deep = year < -10000;
  const lead = encyclopediaArticle(encyclopediaForYear(year));
  const contexts = index!.paginas.filter(p => p.tipo === 'contexto' && p.inicio !== null && p.inicio <= year && year <= (p.fin ?? p.inicio)).sort((x, y) => ((x.fin ?? x.inicio!) - x.inicio!) - ((y.fin ?? y.inicio!) - y.inicio!));
  const parts: string[] = [], headings: Heading[] = [];
  const section = (anchor: string, title: string, body: string) => { headings.push({ level: 2, text: title, anchor }); parts.push(`<section id="${anchor}"><h2>${esc(title)}</h2>${body}</section>`); };
  for (const c of contexts) { const md = await loadSource(c); if (md) section('enc-ctx-' + c.id, c.titulo, renderMarkdown(md.body, renderOptions({ headingOffset: 1, anchorPrefix: 'enc-' + c.id + '-' })).html); }
  if (deep) {
    const covering = [...units].reverse().find(u => pageById('geo-' + u.id));
    if (covering) { const idx = pageById('geo-' + covering.id)!, md = await loadSource(idx); if (md) section('enc-detalle', `${rankLabels[covering.rank]} vigente: ${covering.name}`, renderMarkdown(md.body, renderOptions({ headingOffset: 1, anchorPrefix: 'enc-det-' })).html + `<p class="enc-see">Página completa: <a href="#" class="enc-link" data-encyclopedia-entry="geo-${covering.id}">${esc(covering.name)}</a>.</p>`); }
  }
  if (lead) { const leadId = replacedBy.get(lead.id) ?? lead.id, md = pageById(leadId); section('enc-lectura', 'Lectura principal', `<button class="enc-card" data-encyclopedia-entry="${esc(leadId)}"><strong>${esc(md?.titulo ?? lead.title)}</strong><span>${esc(md?.resumen ?? lead.summary)}</span></button>`); }
  const chain = units.filter(u => u.rank !== 'group').map(u => `<a href="#" class="enc-link" data-encyclopedia-entry="geo-${u.id}"><small>${esc(rankLabels[u.rank])}</small>${esc(u.name)}</a>`).join('');
  section('enc-tiempo', 'Tiempo geológico', `<nav class="enc-chain" aria-label="Unidades geológicas vigentes">${chain}</nav>${humans.length ? `<p class="enc-chain-human">Periodizaciones humanas: ${humans.map(h => `<a href="#" class="enc-link" data-encyclopedia-entry="human-${h.id}">${esc(h.name)}</a> <small>(${esc(h.scope)})</small>`).join(' · ')}</p>` : ''}`);
  if (!deep) {
    const bucket = await loadCentury(year);
    if (bucket) {
      const groups = new Map<string, string[]>();
      for (const [entity, person, role, start, end] of bucket.m) if (activeIn(year, start, end)) {
        const list = groups.get(entity) ?? []; groups.set(entity, list);
        const item = `<li><a href="#" class="enc-link" data-encyclopedia-entry="persona-${esc(person)}">${esc(bucket.p[person])}</a> <small>${esc(role)} · ${esc(dateLabel(start))}–${esc(dateLabel(end))}</small></li>`;
        if (!list.includes(item)) list.push(item);
      }
      const sorted = [...groups].sort((a, b) => bucket.e[a[0]].localeCompare(bucket.e[b[0]], 'es'));
      if (sorted.length) section('enc-dirigentes', `Dirigentes en ${formatYear(year)}`, `<p class="enc-muted">${sorted.length} entidades con autoridades documentadas en el atlas para este año.</p><div class="enc-rulers">${sorted.map(([k, items]) => `<div><a href="#" class="enc-entity" data-encyclopedia-entry="entidad-${esc(k)}">${esc(bucket.e[k])}</a><ul>${items.join('')}</ul></div>`).join('')}</div>`);
    }
  }
  const dated = index!.paginas.filter(p => p.tipo !== 'contexto' && p.inicio !== null && p.fin !== null && p.inicio <= year && year <= p.fin && !p.id.startsWith('geo-'));
  if (dated.length) section('enc-paginas', 'Páginas de esta época', `<div class="enc-children">${dated.slice(0, 80).map(p => `<button data-encyclopedia-entry="${p.id}"><strong>${esc(p.titulo)}</strong><span>${esc(p.resumen)}</span></button>`).join('')}</div>`);
  const ay = Math.abs(year), step = ay >= 1e9 ? 5e7 : ay >= 1e8 ? 5e6 : ay >= 1e7 ? 1e6 : ay >= 1e6 ? 1e5 : ay >= 1e5 ? 1e4 : ay >= 1e4 ? 1000 : 1;
  const shift = (y: number, d: number) => { const n = y + d; return n === 0 ? (d > 0 ? 1 : -1) : y < 0 && n > 0 && d > 0 ? n : n; };
  const prev = shift(year, -step), next = shift(year, step);
  const nav = `<nav class="enc-years" aria-label="Navegación por fechas"><button data-encyclopedia-entry="fecha-${prev}">← ${esc(formatYear(prev))}</button><button data-encyclopedia-entry="fecha-${next}">${esc(formatYear(next))} →</button></nav>`;
  if (!contexts.length) parts.unshift(`<p class="enc-pending">El panorama narrado de esta fecha forma parte de las próximas fases de la enciclopedia. Mientras tanto, esta página reúne lo que el atlas ya sabe de esta fecha.</p>`);
  return {
    id: 'fecha-' + year, kind: 'Panorama de la fecha', title: year <= -1000000 ? 'La Tierra hace ' + formatYear(year) : 'El mundo en ' + formatYear(year),
    summary: contexts[0]?.resumen ?? (units.length ? `${units.filter(u => u.rank !== 'group').map(u => u.name).join(' › ')}.` : ''),
    year, html: nav + parts.join(''), headings, infobox: [], breadcrumb: [], children: [], related: [], sources: [], top: planetFacts(year)
  };
}

function legacyPage(a: EncyclopediaArticle): Page {
  const year = encyclopediaReferenceYear(a, consultedYear), human = humanUnits.find(u => 'human-' + u.id === a.id);
  const { html, headings } = legacyBody(a, year);
  return {
    id: a.id, kind: a.kind ?? 'Artículo temático', title: a.title, summary: a.summary, year, html, headings,
    infobox: human ? [['Ámbito', esc(human.scope)], ['Desde', esc(formatYear(human.startYear))], ['Hasta', human.endYear ? esc(formatYear(human.endYear)) : 'sin final fijado']] : [],
    breadcrumb: [], children: [], related: a.related, top: humanPhoto(a.themeId ?? a.id) + legacyImage(a) + planetFacts(year), legacy: a,
    sources: [...legacySources(a), ...(human ? [{ title: humanChronologySources[human.sourceId].title, url: humanChronologySources[human.sourceId].url }] : [])]
  };
}

/** Resuelve cualquier identificador en una página. */
async function resolve(id: string, compact = false): Promise<Page | undefined> {
  if (!index) { index = await loadIndex(); replacedBy = new Map(index.paginas.flatMap(p => (p.reemplaza ?? []).map(r => [r, p.id] as [string, string]))); }
  if (replacedBy.has(id)) return resolve(replacedBy.get(id)!, compact);
  if (/^fecha--?\d+$/.test(id)) return datePage(Number(id.slice(6)));
  const idx = pageById(id);
  if (id.startsWith('geo-')) { const u = unitById(id.slice(4)); if (u) return geologicalPage(u, idx ? await loadSource(idx) : null, idx, compact); }
  const md = idx ? await markdownPage(idx) : undefined;
  if (id.startsWith('persona-')) return personPage(id, md);
  if (id.startsWith('entidad-')) return entityPage(id, md);
  if (md) return md;
  const legacy = encyclopediaArticle(id);
  return legacy ? legacyPage(legacy) : undefined;
}

/* ---------- Composición: «leer completo» incluye las páginas hijas ---------- */
async function composedChildren(page: Page, depth: number): Promise<string> {
  if (depth > 4 || !page.children.length) return '';
  const out: string[] = [];
  for (const c of page.children) {
    const child = await resolve(c.id, true); if (!child) continue;
    const level = Math.min(6, depth + 1);
    const body = child.html.replace(/<h([2-5])( [^>]*)?>/g, (_m, n, attrs = '') => `<h${Math.min(6, Number(n) + depth)}${attrs.replace(/id="/, 'id="c-' + child.id + '-')}>`).replace(/<\/h([2-5])>/g, (_m, n) => `</h${Math.min(6, Number(n) + depth)}>`).replace(/id="encyclopedia-video-frame"/g, '').replace(/id="(encyclopedia-lab[^"]*|human-[^"]+)"/g, '');
    out.push(`<section class="enc-composed" data-depth="${depth}"><h${level} id="c-${esc(child.id)}"><a href="#" class="enc-link" data-encyclopedia-entry="${esc(child.id)}">${esc(child.title)}</a> <small>${esc(c.meta)}</small></h${level}>${body}${await composedChildren(child, depth + 1)}</section>`);
  }
  return out.join('');
}
function countDescendants(page: Page): number {
  const walk = (id: string): number => index!.paginas.filter(p => p.padre === id).reduce((n, p) => n + 1 + walk(p.id), 0) + (id.startsWith('geo-') ? geologicalUnits.filter(u => u.parent === id.slice(4)).reduce((n, u) => n + 1 + walk('geo-' + u.id), 0) : 0);
  return walk(page.id);
}

/* ---------- Índice lateral ---------- */
function unitTree(parent: string | null, path: Set<string>): string {
  return geologicalUnits.filter(u => u.parent === parent).sort((a, b) => b.oldestMa - a.oldestMa).map(u => {
    const kids = geologicalUnits.some(c => c.parent === u.id), current = history[cursor] === 'geo-' + u.id ? ' aria-current="page"' : '', open = path.has(u.id);
    const button = `<button data-encyclopedia-entry="geo-${u.id}"${current}><i style="background:${esc(u.color)}"></i>${esc(u.name)}</button>`;
    return `<div class="enc-node" data-open="${open}"><span class="enc-row">${kids ? `<button class="enc-toggle" data-enc-toggle aria-expanded="${open}" aria-label="Desplegar ${esc(u.name)}"></button>` : '<span class="enc-toggle"></span>'}${button}</span>${kids ? `<div class="enc-kids">${unitTree(u.id, path)}</div>` : ''}</div>`;
  }).join('');
}
function group(title: string, body: string, open = false, count?: number, sub = false) { return `<details class="enc-group${sub ? ' enc-subgroup' : ''}"${open ? ' open' : ''}><summary>${esc(title)}${count !== undefined ? ` <small>${count.toLocaleString('es')}</small>` : ''}</summary><div>${body}</div></details>`; }
const entry = (id: string, title: string, sub = '') => `<button data-encyclopedia-entry="${esc(id)}"${history[cursor] === id ? ' aria-current="page"' : ''}>${sub ? `<small>${esc(sub)}</small>` : ''}${esc(title)}</button>`;

let searchSerial = 0;
async function renderIndex() {
  const input = byId('encyclopedia-search') as HTMLInputElement, query = input.value.trim(), nav = byId('encyclopedia-index'), serial = ++searchSerial;
  const stats = index?.stats;
  if (query) {
    const q = normalizeText(query);
    const legacy = searchEncyclopedia(query, true).filter(a => !isReplaced(a.id)).slice(0, 60).map(a => ({ id: a.id, title: a.title, group: a.group }));
    const pages = (index?.paginas ?? []).filter(p => normalizeText([p.titulo, ...p.alias, p.resumen].join(' ')).includes(q)).map(p => ({ id: p.id, title: p.titulo, group: 'Enciclopedia' }));
    const seen = new Set<string>(), results = [...pages, ...legacy].filter(r => !seen.has(r.id) && seen.add(r.id));
    nav.innerHTML = results.map(r => entry(r.id, r.title, r.group)).join('');
    byId('encyclopedia-count').textContent = `${results.length} entradas · buscando dirigentes y entidades…`;
    if (q.length < 3) { byId('encyclopedia-count').textContent = `${results.length} entradas`; return; }
    const names = await loadNames(); if (serial !== searchSerial) return;
    const hits = names.filter(n => normalizeText(n[1]).includes(q) && !seen.has(n[0])).slice(0, 80);
    nav.insertAdjacentHTML('beforeend', hits.map(n => entry(n[0], n[1], n[2] === 'p' ? 'Dirigente' : 'Entidad política')).join(''));
    byId('encyclopedia-count').textContent = `${results.length + hits.length} resultados${hits.length === 80 ? ' (se muestran los primeros)' : ''}`;
    return;
  }
  const currentUnit = history[cursor]?.startsWith('geo-') ? unitById(history[cursor].slice(4)) : geologicalAt(consultedYear).at(-1);
  const path = new Set<string>(currentUnit ? [currentUnit.id, ...unitTrail(currentUnit).map(u => u.id)] : []);
  const pages = index?.paginas ?? [];
  const branches: Record<string, string> = { tierra: 'Planeta Tierra', clima: 'Clima y glaciaciones', vida: 'La vida', humanidad: 'Humanidad', culturas: 'Culturas', contextos: 'El mundo en cada época', entidades: 'Estados e imperios', personas: 'Biografías', eventos: 'Acontecimientos', obras: 'Obras y monumentos', temas: 'Temas' };
  // Cada rama se subdivide por el eón o la era a la que pertenece la página (por su padre geológico).
  const eraOf = (p: IndexPage) => {
    let u = p.padre?.startsWith('geo-') ? unitById(p.padre.slice(4)) : p.id.startsWith('geo-') ? unitById(p.id.slice(4)) : undefined;
    if (!u) return 'General';
    const trail = [u, ...unitTrail(u)];
    return (trail.find(t => t.rank === 'era' && t.parent === 'Phanerozoic') ?? trail.find(t => t.rank === 'eon'))?.name ?? 'General';
  };
  const ERA_ORDER = ['Hádico', 'Arcaico', 'Proterozoico', 'Paleozoico', 'Mesozoico', 'Cenozoico', 'General'];
  const byBranch = Object.entries(branches).map(([b, title]) => {
    const all = pages.filter(p => p.rama === b); if (!all.length) return '';
    const sorted = all.sort((x, y) => (x.inicio !== null && y.inicio !== null ? x.inicio - y.inicio : 0) || (x.orden ?? 1e9) - (y.orden ?? 1e9) || x.titulo.localeCompare(y.titulo, 'es'));
    const buckets = new Map<string, IndexPage[]>(); for (const p of sorted) { const k = eraOf(p); buckets.set(k, [...(buckets.get(k) ?? []), p]); }
    const body = buckets.size === 1 ? sorted.map(p => entry(p.id, p.titulo)).join('') : [...buckets].sort((a, c) => ERA_ORDER.indexOf(a[0]) - ERA_ORDER.indexOf(c[0])).map(([k, list]) => group(k, list.map(p => entry(p.id, p.titulo)).join(''), list.some(p => p.id === history[cursor]), list.length, true)).join('');
    return group(title, body, all.some(p => p.id === history[cursor]), all.length);
  }).join('');
  const archiveBuckets: [string, (ma: number) => boolean][] = [['Precámbrico', ma => ma > 538.8], ['Paleozoico', ma => ma <= 538.8 && ma > 251.9], ['Mesozoico', ma => ma <= 251.9 && ma > 66], ['Cenozoico', ma => ma <= 66]];
  const events = [...reviewedEvents].sort((a, c) => (c.observedAgeMa ?? 0) - (a.observedAgeMa ?? 0));
  const archive = archiveBuckets.map(([k, test]) => { const list = events.filter(e => test(e.observedAgeMa ?? 0)); return list.length ? group(k, list.map(e => entry(e.videoId, e.name)).join(''), false, list.length, true) : ''; }).join('');
  const concepts = curatedGroups.map(([k, list]) => { const l = list.filter(a => !isReplaced(a.id) && !pageById(a.id)); return l.length ? group(k, l.map(a => entry(a.id, a.title)).join(''), l.some(a => a.id === history[cursor]), l.length, true) : ''; }).join('');
  const conceptCount = curatedGroups.reduce((n, [, l]) => n + l.filter(a => !isReplaced(a.id) && !pageById(a.id)).length, 0);
  const general = pages.filter(p => ['portada', 'guia'].includes(p.tipo)).sort((x, y) => (x.orden ?? 1e9) - (y.orden ?? 1e9));
  nav.innerHTML = [
    entry('fecha-' + consultedYear, (consultedYear <= -1000000 ? 'La Tierra hace ' : 'El mundo en ') + formatYear(consultedYear), 'Ahora en el mapa'),
    ...general.map(p => entry(p.id, p.titulo)),
    group('Escala temporal geológica', `<div class="enc-tree">${unitTree(null, path)}</div>`, history[cursor]?.startsWith('geo-'), geologicalUnits.length),
    group('Conceptos y procesos', concepts, false, conceptCount),
    group('Evolución humana', humanKnowledge.articles.map(a => entry(a.id, a.title)).join(''), false, humanKnowledge.articles.length),
    group('Edades de la humanidad', humanUnits.map(u => entry('human-' + u.id, u.name, u.scope)).join(''), false, humanUnits.length),
    byBranch,
    group('Archivo audiovisual', archive, history[cursor]?.startsWith('video-'), events.length)
  ].join('');
  byId('encyclopedia-count').textContent = stats ? `${(stats.paginas + geologicalUnits.length + curatedArticles.length).toLocaleString('es')} artículos · ${stats.personas.toLocaleString('es')} dirigentes · ${stats.entidades.toLocaleString('es')} entidades` : '';
}

/* ---------- Pintado ---------- */
async function render(composeAll = false) {
  const id = history[cursor], token = ++renderToken;
  byId('encyclopedia-back').toggleAttribute('disabled', cursor <= 0);
  byId('encyclopedia-forward').toggleAttribute('disabled', cursor >= history.length - 1);
  byId('encyclopedia-context').textContent = 'Consulta del mapa · ' + formatYear(consultedYear);
  const page = await resolve(id);
  if (token !== renderToken) return;
  if (!page) { byId('encyclopedia-article').innerHTML = `<article data-article="${esc(id)}"><h1 tabindex="-1">Página no encontrada</h1><p>No existe ninguna entrada con el identificador «${esc(id)}».</p></article>`; return; }
  const descendants = countDescendants(page);
  const composed = composeAll ? await composedChildren(page, 1) : '';
  if (token !== renderToken) return;
  const related = page.related.map(r => ({ id: r, title: knownTitle(r) })).filter(r => r.title);
  const toc = [...page.headings.filter(h => h.level === 2), ...(page.children.length && !composeAll ? [{ level: 2, text: 'Contenido', anchor: 'enc-contenido' }] : [])];
  byId('encyclopedia-article').innerHTML = `<article data-article="${esc(page.id)}" class="enc-page">
<header class="enc-head">
${page.breadcrumb.length ? `<nav class="encyclopedia-breadcrumb" aria-label="Jerarquía">${page.breadcrumb.map(b => `<button data-encyclopedia-entry="${esc(b.id)}">${esc(b.title)}</button>`).join('<span>›</span>')}</nav>` : ''}
<div class="encyclopedia-kicker">${esc(page.kind)}</div><h1 tabindex="-1">${esc(page.title)}</h1>${page.summary ? `<p class="encyclopedia-lead">${esc(page.summary)}</p>` : ''}
<div class="encyclopedia-actions"><button class="primary-button" data-encyclopedia-map="${page.year}">Ver en el mapa · ${formatYear(page.year)}</button>${descendants ? `<button class="enc-compose" data-encyclopedia-compose="${composeAll ? 'off' : 'on'}" aria-pressed="${composeAll}">${composeAll ? 'Leer solo esta página' : `Leer completo · incluye ${descendants} subdivisiones`}</button>` : ''}</div>
</header>
<div class="enc-columns"><div class="enc-main">
${page.infobox.length || page.portrait ? `<aside class="enc-infobox" aria-label="Ficha">${page.portrait ?? ''}<dl>${page.infobox.map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('')}</dl></aside>` : ''}
${page.top}
${toc.length > 1 ? `<nav class="encyclopedia-contents" aria-label="En este artículo"><strong>En este artículo</strong>${toc.map(h => `<a href="#${esc(h.anchor)}">${esc(h.text)}</a>`).join('')}</nav>` : ''}
<div class="enc-body">${page.html}</div>
${composeAll ? `<div class="enc-composition">${composed}</div>` : page.children.length ? `<section id="enc-contenido"><h2>Contenido</h2><div class="enc-children">${page.children.map(c => `<button data-encyclopedia-entry="${esc(c.id)}"><strong>${esc(c.title)}</strong>${c.meta ? `<small>${esc(c.meta)}</small>` : ''}${c.summary ? `<span>${esc(c.summary)}</span>` : ''}</button>`).join('')}</div></section>` : ''}
${related.length ? `<section><h2>Continúa explorando</h2><div class="encyclopedia-related">${related.map(r => `<button data-encyclopedia-entry="${esc(r.id)}">${esc(r.title!)} →</button>`).join('')}</div></section>` : ''}
${page.sources.length || page.note ? `<section class="encyclopedia-references"><h2>Fuentes</h2>${page.sources.map(s => `<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)} ↗</a>`).join('')}${page.note ? `<p>${esc(page.note)}</p>` : ''}</section>` : ''}
</div></div>
</article>`;
  dialog.dataset.article = page.id;
  resetSpeech();
  void hydrate(byId('encyclopedia-article'));
  void renderIndex();
  const reading = byId('encyclopedia-article'); reading.scrollTop = 0;
  reading.querySelector<HTMLElement>('h1')?.focus({ preventScroll: true });
}

/** Completa componentes que necesitan datos asíncronos (mapas). */
async function hydrate(root: HTMLElement) {
  const maps = [...root.querySelectorAll<HTMLElement>('[data-enc-map]')]; if (!maps.length) return;
  const world = await loadWorld();
  for (const m of maps) { try { m.querySelector('.enc-map-canvas')!.innerHTML = mapSvg(world, JSON.parse(m.dataset.encMap!)); } catch { /* sin mapa */ } }
}

export function navigateEncyclopedia(id: string) {
  history = history.slice(0, cursor + 1); history.push(id); cursor = history.length - 1; void render();
}

function setup() {
  dialog = document.createElement('dialog'); dialog.id = 'encyclopedia'; dialog.setAttribute('aria-labelledby', 'encyclopedia-title');
  dialog.innerHTML = `<header class="encyclopedia-header"><div><span class="eyebrow">HISTORICMAP</span><h2 id="encyclopedia-title">Enciclopedia</h2></div><div class="encyclopedia-history"><button id="encyclopedia-back" aria-label="Página anterior">←</button><button id="encyclopedia-forward" aria-label="Página siguiente">→</button></div><span id="encyclopedia-context"></span>${playerMarkup()}<button id="encyclopedia-close" aria-label="Cerrar enciclopedia y volver al mapa"><span class="enc-close-label">Volver al mapa </span>×</button></header><div class="encyclopedia-layout"><aside><label for="encyclopedia-search">Buscar en la enciclopedia</label><input id="encyclopedia-search" type="search" placeholder="Época, persona, estado, concepto…" autocomplete="off"><p id="encyclopedia-count"></p><nav id="encyclopedia-index" aria-label="Índice enciclopédico"></nav></aside><div id="encyclopedia-article" class="encyclopedia-reading"></div></div>`;
  document.body.append(dialog);
  byId('encyclopedia-search').oninput = () => void renderIndex();
  byId('encyclopedia-close').onclick = () => dialog.close();
  byId('encyclopedia-back').onclick = () => { if (cursor > 0) { cursor--; void render(); } };
  byId('encyclopedia-forward').onclick = () => { if (cursor < history.length - 1) { cursor++; void render(); } };
  dialog.addEventListener('change', e => { handleSpeechChange(e.target as Element); });
  dialog.addEventListener('close', () => { stopSpeech(); byId('encyclopedia-video-frame')?.replaceChildren(); returnFocus?.setAttribute('aria-expanded', 'false'); returnFocus?.focus(); });
  dialog.addEventListener('click', e => {
    const target = e.target as Element;
    if (target.closest('summary')) return;
    if (handleSpeechClick(target)) return;
    const zoom = target.closest<HTMLElement>('[data-scale-zoom]');
    if (zoom) { const fig = zoom.closest<HTMLElement>('.enc-scale'); if (fig) { const caption = fig.querySelector('figcaption')?.outerHTML ?? ''; fig.innerHTML = scaleView(zoom.dataset.scaleZoom ?? '') + caption; } return; }
    const toggle = target.closest<HTMLElement>('[data-enc-toggle]');
    if (toggle) { const node = toggle.closest<HTMLElement>('.enc-node')!, open = node.dataset.open !== 'true'; node.dataset.open = String(open); toggle.setAttribute('aria-expanded', String(open)); return; }
    const entryEl = target.closest<HTMLElement>('[data-encyclopedia-entry]'), jump = target.closest<HTMLElement>('[data-encyclopedia-map]'), video = target.closest<HTMLElement>('[data-video-id]'), compose = target.closest<HTMLElement>('[data-encyclopedia-compose]');
    const anchor = target.closest<HTMLAnchorElement>('a[href^="#enc"], a[href^="#encyclopedia-section"], a[href^="#c-"]');
    if (anchor) { e.preventDefault(); byId('encyclopedia-article').querySelector(anchor.getAttribute('href')!)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    if (entryEl) { e.preventDefault(); navigateEncyclopedia(entryEl.dataset.encyclopediaEntry!); }
    if (compose) void render(compose.dataset.encyclopediaCompose === 'on');
    if (jump) { dialog.close(); onMap(Number(jump.dataset.encyclopediaMap)); }
    if (video) { const frame = document.createElement('iframe'); frame.src = `https://www.youtube-nocookie.com/embed/${video.dataset.videoId}`; frame.title = 'NASA · simulación de la formación lunar'; frame.allowFullscreen = true; frame.referrerPolicy = 'strict-origin-when-cross-origin'; byId('encyclopedia-video-frame').replaceChildren(frame); }
  });
  dialog.addEventListener('keydown', e => { const t = e.target as HTMLElement; if ((e.key === 'Enter' || e.key === ' ') && t.matches('g[role=button], g[role=link]')) { e.preventDefault(); t.dispatchEvent(new MouseEvent('click', { bubbles: true })); } });
  dialog.addEventListener('input', e => {
    const range = e.target as HTMLInputElement; if (handleHumanInput(range)) return; if (range.id !== 'encyclopedia-lab') return;
    const a = encyclopediaArticle(history[cursor]); if (!a) return;
    if (a.diagram === 'albedo') { byId('encyclopedia-lab-output').textContent = `${100 - Number(range.value)} % de luz absorbida · balance simplificado`; (byId('encyclopedia-energy') as HTMLProgressElement).value = 100 - Number(range.value); }
    else { dialog.style.setProperty('--impact-progress', String(Number(range.value) / 100)); byId('encyclopedia-lab-output').textContent = Number(range.value) < 33 ? 'Acercamiento · sin escala temporal' : Number(range.value) < 66 ? 'Impacto y material expulsado · escenario' : 'Reorganización · escenario'; }
  });
}

/** Abre la enciclopedia. Sin entrada concreta, abre el panorama de la fecha consultada en el mapa. */
export function openEncyclopedia(year: number, callback: (year: number) => void, entryId?: string) {
  if (!dialog) setup();
  consultedYear = year; onMap = callback; returnFocus = document.getElementById('encyclopedia-button')!; returnFocus.setAttribute('aria-expanded', 'true');
  history = []; cursor = -1; (byId('encyclopedia-search') as HTMLInputElement).value = ''; dialog.style.setProperty('--impact-progress', '0');
  dialog.showModal();
  navigateEncyclopedia(entryId ?? 'fecha-' + year);
}
