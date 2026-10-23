import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,normalizedName,withHistoricalSupplements} from '../src/history';
import {politicalData} from '../src/political';
import {identityFor} from '../src/identities';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology=read('history.topojson'),profiles=read('profiles.json'),identities=read('identities.json');
const supplements=read('historical-supplements.geojson');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
describe('1950–1959 authority acquisition review',()=>{
 it('inventories concrete country-year gaps rather than hiding missing records',()=>{
  const missing:any[]=[],photos=new Map(),symbols:any[]=[];let countryYears=0;
  for(let year=1950;year<1960;year++)for(const f of politicalData(withHistoricalSupplements(historyAt(topology,year,names),year,supplements,historyAt(topology,1974,names)),year).features){
   const p=f.properties!,id=identityFor(p,year,identities,new Date(2026,9,23));countryYears++;
   if(!id.leaders.length&&!id.territoryStatus)missing.push({year,name:p.originalName,key:id.key,status:p.status,owner:p.ownerName});
   if(!id.flag)symbols.push({year,name:p.originalName,key:id.key});
   for(const l of id.leaders)if(!l.portrait)photos.set(l.person,{person:l.person,name:l.name,country:p.originalName,year});
  }
  mkdirSync('.cache',{recursive:true});writeFileSync('.cache/coverage-1950.json',JSON.stringify({countryYears,missingAuthorities:missing,missingPortraits:[...photos.values()],missingSymbols:symbols},null,2));
  expect(missing).toEqual([]);
 },60000);
});
