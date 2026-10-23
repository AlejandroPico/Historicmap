import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import type {FeatureCollection,Polygon,MultiPolygon,Position} from 'geojson';
import {historyAt,normalizedName,withHistoricalSupplements,historicalCapitals,type HistoryTopology} from '../src/history';

const read=(file:string)=>JSON.parse(readFileSync(new URL('../public/data/'+file,import.meta.url),'utf8'));
const topology:HistoryTopology=read('history.topojson'),modern:FeatureCollection=read('countries.geojson'),supplements:FeatureCollection=read('historical-supplements.geojson');
const profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const world=(year:number)=>withHistoricalSupplements(historyAt(topology,year,names),year,supplements,historyAt(topology,1974,names));
const entity=(year:number,code:string)=>world(year).features.find(f=>f.properties?.entityCode===code);
const original=(year:number,name:string)=>world(year).features.find(f=>f.properties?.originalName===name);
const insideRing=([x,y]:number[],ring:Position[])=>{let inside=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const [xi,yi]=ring[i],[xj,yj]=ring[j];if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/(yj-yi)+xi)inside=!inside;}return inside;};
const contains=(geometry:Polygon|MultiPolygon,point:number[])=>{const polygons=geometry.type==='Polygon'?[geometry.coordinates]:geometry.coordinates;return polygons.some(rings=>insideRing(point,rings[0])&&!rings.slice(1).some(ring=>insideRing(point,ring)));};

describe('1970–1989 source boundaries and dated territorial identities',()=>{
 it('keeps the Vietnamese states distinct and does not transfer successor statistics backwards',()=>{
  for(const year of [1970,1974]){
   expect(entity(year,'VDR')?.properties).toMatchObject({identityKey:'VDR',code:''});
   expect(entity(year,'RVN')?.properties).toMatchObject({identityKey:'RVN',code:''});
   expect(contains(entity(year,'VDR')!.geometry as Polygon,[105.85,21.03])).toBe(true);
   expect(contains(entity(year,'RVN')!.geometry as Polygon,[106.7,10.77])).toBe(true);
  }
  expect(entity(1975,'RVN')).toBeUndefined();
  expect(entity(1975,'VDR')?.properties?.note).toContain('2 de julio de 1976');
  expect(entity(1976,'VNM')?.properties).toMatchObject({code:'VNM',name:'Vietnam'});
  expect(entity(1976,'VDR')).toBeUndefined();
 });
 it('shows the Bangladesh separation and Portuguese colonial independence at source dates',()=>{
  expect(original(1970,'Congo, Democratic Republic of (Zaire)')?.properties?.name).toBe('República Democrática del Congo');
  expect(original(1971,'Congo, Democratic Republic of (Zaire)')?.properties?.name).toBe('Zaire');
  expect(entity(1970,'BGD')).toBeUndefined();
  expect(contains(entity(1970,'PAK')!.geometry as MultiPolygon,[90.41,23.72])).toBe(true);
  expect(contains(entity(1971,'BGD')!.geometry as Polygon,[90.41,23.72])).toBe(true);
  for(const name of ['Angola','Mozambique']){
   expect(original(1974,name)?.properties).toMatchObject({status:'colony',ownerName:'Portugal',code:''});
   expect(original(1975,name)?.properties?.status).toBe('independent');
  }
 });
 it('preserves Germanies, the USSR, Czechoslovakia and two Yemens without successor statistics',()=>{
  for(const year of [1970,1980,1989])for(const code of ['DDR','SUN','CSK','YAR','YPR'])expect(entity(year,code)?.properties?.code,`${code} ${year}`).toBe('');
  expect(entity(1989,'DDR')?.properties?.identityKey).toBe('DDR');
  expect(entity(1989,'YAR')?.properties?.identityKey).toBe('YAR');
  expect(entity(1989,'YPR')?.properties?.identityKey).toBe('YPR');
  expect(entity(1990,'YAR')).toBeUndefined();expect(entity(1990,'YPR')).toBeUndefined();
  expect(entity(1990,'YEM')).toBeDefined();
 });
 it('dates small-state reference supplements without treating UN admission as independence',()=>{
  const years:Record<string,number>={GRD:1974,STP:1975,SYC:1976,DMA:1978,TUV:1978,KIR:1979,LCA:1979,VCT:1979,VUT:1980,ATG:1981,KNA:1983,MHL:1986,FSM:1986,PLW:1994};
  for(const [code,year] of Object.entries(years)){
   expect(entity(year-1,code),`${code} before independence`).toBeUndefined();
   const f=entity(year,code)!;expect(f.properties?.territorialReference,code).toBe(true);
   expect(f.geometry,`${code} original reference coordinates`).toEqual(modern.features.find(a=>a.properties?.code===code)!.geometry);
  }
  for(const code of ['AND','LIE','MCO','SMR','VAT','NRU','WSM'])expect(entity(1970,code)?.properties?.coverageStartIsFloor).toBe(true);
  expect(entity(1970,'TON')).toBeDefined();
 });
 it('keeps Spanish Sahara colonial before withdrawal and separates later claimed sectors',()=>{
  expect(entity(1974,'ESH')?.properties).toMatchObject({status:'colony',ownerName:'España',code:''});
  const sahara=entity(1975,'ESH')!;
  expect(sahara.properties).toMatchObject({status:'non-self-governing',code:'SAH',territorialReference:true});
  expect(sahara.properties?.note).toContain('administración española transitoria');
  for(const year of [1975,1978,1989]){
   expect(entity(year,'MAR')!.geometry).toEqual(original(1974,'Morocco')!.geometry);
   expect(contains(entity(year,'MAR')!.geometry as Polygon,[-13.2,27.15])).toBe(false);
  }
  expect(entity(1976,'MRT')!.geometry).toEqual(original(1974,'Mauritania')!.geometry);
 });
 it('distinguishes unrecognized Rhodesia and the 1979 British transition from Zimbabwe',()=>{
  expect(entity(1970,'RHO')?.properties).toMatchObject({identityKey:'RHO',code:'',capital:'Salisbury',politicalStatus:'Régimen de facto no reconocido internacionalmente'});
  expect(entity(1979,'RHO')?.properties?.politicalStatus).toContain('británica');
  expect(entity(1980,'RHO')).toBeUndefined();expect(entity(1980,'ZWE')?.properties?.code).toBe('ZWE');
  expect(historicalCapitals(world(1981)).features.some(f=>f.properties?.name==='Salisbury')).toBe(true);
  expect(historicalCapitals(world(1982)).features.some(f=>f.properties?.name==='Harare')).toBe(true);
 });
});
