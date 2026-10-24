import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,normalizedName,withHistoricalSupplements} from '../src/history';
import {politicalData} from '../src/political';
import {identityFor} from '../src/identities';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology=read('history.topojson'),profiles=read('profiles.json'),identities=read('identities.json'),supplements=read('historical-supplements.geojson');
const controls=[...read('historical-control.geojson').features,...read('spanish-civil-war.geojson').features];
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
describe('1900–1919 country-year authority and symbol audit',()=>{
 it('records every source country-year and active control identity, retaining actual gaps',()=>{
  const decades:any[]=[];
  for(const start of [1900,1910]){
   const missing:any[]=[],photos=new Map(),symbols:any[]=[];let countryYears=0,controlYears=0;
   for(let year=start;year<start+10;year++){
    const base=politicalData(withHistoricalSupplements(historyAt(topology,year,names),year,supplements,historyAt(topology,1974,names)),year);
    const active=controls.filter(f=>f.properties.start<=year&&f.properties.end>=year).map(f=>({...f,properties:{...f.properties,identityKey:f.properties.identityKey??f.properties.controller}}));
    for(const [isControl,features] of [[false,base.features],[true,active]] as const)for(const f of features){
     const p=f.properties!,id=identityFor(p,year,identities,new Date(2026,9,24));if(isControl)controlYears++;else countryYears++;
     if(!id.leaders.length&&!id.territoryStatus)missing.push({year,name:p.originalName??p.name,key:id.key,status:p.status,owner:p.ownerName,control:isControl});
     if(!id.flag)symbols.push({year,name:p.originalName??p.name,key:id.key,control:isControl});
     for(const l of id.leaders)if(!l.portrait)photos.set(l.person,{person:l.person,name:l.name,country:p.originalName??p.name,year});
    }
   }
   const result={decade:start,countryYears,controlYears,missingAuthorities:missing,missingPortraits:[...photos.values()],missingSymbols:symbols};decades.push(result);
   mkdirSync('.cache',{recursive:true});writeFileSync(`.cache/coverage-${start}.json`,JSON.stringify(result,null,2));
  }
  const missing=decades.flatMap(d=>d.missingAuthorities);
  writeFileSync('.cache/coverage-1900-1919.json',JSON.stringify({countryYears:decades.reduce((n,d)=>n+d.countryYears,0),controlYears:decades.reduce((n,d)=>n+d.controlYears,0),decades},null,2));
  expect(missing).toEqual([]);
 },60000);
});
