import {readFileSync,existsSync,mkdtempSync,mkdirSync,writeFileSync,copyFileSync,rmSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve,dirname,basename} from 'node:path';
import {execFileSync} from 'node:child_process';
import {describe,it,expect} from 'vitest';
const read=(file:string)=>JSON.parse(readFileSync(new URL('../'+file,import.meta.url),'utf8'));
describe('entity folders and original media references',()=>{
 it('refreshes a stale entity folder when revised identities are registered, before any build',()=>{
  const root=mkdtempSync(join(tmpdir(),'historicmap-catalog-'));
  const save=(path:string,data:unknown)=>{mkdirSync(resolve(root,path,'..'),{recursive:true});writeFileSync(join(root,path),JSON.stringify(data,null,2)+'\n');};
  try{
   mkdirSync(join(root,'scripts'));
   for(const name of ['register-entity-revisions.mjs','prepare-country-catalog.mjs','prepare-display-labels.mjs'])copyFileSync(new URL('../scripts/'+name,import.meta.url),join(root,'scripts',name));
   save('package.json',{version:'test'});
   const key='QIN-STATE-WARRING',folder='Qin-existing-folder';
   const leaders=[{person:'HUIWEN',role:'Señor',start:'-0337-01-01',end:'-0326-12-31'},{person:'HUIWEN',role:'Rey',start:'-0325-01-01',end:'-0311-12-31'}];
   save('public/data/identities.json',{countries:{[key]:{name:'Qin',qid:'',leaders,flags:[]}}});
   save('public/data/profiles.json',{countries:{}});save('public/data/portrait-series.json',{records:[]});save('public/data/history.topojson',{objects:{countries:{geometries:[]}}});
   const resources=['identities.json','country-history.json','governance.json','historical-places.json','historical-context.json','conflict-points.geojson','political-influence.json'];
   for(const file of resources.slice(1))save('public/data/'+file,{});
   save('public/data/manifest.json',{entries:resources.map(file=>({file,transform:'test',sha256:'stale'}))});
   save('Países/indice.json',{entities:[{key,folder}]});
   save('Países/'+folder+'/entidad.json',{key,leaders:[{person:'HUIWEN',role:'Rey',start:'-0337-01-01',end:'-0311-12-31'}],flags:[]});
   const run=()=>execFileSync(process.execPath,[join(root,'scripts/register-entity-revisions.mjs')],{cwd:root,stdio:'pipe'});
   run();
   const file=join(root,'Países',folder,'entidad.json'),generated=readFileSync(file,'utf8');
   expect(JSON.parse(generated).leaders).toEqual(leaders);
   const index=readFileSync(join(root,'Países/indice.json'),'utf8');
   expect(JSON.parse(index).entities[0]).toMatchObject({key,folder,leaders:2});
   run();expect(readFileSync(file,'utf8')).toBe(generated);expect(readFileSync(join(root,'Países/indice.json'),'utf8')).toBe(index);
   save('Países/'+folder+'/recursos.json',{key:'INVALID-OWNER',resources:[]});
   expect(run).toThrow();
  }finally{
   if(dirname(resolve(root))!==resolve(tmpdir())||!basename(root).startsWith('historicmap-catalog-'))throw Error('Unexpected temporary catalogue directory');
   rmSync(root,{recursive:true,force:true});
  }
 },15000);
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
