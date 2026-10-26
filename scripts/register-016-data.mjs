/** Update only resources changed by the1820 extension. */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read=f=>JSON.parse(readFileSync('public/data/'+f,'utf8')),manifest=read('manifest.json');
const descriptions={
 'identities.json':'Isolated1820–1839 acquisition and explicit historical offices. Sovereigns, regents and collegial authorities distinguished; honorary titles and a Sardinian source-date typo rejected. All1840+ mandate facts preserved. Nominal gaps remain in REVIEW-1820-1839.',
 'historical-1820-entities.json':'Dated1820–1839 identity resolution over unchanged Cliopatria geometry. Restoration and July Monarchy, Spanish regimes, Company India, First Mexican Empire, Haiti and Gran Colombia distinguished. Defective Gran Colombia persistence1831–1833 explicitly flagged, not asserted as continued union.',
 'historical-context.json':'Fourteen sourced1820–1839 documentary phases appended idempotently. Existing observations preserved; no military front inferred from prose.',
 'country-history.json':'Fourteen records and three fully named regime-transition links for1820–1839. Coverage begins1820; existing observations retained.',
 'pacific-components.json':'Original island-component index extended to1820, with coordinate/component-multiplicity conservation. No replacement modern coastline.',
 'pacific-references.geojson':'Unadministered local-reference windows extended to1820. Dated colonial windows remain unchanged; no British New Zealand projected before1840.',
 'portrait-series.json':'Existing1838 Victoria painting available from1838. Image date remains independent from accession; no future painting assigned by this variant before1838.'
};
for(const [file,transform] of Object.entries(descriptions)){
 let e=manifest.entries.find(e=>e.file===file);
 if(!e){e={file,format:'dated-entity-resolution',source:'Cliopatria and dated editorial identity corrections',url:'https://github.com/Seshat-Global-History-Databank/cliopatria',license:'CC0 factual identity metadata'};manifest.entries.push(e);}
 const bytes=readFileSync('public/data/'+file),d=JSON.parse(bytes);
 Object.assign(e,{sha256:createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length,version:'Historicmap0.16.0; preparation2026-10-26; contemporary reference unchanged',transform});
 if(d.records)e.records=d.records.length;if(d.events)e.records=d.events.length;if(d.features)e.features=d.features.length;if(d.relations)e.relations=d.relations.length;
 if(d.countries){e.countries=Object.keys(d.countries).length;e.records=Object.values(d.countries).reduce((n,c)=>n+c.leaders.length,0);}
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));writeFileSync('public/data/manifest.json',JSON.stringify(manifest,null,2)+'\n');
