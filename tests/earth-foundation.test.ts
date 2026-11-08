import{describe,it,expect}from'vitest';
import{geologicalUnits,geologicalAt,humanAt,humanUnits,humanChronologySources,chronologyVersion,geologicalEmphasis}from'../src/earth-chronology';
import{chronologyBands}from'../src/chronology-bands';
import{planetRecords,planetSources,planetRecordFor,planetValue,planetReferenceLabel,type PlanetRecord}from'../src/planet';
import{planetCard}from'../src/planet-card';
import{yearToPosition,PRESENT}from'../src/time';
import{HOLOCENE_START}from'../src/ice-history';

describe('Earth foundation: chronological and evidential boundaries',()=>{
 it('retains a complete ICS hierarchy, with no overlapping same-rank units at handovers',()=>{
  expect(chronologyVersion).toBe('2026/06');expect(geologicalUnits).toHaveLength(178);
  const ids=new Set(geologicalUnits.map(u=>u.id));expect(ids.size).toBe(178);
  for(const u of geologicalUnits){
   expect(u.name).not.toBe('');expect(u.parent===null||ids.has(u.parent)).toBe(true);
   expect(u.axisOldestYear).toBeLessThan(u.axisEndYear??PRESENT);
   if(u.rank==='group')continue;
   for(const year of[u.axisOldestYear-1,u.axisOldestYear,u.axisOldestYear+1]){
    const at=geologicalAt(year).filter(v=>v.rank===u.rank);expect(at.length,`${u.id}:${year}`).toBeLessThanOrEqual(1);
   }
  }
  const a=geologicalUnits.find(u=>u.id==='Archean')!;
  expect(geologicalAt(a.axisOldestYear-1).some(u=>u.id==='Hadean')).toBe(true);
  expect(geologicalAt(a.axisOldestYear).some(u=>u.id==='Archean')).toBe(true);
 });
 it('keeps precise b2k GSSPs and geological continuity through1BCE/1CE',()=>{
  const h=geologicalUnits.find(u=>u.id==='Holocene')!;
  expect(h.axisOldestYear).toBe(HOLOCENE_START);expect(h.axisOldestYear).toBe(-9701);
  expect(geologicalAt(-9702).some(u=>u.id==='Pleistocene')).toBe(true);
  expect(geologicalAt(-9701).some(u=>u.id==='Holocene')).toBe(true);
  expect(geologicalAt(-6237).some(u=>u.id==='Northgrippian')).toBe(true);
  expect(geologicalAt(-2251).some(u=>u.id==='Meghalayan')).toBe(true);
  expect(geologicalAt(-1).map(u=>u.id)).toEqual(geologicalAt(1).map(u=>u.id));
  expect(()=>geologicalAt(0)).toThrow();
 });
 it('declares regional historical conventions and preserves overlapping transformations',()=>{
  for(const u of humanUnits){expect(u.scope).not.toBe('');expect(u.formal).toBe(false);expect(humanChronologySources[u.sourceId].url).toMatch(/^https:/);}
  expect(humanAt(2026).map(u=>u.id)).toEqual(expect.arrayContaining(['contemporary','digital','space-age']));
  expect(humanAt(-4000).find(u=>u.id==='neolithic')?.scope).toContain('Francia');
 });
 it('clips moving bands, resolves overlaps and changes emphasis without ending geology',()=>{
  for(const year of[-4540000000,-4030998051,-100000000,-7000000,-100000,-4000,1,1800,PRESENT]){
   for(const spacing of[96,230,4800]){
    const model=chronologyBands(year,yearToPosition(year),spacing,390);
    for(const b of model.bands){expect(b.x).toBeGreaterThanOrEqual(0);expect(b.width).toBeGreaterThan(0);expect(b.x+b.width).toBeLessThanOrEqual(390.000001);}
    for(let row=0;row<3;row++)for(const family of['human','geological']){
     const bands=model.bands.filter(b=>b.family===family&&b.row===row).sort((a,b)=>a.x-b.x);
     for(let i=1;i<bands.length;i++)expect(bands[i-1].x+bands[i-1].width).toBeLessThanOrEqual(bands[i].x+.00001);
    }
   }
  }
  expect(geologicalEmphasis(-100000000,1000)).toBe(1);
  expect(geologicalEmphasis(2026,1000)).toBe(0);
  expect(geologicalAt(2026).some(u=>u.id==='Holocene')).toBe(true);
 });
 it('never assigns modern measurements backwards or relabels a reference as a newer year',()=>{
  expect(planetRecordFor('oxygen',1990)).toBeUndefined();
  expect(planetRecordFor('temperatureAnomaly',2023)).toBeUndefined();
  expect(planetRecordFor('temperatureAnomaly',2024)?.value).toBe(1.55);
  expect(planetRecordFor('temperatureAnomaly',2026)?.reference).toEqual({basis:'civil',year:2025});
  expect(planetRecordFor('temperatureAnomaly',2027)?.reference).toEqual({basis:'civil',year:2025});
  for(const r of planetRecords){expect(planetSources[r.sourceId].url).toMatch(/^https:/);expect(r.interpolation).toBe('none');expect(r.method).not.toBe('');}
  const bounded={...planetRecords[0],availableFromYear:1900,validUntilYear:1910};
  expect(planetRecordFor(bounded.field,1911,[bounded])).toBeUndefined();
 });
 it('distinguishes unknown, zero, ranges, asymmetric errors and temporal bases',()=>{
  const base={...planetRecords[0],value:0,unit:'°C',evidence:'estimate'} as PlanetRecord;
  expect(planetValue(base)).toBe('0 °C');expect(planetValue({...base,value:null})).toContain('Sin estimación');
  expect(planetValue({...base,value:{min:10,max:20}})).toBe('10–20 °C');
  expect(planetValue({...base,uncertainty:{minus:1,plus:2,description:'rango'}})).toBe('0 −1/+2 °C');
  expect(planetReferenceLabel({basis:'b2k2000',ageYears:11700})).toContain('b2k2000');
  expect(planetCard(-3000000000,'planet')).toContain('Composición atmosférica');expect(planetCard(-3000000000,'planet')).toContain('Escenario audiovisual');
  expect(planetCard(-3000000000,'planet')).not.toContain('≈ 78');
 });
});
