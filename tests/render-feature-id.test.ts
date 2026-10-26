import {it,expect} from 'vitest';
import {GeoJSONVT} from '@maplibre/geojson-vt';
import type {FeatureCollection} from 'geojson';
import {withRenderIds,RENDER_ID} from '../src/render-feature-id';
import {canonicalFeature} from '../src/selection';
import {sourceDiff} from '../src/source-diff';
it('preserves Cliopatria string identities through promoted tile properties and dated updates',()=>{
 const raw:FeatureCollection={type:'FeatureCollection',features:[{type:'Feature',id:'clio-8805',properties:{name:'Francia',identityKey:'FRA'},geometry:{type:'Point',coordinates:[2,48]}}]};
 const saved=JSON.stringify(raw),before=withRenderIds(raw,'history-1885');
 const vt=new GeoJSONVT(before,{updateable:true,promoteId:RENDER_ID});
 const tile=vt.getTile(0,0,0)!.features[0];
 expect(tile.tags![RENDER_ID]).toBe('clio-8805');
 expect(canonicalFeature({id:tile.tags![RENDER_ID] as string,properties:{}},before)?.properties?.identityKey).toBe('FRA');
 const after=withRenderIds({...raw,features:raw.features.map(f=>({...f,properties:{...f.properties,name:'Francia actualizada'}}))},'history-1884');
 vt.updateData(sourceDiff(before,after));expect(vt.getTile(0,0,0)!.features[0].tags!.name).toBe('Francia actualizada');
 expect(JSON.stringify(raw)).toBe(saved);expect(before.features[0].geometry).toBe(raw.features[0].geometry);
 expect(()=>withRenderIds({...raw,features:[raw.features[0],raw.features[0]]},'duplicate')).toThrow(/Duplicate/);
});
