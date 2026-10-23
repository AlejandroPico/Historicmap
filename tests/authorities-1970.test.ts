import {readFileSync,existsSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {identityFor,type IdentityData} from '../src/identities';
const data:IdentityData=JSON.parse(readFileSync(new URL('../public/data/identities.json',import.meta.url),'utf8'));
const at=(key:string,year:number)=>identityFor({identityKey:key},year,data,new Date(2026,9,23));
describe('historical authorities beyond modern office definitions',()=>{
 it('shows dictators, party leaders and formal officeholders in their actual periods',()=>{
  expect(at('YUG',1970).leaders.some(l=>l.person==='Q9161')).toBe(true);
  expect(at('CHL',1975).leaders.some(l=>l.person==='Q368'&&/dictadura/.test(l.role))).toBe(true);
  expect(at('BGR',1980).leaders.some(l=>l.person==='Q28517'&&/Partido/.test(l.role))).toBe(true);
  expect(at('BGR',1980).leaders.some(l=>l.person==='Q508037')).toBe(true);
  expect(at('AFG',1984).leaders.some(l=>l.person==='Q63827'&&/Estado/.test(l.role))).toBe(true);
  expect(at('IRN',1970).leaders.some(l=>l.person==='Q128245')).toBe(true);
  expect(at('NPL',1987).leaders.some(l=>l.person==='Q162306')).toBe(true);
  expect(at('NPL',1970).leaders.some(l=>l.person==='Q313110')).toBe(true);
  expect(at('LAO',1970).leaders.some(l=>l.person==='Q379797')).toBe(true);
  for(const key of ['HUN','ALB','POL','CSK','VDR']){
   expect(at(key,1970).leaders.some(l=>/partido/i.test(l.role)),key).toBe(true);
  }
  expect(at('CHN',1980).leaders.some(l=>/partido/i.test(l.role))).toBe(true);
  expect(at('KHM',1989).leaders.find(l=>l.person==='Q379197'&&l.endIsCoverageBoundary)?.end).toBe('1989-12-31');
 });
 it('keeps northern, Saigon and revolutionary southern Vietnamese authorities distinct',()=>{
  expect(at('VDR',1970).leaders.some(l=>l.person==='Q724317')).toBe(true);
  expect(at('RVN',1970).leaders.some(l=>l.person==='Q313707')).toBe(true);
  expect(at('RVN',1975).leaders.filter(l=>/jefatura del Estado/.test(l.role)).map(l=>l.person)).toEqual(expect.arrayContaining(['Q313707','Q1936777','Q334419']));
  expect(at('VSR',1975).leaders.some(l=>l.person==='Q337811')).toBe(true);
  expect(at('RVN',1974).leaders.some(l=>l.person==='Q337811')).toBe(false);
  expect(at('VNM',1970).leaders).toEqual([]);
  expect(at('VDR',1977).leaders).toEqual([]);
  expect(at('RVN',1975).flag).toBeUndefined();expect(at('VDR',1976).flag).toBeUndefined();
 });
 it('documents collective transitional authorities without inventing an individual portrait',()=>{
  const junta=at('NIC',1980).leaders.find(l=>l.person==='NIC-JGRN-1979');
  expect(junta?.role).toContain('colegiado');expect(junta?.portrait).toBeUndefined();
  expect(at('RHO',1979).leaders.some(l=>l.person==='Q336050')).toBe(true);
  expect(at('RHO',1970).leaders.some(l=>l.person==='Q313424')).toBe(true);
  expect(at('RHO',1970).leaders.some(l=>l.person==='Q57247212')).toBe(false);
 });
 it('keeps licensed local portraits and flags for the focal historical identities',()=>{
  for(const [key,year,person] of [['YUG',1970,'Q9161'],['CHL',1975,'Q368'],['AFG',1984,'Q63827'],['IRN',1970,'Q128245'],['RVN',1974,'Q313707'],['VDR',1970,'Q724317'],['RHO',1970,'Q313424']] as const){
   const portrait=at(key,year).leaders.find(l=>l.person===person)?.portrait;
   expect(portrait,`${key} ${year}`).toBeDefined();expect(portrait!.license).toBeTruthy();expect(existsSync(new URL('../public/'+portrait!.file,import.meta.url))).toBe(true);
  }
  for(const key of ['VDR','RVN','VSR','RHO'])expect(at(key,1970).flag?.file,key).toMatch(/\.svg$/);
 });
 it('does not move current reference forward just because historical data were acquired later',()=>{
  expect(data.retrieved).toBe('2026-10-22');
  expect(at('ESP',2026).flag).toBeDefined();expect(at('USA',2026).flag).toBeDefined();
  expect(at('ESP',2027).flag).toBeUndefined();expect(at('USA',2027).leaders).toEqual([]);
 });
});
