/** Register release metadata after the reviewed data/media writers have finished. */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=p=>JSON.parse(readFileSync(p,'utf8')),save=(p,d)=>writeFileSync(p,JSON.stringify(d,null,2)+'\n');
for(const file of ['package.json','package-lock.json']){const d=read(file);d.version='0.18.0';if(d.packages?.[''])d.packages[''].version='0.18.0';save(file,d);}
const manifest=read('public/data/manifest.json');
const added=[
 ['governance.json','dated-government-forms','CC0 factual metadata and editorial taxonomy','https://www.wikidata.org/','Dated P122/P31 claims, broad historical forms bounded by entity lifetime, reviewed constitutional phases; unknown retained explicitly. Institutional form is distinct from regime assessment.'],
 ['regimes-of-world.json','dated-regime-observations','CC BY-SA 4.0; V-Dem2026 v16, OWID processing','https://ourworldindata.org/grapher/political-regime','Annual Regimes of the World observations1789–2025 compressed losslessly into intervals; explicit historical crosswalks, no extrapolation2026, no colonial democratic assessment inherited from administrator.'],
 ['historical-places.json','dated-urban-references','CC0 factual coordinate/date references and editorial compilation','https://github.com/AlejandroPico/Historicmap/blob/main/docs/REVIEW-0.18.md','Dated capitals, courts, regional colonial seats and selected cities, matched only to active identities; no historical population or city footprint inferred.'],
 ['conflict-points.geojson','geojson','CC0 factual coordinate/date references and editorial compilation','https://github.com/AlejandroPico/Historicmap/blob/main/docs/REVIEW-0.18.md','Battle sites and explicitly labelled regional conflict references; approximate point anchors, never occupation polygons or reconstructed fronts.'],
];
for(const [file,format,license,url,transform] of added){
 const d=read('public/data/'+file);let entry=manifest.entries.find(e=>e.file===file);if(!entry){entry={file};manifest.entries.push(entry);}
 Object.assign(entry,{format,license,url,source:format==='dated-regime-observations'?d.citation:'Per-record dated documentary sources',version:'Historicmap0.18.0; reference2026-10-26',transform});
 if(d.features)entry.features=d.features.length;else if(d.records)entry.records=d.records.length;else entry.records=Object.values(d.series).reduce((n,r)=>n+r.length,0);
 if(d.taxonomy)entry.categories=d.taxonomy.length;if(d.series)entry.countries=Object.keys(d.series).length;
}
const changed=new Set(['identities.json','historical-1800-entities.json','historical-1820-entities.json','historical-1840-entities.json','historical-1860-entities.json','historical-1880-entities.json',...added.map(r=>r[0])]);
for(const e of manifest.entries){
 if(changed.has(e.file)){
  const bytes=readFileSync('public/data/'+e.file),d=JSON.parse(bytes);e.bytes=bytes.length;e.sha256=createHash('sha256').update(bytes).digest('hex');e.version='Historicmap0.18.0; reference2026-10-26';
  if(e.file==='identities.json'){e.countries=Object.keys(d.countries).length;e.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);e.transform='Reviewed1800–1900 sovereign offices, source identity repairs and dated symbol variants; prior authorities and images preserved except documented duplicate corrections. Original geometry unchanged.';}
  else if(d.records)e.records=d.records.length;
 }
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));save('public/data/manifest.json',manifest);
const media=read('public/media/manifest.json');console.log('Registered',manifest.entries.length,'resources,',media.entries.length,'media');
