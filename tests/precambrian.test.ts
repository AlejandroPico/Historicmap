import{describe,it,expect}from'vitest';
import{readFileSync}from'node:fs';import{createHash}from'node:crypto';
import{deepAge,deepSceneAt,deepScenes,deepSources,deepIceAt,deepBackground,chronologyDisplayColor}from'../src/deep-earth';
import{curatedArticles,encyclopediaSources,encyclopediaArticle,encyclopediaForYear,encyclopediaIndex,searchEncyclopedia}from'../src/encyclopedia-model';
import{planetRecordFor,planetValue}from'../src/planet';
import{geologicalUnits}from'../src/earth-chronology';
import{yearFromAge}from'../src/dates';
import{chronologyBands,chronologyBandsMarkup}from'../src/chronology-bands';
import{yearToPosition}from'../src/time';
import review from '../Tierra/Precambrico/revision-video.json' with {type:'json'};
import inventory from '../Tierra/Investigacion/parte-1/inventario-video.json' with {type:'json'};
import media from '../Tierra/Precambrico/medios.json' with {type:'json'};
const at=(ma:number)=>yearFromAge(ma*1e6);
describe('Precambrian scenarios and contextual encyclopedia',()=>{
 it('covers every boundary without overlap, preserves the Cambrian handover and has sources',()=>{
  for(let i=0;i<deepScenes.length;i++){const s=deepScenes[i];if(i)expect(deepScenes[i-1].youngestMa).toBe(s.oldestMa);expect(deepSceneAt(at((s.oldestMa+s.youngestMa)/2))?.id).toBe(s.id);for(const id of s.sourceIds)expect(deepSources).toHaveProperty(id);expect(encyclopediaArticle(s.article)).toBeDefined();}
  for(let ma=539;ma<=4540;ma++)expect(deepSceneAt(at(ma))).toBeDefined();expect(deepSceneAt(at(538.8))?.id).toBe('cambrian');expect(deepSceneAt(2026)).toBeUndefined();expect(deepAge(at(2460))).toBe(2460);
 });
 it('separates glacial intervals and regional evidence instead of freezing the whole Cryogenian',()=>{
  expect(deepIceAt(at(700))).toBe('snowball');expect(deepIceAt(at(655))).toBeNull();expect(deepIceAt(at(640))).toBe('snowball');expect(deepIceAt(at(620))).toBeNull();expect(deepIceAt(at(2900))).toBe('pongola');expect(deepIceAt(at(580.5))).toBe('gaskiers');expect(deepIceAt(2026)).toBeNull();expect(deepBackground(at(700),false)).toBe(deepSceneAt(at(700))!.ocean);expect(deepBackground(at(700),true)).not.toBe(deepBackground(at(700),false));expect(deepBackground(2026)).toBeUndefined();
 });
 it('retains dated paleorotation references without interpolating into other eras',()=>{
  expect(planetValue(planetRecordFor('solarDay',at(2460)))).toContain('16,9 ± 0,2');expect(planetRecordFor('solarDay',at(2460))?.reference).toMatchObject({basis:'Ma',ageMa:2460});expect(planetValue(planetRecordFor('solarDay',at(620)))).toContain('21,9 ± 0,4');for(const y of[at(2500),at(2400),at(700),at(600)])expect(planetRecordFor('solarDay',y)?.evidence).toBe('illustrative-scenario');expect(planetRecordFor('solarDay',2026)).toBeUndefined();expect(planetRecordFor('oxygen',at(3000))?.evidence).toBe('illustrative-scenario');
 });
 it('uses a distinct editorial palette and readable full names while retaining source colours',()=>{
  const source=geologicalUnits.find(u=>u.id==='Hadean')!.color;expect(chronologyDisplayColor('Hadean',source)).not.toBe(source);expect(geologicalUnits.find(u=>u.id==='Hadean')!.color).toBe(source);
  const model=chronologyBands(at(3400),yearToPosition(at(3400)),230,1280),p=model.bands.find(b=>b.id==='Paleoarchean')!;expect(p.width).toBeGreaterThan(180);const html=chronologyBandsMarkup(model);expect(html).toContain('Paleoarcaico');expect(html).toContain('data-encyclopedia-entry="geo-Paleoarchean"');expect(new Set(['Hadean','Archean','Proterozoic'].map(id=>chronologyDisplayColor(id,'#ffffff'))).size).toBe(3);
 });
 it('opens by the consulted context and preserves detailed articles, links and all chronological references',()=>{
  expect(encyclopediaForYear(-4540000000)).toBe('formation');expect(encyclopediaForYear(at(700))).toBe('ice');expect(encyclopediaForYear(2026)).toBe('human-contemporary');expect(encyclopediaArticle('geo-Hadean')?.sections).toEqual(encyclopediaArticle('hadean')?.sections);
  for(const a of curatedArticles){expect(a.sections.length).toBeGreaterThanOrEqual(3);for(const id of a.related)expect(encyclopediaArticle(id),a.id+':'+id).toBeDefined();for(const id of a.sourceIds)expect(encyclopediaSources).toHaveProperty(id);}
  for(const entry of encyclopediaIndex())expect(encyclopediaArticle(entry.id),entry.id).toBeDefined();expect(searchEncyclopedia('nucleo').some(a=>a.id==='interior')).toBe(true);expect(searchEncyclopedia('Precámbrico').some(a=>a.id==='geo-Precambrian')).toBe(true);expect(encyclopediaArticle('video-event-035')?.related).toContain('matachewan');expect(encyclopediaArticle('kpg')?.summary).toContain('no cerró el Jurásico');
 });
 it('accounts for every observed Precambrian candidate without converting OCR dates to physical effects',()=>{
  expect(review.events.map(e=>e.videoId)).toEqual(inventory.events.filter(e=>e.implementationPart===3).map(e=>e.id));expect(new Set(review.events.map(e=>e.videoId)).size).toBe(review.events.length);for(const e of review.events){expect(encyclopediaArticle(e.article)).toBeDefined();expect(e.disposition).not.toBe('validated-exact-date');}expect(review.events.find(e=>e.videoId==='video-event-078')?.note).toContain('635');expect(review.events.find(e=>e.videoId==='video-event-081')?.disposition).toBe('not-adopted');
 });
 it('ships credited scientific illustrations byte-for-byte without moving country media',()=>{
  for(const m of media.images){const data=readFileSync(new URL('../public/'+m.file,import.meta.url));expect(data.length).toBe(m.bytes);expect(createHash('sha256').update(data).digest('hex')).toBe(m.sha256);expect(m.credit).toContain('NASA');expect(m.page).toMatch(/^https:/);}
 });
});
