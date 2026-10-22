import {describe,it,expect} from 'vitest';
import {AFFILIATIONS,AFFILIATION_KINDS,affiliationFor,affiliationsDuringYear,affiliationGroups,organizationActive} from '../src/historical-affiliations';

describe('dated regional and intercontinental organizations',()=>{
 it('dates NATO enlargements and Brexit independently of the current snapshot',()=>{
  expect(affiliationFor('POL','nato',1998)?.category).toBe('other');
  expect(affiliationFor('POL','nato',1999)?.category).toBe('member');
  expect(affiliationFor('FIN','nato',2022)?.category).toBe('other');
  expect(affiliationFor('FIN','nato',2023)?.category).toBe('member');
  expect(affiliationFor('SWE','nato',2023)?.category).toBe('other');
  expect(affiliationFor('SWE','nato',2024)?.category).toBe('member');
  expect(affiliationFor('GBR','eu',2019)?.category).toBe('member');
  expect(affiliationFor('GBR','eu',2020)?.category).toBe('other');
  expect(affiliationsDuringYear('GBR','eu',2020)).toHaveLength(1);
  expect(affiliationFor('GRL','eu',2026)?.category).toBe('other');
 });
 it('does not invent organizations before foundation, after dissolution or outside acquired coverage',()=>{
  expect(organizationActive('brics',1990)).toBe(false);
  expect(affiliationGroups('brics',1990)).toEqual([]);
  expect(organizationActive('warsaw',1990)).toBe(true);
  expect(organizationActive('warsaw',1991)).toBe(false);
  expect(affiliationFor('SUN','warsaw',1990)?.category).toBe('member');
  expect(affiliationFor('RUS','warsaw',1990)?.category).toBe('other');
  expect(organizationActive('nafta',2019)).toBe(true);
  expect(organizationActive('nafta',2020)).toBe(false);
  expect(organizationActive('usmca',2020)).toBe(true);
  expect(affiliationFor('USA','nato',2027)).toBeUndefined();
 });
 it('preserves regional accessions, exits and different categories',()=>{
  expect(AFFILIATION_KINDS.length).toBeGreaterThanOrEqual(25);
  expect(affiliationFor('TLS','asean',2024)?.category).toBe('other');
  expect(affiliationFor('TLS','asean',2025)?.category).toBe('member');
  expect(affiliationFor('SOM','eac',2023)?.category).toBe('other');
  expect(affiliationFor('SOM','eac',2024)?.category).toBe('member');
  expect(affiliationFor('MLI','ecowas',2026)?.category).toBe('other');
  expect(affiliationFor('UKR','threeSeas',2026)?.category).toBe('associate');
  expect(affiliationFor('VNM','brics',2026)?.category).toBe('partner');
  expect(affiliationGroups('nato',2026)[0].codes).toHaveLength(32);
  expect(affiliationGroups('eu',2026)[0].codes).toHaveLength(27);
  expect(affiliationGroups('brics',2026).map(c=>c.codes.length)).toEqual([11,10]);
  expect(affiliationGroups('threeSeas',2026).map(c=>c.codes.length)).toEqual([13,4,6]);
 });
 it('has sourced, nonoverlapping categories for every country at every annual close',()=>{
  for(const o of Object.values(AFFILIATIONS)){
   expect(o.source).toMatch(/^https:\/\//);
   for(const m of o.memberships){expect(m.code).toMatch(/^[A-Z]{3}$/);expect(m.source).toMatch(/^https:\/\//);if(m.end)expect(m.end>m.start,`${o.id}:${m.code}`).toBe(true);}
   for(let year=1990;year<=2026;year++){
    const codes=affiliationGroups(o.id,year).flatMap(c=>c.codes);
    expect(new Set(codes).size,`${o.id} ${year}: overlapping categories`).toBe(codes.length);
   }
  }
 });
});
