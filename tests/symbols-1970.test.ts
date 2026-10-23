import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {describe,it,expect} from 'vitest';
import {identityFor,type IdentityData} from '../src/identities';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/'+f,import.meta.url),'utf8'));
const data:IdentityData=read('data/identities.json');
const manifest=read('media/manifest.json');
const flag=(code:string,year:number)=>identityFor({code},year,data,new Date(2026,9,23)).flag;

describe('historically dated national symbols, 1970–1989',()=>{
 it('uses Bulgarian emblems before 1990 instead of projecting the plain modern tricolor',()=>{
  expect(flag('BGR',1970)?.title).toBe('Flag of Bulgaria (1967–1971).svg');
  expect(flag('BGR',1971)?.title).toBe('Flag of Bulgaria (1971–1990).svg');
  expect(flag('BGR',1989)?.title).toBe('Flag of Bulgaria (1971–1990).svg');
  expect(flag('BGR',1990)?.title).toBe('Flag of Bulgaria.svg');
 });
 it('distinguishes the Lao kingdom and the 1975 republican flag readoption',()=>{
  expect(flag('LAO',1970)?.title).toBe('Flag of Laos (1952–1975).svg');
  expect(flag('LAO',1974)?.title).toBe('Flag of Laos (1952–1975).svg');
  expect(flag('LAO',1975)?.title).toBe('Flag of Laos.svg');
 });
 it('keeps the Iranian lion-and-sun family distinct from later republican designs and retrieval-only artifacts',()=>{
  expect(flag('IRN',1970)?.title).toBe('State flag of Iran 1964-1979 (alternate).svg');
  expect(flag('IRN',1978)?.title).toBe('State flag of Iran 1964-1979 (alternate).svg');
  expect(flag('IRN',1979)?.title).toBe('State flag of Iran 1964-1979 (alternate).svg');
  expect(flag('IRN',1980)?.title).toBe('Flag of Iran.svg');
  expect(flag('IRN',2026)?.title).toBe('Flag of Iran.svg');
 });
 it('follows Afghan design changes through the republican and socialist periods',()=>{
  const expected:Record<number,string>={1970:'1931–1973',1973:'1973–1974',1974:'1974–1978',1977:'1974–1978',1978:'1978–1980',1979:'1978–1980',1980:'1980–1987',1986:'1980–1987',1987:'1987–1992'};
  for(const [year,period] of Object.entries(expected))expect(flag('AFG',Number(year))?.title,year).toBe(`Flag of Afghanistan (${period}).svg`);
 });
 it('finds the actual Mongolian source title and preserves the earlier Burmese design',()=>{
  expect(flag('MNG',1970)?.title).toBe("Flag of the Mongolian People's Republic (1945–1992).svg");
  expect(flag('MNG',1991)?.title).toBe("Flag of the Mongolian People's Republic (1945–1992).svg");
  expect(flag('MNG',1992)?.title).toBe('Flag of Mongolia (1992–2011).svg');
  expect(flag('MMR',1970)?.title).toBe('Flag of Burma (1948–1974).svg');
  expect(flag('MMR',1973)?.title).toBe('Flag of Burma (1948–1974).svg');
  expect(flag('MMR',1974)?.title).toBe('Flag of Myanmar (1974–2010).svg');
 });
 it('retains source licenses and unchanged SVG bytes for every curated design',()=>{
  const flags=Object.values(data.countries).flatMap(c=>c.flags).filter((f:any)=>f.acquisition==='curated-symbols-0.8');
  expect(flags).toHaveLength(11);
  for(const f of flags){
   const m=f.media;expect(m.license).toMatch(/Public domain|CC BY-SA|CC0/);
   expect(f.source).toBe(m.url);expect(m.artist.length).toBeGreaterThan(0);
   if(m.license==='CC BY-SA 3.0')expect(m.licenseUrl).toContain('creativecommons.org/licenses/by-sa/3.0');
   const raw=readFileSync(new URL('../public/'+m.file,import.meta.url));
   expect(createHash('sha256').update(raw).digest('hex')).toBe(m.sha256);
   expect(manifest.entries.find((e:any)=>e.file===m.file)?.sha256).toBe(m.sha256);
   expect(raw.toString()).toContain('<svg');
  }
 });
 it('keeps Traykov mandates while withholding an ambiguously identified portrait',()=>{
  const terms=data.countries.BGR.leaders.filter(l=>l.person==='Q1811651');
  expect(terms.length).toBeGreaterThan(0);
  for(const l of terms){expect(l.portrait).toBeUndefined();expect(l.note).toContain('atribución ambigua');}
 });
});
