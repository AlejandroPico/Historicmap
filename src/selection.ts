import type {Feature,FeatureCollection} from 'geojson';
import {identityKey,type IdentityData} from './identities';

export type CountryAnchor={key:string;name:string;originalName:string;code:string;uid:string;place:boolean;country:string;properties:Record<string,any>;year:number};
/** Tile properties are a rendering projection, never the country record. */
export function canonicalFeature(hit:{id?:string|number;properties:Record<string,any>|null}|undefined,data:FeatureCollection):Feature|undefined{
 if(!hit)return;
 const p=hit.properties??{};
 // Point IDs can be rewritten by the vector-tile worker (especially string
 // GeoJSON IDs). Resolve their immutable documentary identity before IDs.
 // Polygon selection still requires an exact renderer/source match.
 if(p.rank!==undefined&&p.country&&data.features.every(f=>f.geometry.type==='Point')){
  if(p.uid)return data.features.find(f=>f.properties?.uid===p.uid);
  return data.features.find(f=>f.properties?.name===p.name&&f.properties?.country===p.country);
 }
 if(hit.id!==undefined)return data.features.find(f=>f.id===hit.id);
 if(p.uid)return data.features.find(f=>f.properties?.uid===p.uid);
 if(p.name&&p.country)return data.features.find(f=>f.properties?.name===p.name&&f.properties?.country===p.country);
 return undefined;
}
export function anchorFor(p:Record<string,any>,year:number,identities:IdentityData):CountryAnchor{
 return {key:identityKey(p,year,identities),name:p.name??'',originalName:p.originalName??p.name??'',code:p.entityCode??p.code??'',uid:p.uid??'',place:p.rank!==undefined&&Boolean(p.country),country:p.country??'',properties:{...p},year};
}
/** Match the entity, never an arbitrary nearest polygon or one of its successors. */
export function matchingFeature(anchor:CountryAnchor,data:FeatureCollection,year:number,identities:IdentityData):Feature|undefined{
 return data.features.find(f=>{
  const p=f.properties??{};
  if(anchor.place){const normalize=(s:string)=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();return normalize(p.name??'')===normalize(anchor.name)&&(anchor.key?identityKey(p,year,identities)===anchor.key:p.country===anchor.country);}
  if(anchor.uid)return p.uid===anchor.uid;
  if(p.uid)return false;
  if(anchor.key)return identityKey(p,year,identities)===anchor.key;
  return (p.originalName??p.name)===anchor.originalName&&(!anchor.code||(p.entityCode??p.code)===anchor.code);
 });
}
