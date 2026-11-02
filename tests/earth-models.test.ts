import{it,expect}from'vitest';
import{readFileSync}from'node:fs';import{createHash}from'node:crypto';
import{phandaAt,phandaBins,videoScenarioAt}from'../src/earth-models';
import{planetRecordFor,planetRecords}from'../src/planet';
import{deepSceneAt,deepIceAt}from'../src/deep-earth';
import{yearFromAge}from'../src/dates';
import{encyclopediaArticle,encyclopediaForYear,encyclopediaIndex}from'../src/encyclopedia-model';
import{scientificDiagram}from'../src/encyclopedia-diagrams';
import compiled from'../Tierra/Fanerozoico/phanda.json'with{type:'json'};
import media from'../Tierra/Fanerozoico/medios.json'with{type:'json'};
import reference from'../Tierra/Fanerozoico/referencia-audiovisual.json'with{type:'json'};
import manifest from'../public/data/manifest.json'with{type:'json'};
const at=(age:number)=>yearFromAge(age*1e6);
it('retains published bins and percentiles without inventing annual observations or replacing their limits',()=>{
 expect(phandaBins).toHaveLength(85);const raw=readFileSync(new URL('../Tierra/Fanerozoico/originales/'+compiled.original,import.meta.url));expect(createHash('sha256').update(raw).digest('hex')).toBe(compiled.sha256);
 const p=phandaAt(at(100))!,r=planetRecordFor('meanTemperature',at(100))!,co=planetRecordFor('carbonDioxide',at(100))!;expect(r.value).toBe(p.temperature['50']);expect(r.uncertainty?.minus).toBeCloseTo(p.temperature['50']-p.temperature['16']);expect(co.value).toBeCloseTo(p.co2ppm['50']/10000);expect(r.sourceId).toBe('phanda');expect(r.interpolation).toBe('none');expect(phandaAt(at(500))).toBeUndefined();expect(phandaAt(2026)).toBeUndefined();
});
it('keeps author scenarios separate, initial silicate vapour distinct from nitrogen and rounded zero bounded',()=>{
 const original=readFileSync(new URL('../Tierra/Investigacion/parte-1/muestras-indicadores-video.csv',import.meta.url));expect(createHash('sha256').update(original).digest('hex')).toBe(reference.transcriptionSha256);
 const s=videoScenarioAt(-4540000000)!;expect(s.gases.rockVapor).toBe(100);expect(s.gases.nitrogen).toBeUndefined();expect(planetRecordFor('rockVapor',-4540000000)?.evidence).toBe('illustrative-scenario');expect(planetRecordFor('nitrogen',-4540000000)).toBeUndefined();expect(planetRecordFor('oxygen',at(3970))?.value).toEqual({min:0,max:.005});expect(planetRecordFor('oceanArea',at(3970))).toBeUndefined();
 expect(planetRecordFor('meanTemperature',at(100),planetRecords,'video')?.sourceId).toBe('video-scenario');expect(planetRecordFor('solarDay',at(2460))?.value).toBe(16.9);expect(planetRecordFor('oxygen',1990)).toBeUndefined();
 expect(planetRecordFor('oxygen',2026,planetRecords,'video')).toEqual(planetRecordFor('oxygen',2026));expect(planetRecordFor('temperatureAnomaly',2026,planetRecords,'video')).toEqual(planetRecordFor('temperatureAnomaly',2026));
});
it('registers each additional coastline under its actual age with original geometry and checksum',()=>{
 for(const age of[34,56,145,201,252,360,420,445]){const e=manifest.entries.find(e=>e.file===`coastlines-${age}.geojson`)!;expect(e.year).toBe(-age*1e6);const bytes=readFileSync(new URL('../public/data/'+e.file,import.meta.url));expect(createHash('sha256').update(bytes).digest('hex')).toBe(e.sha256);expect(JSON.parse(bytes.toString()).features.length).toBe(e.features);}
});
it('continues period surfaces through the Cambrian and stops before existing hominin references',()=>{
 for(const age of[538.8,500,450,400,350,300,250,200,150,100,50,10])expect(deepSceneAt(at(age))).toBeDefined();expect(deepSceneAt(at(7))).toBeUndefined();expect(deepIceAt(at(460))).toBeNull();expect(deepIceAt(at(444))).toBe('gondwana');expect(deepIceAt(at(34))).toBe('antarctic');expect(deepIceAt(at(40))).toBeNull();
});
it('opens substantial period articles and keeps the audiovisual archive out of the main index',()=>{
 expect(encyclopediaForYear(at(150))).toBe('jurassic');expect(encyclopediaArticle('geo-Darriwilian')?.themeId).toBe('ordovician');expect(encyclopediaIndex().some(a=>a.id.startsWith('video-event'))).toBe(false);expect(encyclopediaIndex(true).some(a=>a.id.startsWith('video-event'))).toBe(true);
 for(const id of['cambrian','jurassic','cretaceous','paleogene','fossils','extinctions','geologic-ranks']){const a=encyclopediaArticle(id)!;expect(a.sections.length).toBeGreaterThanOrEqual(3);expect(scientificDiagram(a)).toContain('<svg');}
});
it('keeps original thematic media credited and byte-identical',()=>{
 for(const m of media.images){const bytes=readFileSync(new URL('../public/'+m.file,import.meta.url));expect(bytes.length).toBe(m.bytes);expect(createHash('sha256').update(bytes).digest('hex')).toBe(m.sha256);expect(m.credit).not.toBe('');expect(m.caption).not.toBe('');}
});
