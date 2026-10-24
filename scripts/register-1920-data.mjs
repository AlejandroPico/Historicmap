import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url),manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const version=JSON.parse(await readFile(new URL('../package.json',import.meta.url))).version;
const descriptions={
 'identities.json':'Incremental worldwide1920–1949 acquisition and sourced documentary windows; RSR/ROC/YKM/DAN/TIB/RSI historical keys, formal/dominant offices and collective occupation administrations. Licensed media, later curations, missing portraits and current reference2026-10-22 preserved. Resolver coverage is not an exhaustive daily census.',
 'territorial-administrations.json':'Dated administrative relationships from1920; French colonies/departments distinguished in1946 and Austria under German control1938–1945. External national offices do not substitute a complete local-governor series or transfer statistics.',
 'historical-supplements.geojson':'Unchanged Natural Earth contemporary reference outlines for source omissions from1920, including Vatican only from7June1929. Coverage floors and statehood dates are distinct from UN admission; not a reconstructed historical coastline.',
 'affiliations.json':'38 dated organizations including League of Nations and UN succession/representation. Legal accessions, foundation/signature, entry into force, withdrawals and coverage boundaries are explicit. No automatic inference of subordination or belligerency.',
 'historical-context.json':'Fifty additional sourced phases1920–1949, including interwar regimes, WWII, occupation, independence and civil wars. Not a worldwide daily military-front or conflict census.',
 'country-history.json':'Dated institutions and links for interwar predecessor entities, League/UN, partitions and occupation transitions. Documentary windows do not assert exact constitutional inception or termination dates.'
};
for(const [file,transform] of Object.entries(descriptions)){
 const bytes=await readFile(new URL(file,root)),data=JSON.parse(bytes),entry=manifest.entries.find(e=>e.file===file);
 Object.assign(entry,{bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),version:`Historicmap ${version}; historical preparation2026-10-24; current reference2026-10-22`,transform});
 if(data.countries){entry.countries=Object.keys(data.countries).length;entry.records=Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0);}
 if(data.organizations){entry.organizations=data.organizations.length;entry.records=data.organizations.reduce((n,o)=>n+o.memberships.length,0);}
 if(data.events)entry.records=data.events.length;
 if(data.features)entry.features=data.features.length;
 if(data.records)entry.records=data.records.length;
 if(data.relations)entry.relations=data.relations.length;
}
await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');
const review=JSON.parse(await readFile(new URL('../.cache/coverage-1920-1949.json',import.meta.url)));
const uniquePortraits=new Map(review.decades.flatMap(d=>d.missingPortraits.map(p=>[p.person,p])));
await writeFile(new URL('../docs/REVIEW-1920-1949.json',import.meta.url),JSON.stringify({reviewed:'2026-10-24',scope:'1920–1949 annual source-country and active-control resolver audit, including reference supplements. Counts represent resolver availability, not exhaustive daily offices, portrait identity assurance or historically exact front lines. Portrait gaps deduplicated across all decades.',uniqueMissingPortraits:[...uniquePortraits.values()],...review},null,2)+'\n');
console.log('Registered six revised resources and1920–1949 nominal coverage gaps.');
