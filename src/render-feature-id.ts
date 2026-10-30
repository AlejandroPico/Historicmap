import type {FeatureCollection} from 'geojson';
import{displayLabel,culturalColor}from'./map-presentation';
export const RENDER_ID='__atlasId';
/** Preserve arbitrary source IDs in a promoted property across vector tiles,
 * hit testing and feature state. Original geometry and IDs stay untouched. */
export function withRenderIds(data:FeatureCollection,scope:string):FeatureCollection{
 const used=new Set<string|number>();
 return {...data,features:data.features.map((f,index)=>{
  const id=f.id??`atlas:${scope}:${index}`;
  if(used.has(id))throw Error(`Duplicate render identity ${id}`);
  used.add(id);
  const p=f.properties??{};
  return {...f,id,properties:{...p,...(p.name?{name:displayLabel(p.name),sourceDisplayName:p.name}:{}),...(p.contextKey?{color:culturalColor(p)}:{}),[RENDER_ID]:id}};
 })};
}
