import {readFileSync,writeFileSync} from 'node:fs';
import {beforeAll,afterAll,it,expect,vi} from 'vitest';
import {annualData} from '../src/data';
import {politicalData} from '../src/political';
import {identityFor,identityMarkup,identityNotesMarkup} from '../src/identities';
import {governmentFor,withGovernance,governmentCounts,governmentTags} from '../src/governance';
import {datedPlaces} from '../src/historical-places';
import {conflictPointsFor} from '../src/conflict-points';
import {canonicalFeature} from '../src/selection';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const ids=read('identities.json'),profiles=read('profiles.json');
beforeAll(()=>vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync(new URL('../public/data/'+String(input).split('/').at(-1),import.meta.url)),{status:200})));
afterAll(()=>vi.unstubAllGlobals());
const world=async(y:number)=>politicalData(await annualData(y),y,profiles);
const own=(k:string,y:number)=>identityFor({identityKey:k},y,ids);
it('repairs historical source identifiers and preserves dated constitutional transitions',async()=>{
 const w=await world(1800),h=w.features.find(f=>f.properties?.identityKey==='HABSBURG-MONARCHY')!;
 expect(h).toBeDefined();expect(identityFor(h.properties!,1800,ids).leaders.some(l=>l.person==='Q130834')).toBe(true);expect(identityFor(h.properties!,1800,ids).flag).toBeDefined();
 const swiss=w.features.find(f=>f.properties?.identityKey==='HIST-Q206696')!;expect(identityFor(swiss.properties!,1800,ids).flag?.title).toContain('Helvetic');expect(identityFor(swiss.properties!,1800,ids).leaders.some(l=>l.person==='HELVETIC-EXECUTIVE-1800')).toBe(true);
 expect((await world(1805)).features.some(f=>f.properties?.originalName==='Helvetic Republic'&&f.properties.identityKey==='CHE')).toBe(true);
 const rio=(await world(1824)).features.find(f=>f.properties?.identityKey==='RIO-DE-LA-PLATA')!;expect(rio).toBeDefined();const i=identityFor(rio.properties!,1824,ids);expect(i.flag).toBeDefined();expect(i.leaders.some(l=>l.person==='Q1710498'&&l.role.includes('provincial'))).toBe(true);expect(i.leaders.some(l=>/Presidente/.test(l.role))).toBe(false);
 const colonies=w.features.find(f=>f.properties?.identityKey==='BRITISH-COLONIES')!;expect(colonies).toBeDefined();expect(identityFor(colonies.properties!,1800,ids).leaders.some(l=>l.person==='Q127318'&&l.authorityScope==='external')).toBe(true);expect(identityFor(colonies.properties!,1800,ids).flagContext).toContain('administrador');
 expect(w.features.some(f=>f.properties?.identityKey==='GBR'&&f.properties.status!=='colony')).toBe(true);
});
it('uses sovereign titles and reviewed dates rather than biographies, regencies or homonyms',()=>{
 expect(own('HIST-Q14551680',1824).leaders.some(l=>l.person==='Q213882'&&l.role==='Príncipe de Lippe')).toBe(true);
 expect(own('HIST-Q836680',1850).leaders.some(l=>l.person==='Q57302'&&l.role==='Duque de Nassau')).toBe(true);
 expect(own('HIST-Q20135',1835).leaders.some(l=>l.person==='Q166701')).toBe(true);expect(own('HIST-Q20135',1835).leaders.some(l=>l.person==='Q141272506')).toBe(false);
 expect(own('HIST-Q186320',1857).leaders.find(l=>l.person==='Q57483')?.start).toBe('1856-09-05');
 expect(own('CHL',1824).leaders.some(l=>l.person==='Q1332')).toBe(true);expect(own('PRY',1824).leaders.some(l=>l.person==='Q34063')).toBe(true);
 expect(own('HIST-Q600524',1824).leaders.some(l=>l.person==='Q608989')).toBe(true);expect(own('HIST-Q600524',1875).leaders.some(l=>l.person==='SOKOTO-ABUBAKAR-II')).toBe(true);
 expect(own('HIST-Q600524',1900).leaders.find(l=>l.person==='Q21039523')?.endIsCoverageBoundary).toBe(true);expect(own('HIST-Q14551680',1800).leaders.find(l=>l.person==='Q67043')?.startIsCoverageBoundary).toBe(true);
 expect(own('HIST-Q1132786',1810).leaders.some(l=>l.person==='Q16157327')).toBe(true);expect(own('HIST-Q1139762',1824).leaders.some(l=>l.person==='Q341882')).toBe(true);
});
it('dates symbols and exposes their type and evidence without fabricating absent flags',()=>{
 for(const [key,y] of [['HIST-Q12548',1800],['PAPAL-STATES',1800],['OTT',1800],['NAPLES-BOURBON',1800],['HIST-Q199821',1824],['PER',1824],['HIST-Q20135',1824],['HIST-Q836680',1850]] as const)expect(own(key,y).flag,key).toBeDefined();
 expect(own('HIST-Q12548',1800).flag?.symbolLabel).toBe('Estandarte imperial');expect(identityMarkup({identityKey:'HIST-Q12548'},1800,ids,'/','header')).toContain('Estandarte imperial');expect(identityNotesMarkup({identityKey:'HIST-Q12548'},1800,ids)).toContain('Documentación del símbolo');
 expect(own('PER',1824).flag?.title).toContain('1822');expect(own('HIST-Q1139762',1824).flag).toBeUndefined();expect(own('HIST-Q1132786',1824).flag).toBeUndefined();
});
it('separates institutional form, dependency and dated political assessment',()=>{
 expect(governmentFor({identityKey:'FRA'},1800).tags).toContain('consulate');expect(governmentFor({identityKey:'FRA'},1812).tags).toContain('monarchy');expect(governmentFor({identityKey:'FRA'},1824).tags).toContain('constitutional-monarchy');
 expect(governmentFor({identityKey:'HIST-Q14551680'},1824).tags).toContain('monarchy');expect(governmentFor({identityKey:'USSR'},1970).tags).toContain('communist-dictatorship');
 expect(governmentFor({identityKey:'USA'},2025).regimeYear).toBe(2025);expect(governmentFor({identityKey:'USA'},2026).regimeTag).toBeUndefined();
 expect(governmentFor({identityKey:'USA',administratorKey:'GBR',status:'colony'},1824).regimeTag).toBeUndefined();expect(governmentFor({identityKey:'no-source'},1800).tags).toContain('unclassified');
 expect(governmentFor({identityKey:'SAH'},2026).key).toBe('SAH');expect(governmentFor({code:'SSD'},2026).key).toBe('SDS');expect(governmentFor({code:'PSE'},2026).key).toBe('PSX');
 expect(new Set(governmentTags.map(t=>t.id)).size).toBe(governmentTags.length);
 for(const tag of governmentTags)for(const parent of tag.parents)expect(governmentTags.some(t=>t.id===parent)).toBe(true);
});
it('provides dated urban references and battle points without pretending they are occupation polygons',async()=>{
 const w=await world(1824),p=datedPlaces(w,1824);expect(p.features.length).toBeGreaterThan(20);expect(p.features.some(f=>f.properties?.name==='Viena')).toBe(true);expect(p.features.some(f=>f.properties?.name==='Brasilia')).toBe(false);
 expect(datedPlaces(await world(1800),1800).features.some(f=>f.properties?.name==='Tokio')).toBe(false);
 const c=conflictPointsFor(1812);expect(c.features.some(f=>f.properties?.name.includes('Borodin'))).toBe(true);expect(c.features.every(f=>f.geometry.type==='Point')).toBe(true);expect(conflictPointsFor(1811).features.some(f=>f.properties?.name.includes('Borodin'))).toBe(false);
 const point=c.features.find(f=>f.properties?.name.includes('Borodin'))!;expect(canonicalFeature({id:0,properties:point.properties},c)).toBe(point);
 const annotated=withGovernance(w,1824);expect(annotated.features[0].geometry).toEqual(w.features[0].geometry);expect(governmentCounts(annotated).get('monarchy')).toBeGreaterThan(5);
});
it('records remaining annual gaps over the real production identity path',async()=>{
 const years:any[]=[],missingAuthorities:any[]=[],missingSymbols:any[]=[],missingPortraits=new Map<string,any>();
 for(let y=1800;y<=1900;y++){
  const w=await world(y);let flagged=0,led=0;
  for(const f of w.features){const p=f.properties!,i=identityFor(p,y,ids);if(i.flag)flagged++;else missingSymbols.push({year:y,key:i.key,name:p.name});if(i.leaders.length)led++;else missingAuthorities.push({year:y,key:i.key,name:p.name});for(const l of i.leaders)if(!l.portrait)missingPortraits.set(l.person,{person:l.person,name:l.name,key:i.key});}
  years.push({year:y,territories:w.features.length,withSymbol:flagged,withAuthority:led});
 }
 if(process.env.ATLAS_WRITE_AUDIT)writeFileSync('docs/REVIEW-1800-1900.json',JSON.stringify({release:'0.18.0',reviewed:'2026-10-26',scope:'Availability, not exhaustive historiographic validation; aggregates and duplicated components retained as source inventory.',years,missingAuthorities,missingSymbols,missingPortraits:[...missingPortraits.values()]},null,2)+'\n');
 expect(years).toHaveLength(101);
},120000);
