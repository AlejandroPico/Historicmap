import{readFileSync}from'node:fs';import{describe,it,expect}from'vitest';
import{snapshotFor,navigationYear,playbackYear,anchors}from'../src/time';
import{distributionsAt,distributionCoast,distributionCard,coexistencePattern,lineageCatalogue}from'../src/human-distributions';
import{containsLocation,entitiesAt}from'../src/cultural-regions';
import{iceEnabledFor,climateRecordFor}from'../src/ice-automatic';
import{anchorFor,matchingFeature}from'../src/selection';
import{humanEvidenceAt}from'../src/prehistory';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),raw=read('public/data/human-ranges.geojson'),sites=read('public/data/hominin-sites.geojson'),empty={type:'FeatureCollection' as const,features:[]};
describe('dated hominin distributions and automatic ice',()=>{
 it('keeps the deep human timeline distinct from political borders and coasts dated by model',()=>{
  for(const y of[-7000000,-6500000,-4400000,-3200000,-1800000,-300000,-100001])expect(snapshotFor(y).kind).toBe('prehistoric');
  expect(snapshotFor(-10000).kind).toBe('annual');expect(snapshotFor(-300000000).kind).toBe('geological');expect(playbackYear(-3200000)).toBe(-3190000);expect(navigationYear(-300000,1)).toBe(-299000);expect(anchors.every((y,i)=>i===0||y>anchors[i-1])).toBe(true);
  expect(distributionCoast(-3200000)).toBe('coastlines-3.geojson');expect(distributionCoast(-4200000)).toBe('coastlines-4.geojson');expect(distributionCoast(-100000)).toBe('countries.geojson');
 });
 it('represents actual phase changes and does not extend inferred distributions beyond their windows',()=>{
  expect(distributionsAt(raw,-6500000).areas.features.some(f=>f.properties!.lineage==='sahelanthropus')).toBe(true);
  expect(distributionsAt(raw,-3200000).areas.features.some(f=>f.properties!.lineage==='afarensis')).toBe(true);
  const early=distributionsAt(raw,-45000).areas.features.find(f=>f.properties!.lineage==='sapiens')!,later=distributionsAt(raw,-42000).areas.features.find(f=>f.properties!.lineage==='sapiens')!;
  expect(containsLocation(early.geometry,[25,45])).toBe(false);expect(containsLocation(later.geometry,[25,45])).toBe(true);
  expect(distributionsAt(raw,-14000).areas.features.filter(f=>f.properties!.lineage==='sapiens').some(f=>containsLocation(f.geometry,[-70,-30]))).toBe(false);
  expect(distributionsAt(raw,-12000).areas.features.some(f=>f.properties!.lineage==='sapiens'&&containsLocation(f.geometry,[-70,-30]))).toBe(true);
  expect(distributionsAt(raw,-10001).areas.features.length).toBeGreaterThan(0);expect(distributionsAt(raw,-10000).areas.features).toHaveLength(0);
 });
 it('partitions shared regions while preserving both full selectable lineages without inventing a war',()=>{
  const result=distributionsAt(raw,-42000),shared=result.overlaps.features.find(f=>f.properties!.members.includes('sapiens')&&f.properties!.members.includes('neanderthal'))!;expect(shared).toBeDefined();
  const hits=entitiesAt([25,45],empty,result.areas);expect(hits.map(f=>f.properties!.lineage)).toEqual(expect.arrayContaining(['sapiens','neanderthal']));
  for(const k of shared.properties!.members)expect(result.areas.features.some(f=>f.properties!.lineage===k)).toBe(true);
  const card=distributionCard(hits[0].properties!,-42000);expect(card).toContain('No se deducen guerras');expect(card).toContain('frontera biológica exacta');
  const p=coexistencePattern(['#ff0000','#0000ff']),focused=coexistencePattern(['#ff0000','#0000ff'],0);let red=0,focusRed=0;for(let i=0;i<p.data.length;i+=4){red+=Number(p.data[i]===255);focusRed+=Number(focused.data[i]===255);}expect(red).toBe(288);expect(focusRed).toBeGreaterThan(red);
 });
 it('does not count alternative Denisovan names as separate biological populations',()=>{
  expect(lineageCatalogue.taxa).toHaveLength(39);for(const key of['longi','juluensis','georgicus','bodoensis']){const d=lineageCatalogue.taxa.find(t=>t.key===key)!;expect(d.regions).toHaveLength(0);expect(d.classification).toContain('alternativa');}
  for(const t of lineageCatalogue.taxa){const {canonicalFile,...compiled}=t;expect(compiled).toEqual(read(canonicalFile));}
  expect(sites.features).toHaveLength(1007);expect(sites.features.filter((f:any)=>f.properties.originalRow)).toHaveLength(982);
  expect(sites.features.filter((f:any)=>f.properties.originalRow)).toEqual(read('Tierra/Humanidad/fossiles/timmermann2022-anteriores.json').records);
  for(const f of raw.features){expect(f.properties.canonicalFile).toMatch(/^Tierra\/Humanidad\/linajes\//);expect(f.properties.source).toMatch(/^https:\/\//);expect(f.properties.start).toBeLessThanOrEqual(f.properties.end);expect(f.properties.spatialUncertaintyKm).toBeGreaterThan(0);}
 });
 it('keeps new fossil references selectable without inheriting a political authority',()=>{
  const f=humanEvidenceAt(sites,-3200000).features.find(f=>f.properties!.identityKey==='HOMININ-REF-afarensis')!,ids={countries:{},retrieved:'2026-11-01',source:'',license:''};expect(f).toBeDefined();
  const anchor=anchorFor(f.properties!,-3200000,ids);expect(anchor.key).toBe('HOMININ-REF-afarensis');expect(matchingFeature(anchor,{...empty,features:[f]},-3200000,ids)).toBe(f);
  expect(humanEvidenceAt(sites,-2000000).features.some(f=>f.properties!.identityKey==='HOMININ-REF-afarensis')).toBe(false);
 });
 it('uses data-supported excess ice with a manual override and never extrapolates to unmodelled ages',()=>{
  expect(iceEnabledFor(2026,'auto')).toBe(false);expect(iceEnabledFor(-4000,'auto')).toBe(false);expect(iceEnabledFor(-20000,'auto')).toBe(true);expect(iceEnabledFor(-100000,'auto')).toBe(false);expect(iceEnabledFor(-3200000,'on')).toBe(true);
  expect(iceEnabledFor(-20000,'off')).toBe(false);expect(iceEnabledFor(2026,'on')).toBe(true);
  expect(climateRecordFor(-3200000)).toBeDefined();expect(climateRecordFor(-6500000)).toBeUndefined();
 });
});
