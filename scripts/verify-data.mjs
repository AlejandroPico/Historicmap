import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const root = new URL('../public/data/',import.meta.url);
const manifest = JSON.parse(await readFile(new URL('manifest.json',root),'utf8'));
for(const required of ['history.topojson','ww2.geojson','territorial-overlays.geojson','cities.geojson','profiles.json'])if(!manifest.entries.some(e=>e.file===required))throw Error(`Missing ${required}`);
for (const entry of manifest.entries) {
  const bytes = await readFile(new URL(entry.file,root));
  if (createHash('sha256').update(bytes).digest('hex') !== entry.sha256) throw new Error(`Checksum mismatch ${entry.file}`);
  const data = JSON.parse(bytes);
  if (entry.format==='unquantized-topology') {if(data.type!=='Topology'||data.objects.countries.geometries.length!==entry.records)throw Error(`Invalid ${entry.file}`);}
  else if(entry.format==='country-indicator-series'){if(!data.countries.USA?.series.population?.length)throw Error('Missing country indicators');}
  else if (data.type !== 'FeatureCollection' || data.features.length !== entry.features) throw new Error(`Invalid ${entry.file}`);
  if (!entry.license || !entry.url || !entry.version) throw new Error(`Missing provenance ${entry.file}`);
}
const fontsRoot=new URL('../public/fonts/',import.meta.url);
const fonts=JSON.parse(await readFile(new URL('manifest.json',fontsRoot)));
for(const entry of fonts.entries){const bytes=await readFile(new URL(entry.file,fontsRoot));if(createHash('sha256').update(bytes).digest('hex')!==entry.sha256)throw Error(`Invalid glyphs ${entry.file}`);}
console.log(`Verified ${manifest.entries.length} data resources and ${fonts.entries.length} local glyph ranges, provenance and SHA-256.`);
