import{describe,it,expect,vi}from'vitest';import{readFileSync,writeFileSync}from'node:fs';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{regionsAt,entitiesAt,regionalCard,hasRegionalCoverage,regionalAsset}from'../src/cultural-regions';import{anchorFor,matchingFeature}from'../src/selection';import{systemYear}from'../src/time';
const read=(f:string)=>JSON.parse(readFileSync(f,'utf8')),all=read('public/data/cultural-regions.geojson'),ids=read('public/data/identities.json'),empty:any={type:'FeatureCollection',features:[]};
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const active=(y:number)=>regionsAt(all,y,empty).features,byContext=(y:number,k:string)=>active(y).find(f=>f.properties?.contextKey===k)!;
const contemporary=read('public/data/countries.geojson'),profiles=read('public/data/profiles.json');
const politicalAt=async(year:number)=>year>=2020?politicalData(contemporary,year,profiles):politicalData(await annualData(year),year);
describe('cultural consultation1905–present',()=>{
 it('retains every1905 cultural context annually, without modifying political data or extending political references',async()=>{
  const base=active(1905).filter(f=>f.properties?.kind==='cultural-region'),keys=base.map(f=>f.properties?.contextKey),annual=[];expect(keys).toHaveLength(1769);
  for(let year=1900;year<=2027;year++){
   expect(hasRegionalCoverage(year)).toBe(true);expect(regionalAsset(year)).toBeDefined();const p=await politicalAt(year),before=JSON.stringify(p),r=regionsAt(all,year,p);expect(JSON.stringify(p)).toBe(before);expect(p.features.length).toBeGreaterThan(40);
   if(year>1905){const actual=new Set(r.features.map(f=>f.properties?.contextKey));for(const k of keys)expect(actual.has(k),String(k)+' '+year).toBe(true);expect(r.features.every(f=>f.properties?.kind==='cultural-region')).toBe(true);}
   annual.push({year,politicalFeatures:p.features.length,culturalReferences:r.features.filter(f=>f.properties?.kind==='cultural-region').length,politicalReferences:r.features.filter(f=>f.properties?.kind==='polity-reference').length,evidenceThrough:year>1905?2026:undefined,prospectiveReferenceOnly:year>2026});
  }
  if(process.env.WRITE_REGIONAL_AUDIT==='1')writeFileSync('docs/CULTURAL-MODERN-ANNUAL-REVIEW.json',JSON.stringify({scope:'Consultation, political preservation and cultural availability1900–2027. Not a census or independent verification of all current boundaries.2027 is reference availability only.',annual},null,2)+'\n');expect(hasRegionalCoverage(2028)).toBe(false);
 },120000);
 it('distinguishes documentary institutional dates from the age or territorial extent of a people',()=>{
  const k='CULTURE-SAMI';expect(regionalCard(byContext(1972,k).properties as any,1972,true)).not.toContain('Delegación Sámi desde1973');expect(regionalCard(byContext(1973,k).properties as any,1973,true)).toContain('Delegación Sámi desde1973');expect(regionalCard(byContext(1996,k).properties as any,1996,true)).toContain('autonomía cultural');expect(regionalCard(byContext(2026,k).properties as any,2026,true)).toContain('agosto de2025');
  expect(byContext(1974,'CULTURE-MAORI-2565AD9A').properties?.interpretation).not.toContain('creado por la ley de1975');expect(byContext(1975,'CULTURE-MAORI-2565AD9A').properties?.interpretation).toContain('creado por la ley de1975');expect(byContext(1985,'CULTURE-MAORI-2565AD9A').properties?.interpretation).toContain('desde1840');expect(byContext(2019,'CULTURE-HOKKAIDO').properties?.interpretation).toContain('mayo de2019');expect(byContext(1999,'CULTURE-INUIT-BE0E1C96').properties?.interpretation).toContain('no equivale sólo aNunavut');
 });
 it('does not redraw traditional areas as modern reserves or future observations',()=>{
  const key='CULTURE-BURARRA-903375F8',before=byContext(1905,key),after=byContext(2026,key);expect(after.geometry).toEqual(before.geometry);expect(after.properties?.temporalMode).toBe('historical-area-context');expect(regionalCard(after.properties as any,2026,true)).toContain('no los sustituye');expect(regionalCard(byContext(2027,key).properties as any,2027,true)).toContain('no hay observaciones futuras');expect(regionalCard(after.properties as any,2026,true)).not.toContain('regional-future');expect(systemYear(new Date(2027,5,1))).toBe(2027);
 });
 it('keeps simultaneous political and cultural selections across decolonization and current reference data',async()=>{
  const original=byContext(1905,'CULTURE-BURARRA-903375F8'),anchor=anchorFor(original.properties!,1905,ids);for(const year of[1906,1945,1960,1999,2020,2026]){const p=await politicalAt(year),r=regionsAt(all,year,p),at=entitiesAt(original.properties!.focus,p,r);expect(matchingFeature(anchor,r,year,ids)).toBeDefined();expect(at[0].properties?.contextKey).toBeUndefined();expect(at.some(f=>f.properties?.contextKey===anchor.key),year+':'+at.map(f=>f.properties?.name).join(',')).toBe(true);}
 });
 it('keeps the former published endpoint resource and serves complete new century segments',()=>{
  const idx=read('public/data/cultural-index.json'),manifest=read('public/data/manifest.json');expect(manifest.entries.find((e:any)=>e.file==='cultural-regions-1900-1905.geojson').archivedReference).toBe(true);expect(regionalAsset(1906)).toBe('cultural-regions-1900-1999.geojson');expect(regionalAsset(2026)).toBe('cultural-regions-2000-2027.geojson');for(const y of[1906,1996,2007,2026,2027]){const s=read('public/data/'+regionalAsset(y));expect(regionsAt(s,y,empty).features).toEqual(active(y));}expect(idx.reviewedThrough).toBe(2027);
 });
});
