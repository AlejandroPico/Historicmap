/** Refresh generated resource metadata after compiling entity-owned revisions. */
import{readFileSync,writeFileSync,readdirSync,existsSync}from'node:fs';import{createHash}from'node:crypto';
const read=p=>JSON.parse(readFileSync(p,'utf8')),manifest=read('public/data/manifest.json');
const changed=new Set(['identities.json','country-history.json','governance.json']);
for(const folder of readdirSync('Países',{withFileTypes:true}).filter(d=>d.isDirectory())){
 const file='Países/'+folder.name+'/revision-historica.json';if(!existsSync(file))continue;
 for(const fix of read(file).entityRules??[])for(const f of fix.files)changed.add(f);
}
for(const e of manifest.entries)if(changed.has(e.file)){
 const raw=readFileSync('public/data/'+e.file),data=JSON.parse(raw);
 Object.assign(e,{sha256:createHash('sha256').update(raw).digest('hex'),bytes:raw.length,version:'Historicmap0.26.1; entity reviews2026-10-27'});
 if(data.records)e.records=data.records.length;
 if(e.file==='identities.json'){e.countries=Object.keys(data.countries).length;e.records=Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0);e.transform=e.transform.split(' Entity-owned corrections')[0]+' Entity-owned corrections distinguish dated symbols from retrospective heraldic references, provincial offices and governments without a common national executive.';}
}
writeFileSync('public/data/manifest.json',JSON.stringify(manifest,null,2)+'\n');
console.log('Registered entity revisions:',changed.size,'data resources.');
