import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{hasRegionalCoverage,regionsAt,containsLocation,entitiesAt,regionalCard}from'../src/cultural-regions';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{anchorFor,matchingFeature}from'../src/selection';import type{FeatureCollection}from'geojson';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8')),regions=read('cultural-regions.geojson'),ids=read('identities.json');
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
describe('coexisting cultural regions and political entities',()=>{
 it('keeps cultural coverage across every annual boundary900–1200 without changing political records',async()=>{
  const active=(y:number)=>regionsAt(regions,y,{type:'FeatureCollection',features:[]}).features.filter(f=>f.properties?.kind==='cultural-region');
  for(let y=900;y<=1200;y++){expect(hasRegionalCoverage(y)).toBe(true);const r=active(y);expect(r.length).toBeGreaterThan(40);expect(r.some(f=>f.properties?.contextKey==='CULTURE-SAMI')).toBe(true);expect(r.some(f=>f.properties?.contextKey==='CULTURE-AMAZON')).toBe(true);}
  expect(hasRegionalCoverage(1201)).toBe(false);expect(active(1201)).toHaveLength(0);
  for(const y of[900,999,1000,1099,1100,1199,1200]){const political=politicalData(await annualData(y),y),before=JSON.stringify(political);regionsAt(regions,y,political);expect(JSON.stringify(political)).toBe(before);}
  if(process.env.WRITE_REGIONAL_AUDIT==='1'){
   const years=[];for(let year=900;year<=1200;year++){const p=politicalData(await annualData(year),year),r=regionsAt(regions,year,p);years.push({year,politicalFeatures:p.features.length,culturalAndGeographicReferences:r.features.filter(f=>f.properties?.kind==='cultural-region').length,additionalPoliticalReferences:r.features.filter(f=>f.properties?.kind==='polity-reference').length});}
   writeFileSync('docs/CULTURAL-AVAILABILITY-900-1200.json',JSON.stringify({scope:'Annual availability of displayed records, not populations, sovereign countries, independently verified annual extents or a spatial completeness percentage.',years},null,2)+'\n');
  }
 });
 it('does not repeat represented sovereigns or create a medieval Merina kingdom',async()=>{
  const p=politicalData(await annualData(1000),1000),r=regionsAt(regions,1000,p);expect(r.features.some(f=>f.properties?.contextKey==='REFERENCE-KINGDOM-OF-FRANCE')).toBe(false);
  expect(regions.features.some((f:any)=>f.properties.originalNames.includes('Merina Kingdom'))).toBe(false);expect(regions.features.find((f:any)=>f.properties.contextKey==='CULTURE-ZIMBABWE').properties.start).toBe(1100);
  const h=regions.features.find((f:any)=>f.properties.contextKey==='CULTURE-HOKKAIDO');expect(h.geometry.coordinates).toHaveLength(1);expect(h.properties.name).toContain('Satsumon');
 });
 it('retains independent selections under a kingdom, with political priority and no inherited leaders',()=>{
  const geometry={type:'Polygon',coordinates:[[[0,0],[10,0],[10,10],[0,10],[0,0]]]}as const;
  const p:FeatureCollection=JSON.parse(JSON.stringify({type:'FeatureCollection',features:[{type:'Feature',id:'kingdom',geometry,properties:{identityKey:'FRA',name:'Reino'}}]}));
  const c:FeatureCollection=JSON.parse(JSON.stringify({type:'FeatureCollection',features:[{type:'Feature',id:'culture',geometry,properties:{contextKey:'CULTURE-TEST',name:'Pueblo',kind:'cultural-region',start:900,end:1200}}]}));
  expect(entitiesAt([5,5],p,c).map(f=>f.id)).toEqual(['kingdom','culture']);const anchor=anchorFor(c.features[0].properties!,1000,ids);expect(anchor.key).toBe('CULTURE-TEST');expect(matchingFeature(anchor,p,1000,ids)).toBeUndefined();expect(matchingFeature(anchor,c,1000,ids)?.id).toBe('culture');
  const r=regions.features.find((f:any)=>f.properties.contextKey==='CULTURE-SAMI');const html=regionalCard(r.properties,1201,false);expect(html).toContain('no indica desaparición');expect(html).not.toContain('Jefatura');expect(html).toContain('Referencia espacial');
 });
 it('resolves polygon holes, multiple parts and the date line',()=>{
  const polygon:any={type:'Polygon',coordinates:[[[0,0],[10,0],[10,10],[0,10],[0,0]],[[4,4],[6,4],[6,6],[4,6],[4,4]]]};expect(containsLocation(polygon,[2,2])).toBe(true);expect(containsLocation(polygon,[5,5])).toBe(false);expect(containsLocation(polygon,[12,2])).toBe(false);
  const dateline:any={type:'Polygon',coordinates:[[[170,-10],[-170,-10],[-170,10],[170,10],[170,-10]]]};expect(containsLocation(dateline,[179,0])).toBe(true);expect(containsLocation(dateline,[-179,0])).toBe(true);expect(containsLocation(dateline,[0,0])).toBe(false);
 });
 it('documents coexisting records at real geographical locations',async()=>{
  const p=politicalData(await annualData(1100),1100),r=regionsAt(regions,1100,p);
  const cases=[[18,67],[27.8,66.9],[10,60],[18,61],[24,62],[33,60],[50,60],[60,60],[85,55],[-8,14],[-10,12],[10,12],[20,15],[25,15],[39,-6],[100,15],[110,1],[-89,17],[-3,53]].map(point=>({point,names:entitiesAt(point,p,r).map(f=>f.properties?.name)}));if(process.env.WRITE_REGION_AUDIT==='1')writeFileSync('.cache/overlap028.json',JSON.stringify(cases));expect(cases.some(c=>c.names.length>=2),JSON.stringify(cases)).toBe(true);
 });
 it('accounts for every named source feature and preserves adopted coordinate arrays',async()=>{
  const audit=JSON.parse(readFileSync('docs/CULTURAL-REVIEW-900-1200.json','utf8')),source=read('world_1000.geojson');
  for(const f of source.features.filter((f:any)=>f.properties.name!=='Masa continental'))expect(audit.entities.some((r:any)=>r.originalNames.includes(f.properties.name)),f.properties.name).toBe(true);
  for(const r of audit.entities){const d=JSON.parse(readFileSync(r.file,'utf8'));expect(d.references.length).toBeGreaterThan(0);if(d.decision==='excluded'){expect(d.interpretation.length).toBeGreaterThan(40);continue;}
   const coordinates=d.geometryProvenance.featureIds.flatMap((i:number)=>source.features[i].geometry.type==='MultiPolygon'?source.features[i].geometry.coordinates:[source.features[i].geometry.coordinates]);
   const expected=d.geometryProvenance.components?d.geometryProvenance.components.map((i:number)=>coordinates[i]):coordinates;
   const original=JSON.parse(readFileSync(r.file.replace(/[^/]+$/,d.geometryFile),'utf8'));expect(original.geometry.coordinates).toEqual(expected);expect(regions.features.find((f:any)=>f.properties.contextKey===d.key)?.geometry).toEqual(original.geometry);
   for(const phase of d.phases){const p=regions.features.find((f:any)=>f.properties.contextKey===d.key&&f.properties.start===phase.start&&f.properties.end===phase.end)?.properties;expect(p,d.key).toBeDefined();expect(p.references).toEqual(d.references);expect(p.name).toBe(phase.label??d.name);expect(p.sourceYear).toBe(d.geometryProvenance.year);expect(p.spatialUncertainty).toBe(d.spatialUncertainty);}
  }
  const p=politicalData(await annualData(1000),1000),r=regionsAt(regions,1000,p);const overlapping=entitiesAt([33.3,35.09],p,r);expect(overlapping.some(f=>f.properties?.identityKey==='BYZANTINE')).toBe(true);expect(overlapping.some(f=>f.properties?.contextKey==='REFERENCE-CYPRUS')).toBe(true);
 });
});
