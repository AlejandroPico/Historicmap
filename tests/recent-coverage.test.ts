import {describe,it,expect} from 'vitest';
import {readFileSync} from 'node:fs';
import {historyAt,normalizedName,type HistoryTopology} from '../src/history';
import {identityFor,type IdentityData} from '../src/identities';
import {politicalData} from '../src/political';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology:HistoryTopology=read('history.topojson'),profiles=read('profiles.json'),identities:IdentityData=read('identities.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));

describe('country-year authority lookup through the actual map identity resolver',()=>{
 it('resolves an authority or a sourced institutional vacancy for every independent CShapes country in 1970–2019',()=>{
  const missing:string[]=[],cache=new Map();
  for(let year=1970;year<=2019;year++){
   const world=politicalData(historyAt(topology,year,names,cache),year);
   for(const f of world.features.filter(f=>f.properties?.status==='independent')){
    const identity=identityFor(f.properties!,year,identities,new Date(2026,9,22));
    if(!identity.leaders.length&&!identity.territoryStatus)missing.push(`${year}: ${f.properties!.name} (${identity.key||'unresolved'})`);
   }
  }
  expect(missing).toEqual([]);
 },30000);
});
