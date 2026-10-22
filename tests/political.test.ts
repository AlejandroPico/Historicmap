import {readFileSync} from 'node:fs';
import type {Feature,FeatureCollection} from 'geojson';
import {describe,it,expect} from 'vitest';
import {entityKey,politicalData,regimeColor} from '../src/political';
import {historyAt,type HistoryTopology} from '../src/history';
const json=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const early:FeatureCollection=json('early-modern.geojson');
const controls:FeatureCollection=json('historical-control.geojson');
// Geographic regression probes, independent of MapLibre tiling and camera position.
function contains(f:Feature,point:number[]){
 const ring=(r:number[][])=>{let inside=false;for(let i=0,j=r.length-1;i<r.length;j=i++)if((r[i][1]>point[1])!==(r[j][1]>point[1])&&point[0]<(r[j][0]-r[i][0])*(point[1]-r[i][1])/(r[j][1]-r[i][1])+r[i][0])inside=!inside;return inside;};
 const polygon=(p:number[][][])=>ring(p[0])&&!p.slice(1).some(ring);
 return f.geometry.type==='Polygon'?polygon(f.geometry.coordinates):f.geometry.type==='MultiPolygon'&&f.geometry.coordinates.some(polygon);
}
describe('political regimes and territorial control',()=>{
 it('selects a nonempty unique inventory for every year from the Revolution to CShapes',()=>{
  for(let year=1789;year<1886;year++){
   const active=early.features.filter(f=>f.properties!.start<=year&&f.properties!.end>=year);
   expect(active.length,`${year}`).toBeGreaterThan(75);
   expect(new Set(active.map(f=>f.id)).size).toBe(active.length);
   expect(active.every(f=>!String(f.properties!.name).startsWith('('))).toBe(true);
  }
  const topology:HistoryTopology=json('history.topojson');
  for(let year=1886;year<1900;year++)expect(historyAt(topology,year).features.length).toBeGreaterThan(120);
 });
 it('keeps USSR red and distinct from Britain, and changes French and Spanish regimes',()=>{
  expect(entityKey({gwcode:365,originalName:'Russia (Soviet Union)'},1942)).toBe('USSR');
  expect(regimeColor('USSR',1942)).not.toBe(regimeColor('GBR',1942));
  expect(regimeColor('FRA',1789)).not.toBe(regimeColor('FRA',1812));
  expect(regimeColor('ESP-REPUBLIC',1936)).not.toBe(regimeColor('ESP-NATIONALIST',1936));
  const topology:HistoryTopology=json('history.topojson');
  const map=politicalData(historyAt(topology,1942),1942);
  const germany=map.features.find(f=>f.properties?.country_name==='Germany (Prussia)')!;
  expect(germany.properties?.politicalColor).toBe(regimeColor('DEU',1942));
  expect(map.features.find(f=>f.properties?.country_name==='India')?.properties?.politicalColor).toBe(regimeColor('GBR',1942));
 });
 it('unifies actual German controlled locations, leaving allies distinct until occupied',()=>{
  const german=(year:number)=>controls.features.find(f=>f.properties!.controller==='DEU'&&f.properties!.start<=year&&f.properties!.end>=year)!;
  for(const p of [[16.37,48.21],[14.42,50.08],[4.35,50.85],[10.75,59.91]])expect(contains(german(1942),p)).toBe(true);
  expect(contains(german(1942),[19.04,47.5])).toBe(false);
  expect(contains(german(1944),[19.04,47.5])).toBe(true);
  expect(contains(german(1942),[26.1,44.43])).toBe(false);
  const client=controls.features.find(f=>f.properties!.controller==='CROATIA-CLIENT'&&f.properties!.start<=1942&&f.properties!.end>=1942)!;
  expect(client.properties?.relation).toBe('client');expect(contains(client,[15.98,45.81])).toBe(true);
 });
 it('reflects WWII Japanese control at Nanjing and WWI German control at Brussels',()=>{
  const japanese=controls.features.find(f=>f.properties!.controller==='JPN'&&f.properties!.start<=1942&&f.properties!.end>=1942)!;
  expect(contains(japanese,[118.8,32.06])).toBe(true);
  const german=controls.features.find(f=>f.properties!.controller==='DEU'&&f.properties!.start<=1917&&f.properties!.end>=1917)!;
  expect(contains(german,[4.35,50.85])).toBe(true);
 });
});
