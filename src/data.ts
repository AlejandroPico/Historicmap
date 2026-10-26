import type {FeatureCollection, MultiPolygon, Polygon} from 'geojson';
import {historyAt, withHistoricalSupplements, normalizedName, type HistoryTopology} from './history';
import type {ProfileData} from './profiles';
import {regimeColor} from './political';
import type {PartitionControls,WartimePartitions} from './wartime-partition';
import {resolve1880,type EntityResolution} from './historical-1880';
import {pacificComponents,pacificReferences} from './pacific';
const base=import.meta.env.BASE_URL+'data/';
// Share in-flight requests. Changing the ruler never aborts a reusable download.
const requests=new Map<string,Promise<unknown>>();
export function asset<T>(file:string):Promise<T>{
  const previous=requests.get(file);
  if(previous){requests.delete(file);requests.set(file,previous);return previous as Promise<T>;}
  const request=fetch(base+file).then(async r=>{if(!r.ok)throw Error(`${file}: ${r.status}`);return r.json();}).catch(error=>{requests.delete(file);throw error;});
  requests.set(file,request);
  // Bound retained geological/snapshot data; shared contemporary/history assets persist.
  const snapshots=[...requests.keys()].filter(k=>k.startsWith('world_')||k.startsWith('coastlines-'));
  if(snapshots.length>3)requests.delete(snapshots[0]);
  return request as Promise<T>;
}
const geometryCache=new Map<number,Polygon|MultiPolygon>();
let names:Map<string,string>|undefined;
export async function annualData(year:number){
  if(year<1886){
    const data=await asset<FeatureCollection>(year<1400?'early-modern-1300.geojson':year<1500?'early-modern-1400.geojson':year<1600?'early-modern-1500.geojson':year<1700?'early-modern-1600.geojson':year<1789?'early-modern-1700.geojson':'early-modern.geojson');
    let selected=pacificComponents({...data,features:data.features.filter(f=>f.properties!.start<=year&&f.properties!.end>=year)},year);
    if(year>=1300)selected=resolve1880(selected,year,await asset<EntityResolution>(year>=1880?'historical-1880-entities.json':year>=1860?'historical-1860-entities.json':year>=1840?'historical-1840-entities.json':year>=1820?'historical-1820-entities.json':year>=1800?'historical-1800-entities.json':year>=1700?'historical-1700-entities.json':year>=1600?'historical-1600-entities.json':year>=1500?'historical-1500-entities.json':year>=1400?'historical-1400-entities.json':'historical-1300-entities.json'));
    return year>=1800?pacificReferences(selected,year,await asset<FeatureCollection>('pacific-references.geojson')):selected;
  }
  const [history,profiles,supplements]=await Promise.all([asset<HistoryTopology>('history.topojson'),asset<ProfileData>('profiles.json'),year>=1900?asset<FeatureCollection>('historical-supplements.geojson'):Promise.resolve(undefined)]);
  names??=new Map(Object.entries(profiles.countries).flatMap(([iso,p])=>[p.name,p.englishName??'',p.official??''].filter(Boolean).map(n=>[normalizedName(n),iso])));
  const raw=historyAt(history,year,names,geometryCache);
  const reference=await asset<FeatureCollection>('historical-1880-supplements.geojson');
  let data=withHistoricalSupplements(raw,year,reference,historyAt(history,1974,names,geometryCache));
  if(year>=1886&&year<1900){
    data=resolve1880(data,year,await asset<EntityResolution>('historical-1880-entities.json'));
  }
  if(supplements)data=withHistoricalSupplements(data,year,supplements,historyAt(history,1974,names,geometryCache));
  return pacificReferences(data,year,await asset<FeatureCollection>('pacific-references.geojson'));
}
export const modernCities=()=>asset<FeatureCollection>('cities.geojson');
export async function overlaysFor(year:number):Promise<PartitionControls>{
  if(year>=1940&&year<=1944){
    const prepared=await asset<WartimePartitions>('wartime-partitions.json');
    const partition=prepared.years[String(year)];
    if(!partition)throw Error(`Missing dated control partition ${year}`);
    return {type:'FeatureCollection',features:[],partition};
  }
  const files=['territorial-overlays.geojson',...(year>=1898&&year<=1899?['historical-1880-control.geojson']:[]),...(year>=1990?['recent-control.geojson']:[]),...(year>=1914&&year<=1949?['historical-control.geojson']:[]),...(year===1939?['central-europe-1939.geojson']:[]),...(year>=1936&&year<=1939?['spanish-civil-war.geojson']:[])];
  const data=await Promise.all(files.map(f=>asset<FeatureCollection>(f)));
  const all=data.flatMap(d=>d.features).filter(f=>!(year>=2022&&year<=2026&&f.properties?.uid==='crimea'));
  if(year>=2022&&year<=2026)all.push(...(await asset<FeatureCollection>('ukraine-control-2022.geojson')).features);
  const features:FeatureCollection['features']=all.filter(f=>f.properties!.start<=year&&f.properties!.end>=year).map(f=>{
    const p=f.properties!;
    const controller=p.controller??(p.uid==='crimea'?'RUS':p.kind==='dispute'?'ISR':'');
    const occupiedKey=p.uid==='crimea'?'UKR':p.uid==='golan'?'SYR':String(p.uid).startsWith('sinai')?'EGY':p.uid==='kuwait-1990'?'KWT':undefined;
    return {...f,properties:{...p,controller,occupiedKey:p.occupiedKey??occupiedKey,identityKey:p.identityKey??controller,controlColor:p.controlColor??(controller==='ISR'?'#679ab6':regimeColor(controller,year))}};
  });
  // The 1938 extent documents incorporation of Austria/Sudeten areas before
  // wartime occupation. It is a mask for hatching, not another control country.
  if(year>=1939&&year<=1944){const incorporation=all.find(f=>f.properties?.controller==='DEU'&&f.properties?.start===1938);if(incorporation)features.push({...incorporation,properties:{...incorporation.properties,kind:'annexation-mask',controller:'DEU'}});}
  return {type:'FeatureCollection',features};
}
