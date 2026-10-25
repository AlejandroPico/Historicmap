/** Register only the resources revised by this extension; older input hashes stay intact. */
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url),manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
const version=JSON.parse(await readFile(new URL('../package.json',import.meta.url))).version;
const descriptions={
 'identities.json':'Isolated1880–1899 acquisition, sourced regional curations and explicitly reported later identity/portrait corrections. Real-human eligibility rejects fictional holders of real offices. Original1900+ curations preserved apart from documented requested corrections; current reference2026-10-22 unchanged. Availability is not an exhaustive daily office census.',
 'affiliations.json':'Dated coverage from1880; three earlier Triple Alliance membership windows added, preserving later903 memberships and organization metadata. Ratification exchange30May1882 distinct from signature20May. Membership does not establish dependency or belligerency.',
 'historical-context.json':'Sourced phases1880–1899 appended without changing earlier contemporary reference or prior events. Documentary phases do not supply geographic fronts.',
 'country-history.json':'Institutions, events and predecessor navigation extended1880–1899 with dated sources; existing records preserved.',
 'historical-1880-entities.json':'Date-scoped correction of anachronistic source names and QIDs over unchanged source contours. Cliopatria1880–1885 and CShapes1886–1899 are different geographic inventories. Unresolved source references remain explicitly unassigned.',
 'historical-1880-administrations.json':'Seventeen bounded relationships including local/native institutions and external national offices. Greenland omission correction extends through2019 and distinguishes1953,1979,2009; not a fabricated independence or complete governor series.',
 'historical-1880-supplements.geojson':'Nine unchanged reference features for omitted entities. Natural Earth contemporary contours explicitly labelled as references, plus Cliopatria1885 Hawaii. Greenland1886–2019 is an omission correction; other additions stop before1900.',
 'historical-1880-control.geojson':'Hawaii incorporation1898–1899 uses the exact dated CShapes island contour, avoiding fragments from different coastlines. Integrated in the USA selectable territory; not an opaque visual overlay and not statehood in1898.'
};
const source={
 'historical-1880-entities.json':['Editorial identity resolution; Cliopatria and institutional historical sources','https://github.com/Seshat-Global-History-Databank/cliopatria','CC0 identity metadata; editorial corrections'],
 'historical-1880-administrations.json':['Institutional administrative history','https://stm.dk/statsministeriet/rigsfaellesskabet/groenland/?embed=true','CC0 editorial factual metadata'],
 'historical-1880-supplements.geojson':['Natural Earth contemporary reference; Cliopatria Hawaii1885','https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/','Natural Earth public domain; Hawaii Cliopatria CC BY4.0'],
 'historical-1880-control.geojson':['CShapes unchanged dated Hawaii; US National Archives annexation resolution','https://www.archives.gov/milestone-documents/joint-resolution-for-annexing-the-hawaiian-islands','CShapes2.0 CC BY-NC-SA4.0']
};
for(const [file,transform] of Object.entries(descriptions)){
 const bytes=await readFile(new URL(file,root)),data=JSON.parse(bytes);let e=manifest.entries.find(e=>e.file===file);
 if(!e){const [provider,url,license]=source[file];e={file,format:data.format??'geojson',source:provider,url,license};manifest.entries.push(e);}
 e.format=({'country-history.json':'country-workspace-history','affiliations.json':'dated-organizations','historical-context.json':'dated-historical-context','identities.json':'dated-political-identities'})[file]??data.format??'geojson';
 Object.assign(e,{bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),version:`Historicmap ${version}; preparation2026-10-25; current reference2026-10-22`,transform});
 if(data.countries){e.countries=Object.keys(data.countries).length;e.records=Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0);}
 if(data.organizations){e.organizations=data.organizations.length;e.records=data.organizations.reduce((n,o)=>n+o.memberships.length,0);}
 if(data.events)e.records=data.events.length;
 if(data.records)e.records=data.records.length;
 if(data.relations)e.relations=data.relations.length;
 if(data.features)e.features=data.features.length;
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));
await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');
const review=JSON.parse(await readFile(new URL('../.cache/review-1880.json',import.meta.url)));
await writeFile(new URL('../docs/REVIEW-1880-1899.json',import.meta.url),JSON.stringify({reviewed:'2026-10-25',...review},null,2)+'\n');
console.log('Registered1880 extension and explicit reported corrections; source geometries unchanged.');
