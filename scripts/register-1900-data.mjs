import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url),manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const version=JSON.parse(await readFile(new URL('../package.json',import.meta.url))).version;
const descriptions={
 'identities.json':'Isolated incremental worldwide1900–1919 acquisition and sourced focal authority windows. Imperial, republican, local/protector and collective offices distinguished; licensed media and later curations preserved. Contemporary reference2026-10-22 unchanged. Resolver coverage is not an exhaustive daily census.',
 'territorial-administrations.json':'Dated administrative coverage from1900, including Korean protection/annexation, Boer colonies, Moroccan protectorate, Tonga and Congo1908 transfer. Coverage boundaries differ from legal inception. External national offices do not substitute complete local governor series.',
 'historical-supplements.geojson':'26 unchanged Natural Earth contemporary reference contours for source omissions from1900, including protected Tonga before1970 and Vatican only from7June1929. Coverage floors and statehood dates are distinct; not reconstructed historical coastlines.',
 'affiliations.json':'41 dated organizations/groupings; Triple Alliance and WWI Central/Allied-associated powers added to prior memberships. Legal dates, categories and coverage boundaries explicit; neutral treaty partners are not automatically active belligerents or dependencies.',
 'historical-context.json':'48 additional sourced phases1900–1919, including imperial regimes, revolutions, colonial transitions and WWI. Not a worldwide daily front-line or conflict census.',
 'country-history.json':'Dated institutions and predecessor links from1900, including imperial transitions, WWI treaties and early international institutions. Documentary windows are not exact constitutional inception dates; PCA/ITU/UPU records are not fabricated historical member rosters.'
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
const review=JSON.parse(await readFile(new URL('../.cache/coverage-1900-1919.json',import.meta.url)));
const uniquePortraits=new Map(review.decades.flatMap(d=>d.missingPortraits.map(p=>[p.person,p])));
await writeFile(new URL('../docs/REVIEW-1900-1919.json',import.meta.url),JSON.stringify({reviewed:'2026-10-24',scope:'1900–1919 annual source-country and active-control resolver audit, including reference supplements. Counts mean availability of some authority or documented institutional absence, not exhaustive daily offices, photographic identity assurance or exact military fronts. Portrait gaps deduplicated across decades.',uniqueMissingPortraits:[...uniquePortraits.values()],...review},null,2)+'\n');
console.log('Registered six revised resources and1900–1919 nominal coverage gaps.');
