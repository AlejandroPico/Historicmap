/** Refresh only resources prepared in0.15; immutable cartographic inputs stay intact. */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=f=>JSON.parse(readFileSync('public/data/'+f,'utf8')),manifest=read('manifest.json');
const descriptions={
 'identities.json':'Isolated1840–1859 acquisition, explicit historical office queries1840–1879 and101 reviewed observations. Joseon corrected toQ28179, Taiping ruler separated from Qing, regencies and collegial offices distinguished. All previous1880+ mandate facts preserved; images may be added to previously empty portraits. Current reference2026-10-22 unchanged. Nominal gaps remain in REVIEW files.',
 'historical-1840-entities.json':'Dated1840–1859 name/regime corrections over unchanged Cliopatria contours. French1848/1852 changes, Sardinia not Italy, Company India before1858, and source anachronisms explicitly repaired. Source labels/QIDs retained as provenance, not accepted as political fact.',
 'historical-context.json':'Seventeen sourced1840–1859 documentary phases appended idempotently, with preserved precision and observation boundaries. No geometric fronts inferred from event descriptions.',
 'country-history.json':'Seventeen sourced records and four fully named regime/administration navigation links. Existing observations preserved; coverage metadata extended to1840.',
 'pacific-components.json':'Thirteen original-component index periods covering1840–1885. Source polygons removed from aggregates before local selection, preserving every coordinate and component multiplicity.',
 'pacific-references.geojson':'Earlier local-authority reference windows extended to1840 without assigning later colonizers retrospectively. Contemporary Natural Earth reference contours remain labelled; existing independent-state supplements take priority.',
 'portrait-series.json':'Thirty-four dated representative portrait windows, including Victoria1838 painting and1854 photograph. Image dates remain independent of office dates; no painting is labelled as a photograph.'
};
for(const [file,transform] of Object.entries(descriptions)){
 let e=manifest.entries.find(e=>e.file===file);
 if(!e){e={file,format:'dated-entity-resolution',source:'Cliopatria and dated editorial identity corrections',url:'https://github.com/Seshat-Global-History-Databank/cliopatria',license:'CC0 factual identity metadata'};manifest.entries.push(e);}
 const bytes=readFileSync('public/data/'+file),d=JSON.parse(bytes);
 Object.assign(e,{sha256:createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length,version:'Historicmap0.15.0; preparation2026-10-26; current office reference2026-10-22 preserved',transform});
 if(d.records)e.records=d.records.length;if(d.events)e.records=d.events.length;if(d.features)e.features=d.features.length;if(d.relations)e.relations=d.relations.length;
 if(d.countries){e.countries=Object.keys(d.countries).length;e.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);}
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));writeFileSync('public/data/manifest.json',JSON.stringify(manifest,null,2)+'\n');
