import clipping, {type MultiPolygon as ClipMultiPolygon, type Polygon as ClipPolygon} from 'polygon-clipping';
import type {Feature, FeatureCollection, Polygon, MultiPolygon} from 'geojson';
import {regimeColor} from './political';
import {centralEuropeanControls} from './central-europe';
import {applyControlPartition,type PartitionControls} from './wartime-partition';

type Area=Feature<Polygon|MultiPolygon>;
const area=(f:Feature):f is Area=>f.geometry.type==='Polygon'||f.geometry.type==='MultiPolygon';
const coords=(f:Area)=>f.geometry.coordinates as ClipPolygon|ClipMultiPolygon;
const feature=(f:Feature,coordinates:ClipMultiPolygon):Area=>({...f,geometry:{type:'MultiPolygon',coordinates}});
const empty=():FeatureCollection=>({type:'FeatureCollection',features:[]});
function bounds(f:Area){
 const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;
 const box=[Infinity,Infinity,-Infinity,-Infinity];
 for(const polygon of polygons)for(const ring of polygon)for(const [x,y] of ring){box[0]=Math.min(box[0],x);box[1]=Math.min(box[1],y);box[2]=Math.max(box[2],x);box[3]=Math.max(box[3],y);}
 return box;
}
function overlaps(a:number[],b:number[]){return a[0]<=b[2]&&a[2]>=b[0]&&a[1]<=b[3]&&a[3]>=b[1];}
/** Documentary correction: the original CShapes record ends Danzig a year early.
 * Apply its unchanged source contour after control composition so the1938
 * German outline cannot also own the city. This is not an occupation overlay.
 */
function correctDanzig(base:FeatureCollection,territories:FeatureCollection,occupations:FeatureCollection){
 const reference=base.features.find(f=>f.properties?.boundaryCorrection==='danzig-1938');
 if(!reference||!area(reference))return {territories,occupations};
 const box=bounds(reference);
 const subtract=(features:Feature[])=>features.flatMap(f=>{
  if(!area(f)||!overlaps(bounds(f),box))return [f];
  const intersection=clipping.intersection(coords(f),coords(reference));if(!intersection.length)return [f];
  const remaining=clipping.difference(coords(f),coords(reference));return remaining.length?[feature(f,remaining)]:[];
 });
 return {territories:{...territories,features:[...subtract(territories.features.filter(f=>f.properties?.identityKey!=='DAN')),reference]},occupations:{...occupations,features:subtract(occupations.features)}};
}
/** Compose the displayed control map, without mutating or redistributing source geometries.
 * Boolean geometry runs in a worker. Optional hatching never changes this inventory.
 * Each hatch retains the documentary territory and controller, not a claim of sovereignty.
 */
export function composeControl(base:FeatureCollection,controls:PartitionControls,year:number){
 if(controls.partition)return applyControlPartition(base,controls.partition,year);
 controls=centralEuropeanControls(base,controls,year);
 if(!controls.features.length)return correctDanzig(base,base,empty());
 let territories=base.features.slice();const occupations=empty();
 const annexations=controls.features.filter(f=>area(f)&&f.properties?.kind==='annexation-mask') as Area[];
 const civil=controls.features.filter(f=>f.properties?.kind==='civil-war'&&area(f)) as Area[];
 if(civil.length){
  const boxes=civil.map(bounds);
  // The Spanish fronts are independently licensed BY-SA 3.0 partitions on a
  // Natural Earth outline. Replace the matching Spanish components as a
  // collection, never clip NC-SA CShapes with that incompatible SA geometry.
  territories=territories.flatMap(f=>{
   if(!area(f)||!String(f.properties?.identityKey).startsWith('ESP'))return [f];
   const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;
   const retained=polygons.filter(coordinates=>!boxes.some(box=>overlaps(bounds({type:'Feature',properties:{},geometry:{type:'Polygon',coordinates}}),box)));
   return retained.length?[{...f,geometry:{type:'MultiPolygon' as const,coordinates:retained}}]:[];
  });
  const partitions=civil.map((f,index)=>{const p:Record<string,any>={...f.properties,politicalColor:regimeColor(f.properties!.controller,year),controlComponent:true,controlRecord:f.properties!.uid,controlNote:f.properties!.note,controlSource:f.properties!.source};delete p.uid;return {...f,id:6100000+index,properties:p};});
  territories=[...partitions,...territories];
 }
 for(const [index,control] of controls.features.entries()){
  if(!area(control)||!control.properties?.controller)continue;
  if(control.properties.kind==='annexation-mask')continue;
  if(control.properties.kind==='civil-war')continue;
  const p=control.properties,controller=String(p.controller),box=bounds(control);
  // A reference outline explicitly lacking phase geometry is contextual only.
  if(p.uid==='sinai-withdrawal')continue;
  const root=territories.find(f=>f.properties?.identityKey===controller);
  if(p.occupiedKey){
   const occupied=base.features.find(f=>f.properties?.identityKey===p.occupiedKey)?.properties;
   const occupiedColor=occupied?.politicalColor??regimeColor(p.occupiedKey,year),controlColor=regimeColor(controller,year);
   occupations.features.push({...control,id:7000000+index*10000,properties:{...p,occupiedName:occupied?.name??p.occupiedKey,occupiedColor,controlColor,patternKey:`${controlColor}:${occupiedColor}`}});
  }
  const own=root&&area(root)?coords(root):undefined;
  const remaining:Feature[]=[];
  for(const f of territories){
   if(!area(f)||!overlaps(bounds(f),box)){remaining.push(f);continue;}
   const q=f.properties??{};
   const same=q.identityKey===controller;
   if(same)continue; // Its original geometry is merged into the controller below.
   const overlap=clipping.intersection(coords(f),coords(control));
   if(!overlap.length){remaining.push(f);continue;}
   if(!p.occupiedKey&&!same&&!['client','civil-war','incorporation'].includes(String(p.relation))&&p.kind!=='civil-war'&&(q.administratorKey!==controller||q.status==='occupied')){
    let intersection=overlap;
    for(const annexation of annexations.filter(a=>a.properties?.controller===controller))if(intersection.length)intersection=clipping.difference(intersection,coords(annexation));
    const occupiedColor=q.status==='occupied'?regimeColor(q.identityKey,year):q.politicalColor??'#a5a092';
    if(intersection.length)occupations.features.push(feature({type:'Feature',id:7000000+index*10000+occupations.features.length,geometry:f.geometry,properties:{...p,occupiedKey:q.identityKey,occupiedName:q.name,occupiedColor,controlColor:regimeColor(controller,year),patternKey:`${regimeColor(controller,year)}:${occupiedColor}`}},intersection));
   }
   const difference=clipping.difference(coords(f),coords(control));
   if(difference.length)remaining.push(feature(f,difference));
  }
  // Merge the controller's original territory and the sourced control extent.
  // Remove its remaining component before inserting the unified feature.
  territories=remaining.filter(f=>f!==root&&!(root&&f.id===root.id));
  const geometry=own?clipping.union(own,coords(control)):clipping.union(coords(control));
  const properties={...(root?.properties??p),identityKey:controller,controller,politicalColor:regimeColor(controller,year),controlComponent:true,controlName:p.name,controlNote:p.note,controlSource:p.source,controlRecord:p.uid,...(p.observationDate?{controlObservationDate:p.observationDate,controlUncertaintyMetres:p.registrationUncertaintyMetres}: {})};
  // A controller has a persistent country anchor rather than an overlay UID.
  delete (properties as Record<string,unknown>).uid;
  territories.push(feature({type:'Feature',id:root?.id??6000000+index,geometry:control.geometry,properties},geometry));
 }
 // The dated1939 replacement partitions the old Czechoslovak component into
 // occupied Czech lands, the Slovak client and Hungarian incorporation. Do not
 // leave a selectable predecessor made of numerical clipping remnants.
 if(year===1939&&controls.features.some(f=>f.properties?.uid==='central-slovakia-reference-1939'))territories=territories.filter(f=>f.properties?.identityKey!=='CSK');
 return correctDanzig(base,{...base,features:territories},occupations);
}
