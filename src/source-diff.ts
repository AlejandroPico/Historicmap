import type {FeatureCollection} from 'geojson';
import type {GeoJSONSourceDiff} from 'maplibre-gl';
/** Only send changed entities to the map worker; IDs must already be unique. */
export function sourceDiff(before:FeatureCollection,after:FeatureCollection):GeoJSONSourceDiff{
  const old=new Map(before.features.map(f=>[f.id!,f]));
  const next=new Set(after.features.map(f=>f.id!));
  const diff:Required<Pick<GeoJSONSourceDiff,'remove'|'add'|'update'>>={remove:before.features.filter(f=>!next.has(f.id!)).map(f=>f.id!),add:[],update:[]};
  for(const f of after.features){
    const previous=old.get(f.id!);
    if(!previous){diff.add.push(f);continue;}
    const propertiesChanged=JSON.stringify(previous.properties)!==JSON.stringify(f.properties);
    const geometryChanged=previous.geometry!==f.geometry;
    if(!propertiesChanged&&!geometryChanged)continue;
    // geojson-vt 6.3 returns immediately on removeAllProperties, ignoring any
    // additions in that same update. Send explicit deletions instead, keeping
    // worker tiles and the authoritative GeoJSON in agreement.
    const removed=Object.keys(previous.properties??{}).filter(key=>!Object.hasOwn(f.properties??{},key));
    diff.update.push({id:f.id!,...(geometryChanged?{newGeometry:f.geometry}:{}),...(propertiesChanged?{...(removed.length?{removeProperties:removed}:{}),addOrUpdateProperties:Object.entries(f.properties??{}).map(([key,value])=>({key,value}))}:{})});
  }
  return diff;
}
