import {readFileSync,existsSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {identityFor} from '../src/identities';
const data=JSON.parse(readFileSync(new URL('../public/data/identities.json',import.meta.url),'utf8'));
const id=(key:string,year:number)=>identityFor({identityKey:key},year,data,new Date(2026,9,25));
describe('reported identities and licensed portraits',()=>{
 it('excludes fictional officeholders while retaining the real US president and photograph in2020',()=>{
  const usa=id('USA',2020);expect(usa.leaders.map(l=>l.person)).toEqual(['Q22686']);
  expect(usa.leaders[0].portrait).toBeDefined();
  for(const c of Object.values<any>(data.countries))expect(c.leaders.some((l:any)=>['Q107054330','Q131426522'].includes(l.person))).toBe(false);
 });
 it('uses reviewed real portraits instead of banknotes or unrelated generated images',()=>{
  for(const [key,year,person,title] of [['IRQ',2026,'Q139573306','2026 Ali al-Zaidi'],['TJK',2026,'Q15222839','29-04-2021'],['BTN',1970,'Q298020','portrait'],['FRA',1900,'Q169502','Loubet']] as const){
   const l=id(key,year).leaders.find(l=>l.person===person)!;expect(l,person).toBeDefined();expect(l.portrait?.title).toContain(title);
   expect(existsSync(new URL('../public/'+l.portrait!.file,import.meta.url))).toBe(true);
   expect(l.portrait!.title).not.toMatch(/Pope Trump|Ngultrum/);
  }
  const iraq=id('IRQ',2026).leaders;expect(iraq.find(l=>l.person==='Q139573306')?.start).toBe('2026-05-14');
  expect(iraq.find(l=>l.person==='Q115579547')?.start).toBe('2026-04-11');
 });
 it('fills India2011 and both2016 Vietnamese presidents with individually credited portraits',()=>{
  for(const [key,y,people] of [['IND',2011,['Q41914','Q47854']],['BGD',2016,['Q3246667']],['VNM',2016,['Q57407','Q7833292']],['NPL',2014,['Q57441','Q422969']]] as const){
   for(const person of people){const l=id(key,y).leaders.find(l=>l.person===person)!;expect(l?.portrait,person).toBeDefined();expect(l.portrait!.license).toBeTruthy();}
  }
  expect(id('VNM',2016).leaders.find(l=>l.person==='Q57407')?.end).toBe('2016-04-02');
  expect(data.countries.IND.leaders.filter((l:any)=>l.start>='1947-01-01'&&!l.portrait)).toEqual([]);
 });
});
