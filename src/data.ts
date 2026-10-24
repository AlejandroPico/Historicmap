import type {FeatureCollection, MultiPolygon, Polygon} from 'geojson';
import {historyAt, withHistoricalSupplements, normalizedName, type HistoryTopology} from './history';
import type {ProfileData} from './profiles';
import {regimeColor} from './political';
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
    const data=await asset<FeatureCollection>('early-modern.geojson');
    return {...data,features:data.features.filter(f=>f.properties!.start<=year&&f.properties!.end>=year)};
  }
  const [history,profiles,supplements]=await Promise.all([asset<HistoryTopology>('history.topojson'),asset<ProfileData>('profiles.json'),year>=1920?asset<FeatureCollection>('historical-supplements.geojson'):Promise.resolve(undefined)]);
  names??=new Map(Object.entries(profiles.countries).flatMap(([iso,p])=>[p.name,p.englishName??'',p.official??''].filter(Boolean).map(n=>[normalizedName(n),iso])));
  const data=historyAt(history,year,names,geometryCache);
  if(!supplements)return data;
  return withHistoricalSupplements(data,year,supplements,historyAt(history,1974,names,geometryCache));
}
export const modernCities=()=>asset<FeatureCollection>('cities.geojson');
export async function overlaysFor(year:number):Promise<FeatureCollection>{
  const files=['territorial-overlays.geojson',...(year>=1990?['recent-control.geojson']:[]),...(year>=1914&&year<=1949?['historical-control.geojson']:[]),...(year>=1936&&year<=1939?['spanish-civil-war.geojson']:[])];
  const data=await Promise.all(files.map(f=>asset<FeatureCollection>(f)));
  const all=data.flatMap(d=>d.features);
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
