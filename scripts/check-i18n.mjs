// Comprueba la internacionalización: JSON válidos, claves usadas en el código presentes en el idioma base,
// claves sin uso y, para cada idioma traducido, claves que faltan, sobran o pierden sus marcadores {nombre}.
// Uso: node scripts/check-i18n.mjs  (sale con error si falta alguna clave del idioma base).
import fs from 'node:fs'; import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..'), dir = path.join(root, 'i18n');
const { base, idiomas } = JSON.parse(fs.readFileSync(path.join(dir, 'idiomas.json'), 'utf8'));
const load = lang => { const out = {}; const d = path.join(dir, lang); if (!fs.existsSync(d)) return null;
  for (const f of fs.readdirSync(d).filter(f => f.endsWith('.json'))) for (const [ns, e] of Object.entries(JSON.parse(fs.readFileSync(path.join(d, f), 'utf8')))) for (const [k, v] of Object.entries(e)) out[`${ns}.${k}`] = { v, f }; return out; };
const ref = load(base);
const used = new Set();
for (const f of fs.readdirSync(path.join(root, 'src'), { recursive: true }).filter(f => f.endsWith('.ts')))
  for (const m of fs.readFileSync(path.join(root, 'src', f), 'utf8').matchAll(/\btx\(\s*'([\w.]+)'/g)) used.add(m[1]);
const missing = [...used].filter(k => !ref[k]), unused = Object.keys(ref).filter(k => !used.has(k));
const marks = s => (s.match(/\{\w+\}/g) ?? []).sort().join();
console.log(`i18n · ${base}: ${Object.keys(ref).length} textos en ${new Set(Object.values(ref).map(r => r.f)).size} archivos; ${used.size} claves usadas en el código.`);
if (unused.length) console.log(`  ${unused.length} claves sin uso: ${unused.slice(0, 10).join(', ')}${unused.length > 10 ? '…' : ''}`);
for (const { codigo } of idiomas.filter(l => l.codigo !== base)) {
  const tr = load(codigo); if (!tr) continue;
  const lack = Object.keys(ref).filter(k => !tr[k]), extra = Object.keys(tr).filter(k => !ref[k]), bad = Object.keys(tr).filter(k => ref[k] && marks(tr[k].v) !== marks(ref[k].v));
  console.log(`  ${codigo}: ${Object.keys(tr).length - extra.length}/${Object.keys(ref).length} traducidos${lack.length ? `, faltan ${lack.length}` : ''}${extra.length ? `, sobran ${extra.length}` : ''}${bad.length ? `, marcadores distintos en ${bad.join(', ')}` : ''}`);
}
if (missing.length) { console.error(`Faltan en ${base}: ${missing.join(', ')}`); process.exit(1); }
