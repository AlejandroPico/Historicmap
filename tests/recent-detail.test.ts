import {describe,it,expect} from 'vitest';
import {readFileSync} from 'node:fs';
import {historyAt,normalizedName,territorialEntityCode,type HistoryTopology} from '../src/history';
import {identityFor,type IdentityData} from '../src/identities';
import {eventsForCountry,eventsInYear} from '../src/historical-context';
import {politicalData} from '../src/political';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology:HistoryTopology=read('history.topojson'),profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const at=(year:number,name:string)=>historyAt(topology,year,names).features.find(f=>f.properties?.originalName===name)!;

describe('1990–2026 territorial and contextual continuity',()=>{
 it('keeps USSR, Czechoslovakia and Yugoslav entities separate from successor statistics',()=>{
  expect(at(1990,'Russia (Soviet Union)').properties).toMatchObject({entityCode:'SUN',identityKey:'USSR',code:''});
  expect(at(1991,'Russia (Soviet Union)').properties).toMatchObject({entityCode:'RUS',code:'RUS'});
  expect(at(1992,'Czechoslovakia').properties).toMatchObject({entityCode:'CSK',identityKey:'CSK',code:''});
  expect(at(1990,'Yugoslavia').properties?.identityKey).toBe('YUG');
  expect(at(2000,'Yugoslavia').properties).toMatchObject({entityCode:'SCG',identityKey:'FRY',code:'',name:'República Federal de Yugoslavia'});
  expect(at(2005,'Yugoslavia').properties?.identityKey).toBe('SCG');
  expect(at(1990,'Yemen (Arab Republic of Yemen)').properties?.code).toBe('YEM');
  expect(at(1990,'Vietnam, Democratic Republic of').properties?.code).toBe('VNM');
 });
 it('keeps Crimea within the recognized Ukrainian base independently of occupation paint',()=>{
  for(const year of [2014,2015,2019]){
   expect(at(year,'Ukraine').geometry).toEqual(at(2013,'Ukraine').geometry);
   expect(at(year,'Russia (Soviet Union)').geometry).toEqual(at(2013,'Russia (Soviet Union)').geometry);
  }
  const control=read('recent-control.geojson').features[0];
  expect(control.properties).toMatchObject({controller:'IRQ',code:'KWT',start:1990,end:1990});
  expect(control.geometry).toEqual(at(1990,'Kuwait').geometry);
 });
 it('dates independence, reunification and dissolution boundaries at annual close',()=>{
  expect(historyAt(topology,1990,names).features.some(f=>f.properties?.entityCode==='DDR')).toBe(false);
  expect(at(1990,'German Federal Republic').properties?.name).toBe('Alemania');
  expect(historyAt(topology,1992,names).features.some(f=>f.properties?.code==='ERI')).toBe(false);
  expect(at(1993,'Eritrea').properties?.code).toBe('ERI');
  expect(historyAt(topology,2010,names).features.some(f=>f.properties?.code==='SSD')).toBe(false);
  expect(territorialEntityCode(at(2011,'South Sudan').properties!,2011)).toBe('SSD');
  const supplements=read('historical-supplements.geojson');
  for(const code of ['AND','SMR','MCO','LIE','VAT','SAH','FSM','KIR'])expect(supplements.features.some((f:any)=>f.properties.code===code)).toBe(true);
  expect(supplements.features.find((f:any)=>f.properties.code==='PLW').properties.start).toBe('1994-10-01');
  const historical=politicalData(historyAt(topology,2019,names),2019).features.find(f=>f.properties?.entityCode==='SSD')!;
  const contemporary=politicalData(read('countries.geojson'),2026).features.find(f=>f.properties?.code==='SDS')!;
  expect(historical.properties?.politicalColor).toBe(contemporary.properties?.politicalColor);
 });
 it('selects country conflict phases by year without bringing later events backwards',()=>{
  const ukraine2014=eventsForCountry({code:'UKR'},2014,'conflict');
  expect(ukraine2014.some(e=>/2014/.test(e.id))).toBe(true);
  expect(ukraine2014.some(e=>e.id==='ukraine-full-scale-invasion')).toBe(false);
  expect(eventsForCountry({code:'UKR'},2022,'conflict').some(e=>e.id==='ukraine-full-scale-invasion')).toBe(true);
  expect(eventsForCountry({code:'SAH'},1990,'conflict').some(e=>e.id==='western-sahara-pre-ceasefire')).toBe(true);
  expect(eventsInYear(2027)).toEqual([]);
 });
 it('retains consecutive reappointments on the same handover day while merging duplicate sources',()=>{
  const data:IdentityData={retrieved:'2026-10-22',license:'test',source:'test',countries:{TST:{qid:'Q1',name:'Test',flags:[],leaders:[
   {person:'Q2',name:'A',role:'Primer ministro',start:'1990-01-01',end:'1990-06-01',source:'https://example.org'},
   {person:'Q2',name:'A',role:'Jefatura del Gobierno',start:'1990-01-01',end:'1990-06-01',source:'https://example.org'},
   {person:'Q2',name:'A',role:'Primer ministro',start:'1990-06-01',end:'1991-01-01',source:'https://example.org'},
  ]}}};
  const selected=identityFor({code:'TST'},1990,data,new Date(2026,9,22));
  expect(selected.leaders).toHaveLength(2);
  expect(selected.leaders.map(l=>l.start)).toContain('1990-06-01');
 });
 it('prefers documented daily precision and keeps party and national offices distinct',()=>{
  const data:IdentityData=read('identities.json');
  const salinas=identityFor({code:'MEX'},1990,data,new Date(2026,9,22)).leaders.find(l=>l.name.includes('Salinas'))!;
  expect(salinas.start).toBe('1988-12-01');expect(salinas.end).toBe('1994-11-30');
  const china=identityFor({code:'CHN'},2000,data,new Date(2026,9,22)).leaders;
  expect(china.some(l=>/Jiang/.test(l.name)&&/partido|secretario/i.test(l.role))).toBe(true);
  expect(china.some(l=>/Jiang/.test(l.name)&&/Estado|Presidente/.test(l.role))).toBe(true);
  expect(identityFor({code:'LBY'},1995,data,new Date(2026,9,22)).leaders[0].person).toBe('Q19878');
 });
});
