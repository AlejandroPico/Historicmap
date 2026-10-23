import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,normalizedName} from '../src/history';
import {politicalData} from '../src/political';
import {identityFor,identityMarkup,type IdentityData} from '../src/identities';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const identities:IdentityData=read('identities.json'),profiles=read('profiles.json'),topology=read('history.topojson');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const world=(y:number)=>politicalData(historyAt(topology,y,names),y);
const territory=(name:string,y:number)=>world(y).features.find(f=>f.properties?.originalName===name)!.properties!;
const at=(name:string,y:number)=>identityFor(territory(name,y),y,identities,new Date(2026,9,23));
describe('dated national and local authorities of dependent territories',()=>{
 it('finds an authority for every source-classified colony, mandate or protectorate in the reviewed annual period',()=>{
  const missing:string[]=[];
  for(let year=1970;year<=2019;year++)for(const f of world(year).features){
   if(!['colony','mandate','protectorate'].includes(f.properties?.status))continue;
   if(!identityFor(f.properties!,year,identities,new Date(2026,9,23)).leaders.length)missing.push(`${year}:${f.properties?.originalName}`);
  }
  expect(missing).toEqual([]);
 },30000);
 it('fills the source-dependent territories reported in 1970 without borrowing independent successor governments',()=>{
  for(const name of ['Angola','Mozambique','Guinea-Bissau']){
   const id=at(name,1970);expect(id.leaders.map(l=>l.name).join(' ')).toMatch(/Américo Tomás/);expect(id.leaders.map(l=>l.name).join(' ')).toMatch(/Marcelo Caetano/);
   expect(id.leaders.every(l=>l.authorityScope==='external')).toBe(true);expect(territory(name,1970).code).toBe('');
   expect(id.leaders.find(l=>l.name==='Marcelo Caetano')?.end).toBe('1974-04-25');
  }
  expect(at('Namibia',1970).leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q886942','Q313903']));
  expect(at('Namibia',1970).administration?.label).toContain('ilegal');
  expect(at('Spanish Sahara',1970).leaders.some(l=>/Francisco Franco/.test(l.name))).toBe(true);
  expect(at('Spanish Sahara',1970).leaders.some(l=>l.person==='Q24279111'&&l.authorityScope==='local')).toBe(true);
 });
 it('separates autonomous local governments from the shared crown and labels metropolitan symbols',()=>{
  const sur=at('Surinam',1970);
  expect(sur.leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q333129','Q924337']));
  expect(sur.leaders.some(l=>/Juliana/.test(l.name)&&l.authorityScope==='external')).toBe(true);
  expect(sur.leaders.some(l=>/Piet de Jong/.test(l.name))).toBe(false);
  const bahamas=at('Bahamas',1970);expect(bahamas.leaders.some(l=>l.person==='Q920953'&&l.authorityScope==='local')).toBe(true);
  expect(bahamas.leaders.some(l=>/Heath|Wilson/.test(l.name))).toBe(false);
  const guiana=territory('French Guyana',1970),markup=identityMarkup(guiana,1970,identities,'/','all');
  expect(markup).toContain('Pompidou');expect(markup).toContain('Chaban-Delmas');expect(markup).toContain('Símbolo del Estado administrador');
  for(const name of ['Guadeloupe','Martinique'])expect(at(name,1970).leaders.some(l=>/Pompidou/.test(l.name))).toBe(true);
  const pr=at('Puerto Rico',1970);expect(pr.leaders.some(l=>/Ferré/.test(l.name)&&l.authorityScope==='local')).toBe(true);expect(pr.leaders.some(l=>/Nixon/.test(l.name)&&l.authorityScope==='external')).toBe(true);
 });
 it('clips jurisdictional mandates at independence without turning those limits into resignations',()=>{
  const angola=at('Angola',1975);expect(angola.leaders.some(l=>l.authorityScope==='local'&&/Neto/.test(l.name))).toBe(true);
  expect(angola.leaders.filter(l=>l.authorityScope==='external').every(l=>l.end<='1975-11-10')).toBe(true);
  expect(angola.leaders.some(l=>l.authorityScope==='external'&&l.end==='1975-11-10'&&l.endIsCoverageBoundary)).toBe(true);
  for(const [name,y] of [['Angola',1976],['Mozambique',1976],['Guinea-Bissau',1975],['Surinam',1976],['Bahamas',1974],['Namibia',1991]] as const)expect(at(name,y).administration,`${name} ${y}`).toBeUndefined();
  expect(at('Bahamas',1974).leaders.some(l=>/Isabel/.test(l.name))).toBe(true);
  expect(identityFor({code:'PRI',name:'Puerto Rico'},2027,identities,new Date(2027,0,1)).leaders).toEqual([]);
 });
 it('uses source administration for other colonies while leaving independent allies untouched',()=>{
  const colony=world(1970).features.find(f=>f.properties?.status==='colony'&&f.properties?.administratorKey&&!['Angola','Mozambique','Guinea-Bissau','Namibia','Surinam','French Guyana','Guadeloupe','Martinique','Spanish Sahara','Puerto Rico','Bahamas'].includes(f.properties?.originalName));
  expect(colony).toBeDefined();expect(identityFor(colony!.properties!,1970,identities).leaders.length).toBeGreaterThan(0);
  expect(identityFor({code:'POL',identityKey:'POL',status:'independent',dominantPower:'USSR'},1970,identities).administration).toBeUndefined();
 });
});
