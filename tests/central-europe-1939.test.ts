import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import type {Feature,FeatureCollection} from 'geojson';
import {historyAt,normalizedName} from '../src/history';
import {politicalData} from '../src/political';
import {composeControl} from '../src/control-map';
import {identityFor} from '../src/identities';
const read=(file:string)=>JSON.parse(readFileSync(new URL('../public/data/'+file,import.meta.url),'utf8'));
const topology=read('history.topojson'),raw=read('historical-control.geojson'),patch=read('central-europe-1939.geojson'),identities=read('identities.json'),profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
function contains(f:Feature,[x,y]:number[]){
 const ring=(r:number[][])=>{let yes=false;for(let i=0,j=r.length-1;i<r.length;j=i++){const a=r[i],b=r[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;};
 const ps=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
 return ps.some(p=>ring(p[0])&&!p.slice(1).some(ring));
}
function composed(y:number){
 const base=politicalData(historyAt(topology,y,names),y),controls:FeatureCollection={type:'FeatureCollection',features:raw.features.filter((f:any)=>f.properties.start<=y&&f.properties.end>=y)};
 if(y===1939){controls.features.push(...patch.features);const a=raw.features.find((f:any)=>f.properties.controller==='DEU'&&f.properties.start===1938);controls.features.push({...a,properties:{...a.properties,kind:'annexation-mask'}});}
 return composeControl(base,controls,y);
}
describe('1938–1939 integrated Central European control correction',()=>{
 it('removes remote German source cells and protects the actual dated neighbours without removing real islands',()=>{
  const input=JSON.stringify(raw),result=composed(1939),germany=result.territories.features.filter(f=>f.properties?.identityKey==='DEU');expect(germany).toHaveLength(1);
  for(const [name,point] of Object.entries({Karelia:[30.182290554,60.875223160],Russia:[35.270770073,61.016569138],Italy:[12.250466585,41.943910599],Netherlands:[4.942323665,52.673453617],Yugoslavia:[17.579929057,45.921695626],Belgium:[5.909728848,50.115068362],LuxembourgBorder:[6.395346,49.679601],DutchBorder:[6.024572,50.890684],ItalianBorder:[10.722769,46.815968]}))expect(germany.some(f=>contains(f,point)),name).toBe(false);
  for(const [name,point] of Object.entries({Berlin:[13.405,52.52],Vienna:[16.37,48.21],Prague:[14.42,50.08],Konigsberg:[20.51,54.71],Sylt:[8.33,54.91]}))expect(germany.some(f=>contains(f,point)),name).toBe(true);
  expect(JSON.stringify(raw)).toBe(input);expect(new Set(result.territories.features.map(f=>f.id)).size).toBe(result.territories.features.length);
 },60000);
 it('separates Sudeten incorporation from occupied Bohemia and the Slovak client, without a surviving Czech patch',()=>{
  const before=composed(1938),after=composed(1939),owner=(fs:Feature[],point:number[])=>fs.filter(f=>contains(f,point)).map(f=>f.properties?.identityKey);
  expect(owner(before.territories.features,[14.42,50.08])).toEqual(['CSK']);expect(owner(before.territories.features,[12.875,50.23])).toEqual(['DEU']);
  expect(owner(after.territories.features,[14.42,50.08])).toEqual(['DEU']);
  for(const [city,point] of Object.entries({Brno:[16.61,49.20],Olomouc:[17.25,49.59]})){
   expect(owner(before.territories.features,point),city+'1938').toEqual(['CSK']);expect(owner(after.territories.features,point),city+'1939').toEqual(['DEU']);
   expect(after.occupations.features.some(f=>contains(f,point)),city+'occupied1939').toBe(true);
  }
  for(const point of [[17.1077,48.1486],[18.74,49.22],[21.24,49]])expect(owner(after.territories.features,point),String(point)).toEqual(['SVK-1939']);
  expect(owner(after.territories.features,[21.26,48.72])).toEqual(['HUN']);
  expect(after.territories.features.some(f=>f.properties?.identityKey==='CSK')).toBe(false);
  expect(after.occupations.features.some(f=>contains(f,[14.42,50.08]))).toBe(true);expect(after.occupations.features.some(f=>contains(f,[16.37,48.21]))).toBe(false);
  const slovakia=after.territories.features.find(f=>f.properties?.identityKey==='SVK-1939')!;
  expect(slovakia.properties).toMatchObject({code:'',entityCode:'SVW',territorialReference:true});expect(slovakia.properties?.note).toContain('referencia');
  expect(identityFor(slovakia.properties!,1939,identities).leaders.map(l=>l.name)).toEqual(expect.arrayContaining(['Jozef Tiso','Vojtech Tuka']));
 },60000);
});
