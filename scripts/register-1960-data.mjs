import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url),manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const notes={
 'identities.json':'Incremental 1960–1969 office acquisition and focal reviewed terms/documentary coverage windows; preserve current reference 2026-10-22 and all previous curations. YMK/TAN/ZAN/UAR and UNTEA distinct, inclusive terms and documented boundary flags. Missing portraits remain explicit; licensed local media retain individual credits and hashes.',
 'territorial-administrations.json':'Dated external/local authority relationships from coverage floor 1960, with pre/post-1966 Namibia, Bahamian self-government, four protected states and effective UNTEA administration. No successor statistics inherited; national, local and external scope distinguished.',
 'affiliations.json':'Dated organizations from 1960; preserve later accessions, departures and categories. Coverage boundaries are not accession dates; military alliance never establishes subordination. Albania and earlier COMECON/OAS/Arab League participation distinguished.',
 'historical-context.json':'Focal conflict and transition phases expanded to 1960. Country keys associate a card, not a formal belligerent roster or front geometry. Incomplete worldwide; absence of event never establishes peace.',
 'historical-supplements.geojson':'Unchanged contemporary Natural Earth reference outlines for omitted entities from 1960, including pre-independence Kuwait/Bahrain as explicitly protected states. Independence dates distinct from reference geometry, coverage floors and UN admission. Existing Sahara exception retained.',
 'country-history.json':'Focal institutions and navigable transitions including UAR separation, Yemen revolution, Tanganyika/Zanzibar union, Singapore separation and selected decolonization. Event date distinct from map-year anchors; no automatic successor inheritance.'
};
for(const [file,transform] of Object.entries(notes)){
 const bytes=await readFile(new URL(file,root)),d=JSON.parse(bytes),old=manifest.entries.find(e=>e.file===file);
 const entry={...old,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),version:'Historicmap 0.9.0; historical preparation 2026-10-23; current reference 2026-10-22',transform};
 if(d.countries){entry.countries=Object.keys(d.countries).length;entry.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);}
 if(d.organizations){entry.organizations=d.organizations.length;entry.records=d.organizations.reduce((n,o)=>n+o.memberships.length,0);}
 if(d.events)entry.records=d.events.length;
 if(d.features)entry.features=d.features.length;
 if(d.records)entry.records=d.records.length;
 if(d.relations)entry.relations=d.relations.length;
 manifest.entries=manifest.entries.map(e=>e.file===file?entry:e);
}
await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');
const review=JSON.parse(await readFile(new URL('../.cache/coverage-1960.json',import.meta.url)));
await writeFile(new URL('../docs/REVIEW-1960.json',import.meta.url),JSON.stringify({reviewed:'2026-10-23',scope:'1960–1969 country-year resolver audit, including historical supplements. Does not certify all offices, exact tenure dates, photographic identity or historical geometry. Missing media are not replaced with invented/unlicensed images.',...review},null,2)+'\n');
console.log('Registered six revised resources and durable 1960 coverage gaps.');
