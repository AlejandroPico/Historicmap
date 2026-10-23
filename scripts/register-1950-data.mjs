import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url),manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const version=JSON.parse(await readFile(new URL('../package.json',import.meta.url))).version;
const descriptions={
 'identities.json':'Incremental1950–1959 acquisition, focal reviewed terms and documentary windows. State of Vietnam and Federation of Malaya separate from successors; formal and dominant offices distinguished. Earlier curations, current reference2026-10-22, licensed portraits and known gaps preserved.',
 'territorial-administrations.json':'Dated territorial relationships from1950, including distinct pre/post1952 Puerto Rico and pre/post1954 Surinam constitutional frameworks. External national offices never replace unresearched local governors or transfer successor statistics.',
 'historical-supplements.geojson':'Unchanged contemporary Natural Earth reference outlines for source omissions from1950; explicit coverage floors and dates of independence, not UN admission dates or historic coastline reconstruction.',
 'affiliations.json':'Dated organizations from1950, including CECA, Euratom, ANZUS, SEATO and Baghdad/CENTO. Category and legal accession separated from coverage windows; no inference of subordination or belligerency. Cuban Government exclusion dated1962, not1960.',
 'historical-context.json':'Focal1950s conflicts/transitions with source dates and documentary windows, including Korea, Indochina, Suez, Hungary, Taiwan and decolonization. Not a worldwide conflict census or military front reconstruction.',
 'country-history.json':'Focal dated institutions and transitions for1950s independence, political unions and predecessor entities. Context coverage dates are not automatically constitutional inception or termination dates.'
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
const review=JSON.parse(await readFile(new URL('../.cache/coverage-1950.json',import.meta.url)));
await writeFile(new URL('../docs/REVIEW-1950.json',import.meta.url),JSON.stringify({reviewed:'2026-10-24',scope:'1950–1959 country-year resolver audit, including supplements. Does not certify every office, daily succession, identification of every portrait or exhaustive historical borders.',...review},null,2)+'\n');
console.log('Registered six revised resources and1950 coverage gaps.');
