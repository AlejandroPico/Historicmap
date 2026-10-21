import {it,expect} from 'vitest';
import {sourceDiff} from '../src/source-diff';
import type {FeatureCollection,Feature} from 'geojson';
const feature=(id:number,name:string,geometry:Feature['geometry']):Feature=>({type:'Feature',id,properties:{name},geometry});
it('removes obsolete periods and sends only changed entity properties or geometry',()=>{
 const geometry:Feature['geometry']={type:'Point',coordinates:[0,0]};
 const before:FeatureCollection={type:'FeatureCollection',features:[feature(1,'old',geometry),feature(2,'keep',geometry),feature(3,'removed',geometry)]};
 const added=feature(4,'new',geometry);
 const after:FeatureCollection={type:'FeatureCollection',features:[feature(1,'updated',geometry),before.features[1],added]};
 const diff=sourceDiff(before,after);
 expect(diff.remove).toEqual([3]);expect(diff.add).toEqual([added]);
 expect(diff.update).toEqual([{id:1,removeAllProperties:true,addOrUpdateProperties:[{key:'name',value:'updated'}]}]);
 expect(sourceDiff(after,after)).toEqual({remove:[],add:[],update:[]});
});
