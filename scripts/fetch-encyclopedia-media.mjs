#!/usr/bin/env node
// Descarga imágenes de Wikimedia Commons para la enciclopedia con su autor, licencia y fuente.
// Uso: node scripts/fetch-encyclopedia-media.mjs "File:Nombre.jpg" carpeta/archivo.jpg [--ancho 1280] [--pie "texto"]
//      node scripts/fetch-encyclopedia-media.mjs --lista lista.txt    (una línea por imagen: «File:… | carpeta/archivo.jpg | pie»)
// Solo admite licencias libres (dominio público, CC0, CC BY, CC BY-SA). Escribe en enciclopedia/medios/ y en creditos.json.
import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const MEDIA = join(ROOT, 'enciclopedia', 'medios');
const CREDITS = join(MEDIA, 'creditos.json');
const UA = 'HistoricmapEncyclopedia/1.0 (https://github.com/AlejandroPico/Historicmap)';
const FREE = /^(public domain|pd|cc0|cc[ -]by(-sa)?[ -]?\d(\.\d)?|cc[ -]by(-sa)?|attribution|gfdl)/i;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const strip = html => String(html ?? '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#0?39;/g, "'").replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();

async function get(url, binary = false) {
  for (let attempt = 0; attempt < 6; attempt++) {
    const res = await fetch(url, { headers: { 'User-Agent': UA } });
    if (res.status === 429 || res.status >= 500) { await sleep(2000 * 2 ** attempt); continue; }
    if (!res.ok) throw Error(`${res.status} ${url}`);
    return binary ? Buffer.from(await res.arrayBuffer()) : res.json();
  }
  throw Error('Demasiados reintentos: ' + url);
}

export async function fetchCommons(file, dest, { width = 1280, caption = '' } = {}) {
  const title = file.startsWith('File:') ? file : 'File:' + file;
  const api = `https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata|mime&iiurlwidth=${width}&titles=${encodeURIComponent(title)}`;
  const data = await get(api);
  const page = Object.values(data.query.pages)[0];
  const info = page?.imageinfo?.[0];
  if (!info) throw Error('No existe en Commons: ' + title);
  const meta = info.extmetadata ?? {};
  const license = strip(meta.LicenseShortName?.value) || strip(meta.License?.value);
  if (!FREE.test(license)) throw Error(`Licencia no admitida (${license || 'desconocida'}): ${title}`);
  const bytes = await get(info.thumburl ?? info.url, true);
  const target = join(MEDIA, dest);
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, bytes);
  const credits = existsSync(CREDITS) ? JSON.parse(readFileSync(CREDITS, 'utf8')) : {};
  credits[dest] = {
    titulo: caption || strip(meta.ObjectName?.value) || title.slice(5),
    autor: strip(meta.Artist?.value) || 'Autor no identificado',
    licencia: license, licenciaUrl: meta.LicenseUrl?.value ?? '',
    fuente: info.descriptionurl, archivo: title, consultado: new Date().toISOString().slice(0, 10)
  };
  writeFileSync(CREDITS, JSON.stringify(Object.fromEntries(Object.entries(credits).sort()), null, 2) + '\n');
  return credits[dest];
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2), opt = name => { const i = args.indexOf(name); return i >= 0 ? args.splice(i, 2)[1] : undefined; };
  const width = Number(opt('--ancho') ?? 1280), list = opt('--lista'), caption = opt('--pie') ?? '';
  const jobs = list ? readFileSync(list, 'utf8').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#')).map(l => l.split('|').map(s => s.trim())) : [[args[0], args[1], caption]];
  let failed = 0;
  for (const [file, dest, cap = ''] of jobs) {
    if (!file || !dest) { console.error('Uso: fetch-encyclopedia-media.mjs "File:…" carpeta/archivo.jpg'); process.exit(2); }
    try { const c = await fetchCommons(file, dest, { width, caption: cap }); console.log(`✓ ${dest} · ${c.autor} · ${c.licencia}`); }
    catch (e) { failed++; console.error(`✗ ${file}: ${e.message}`); }
    await sleep(800);
  }
  process.exit(failed ? 1 : 0);
}
