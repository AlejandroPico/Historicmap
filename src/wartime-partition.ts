import type {FeatureCollection} from 'geojson';
import {regimeColor} from './political';

export type ControlPartition={replaceIds:(string|number)[];territories:FeatureCollection;occupations:FeatureCollection};
export type PartitionControls=FeatureCollection&{partition?:ControlPartition};
export type WartimePartitions={format:'dated-control-partitions';years:Record<string,ControlPartition>};

/** Replace political features, not their paint. Both the map and selection use
 * this single ownership inventory; hatching is only a view of its final cuts. */
export function applyControlPartition(base:FeatureCollection,partition:ControlPartition,year:number){
 const replaced=new Set(partition.replaceIds);
 const territories:FeatureCollection={type:'FeatureCollection',features:[
  ...base.features.filter(f=>!replaced.has(f.id!)),
  ...partition.territories.features.map(f=>f.properties?.controller?{...f,properties:{...f.properties,politicalColor:regimeColor(f.properties.controller,year)}}:f)
 ]};
 const occupations:FeatureCollection={...partition.occupations,features:partition.occupations.features.map(f=>{
  const p=f.properties!,controlColor=regimeColor(p.controller,year);
  return {...f,properties:{...p,controlColor,patternKey:`${controlColor}:${p.occupiedColor}`}};
 })};
 return {territories,occupations};
}
