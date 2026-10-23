import {describe,it,expect} from 'vitest';
import {politicalData,regimeColor,dependencyColor,influenceFor,politicalInfluences} from '../src/political';
import type {FeatureCollection} from 'geojson';
import type {ProfileData} from '../src/profiles';
const feature=(properties:Record<string,unknown>)=>({type:'Feature' as const,geometry:{type:'Polygon' as const,coordinates:[]},properties});
const paint=(code:string,year:number)=>politicalData({type:'FeatureCollection',features:[feature({code,name:code,status:'independent'})]},year).features[0].properties!;
describe('dated colour families for documented political dependency',()=>{
 it('keeps Soviet satellites red but visually distinct, with dates and sources',()=>{
  const soviet=regimeColor('USSR',1980);
  for(const key of ['POL','HUN','CSK','BGR','DDR']){
   const p=paint(key,1980);
   expect(p.dominantPower).toBe('USSR');expect(p.politicalColor).toBe(dependencyColor(soviet,key));expect(p.politicalColor).not.toBe(soviet);
   const rgb=p.politicalColor.match(/\w{2}/g)!.map((c:string)=>parseInt(c,16));expect(rgb[0]).toBeGreaterThan(rgb[1]+50);expect(p.influenceSource).toMatch(/^https:/);
  }
  expect(paint('POL',1990).dominantPower).toBeUndefined();expect(paint('DDR',1989).dominantPower).toBe('USSR');
 });
 it('does not infer subordination from communism, a modern alliance or a past relationship',()=>{
  for(const code of ['YUG','ALB','CHN','CUB','USA','FRA'])expect(paint(code,1980).dominantPower).toBeUndefined();
  expect(influenceFor('ALB',1960)?.power).toBe('USSR');expect(influenceFor('ALB',1970)).toBeUndefined();
  expect(paint('ROU',1980).politicalColor).toBe(dependencyColor(regimeColor('USSR',1980),'ROU',true));
 });
 it('uses the actual administrator colour for colonies even if its name is not a hardcoded alias',()=>{
  const data:FeatureCollection={type:'FeatureCollection',features:[feature({code:'PRT',name:'Portugal',originalName:'Portugal',status:'independent'}),feature({code:'',name:'Angola',originalName:'Angola',status:'colony',ownerName:'Portugal'})]};
  const result=politicalData(data,1970).features;
  expect(result[1].properties!.politicalColor).toBe(dependencyColor(regimeColor('PRT',1970),'Angola'));
  expect(result[1].geometry).toBe(data.features[1].geometry);
 });
 it('keeps intervention paint separate so the occupation switch can restore the sovereign base',()=>{
  const afghan=paint('AFG',1980);expect(afghan.politicalColor).toBe(regimeColor('AFG',1980));expect(afghan.controlInfluenceColor).toBe(dependencyColor(regimeColor('USSR',1980),'AFG'));
  expect(paint('AFG',1989).controlInfluenceColor).toBeUndefined();
  expect(paint('JPN',1950).controlInfluenceColor).toBe(dependencyColor(regimeColor('USA',1950),'JPN'));expect(paint('JPN',1952).controlInfluenceColor).toBeUndefined();
  expect(paint('SVK',1942).dominantPower).toBe('DEU');
 });
 it('uses contemporary dependency metadata only in the contemporary reference and excludes disputed claims',()=>{
  const data:FeatureCollection={type:'FeatureCollection',features:[feature({code:'USA',name:'Estados Unidos',group:'United States of America'}),feature({code:'GUM',name:'Guam'}),feature({code:'SAH',name:'Sáhara Occidental'})]};
  const profiles:ProfileData={retrieved:'2026-10-22',countries:{GUM:{name:'Guam',capital:'Agaña',territoryType:'Dependency',sovereign:'United States of America',series:{}},SAH:{name:'Sáhara Occidental',capital:'',territoryType:'Disputed',sovereign:'United States of America',series:{}}}};
  const contemporary=politicalData(data,2026,profiles).features;
  expect(contemporary[1].properties!.politicalColor).toBe(dependencyColor(regimeColor('USA',2026),'GUM'));
  expect(contemporary[2].properties!.dominantPower).toBeUndefined();
  expect(politicalData(data,1970,profiles).features[1].properties!.dominantPower).toBeUndefined();
 });
 it('has unambiguous, sourced intervals for every curated relationship',()=>{
  for(const r of politicalInfluences){expect(r.start<r.end).toBe(true);expect(r.note).not.toBe('');expect(r.source).toMatch(/^https:/);
   for(const other of politicalInfluences)if(r.id!==other.id&&r.keys.some(k=>other.keys.includes(k)))expect(r.end<=other.start||other.end<=r.start).toBe(true);
  }
 });
});
