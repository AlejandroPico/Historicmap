import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=f=>JSON.parse(readFileSync('public/data/'+f,'utf8')),manifest=read('manifest.json');
const descriptions={
 'identities.json':'Isolated1800–1819 acquisition and historical offices; Gregorian Russian succession, British regency and distinct Italian offices. Previous mandate facts and symbols retained; missing portraits may be filled. Nominal gaps remain in REVIEW-1800-1819.',
 'historical-1800-entities.json':'Dated1800–1819 identity resolution over unchanged Cliopatria contours. Consulate, Empire and Restorations; separate Italian states, British crowns/union and Haitian powers. No reconstructed internal military fronts.',
 'historical-context.json':'Twelve documentary phases1800–1819 appended idempotently; annual precision and coverage boundaries preserved. No geometric fronts inferred from texts.',
 'country-history.json':'Twelve dated records and three fully named French regime-transition links. Earlier observations retained, coverage extended to1800.',
 'pacific-components.json':'Original island-component index from1800; coordinates and component multiplicity conserved.',
 'pacific-references.geojson':'Only unadministered local-reference windows extended to1800; later colonial relations not backdated.',
 'political-influence.json':'Three bounded French-client relationships for Italian states, with distinct identities and authorities. Colour affinity does not assign colonial administration or annexation.'
};
for(const [file,transform] of Object.entries(descriptions)){
 let e=manifest.entries.find(e=>e.file===file);
 if(!e){e={file,format:'dated-entity-resolution',source:'Cliopatria and dated editorial identity corrections',url:'https://github.com/Seshat-Global-History-Databank/cliopatria',license:'CC0 factual identity metadata'};manifest.entries.push(e);}
 const bytes=readFileSync('public/data/'+file),d=JSON.parse(bytes);
 Object.assign(e,{sha256:createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length,version:'Historicmap0.17.0; preparation2026-10-26; contemporary reference unchanged',transform});
 if(d.records)e.records=d.records.length;if(d.events)e.records=d.events.length;if(d.features)e.features=d.features.length;if(d.relations)e.relations=d.relations.length;
 if(d.countries){e.countries=Object.keys(d.countries).length;e.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);}
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));writeFileSync('public/data/manifest.json',JSON.stringify(manifest,null,2)+'\n');
