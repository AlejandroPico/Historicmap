import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import type {Feature,FeatureCollection} from 'geojson';
import {historyAt,withHistoricalSupplements,normalizedName} from '../src/history';
import {politicalData} from '../src/political';
import {composeControl} from '../src/control-map';
import {controlledMap} from '../src/control-loader';
import {identityFor} from '../src/identities';
import type {WartimePartitions} from '../src/wartime-partition';
const read=(name:string)=>JSON.parse(readFileSync(new URL('../public/data/'+name,import.meta.url),'utf8'));
const prepared:WartimePartitions=read('wartime-partitions.json'),topology=read('history.topojson'),supplements=read('historical-supplements.geojson'),profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const identities=read('identities.json');
function contains(f:Feature,[x,y]:number[]){
 const ring=(r:number[][])=>{let yes=false;for(let i=0,j=r.length-1;i<r.length;j=i++){const a=r[i],b=r[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;};
 const ps=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
 return ps.some(p=>ring(p[0])&&!p.slice(1).some(ring));
}
const world=(y:number)=>politicalData(withHistoricalSupplements(historyAt(topology,y,names),y,supplements,historyAt(topology,1974,names)),y);
const badPoints={Sweden:[18.48446,59.39957],Karelia:[35.270770073,61.016569138],Italy:[12.250466585,41.943910599],Syria:[35.86668,33.07161],Iran:[47.88789,31.88247],Iraq:[47.73497,30.98271],Switzerland:[8.2,46.8]};

describe('1940–1944 shared ownership partitions',()=>{
 for(const year of [1940,1941,1942,1943,1944])it(`${year}: replaces territories, protects neutral land and trims hatches to final owners`,async()=>{
  const base=world(year),before=JSON.stringify(base),partition=prepared.years[String(year)];
  const controls={type:'FeatureCollection' as const,features:[],partition};
  // Production loader must honour the prepared partition despite no raw
  // overlays. Otherwise an early no-controls shortcut silently skips the fix.
  const result=await controlledMap(base,controls,year);
  expect(result).toEqual(composeControl(base,controls,year));
  expect(JSON.stringify(base)).toBe(before);
  const germany=result.territories.features.filter(f=>f.properties?.identityKey==='DEU');expect(germany).toHaveLength(1);
  for(const [name,point] of Object.entries(badPoints))expect(germany.some(f=>contains(f,point)),name).toBe(false);
  const owner=(point:number[])=>result.territories.features.filter(f=>contains(f,point)).map(f=>f.properties?.identityKey);
  for(const point of [[13.405,52.52],[14.42,50.08],[10.75,59.91],[2.35,48.86],[8.33,54.91]])expect(owner(point),String(point)).toEqual(['DEU']);
  if(year<=1942)for(const point of [[9.19,45.46],[12.49,41.9],[14.27,40.85]])expect(owner(point),String(point)).toEqual(['ITA']);
  expect(owner([18.48446,59.39957])).toEqual(['SWE']);
  if(year<=1943){
   expect(owner([17.1077,48.1486])).toEqual(['SVK-1939']);
   const id=identityFor({identityKey:'SVK-1939'},year,identities);
   expect(id.leaders.map(l=>l.name)).toEqual(expect.arrayContaining(['Jozef Tiso','Vojtech Tuka']));expect(id.flag).toBeDefined();
   expect(id.leaders.every(l=>l.portrait)).toBe(true);
  }
  expect(result.territories.features.some(f=>f.properties?.identityKey==='CSK')).toBe(false);
  expect(new Set(result.territories.features.map(f=>f.id)).size).toBe(result.territories.features.length);
  expect(result.territories.features.some(f=>f.properties?.uid)).toBe(false);
  expect(result.occupations.features.some(f=>contains(f,[16.37,48.21]))).toBe(false);
  expect(result.occupations.features.some(f=>contains(f,[14.42,50.08]))).toBe(true);
  for(const hatch of result.occupations.features){
   const p=hatch.properties!;expect(p.patternKey).toBe(`${p.controlColor}:${p.occupiedColor}`);
   // Controller metadata must match an actual final selectable territory.
   expect(result.territories.features.some(f=>f.properties?.identityKey===p.controller)).toBe(true);
  }
  if(year>=1941){expect(owner([15.98,45.81])).toEqual(['CROATIA-CLIENT']);expect(result.occupations.features.some(f=>f.properties?.controller==='DEU'&&contains(f,[15.98,45.81]))).toBe(false);}
  // The Chinese civil-war partition must replace, rather than overlap, China.
  expect(owner([109.5,37.5])).toEqual(['CHN-COMMUNIST']);
 },30000);
 it('records full land conservation, protected-country intersections and final hatch containment during preparation',()=>{
  const report=JSON.parse(readFileSync(new URL('../docs/WWII-PARTITIONS-AUDIT.json',import.meta.url),'utf8'));
  expect(report.years.map((r:any)=>r.year)).toEqual([1940,1941,1942,1943,1944]);
  for(const r of report.years){
   expect(r.extraLandArea).toBeLessThan(1e-7);expect(r.missingLandArea).toBeLessThan(1e-7);expect(r.newOverlapArea).toBeLessThan(1e-7);
   for(const a of Object.values(r.protectedGermanIntersectionArea))expect(a).toBeLessThan(1e-8);
   expect(r.hatchOutsideFinalControllerArea).toBeLessThan(1e-8);
  }
 });
 it('retains both1944 governments and their portraits without carrying the earlier government beyond its dated handover',()=>{
  const id=identityFor({identityKey:'SVK-1939'},1944,identities);
  expect(id.leaders.map(l=>l.name)).toEqual(expect.arrayContaining(['Jozef Tiso','Vojtech Tuka','Štefan Tiso']));
  expect(id.leaders.find(l=>l.name==='Vojtech Tuka')?.end).toBe('1944-09-05');
  expect(id.leaders.find(l=>l.name==='Štefan Tiso')?.start).toBe('1944-09-05');expect(id.leaders.every(l=>l.portrait)).toBe(true);
 });
});
