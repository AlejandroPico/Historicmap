import{readFileSync}from'node:fs';import{describe,it,expect}from'vitest';
import{snapshotFor,playbackYear,navigationYear,ANNUAL_CONSULTATION_START}from'../src/time';
import{regionalAsset,regionalAssets,regionsAt,hasRegionalCoverage}from'../src/cultural-regions';
import{humanEvidenceAt,humanGroupCounts,humanEvidenceMarkup,groupsFor}from'../src/prehistory';
import{iceSampleFor,yearFromAge}from'../src/ice-history';
import{canonicalFeature,anchorFor,matchingFeature}from'../src/selection';
import{comparisonShell,comparisonMarkup}from'../src/country-comparison';
import{emptyIndicators}from'../src/country-workspace';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),data=read('public/data/human-evidence.geojson'),inventory=read('docs/PALEOLITHIC-INVENTORY.json'),ids=read('public/data/identities.json'),empty={type:'FeatureCollection' as const,features:[]};
describe('100000–10001BCE: individually dated human evidence',()=>{
 it('keeps exact consultation separate from political annual maps and advances without giant jumps',()=>{
  expect(snapshotFor(-100001).kind).toBe('concept');expect(snapshotFor(-100000).kind).toBe('prehistoric');expect(snapshotFor(-10001).kind).toBe('prehistoric');expect(snapshotFor(-10000).kind).toBe('annual');expect(ANNUAL_CONSULTATION_START).toBe(-10000);
  for(const y of[-100000,-80000,-60000,-40000,-20000,-10001]){expect(regionalAsset(y)).toBe('human-evidence.geojson');expect(hasRegionalCoverage(y)).toBe(true);expect(regionsAt(data,y,empty).features.length).toBeGreaterThan(0);}
  expect(hasRegionalCoverage(-100001)).toBe(false);expect(playbackYear(-100000)).toBe(-99900);expect(navigationYear(-60000,1)).toBe(-59900);expect(navigationYear(-100000,-1)).toBe(-100100);expect(playbackYear(-10001)).toBe(-10000);expect(playbackYear(-10000)).toBe(-9999);expect(navigationYear(-1,1)).toBe(1);
  expect(read('public/data/historical-context.json').startYear).toBe(ANNUAL_CONSULTATION_START);expect(read('public/data/country-history.json').coverageStart).toBe(ANNUAL_CONSULTATION_START);
 });
 it('keeps every original accepted source row and binds all records to an owned dossier',()=>{
  expect(inventory.canonicalDossiers).toHaveLength(565);expect(data.features).toHaveLength(2820);const raw=data.features.filter((f:any)=>f.properties.originalRow);expect(raw).toHaveLength(2390);expect(new Set(raw.map((f:any)=>f.properties.originalRow)).size).toBe(2390);
  for(const f of data.features){const p=f.properties;expect(f.geometry.type).toBe('Point');expect(p.canonicalFile).toMatch(/^Países\/[^/]+\/arqueologia\/bc100000-bc10001(?:-paleohumans)?\.json$/);expect(p.start).toBeLessThanOrEqual(p.end);expect(p.attributionBasis).toBeTruthy();expect(p.dateBasis).toBeTruthy();if(p.originalRow){expect(p.originalWorkbookSha256).toBe(inventory.workbook.sha256);expect(p.originalProperties).toBeTruthy();}expect(ids.countries[p.identityKey],p.identityKey).toBeDefined();}
  for(const file of inventory.canonicalDossiers){const d=read(file);expect(d.leaders).toEqual([]);expect(d.symbols).toEqual([]);expect(d.entityRules).toEqual([]);expect(d.homininEvidence.length).toBeGreaterThan(0);}
  expect(inventory.mergedSiteReferences).toHaveLength(3);expect(inventory.rejected).toHaveLength(1);
 });
 it('checks every interval change, so no dating gap is filled by a site’s outer range',()=>{
  // Between adjacent boundaries the active set is constant; an annual loop
  // would repeat identical interval predicates ninety thousand times.
  const boundaries=new Set<number>([-100000,-10001]);for(const f of data.features){boundaries.add(f.properties.start);if(f.properties.end<-10001)boundaries.add(f.properties.end+1);}
  for(const y of boundaries){const sites=humanEvidenceAt(data,y),expected=data.features.filter((f:any)=>f.properties.start<=y&&y<=f.properties.end);expect(sites.features.reduce((n,f)=>n+f.properties!.evidenceCount,0),String(y)).toBe(expected.length);expect(new Set(sites.features.map(f=>f.properties!.identityKey)).size).toBe(sites.features.length);for(const f of sites.features)expect(f.properties!.evidenceRecords.every((r:any)=>r.start<=y&&y<=r.end)).toBe(true);}
 },60000);
 it('distinguishes biological assignments, mixed attributions and material cultures without national symbols',()=>{
  const site=(k:string,y:number)=>humanEvidenceAt(data,y).features.find(f=>f.properties!.identityKey===k)!;
  const denisova=site('ARCHAEOLOGY-DENISOVA',-90000);expect(denisova.properties!.taxonGroups).toContain('denisovan');expect(denisova.properties!.taxonGroups).toContain('neanderthal');expect(denisova.properties!.taxonGroups).toContain('mixed');expect(humanEvidenceMarkup(denisova.properties!)).toContain('Las industrias no identifican por sí solas una especie');
  expect(site('ARCHAEOLOGY-BAISHIYA',-40000).properties!.taxonGroups).toContain('denisovan');expect(site('ARCHAEOLOGY-LIANG-BUA',-70000).properties!.taxonGroups).toContain('flores');expect(site('ARCHAEOLOGY-MADJEDBEBE',-60000).properties!.taxonGroups).toContain('sapiens');expect(site('ARCHAEOLOGY-WHITE-SANDS',-20000)).toBeTruthy();expect(site('ARCHAEOLOGY-WHITE-SANDS',-40000)).toBeUndefined();expect(groupsFor('H. sapiens / Neanderthal')).toEqual(['sapiens','neanderthal']);expect(humanGroupCounts(humanEvidenceAt(data,-90000)).find(g=>g.id==='mixed')!.count).toBeGreaterThan(0);
 });
 it('restores complete point records from tile hits and retains the same owner through the10000 seam',()=>{
  const a=humanEvidenceAt(data,-10500),f=a.features.find(f=>f.properties!.identityKey==='ARCHAEOLOGY-LAPA-DO-SANTO')!,hit={id:999,properties:{identityKey:f.properties!.identityKey,referenceKind:'archaeological-site'}};
  expect(canonicalFeature(hit,a)).toBe(f);expect(canonicalFeature({...hit,properties:{...hit.properties,identityKey:'missing'}},a)).toBeUndefined();const anchor=anchorFor(f.properties!,-10500,ids);expect(anchor.place).toBe(false);expect(matchingFeature(anchor,humanEvidenceAt(data,-10001),-10001,ids)?.properties!.identityKey).toBe(anchor.key);expect(matchingFeature(anchor,humanEvidenceAt(data,-60000),-60000,ids)).toBeUndefined();
 });
 it('does not extrapolate ice beyond the model or substitute a contemporary coastline reconstruction',()=>{
  expect(iceSampleFor(-100000)).toBeUndefined();expect(iceSampleFor(-78052)).toBeUndefined();expect(iceSampleFor(-78051)?.ageBP).toBe(80000);expect(iceSampleFor(yearFromAge(22500))?.ageBP).toBe(22500);expect(iceSampleFor(yearFromAge(62500))?.ageBP).toBe(65000);
 });
 it('compares dated archaeological evidence instead of manufacturing political or economic observations',()=>{
  const f=humanEvidenceAt(data,-10500).features.find(f=>f.properties!.identityKey==='ARCHAEOLOGY-LAPA-DO-SANTO')!,anchor=anchorFor(f.properties!,-10500,ids),state={mode:'dates' as const,a:-10600,b:-10400,metric:'population',pinned:[]},profiles={retrieved:'',countries:{}};
  expect(comparisonShell(state,-10500,profiles,emptyIndicators)).toContain('min="-100000"');const html=comparisonMarkup([{anchor,year:-10600,feature:f},{anchor,year:-10400,feature:f}],state,profiles,emptyIndicators,ids,'/',-10500);expect(html).toContain('Intervalos activos');expect(html).toContain('Homo sapiens');expect(html).not.toContain('retraso máximo de cinco años');expect(html).not.toContain('Fuente territorial');
 });
 it('adds Upper Palaeolithic skeletal contexts without treating raw radiocarbon measurements as calendar dates',()=>{
  const ph=data.features.filter((f:any)=>f.properties.sourceDataset==='PaleoHumans1.0.0');expect(ph).toHaveLength(417);expect(inventory.PaleoHumans.canonicalDossiers).toHaveLength(250);expect(inventory.PaleoHumans.unmapped).toHaveLength(5);expect(inventory.PaleoHumans.sharedOwners).toHaveLength(10);
  for(const f of ph){const p=f.properties,source=p.originalProperties;expect(p.dateQuality).toBe('archaeological-culture-window');expect(p.sourceSnapshotSha256).toBe(inventory.PaleoHumans.archiveSha256);expect(p.ageMinBP).toBe(Number(source.culture.end_bp));expect(p.ageMaxBP).toBe(Number(source.culture.start_bp));expect(p.start).toBe(yearFromAge(p.ageMaxBP));expect(p.end).toBe(yearFromAge(p.ageMinBP));expect(source.culture.culture_name).not.toBe('Uncertain');expect(Array.isArray(source.dating)).toBe(true);}
  expect(humanEvidenceAt(data,-20551).features.length).toBeGreaterThan(40);expect(read('public/data/human-evidence-index.json').sites).toBe(new Set(data.features.map((f:any)=>f.properties.identityKey)).size);
 });
 it('keeps source-supported human contexts alongside cultural areas across10001/10000 until their actual published window ends',()=>{
  const regional=read('public/data/cultural-regions.geojson'),merged={...data,features:[...data.features,...regional.features]},sample=data.features.find((f:any)=>f.properties.sourceDataset==='PaleoHumans1.0.0'&&f.properties.end===-9751)!.properties;
  expect(regionalAssets(-10000)).toEqual([regionalAsset(-10000),'human-evidence.geojson']);expect(regionalAssets(-9000)).not.toContain('human-evidence.geojson');for(const y of[-10001,-10000,-9751])expect(regionsAt(merged,y,empty).features.some(f=>f.properties!.identityKey===sample.identityKey)).toBe(true);const at=regionsAt(merged,-10000,empty);expect(at.features.some(f=>f.properties!.contextKey==='CULTURE-TASMANIA')).toBe(true);expect(at.features.some(f=>f.properties!.evidenceRecords)).toBe(true);expect(humanEvidenceAt(data,-9750).features.some(f=>f.properties!.identityKey===sample.identityKey)).toBe(false);
 });
});
