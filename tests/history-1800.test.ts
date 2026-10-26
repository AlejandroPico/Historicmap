import {readFileSync,writeFileSync} from 'node:fs';
import {beforeAll,afterAll,it,expect,vi} from 'vitest';
import {annualData} from '../src/data';
import {politicalData,influenceFor,regimeColor} from '../src/political';
import {identityFor} from '../src/identities';
import {eventsForCountry} from '../src/historical-context';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const ids=read('identities.json'),profiles=read('profiles.json');
beforeAll(()=>vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync(new URL('../public/data/'+String(input).split('/').at(-1),import.meta.url)),{status:200})));
afterAll(()=>vi.unstubAllGlobals());
const id=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
it('resolves annual1800–1819 inventories and records real documentary gaps',async()=>{
 const years:any[]=[],missing:any[]=[],portraits=new Map(),symbols:any[]=[];
 for(let y=1800;y<=1819;y++){
  const w=politicalData(await annualData(y),y,profiles);expect(w.features.length).toBeGreaterThan(100);expect(new Set(w.features.map(f=>f.id)).size).toBe(w.features.length);
  for(const key of ['FRA','ESP','GBR','USA','RUE','QING','JPN','IRN','NPL','JOS']){
   const p=w.features.find(f=>f.properties?.identityKey===key)?.properties;expect(p,key+':'+y).toBeDefined();expect(identityFor(p!,y,ids).leaders.length,key+':'+y).toBeGreaterThan(0);
  }
  for(const f of w.features){const p=f.properties!,i=identityFor(p,y,ids);if(!i.leaders.length&&!i.territoryStatus)missing.push({year:y,key:i.key,name:p.name});if(!i.flag)symbols.push({year:y,key:i.key,name:p.name});for(const l of i.leaders)if(!l.portrait)portraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
  years.push({year:y,territories:w.features.length});
 }
 if(process.env.ATLAS_WRITE_AUDIT)writeFileSync('docs/REVIEW-1800-1819.json',JSON.stringify({release:'0.17.0',reviewed:'2026-10-26',scope:'Annual production-path availability; not an exhaustive census or frontier validation.',years,missingAuthorities:missing,missingPortraits:[...portraits.values()],missingSymbols:symbols},null,2)+'\n');
},60000);
it('keeps Gregorian succession, regency and separate state roles',()=>{
 expect(id('GBR',1802).leaders.some(l=>l.person==='Q128902')).toBe(false);
 expect(id('ESP',1812).leaders.some(l=>l.person==='Q186256'&&l.role.includes('ausente'))).toBe(true);
 const russian=id('RUE',1801).leaders;expect(russian.find(l=>l.person==='Q15189')?.end).toBe('1801-03-24');expect(russian.find(l=>l.person==='Q15193')?.start).toBe('1801-03-24');
 expect(id('GBR',1812).leaders.some(l=>l.person==='Q130586'&&l.role.includes('regente'))).toBe(true);
 expect(id('GBR',1800).flag?.title).toContain('Great Britain');expect(id('GBR',1801).flag?.title).toContain('United Kingdom');
 expect(id('PRUSSIA',1825).flag).toBeDefined();
 expect(id('NAPOLEONIC-NAPLES',1807).leaders.some(l=>l.person==='Q7726')).toBe(true);expect(id('NAPOLEONIC-NAPLES',1812).leaders.some(l=>l.person==='Q151173')).toBe(true);
 expect(id('HTI',1808).leaders.some(l=>l.person==='Q353458'&&l.role.includes('Presidente'))).toBe(true);expect(id('HTI',1812).leaders.some(l=>l.person==='Q353458'&&l.role.includes('Rey'))).toBe(true);
});
it('links dated conflicts and client colours without colonial administration',async()=>{
 const w=politicalData(await annualData(1812),1812,profiles),p=w.features.find(f=>f.properties?.identityKey==='ESP')!.properties!;
 expect(eventsForCountry(p,1812,'conflict').some(e=>e.title.includes('peninsular'))).toBe(true);expect(eventsForCountry(p,1806,'conflict').some(e=>e.title.includes('peninsular'))).toBe(false);
 const italy=w.features.find(f=>f.properties?.identityKey==='NAPOLEONIC-ITALY')!.properties!;expect(italy.dominantPower).toBe('FRA');expect(italy.administratorKey).toBeUndefined();expect(influenceFor('NAPOLEONIC-ITALY',1816)).toBeUndefined();
 expect(regimeColor('FRA',1814)).not.toBe(regimeColor('FRA',1812));
});
