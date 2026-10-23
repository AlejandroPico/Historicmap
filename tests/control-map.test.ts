import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import type {FeatureCollection,Feature} from 'geojson';
import {composeControl} from '../src/control-map';
import {occupationPattern} from '../src/occupation-pattern';
import {historyAt} from '../src/history';
import {politicalData,regimeColor} from '../src/political';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const rectangle=(id:number,key:string,color:string,x0:number,x1:number):Feature=>({type:'Feature',id,properties:{name:key,identityKey:key,politicalColor:color},geometry:{type:'Polygon',coordinates:[[[x0,0],[x1,0],[x1,2],[x0,2],[x0,0]]]}});
describe('control is part of the territory inventory',()=>{
 it('partitions the sovereign map, merges controller territory and keeps occupation metadata separate',()=>{
  const a=rectangle(1,'DEU','#50545a',0,2),b=rectangle(2,'FRA','#6796ad',2,4);
  const control={...rectangle(3,'DEU','#50545a',0,3),properties:{controller:'DEU',relation:'occupation',uid:'test',note:'test',source:'test'}};
  const base:FeatureCollection={type:'FeatureCollection',features:[a,b]};
  const result=composeControl(base,{type:'FeatureCollection',features:[control]},1942);
  expect(result.territories.features).toHaveLength(2);
  const germany=result.territories.features.find(f=>f.properties?.identityKey==='DEU')!;
  expect(germany.id).toBe(1);expect(germany.properties?.uid).toBeUndefined();
  expect(result.occupations.features).toHaveLength(1);
  expect(result.occupations.features[0].properties).toMatchObject({occupiedKey:'FRA',occupiedColor:'#6796ad',controller:'DEU'});
  expect(base.features[1].geometry).toEqual(b.geometry);
 });
 it('does not hatch incorporation already present in the base or civil-war territory',()=>{
  const base:FeatureCollection={type:'FeatureCollection',features:[rectangle(1,'DEU','#50545a',0,4)]};
  const control={...rectangle(3,'DEU','#50545a',0,3),properties:{controller:'DEU',relation:'occupation'}};
  expect(composeControl(base,{type:'FeatureCollection',features:[control]},1938).occupations.features).toHaveLength(0);
 });
 it('uses exactly one quarter thin territory-colour stripes and three quarters controller-colour stripes',()=>{
  const pattern=occupationPattern('#112233','#aabbcc');
  let thin=0;for(let i=0;i<pattern.data.length;i+=4){if(pattern.data[i]===170)thin++;expect(pattern.data[i+3]).toBe(255);}
  expect(thin).toBe(64);
 });
 it('composes actual WWII source geometry without dropping country properties',()=>{
  const base=politicalData(historyAt(read('history.topojson'),1942),1942);
  const controls:FeatureCollection=read('historical-control.geojson');
  const incorporation=controls.features.find(f=>f.properties?.controller==='DEU'&&f.properties?.start===1938)!;
  controls.features=controls.features.filter(f=>f.properties!.start<=1942&&f.properties!.end>=1942);
  expect(incorporation).toBeDefined();controls.features.push({...incorporation,properties:{...incorporation.properties,kind:'annexation-mask'}});
  const result=composeControl(base,controls,1942);
  expect(result.territories.features.find(f=>f.properties?.identityKey==='DEU')?.properties?.politicalColor).toBe(regimeColor('DEU',1942));
  expect(result.occupations.features.some(f=>f.properties?.occupiedName==='Noruega'||f.properties?.occupiedName==='Norway')).toBe(true);
  expect(new Set(result.territories.features.map(f=>f.id)).size).toBe(result.territories.features.length);
  const contains=(f:Feature,[x,y]:number[])=>{
   const ring=(r:number[][])=>{let yes=false;for(let i=0,j=r.length-1;i<r.length;j=i++){const a=r[i],b=r[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;};
   const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
   return polygons.some(p=>ring(p[0])&&!p.slice(1).some(ring));
  };
  expect(result.occupations.features.some(f=>contains(f,[16.37,48.21])),'Vienna is in the documented incorporation extent').toBe(false);
  expect(result.occupations.features.some(f=>contains(f,[10.75,59.91])),'Oslo is occupied, not incorporated').toBe(true);
 },60000);
});
