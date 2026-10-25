import type {FeatureCollection} from 'geojson';
import {applyControlPartition,type PartitionControls} from './wartime-partition';
type Result={territories:FeatureCollection;occupations:FeatureCollection};
let worker:Worker|undefined,sequence=0;
const pending=new Map<number,{resolve:(r:Result)=>void;reject:(e:Error)=>void}>();
const cache=new Map<number,Promise<Result>>();
export function controlledMap(base:FeatureCollection,controls:PartitionControls,year:number):Promise<Result>{
 if(controls.partition)return Promise.resolve(applyControlPartition(base,controls.partition,year));
 if(!controls.features.length)return Promise.resolve({territories:base,occupations:{type:'FeatureCollection',features:[]}});
 const previous=cache.get(year);if(previous)return previous;
 if(!worker){
  worker=new Worker(new URL('./control-worker.ts',import.meta.url),{type:'module'});
  worker.onmessage=({data})=>{const request=pending.get(data.id);pending.delete(data.id);if(data.error)request?.reject(new Error(data.error));else request?.resolve(data.result);};
  worker.onerror=event=>{for(const request of pending.values())request.reject(new Error(event.message));pending.clear();worker?.terminate();worker=undefined;cache.clear();};
 }
 const id=++sequence;
 const promise=new Promise<Result>((resolve,reject)=>{pending.set(id,{resolve,reject});worker!.postMessage({id,base,controls,year});}).catch(error=>{cache.delete(year);throw error;});
 cache.set(year,promise);if(cache.size>3)cache.delete(cache.keys().next().value!);
 return promise;
}
