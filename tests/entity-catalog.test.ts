import {readFileSync,existsSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import {describe,it,expect} from 'vitest';
const read=(file:string)=>JSON.parse(readFileSync(new URL('../'+file,import.meta.url),'utf8'));
describe('entity folders and original media references',()=>{
 it('provides an indexed folder for every authority identity without moving its credited media',async()=>{
  const identities=read('public/data/identities.json'),index=read('Países/indice.json').entities;
  expect(new Set(index.map((e:any)=>e.key)).size).toBe(index.length);
  const byKey=new Map<string,any>(index.map((e:any)=>[e.key,e])),countries=Object.entries<any>(identities.countries),files=new Set<string>();
  // Bound filesystem concurrency; large catalogues also run on synced folders.
  for(let offset=0;offset<countries.length;offset+=16)await Promise.all(countries.slice(offset,offset+16).map(async([key,c])=>{
   const entry=byKey.get(key);expect(entry,key).toBeDefined();
   const entity=JSON.parse(await readFile(new URL('../Países/'+entry.folder+'/entidad.json',import.meta.url),'utf8'));
   expect(entity.leaders,key).toEqual(c.leaders);expect(entity.flags,key).toEqual(c.flags);
   for(const f of entity.flags)files.add(f.media.file);
  }));
  for(const file of files)expect(existsSync(new URL('../public/'+file,import.meta.url))).toBe(true);
 },60000);
});
