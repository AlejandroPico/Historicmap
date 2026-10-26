import type {Feature,FeatureCollection} from 'geojson';
import catalogue from '../public/data/historical-places.json';
import {historicalCapitals} from './history';
type UrbanRecord={id:string;keys:string[];name:string;coordinates:number[];start:number;end:number;capital:boolean;role:string;source:string;note:string;keyPeriods?:Record<string,number[]>};
export function datedPlaces(data:FeatureCollection,year:number):FeatureCollection{
 const result=historicalCapitals(data),active=new Map<string,Record<string,any>>();
 for(const f of data.features){const p=f.properties??{},key=p.identityKey??p.entityCode??p.code;if(key&&!active.has(key))active.set(key,p);}
 for(const r of catalogue.records as UrbanRecord[]){
  if(year<r.start||year>r.end)continue;
  const key=r.keys.find(k=>active.has(k)&&(!r.keyPeriods?.[k]||r.keyPeriods[k][0]<=year&&r.keyPeriods[k][1]>=year));
  if(!key)continue;const p=active.get(key)!;
  // Existing source seats win. Deduplicate different-language names at the
  // same location without suppressing a dated change to another city.
  const duplicate=result.features.some(f=>f.geometry.type==='Point'&&Math.abs(f.geometry.coordinates[0]-r.coordinates[0])<.08&&Math.abs(f.geometry.coordinates[1]-r.coordinates[1])<.08&&(f.properties?.identityKey??f.properties?.entityCode)===key);
  if(duplicate)continue;
  result.features.push({type:'Feature',id:r.id,geometry:{type:'Point',coordinates:r.coordinates},properties:{name:r.name,originalName:r.name,identityKey:key,entityCode:p.entityCode??key,code:p.code??'',country:p.name,capital:r.capital,rank:r.capital?1:3,role:r.role,note:r.role+'. '+r.note,source:r.source,status:p.status,administratorKey:p.administratorKey,localAuthorityKey:p.localAuthorityKey,referenceKind:'dated-urban-reference'}} as Feature);
 }
 return result;
}
