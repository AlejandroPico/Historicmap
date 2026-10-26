/** Register this delivery only; never rewrite checksums of untouched source assets. */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=f=>JSON.parse(readFileSync('public/data/'+f,'utf8'));
const manifest=read('manifest.json');
const added={
 'historical-1860-entities.json':['dated-entity-resolution','Cliopatria and dated editorial identity corrections','https://github.com/Seshat-Global-History-Databank/cliopatria','CC0 factual identity metadata','Bounded1860–1879 names and regimes over unchanged source contours; annual synthesis, not monthly frontier reconstruction.'],
 'pacific-components.json':['source-component-index','Cliopatria components identified with Natural Earth envelopes','https://github.com/Seshat-Global-History-Databank/cliopatria','CC BY4.0','Indexes split Guam and New Caledonia from colonial aggregates without changing or duplicating source polygon coordinates.'],
 'pacific-references.geojson':['geojson','Natural Earth reference land and sourced territorial status metadata','https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/','Natural Earth public domain; CC0 factual metadata','Date-bounded reference contours for omitted Pacific islands. Present contours are not reconstructed historic coastlines; uncertain local and joint governments explicitly remain unresolved.'],
 'ukraine-control-2022.geojson':['geojson','Viewsridge and Wikimedia Commons contributors; Historicmap georeferencing','https://commons.wikimedia.org/wiki/File:2022_Russian_invasion_of_Ukraine.svg','CC BY-SA4.0; Natural Earth land public domain','Five archived observations2022–2026, affine georeferencing with16 city controls and minimum7km uncertainty. Solid occupation fills only, clipped to Natural Earth land, no CShapes inputs. The2026 observation remains17December2025; source revisionApril2026 is not a new territorial assessment. Full attribution and archival source checksums in the data and research document.'],
 'portrait-series.json':['dated-portrait-series','Individually licensed Wikimedia Commons images','https://commons.wikimedia.org/','CC0 factual windows; images each retain their own recorded license','32 representative portrait windows after office resolution. Photo dates remain separate from selection year; unknown date labelled. Original bytes preserved; licensed framing declared.']
};
for(const [file,[format,source,url,license,transform]] of Object.entries(added)){
 let e=manifest.entries.find(e=>e.file===file);if(!e){e={file};manifest.entries.push(e);}Object.assign(e,{format,source,url,license,transform});
}
for(const file of ['identities.json','historical-context.json','country-history.json',...Object.keys(added)]){
 const bytes=readFileSync('public/data/'+file),d=JSON.parse(bytes),e=manifest.entries.find(e=>e.file===file);
 Object.assign(e,{sha256:createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length,version:'Historicmap0.14.0; preparation2026-10-26; contemporary office reference2026-10-22 unchanged'});
 if(d.records)e.records=d.records.length;if(d.events)e.records=d.events.length;if(d.relations)e.relations=d.relations.length;if(d.features)e.features=d.features.length;
 if(d.countries){e.countries=Object.keys(d.countries).length;e.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);}
 if(file==='identities.json')e.transform='Isolated1860–1879 acquisition plus bounded sourced curator; earlier published1880+ offices preserved.225 newly acquired portraits and reused earlier media; availability does not establish a complete worldwide census. See REVIEW-1860-1879.';
 if(file==='historical-context.json'||file==='country-history.json')e.transform='Sourced1860–1879 phases, institutional events and predecessor navigation appended idempotently. Earlier records unchanged; documentary context is not geometric front data.';
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));writeFileSync('public/data/manifest.json',JSON.stringify(manifest,null,2)+'\n');
