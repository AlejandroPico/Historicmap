import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,normalizedName,withHistoricalSupplements} from '../src/history';
import {politicalData} from '../src/political';
import {identityFor} from '../src/identities';
import {affiliationFor,organizationActive} from '../src/historical-affiliations';
import {eventsForCountry} from '../src/historical-context';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology=read('history.topojson'),identities=read('identities.json'),profiles=read('profiles.json'),supplements=read('historical-supplements.geojson');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([c,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),c] as [string,string])));
const world=(y:number)=>politicalData(withHistoricalSupplements(historyAt(topology,y,names),y,supplements,historyAt(topology,1974,names)),y);
const country=(y:number,name:string)=>world(y).features.find(f=>f.properties?.originalName===name)!.properties!;
const identity=(key:string,y:number)=>identityFor({identityKey:key},y,identities);
describe('1950s historical distinctions',()=>{
 it('separates the State of Vietnam from the later republic without successor statistics',()=>{
  const p=country(1954,'Vietnam, Republic of');expect(p).toMatchObject({identityKey:'VSV',code:'',name:'Estado de Vietnam'});
  expect(identity('VSV',1954).leaders.map(l=>l.name)).toEqual(expect.arrayContaining(['Bảo Đại','Ngô Đình Diệm']));
  expect(identity('VSV',1954).leaders.find(l=>l.person==='Q192502')?.role).toContain('Primer ministro');
  expect(country(1955,'Vietnam, Republic of').identityKey).toBe('RVN');
 });
 it('distinguishes Malaya from the1963 federation and preserves dated sovereigns',()=>{
  expect(country(1959,'Malaysia')).toMatchObject({identityKey:'MAL',code:'',name:'Federación de Malaya'});
  expect(identity('MAL',1959).leaders.length).toBeGreaterThan(1);
  expect(identity('MAL',1959).flag?.title).toContain('Malaya');
  expect(country(1963,'Malaysia').entityCode).toBe('MYS');
  expect(identity('EGY',1952).leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q213001','Q311796']));
 });
 it('keeps formal and effective offices distinct in Korea, Taiwan and Uruguay',()=>{
  expect(identity('PRK',1950).leaders.find(l=>l.person==='Q41117')?.role).not.toContain('Estado');
  expect(identity('PRK',1950).leaders.some(l=>l.person==='Q334326')).toBe(true);
  expect(identity('TWN',1950).leaders.find(l=>l.person==='Q699698')?.role).toContain('Primer ministro');
  expect(identity('URY',1954).leaders.find(l=>l.person==='Q522975')?.role).toContain('colegiado');
 });
 it('dates independence, colonial administrations, Germanies and UAR at the annual close',()=>{
  expect(country(1950,'Angola')).toMatchObject({status:'colony',administratorKey:'PRT'});
  expect(identityFor(country(1950,'Angola'),1950,identities).leaders.some(l=>/Salazar/.test(l.name))).toBe(true);
  expect(country(1950,'German Democratic Republic').identityKey).toBe('DDR');
  expect(country(1950,'German Federal Republic').identityKey).toBe('DEU');
  expect(country(1950,'Ghana').status).toBe('colony');expect(country(1957,'Ghana').status).toBe('independent');
  expect(world(1958).features.some(f=>f.properties?.identityKey==='UAR')).toBe(true);
  expect(identity('GIN',1957).leaders.some(l=>l.person==='Q155402'&&/Estado/.test(l.role))).toBe(false);
 });
 it('distinguishes treaty dates, organizations and country-specific conflict context',()=>{
  expect(affiliationFor('TUR','nato',1951)?.category).toBe('other');expect(affiliationFor('TUR','nato',1952)?.category).toBe('member');
  expect(affiliationFor('DEU','nato',1954)?.category).toBe('other');expect(affiliationFor('DEU','nato',1955)?.category).toBe('member');
  expect(organizationActive('warsaw',1954)).toBe(false);expect(organizationActive('warsaw',1955)).toBe(true);
  expect(organizationActive('ecsc',1951)).toBe(false);expect(organizationActive('ecsc',1952)).toBe(true);
  expect(organizationActive('eu',1957)).toBe(false);expect(organizationActive('eu',1958)).toBe(true);
  expect(affiliationFor('CUB','oas',1959)?.category).toBe('member');expect(affiliationFor('CUB','oas',1962)?.category).toBe('suspended');
  expect(eventsForCountry({code:'EGY'},1956,'conflict').some(e=>/Suez/.test(e.title))).toBe(true);
  expect(eventsForCountry({code:'KOR'},1951,'conflict').some(e=>/Corea/.test(e.title))).toBe(true);
 });
});
