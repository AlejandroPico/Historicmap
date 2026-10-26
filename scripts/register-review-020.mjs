/** Register changed release resources, preserving earlier geographic files. */
import{readFileSync,writeFileSync}from'node:fs';import{createHash}from'node:crypto';
const read=p=>JSON.parse(readFileSync(p,'utf8')),save=(p,d)=>writeFileSync(p,JSON.stringify(d,null,2)+'\n');
for(const p of ['package.json','package-lock.json']){const d=read(p);d.version='0.20.0';if(d.packages?.[''])d.packages[''].version=d.version;save(p,d);}
const m=read('public/data/manifest.json');
if(!m.entries.some(e=>e.file==='historical-1600-entities.json'))m.entries.push({file:'historical-1600-entities.json',format:'dated-entity-resolution',source:'Date-scoped identity and administration rules over original Cliopatria geometry',url:'https://github.com/AlejandroPico/Historicmap/blob/main/docs/RESEARCH-1600.md',license:'CC0 factual metadata and editorial compilation',coverageStart:1600,coverageEnd:1699});
const changed=new Set(['early-modern-1600.geojson','historical-1600-entities.json','identities.json','governance.json','historical-places.json','historical-context.json','country-history.json','conflict-points.geojson']);
for(const e of m.entries)if(changed.has(e.file)){
 const raw=readFileSync('public/data/'+e.file),d=JSON.parse(raw);Object.assign(e,{sha256:createHash('sha256').update(raw).digest('hex'),bytes:raw.length,version:'Historicmap0.20.0; reference2026-10-26'});
 if(d.features)e.features=d.features.length;if(d.records)e.records=d.records.length;if(d.events){e.records=d.events.length;delete e.events;}if(d.taxonomy)e.categories=d.taxonomy.length;
 if(e.file==='identities.json'){e.countries=Object.keys(d.countries).length;e.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);e.transform='Isolated1600–1699 acquisition and reviewed sovereign titles, rival claims, regencies and calendars. Dated symbols distinguish ensigns, seals and dynastic devices; earlier mandate facts and symbol windows conserved. Not a complete world census.';}
 if(e.file==='historical-1600-entities.json')e.transform='Canonical date-scoped identities1600–1699, dynastic unions, Ming/Qing and interregnum, with source defects disclosed; original coordinate arrays unchanged.';
}
m.entries.sort((a,b)=>a.file.localeCompare(b.file));save('public/data/manifest.json',m);console.log('Registered',m.entries.length,'data resources;',read('public/media/manifest.json').entries.length,'media');
