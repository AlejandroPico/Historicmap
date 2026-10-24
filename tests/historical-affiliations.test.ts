import {describe,it,expect} from 'vitest';
import {AFFILIATIONS,AFFILIATION_KINDS,affiliationFor,affiliationsDuringYear,affiliationGroups,affiliationSummary,affiliationsAvailable,organizationActive} from '../src/historical-affiliations';

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
   for(let year=1970;year<=2026;year++){
    const codes=affiliationGroups(o.id,year).flatMap(c=>c.codes);
    expect(new Set(codes).size,`${o.id} ${year}: overlapping categories`).toBe(codes.length);
   }
  }
 });
 it('extends acquired coverage to1970 without backdating subsequent institutions',()=>{
  expect(affiliationsAvailable(1899)).toBe(false);expect(affiliationsAvailable(1900)).toBe(true);expect(affiliationsAvailable(1949)).toBe(true);
  expect(affiliationsAvailable(1960)).toBe(true);
  expect(affiliationsAvailable(1970)).toBe(true);
  expect(affiliationGroups('nato',1970)[0].codes).toHaveLength(15);
  expect(affiliationFor('ESP','nato',1981)?.category).toBe('other');
  expect(affiliationFor('ESP','nato',1982)?.category).toBe('member');
  expect(organizationActive('gcc',1980)).toBe(false);
  expect(affiliationGroups('gcc',1981)[0].codes).toHaveLength(6);
  expect(organizationActive('saarc',1984)).toBe(false);
  expect(affiliationGroups('saarc',1985)[0].codes).toHaveLength(7);
  expect(organizationActive('apec',1988)).toBe(false);
  expect(affiliationGroups('apec',1989)[0].codes).toHaveLength(12);
 });
 it('distinguishes EFTA associations, European enlargement and territorial application',()=>{
  expect(affiliationFor('FIN','efta',1970)?.category).toBe('associate');
  expect(affiliationFor('FIN','efta',1986)?.category).toBe('member');
  expect(affiliationFor('GBR','efta',1972)?.category).toBe('member');
  expect(affiliationFor('GBR','efta',1973)?.category).toBe('other');
  expect(affiliationFor('PRT','efta',1985)?.category).toBe('member');
  expect(affiliationFor('PRT','efta',1986)?.category).toBe('other');
  expect(affiliationFor('ESP','eu',1985)?.category).toBe('other');
  expect(affiliationFor('ESP','eu',1986)?.category).toBe('member');
  expect(affiliationFor('GRL','eu',1984)?.territorialApplication).toBe(true);
  expect(affiliationFor('GRL','eu',1985)?.category).toBe('other');
  expect(affiliationSummary('eu',1973)).toContain('9 miembros · 1 territorio de aplicación');
 });
 it('preserves ColdWar entities and different COMECON participation categories',()=>{
  expect(affiliationFor('SUN','warsaw',1970)?.category).toBe('member');
  expect(affiliationFor('RUS','warsaw',1970)?.category).toBe('other');
  expect(affiliationFor('ALB','warsaw',1970)?.category).toBe('other');
  expect(affiliationFor('YUG','warsaw',1970)?.category).toBe('other');
  expect(affiliationFor('YUG','comecon',1970)?.category).toBe('associate');
  expect(affiliationFor('ALB','comecon',1970)?.category).toBe('suspended');
  expect(affiliationFor('ALB','comecon',1987)?.category).toBe('other');
  expect(affiliationFor('CUB','comecon',1971)?.category).toBe('other');
  expect(affiliationFor('CUB','comecon',1972)?.category).toBe('member');
  expect(affiliationFor('VNM','comecon',1977)?.category).toBe('other');
  expect(affiliationFor('VNM','comecon',1978)?.category).toBe('member');
  expect(affiliationFor('FIN','comecon',1973)?.category).toBe('partner');
  expect(affiliationFor('YPR','comecon',1990)?.category).toBe('other');
 });
 it('dates decolonization and changes in African regional cooperation',()=>{
  expect(affiliationFor('AGO','au',1975)?.category).toBe('other');
  expect(affiliationFor('AGO','au',1976)?.category).toBe('member');
  expect(affiliationFor('CPV','au',1974)?.category).toBe('other');
  expect(affiliationFor('CPV','au',1975)?.category).toBe('member');
  expect(affiliationFor('ESH','au',1981)?.category).toBe('other');
  expect(affiliationFor('ESH','au',1982)?.category).toBe('member');
  expect(affiliationFor('MAR','au',1983)?.category).toBe('member');
  expect(affiliationFor('MAR','au',1984)?.category).toBe('other');
  expect(affiliationFor('CPV','ecowas',1976)?.category).toBe('other');
  expect(affiliationFor('CPV','ecowas',1977)?.category).toBe('member');
  expect(organizationActive('sadc',1979)).toBe(false);
  expect(affiliationGroups('sadc',1980)[0].codes).toHaveLength(9);
  expect(organizationActive('eac1967',1976)).toBe(true);
  expect(organizationActive('eac1967',1977)).toBe(false);
  expect(organizationActive('eacCooperation',1992)).toBe(false);
  expect(organizationActive('eacCooperation',1993)).toBe(true);
  expect(organizationActive('eacCooperation',2000)).toBe(false);
  expect(organizationActive('eac',2000)).toBe(true);
  expect(affiliationGroups('maghreb',1989)[0].codes).toHaveLength(5);
 });
 it('records LatinAmerican accessions and withdrawals without modern backprojection',()=>{
  expect(affiliationFor('CHL','andean',1975)?.category).toBe('member');
  expect(affiliationFor('CHL','andean',1976)?.category).toBe('other');
  expect(affiliationFor('CHL','andean',2006)?.category).toBe('associate');
  expect(affiliationFor('VEN','andean',1972)?.category).toBe('other');
  expect(affiliationFor('VEN','andean',1973)?.category).toBe('member');
  expect(affiliationGroups('caricom',1973)[0].codes).toHaveLength(4);
  expect(affiliationGroups('caricom',1974)[0].codes).toHaveLength(12);
  expect(affiliationFor('BHS','caricom',1982)?.category).toBe('other');
  expect(affiliationFor('BHS','caricom',1983)?.category).toBe('member');
  expect(affiliationFor('ATG','oas',1980)?.category).toBe('other');
  expect(affiliationFor('ATG','oas',1981)?.category).toBe('member');
  expect(affiliationFor('CAN','oas',1989)?.category).toBe('other');
  expect(affiliationFor('CAN','oas',1990)?.category).toBe('member');
  expect(affiliationFor('CUB','oas',1970)?.category).toBe('suspended');
  expect(affiliationFor('ARG','oas',1970)?.start).toBe('1948-04-30');
  expect(affiliationFor('ARG','oas',1970)?.note).toContain('13/12/1951');
 });
 it('keeps the two Yemens and Egyptian suspension distinct from later membership',()=>{
  expect(affiliationFor('YAR','arabLeague',1970)?.category).toBe('member');
  expect(affiliationFor('YPR','arabLeague',1970)?.category).toBe('member');
  expect(affiliationFor('YEM','arabLeague',1989)?.category).toBe('other');
  expect(affiliationFor('YAR','arabLeague',1990)?.category).toBe('other');
  expect(affiliationFor('YEM','arabLeague',1990)?.category).toBe('member');
  expect(affiliationFor('EGY','arabLeague',1978)?.category).toBe('member');
  expect(affiliationFor('EGY','arabLeague',1979)?.category).toBe('suspended');
  expect(affiliationFor('EGY','arabLeague',1988)?.category).toBe('suspended');
  expect(affiliationFor('EGY','arabLeague',1989)?.category).toBe('member');
  expect(affiliationsDuringYear('EGY','arabLeague',1989).map(m=>m.category)).toEqual(['suspended','member']);
 });
 it('uses OECD Convention dates rather than presentmembership lists',()=>{
  expect(affiliationFor('AUS','oecd',1970)?.category).toBe('other');
  expect(affiliationFor('AUS','oecd',1971)?.category).toBe('member');
  expect(affiliationFor('NZL','oecd',1972)?.category).toBe('other');
  expect(affiliationFor('NZL','oecd',1973)?.category).toBe('member');
  expect(affiliationGroups('oecd',1970)[0].codes).toHaveLength(22);
  expect(affiliationGroups('oecd',2026)[0].codes).toHaveLength(38);
  expect(affiliationFor('DDR','oecd',1989)?.category).toBe('other');
 });
});
