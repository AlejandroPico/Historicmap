import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,normalizedName,withHistoricalSupplements} from '../src/history';
import {politicalData,regimeColor} from '../src/political';
import {identityFor} from '../src/identities';
import {membershipsAt,organizationActive} from '../src/historical-affiliations';
import {eventsForCountry} from '../src/historical-context';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology=read('history.topojson'),profiles=read('profiles.json'),identities=read('identities.json'),supplements=read('historical-supplements.geojson');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const world=(y:number)=>politicalData(withHistoricalSupplements(historyAt(topology,y,names),y,supplements,historyAt(topology,1974,names)),y);
const country=(name:string,y:number)=>world(y).features.find(f=>f.properties?.originalName===name)!.properties!;
const id=(name:string,y:number)=>identityFor(country(name,y),y,identities,new Date(2026,9,24));

describe('1900–1919 historical states, administrations and transitions',()=>{
 it('keeps imperial and republican identities separate from successor statistics',()=>{
  for(const [name,year,key] of [['Russia (Soviet Union)',1900,'RUE'],['China',1900,'QING'],['Austria-Hungary',1900,'AUT-HUN'],['Turkey (Ottoman Empire)',1900,'OTT'],['Serbia',1900,'SRK'],['Montenegro',1900,'MNK'],['Korea',1900,'KEM']] as const){
   expect(id(name,year).key).toBe(key);expect(country(name,year).code).toBe('');expect(id(name,year).leaders.length).toBeGreaterThan(0);
  }
  expect(id('China',1912).key).toBe('ROC');expect(id('China',1912).leaders.map(l=>l.name).join(' ')).toMatch(/Sun Yat-sen/);
  expect(id('China',1912).leaders.some(l=>/predecesora/.test(l.role)&&l.person==='Q185152')).toBe(true);
  expect(id('Russia (Soviet Union)',1917).leaders.map(l=>l.name).join(' ')).toMatch(/Nicolás.*Lvov.*Kerenski|Lenin/);
  expect(id('Russia (Soviet Union)',1916).leaders.some(l=>l.person==='Q1394')).toBe(false);
  expect(regimeColor('RUE',1900)).not.toBe(regimeColor('USSR',1970));
  expect(country('Serbia',2006)).toMatchObject({code:'SRB',entityCode:'SRB'});expect(id('Serbia',2006).key).toBe('SRB');
  expect(country('Montenegro',2006)).toMatchObject({code:'MNE',entityCode:'MNE'});expect(id('Montenegro',2006).key).toBe('MNE');
  expect(country('Serbia',2006).name).not.toContain('Reino');expect(country('Montenegro',2006).name).not.toContain('Reino');
 });
 it('distinguishes Korean local sovereigns, Japanese protection and colonial annexation',()=>{
  const protectedId=id('Korea',1907);
  expect(country('Korea',1907).status).toBe('protectorate');expect(protectedId.administration?.admin).toBe('JPN');
  expect(protectedId.leaders.some(l=>l.authorityScope==='local'&&l.person==='Q334111')).toBe(true);
  expect(protectedId.leaders.some(l=>l.authorityScope==='external')).toBe(true);
  const colony=id('Korea',1911);expect(colony.leaders.some(l=>l.authorityScope==='local'&&l.person==='Q334111')).toBe(false);
  expect(id('Korea',1910).flag?.title).toMatch(/Japan/);expect(id('Korea',1910).flagContext).toContain('administrador');
 });
 it('corrects Boer colonial status and personal sovereignty in Congo without altering source polygons',()=>{
  expect(country('Transvaal',1901).status).toBe('independent');expect(country('Transvaal',1903).status).toBe('colony');
  expect(id('Transvaal',1903).administration?.admin).toBe('GBR');expect(id('Orange Free State',1903).leaders.length).toBeGreaterThan(0);
  const congo=id('Congo, Democratic Republic of (Zaire)',1907);expect(congo.key).toBe('CFS');expect(congo.administration).toBeUndefined();
  expect(congo.leaders.every(l=>l.person==='Q12967')).toBe(true);
  const transfer=id('Congo, Democratic Republic of (Zaire)',1908);expect(transfer.administration?.admin).toBe('BEL');expect(transfer.leaders.some(l=>l.authorityScope==='local')).toBe(true);
  const source=topology.objects.countries.geometries.find((g:any)=>g.properties.country_name==='Transvaal'&&g.properties.start<='1903-12-31'&&g.properties.end>='1903-12-31');expect(source.properties.status).toBe('independent');
 });
 it('retains Moroccan and Tongan native monarchs alongside dated external administrators',()=>{
  expect(id('Morocco',1905).key).toBe('MAR');expect(country('Morocco',1905).status).toBe('independent');
  const morocco=id('Morocco',1913);expect(morocco.leaders.some(l=>l.person==='Q276937'&&l.authorityScope==='local')).toBe(true);expect(morocco.administration?.admin).toBe('FRA');
  const tonga=id('Tonga',1900);expect(tonga.leaders.some(l=>l.authorityScope==='local')).toBe(true);expect(tonga.administration?.admin).toBe('GBR');
  expect(id('Tonga',1971).administration).toBeUndefined();
 });
 it('shows dated WWI groupings without treating neutral Italy as an active Central Power',()=>{
  expect(organizationActive('tripleAlliance',1900)).toBe(true);
  expect(membershipsAt('tripleAlliance',1914).some(m=>m.code==='ITA')).toBe(true);
  expect(membershipsAt('centralPowersWW1',1914).some(m=>m.code==='ITA')).toBe(false);
  expect(membershipsAt('tripleAlliance',1915)).toEqual([]);
  expect(eventsForCountry(country('Russia (Soviet Union)',1905),1905).length).toBeGreaterThan(0);
 });
});
