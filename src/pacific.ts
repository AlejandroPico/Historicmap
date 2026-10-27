import {isoYear} from './dates';
import type {Feature,FeatureCollection,Polygon,MultiPolygon} from 'geojson';
import components from '../public/data/pacific-components.json';
/** Split named island components out of source aggregates. Coordinates are
 * reused verbatim and removed from the aggregate, so there is one owner. */
export function pacificComponents(data:FeatureCollection,year:number):FeatureCollection{
 if(year<1800||year>1885)return data;
 return {...data,features:data.features.flatMap(f=>{
  const rows=components.records.filter(r=>r.sourceFeatureId===f.id&&r.start<=year&&r.end>=year);
  if(!rows.length||!['Polygon','MultiPolygon'].includes(f.geometry.type))return [f];
  const g=f.geometry as Polygon|MultiPolygon,polygons=g.type==='Polygon'?[g.coordinates]:g.coordinates;
  const removed=new Set(rows.flatMap(r=>r.sourceComponentIndexes));
  const retained=polygons.filter((_,i)=>!removed.has(i));
  const result:Feature[]=retained.length?[{...f,geometry:{type:'MultiPolygon',coordinates:retained}}]:[];
  for(const r of rows){const admin=r.entityCode==='GUM'?'ESP':'FRA';result.push({...f,id:r.id,geometry:{type:'MultiPolygon',coordinates:r.sourceComponentIndexes.map(i=>polygons[i])},properties:{...f.properties,name:r.entityCode==='GUM'?'Guam':'Nueva Caledonia',originalName:r.entityCode==='GUM'?'Guam':'New Caledonia',identityKey:r.entityCode,entityCode:r.entityCode,code:'',status:'colony',administratorKey:admin,localAuthorityKey:r.entityCode,ownerName:admin==='ESP'?'España':'Francia',sourceFeatureId:r.sourceFeatureId,sourceOriginalName:r.sourceOriginalName,sourceComponentExtraction:true,note:'Componente separado del agregado histórico, conservando sus coordenadas y retirándolo de éste. No se añade una costa superpuesta.'}});}
  return result;
 })};
}
/** Add only reference islands omitted by the dated source or older supplements. */
export function pacificReferences(data:FeatureCollection,year:number,references:FeatureCollection):FeatureCollection{
 if(year<1800||year>2019)return data;
 const aliases:Record<string,string>={'New Caledonia and Dependencies':'NCL','French Polynesia':'PYF','Fiji':'FJI'};
 const features=data.features.map(f=>{const key=aliases[String(f.properties?.originalName??f.properties?.country_name??'')];return key?{...f,properties:{...f.properties,identityKey:key,entityCode:key,localAuthorityKey:key}}:f;});
 const existing=new Set(features.flatMap(f=>[f.properties?.identityKey,f.properties?.entityCode,f.properties?.code]));
 const date=`${isoYear(year)}-12-31`;
 return {...data,features:[...features,...references.features.filter(f=>f.properties!.start<=date&&f.properties!.end>=date&&!existing.has(f.properties!.identityKey))]};
}
