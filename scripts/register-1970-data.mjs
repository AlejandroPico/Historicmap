import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url);
const manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const changes={
 'identities.json':{format:'dated-political-identities',transform:'Incremental dated authorities through 1970–1989, national and dissolved historical offices; existing 1990–2026 curations retained. Formal, party, de facto and rival authorities distinguished. All mandates intersecting selected year; precision and inferred upper bounds retained. Current reference remains 2026-10-22; historical acquisition 2026-10-23 does not extend current incumbents or flags. Separate VDR/RVN/VSR/RHO/YAR/YPR/USSR/DDR identities, no successor statistics. Licensed local portraits and dated symbols with individual media manifest SHA-256; collective authorities have no invented portrait. Sources and limitations in HISTORICAL-AUTHORITIES.'},
 'affiliations.json':{transform:'31 regional/intercontinental organizations, dated participation and category intervals, 1970–2026. End exclusive; annual map at Dec 31 capped at reference. Explicit coverage-floor flag, territorial applications and discontinuous EAC organizations; membership is not political subordination. Sources/precision per record; historical suspensions remain partial.'},
 'historical-context.json':{transform:'Selected sourced conflict/transition phases since 1970, start inclusive/end exclusive. Separate phases prevent later outcomes being brought backwards. Codes associate relevant country cards, not a formal belligerent register; no front geometry or peace inference from absent events.'},
 'historical-supplements.geojson':{transform:'23 unchanged Natural Earth contemporary reference contours for omitted small states and Western Sahara, 1970–2019 with individual documented independence/association starts. Coverage floor is not independence or UN admission. Pre-independence successors not retrojected. Morocco 1975+ and Mauritania 1975–1978 separately use intact CShapes 1974 source contours at runtime, with explicit source labels, to avoid claimed Sahara sectors in the recognized base.'},
 'country-history.json':{transform:'Curated dated institutions/history and directed entity-navigation relations. Expanded decolonization, constitutional transitions and Vietnamese identities through 1970. Record end exclusive, source/event date distinct from navigable annual map anchor. No automatic successor data inheritance or claim of complete institutional history.'},
 'political-influence.json':{format:'dated-political-influence',source:'Official historical and archival accounts; national institutions and ECCC',url:'https://history.state.gov/milestones/1989-1992/fall-of-communism',license:'Original factual compilation and editorial colour convention; sources per relationship',transform:'Dated selected satellite, client, bloc and military-intervention relationships. Tint dominant power colour without merging boundaries or sovereignty. Colonial administrator colours resolved from contemporaneous source entities. Occupation/intervention tint follows the occupations toggle. Alliances alone never imply subordination; incomplete worldwide inventory.'},
};
for(const [file,metadata] of Object.entries(changes)){
 const bytes=await readFile(new URL(file,root)),data=JSON.parse(bytes);
 const old=manifest.entries.find(e=>e.file===file)??{};
 const entry={...old,...metadata,file,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),version:`Historicmap 0.8.0; historical preparation 2026-10-23; reference ${data.referenceDate??data.retrieved??'per record'}`};
 if(data.countries){entry.countries=Object.keys(data.countries).length;entry.records=Object.values(data.countries).reduce((n,c)=>n+(c.leaders?.length??0),0);}
 if(data.organizations){entry.organizations=data.organizations.length;entry.records=data.organizations.reduce((n,o)=>n+o.memberships.length,0);}
 if(data.events)entry.records=data.events.length;
 if(data.features)entry.features=data.features.length;
 if(data.records)entry.records=data.records.length;
 if(data.relations)entry.relations=data.relations.length;
 manifest.entries=manifest.entries.filter(e=>e.file!==file);manifest.entries.push(entry);
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));
await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');
console.log('Registered 1970 expansion and dated political colour relationships.');
