import {readFileSync,writeFileSync} from 'node:fs';
import {beforeAll,afterAll,it,expect,vi} from 'vitest';
import {annualData} from '../src/data';
import {politicalData,regimeColor} from '../src/political';
import {identityFor,identityMarkup} from '../src/identities';
import {relatedEntities,type CountryHistory} from '../src/country-history';
import {eventsForCountry} from '../src/historical-context';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const ids=read('identities.json'),profiles=read('profiles.json');
beforeAll(()=>vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync(new URL('../public/data/'+String(input).split('/').at(-1),import.meta.url)),{status:200})));
afterAll(()=>vi.unstubAllGlobals());
const world=async(y:number)=>politicalData(await annualData(y),y,profiles);
const id=(key:string,y:number)=>identityFor({identityKey:key},y,ids);
it('loads annual1840–1859 identities and keeps the core sovereign series populated',async()=>{
 for(let y=1840;y<=1859;y++){
  const w=await world(y);expect(w.features.length).toBeGreaterThan(100);expect(new Set(w.features.map(f=>f.id)).size).toBe(w.features.length);
  for(const key of ['FRA','USA','ESP','GBR','RUE','OTT','QING','JPN','IRN','EGY','NPL','BRA-EMPIRE']){
   const p=w.features.find(f=>f.properties?.identityKey===key)?.properties;
   expect(p,key+':'+y).toBeDefined();expect(identityFor(p!,y,ids).leaders.length,key+':'+y).toBeGreaterThan(0);
  }
 }
},60000);
it('separates the French provisional executive from the constitutional presidency and imperial restoration',()=>{
 const f=id('FRA',1848);expect(f.leaders.some(l=>l.person==='Q7771')).toBe(true);expect(f.leaders.some(l=>l.person==='Q7721')).toBe(true);
 expect(f.leaders.filter(l=>['Q2309694','Q379702'].includes(l.person)).every(l=>!l.role.includes('Presidente de la República'))).toBe(true);
 expect(f.leaders.some(l=>l.person==='FRENCH-EXECUTIVE-COMMISSION-1848')).toBe(true);
 expect(regimeColor('FRA',1847)).not.toBe(regimeColor('FRA',1849));expect(regimeColor('FRA',1853)).not.toBe(regimeColor('FRA',1849));
});
it('repairs Joseon, keeps Taiping outside the Qing court and fills earlier monarchical omissions',()=>{
 expect(ids.countries.JOS.qid).toBe('Q28179');expect(id('JOS',1840).leaders.some(l=>l.person==='Q484966')).toBe(true);
 expect(id('JOS',1855).leaders.some(l=>l.person==='Q482850')).toBe(true);expect(id('JOS',1870).leaders.some(l=>l.person==='Q257425')).toBe(true);
 expect(id('QING',1855).leaders.some(l=>l.person==='Q334732')).toBe(false);expect(id('HIST-Q3486676',1855).leaders.some(l=>l.person==='Q334732')).toBe(true);
 for(const [key,y] of [['IRN',1860],['MMR',1860],['MAR',1860],['HAW-KINGDOM',1840],['HAW-KINGDOM',1873],['NPL',1870]] as const)expect(id(key,y).leaders.length,key+':'+y).toBeGreaterThan(0);
});
it('keeps regencies, dated symbols and dated representative portraits distinct',()=>{
 expect(id('ESP',1840).leaders.some(l=>l.person==='Q230566')).toBe(true);expect(id('ESP',1842).leaders.some(l=>l.person==='Q434529')).toBe(true);
 expect(id('BRA-EMPIRE',1840).leaders.some(l=>l.person==='Q1797348')).toBe(true);
 for(const [key,q] of [['FRA','Q7721'],['RUE','Q83171'],['PRUSSIA','Q150652']])expect(id(key,1859).leaders.find(l=>l.person===q)?.endIsCoverageBoundary,key).toBe(true);
 const a=id('GBR',1840).leaders.find(l=>l.person==='Q9439')!,b=id('GBR',1855).leaders.find(l=>l.person==='Q9439')!;
 expect(a.portrait?.file).not.toBe(b.portrait?.file);expect(a.portrait?.photoDateLabel).toContain('1838');expect(b.portrait?.photoDateLabel).toContain('1854');
 for(const key of ['PRUSSIA','AUSTRIAN-EMPIRE','TWO-SICILIES','PAPAL-STATES','TEXAS'])expect(id(key,1840).flag,key).toBeDefined();
 expect(identityMarkup({identityKey:'GBR'},1840,ids,'/','authorities')).toContain('Retrato pintado');
});
it('provides navigable, fully named historical relations',()=>{
 const history=read('country-history.json') as CountryHistory;
 for(const r of history.relations.filter(r=>r.id.startsWith('extension-1840-'))){expect(r.from.name).toBeTruthy();expect(r.to.name).toBeTruthy();expect(r.label).toBeTruthy();expect(r.type).toBeTruthy();}
 expect(relatedEntities('FRA',history).some(r=>r.date==='1848-02-24')).toBe(true);
 expect(eventsForCountry({entityCode:'TEXAS'},1846,'conflict')).toEqual([]);
});
it('routes documented context through the dated entity without assigning a successor statistical code',async()=>{
 const w=await world(1855);
 for(const key of ['FRA','RUE','QING']){
  const p=w.features.find(f=>f.properties?.identityKey===key)!.properties!;
  expect(p.code).toBe('');expect(eventsForCountry(p,1855).length,key).toBeGreaterThan(0);
 }
 const france=w.features.find(f=>f.properties?.identityKey==='FRA')!.properties!;
 expect(eventsForCountry(france,1855,'conflict').some(e=>e.title.includes('Crimea'))).toBe(true);
 expect(eventsForCountry(france,1853,'conflict').some(e=>e.title.includes('Crimea'))).toBe(false);
 const sardinia={identityKey:'SAR',entityCode:'SAR',code:''};
 expect(eventsForCountry(sardinia,1854,'conflict').some(e=>e.title.includes('Crimea'))).toBe(false);
 expect(eventsForCountry(sardinia,1855,'conflict').some(e=>e.title.includes('Crimea'))).toBe(true);
});
it('records the actual annual availability and unresolved names for both historical windows',async()=>{
 if(!process.env.ATLAS_WRITE_AUDIT)return;
 for(const [first,last] of [[1840,1859],[1860,1879]]){
  const years:any[]=[],missing:any[]=[],photos=new Map<string,any>(),symbols:any[]=[];
  for(let year=first;year<=last;year++){
   const w=await world(year);let withAuthorities=0;
   for(const f of w.features){const p=f.properties!,i=identityFor(p,year,ids);
    if(!i.leaders.length&&!i.territoryStatus)missing.push({year,name:p.name,key:i.key,sourceName:p.originalName});else withAuthorities++;
    if(!i.flag)symbols.push({year,name:p.name,key:i.key});for(const l of i.leaders)if(!l.portrait)photos.set(l.person,{person:l.person,name:l.name,key:i.key,year});
   }years.push({year,territories:w.features.length,withSomeAuthorityOrDocumentedAbsence:withAuthorities});
  }
  writeFileSync(`docs/REVIEW-${first}-${last}.json`,JSON.stringify({reviewed:'2026-10-26',release:'0.15.0',scope:'Production-path availability, not a complete office census or a validation of every frontier.',years,missingAuthorities:missing,missingPortraits:[...photos.values()],missingSymbols:symbols},null,2)+'\n');
 }
},60000);
