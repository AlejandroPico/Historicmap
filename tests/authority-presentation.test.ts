import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {identityFor,identityMarkup,identityNotesMarkup,type IdentityData} from '../src/identities';
const data:IdentityData=JSON.parse(readFileSync(new URL('../public/data/identities.json',import.meta.url),'utf8'));

describe('uniform dated authority presentation',()=>{
 it('keeps Italy1912 documentary commentary in Context and dates together in Authorities',()=>{
  const p={identityKey:'ITA',name:'Italia'},identity=identityFor(p,1912,data);
  const king=identity.leaders.find(l=>l.person==='Q150642')??identity.leaders.find(l=>l.name.includes('Víctor Manuel'))!;
  expect(king).toBeDefined();expect(king.note).toBeTruthy();
  const card=identityMarkup(p,1912,data,'/','authorities'),notes=identityNotesMarkup(p,1912,data);
  expect(card).toContain('leader-term');expect(card).toContain('Fuente del mandato');expect(card).not.toContain(king.note!);
  expect(notes).toContain('Notas de las autoridades');expect(notes).toContain(king.note!);expect(notes).toContain(king.source);
  expect(notes).not.toContain('<details open');
 });
 it('retains explicit coverage and maximum-end qualifications with compact date ranges',()=>{
  const fixture:IdentityData={retrieved:'2026-10-22',license:'test',source:'test',countries:{T:{qid:'',name:'T',flags:[],leaders:[{person:'TEST',name:'Name',role:'Office',source:'https://example.org',start:'1900-01-01',end:'1904-12-31',startIsCoverageBoundary:true,endIsUpperBound:true,note:'Documentary explanation.'}]}}};
  const card=identityMarkup({identityKey:'T'},1901,fixture,'/','authorities');
  expect(card).toContain('1/1/1900 — 31/12/1904');expect(card).toContain('Inicio de cobertura');expect(card).toContain('Fin: límite máximo');expect(card).not.toContain('Documentary explanation.');
  expect(identityNotesMarkup({identityKey:'T'},1901,fixture)).toContain('Documentary explanation.');
 });
 it('keeps Swiss annual presidency separate from membership and supplies the previously missing originals',()=>{
  for(const year of [1900,1913,1919,1930,1950,1985]){
   const leaders=identityFor({identityKey:'CHE'},year,data).leaders;
   expect(leaders.length).toBeGreaterThan(2);expect(leaders[0].authorityClass).toBe('annual-presidency');
   const president=leaders[0];
   if(data.countries.CHE.leaders.some(l=>l.authorityClass==='council-member'&&l.person===president.person&&l.start<=`${year}-12-31`&&l.end>=`${year}-01-01`))expect(leaders.some(l=>l.authorityClass==='council-member'&&l.person===president.person)).toBe(true);
   for(const l of leaders.filter(l=>/^Q\d+$/.test(l.person)&&l.person!=='Q30917'))expect(l.portrait,l.name).toBeDefined();
  }
  for(const person of ['Q693588','Q664398','Q118239'])expect(data.countries.CHE.leaders.find(l=>l.person===person)?.portrait?.file).toMatch(/\.gif$/);
 });
});
