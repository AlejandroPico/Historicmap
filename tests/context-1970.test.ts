import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {eventsInYear,eventsForCountry,historicalEvents} from '../src/historical-context';
import {recordsFor,type CountryHistory} from '../src/country-history';

const read=(file:string)=>JSON.parse(readFileSync(new URL('../public/data/'+file,import.meta.url),'utf8'));
const context=read('historical-context.json');
const history:CountryHistory=read('country-history.json');
const ids=(year:number,code:string)=>eventsForCountry({code},year).map(e=>e.id);
const text=(year:number,code:string)=>eventsForCountry({code},year).map(e=>e.text).join(' ');
const dateIsValid=(s:string)=>/^\d{4}-\d{2}-\d{2}$/.test(s)&&new Date(s+'T00:00:00Z').toISOString().slice(0,10)===s;

describe('1970–1989 contextual phases and institutional chronology',()=>{
 it('preserves dated, sourced records and the acquisition horizon',()=>{
  expect(context.startYear).toBe(1950);
  expect(new Set(historicalEvents.map(e=>e.id)).size).toBe(historicalEvents.length);
  for(const e of historicalEvents){
   expect(dateIsValid(e.start),e.id).toBe(true);
   expect(e.start<=context.referenceDate,e.id).toBe(true);
   if(e.end){expect(dateIsValid(e.end),e.id).toBe(true);expect(e.end>e.start,e.id).toBe(true);}
   expect(e.countries.length,e.id).toBeGreaterThan(0);expect(new Set(e.countries).size,e.id).toBe(e.countries.length);
   expect(e.source,e.id).toMatch(/^https:\/\//);expect(e.sourceLabel.length,e.id).toBeGreaterThan(4);
  }
  expect(eventsInYear(1949)).toEqual([]);expect(eventsInYear(1969).length).toBeGreaterThan(0);expect(eventsInYear(2027)).toEqual([]);
  expect(recordsFor('USA','institutions',2027,history)).toEqual([]);
 });
 it('distinguishes the fall of Saigon in 1975 from formal unification in 1976',()=>{
  expect(ids(1974,'RVN')).toContain('vietnam-after-paris-1973');
  expect(ids(1974,'RVN')).not.toContain('vietnam-final-offensive-1975');
  expect(ids(1975,'VDR')).toContain('vietnam-final-offensive-1975');
  expect(ids(1975,'VDR')).not.toContain('vietnam-formal-union-1976');
  expect(ids(1976,'VNM')).toContain('vietnam-formal-union-1976');
  expect(recordsFor('VNM','history',1975,history).some(r=>r.id==='vnm-unification-1976')).toBe(false);
  expect(recordsFor('VNM','history',1976,history).some(r=>r.id==='vnm-unification-1976')).toBe(true);
  expect(recordsFor('VSR','history',1976,history).some(r=>r.id==='vnm-unification-1976')).toBe(true);
  expect(history.relations.find(r=>r.id==='vdr-vnm')?.date).toBe('1976-07-02');
  expect(history.relations.find(r=>r.id==='rvn-vsr')).toMatchObject({date:'1975-04-30',from:{key:'RVN'},to:{key:'VSR'}});
  expect(history.relations.find(r=>r.id==='vsr-vnm')).toMatchObject({date:'1976-07-02',from:{key:'VSR'},to:{key:'VNM'}});
 });
 it('does not move Bangladesh independence into 1970 or confuse it with UN admission',()=>{
  expect(ids(1970,'PAK')).not.toContain('bangladesh-liberation-1971');
  expect(ids(1971,'PAK')).toContain('bangladesh-liberation-1971');
  expect(ids(1971,'BGD')).toContain('bangladesh-liberation-1971');
  expect(history.relations.find(r=>r.id==='pak-bgd')).toMatchObject({date:'1971-12-16',to:{key:'BGD',year:1972}});
 });
 it('separates the October war, Camp David and the Egyptian-Israeli peace treaty',()=>{
  expect(ids(1972,'EGY')).not.toContain('october-war-1973');
  expect(ids(1973,'EGY')).toContain('october-war-1973');
  expect(ids(1973,'EGY')).not.toContain('camp-david-framework-1978');
  expect(ids(1973,'EGY')).not.toContain('egypt-israel-treaty-1979');
  expect(ids(1978,'EGY')).toContain('camp-david-framework-1978');
  expect(ids(1979,'EGY')).toContain('egypt-israel-treaty-1979');
  expect(ids(1980,'EGY')).not.toContain('october-war-1973');
 });
 it('keeps the Soviet intervention, withdrawal and continuing Afghan war in their phases',()=>{
  expect(ids(1978,'AFG')).not.toContain('afghanistan-soviet-war-1979');
  expect(ids(1979,'AFG')).toContain('afghanistan-soviet-war-1979');
  expect(ids(1979,'AFG')).not.toContain('afghanistan-withdrawal-1988');
  expect(ids(1988,'AFG')).toContain('afghanistan-withdrawal-1988');
  expect(ids(1988,'AFG')).not.toContain('afghanistan-after-soviet-1989');
  expect(ids(1989,'AFG')).toContain('afghanistan-after-soviet-1989');
  expect(ids(1989,'AFG')).not.toContain('afghanistan-soviet-war-1979');
 });
 it('keeps 1989 European transitions separate from later state dissolution',()=>{
  for(const [code,event] of [['DDR','berlin-wall-opening-1989'],['CSK','czechoslovakia-velvet-1989'],['POL','poland-round-table-1989']]){
   expect(ids(1988,code)).not.toContain(event);expect(ids(1989,code)).toContain(event);
  }
  expect(text(1989,'DDR')).toContain('Estados separados');
  expect(text(1989,'CSK')).not.toMatch(/separación de 1993|se ha disuelto/);
  expect(ids(1989,'DEU')).not.toContain('german-reunification-1990');
 });
 it('keeps Portuguese independence and constitutional milestones dated without anticipating them',()=>{
  for(const [key,day] of [['AGO','1975-11-11'],['MOZ','1975-06-25'],['STP','1975-07-12']]){
   const record=history.records.find(r=>r.id===`${key.toLowerCase()}-independence-1975`)!;
   expect(record.start).toBe(day);
   expect(recordsFor(key,'history',1974,history)).not.toContain(record);
   expect(recordsFor(key,'history',1975,history)).toContain(record);
  }
  expect(ids(1974,'AGO')).not.toContain('angola-alvor-breakdown-1975');
  expect(text(1974,'AGO')).not.toMatch(/reparto del poder fracasa|Alvor/);
  expect(ids(1974,'PRT')).not.toContain('portugal-constituent-1975');
  expect(recordsFor('PRT','institutions',1974,history).map(r=>r.text).join(' ')).not.toMatch(/elegida en 1975|elecciones de abril de 1975/);
  expect(recordsFor('GRC','institutions',1975,history).map(r=>r.text).join(' ')).not.toMatch(/revisión de 1986/);
  expect(recordsFor('GRC','history',1986,history).some(r=>r.id==='grc-revision-1986')).toBe(true);
 });
 it('does not move the Spanish withdrawal or the Nicaragua judgment into earlier phases',()=>{
  expect(ids(1975,'ESH')).not.toContain('sahara-war-1976-1979');
  expect(ids(1976,'ESH')).toContain('sahara-war-1976-1979');
  expect(text(1975,'ESH')).not.toContain('Tras los acuerdos de Madrid y la retirada española');
  expect(ids(1981,'NIC')).not.toContain('nicaragua-icj-judgment-1986');
  expect(text(1981,'NIC')).not.toContain('La CIJ examina');
  expect(ids(1986,'NIC')).toContain('nicaragua-icj-judgment-1986');
 });
});
