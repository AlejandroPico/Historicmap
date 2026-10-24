import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import type {Feature,FeatureCollection,Position} from 'geojson';
import {historyAt,normalizedName} from '../src/history';
import {politicalData,regimeColor} from '../src/political';
import {composeControl} from '../src/control-map';
import {identityFor} from '../src/identities';
import {affiliationFor,affiliationGroups,organizationActive} from '../src/historical-affiliations';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology=read('history.topojson'),identities=read('identities.json'),profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const world=(year:number)=>politicalData(historyAt(topology,year,names),year);
const original=(year:number,name:string)=>world(year).features.find(f=>f.properties?.originalName===name)!;
const ring=([x,y]:number[],r:Position[])=>{let yes=false;for(let i=0,j=r.length-1;i<r.length;j=i++){const a=r[i],b=r[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;};
const contains=(f:Feature,p:number[])=>{const polys=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];return polys.some(a=>ring(p,a[0])&&!a.slice(1).some(r=>ring(p,r)));};
const id=(key:string,year:number)=>identityFor({identityKey:key},year,identities,new Date(2026,9,24));

describe('1920–1949 historical entities and documentary corrections',()=>{
 it('separates Soviet Russia, the USSR, republican China and the Yugoslav monarchy from successors',()=>{
  expect(original(1921,'Russia (Soviet Union)').properties).toMatchObject({identityKey:'RSR',code:''});
  expect(original(1922,'Russia (Soviet Union)').properties?.identityKey).toBe('USSR');
  expect(original(1930,'China').properties).toMatchObject({identityKey:'ROC',code:'',name:'República de China'});
  expect(original(1928,'Yugoslavia').properties?.identityKey).toBe('YKM');
  expect(original(1929,'Yugoslavia').properties?.name).toBe('Reino de Yugoslavia');
  expect(original(1946,'Yugoslavia').properties?.identityKey).toBe('YUG');
  expect(id('RSR',1921).leaders.some(l=>l.name.includes('Lenin'))).toBe(true);
  expect(id('ROC',1935).leaders.some(l=>l.name==='Lin Sen')).toBe(true);
  expect(regimeColor('RSR',1921)).toBe(regimeColor('USSR',1921));
 });
 it('corrects Danzig1938 exactly once without altering its source topology or adjacent annexations',()=>{
  const source=JSON.stringify(topology),controls:FeatureCollection=read('historical-control.geojson');
  const base=world(1938),active={...controls,features:controls.features.filter(f=>f.properties!.start<=1938&&f.properties!.end>=1938)};
  const result=composeControl(base,active,1938);
  const at=(p:number[])=>result.territories.features.filter(f=>contains(f,p));
  expect(at([18.64,54.35]).map(f=>f.properties?.identityKey)).toEqual(['DAN']);
  for(const point of [[13.4,52.52],[16.37,48.21]])expect(at(point).map(f=>f.properties?.identityKey)).toEqual(['DEU']);
  expect(result.occupations.features.some(f=>contains(f,[18.64,54.35]))).toBe(false);
  expect(original(1939,'Danzig')).toBeUndefined();
  expect(world(1939).features.find(f=>contains(f,[18.64,54.35]))?.properties?.identityKey).toBe('DEU');
  expect(JSON.stringify(topology)).toBe(source);
  const raw=topology.objects.countries.geometries.find((g:any)=>g.properties.country_name==='Danzig');
  expect(raw.properties.end).toBe('1938-08-31');
 },60000);
 it('resolves German control of Austria, collective occupation and separately dated German republics',()=>{
  const austria=identityFor(original(1940,'Austria').properties!,1940,identities,new Date(2026,9,24));
  expect(austria.leaders.some(l=>l.name.includes('Hitler'))).toBe(true);
  expect(id('DEU',1946).flag).toBeUndefined();
  expect(id('DEU',1946).leaders.some(l=>l.person==='COLLECTIVE-DEU-ALLIED-OCCUPATION')).toBe(true);
  const west=identityFor(original(1946,'German Federal Republic').properties!,1946,identities,new Date(2026,9,24));
  expect(west.administration).toBeUndefined();expect(west.flag).toBeUndefined();
  expect(west.leaders.map(l=>l.person)).toEqual(['COLLECTIVE-DEU-ALLIED-OCCUPATION']);
  expect(original(1946,'German Federal Republic').properties?.ownerName).toContain('Francia');
  expect(id('DEU',1949).leaders.some(l=>l.name.includes('Adenauer'))).toBe(true);
  expect(id('DDR',1949).leaders.some(l=>l.name.includes('Grotewohl'))).toBe(true);
 });
 it('keeps dominant and formal offices distinct in Nepal, Ethiopia, Albania and pre-republican Ankara',()=>{
  for(const [key,year,person] of [['NPL',1927,'Q1061786'],['ETH',1925,'Q148524'],['ETH',1942,'Q41178'],['ALB',1942,'Q984363'],['TUR',1922,'Q5152']] as const)expect(id(key,year).leaders.some(l=>l.person===person),`${key}${year}`).toBe(true);
  expect(id('NPL',1937).leaders.some(l=>l.person==='Q381928')).toBe(true);
  expect(id('TUR',1935).leaders.filter(l=>l.person==='Q5152').every(l=>!l.role.includes('Gobierno'))).toBe(true);
  expect(id('YMK',1949).leaders.some(l=>l.person==='Q400961')).toBe(true);
 });
 it('dates League membership, UN representation and treaty entry into force',()=>{
  expect(organizationActive('nato',1948)).toBe(false);expect(organizationActive('nato',1949)).toBe(true);
  expect(affiliationFor('USA','nato',1949)?.start).toBe('1949-08-24');
  expect(affiliationFor('DEU','leagueOfNations',1934)?.category).toBe('member');
  expect(affiliationFor('DEU','leagueOfNations',1935)?.category).toBe('other');
  expect(affiliationFor('SUN','leagueOfNations',1934)?.category).toBe('member');
  expect(affiliationFor('SUN','leagueOfNations',1939)?.category).toBe('other');
  expect(affiliationFor('SUN','un',1945)?.category).toBe('member');
  expect(affiliationFor('RUS','un',1945)?.category).toBe('other');
  for(const [year,count] of [[1945,51],[1946,55],[1947,57],[1948,58],[1949,59],[2026,193]])expect(affiliationGroups('un',year).find(g=>g.category==='member')?.codes.length,`UN${year}`).toBe(count);
 });
 it('uses interwar symbol variants and does not backdate the PRC or a national occupation flag',()=>{
  expect(id('MEX',1920).flag?.title).toContain('1916');expect(id('MEX',1935).flag?.title).toContain('1934');
  expect(id('NIC',1930).flag?.title).toContain('1908');expect(id('GRC',1930).flag?.title).toContain('1822');
  expect(id('ALB',1942).flag?.title).toContain('1939');
  expect(id('CHN',1948).flag).toBeUndefined();expect(id('ROC',1930).flag).toBeDefined();
  expect(id('DEU',1947).flag).toBeUndefined();expect(id('DDR',1948).flag).toBeUndefined();
  expect(id('DAN',1938).flag?.title).toContain('Danzig');
 });
});
