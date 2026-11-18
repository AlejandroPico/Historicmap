// Internacionalización. Los textos de la interfaz viven en i18n/<idioma>/*.json (uno por área: interfaz, fichas,
// historia, tierra, enciclopedia, acerca), agrupados por módulo y clave: { "main": { "verMapa2d": "Ver mapa 2D" } }.
// El código pide cada texto con tx('main.verMapa2d') o, con datos, tx('main.cargando', { year }) → «Cargando {year}…».
// Español es el idioma base y el de reserva: una clave que falte en otro idioma se muestra en español.
// Para añadir un idioma basta con crear i18n/<código>/ con los mismos archivos y declararlo en i18n/idiomas.json.
import idiomas from '../i18n/idiomas.json' with { type: 'json' };

import interfaz from '../i18n/es/interfaz.json' with { type: 'json' };
import fichas from '../i18n/es/fichas.json' with { type: 'json' };
import historia from '../i18n/es/historia.json' with { type: 'json' };
import tierra from '../i18n/es/tierra.json' with { type: 'json' };
import enciclopedia from '../i18n/es/enciclopedia.json' with { type: 'json' };
import acerca from '../i18n/es/acerca.json' with { type: 'json' };

type Bundle = Record<string, Record<string, string>>;
/** localStorage del navegador, o null fuera de él (Node trae un localStorage experimental que avisa al tocarlo). */
export function browserStorage(): Storage | null {
  if (typeof window === 'undefined' || typeof document === 'undefined') return null;
  try { return window.localStorage; } catch { return null; }
}
// El español va siempre incluido; los demás idiomas se recogen de la carpeta al compilar con Vite
// (fuera de Vite, p. ej. en las pruebas de Node, import.meta.glob no existe y solo hay español).
let files: Record<string, Bundle> = {};
try { files = import.meta.glob(['../i18n/*/*.json', '!../i18n/es/*.json', '!../i18n/idiomas.json'], { eager: true, import: 'default' }) as Record<string, Bundle>; } catch { /* sin Vite */ }
files = { ...files, ...Object.fromEntries(Object.entries({ interfaz, fichas, historia, tierra, enciclopedia, acerca }).map(([k, v]) => [`../i18n/es/${k}.json`, v as Bundle])) };
const dictionaries: Record<string, Record<string, string>> = {};
for (const [file, bundle] of Object.entries(files)) {
  const lang = file.split('/').at(-2)!;
  const flat = (dictionaries[lang] ??= {});
  for (const [ns, entries] of Object.entries(bundle)) for (const [key, text] of Object.entries(entries)) flat[`${ns}.${key}`] = text;
}
export const BASE_LANGUAGE = idiomas.base;
export const languages = idiomas.idiomas.filter(l => dictionaries[l.codigo]);

/** Idioma elegido por el usuario (si lo hay) o el primero del sistema que tenga traducción; si no, el base. */
function detect(): string {
  const available = new Set(Object.keys(dictionaries));
  try { const saved = browserStorage()?.getItem('historicmap-idioma'); if (saved && available.has(saved)) return saved; } catch { /* sin almacenamiento */ }
  const wanted = typeof navigator === 'undefined' ? [] : [...(navigator.languages ?? []), navigator.language].filter(Boolean);
  for (const tag of wanted) { const code = tag.toLowerCase().split('-')[0]; if (available.has(code)) return code; }
  return BASE_LANGUAGE;
}
export const language = detect();
if (typeof document !== 'undefined') {
  document.documentElement.lang = language;
  document.documentElement.dir = idiomas.idiomas.find(l => l.codigo === language && 'direccion' in l) ? 'rtl' : 'ltr';
}

const active = dictionaries[language] ?? {}, base = dictionaries[BASE_LANGUAGE] ?? {};
/** Texto traducido. Las llaves {nombre} se sustituyen por los valores dados. */
export function tx(key: string, values?: Record<string, unknown>): string {
  const text = active[key] ?? base[key];
  if (text === undefined) { if (import.meta.env?.DEV) console.warn('i18n: falta la clave', key); return key; }
  return values ? text.replace(/\{(\w+)\}/g, (m, k: string) => (k in values ? String(values[k]) : m)) : text;
}
/** Cambia de idioma y recarga la aplicación (los textos se resuelven al cargar). */
export function setLanguage(code: string) {
  try { browserStorage()?.setItem('historicmap-idioma', code); } catch { /* sin almacenamiento */ }
  location.reload();
}
