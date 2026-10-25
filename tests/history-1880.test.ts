import {readFileSync} from 'node:fs';
import {afterAll,beforeAll,describe,it,expect,vi} from 'vitest';
import {annualData,overlaysFor} from '../src/data';
import {politicalData,regimeColor} from '../src/political';
import {composeControl} from '../src/control-map';
import {identityFor} from '../src/identities';
import {membershipsAt,organizationActive} from '../src/historical-affiliations';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const identities=read('identities.json'),profiles=read('profiles.json');
beforeAll(()=>vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync(new URL('../public/data/'+String(input).split('/').at(-1),import.meta.url)),{status:200})));
afterAll(()=>vi.unstubAllGlobals());
const world=async(y:number)=>composeControl(politicalData(await annualData(y),y,profiles),await overlaysFor(y),y).territories;
const country=async(key:string,y:number)=>{const found=(await world(y)).features.find(f=>f.properties?.identityKey===key);if(!found)throw Error('Missing '+key+' in'+y);return found.properties!;};
const id=async(key:string,y:number)=>identityFor(await country(key,y),y,identities,new Date(2026,9,25));
describe('1880 extension through the production loader',()=>{
 it('resolves both source inventories without anachronistic successor governments',async()=>{
  for(const y of [1880,1885,1886,1888,1889,1893,1897,1898,1899]){
   const w=await world(y);expect(w.features.length).toBeGreaterThan(95);expect(new Set(w.features.map(f=>f.id)).size).toBe(w.features.length);
   for(const key of ['FRA','USA','ESP','RUE','QING','OTT','AUT-HUN'])expect((await id(key,y)).leaders.length,key+':'+y).toBeGreaterThan(0);
  }
  expect((await id('RUE',1880)).leaders.map(l=>l.name).join(' ')).toMatch(/Alejandro/);
  expect((await id('HTI',1880)).leaders.map(l=>l.name).join(' ')).not.toMatch(/Soulouque/);
  expect((await country('SWZ',1897)).identityKey).toBe('SWZ');
  expect((await id('NPL',1880)).leaders.map(l=>l.name).join(' ')).toMatch(/Ranodip/);
 });
 it('separates the Brazilian monarchy/republic and retains predecessor offices in1889',async()=>{
  expect((await id('BRA-EMPIRE',1888)).leaders.some(l=>l.person==='Q156774')).toBe(true);
  const transition=await id('BRA',1889);expect(transition.leaders.some(l=>l.person==='Q200812')).toBe(true);
  expect(transition.leaders.some(l=>l.person==='Q156774'&&/predecesora/.test(l.role))).toBe(true);
  expect(transition.flag?.title).toContain('1889');expect(regimeColor('BRA',1889)).not.toBe(regimeColor('BRA-EMPIRE',1888));
  expect((await country('BRA-EMPIRE',1888)).code).toBe('');
 });
 it('keeps Hawaiian phases and annexation distinct, integrating islands into USA only from1898',async()=>{
  expect((await id('HAW-KINGDOM',1892)).leaders.length).toBeGreaterThan(0);
  const provisional=await id('HAW-PROVISIONAL',1893);expect(provisional.leaders.some(l=>/predecesora/.test(l.role))).toBe(true);
  expect((await id('HAW-REPUBLIC',1894)).leaders.some(l=>/Dole/.test(l.name))).toBe(true);
  expect((await world(1898)).features.some(f=>f.properties?.identityKey==='HAW')).toBe(false);
  expect((await overlaysFor(1898)).features.every(f=>f.properties?.relation==='incorporation')).toBe(true);
 });
 it('shows early treaty membership without retrojecting organizations or independence',async()=>{
  expect(organizationActive('tripleAlliance',1881)).toBe(false);
  expect(membershipsAt('tripleAlliance',1882).map(m=>m.code)).toEqual(expect.arrayContaining(['DEU','AUH','ITA']));
  expect(membershipsAt('un',1889)).toEqual([]);
  expect((await id('GRL',1890)).administration?.admin).toBe('DNK');
  expect((await id('GRL',2016)).administration?.admin).toBe('DNK');
  expect((await world(1942)).features.find(f=>f.properties?.entityCode==='GRL')?.properties?.identityKey).toBe('GRL');
 });
});
