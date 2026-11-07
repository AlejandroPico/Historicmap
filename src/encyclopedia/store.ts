// Acceso a los datos de la enciclopedia nueva: páginas Markdown de enciclopedia/ y datos generados
// por scripts/build-encyclopedia.mjs (índice, dirigentes, entidades, mandatos). Todo se carga bajo demanda.
import { splitPage, shardOf, PERSON_SHARDS, ENTITY_SHARDS, centuryOf, normalizeText } from '../../scripts/lib/encyclopedia-format.mjs';

export interface IndexPage { id: string; tipo: string; titulo: string; alias: string[]; resumen: string; inicio: number | null; fin: number | null; ancla: number | null; padre: string | null; orden: number | null; ruta: string; rama: string; palabras: number }
export interface EncyclopediaIndexFile { version: number; stats: { paginas: number; palabras: number; enlaces: number; personas: number; entidades: number; mandatos: number }; paginas: IndexPage[] }
/** [entidad, cargo, inicio, fin, precisión] */
export type PersonMandate = [string, string, string, string, number];
export interface PersonRecord { id: string; n: string; m: PersonMandate[]; w: string | null; p: { f: string; a: string; l: string; u: string } | null }
/** [persona, nombre, cargo, inicio, fin] */
export interface EntityRecord { k: string; n: string; q: string | null; a: number | null; b: number | null; m: [string, string, string, string, string][] }
export interface CenturyBucket { e: Record<string, string>; p: Record<string, string>; m: [string, string, string, string, string][] }

type Loader<T> = () => Promise<T>;
const generated = import.meta.glob('../../enciclopedia/_generado/**/*.json', { import: 'default' }) as Record<string, Loader<unknown>>;
const sources = import.meta.glob(['../../enciclopedia/**/*.md', '!../../enciclopedia/_generado/**', '!../../enciclopedia/PLAN.md', '!../../enciclopedia/README.md'], { query: '?raw', import: 'default' }) as Record<string, Loader<string>>;
const mediaUrls = import.meta.glob('../../enciclopedia/medios/**/*.{jpg,jpeg,png,webp,svg,gif}', { query: '?url', import: 'default', eager: true }) as Record<string, string>;

const cache = new Map<string, Promise<unknown>>();
function load<T>(path: string, fallback: T): Promise<T> {
  const key = '../../enciclopedia/_generado/' + path;
  if (!cache.has(key)) cache.set(key, generated[key] ? generated[key]().catch(() => fallback) : Promise.resolve(fallback));
  return cache.get(key) as Promise<T>;
}

export const loadIndex = () => load<EncyclopediaIndexFile>('indice.json', { version: 0, stats: { paginas: 0, palabras: 0, enlaces: 0, personas: 0, entidades: 0, mandatos: 0 }, paginas: [] });
export const loadNames = () => load<[string, string, 'p' | 'e'][]>('nombres.json', []);
export async function loadPerson(id: string) { const shard = await load<Record<string, PersonRecord>>(`personas/${String(shardOf(id, PERSON_SHARDS)).padStart(2, '0')}.json`, {}); return shard[id]; }
export async function loadEntity(key: string) { const shard = await load<Record<string, EntityRecord>>(`entidades/${String(shardOf(key, ENTITY_SHARDS)).padStart(2, '0')}.json`, {}); return shard[key]; }
export const loadWorld = () => load<Record<string, string>>('mundo.json', {});
export const loadCentury = (year: number) => load<CenturyBucket | null>(`mandatos/${centuryOf(year)}.json`, null);

/** Página Markdown por identificador (null si no existe). */
export async function loadSource(page: IndexPage) {
  const loader = sources['../../enciclopedia/' + page.ruta];
  return loader ? splitPage(await loader()) : null;
}
export interface MediaCredit { titulo?: string; autor: string; licencia: string; licenciaUrl?: string; fuente: string }
const creditFiles = import.meta.glob('../../enciclopedia/medios/creditos.json', { import: 'default', eager: true }) as Record<string, Record<string, MediaCredit>>;
const credits: Record<string, MediaCredit> = Object.values(creditFiles)[0] ?? {};
const cleanMedia = (path: string) => path.replace(/^\.?\/?(medios\/)?/, '');
/** Crédito HTML de una imagen de enciclopedia/medios (autor, licencia y fuente). */
export function mediaCredit(path: string) {
  const c = credits[cleanMedia(path)]; if (!c) return undefined;
  const e = (s: string) => s.replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]!));
  return `${e(c.autor)} · ${c.licenciaUrl ? `<a href="${e(c.licenciaUrl)}" target="_blank" rel="noopener">${e(c.licencia)}</a>` : e(c.licencia)} · <a href="${e(c.fuente)}" target="_blank" rel="noopener">Fuente ↗</a>`;
}
export function mediaUrl(path: string) {
  const clean = path.replace(/^\.?\/?(medios\/)?/, '');
  return mediaUrls['../../enciclopedia/medios/' + clean];
}

/** Años de un mandato (YYYY-MM-DD civil). */
export const dateYearOf = (date: string) => { const m = /^(-?\d+)-/.exec(date ?? ''); return m ? Number(m[1]) : null; };
export function activeIn(year: number, start: string, end: string) {
  const a = dateYearOf(start), b = dateYearOf(end) ?? a;
  return a !== null && b !== null && a <= year && year <= b;
}
export { normalizeText };
