import{it,expect}from'vitest';
import{encyclopediaArticle,encyclopediaReferenceYear,encyclopediaIndex,encyclopediaSources}from'../src/encyclopedia-model';
import{geologicalUnits,geologicalAt}from'../src/earth-chronology';
import{deepScenes,sceneYear,deepSceneAt}from'../src/deep-earth';
import{lineageCatalogue}from'../src/human-distributions';
import{humanKnowledge}from'../src/human-knowledge';
import{displayIceSampleFor,iceAvailabilityNote}from'../src/ice-synthesis';
import{iceEnabledFor}from'../src/ice-automatic';
import{yearFromAge}from'../src/dates';
import{readableRulerLabels}from'../src/ruler-labels';

it('keeps an applicable lineage or geological date while unrelated reading uses its documented reference',()=>{
 const lucy=encyclopediaArticle('hominin-afarensis')!;
 expect(encyclopediaReferenceYear(lucy,-3200000)).toBe(-3200000);
 expect(encyclopediaReferenceYear(lucy,-45000)).toBe(lucy.year);
 expect(encyclopediaReferenceYear(lucy,2026)).toBe(lucy.year);
 expect(encyclopediaReferenceYear(lucy,0)).toBe(lucy.year);
 for(const t of lineageCatalogue.taxa){const a=encyclopediaArticle('hominin-'+t.key)!;const y=yearFromAge((t.oldestKa+t.youngestKa)*500);if(Number.isInteger(y)&&y<=-10001)expect(encyclopediaReferenceYear(a,y),t.key).toBe(y);}
 for(const u of geologicalUnits){const a=encyclopediaArticle('geo-'+u.id)!;expect(encyclopediaReferenceYear(a,u.axisOldestYear),u.id).toBe(u.axisOldestYear);}
 const h=encyclopediaArticle('human-middle-ages')!;expect(encyclopediaReferenceYear(h,1100)).toBe(1100);
});
it('connects Quaternary epochs and ages to substantive sourced content without claiming full-period CO2 measurements',()=>{
 for(const id of['Quaternary','Pleistocene','Holocene','Gelasian','Chibanian','Meghalayan']){
  const a=encyclopediaArticle('geo-'+id)!;expect(a.themeId).toBe('quaternary');expect(a.sections.length).toBeGreaterThan(5);expect(a.sections.map(s=>s.text).join(' ')).toContain('800–12ka');
 }
 const q=encyclopediaArticle('quaternary')!;expect(encyclopediaReferenceYear(q,2026)).toBe(2026);expect(encyclopediaReferenceYear(q,-5000000)).toBe(q.year);
});
it('retains complete internal navigation and registered references, including every scene and geological unit',()=>{
 const entries=encyclopediaIndex(true);expect(new Set(entries.map(a=>a.id)).size).toBe(entries.length);
 for(const entry of entries){const a=encyclopediaArticle(entry.id)!;expect(a,entry.id).toBeDefined();for(const id of a.related)expect(encyclopediaArticle(id),a.id+':'+id).toBeDefined();for(const id of a.sourceIds)expect(encyclopediaSources,id).toHaveProperty(id);}
 for(const s of deepScenes){const y=sceneYear(s);expect(deepSceneAt(y)?.id,s.id).toBe(s.id);expect(encyclopediaArticle(s.article),s.id).toBeDefined();}
 expect(geologicalAt(-1).map(u=>u.id)).toEqual(geologicalAt(1).map(u=>u.id));
});
it('explains old warm hypotheses, switched-off recent references and actual gaps without equating missing data to no ice',()=>{
 const at=(ka:number)=>yearFromAge(ka*1000);
 expect(displayIceSampleFor(at(80))?.kind).toBe('margin');expect(displayIceSampleFor(at(81))?.kind).toBe('interval-hypothesis');
 expect(iceAvailabilityNote(at(20),false)).toContain('Referencia PaleoMIST disponible');
 expect(iceAvailabilityNote(at(100),false)).toContain('MIS 5c');expect(iceAvailabilityNote(at(100),false)).toContain('no activada');
 expect(iceAvailabilityNote(at(100),true)).toContain('no frente de este año');expect(iceAvailabilityNote(at(100),true)).not.toContain('no activada');
 for(const ka of[120,200,300,550,1000,3700]){expect(iceEnabledFor(at(ka),'on')).toBe(false);expect(iceAvailabilityNote(at(ka),false)).toContain('no significa ausencia de hielo');}
});
it('preserves every existing human image while filling six named photographic gaps',()=>{
 for(const key of['africanus','rudolfensis','sediba','heidelbergensis','antecessor','luzon']){
  const image=humanKnowledge.images.find(m=>m.articleIds.includes('hominin-'+key))!;expect(image,key).toBeDefined();expect(image.canonicalFile).toBe('Tierra/Humanidad/linajes/'+key+'/medios.json');expect(image.caption).not.toContain('retrato oficial');
 }
 expect(humanKnowledge.images.filter(m=>m.caption.includes('Réplica')).length).toBeGreaterThanOrEqual(6);
});
it('avoids overlapping year labels at segment seams without dropping the year1 priority',()=>{
 const labels=[{year:-100,x:10,width:90},{year:1,x:60,width:50},{year:100,x:110,width:70},{year:200,x:230,width:70}];
 const shown=readableRulerLabels(labels);expect(shown.has(1)).toBe(true);expect(shown.has(200)).toBe(true);
 const fitted=labels.filter(a=>shown.has(a.year));for(let i=0;i<fitted.length;i++)for(let j=i+1;j<fitted.length;j++)expect(Math.abs(fitted[i].x-fitted[j].x)).toBeGreaterThanOrEqual((fitted[i].width+fitted[j].width)/2+12);
 expect(readableRulerLabels([{year:100,x:0,width:70},{year:150,x:115,width:70},{year:200,x:230,width:70}]).size).toBe(3);
});
