import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {describe,it,expect} from 'vitest';
import {identityFor,identityMarkup,type IdentityData} from '../src/identities';
const data:IdentityData=JSON.parse(readFileSync(new URL('../public/data/identities.json',import.meta.url),'utf8'));
const now=new Date(2026,9,22,12);
const at=(key:string,year:number)=>identityFor({identityKey:key,name:key},year,data,now);
const names=(key:string,year:number)=>at(key,year).leaders.map(l=>l.name).join(' / ');

describe('dated flags and political authorities',()=>{
 it('follows real US presidential terms across different lengths and repeat presidencies',()=>{
  for(const [year,name] of [[1789,'Washington'],[1865,'Johnson'],[1942,'Roosevelt'],[2006,'Bush'],[2012,'Obama'],[2018,'Trump'],[2023,'Biden'],[2026,'Trump']] as const)expect(names('USA',year),String(year)).toContain(name);
  expect(at('USA',1942).flag?.title).toContain('1912-1959');
  expect(at('USA',2026).flag?.title).toBe('Flag of the United States.svg');
 });
 it('selects Spanish heads of government without replacing past officeholders with the incumbent',()=>{
  for(const [year,name] of [[1976,'Suárez'],[1981,'Calvo-Sotelo'],[1990,'González'],[2000,'Aznar'],[2008,'Zapatero'],[2015,'Rajoy'],[2026,'Sánchez']] as const)expect(names('ESP',year),String(year)).toContain(name);
  expect(names('ESP',2015)).not.toContain('Sánchez');
  expect(at('ESP',2026).leaders[0].name).toContain('Sánchez');
 });
 it('preserves authentic historical German flags and leaves the occupation interval without a national flag',()=>{
  expect(at('DEU',1942).flag?.title).toBe('Flag of Germany (1935–1945).svg');
  expect(names('DEU',1942)).toContain('Hitler');
  expect(at('DEU',1946).flag).toBeUndefined();
  expect(at('DEU',1946).leaders).toHaveLength(0);
  expect(at('DEU',1946).note).toContain('Administración militar');
  expect(at('DDR',1948).flag).toBeUndefined();
  expect(at('DDR',1958).flag?.title).toBe('Flag of Germany.svg');
  expect(at('DDR',1960).flag?.title).toBe('Flag of East Germany.svg');
 });
 it('keeps both sides of the Spanish Civil War distinct',()=>{
  expect(names('ESP-REPUBLIC',1936)).toContain('Azaña');
  expect(names('ESP-REPUBLIC',1936)).toContain('Largo Caballero');
  expect(names('ESP-REPUBLIC',1937)).toContain('Negrín');
  expect(names('ESP-NATIONALIST',1936)).toContain('Franco');
  expect(names('ESP-REPUBLIC',1938)).not.toContain('Franco');
  expect(at('ESP-REPUBLIC',1938).flag?.title).toContain('1931');
  expect(at('ESP-NATIONALIST',1936).flag?.title).toContain('1785');
  expect(at('ESP-NATIONALIST',1938).flag?.title).toContain('1938');
 });
 it('distinguishes collective revolutionary authority, Napoleon, Stalin and rival French authorities',()=>{
  expect(names('FRA',1789)).toContain('Luis XVI');
  expect(names('FRA',1793)).toContain('Convención Nacional');
  expect(names('FRA',1812)).toContain('Napoleón');
  expect(names('USSR',1942)).toContain('Stalin');
  expect(names('FRA-VICHY',1942)).toContain('Pétain');
  expect(names('FRA-FREE',1942)).toContain('de Gaulle');
  expect(names('ROC',1942)).toContain('Chiang');
  expect(names('CHN-COMMUNIST',1942)).toContain('Mao');
 });
 it('does not infer colonial or future leaders from present sovereign-state profiles',()=>{
  expect(identityFor({identityKey:'IND',code:'IND',status:'colony'},1946,data,now).leaders).toHaveLength(0);
  const future=identityFor({identityKey:'USA'},2028,data,new Date(2028,1,1));
  expect(future.leaders).toHaveLength(0);expect(future.flag).toBeUndefined();
  expect(future.note).toContain('posteriores');
  expect(at('DEU',1789).leaders).toHaveLength(0);
 });
 it('renders real local image references and attribution within the integrated card',()=>{
  const html=identityMarkup({identityKey:'DEU',name:'Alemania nazi'},1942,data,'/Historicmap/');
  expect(html).toContain('historic-flag');expect(html).toContain('Adolf Hitler');
  expect(html).toContain('leader-portrait');expect(html).toContain('media-credit');
  expect(html).toContain('/Historicmap/media/');
  const media=JSON.parse(readFileSync(new URL('../public/media/manifest.json',import.meta.url),'utf8'));
  for(const m of media.entries){
   const bytes=readFileSync(new URL('../public/'+m.file,import.meta.url));
   expect(createHash('sha256').update(bytes).digest('hex'),m.file).toBe(m.sha256);
   expect(m.license).toBeTruthy();expect(m.url).toMatch(/^https:\/\/commons.wikimedia.org\//);
  }
 });
});
