import{describe,it,expect,vi}from'vitest';
import{readFileSync,writeFileSync}from'node:fs';import{createHash}from'node:crypto';
import{hasRegionalCoverage,regionsAt,regionalCard,entitiesAt}from'../src/cultural-regions';
import{anchorFor,matchingFeature}from'../src/selection';import{annualData}from'../src/data';import{politicalData}from'../src/political';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),regions=read('public/data/cultural-regions.geojson'),identities=read('public/data/identities.json'),empty:any={type:'FeatureCollection',features:[]};
const regionalByPhase=new Map(regions.features.map((f:any)=>[f.properties.key+':'+f.properties.start,f]));
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));
const active=(y:number)=>regionsAt(regions,y,empty).features;
describe('regional references and consultation phases 1200–1700',()=>{
 it('preserves the earlier inventory and represents cultures in every new annual selection',async()=>{
  expect(regions.features.filter((f:any)=>f.properties.end<=1200&&f.properties.sourceYear===1000)).toHaveLength(127);
  for(let y=1201;y<=1700;y++){expect(hasRegionalCoverage(y),String(y)).toBe(true);const r=active(y);expect(r.filter(f=>f.properties?.kind==='cultural-region').length,String(y)).toBeGreaterThan(40);expect(r.some(f=>f.properties?.contextKey==='CULTURE-SAMI'),String(y)).toBe(true);expect(r.some(f=>f.properties?.contextKey==='CULTURE-AMAZON'),String(y)).toBe(true);}
  expect(hasRegionalCoverage(1906)).toBe(false);
  const years=[];for(const y of[1200,1201,1250,1279,1300,1400,1492,1500,1530,1600,1650,1700]){const p=politicalData(await annualData(y),y),before=JSON.stringify(p),r=regionsAt(regions,y,p);expect(JSON.stringify(p)).toBe(before);years.push({year:y,politicalFeatures:p.features.length,regionalReferences:r.features.length,sourceYears:[...new Set(r.features.map(f=>f.properties?.sourceYear))]});}
  if(process.env.WRITE_REGIONAL_AUDIT==='1'){const annual=[];for(let y=1201;y<=1700;y++)annual.push({year:y,references:active(y).length});writeFileSync('docs/CULTURAL-AVAILABILITY-1201-1700.json',JSON.stringify({scope:'Availability of documentary references, not a territorial completeness or historical certainty score.',samples:years,annual},null,2)+'\n');}
 });
 it('updates a stable regional identity across spatial and cultural phases',()=>{
  const f=active(1200).find(f=>f.properties?.contextKey==='CULTURE-HOKKAIDO')!,anchor=anchorFor(f.properties!,1200,identities);expect(f.properties?.name).toContain('Satsumon');const next=matchingFeature(anchor,{...empty,features:active(1300)},1300,identities)!;expect(next).toBeDefined();expect(next.properties?.name).toContain('ainu');expect(next.properties?.sourceYear).toBe(1300);expect(anchor.key).toBe('CULTURE-HOKKAIDO');
 });
 it('has disjoint phases and distinct Hawaii/Rapa Nui components',()=>{
  const groups=new Map<string,any[]>();for(const f of regions.features){const p=f.properties;groups.set(p.contextKey,[...groups.get(p.contextKey)??[],p]);}
  for(const[key,phases]of groups){phases.sort((a,b)=>a.start-b.start);for(let i=1;i<phases.length;i++)expect(phases[i-1].end,key).toBeLessThan(phases[i].start);}
  const maori=regions.features.filter((f:any)=>f.properties.originalNames.some((n:string)=>['Maori','Maoris'].includes(n)));expect(new Set(maori.map((f:any)=>f.properties.contextKey)).size).toBe(1);
  for(const f of regions.features.filter((f:any)=>f.properties.sourceYear>1000&&f.properties.start<f.properties.sourceYear)){expect(f.properties.contextKey).toBe('CULTURE-MAORI-2565AD9A');expect(f.properties.sourceYear).toBe(1279);}
  for(const y of[1201,1300,1492,1600,1700]){const r=active(y);const h=r.find(f=>f.properties?.contextKey==='CULTURE-HAWAII')!,n=r.find(f=>f.properties?.contextKey==='CULTURE-RAPA-NUI')!;expect(h).toBeDefined();expect(n).toBeDefined();expect(h.geometry).not.toEqual(n.geometry);expect(entitiesAt([-109.32,-27.12],empty,{...empty,features:[h]})).toHaveLength(0);}
  expect(active(1249).some(f=>String(f.properties?.name).includes('Aotearoa'))).toBe(false);expect(active(1250).some(f=>String(f.properties?.name).includes('Aotearoa'))).toBe(true);
 });
 it('keeps traditional-area uncertainty visible and avoids inherited contemporary offices',()=>{
  const f=active(1600).find(f=>f.properties?.originalNames.includes('Burarra'))!;expect(f).toBeDefined();expect(f.properties?.temporalMode).toBe('traditional-area-undated');const html=regionalCard(f.properties as any,1600,true);expect(html).toContain('datación local pendiente');expect(html).toContain('NO acredita');expect(html).not.toContain('leader-name');expect(html).not.toContain('historic-flag');expect(regionalCard(f.properties as any,1906,false)).toContain('no indica desaparición');
 });
 it('accounts for all source names and checksums, without fusing diacritic names',()=>{
  const report=read('docs/CULTURAL-REVIEW-900-1700.json');const expected:any={1200:129,1279:113,1300:113,1400:115,1492:1307,1500:139,1530:269,1600:638,1650:593,1700:584};
  for(const[year,count]of Object.entries(expected))expect(report.sourceInventories.find((s:any)=>s.year===Number(year)).names.length,year).toBe(count);
  const source=report.sourceInventories.find((s:any)=>s.year===1492);expect(source.names.some((n:any)=>n.name==='Awá')).toBe(true);expect(source.names.some((n:any)=>n.name==='Ãwa')).toBe(true);const a=active(1492).find(f=>f.properties?.originalNames.includes('Awá'))!,b=active(1492).find(f=>f.properties?.originalNames.includes('Ãwa'))!;expect(a.properties?.contextKey).not.toBe(b.properties?.contextKey);expect(a.geometry).not.toEqual(b.geometry);
  for(const r of report.entities.filter((r:any)=>r.sourceYear!==1000)){
   const d=read(r.file),raw=readFileSync(r.file.replace(/[^/]+$/,d.geometryFile));expect(createHash('sha256').update(raw).digest('hex'),d.key).toBe(d.geometrySha256);expect(d.originalSourceProperties.length,d.key).toBe(d.geometryProvenance.featureIds.length);if(d.decision==='adopted-reference')for(const phase of d.phases){const f=regionalByPhase.get(d.key+':'+phase.start) as any;expect(f,d.key).toBeDefined();expect(f.geometry).toEqual(JSON.parse(raw.toString()).geometry);expect(f.properties.contextKey).toBe(d.contextKey??d.key);}
  }
 },300000);
 it('does not revive obsolete powers or project modern relocation areas into this period',()=>{
  for(const f of regions.features.filter((f:any)=>f.properties.sourceYear>1000&&f.properties.start<=1700))expect(f.properties.originalNames.some((n:string)=>/Oklahoma|First Nation|Treaty Group|Council|Comanche|Huari Empire|Fatimid Caliphate|Hong Kong/.test(n)),f.id).toBe(false);
  expect(active(1530).some(f=>f.properties?.originalNames.includes('Luba'))).toBe(false);expect(active(1650).some(f=>f.properties?.originalNames.includes('Luba'))).toBe(true);
  expect(active(1492).filter(f=>f.properties?.originalNames.includes('Funj')).every(f=>f.properties?.kind==='cultural-region')).toBe(true);expect(active(1503).find(f=>f.properties?.originalNames.includes('Funj'))?.properties?.kind).toBe('cultural-region');expect(active(1504).find(f=>f.properties?.originalNames.includes('Funj'))?.properties?.kind).toBe('polity-reference');
  expect(active(1590).find(f=>f.properties?.originalNames.includes('Songhai'))?.properties?.kind).toBe('polity-reference');expect(active(1591).find(f=>f.properties?.originalNames.includes('Songhai'))?.properties?.kind).toBe('cultural-region');expect(active(1650).find(f=>f.properties?.originalNames.includes('Songhai'))?.properties?.kind).toBe('cultural-region');
 });
 it('keeps Siberian communities selectable under the dated political representation',async()=>{
  const p=politicalData(await annualData(1650),1650),r=regionsAt(regions,1650,p),cases=[[65,64],[72,64],[75,60],[67,67],[80,68],[90,65]].map(point=>({point,names:entitiesAt(point,p,r).map(f=>[f.properties?.identityKey,f.properties?.contextKey,f.properties?.name])}));if(process.env.WRITE_REGIONAL_AUDIT==='1')writeFileSync('.cache/overlap029.json',JSON.stringify(cases,null,2));expect(cases.some(c=>c.names.some(n=>n[0]==='RUSSIA-TSARDOM')&&c.names.some(n=>n[1])),JSON.stringify(cases)).toBe(true);
 });
});
