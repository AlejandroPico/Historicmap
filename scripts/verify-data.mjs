import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const root = new URL('../public/data/',import.meta.url);
const manifest = JSON.parse(await readFile(new URL('manifest.json',root),'utf8'));
for(const required of ['history.topojson','ww2.geojson','territorial-overlays.geojson','cities.geojson','profiles.json','early-modern.geojson','historical-control.geojson','spanish-civil-war.geojson','identities.json'])if(!manifest.entries.some(e=>e.file===required))throw Error(`Missing ${required}`);
for (const entry of manifest.entries) {
  const bytes = await readFile(new URL(entry.file,root));
  if (createHash('sha256').update(bytes).digest('hex') !== entry.sha256) throw new Error(`Checksum mismatch ${entry.file}`);
  const data = JSON.parse(bytes);
  if (entry.format==='unquantized-topology') {if(data.type!=='Topology'||data.objects.countries.geometries.length!==entry.records)throw Error(`Invalid ${entry.file}`);}
  else if(entry.format==='country-indicator-series'){if(!data.countries.USA?.series.population?.length)throw Error('Missing country indicators');}
  else if(entry.format==='dated-political-identities'){if(Object.keys(data.countries).length!==entry.countries||!data.retrieved)throw Error('Invalid dated identities');}
  else if (data.type !== 'FeatureCollection' || data.features.length !== entry.features) throw new Error(`Invalid ${entry.file}`);
  if (!entry.license || !entry.url || !entry.version) throw new Error(`Missing provenance ${entry.file}`);
}
const fontsRoot=new URL('../public/fonts/',import.meta.url);
const fonts=JSON.parse(await readFile(new URL('manifest.json',fontsRoot)));
for(const entry of fonts.entries){const bytes=await readFile(new URL(entry.file,fontsRoot));if(createHash('sha256').update(bytes).digest('hex')!==entry.sha256)throw Error(`Invalid glyphs ${entry.file}`);}
const media=JSON.parse(await readFile(new URL('../public/media/manifest.json',import.meta.url)));
const files=new Set();
for(const m of media.entries){
 if(!/^media\/[a-z0-9-]+\.(svg|png|jpg)$/.test(m.file)||!m.license||!m.url)throw Error(`Incomplete media provenance ${m.file}`);
 const bytes=await readFile(new URL('../public/'+m.file,import.meta.url));
 if(createHash('sha256').update(bytes).digest('hex')!==m.sha256||bytes.length!==m.bytes)throw Error(`Invalid media ${m.file}`);
 files.add(m.file);
}
const identities=JSON.parse(await readFile(new URL('identities.json',root)));
for(const country of Object.values(identities.countries)){
 for(const f of country.flags){if(f.start>f.end||!files.has(f.media.file))throw Error('Invalid flag interval or image');}
 for(const l of country.leaders){if(l.start>l.end||!l.name||!l.role||!l.source||(l.portrait&&!files.has(l.portrait.file)))throw Error('Invalid leadership interval or image');}
}
console.log(`Verified ${manifest.entries.length} data resources, ${fonts.entries.length} glyph ranges and ${files.size} licensed media with SHA-256.`);
