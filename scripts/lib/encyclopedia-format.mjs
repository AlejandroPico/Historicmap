// Formato de las páginas de enciclopedia/: cabecera YAML reducida + Markdown.
// Módulo compartido por el compilador (Node) y el lector (navegador). Sin dependencias.

/** Convierte un escalar YAML reducido. */
function scalar(raw) {
  const v = raw.trim();
  if (v === '') return '';
  if (v === 'null' || v === '~') return null;
  if (v === 'true') return true;
  if (v === 'false') return false;
  if (/^-?\d+(\.\d+)?$/.test(v) && !/^-?0\d/.test(v)) return Number(v);
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) return v.slice(1, -1).replace(/\\"/g, '"');
  if (v.startsWith('[') && v.endsWith(']')) return splitInline(v.slice(1, -1)).map(scalar);
  if (v.startsWith('{') && v.endsWith('}')) {
    const o = {};
    for (const part of splitInline(v.slice(1, -1))) {
      const i = part.indexOf(':');
      if (i < 0) throw Error('Objeto en línea mal formado: ' + v);
      o[part.slice(0, i).trim()] = scalar(part.slice(i + 1));
    }
    return o;
  }
  return v;
}

/** Divide por comas de primer nivel, respetando comillas, corchetes y llaves. */
function splitInline(s) {
  const out = []; let depth = 0, quote = '', cur = '';
  for (const ch of s) {
    if (quote) { cur += ch; if (ch === quote) quote = ''; continue; }
    if (ch === '"' || ch === "'") { quote = ch; cur += ch; continue; }
    if (ch === '[' || ch === '{') depth++;
    if (ch === ']' || ch === '}') depth--;
    if (ch === ',' && depth === 0) { out.push(cur); cur = ''; continue; }
    cur += ch;
  }
  if (cur.trim()) out.push(cur);
  return out.map(x => x.trim()).filter(x => x !== '');
}

/** YAML reducido: mapas por sangría de 2 espacios, listas con «- », escalares y estructuras en línea. */
export function parseYaml(text) {
  const lines = text.split(/\r?\n/).map(l => l.replace(/\s+#\s.*$/, '')).filter(l => l.trim() !== '' && !l.trim().startsWith('#'));
  let i = 0;
  const indent = l => l.length - l.trimStart().length;
  function block(level) {
    if (i >= lines.length) return null;
    if (lines[i].trimStart().startsWith('- ') || lines[i].trim() === '-') {
      const arr = [];
      while (i < lines.length && indent(lines[i]) === level && lines[i].trimStart().startsWith('-')) {
        const rest = lines[i].trimStart().slice(1).trim();
        i++;
        if (rest === '') { arr.push(block(level + 2)); continue; }
        const m = /^([^\s:'"[{][^:]*):(\s+(.*))?$/.exec(rest);
        if (m && !rest.startsWith('{')) {
          // elemento de lista que es un mapa: «- clave: valor» y continuación con sangría
          const o = {}; o[m[1].trim()] = m[3] !== undefined && m[3].trim() !== '' ? scalar(m[3]) : block(level + 4);
          while (i < lines.length && indent(lines[i]) === level + 2 && !lines[i].trimStart().startsWith('-')) {
            const mm = /^([^:]+):(\s+(.*))?$/.exec(lines[i].trim()); i++;
            if (!mm) throw Error('Línea no válida en la cabecera: ' + lines[i - 1]);
            o[mm[1].trim()] = mm[3] !== undefined && mm[3].trim() !== '' ? scalar(mm[3]) : block(level + 4);
          }
          arr.push(o);
        } else arr.push(scalar(rest));
      }
      return arr;
    }
    const obj = {};
    while (i < lines.length && indent(lines[i]) === level) {
      const line = lines[i].trim();
      const m = /^([^:]+):(\s+(.*))?$/.exec(line);
      if (!m) throw Error('Línea no válida en la cabecera: ' + line);
      i++;
      const key = m[1].trim();
      if (m[3] !== undefined && m[3].trim() !== '') obj[key] = scalar(m[3]);
      else if (i < lines.length && indent(lines[i]) > level) obj[key] = block(indent(lines[i]));
      else obj[key] = null;
    }
    return obj;
  }
  const result = block(0) ?? {};
  if (i < lines.length) throw Error('Sangría inesperada en la cabecera: ' + lines[i]);
  return result;
}

/** Separa cabecera y cuerpo de una página. */
export function splitPage(source) {
  const text = source.replace(/^﻿/, '');
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(text);
  if (!m) throw Error('La página no empieza con una cabecera «---»');
  return { meta: parseYaml(m[1]), body: m[2] };
}

export const PAGE_TYPES = ['portada', 'guia', 'geologia', 'tierra', 'clima', 'vida', 'especie', 'humanidad', 'cultura', 'contexto', 'entidad', 'persona', 'evento', 'obra', 'tema', 'lista'];
export const ID_PATTERN = /^[a-z0-9][A-Za-z0-9-]*$/;

/**
 * Convierte una fecha de la cabecera en año civil (sin año cero; negativo = a. C.).
 * Admite: 1943 · -490 · "1943-05-01" · "-0490-09-12" · "201.4 Ma" · "4.54 Ga" · "11.7 ka" (antes de 1950).
 */
export function civilYear(value) {
  if (value === null || value === undefined || value === '') return null;
  if (typeof value === 'number') { if (!Number.isInteger(value) || value === 0) throw Error('Año civil no válido: ' + value); return value; }
  const s = String(value).trim().replace(',', '.');
  let m = /^(-?\d{1,})-(\d{2})-(\d{2})$/.exec(s);
  if (m) { const y = Number(m[1]); if (y === 0) throw Error('Año cero: ' + s); return y; }
  m = /^(\d+(?:\.\d+)?)\s*(Ga|Ma|ka)$/.exec(s);
  if (m) {
    const age = Number(m[1]) * (m[2] === 'Ga' ? 1e9 : m[2] === 'Ma' ? 1e6 : 1e3);
    const y = Math.round(1950 - age); return y <= 0 ? y - 1 : y;
  }
  m = /^-?\d+$/.exec(s);
  if (m) return civilYear(Number(s));
  throw Error('Fecha no reconocida: ' + s);
}

/** Enlaces internos «[[id]]» o «[[id|texto]]». */
export const LINK_PATTERN = /\[\[([A-Za-z0-9][A-Za-z0-9-]*)(?:\|([^\]]+))?\]\]/g;
export function internalLinks(body) { return [...body.matchAll(LINK_PATTERN)].map(m => m[1]); }

/** Normaliza para búsqueda: sin acentos ni mayúsculas. */
export const normalizeText = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

/** Resumen: primer párrafo de texto del cuerpo, sin marcas. */
export function firstParagraph(body) {
  for (const block of body.split(/\n\s*\n/)) {
    const t = block.trim();
    if (!t || /^(#|:::|\||!|>|-\s|\d+\.\s)/.test(t)) continue;
    return t.replace(LINK_PATTERN, (_, id, label) => label ?? id).replace(/\*\*|\*|`/g, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\s+/g, ' ');
  }
  return '';
}

/** Reparto estable en fragmentos para cargar bajo demanda. */
export function shardOf(key, count) {
  let h = 5381; for (const ch of String(key)) h = ((h * 33) ^ ch.charCodeAt(0)) >>> 0;
  return h % count;
}
export const PERSON_SHARDS = 64;
export const ENTITY_SHARDS = 32;
/** Siglo civil (sin año cero): 1–100 → 0, -100…-1 → -1. */
export const centuryOf = year => year > 0 ? Math.floor((year - 1) / 100) : -Math.floor((-year - 1) / 100) - 1;

/** Componentes visuales disponibles (debe coincidir con src/encyclopedia/components.ts). */
export const COMPONENT_NAMES = ['escala-geologica', 'reloj-geologico', 'curva-temperatura-fanerozoico', 'atmosfera', 'grafico', 'linea-tiempo', 'mapa', 'galeria'];
export const CALLOUT_KINDS = ['nota', 'debate', 'clave', 'curiosidad', 'cita'];
/** Bloques «:::tipo» usados en un cuerpo, con sus argumentos. */
export function blocksIn(body) { return [...body.matchAll(/^:::[ \t]*([a-z][a-z-]*)[ \t]*(.*)$/gm)].map(m => ({ kind: m[1], arg: m[2].trim() })); }
