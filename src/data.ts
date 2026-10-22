import type {FeatureCollection, MultiPolygon, Polygon} from 'geojson';
import {historyAt, normalizedName, type HistoryTopology} from './history';
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
  const [history,profiles,supplements,modern]=await Promise.all([asset<HistoryTopology>('history.topojson'),asset<ProfileData>('profiles.json'),year>=1990?asset<FeatureCollection>('historical-supplements.geojson'):Promise.resolve(undefined),year>=1990?asset<FeatureCollection>('countries.geojson'):Promise.resolve(undefined)]);
  names??=new Map(Object.entries(profiles.countries).flatMap(([iso,p])=>[p.name,p.englishName??'',p.official??''].filter(Boolean).map(n=>[normalizedName(n),iso])));
  const data=historyAt(history,year,names,geometryCache);
  if(!supplements)return data;
  // Western Sahara remains a distinct UN non-self-governing territory. Reuse
  // the separately sourced reference outlines, without inventing a berm/front.
  const morocco=modern?.features.find(f=>f.properties?.code==='MAR');
  if(morocco)data.features=data.features.map(f=>f.properties?.code==='MAR'?{...f,geometry:morocco.geometry,properties:{...f.properties,territorialReference:true,geometrySource:'https://www.naturalearthdata.com/',note:'Contorno contemporáneo de referencia, separado del Sáhara Occidental. No reconstruye las líneas de control de cada año.'}}:f);
  const existing=new Set(data.features.map(f=>f.properties?.entityCode));
  data.features.push(...supplements.features.filter(f=>f.properties!.start<=`${year}-12-31`&&f.properties!.end>=`${year}-12-31`&&!existing.has(f.properties!.entityCode)));
  return data;
}
export const modernCities=()=>asset<FeatureCollection>('cities.geojson');
export async function overlaysFor(year:number):Promise<FeatureCollection>{
  const files=['territorial-overlays.geojson',...(year>=1990?['recent-control.geojson']:[]),...(year>=1914&&year<=1949?['historical-control.geojson']:[]),...(year>=1936&&year<=1939?['spanish-civil-war.geojson']:[])];
  const data=await Promise.all(files.map(f=>asset<FeatureCollection>(f)));
  return {type:'FeatureCollection',features:data.flatMap(d=>d.features).filter(f=>f.properties!.start<=year&&f.properties!.end>=year).map(f=>{
    const p=f.properties!;
    const controller=p.controller??(p.uid==='crimea'?'RUS':p.kind==='dispute'?'ISR':'');
    return {...f,properties:{...p,controller,identityKey:p.identityKey??controller,controlColor:p.controlColor??(controller==='ISR'?'#679ab6':regimeColor(controller,year))}};
  })};
}
