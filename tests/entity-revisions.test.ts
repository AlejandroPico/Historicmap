import{describe,it,expect,vi}from'vitest';
import{readFileSync,existsSync}from'node:fs';import{createHash}from'node:crypto';
import{identityFor,identityMarkup,type IdentityData}from'../src/identities';
import{annualData}from'../src/data';import{politicalData}from'../src/political';import{governmentFor}from'../src/governance';
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),ids:IdentityData=read('public/data/identities.json');
const identity=(key:string,y:number)=>identityFor({identityKey:key,name:key},y,ids);
vi.stubGlobal('fetch',async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200}));

describe('entity-owned historical corrections',()=>{
 it('uses historical Dutch tricolours, dated provincial stadholders and actual regencies',()=>{
  for(let y=1581;y<=1794;y++)expect(identity('DUTCH-REPUBLIC',y).flag,y.toString()).toBeDefined();
  expect(identity('DUTCH-REPUBLIC',1723).flag?.title).toBe('Statenvlag.svg');
  const l=identity('DUTCH-REPUBLIC',1723).leaders;
  expect(l.some(l=>l.person==='Q380949'&&l.role.includes('Frisia'))).toBe(true);
  expect(l.some(l=>l.person==='Q62593'&&l.role.includes('Regente'))).toBe(true);
  expect(l.some(l=>l.role.includes('todas las provincias'))).toBe(false);
  expect(identity('DUTCH-REPUBLIC',1755).leaders.some(l=>l.person==='Q239487')).toBe(true);
  expect(identity('DUTCH-REPUBLIC',1660).leaders.some(l=>l.name==='Johan de Witt')).toBe(true);
 });
 it('keeps the Río de la Plata symbols through1830 and separates all government phases',()=>{
  for(let y=1810;y<=1831;y++){const i=identity('RIO-DE-LA-PLATA',y);expect(i.flag,String(y)).toBeDefined();expect(i.leaders.length,String(y)).toBeGreaterThan(0);}
  expect(identity('RIO-DE-LA-PLATA',1810).flag?.referenceOnly).toBe(true);
  expect(identity('RIO-DE-LA-PLATA',1814).flag?.symbolLabel).toContain('Escudo');
  expect(identity('RIO-DE-LA-PLATA',1816).flag?.title).toContain('civil');
  expect(identity('RIO-DE-LA-PLATA',1830).flag?.title).toContain('Argentina');
  expect(identity('RIO-DE-LA-PLATA',1810).leaders.some(l=>l.person==='Q2361877')).toBe(true);
  expect(identity('RIO-DE-LA-PLATA',1812).leaders.some(l=>l.name==='Primer Triunvirato')).toBe(true);
  expect(identity('RIO-DE-LA-PLATA',1813).leaders.some(l=>l.name==='Segundo Triunvirato')).toBe(true);
  expect(identity('RIO-DE-LA-PLATA',1819).leaders.some(l=>l.person==='Q959624')).toBe(true);
  expect(identity('RIO-DE-LA-PLATA',1824).leaders.some(l=>l.person==='Q1710498'&&l.role.includes('provincial'))).toBe(true);
  expect(identity('RIO-DE-LA-PLATA',1827).leaders.map(l=>l.person)).toEqual(expect.arrayContaining(['Q188891','Q441072']));
  expect(identity('RIO-DE-LA-PLATA',1830).leaders.some(l=>l.role==='Sin ejecutivo nacional común')).toBe(true);
  expect(governmentFor({identityKey:'RIO-DE-LA-PLATA'},1813).tags).toContain('collective');
  expect(governmentFor({identityKey:'RIO-DE-LA-PLATA'},1819).tags).toContain('directorial');
  expect(governmentFor({identityKey:'RIO-DE-LA-PLATA'},1830).tags).toContain('confederal');
  expect(governmentFor({identityKey:'RIO-DE-LA-PLATA'},1830).tags).not.toContain('presidential-republic');
 });
 it('distinguishes colonial title, national ensigns, union ensigns and dated Paraguayan variants',()=>{
  const louisiana=identity('HIST-Q5501836',1802).flag!;expect(louisiana.title).toContain('France');expect(louisiana.presentationNote).toContain('administración española');expect(louisiana.title).not.toContain('royal');
  expect(identity('HIST-Q5501836',1750).flag?.symbolLabel).toContain('real');
  for(let y=1815;y<=1904;y++)expect(identity('HIST-Q62589',y).flag,String(y)).toBeDefined();
  expect(identity('HIST-Q62589',1830).flag?.title).toContain('1815');expect(identity('HIST-Q62589',1850).flag?.title).toContain('1844');
  for(let y=1811;y<=2026;y++)expect(identity('PRY',y).flag,String(y)).toBeDefined();
  expect(identity('PRY',1830).flag?.title).toContain('1826-1842');expect(identity('PRY',1850).flag?.title).toContain('1842');expect(identity('PRY',2026).flag?.title).toBe('Flag of Paraguay.svg');
 });
 it('labels retrospective heraldry without asserting later emblems were contemporary flags',()=>{
  for(const[key,y]of [['URGELL-COUNTY',1146],['HIST-Q1541699',1146],['PRT',1146],['HIST-Q154667',1100],['HIST-Q151536',1291],['MUSCOVY',1300],['HIST-Q269109',1291]] as const){
   const flag=identity(key,y).flag!;expect(flag,key).toBeDefined();expect(flag.referenceOnly,key).toBe(true);expect(flag.evidenceDate).toBeTruthy();
   const markup=identityMarkup({identityKey:key,name:key},y,ids,'/','header');expect(markup).toContain('Referencia retrospectiva');expect(markup).not.toContain('Símbolo al');
  }
  expect(identity('HIST-Q1514510',1146).flag?.file).toBe(identity('URGELL-COUNTY',1146).flag?.file);
  expect(identity('URGELL-COUNTY',1250).flag?.referenceOnly).not.toBe(true);expect(identity('HIST-Q154667',1400).flag?.referenceOnly).not.toBe(true);
  expect(identity('HIST-Q45670',1915).flag).toBeUndefined();expect(identity('IBERIAN-UNION',1620).flag?.symbolLabel).toContain('monarca común');expect(identity('PRT',1620).flag?.title).toContain('1616');
  for(let y=1139;y<=1910;y++)expect(identity('PRT',y).flag,String(y)).toBeDefined();
 });
 it('resolves symbols through the actual political map and keeps canonical source files inside entity folders',async()=>{
  for(const[y,key]of [[1802,'HIST-Q5501836'],[1146,'HIST-Q1514510'],[1146,'HIST-Q1541699'],[1590,'IBERIAN-UNION'],[1100,'HIST-Q154667'],[1723,'DUTCH-REPUBLIC'],[1830,'RIO-DE-LA-PLATA'],[1830,'HIST-Q62589'],[1146,'PRT'],[1291,'HIST-Q151536']] as const){
   const world=politicalData(await annualData(y),y);const f=world.features.find(f=>identityFor(f.properties!,y,ids).key===key);expect(f,key).toBeDefined();expect(identityFor(f!.properties!,y,ids).flag,key).toBeDefined();
  }
  const index=read('Países/indice.json').entities;
  let revisions=0;
  for(const e of index){const file=`Países/${e.folder}/revision-historica.json`;if(!existsSync(file))continue;revisions++;const r=read(file);expect(r.key).toBe(e.key);
   for(const s of r.symbols){expect(s.media.canonicalFile).toMatch(new RegExp('^Países/'+e.folder+'/simbolos/'));expect(createHash('sha256').update(readFileSync(s.media.canonicalFile)).digest('hex')).toBe(s.media.sha256);}
   for(const l of r.leaders)if(l.portrait){expect(l.portrait.canonicalFile).toContain(`/retratos/`);expect(existsSync(l.portrait.canonicalFile)).toBe(true);}
   for(const correction of r.portraitCorrections??[]){const m=correction.portrait;expect(m.canonicalFile).toMatch(new RegExp('^Países/'+e.folder+'/retratos/'));expect(createHash('sha256').update(readFileSync(m.canonicalFile)).digest('hex')).toBe(m.sha256);expect(ids.countries[e.key].leaders.filter(l=>l.person===correction.person).every(l=>l.portrait?.file===m.file)).toBe(true);}
   const entity=read(`Países/${e.folder}/entidad.json`);expect(entity.symbolReferences).toEqual(ids.countries[e.key].symbolReferences??[]);
  }
  expect(revisions).toBe(15);
 },60000);
});
