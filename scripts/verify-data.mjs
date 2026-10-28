import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const root = new URL('../public/data/',import.meta.url);
const manifest = JSON.parse(await readFile(new URL('manifest.json',root),'utf8'));
if(!manifest.entries.some(e=>e.file==='territorial-administrations.json'))throw Error('Missing territorial administration provenance');
for(const required of ['history.topojson','ww2.geojson','territorial-overlays.geojson','cities.geojson','profiles.json','early-modern.geojson','historical-control.geojson','spanish-civil-war.geojson','identities.json','affiliations.json','historical-context.json','historical-supplements.geojson','recent-control.geojson'])if(!manifest.entries.some(e=>e.file===required))throw Error(`Missing ${required}`);
for (const entry of manifest.entries) {
  const bytes = await readFile(new URL(entry.file,root));
  if (createHash('sha256').update(bytes).digest('hex') !== entry.sha256) throw new Error(`Checksum mismatch ${entry.file}`);
  for(const [input,expected] of Object.entries(entry.inputSha256??{}))if(createHash('sha256').update(await readFile(new URL(input,root))).digest('hex')!==expected)throw Error(`Stale prepared input ${entry.file}: ${input}`);
  const data = JSON.parse(bytes);
  if(entry.format==='dated-cultural-regions'){
    if(data.type!=='FeatureCollection'||data.features.length!==entry.features)throw Error('Invalid cultural regions');const ids=new Set();
    for(const f of data.features){const p=f.properties;if(ids.has(f.id)||!p.contextKey||!p.ownerKey||p.start>p.end||!p.dateBasis||!p.sourceYear||!p.spatialUncertainty||!p.temporalUncertainty||!p.references.length||!p.canonicalFile||!['cultural-region','polity-reference'].includes(p.kind))throw Error('Invalid cultural evidence '+f.id);ids.add(f.id);}
  }
  else if(entry.format==='cultural-coverage-index'){if(data.records.length!==entry.records||!data.windows.length||!data.reviewedThrough)throw Error('Invalid cultural coverage index');}
  else if (entry.format==='unquantized-topology') {if(data.type!=='Topology'||data.objects.countries.geometries.length!==entry.records)throw Error(`Invalid ${entry.file}`);}
  else if(entry.format==='dated-control-partitions'){
    if(data.format!==entry.format||Object.keys(data.years).join(',')!=='1940,1941,1942,1943,1944')throw Error('Invalid wartime partition coverage');
    for(const [year,p] of Object.entries(data.years)){
      const ids=new Set();
      for(const f of p.territories.features){if(f.id===undefined||ids.has(f.id)||!f.properties.identityKey||f.properties.uid||!['Polygon','MultiPolygon'].includes(f.geometry.type))throw Error('Invalid partition territory '+year);ids.add(f.id);}
      for(const f of p.occupations.features)if(!f.properties.controller||!f.properties.occupiedKey||!f.properties.occupiedColor)throw Error('Invalid final-owner hatching '+year);
    }
  }
  else if(entry.format==='dated-government-forms'){
    if(data.records.length!==entry.records||data.taxonomy.length!==entry.categories||!data.referenceDate)throw Error('Invalid governance catalogue');
    const tags=new Map(data.taxonomy.map(t=>[t.id,t]));if(tags.size!==data.taxonomy.length)throw Error('Duplicate government tag');
    const visit=(id,chain=[])=>{if(!tags.has(id)||chain.includes(id))throw Error('Invalid government hierarchy '+id);for(const p of tags.get(id).parents)visit(p,[...chain,id]);};
    for(const id of tags.keys())visit(id);
    for(const r of data.records)if(!r.keys.length||r.start>r.end||!r.source||r.tags.some(t=>!tags.has(t)))throw Error('Invalid government record');
  }
  else if(entry.format==='dated-regime-observations'){
    if(Object.keys(data.series).length!==entry.countries||!data.citation||!data.license||!data.source)throw Error('Missing regime provenance');let count=0;
    for(const runs of Object.values(data.series)){let last=-Infinity;for(const [a,b,v] of runs){if(a> b||a<=last||a<data.startYear||b>data.endYear||![0,1,2,3].includes(v))throw Error('Invalid regime interval');last=b;count++;}}
    if(count!==entry.records)throw Error('Regime interval count mismatch');
  }
  else if(entry.format==='dated-urban-references'){
    if(data.records.length!==entry.records||!data.referenceDate)throw Error('Invalid urban catalogue');const ids=new Set();
    for(const r of data.records){if(ids.has(r.id)||!r.keys.length||r.start>r.end||!r.source||!r.role||r.coordinates.length!==2||r.coordinates.some(n=>!Number.isFinite(n)))throw Error('Invalid urban reference '+r.id);ids.add(r.id);}
  }
  else if(entry.format==='country-indicator-series'){if(!data.countries.USA?.series.population?.length)throw Error('Missing country indicators');}
  else if(entry.format==='dated-entity-resolution'){
    if(data.format!==entry.format||data.records.length!==entry.records||!data.referenceDate||![[200,299],[300,399],[400,499],[500,599],[600,699],[700,799],[800,899],[900,999],[1000,1099],[1100,1199],[1200,1299],[1300,1399],[1400,1499],[1500,1599],[1600,1699],[1700,1799],[1800,1819],[1820,1839],[1840,1859],[1860,1879],[1880,1899]].some(([a,b])=>data.coverageStart===a&&data.coverageEnd===b))throw Error('Invalid dated entity resolution');
    for(const r of data.records)if(!r.names.length||!r.key||!r.source||!r.label||r.start<data.coverageStart||r.end>data.coverageEnd||r.start>r.end)throw Error('Invalid dated identity rule');
  }
  else if(entry.format==='dated-portrait-series'){
    if(!data.referenceDate||data.records.length!==entry.records)throw Error('Invalid dated portrait series');
    for(const r of data.records)if(!r.person||r.start>r.end||!r.source||!r.media.file||!r.dateLabel)throw Error('Invalid portrait interval');
  }
  else if(entry.format==='source-component-index'){
    if(!data.referenceDate||data.records.length!==entry.records)throw Error('Invalid source component index');
    const source=JSON.parse(await readFile(new URL('early-modern.geojson',root)));
    for(const r of data.records){const f=source.features.find(f=>f.id===r.sourceFeatureId),polys=f?.geometry.type==='Polygon'?[f.geometry.coordinates]:f?.geometry.coordinates;if(!polys||r.sourceComponentIndexes.some(i=>!polys[i]))throw Error('Missing source island component');}
  }
  else if(entry.format==='dated-political-identities'){if(Object.keys(data.countries).length!==entry.countries||Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0)!==entry.records||!data.retrieved)throw Error('Invalid dated identities');}
  else if(entry.format==='country-workspace-indicators'){
    if(Object.keys(data.indicators).length!==entry.indicators||Object.keys(data.countries).length!==entry.countries||!data.referenceDate)throw Error('Invalid country workspace indicators');
    let count=0;
    for(const [key,m] of Object.entries(data.indicators))if(!m.source||!m.license||!m.unit||!m.description||!['economy','society','defense'].includes(m.section))throw Error(`Missing indicator provenance ${key}`);
    for(const [code,series] of Object.entries(data.countries))for(const [key,values] of Object.entries(series)){
      const seen=new Set();for(const [year,value] of values){if(!data.indicators[key]||!Number.isInteger(year)||year<1960||year>Number(data.referenceDate.slice(0,4))||seen.has(year)||!Number.isFinite(value)||(value<0&&!data.indicators[key].allowNegative))throw Error(`Invalid observation ${code}:${key}:${year}`);seen.add(year);count++;}
    }
    if(count!==entry.records)throw Error('Indicator record count mismatch');
  }
  else if(entry.format==='country-workspace-history'){
    if(data.records.length!==entry.records||data.relations.length!==entry.relations||!data.referenceDate)throw Error('Invalid country workspace history');
    const ids=new Set();for(const r of [...data.records,...data.relations]){if(!r.id||ids.has(r.id)||!r.source||!r.sourceLabel)throw Error('Invalid country history provenance');ids.add(r.id);}
    for(const r of data.records)if(!r.keys.length||!r.start||(r.end&&r.end<=r.start))throw Error(`Invalid institutional interval ${r.id}`);
    for(const r of data.relations)if(!r.date||!r.from.key||!r.to.key||!Number.isInteger(r.from.year)||!Number.isInteger(r.to.year))throw Error(`Invalid entity relation ${r.id}`);
  }
  else if(entry.format==='dated-territorial-administrations'){
    if(!data.referenceDate||data.records.length!==entry.records)throw Error('Invalid territorial administrations');
    const ids=new Set();for(const r of data.records){if(ids.has(r.id)||!r.admin||!r.source||!r.note||!r.label||!r.names.length||!r.start||(r.end&&r.start>=r.end))throw Error('Invalid territorial administration '+r.id);ids.add(r.id);}
  }
  else if(entry.format==='dated-political-influence'){
    if(data.records.length!==entry.records||!data.referenceDate)throw Error('Invalid political influence catalogue');
    const ids=new Set();
    for(const r of data.records){
      if(ids.has(r.id)||!r.keys.length||!r.power||!r.source||!r.note||r.start>=r.end)throw Error(`Invalid political relationship ${r.id}`);
      ids.add(r.id);
      for(const other of data.records)if(r.id!==other.id&&r.keys.some(k=>other.keys.includes(k))&&r.start<other.end&&other.start<r.end)throw Error(`Ambiguous political relationships ${r.id}/${other.id}`);
    }
  }
  else if(entry.format==='dated-organizations'){
    if(data.organizations.length!==entry.organizations||!data.referenceDate)throw Error('Invalid organization catalogue');
    for(const o of data.organizations){if(!o.formed||!o.source||!o.label)throw Error(`Missing organization provenance ${o.id}`);for(const m of o.memberships)if(!m.code||!m.source||!m.start||(m.end&&m.end<=m.start))throw Error(`Invalid membership ${o.id}:${m.code}`);}
  }
  else if(entry.format==='dated-historical-context'){
    if(data.events.length!==entry.records||!data.referenceDate)throw Error('Invalid historical contexts');
    for(const e of data.events)if(!e.id||!e.source||!e.text||!e.start||!e.countries.length||(e.end&&e.end<=e.start))throw Error(`Invalid event ${e.id}`);
  }
  else if (data.type !== 'FeatureCollection' || data.features.length !== entry.features) throw new Error(`Invalid ${entry.file}`);
  if (!entry.license || !entry.url || !entry.version) throw new Error(`Missing provenance ${entry.file}`);
}
const fontsRoot=new URL('../public/fonts/',import.meta.url);
const fonts=JSON.parse(await readFile(new URL('manifest.json',fontsRoot)));
for(const entry of fonts.entries){const bytes=await readFile(new URL(entry.file,fontsRoot));if(createHash('sha256').update(bytes).digest('hex')!==entry.sha256)throw Error(`Invalid glyphs ${entry.file}`);}
const media=JSON.parse(await readFile(new URL('../public/media/manifest.json',import.meta.url)));
const files=new Set();
for(const m of media.entries){
 if(!/^media\/[a-z0-9-]+\.(svg|png|jpg|webp|gif)$/.test(m.file)||!m.license||!m.url)throw Error(`Incomplete media provenance ${m.file}`);
 if(m.license.includes('ND')&&(m.display!=='full-frame'||!m.licenseUrl||!m.attributionRequired))throw Error(`No-derivatives image requires full-frame display and license ${m.file}`);
 const bytes=await readFile(new URL('../public/'+m.file,import.meta.url));
 if(createHash('sha256').update(bytes).digest('hex')!==m.sha256||bytes.length!==m.bytes)throw Error(`Invalid media ${m.file}`);
 files.add(m.file);
}
const identities=JSON.parse(await readFile(new URL('identities.json',root)));
const portraits=JSON.parse(await readFile(new URL('portrait-series.json',root)));
for(const r of portraits.records)if(!files.has(r.media.file))throw Error('Unregistered dated portrait '+r.media.file);
for(const [key,country] of Object.entries(identities.countries)){
 for(const f of [...country.flags,...country.symbolReferences??[]]){if(f.start>f.end||!files.has(f.media.file)||f.media.referenceOnly&&!f.media.evidenceDate)throw Error(`Invalid symbol interval or image ${key}: ${f.start}/${f.end} ${f.media.file}`);}
 for(const l of country.leaders){if(l.start>l.end||!l.name||!l.role||!l.source||(l.portrait&&!files.has(l.portrait.file)))throw Error('Invalid leadership interval or image');}
}
console.log(`Verified ${manifest.entries.length} data resources, ${fonts.entries.length} glyph ranges and ${files.size} licensed media with SHA-256.`);
