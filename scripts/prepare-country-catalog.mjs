/** Human-readable entity inventory; geometry and licensed media stay in their original collections. */
import {readFileSync,writeFileSync as writeFileRawSync,mkdirSync,existsSync,readdirSync,unlinkSync,rmdirSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),dir=resolve(root,'Países');
function writeFileSync(path,content){
 // Avoid rewriting thousands of identical files in synced Windows folders.
 for(let attempt=0;attempt<4;attempt++)try{if(existsSync(path)&&readFileSync(path,'utf8')===content)return;writeFileRawSync(path,content);return;}catch(error){if(attempt===3||!['EBUSY','EPERM','EACCES','UNKNOWN'].includes(error.code))throw error;Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,50*(attempt+1));}
}
const read=f=>JSON.parse(readFileSync(resolve(root,'public/data',f),'utf8'));
const identities=read('identities.json'),profiles=read('profiles.json'),manifest=read('manifest.json'),portraitSeries=read('portrait-series.json');
const entities=new Map(),qids=new Map(),names=new Map();
// Entity-owned inputs keep their folder even when a later phase changes its label.
const canonicalFolders=new Map();
if(existsSync(resolve(dir,'indice.json')))for(const e of JSON.parse(readFileSync(resolve(dir,'indice.json'),'utf8')).entities)canonicalFolders.set(e.key,e.folder);
function retainFolder(key,file){const parts=String(file).split('/');if(parts[0]!=='Países'||!parts[1]||parts[1]==='..'||parts[1].includes('\\'))throw Error('Invalid canonical folder '+file);if(!canonicalFolders.has(key))canonicalFolders.set(key,parts[1]);}
const norm=s=>String(s).normalize('NFD').replace(/\p{Diacritic}/gu,'').toLowerCase().trim();
function add(key,name,qid=''){
 if(!entities.has(key))entities.set(key,{key,name,qid,aliases:new Set([name]),records:[]});
 return entities.get(key);
}
for(const [key,c] of Object.entries(identities.countries)){
 add(key,c.name,c.qid).identity=c;
 if(c.qid&&!qids.has(c.qid))qids.set(c.qid,key);
 for(const name of [c.name,profiles.countries[key]?.englishName])if(name)names.set(norm(name),key);
}
function record(p,file,recordId){
 const name=p.originalName??p.country_name??p.name;
 if(!name||['Masa continental','Continente','Tierra','Ocean','Land'].includes(name))return;
 const qid=p.wikidata??'',key=entities.has(p.identityKey)?p.identityKey:/^Q\d+$/.test(qid)?qids.get(qid)||qid:names.get(norm(name))||'territorio-'+createHash('sha256').update(norm(name)).digest('hex').slice(0,12);
 const e=add(key,name,qid);e.aliases.add(name);
 e.records.push({file,recordId,start:p.start??null,end:p.end??null,name,status:p.status??p.politicalStatus??null});
}
if(manifest.entries.some(e=>e.file==='cultural-regions.geojson'))for(const f of read('cultural-regions.geojson').features){
 const p=f.properties,key=p.ownerKey,e=add(key,p.name);
 retainFolder(key,p.canonicalFile);
 e.culturalRecords??=[];e.culturalRecords.push({file:'cultural-regions.geojson',recordId:f.id,contextKey:p.contextKey,start:p.start,end:p.end,sourceYear:p.sourceYear,canonicalFile:p.canonicalFile});
 if(p.kind==='cultural-region')for(const name of p.originalNames){e.aliases.add(name);names.set(norm(name),key);}
}
if(manifest.entries.some(e=>e.file==='cultural-index.json'))for(const r of read('cultural-index.json').excluded??[]){const e=add(r.ownerKey,r.name);retainFolder(r.ownerKey,r.file);e.culturalReviews??=[];e.culturalReviews.push(r);}
for(const g of read('history.topojson').objects.countries.geometries)record(g.properties,'history.topojson',g.properties.fid);
for(const entry of manifest.entries.filter(e=>/^(early-modern-900|early-modern-1000|early-modern-1100|early-modern-1200|early-modern-1300|early-modern-1400|early-modern-1500|early-modern-1600|early-modern-1700|early-modern|historical-control|historical-1880-control|historical-1880-supplements|pacific-references|ukraine-control-2022|central-europe-1939|spanish-civil-war|recent-control|historical-supplements|countries|world_.*)\.geojson$/.test(e.file))){
 const d=read(entry.file);for(const [i,f] of d.features.entries())record(f.properties,entry.file,f.id??i);
}
if(manifest.entries.some(e=>e.file==='wartime-partitions.json'))for(const [year,p] of Object.entries(read('wartime-partitions.json').years))for(const f of p.territories.features)record({...f.properties,start:year+'-01-01',end:year+'-12-31'},'wartime-partitions.json',`${year}:${f.id}`);
mkdirSync(dir,{recursive:true});const index=[];
for(const e of [...entities.values()].sort((a,b)=>a.key.localeCompare(b.key))){
 const slug=e.name.normalize('NFD').replace(/\p{Diacritic}/gu,'').replace(/[^a-zA-Z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,65)||'entidad';
 const folder=canonicalFolders.get(e.key)||e.key+'-'+slug,path=resolve(dir,folder);mkdirSync(path,{recursive:true});
 const c=e.identity,flags=c?.flags??[],leaders=c?.leaders??[];
 const output={key:e.key,name:e.name,qid:e.qid,aliases:[...e.aliases].sort(),generatedBy:'scripts/prepare-country-catalog.mjs',
  scope:'Inventario de los registros disponibles; no certifica continuidad ni exactitud histórica exhaustiva.',
  sourceIdentity:c?{file:'../../public/data/identities.json',key:e.key}:null,
  flags,symbolReferences:c?.symbolReferences??[],leaders,portraitVariants:portraitSeries.records.filter(r=>leaders.some(l=>l.person===r.person)),territorialRecords:e.records,...(e.culturalRecords?.length?{culturalRecords:e.culturalRecords}:{}),...(e.culturalReviews?.length?{culturalReviews:e.culturalReviews}:{}),
  relatedData:['../../public/data/country-history.json','../../public/data/historical-context.json','../../public/data/affiliations.json'],
  mediaRoot:'../../public/',extensionFile:'recursos.json'};
 writeFileSync(resolve(path,'entidad.json'),JSON.stringify(output,null,2)+'\n');
 const resourceFile=resolve(path,'recursos.json');
 if(!c&&existsSync(resourceFile)){
  const old=JSON.parse(readFileSync(resourceFile,'utf8'));
  if(old.key===e.key&&old.resources?.length===0&&Object.keys(old).length===2)unlinkSync(resourceFile);
 }
 if(c&&!existsSync(resourceFile))writeFileSync(resourceFile,JSON.stringify({key:e.key,resources:[]},null,2)+'\n');
 const custom=existsSync(resourceFile)?JSON.parse(readFileSync(resourceFile,'utf8')):{key:e.key,resources:[]};
 if(custom.key!==e.key||!Array.isArray(custom.resources))throw Error('Invalid resources: '+folder);
 const declared=new Set();
 for(const r of custom.resources){
  if(!/^[\w.-]+\.(mp3|ogg|wav|m4a|pdf)$/i.test(r.file)||!r.title||!r.source||!r.license||!r.start||!r.end||r.start>r.end)throw Error('Resource metadata missing/invalid: '+folder);
  if(declared.has(r.file)||!existsSync(resolve(path,'archivos',r.file)))throw Error('Duplicate/missing resource: '+folder+'/'+r.file);
  declared.add(r.file);
 }
 if(existsSync(resolve(path,'archivos')))for(const f of readdirSync(resolve(path,'archivos')))if(!declared.has(f))throw Error('Resource requires source, license and dates: '+folder+'/'+f);
 index.push({key:e.key,name:e.name,folder,flags:flags.length,symbolReferences:c?.symbolReferences?.length??0,leaders:leaders.length,territorialRecords:e.records.length});
}
writeFileSync(resolve(dir,'indice.json'),JSON.stringify({entities:index},null,2)+'\n');
// Remove only our obsolete generated views after a folder label changes.
// Any custom file or nonempty extension makes the old directory user-owned.
const folders=new Set(index.map(e=>e.folder));
for(const old of readdirSync(dir,{withFileTypes:true}).filter(d=>d.isDirectory()&&!folders.has(d.name))){
 const path=resolve(dir,old.name),files=readdirSync(path),entityFile=resolve(path,'entidad.json');
 if(!files.every(f=>['entidad.json','recursos.json'].includes(f))||!existsSync(entityFile))continue;
 const entity=JSON.parse(readFileSync(entityFile,'utf8'));
 if(entity.generatedBy!=='scripts/prepare-country-catalog.mjs')continue;
 const resources=resolve(path,'recursos.json');
 if(existsSync(resources)){
  const extension=JSON.parse(readFileSync(resources,'utf8'));
  if(extension.resources?.length!==0||Object.keys(extension).length!==2)continue;
  unlinkSync(resources);
 }
 unlinkSync(entityFile);rmdirSync(path);
}
writeFileSync(resolve(dir,'INDICE.md'),'# Entidades del atlas\n\nInventario generado de países, reinos, imperios y territorios presentes en los conjuntos locales. Una carpeta no acredita una ficha completa. Véase [cómo ampliar](README.md).\n\n| Entidad | Clave | Banderas | Referencias retrospectivas | Mandatos | Registros territoriales |\n| --- | --- | ---: | ---: | ---: | ---: |\n'+index.map(e=>`| [${e.name.replaceAll('|','/')}](./${e.folder}/entidad.json) | ${e.key} | ${e.flags} | ${e.symbolReferences} | ${e.leaders} | ${e.territorialRecords} |`).join('\n')+'\n');
console.log('Entity folders:',index.length,'; historical identities:',Object.keys(identities.countries).length);
