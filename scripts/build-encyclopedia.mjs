#!/usr/bin/env node
// Compilador de la enciclopedia: valida enciclopedia/**/*.md, resuelve enlaces internos y genera
// enciclopedia/_generado/ (índice, nombres, personas, entidades y mandatos por siglo).
// Uso: node scripts/build-encyclopedia.mjs [--check]
//   --check  valida sin escribir y termina con error si hay problemas.
import { readFileSync, writeFileSync, readdirSync, statSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { join, relative, dirname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { splitPage, PAGE_TYPES, ID_PATTERN, civilYear, internalLinks, firstParagraph, shardOf, PERSON_SHARDS, ENTITY_SHARDS, centuryOf, COMPONENT_NAMES, CALLOUT_KINDS, blocksIn } from './lib/encyclopedia-format.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const readJson = p => JSON.parse(readFileSync(join(ROOT, p), 'utf8'));

function walk(dir) {
  const out = [];
  for (const name of readdirSync(dir)) {
    if (name.startsWith('_') || name.startsWith('.')) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (name.endsWith('.md') && !['PLAN.md', 'README.md'].includes(name)) out.push(p);
  }
  return out;
}

const yearOf = date => { const m = /^(-?\d+)-/.exec(date ?? ''); return m ? Number(m[1]) : null; };

/** Identificadores ya existentes fuera de enciclopedia/ (contenido heredado y unidades). */
function legacyIds() {
  const ids = new Set();
  for (const f of ['Tierra/Precambrico/enciclopedia.json', 'Tierra/Fanerozoico/enciclopedia.json', 'Tierra/Cuaternario/enciclopedia.json', 'public/data/human-knowledge.json'])
    for (const a of readJson(f).articles) ids.add(a.id);
  for (const f of ['Tierra/Precambrico/revision-video.json', 'Tierra/Fanerozoico/revision-video.json']) for (const e of readJson(f).events) ids.add(e.videoId);
  for (const e of readJson('public/data/human-knowledge.json').videoReview.events) ids.add(e.videoId);
  for (const u of readJson('Tierra/Cronologia/ics-2026-06.json').units) ids.add('geo-' + u.id);
  for (const u of readJson('Tierra/Cronologia/edades-humanas.json').units) ids.add('human-' + u.id);
  return ids;
}

export function entityPageId(key) { return 'entidad-' + key.replace(/[^A-Za-z0-9-]/g, '-'); }
export function personPageId(person) { return 'persona-' + String(person).replace(/[^A-Za-z0-9-]/g, '-'); }


/** Douglas-Peucker sobre un anillo [lon, lat]. */
function simplify(ring, tol) {
  if (ring.length < 4) return ring;
  const keep = new Uint8Array(ring.length); keep[0] = keep[ring.length - 1] = 1;
  const stack = [[0, ring.length - 1]];
  while (stack.length) {
    const [a, b] = stack.pop(); let max = 0, idx = -1;
    const [ax, ay] = ring[a], [bx, by] = ring[b], dx = bx - ax, dy = by - ay, len = Math.hypot(dx, dy) || 1e-12;
    for (let i = a + 1; i < b; i++) { const d = Math.abs(dy * ring[i][0] - dx * ring[i][1] + bx * ay - by * ax) / len; if (d > max) { max = d; idx = i; } }
    if (max > tol && idx > 0) { keep[idx] = 1; stack.push([a, idx], [idx, b]); }
  }
  return ring.filter((_, i) => keep[i]);
}
const ringArea = r => { let a = 0; for (let i = 0, j = r.length - 1; i < r.length; j = i++) a += (r[j][0] - r[i][0]) * (r[j][1] + r[i][1]); return Math.abs(a / 2); };
/** Contorno mundial muy simplificado (Natural Earth, dominio público) para los mapas de localización. */
function worldOutline() {
  const out = {};
  for (const f of readJson('public/data/countries.geojson').features) {
    const polys = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
    const parts = [];
    for (const poly of polys) {
      const outer = poly[0]; if (ringArea(outer) < 0.08) continue;
      let far = 0, fd = 0; outer.forEach((pt, i) => { const d = Math.hypot(pt[0] - outer[0][0], pt[1] - outer[0][1]); if (d > fd) { fd = d; far = i; } });
      const r = [...simplify(outer.slice(0, far + 1), 0.12), ...simplify(outer.slice(far), 0.12).slice(1)]; if (r.length < 4) continue;
      parts.push('M' + r.map(([x, y]) => `${x.toFixed(2)} ${(-y).toFixed(2)}`).join('L') + 'Z');
    }
    if (parts.length) out[f.properties.code ?? f.properties.name] = (out[f.properties.code] ?? '') + parts.join('');
  }
  return out;
}

/** Compila en memoria. Devuelve { files: Map<rutaRelativa, contenido>, errors, stats }. */
export function compileEncyclopedia() {
  const errors = [], warnings = [];
  const dir = join(ROOT, 'enciclopedia');
  const pages = [];
  for (const file of existsSync(dir) ? walk(dir) : []) {
    const rel = relative(dir, file).split(sep).join('/');
    try {
      const { meta, body } = splitPage(readFileSync(file, 'utf8'));
      for (const k of ['id', 'tipo', 'titulo']) if (!meta[k]) throw Error('falta el campo «' + k + '»');
      if (!ID_PATTERN.test(meta.id)) throw Error('identificador no válido: ' + meta.id);
      if (!PAGE_TYPES.includes(meta.tipo)) throw Error('tipo desconocido: ' + meta.tipo);
      const inicio = civilYear(meta.inicio), fin = civilYear(meta.fin);
      pages.push({ meta, body, rel, inicio, fin });
    } catch (e) { errors.push(`${rel}: ${e.message}`); }
  }

  // Dirigentes y entidades del atlas (public/data/identities.json es la fuente que usa el mapa).
  const identities = readJson('public/data/identities.json').countries;
  const persons = new Map(), entities = new Map(), centuries = new Map();
  for (const [key, entity] of Object.entries(identities)) {
    const mandates = [];
    for (const l of entity.leaders ?? []) {
      const p = persons.get(l.person) ?? { id: l.person, n: l.name, m: [], w: null, p: null };
      persons.set(l.person, p);
      p.m.push([key, l.role, l.start, l.end, l.precision ?? 11]);
      if (!p.w && /wikipedia\.org/.test(l.source ?? '')) p.w = l.source;
      if (!p.p && l.portrait?.file) p.p = { f: l.portrait.file, a: l.portrait.artist ?? '', l: l.portrait.license ?? '', u: l.portrait.url ?? '' };
      mandates.push([l.person, l.name, l.role, l.start, l.end]);
      const a = yearOf(l.start), b = yearOf(l.end) ?? a;
      if (a !== null) for (let c = centuryOf(a); c <= centuryOf(b); c++) {
        const bucket = centuries.get(c) ?? { e: {}, p: {}, m: [] };
        centuries.set(c, bucket);
        bucket.e[key] = entity.name; bucket.p[l.person] = l.name;
        bucket.m.push([key, l.person, l.role, l.start, l.end]);
      }
    }
    mandates.sort((x, y) => (yearOf(x[3]) ?? 0) - (yearOf(y[3]) ?? 0) || String(x[3]).localeCompare(String(y[3])));
    const years = mandates.flatMap(m => [yearOf(m[3]), yearOf(m[4])]).filter(y => y !== null);
    entities.set(key, { k: key, n: entity.name, q: entity.qid ?? null, a: years.length ? Math.min(...years) : null, b: years.length ? Math.max(...years) : null, m: mandates });
  }
  for (const p of persons.values()) p.m.sort((x, y) => (yearOf(x[2]) ?? 0) - (yearOf(y[2]) ?? 0));

  // Índice y validación de enlaces.
  const known = legacyIds();
  const credits = existsSync(join(dir, 'medios', 'creditos.json')) ? JSON.parse(readFileSync(join(dir, 'medios', 'creditos.json'), 'utf8')) : {};
  const ids = new Set();
  for (const p of pages) { if (ids.has(p.meta.id)) errors.push(`${p.rel}: identificador duplicado ${p.meta.id}`); ids.add(p.meta.id); }
  const personIds = new Set([...persons.keys()].map(personPageId)), entityIds = new Set([...entities.keys()].map(entityPageId));
  const resolves = id => ids.has(id) || known.has(id) || personIds.has(id) || entityIds.has(id) || /^fecha--?\d+$/.test(id);
  let linkCount = 0; const imageUse = new Map();
  for (const p of pages) {
    const refs = [...internalLinks(p.body), ...(p.meta.relacionados ?? []), ...(p.meta.padre ? [p.meta.padre] : [])];
    for (const id of refs) { linkCount++; if (!resolves(id)) errors.push(`${p.rel}: enlace a una página inexistente «${id}»`); }
    for (const id of p.meta.reemplaza ?? []) if (!known.has(id)) errors.push(`${p.rel}: «reemplaza» apunta a un artículo heredado inexistente «${id}»`);
    if (!Array.isArray(p.meta.fuentes) || !p.meta.fuentes.length) warnings.push(`${p.rel}: sin fuentes`);
    const words = p.body.split(/\s+/).filter(Boolean).length;
    if (words < 1500 && !p.meta.breve) warnings.push(`${p.rel}: ${words} palabras (mínimo editorial: 1.500)`);
    for (const b of blocksIn(p.body)) {
      const name = b.kind === 'componente' ? b.arg.split(/\s+/)[0] : b.kind;
      if (!['cronologia', 'datos', ...CALLOUT_KINDS].includes(name) && !COMPONENT_NAMES.includes(name)) errors.push(`${p.rel}: componente desconocido «${name}»`);
    }
    const images = [...p.body.matchAll(/!\[[^\]]*\]\((?!https?:)([^)\s]+)/g)].map(m => m[1]).concat([...p.body.matchAll(/^\s*(medios\/[^|\s]+)\s*\|/gm)].map(m => m[1]));
    for (const img of images) {
      const clean = img.replace(/^\.?\/?/, '');
      if (!existsSync(join(dir, clean))) errors.push(`${p.rel}: imagen inexistente «${img}»`);
      else if (!credits[clean.replace(/^medios\//, '')]) errors.push(`${p.rel}: la imagen «${img}» no tiene crédito en medios/creditos.json`);
      const used = imageUse.get(clean); if (used && used !== p.rel) errors.push(`${p.rel}: la imagen «${img}» ya se usa en ${used} (cada imagen, una sola vez)`); else imageUse.set(clean, p.rel);
    }
  }
  const index = pages.map(p => ({
    id: p.meta.id, tipo: p.meta.tipo, titulo: p.meta.titulo, alias: p.meta.alias ?? [],
    resumen: p.meta.resumen ?? firstParagraph(p.body), inicio: p.inicio, fin: p.fin,
    ancla: p.meta.anclaMapa !== undefined ? civilYear(p.meta.anclaMapa) : null,
    padre: p.meta.padre ?? null, orden: p.meta.orden ?? null, ruta: p.rel, rama: p.rel.split('/')[0], reemplaza: p.meta.reemplaza ?? [],
    palabras: p.body.split(/\s+/).filter(Boolean).length
  })).sort((a, b) => a.id.localeCompare(b.id));

  const files = new Map();
  const put = (path, data) => files.set(path, JSON.stringify(data));
  const stats = { paginas: index.length, palabras: index.reduce((n, p) => n + p.palabras, 0), enlaces: linkCount, personas: persons.size, entidades: entities.size, mandatos: [...entities.values()].reduce((n, e) => n + e.m.length, 0) };
  put('indice.json', { version: 1, stats, paginas: index });
  put('nombres.json', [...[...persons.values()].map(p => [personPageId(p.id), p.n, 'p']), ...[...entities.values()].map(e => [entityPageId(e.k), e.n, 'e'])]);
  const personShards = Array.from({ length: PERSON_SHARDS }, () => ({}));
  for (const p of persons.values()) personShards[shardOf(p.id, PERSON_SHARDS)][p.id] = p;
  personShards.forEach((s, i) => put(`personas/${String(i).padStart(2, '0')}.json`, s));
  const entityShards = Array.from({ length: ENTITY_SHARDS }, () => ({}));
  for (const e of entities.values()) entityShards[shardOf(e.k, ENTITY_SHARDS)][e.k] = e;
  entityShards.forEach((s, i) => put(`entidades/${String(i).padStart(2, '0')}.json`, s));
  for (const [c, bucket] of centuries) put(`mandatos/${c}.json`, bucket);
  put('mundo.json', worldOutline());
  return { files, errors, warnings, stats };
}

export function writeEncyclopedia() {
  const result = compileEncyclopedia();
  const out = join(ROOT, 'enciclopedia', '_generado');
  rmSync(out, { recursive: true, force: true });
  for (const [path, data] of result.files) {
    const target = join(out, path);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, data);
  }
  return result;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const check = process.argv.includes('--check');
  const t = Date.now();
  const result = check ? compileEncyclopedia() : writeEncyclopedia();
  for (const w of result.warnings) console.warn('aviso: ' + w);
  for (const e of result.errors) console.error('error: ' + e);
  const s = result.stats;
  console.log(`Enciclopedia: ${s.paginas} páginas, ${s.palabras} palabras, ${s.enlaces} enlaces; ${s.personas} dirigentes, ${s.entidades} entidades, ${s.mandatos} mandatos · ${Date.now() - t} ms${check ? ' · comprobación' : ''}`);
  if (result.errors.length) process.exit(1);
}
