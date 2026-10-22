import {describe,it,expect} from 'vitest';
import {appearances,palettes,resolveAppearance} from '../src/appearance';
describe('device-local appearance',()=>{
 it('uses local morning, afternoon and night boundaries',()=>{
  for(const [hour,expected] of [[0,'night'],[6,'night'],[7,'morning'],[12,'morning'],[13,'afternoon'],[19,'afternoon'],[20,'night'],[23,'night']] as const)expect(resolveAppearance('auto',new Date(2026,9,22,hour))).toBe(expected);
  expect(resolveAppearance('morning',new Date(2026,9,22,23))).toBe('morning');
  expect(appearances).toEqual(['morning','afternoon','night','auto']);
 });
 it('keeps the ocean lighter than the outer background in each palette',()=>{
  const luminance=(hex:string)=>hex.slice(1).match(/../g)!.map(v=>parseInt(v,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
  for(const palette of Object.values(palettes))expect(luminance(palette.ocean)).toBeGreaterThan(luminance(palette.background));
 });
});
