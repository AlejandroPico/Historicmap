import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,normalizedName,territorialEntityCode} from '../src/history';
import {politicalData} from '../src/political';
import {identityFor} from '../src/identities';
import {affiliationFor,organizationActive} from '../src/historical-affiliations';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology=read('history.topojson'),identities=read('identities.json'),profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const world=(y:number)=>politicalData(historyAt(topology,y,names),y);
const properties=(y:number,name:string)=>world(y).features.find(f=>f.properties?.originalName===name)!.properties!;
const at=(p:Record<string,any>,year:number)=>identityFor(p,year,identities,new Date(2026,9,23));
describe('1960s territorial and institutional distinctions',()=>{
 it('groups the United Arab Republic in 1960 and restores Syria at the 1961 close',()=>{
  const union=world(1960).features.find(f=>f.properties?.identityKey==='UAR')!;
  expect(union.geometry.type).toBe('MultiPolygon');expect(world(1960).features.some(f=>f.properties?.originalName==='Syria')).toBe(false);
  expect(at(union.properties!,1960).leaders.length).toBeGreaterThan(0);
  expect(properties(1961,'Syria').identityKey).not.toBe('UAR');
 });
 it('separates Yemen monarchy, Tanganyika and Zanzibar from successor statistics and leaders',()=>{
  const yemen=properties(1960,'Yemen (Arab Republic of Yemen)');expect(yemen.identityKey).toBe('YMK');expect(yemen.code).toBe('');expect(at(yemen,1960).leaders.some(l=>l.person==='Q400961')).toBe(true);
  expect(territorialEntityCode(properties(1963,'Tanzania (Tanganyika)'),1963)).toBe('TAN');
  expect(at(properties(1963,'Zanzibar'),1963).leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q2029666','Q6932724']));
  expect(at(properties(1963,'Tanzania (Tanganyika)'),1963).leaders.some(l=>l.person==='Q186525')).toBe(true);
  // The same historical person may hold office in more than one country.
  for(const key of ['FRA','AND'])expect(at({identityKey:key,code:key},1968).leaders.find(l=>l.person==='Q2042')?.portrait?.file).toBe('media/portrait-16d5ec0582fc0fdcd254.jpg');
 });
 it('keeps both UN administrators and the transfer to Indonesian administration within the next year',()=>{
  const a=at(properties(1962,'West Irian (Dutch New Guinea)'),1962);
  expect(a.leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q19593788','Q5955377']));
  expect(a.leaders.find(l=>l.person==='Q5955377')?.start).toBe('1962-11-15');
  const b=at(properties(1963,'West Irian (Dutch New Guinea)'),1963);
  expect(b.leaders.some(l=>l.person==='Q5955377'&&l.end==='1963-04-30')).toBe(true);
  expect(b.leaders.some(l=>/Sukarno|Soekarno/.test(l.name)&&l.start==='1963-05-01')).toBe(true);
  expect(b.flag).toBeDefined();
 });
 it('dates historical accessions without projecting later organizations into 1960',()=>{
  expect(organizationActive('asean',1966)).toBe(false);expect(organizationActive('asean',1967)).toBe(true);
  expect(affiliationFor('ALB','warsaw',1960)?.category).toBe('member');expect(affiliationFor('ALB','warsaw',1969)?.category).toBe('other');
  expect(affiliationFor('MNG','comecon',1961)?.category).toBe('other');expect(affiliationFor('MNG','comecon',1962)?.category).toBe('member');
 });
});
