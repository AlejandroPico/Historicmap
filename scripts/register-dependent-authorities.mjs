import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url),manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
for(const file of ['identities.json','territorial-administrations.json']){
 const bytes=await readFile(new URL(file,root)),data=JSON.parse(bytes),old=manifest.entries.find(e=>e.file===file);
 const e={...old,file,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),version:'Historicmap 0.8.1; reference 2026-10-22; preparation 2026-10-23'};
 if(file==='identities.json'){e.countries=Object.keys(data.countries).length;e.records=Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0);e.transform=old.transform+' Incremental five sourced dependent/local offices; existing acquisition retained.';}
 else Object.assign(e,{format:'dated-territorial-administrations',records:data.records.length,source:'Primary legal, government and UN sources per relationship',url:'https://www.un.org/dppa/decolonization/en',license:data.license,transform:'Eleven dated territorial administration relationships; external national offices distinct from local government and sovereignty. Office intervals clipped to relationship; administrative endpoint is not national resignation. Other source-documented dependencies resolve their contemporary administrator; never derive authority from alliances. Coverage 1970–2026 reference, no successor statistics inherited.'});
 manifest.entries=manifest.entries.filter(x=>x.file!==file);manifest.entries.push(e);
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');console.log('Registered territorial administrations and incremental offices.');
