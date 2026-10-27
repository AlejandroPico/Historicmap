/** Refresh generated resource metadata after compiling entity-owned revisions. */
import{readFileSync,writeFileSync,readdirSync,existsSync}from'node:fs';import{createHash}from'node:crypto';
const read=p=>JSON.parse(readFileSync(p,'utf8')),manifest=read('public/data/manifest.json');
const changed=new Set(['identities.json','country-history.json','governance.json','historical-places.json','historical-context.json','conflict-points.geojson']);
for(const folder of readdirSync('Países',{withFileTypes:true}).filter(d=>d.isDirectory())){
 const root='Países/'+folder.name;
 const inputs=[root+'/revision-historica.json',...(existsSync(root+'/periodos')?readdirSync(root+'/periodos').filter(f=>f.endsWith('.json')).map(f=>root+'/periodos/'+f):[])];
 for(const file of inputs)if(existsSync(file))for(const fix of read(file).entityRules??[])for(const f of fix.files)changed.add(f);
}
for(const file of changed)if(!manifest.entries.some(e=>e.file===file))manifest.entries.push({file,source:'Historicmap · entity-owned dated resolution',url:'https://github.com/AlejandroPico/Historicmap/tree/main/Pa%C3%ADses',license:'CC0-1.0 (metadata); source geometry licensed separately',coverage:'900/999'});
for(const e of manifest.entries)if(changed.has(e.file)){
 const raw=readFileSync('public/data/'+e.file),data=JSON.parse(raw);
 Object.assign(e,{sha256:createHash('sha256').update(raw).digest('hex'),bytes:raw.length,version:'Historicmap '+read('package.json').version+'; entity reviews 2026-10-27'});
 if(!e.format&&data.format)e.format=data.format;
 if(e.file==='country-history.json')e.format='country-workspace-history';
 if(data.format==='dated-entity-resolution')Object.assign(e,{coverageStart:data.coverageStart,coverageEnd:data.coverageEnd});
 if(data.records)e.records=data.records.length;
 if(data.events)e.records=data.events.length;
 if(data.features)e.features=data.features.length;
 if(e.file==='identities.json'){e.countries=Object.keys(data.countries).length;e.records=Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0);e.transform=e.transform.split(' Entity-owned corrections')[0]+' Entity-owned corrections distinguish dated symbols from retrospective heraldic references, provincial offices and governments without a common national executive.';}
}
writeFileSync('public/data/manifest.json',JSON.stringify(manifest,null,2)+'\n');
console.log('Registered entity revisions:',changed.size,'data resources.');
