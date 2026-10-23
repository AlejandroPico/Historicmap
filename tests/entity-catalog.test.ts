import {readFileSync,existsSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
const read=(file:string)=>JSON.parse(readFileSync(new URL('../'+file,import.meta.url),'utf8'));
describe('entity folders and original media references',()=>{
 it('provides an indexed folder for every authority identity without moving its credited media',()=>{
  const identities=read('public/data/identities.json'),index=read('Países/indice.json').entities;
  expect(new Set(index.map((e:any)=>e.key)).size).toBe(index.length);
  for(const [key,c] of Object.entries<any>(identities.countries)){
   const entry=index.find((e:any)=>e.key===key);expect(entry,key).toBeDefined();
   const entity=read('Países/'+entry.folder+'/entidad.json');
   expect(entity.leaders,key).toEqual(c.leaders);expect(entity.flags,key).toEqual(c.flags);
   for(const f of entity.flags)expect(existsSync(new URL('../public/'+f.media.file,import.meta.url))).toBe(true);
  }
 });
});
