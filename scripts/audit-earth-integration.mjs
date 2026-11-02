/** Offline inventory of the six Earth phases. Counts and unresolved gaps are not scientific certification. */
import {readFile,writeFile,mkdir}from'node:fs/promises';
import{createHash}from'node:crypto';
const root=new URL('../',import.meta.url),read=async p=>JSON.parse(await readFile(new URL(p,root),'utf8'));
const hash=b=>createHash('sha256').update(b).digest('hex');
const paths=['Tierra/Precambrico/enciclopedia.json','Tierra/Fanerozoico/enciclopedia.json','Tierra/Cuaternario/enciclopedia.json','public/data/human-knowledge.json'];
const content=await Promise.all(paths.map(read)),articles=content.flatMap(c=>c.articles);
const units=(await read('Tierra/Cronologia/ics-2026-06.json')).units,human=(await read('Tierra/Cronologia/edades-humanas.json')).units;
const reviewFiles=['Tierra/Precambrico/revision-video.json','Tierra/Fanerozoico/revision-video.json','Tierra/Humanidad/revisiones/parte5/revision-video.json'];
const reviews=(await Promise.all(reviewFiles.map(read))).flatMap(r=>r.events);
const events=[...new Map(reviews.map(e=>[e.videoId,e])).values()];
const ids=new Set([...articles.map(a=>a.id),...units.map(u=>'geo-'+u.id),...human.map(u=>'human-'+u.id),...events.map(e=>e.videoId)]);
if(ids.size!==articles.length+units.length+human.length+events.length)throw Error('Duplicate encyclopedia identity');
const sources={...(await read('Tierra/Precambrico/fuentes.json')).sources,...(await read('Tierra/Fanerozoico/fuentes.json')).sources,...content[3].sources,...content[2].sources};
for(const a of articles){for(const id of a.related)if(!ids.has(id))throw Error('Broken internal relation '+a.id+':'+id);for(const id of a.sourceIds)if(!sources[id])throw Error('Missing reference '+a.id+':'+id);}
for(const e of events){if(!ids.has(e.article))throw Error('Unresolved video review '+e.videoId);for(const id of e.sourceIds)if(!sources[id])throw Error('Missing event reference '+id);}
for(const [id,s]of Object.entries(sources))if(!/^https:\/\//.test(s.url))throw Error('Invalid reference URL '+id);
const media=[...(await read('Tierra/Precambrico/medios.json')).images,...(await read('Tierra/Fanerozoico/medios.json')).images,...content[3].images];
for(const m of media){const b=await readFile(new URL('public/'+m.file,root));if(hash(b)!==m.sha256||b.length!==m.bytes)throw Error('Media integrity '+m.file);for(const id of m.articleIds)if(!ids.has(id))throw Error('Media association '+id);}
const taxa=(await read('public/data/human-lineages.json')).taxa;
const ice=await read('public/data/ice-synthesis-index.json');
const inventory=await read('Tierra/Investigacion/parte-1/inventario-video.json');
const missingVideo=inventory.events.filter(e=>!events.some(r=>r.videoId===e.id));if(missingVideo.length)throw Error('Unaccounted audiovisual candidates '+missingVideo.map(e=>e.id));
const countBy=(rows,key)=>Object.fromEntries([...new Set(rows.map(r=>r[key]))].sort().map(v=>[v,rows.filter(r=>r[key]===v).length]));
const report={schemaVersion:1,version:'0.56.0',scope:'Inventario reproducible de integración, no verificación historiográfica mundial ni validación científica individual de todas las observaciones del vídeo.',
 encyclopedia:{authoredArticles:articles.length,geologicalUnits:units.length,humanChronologies:human.length,regularEntries:articles.length+units.length+human.length,archivalCandidates:events.length,sourceRecords:Object.keys(sources).length,internalRelationsChecked:articles.reduce((n,a)=>n+a.related.length,0),sourceUrlsChecked:'Sintaxis HTTPS y registro local, no disponibilidad HTTP ni vigencia editorial de cada página.'},
 media:{originals:media.length,humanOriginals:content[3].images.length,allBinaryChecksumsVerified:true,lineagesWithoutDedicatedPhoto:taxa.filter(t=>!content[3].images.some(m=>m.articleIds.includes('hominin-'+t.key))).map(t=>({key:t.key,name:t.name,classification:t.classification}))},
 humanity:{documentaryEntries:taxa.length,withIndependentAreas:taxa.filter(t=>t.regions.length).length,areaWindows:(await read('public/data/human-ranges.geojson')).features.length,fossilPoints:(await read('public/data/hominin-sites.geojson')).features.length,co2Observations:(await read('public/data/ice-core-co2.json')).rows.length},
 ice:{olderWindows:ice.samples.length,olderVariants:ice.samples.reduce((n,s)=>n+1+s.uncertaintyFiles.length,0),scope:'Hemisferio norte; PaleoMIST conserva precedencia hasta80ka BP1950. No extrapolar huecos, inferir Antártida, hielo marino o espesores.',windows:ice.samples.map(s=>({label:s.folder,youngestKa:s.youngestKa,oldestKa:s.oldestKa,autoVisible:s.autoVisible}))},
 audiovisual:{observedCandidates:inventory.events.length,accountedFor:events.length,dispositions:countBy(events,'disposition'),individualScientificValidationComplete:false},
 remaining:['No paleocostas cuaternarias detalladas ni puente terrestre calculado a partir del hielo.','Las escenas de superficie antiguas son ilustraciones documentadas, no reconstrucciones espectrales o paleogeografías exactas.','No curva publicada completa de temperatura o todos los gases desde4,54Ga; escenarios audiovisuales separados de modelos.','Las áreas de homininos son envolventes interpretativas, no rutas exactas ni evidencia de guerra.','Ampliar monografías, fotografías y contraste individual de acontecimientos; un registro en el archivo no los valida.']};
const target='Tierra/Investigacion/parte-6/integracion.json',bytes=JSON.stringify(report,null,2)+'\n';
if(process.argv.includes('--check')){if(await readFile(new URL(target,root),'utf8')!==bytes)throw Error('Stale integration inventory');}
else{await mkdir(new URL('Tierra/Investigacion/parte-6/',root),{recursive:true});await writeFile(new URL(target,root),bytes,'utf8');}
console.log(`Integration: ${articles.length} articles, ${units.length} units, ${events.length} accounted candidates, ${media.length} credited originals; ${report.media.lineagesWithoutDedicatedPhoto.length} photo gaps retained.`);
