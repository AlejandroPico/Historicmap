import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {politicalData,regimeColor,dependencyColor} from '../src/political';
import {historicalPalette} from '../src/historical-palette';
describe('historical palette and documented colour families',()=>{
 it('colours real Roman and Byzantine snapshots and their source-linked dependencies',()=>{
  const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
  const world=politicalData(read('world_100.geojson'),100);
  const rome=world.features.find(f=>f.properties?.name==='Roman Empire')!,bosporus=world.features.find(f=>f.properties?.name==='Bosporian Kingdom')!;
  expect(rome.properties?.politicalColor).toBe(regimeColor('ROME',100));
  expect(bosporus.properties?.politicalColor).toBe(dependencyColor(regimeColor('ROME',100),'Bosporian Kingdom'));
  expect(regimeColor('ROME',100)).not.toBe(regimeColor('ROME-REPUBLIC',-100));
  expect(regimeColor('BYZANTIUM',500)).not.toBe(regimeColor('ROME',400));
 });
 it('distinguishes Britain from the Soviet family and major regime changes',()=>{
  expect(regimeColor('GBR',1960)).not.toBe(regimeColor('USSR',1960));
  for(const key of ['FRA','DEU','ITA'])expect(regimeColor(key,key==='FRA'?1789:1910)).not.toBe(regimeColor(key,key==='FRA'?1812:1935));
  const names=historicalPalette.flatMap(r=>r.names);expect(new Set(names).size).toBe(names.length);
 });
});
