import {readFileSync,writeFileSync} from 'node:fs';
import {beforeAll,afterAll,it,expect,vi} from 'vitest';
import {annualData} from '../src/data';
import {politicalData,regimeColor} from '../src/political';
import {identityFor} from '../src/identities';
import {eventsForCountry} from '../src/historical-context';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const ids=read('identities.json'),profiles=read('profiles.json');
beforeAll(()=>vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync(new URL('../public/data/'+String(input).split('/').at(-1),import.meta.url)),{status:200})));
afterAll(()=>vi.unstubAllGlobals());
const id=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
it('resolves all1820–1839 annual inventories, core authorities and nominal gaps',async()=>{
 const years:any[]=[],missing:any[]=[],portraits=new Map(),symbols:any[]=[];
 for(let y=1820;y<=1839;y++){
  const w=politicalData(await annualData(y),y,profiles);expect(w.features.length).toBeGreaterThan(100);expect(new Set(w.features.map(f=>f.id)).size).toBe(w.features.length);
  for(const key of ['FRA','ESP','GBR','USA','RUE','QING','JPN','IRN','EGY','NPL','JOS']){
   const p=w.features.find(f=>f.properties?.identityKey===key)?.properties;expect(p,key+':'+y).toBeDefined();expect(identityFor(p!,y,ids).leaders.length,key+':'+y).toBeGreaterThan(0);
  }
  for(const f of w.features){const p=f.properties!,i=identityFor(p,y,ids);if(!i.leaders.length&&!i.territoryStatus)missing.push({year:y,key:i.key,name:p.name});if(!i.flag)symbols.push({year:y,key:i.key,name:p.name});for(const l of i.leaders)if(!l.portrait)portraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
  years.push({year:y,territories:w.features.length});
 }
 if(process.env.ATLAS_WRITE_AUDIT)writeFileSync('docs/REVIEW-1820-1839.json',JSON.stringify({release:'0.16.0',reviewed:'2026-10-26',scope:'Annual production-path availability; not a complete authority census or frontier validation.',years,missingAuthorities:missing,missingPortraits:[...portraits.values()],missingSymbols:symbols},null,2)+'\n');
},60000);
it('keeps actual sovereign identities, regencies and within-year British succession',()=>{
 expect(id('RUE',1820).leaders.some(l=>l.person==='Q15193')).toBe(true);expect(id('RUE',1820).leaders.some(l=>l.person==='Q44387')).toBe(false);
 for(const q of ['Q127318','Q130586'])expect(id('GBR',1820).leaders.some(l=>l.person===q)).toBe(true);
 for(const q of ['Q130822','Q9439'])expect(id('GBR',1837).leaders.some(l=>l.person===q)).toBe(true);
 expect(id('ESP',1832).leaders.some(l=>l.person==='Q183085')).toBe(false);
 for(const q of ['Q183085','Q230566'])expect(id('ESP',1833).leaders.some(l=>l.person===q)).toBe(true);
 expect(id('BRA-EMPIRE',1826).leaders.some(l=>l.person==='Q676301')).toBe(false);expect(id('SAR',1839).leaders.some(l=>l.person==='Q168691')).toBe(false);
 expect(id('HIST-Q285658',1822).leaders.some(l=>l.person==='Q133808')).toBe(true);
});
it('dates regimes and documentary conflicts without carrying future changes backwards',async()=>{
 expect(regimeColor('ESP',1821)).not.toBe(regimeColor('ESP',1825));expect(regimeColor('FRA',1829)).not.toBe(regimeColor('FRA',1830));
 const w=politicalData(await annualData(1839),1839,profiles),p=w.features.find(f=>f.properties?.identityKey==='QING')!.properties!;
 expect(eventsForCountry(p,1839,'conflict').some(e=>e.title.includes('Opio'))).toBe(true);expect(eventsForCountry(p,1838,'conflict').some(e=>e.title.includes('Opio'))).toBe(false);
 const history=read('country-history.json');for(const r of history.relations.filter((r:any)=>r.id.startsWith('extension-1820-'))){expect(r.from.name).toBeTruthy();expect(r.to.name).toBeTruthy();}
});
