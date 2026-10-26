import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {describe,it,expect} from 'vitest';
import {identityFor,identityKey,identityMarkup,type IdentityData} from '../src/identities';
import {historyAt,normalizedName,type HistoryTopology} from '../src/history';
import {politicalData} from '../src/political';
const data:IdentityData=JSON.parse(readFileSync(new URL('../public/data/identities.json',import.meta.url),'utf8'));
const now=new Date(2026,9,22,12);
const at=(key:string,year:number)=>identityFor({identityKey:key,name:key},year,data,now);
const names=(key:string,year:number)=>at(key,year).leaders.map(l=>l.name).join(' / ');

describe('dated flags and political authorities',()=>{
 it('does not recover rejected generic offices when consolidating a reviewed authority',()=>{
  const leader={person:'TEST',name:'Reviewed president',start:'1963-10-01',end:'1966-01-16',source:'test',precision:11};
  const fixture:IdentityData={retrieved:'2026-10-22',license:'test',source:'test',countries:{TEST:{qid:'',name:'Test',flags:[],leaders:[{...leader,role:'Jefatura del Estado'},{...leader,role:'Jefatura del Gobierno'},{...leader,role:'Presidente parlamentario',curated:true}]}}};
  expect(identityFor({identityKey:'TEST'},1964,fixture,now).leaders.map(l=>l.role)).toEqual(['Presidente parlamentario']);
  const nigeria=at('NGA',1963).leaders;
  expect(nigeria.find(l=>l.person==='Q181782')?.role).toMatch(/jefatura del Estado/);
  expect(nigeria.find(l=>l.person==='Q181782')?.role).not.toMatch(/Gobierno/);
  expect(nigeria.some(l=>l.person==='Q335684'&&/Gobierno/.test(l.role))).toBe(true);
 });
 it('never resolves an empty or unknown identifier to a Spanish faction',()=>{
  for(const p of [{},{name:'Brazil'},{name:'Unknown territory',wikidata:''},{code:'-99'},{identityKey:'not-a-country',wikidata:'not-a-qid'}]){
   expect(identityKey(p,1947,data)).toBe('');
   expect(identityFor(p,1947,data,now).name).toBeUndefined();
  }
  const topology:HistoryTopology=JSON.parse(readFileSync(new URL('../public/data/history.topojson',import.meta.url),'utf8'));
  const profiles=JSON.parse(readFileSync(new URL('../public/data/profiles.json',import.meta.url),'utf8'));
  const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
  for(const year of [1937,1947,1976,2000,2026]){
   const raw=year===2026?JSON.parse(readFileSync(new URL('../public/data/countries.geojson',import.meta.url),'utf8')):historyAt(topology,year,names);
   const world=politicalData(raw,year);
   for(const f of world.features){
    const key=identityKey(f.properties!,year,data);
    if(key.startsWith('ESP'))expect(String(f.properties!.originalName??f.properties!.name)).toMatch(/Spain|España/);
   }
   const brazil=world.features.find(f=>f.properties?.code==='BRA');
   expect(brazil,`Brazil ${year}`).toBeDefined();
   expect(identityFor(brazil!.properties!,year,data,now).key).toBe('BRA');
  }
 });
 it('includes short terms, both sides of handovers, and repeat mandates inside one year',()=>{
  expect(names('USA',2025)).toContain('Biden');expect(names('USA',2025)).toContain('Trump');
  expect(names('ESP',1981)).toContain('Suárez');expect(names('ESP',1981)).toContain('Calvo-Sotelo');
  const country={qid:'Q1',name:'Test',flags:[],leaders:[
   {person:'Q2',name:'First',role:'Primer ministro',start:'2026-01-01',end:'2026-02-01',source:'https://example.org'},
   {person:'Q3',name:'Second',role:'Primer ministro',start:'2026-02-02',end:'2026-07-01',source:'https://example.org'},
   {person:'Q2',name:'First',role:'Primer ministro',start:'2026-07-02',end:'2026-10-22',source:'https://example.org'},
   {person:'Q4',name:'Future',role:'Primer ministro',start:'2026-12-01',end:'2026-12-31',source:'https://example.org'}]};
  expect(identityFor({code:'TEST'},2026,{...data,countries:{TEST:country}},now).leaders.map(l=>l.start)).toEqual(['2026-07-02','2026-02-02','2026-01-01']);
 });
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
 it('closes obsolete Nauru mandates and retains the Korean prime-minister handover in 2026',()=>{
  expect(at('NRU',2026).leaders.map(l=>l.person)).toEqual(['Q58096']);
  expect(at('NRU',2012).leaders.some(l=>l.person==='Q57543')).toBe(true);
  const korea=at('KOR',2026).leaders;
  expect(korea.some(l=>l.person==='Q12587400')).toBe(true);
  expect(korea.some(l=>l.person==='Q55082182')).toBe(true);
  expect(korea.find(l=>l.person==='Q12587400')?.portrait).toBeDefined();
  expect(at('FRA',2026).leaders.find(l=>l.person==='Q20089181')?.start).toBe('2025-10-10');
  expect(at('FRA',2025).leaders.filter(l=>l.person==='Q20089181')).toHaveLength(2);
 });
 it('preserves authentic historical German flags and leaves the occupation interval without a national flag',()=>{
  expect(at('DEU',1942).flag?.title).toBe('Flag of Germany (1935–1945).svg');
  expect(names('DEU',1942)).toContain('Hitler');
  expect(at('DEU',1946).flag).toBeUndefined();
  expect(at('DEU',1946).leaders.map(l=>l.person)).toEqual(['COLLECTIVE-DEU-ALLIED-OCCUPATION']);
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
  expect(at('ESP-NATIONALIST',1936).flag?.title).toBe('Bandera del bando sublevado (1936-1938).svg');
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
   expect(m.license).toBeTruthy();expect(m.url).toMatch(/^https:\/\/(commons.wikimedia.org|www.srbija.gov.rs)\//);
  }
  // Full-catalogue byte verification runs in data:verify. This unit test
  // checks the actual card's images, avoiding a second 120 MB disk sweep.
  const selected=at('DEU',1942);
  for(const m of [selected.flag,...selected.leaders.map(l=>l.portrait)].filter(Boolean)){
   const bytes=readFileSync(new URL('../public/'+m!.file,import.meta.url));
   expect(createHash('sha256').update(bytes).digest('hex'),m!.file).toBe(m!.sha256);
  }
 },20000);
 it('preserves the complete official meeting photograph and links its restrictive license',()=>{
  const leader=at('MOZ',2026).leaders.find(l=>l.person==='Q6761049');
  expect(leader?.portrait?.display).toBe('full-frame');
  expect(leader?.portrait?.license).toBe('CC BY-NC-ND 3.0 RS');
  const html=identityMarkup({code:'MOZ',name:'Mozambique'},2026,data,'/');
  expect(html).toContain('full-frame-photo');expect(html).toContain('Fotografía íntegra');
  expect(html).toContain('https://creativecommons.org/licenses/by-nc-nd/3.0/rs/deed.en');
  expect(html).toContain('Slobodan Miljević');
 });
});
