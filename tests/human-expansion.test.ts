import{it,expect}from'vitest';
import{readFileSync}from'node:fs';
import{createHash}from'node:crypto';
import{yearFromAge}from'../src/dates';
import{encyclopediaArticle,encyclopediaForYear,encyclopediaSources,searchEncyclopedia}from'../src/encyclopedia-model';
import{humanKnowledge,reviewedSiteContext,humanPhoto}from'../src/human-knowledge';
import{humanComparison,humanDiagram}from'../src/human-encyclopedia';
import{lineageCatalogue,distributionsAt}from'../src/human-distributions';
import{humanEvidenceAt,humanEvidenceMarkup}from'../src/prehistory';
import{iceCoreCO2,iceCoreAtAge,prehistoricCO2}from'../src/ice-core-co2';
import{planetRecordFor,planetValue}from'../src/planet';
import{displayIceSampleFor,displayIceCaption,olderIceModel}from'../src/ice-synthesis';
import{iceEnabledFor}from'../src/ice-automatic';
const ranges:{features:any[]}=JSON.parse(readFileSync('public/data/human-ranges.geojson','utf8')),sites:{features:any[]}=JSON.parse(readFileSync('public/data/hominin-sites.geojson','utf8'));
const at=(ka:number)=>yearFromAge(ka*1000),raw=ranges as any;
it('resolves every supplied name while keeping alternative classifications distinct from independent areas',()=>{
 const review=humanKnowledge.inputReview;expect(review.entries).toHaveLength(38);expect(review.catalogueCount).toBe(39);expect(review.speciesCensus).toBe(false);expect(new Set(lineageCatalogue.taxa.map(t=>t.key)).size).toBe(39);
 for(const e of review.entries){expect(encyclopediaArticle(e.article),e.inputLabel).toBeDefined();expect(lineageCatalogue.taxa.find(t=>t.key===e.canonicalKey)).toBeDefined();}
 for(const k of['gautengensis','nesher-ramla','ledi-australopithecus','ledi-homo','longi','juluensis'])expect(lineageCatalogue.taxa.find(t=>t.key===k)!.regions).toEqual([]);
 expect(searchEncyclopedia('Pithecanthropus').some(a=>a.id==='hominin-erectus')).toBe(true);expect(searchEncyclopedia('idaltu').some(a=>a.id==='hominin-sapiens')).toBe(true);
});
it('adds dated local evidence without replacing the original 982 rows or labelling every population as a species',()=>{
 const original=JSON.parse(readFileSync('Tierra/Humanidad/fossiles/timmermann2022-anteriores.json','utf8')).records;
 expect(sites.features.filter(f=>(f.properties as any).originalRow)).toEqual(original);expect(sites.features).toHaveLength(1007);
 const pink=sites.features.find(f=>f.id==='HOMININ-P5-PINK')!;expect(pink.properties.taxon).toBe('Homo aff. erectus');expect(pink.properties.ageMinBP).toBe(1100000);
 const early=humanEvidenceAt(sites as any,at(2600)).features.find(f=>f.properties!.identityKey==='HOMININ-P5-LEDI-H2')!;
 expect(early).toBeDefined();expect(early.properties!.taxonGroups).toContain('early-homo');
 expect(reviewedSiteContext(['Sima del los Huesos'])[0].note).toContain('ADN nuclear');expect(reviewedSiteContext(['Nesher Ramla'])[0].note).toContain('140–120');
});
it('retains old areas and adds only the sourced Ranis and Harbin regional windows',()=>{
 for(const [phase,age]of[['sapiens-ranis',46],['denisovan-harbin',180]]as const){const r=ranges.features.find(f=>f.properties.phase===phase)!;expect(r.properties.start).toBeLessThanOrEqual(at(age));expect(r.properties.end).toBeGreaterThanOrEqual(at(age));expect(r.properties.spatialUncertaintyKm).toBe(200);expect(distributionsAt(raw,at(age)).areas.features.some(f=>f.properties!.lineage===r.properties.lineage)).toBe(true);}
 expect(ranges.features.filter(f=>f.properties.phase==='sapiens-ranis')).toHaveLength(1);
});
it('opens substantial human contexts, supports every article and clearly separates video observations from adopted dates',()=>{
 for(const [year,id]of[[-6500000,'hominin-origins'],[-3200000,'australopithecines'],[-1800000,'early-homo-world'],[-250000,'human-diversity'],[-45000,'human-dispersals'],[-10000,'neolithic-transition']]as const)expect(encyclopediaForYear(year)).toBe(id);
 expect(humanKnowledge.articles).toHaveLength(49);
 for(const a of humanKnowledge.articles){expect(a.sections.length).toBeGreaterThanOrEqual(3);for(const id of a.sourceIds)expect(encyclopediaSources).toHaveProperty(id);for(const id of a.related)expect(encyclopediaArticle(id),a.id+':'+id).toBeDefined();expect(humanDiagram(a)).toContain('<svg');}
 const ids=humanKnowledge.videoReview.events.map(e=>e.videoId);expect(new Set(ids).size).toBe(5);expect(encyclopediaArticle('video-event-184')?.summary).toContain('2,8');expect(encyclopediaArticle('video-event-186')?.summary).toContain('315');
 expect(humanComparison('longi','denisovan')).toContain('Sin mancha independiente');expect(humanComparison('sapiens','neanderthal')).toContain('no demuestra encuentro');
});
it('ships real credited images whole and exposes encyclopedia links inside archaeological and distribution cards',()=>{
 expect(humanKnowledge.images).toHaveLength(18);
 for(const m of humanKnowledge.images){const b=readFileSync('public/'+m.file);expect(b.length).toBe(m.bytes);expect(createHash('sha256').update(b).digest('hex')).toBe(m.sha256);expect(m.licenseUrl).toMatch(/^https:/);expect(m.canonicalFile).toMatch(/^Tierra\/Humanidad\//);}
 expect(humanPhoto('hominin-afarensis')).toContain('Réplica');expect(humanPhoto('hominin-denisovan')).toContain('cueva');
 const lucy=humanEvidenceAt(sites as any,-3200000).features.find(f=>f.properties!.identityKey==='HOMININ-REF-afarensis')!;expect(humanEvidenceMarkup(lucy.properties!)).toContain('data-encyclopedia-entry="hominin-afarensis"');expect(humanEvidenceMarkup(lucy.properties!)).toContain('Imagen de referencia del linaje');
});
it('keeps the CO2 original intact and its gas ages, errors and observational limits explicit',()=>{
 const raw=readFileSync(iceCoreCO2.originalFile);expect(createHash('sha256').update(raw).digest('hex')).toBe(iceCoreCO2.originalSha256);expect(iceCoreCO2.rows).toHaveLength(1901);
 const r=iceCoreAtAge(160000)!;expect(iceCoreCO2.rows).toContain(r);expect(iceCoreAtAge(900000)).toBeUndefined();expect(iceCoreAtAge(-100)).toBeUndefined();
 const p=planetRecordFor('carbonDioxide',at(160))!;expect(p.sourceId).toBe('ice-core-co2');expect(p.value).toBe(r.co2ppm/10000);expect(p.reference).toEqual({basis:'BP1950',ageYears:r.ageBP});expect(p.uncertainty!.plus).toBe(r.sigmaPpm/10000);expect(p.interpolation).toBe('none');expect(planetValue(p)).toContain('ppm');expect(Number.isInteger(p.availableFromYear)).toBe(true);
 expect(planetRecordFor('meanTemperature',at(160))).toBeUndefined();expect(prehistoricCO2(-10000)).toBeUndefined();expect(prehistoricCO2(2026)).toBeUndefined();expect(prehistoricCO2(at(900))).toBeUndefined();expect(planetRecordFor('carbonDioxide',2026)?.sourceId).not.toBe('ice-core-co2');
});
it('selects only published ice windows, retains PaleoMIST precedence and never fills unknown gaps',()=>{
 expect(olderIceModel.samples).toHaveLength(12);expect(displayIceSampleFor(at(80))?.kind).toBe('margin');expect(displayIceSampleFor(at(81))?.label).toBe('MIS 5a');
 expect(iceEnabledFor(at(89),'auto')).toBe(true);expect(iceEnabledFor(at(100),'auto')).toBe(false);expect(iceEnabledFor(at(100),'on')).toBe(true);expect(iceEnabledFor(at(160),'auto')).toBe(true);
 for(const age of[120,200,300,390,550,720,1000,3700]){expect(displayIceSampleFor(at(age))).toBeUndefined();expect(iceEnabledFor(at(age),'on')).toBe(false);}
 for(const age of[1800,3000]){expect(displayIceSampleFor(at(age))?.uncertaintyFiles).toHaveLength(2);expect(iceEnabledFor(at(age),'auto')).toBe(false);expect(iceEnabledFor(at(age),'on')).toBe(true);}
 expect(displayIceCaption(at(160))).toContain('no frente de este año');expect(displayIceCaption(at(160))).toContain('Sólo hemisferio norte');
});
