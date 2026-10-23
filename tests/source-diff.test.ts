import {it,expect} from 'vitest';
import {sourceDiff} from '../src/source-diff';
import type {FeatureCollection,Feature} from 'geojson';
import {GeoJSONVT} from '@maplibre/geojson-vt';
import {canonicalFeature} from '../src/selection';
const feature=(id:number,name:string,geometry:Feature['geometry']):Feature=>({type:'Feature',id,properties:{name},geometry});
it('removes obsolete periods and sends only changed entity properties or geometry',()=>{
 const geometry:Feature['geometry']={type:'Point',coordinates:[0,0]};
 const before:FeatureCollection={type:'FeatureCollection',features:[feature(1,'old',geometry),feature(2,'keep',geometry),feature(3,'removed',geometry)]};
 const added=feature(4,'new',geometry);
 const after:FeatureCollection={type:'FeatureCollection',features:[feature(1,'updated',geometry),before.features[1],added]};
 const diff=sourceDiff(before,after);
 expect(diff.remove).toEqual([3]);expect(diff.add).toEqual([added]);
 expect(diff.update).toEqual([{id:1,addOrUpdateProperties:[{key:'name',value:'updated'}]}]);
 expect(sourceDiff(after,after)).toEqual({remove:[],add:[],update:[]});
 // A control worker's structured clone is not a change to a coastline.
 expect(sourceDiff(after,structuredClone(after))).toEqual({remove:[],add:[],update:[]});
});
it('preserves name, identity and colour in the actual tile index through reversals and removes obsolete metadata',()=>{
 const geometry:Feature['geometry']={type:'Point',coordinates:[2,48]};
 const collection=(properties:Record<string,unknown>):FeatureCollection=>({type:'FeatureCollection',features:[{type:'Feature',id:1,geometry,properties}]});
 let before=collection({name:'Francia',identityKey:'FRA',politicalColor:'#6796ad',influenceKind:'old'});
 const tiles=new GeoJSONVT(before,{updateable:true});
 for(const properties of [{name:'Francia',identityKey:'FRA',politicalColor:'#6a9db1'},{name:'Francia',identityKey:'FRA',politicalColor:'#6796ad',influenceKind:'old'},{name:'Francia',identityKey:'FRA',politicalColor:'#6a9db1'}]){
  const after=collection(properties);tiles.updateData(sourceDiff(before,after));
  expect(tiles.getTile(0,0,0)!.features.find(f=>f.id===1)!.tags).toEqual(properties);before=after;
 }
 expect(canonicalFeature({id:1,properties:{}},before)?.properties?.identityKey).toBe('FRA');
 expect(canonicalFeature({id:999,properties:{name:'Francia'}},before)).toBeUndefined();
});
