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
 it('keeps blue water ordered from light morning to dark night without changing the night palette',()=>{
  const rgb=(s:string)=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16));
  for(const p of Object.values(palettes)){const [r,,b]=rgb(p.ocean);expect(b).toBeGreaterThan(r);}
  const sum=(s:string)=>rgb(s).reduce((a,b)=>a+b,0);expect(sum(palettes.morning.ocean)).toBeGreaterThan(sum(palettes.afternoon.ocean));expect(sum(palettes.afternoon.ocean)).toBeGreaterThan(sum(palettes.night.ocean));expect(palettes.night).toEqual({background:'#080f19',ocean:'#152b3b',horizon:'#566b7e'});
 });

});
