/** Compile credited original GMT polygon margins, preserving geographic detail.
 * No scientific outlines or model ages are embedded in this generic writer. */
import{readFileSync,writeFileSync,mkdirSync}from'node:fs';import{dirname,resolve,join}from'node:path';import{fileURLToPath}from'node:url';import{createHash}from'node:crypto';import clipping from'polygon-clipping';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),read=p=>JSON.parse(readFileSync(p,'utf8')),sha=b=>createHash('sha256').update(b).digest('hex');
export function parseGMT(text){
 if(!text.includes('@Je4326'))throw Error('Expected explicitly declared WGS84 margins');
 const polygons=[];let polygon,ring,role='outer';
 const flush=()=>{if(!ring?.length)return;if(ring.length<3)throw Error('Incomplete margin');if(ring[0][0]!==ring.at(-1)[0]||ring[0][1]!==ring.at(-1)[1])ring.push([...ring[0]]);if(role==='outer'){polygon=[ring];polygons.push(polygon);}else{if(!polygon)throw Error('Hole without shell');polygon.push(ring);}ring=undefined;};
 for(const line of text.split(/\r?\n/)){
  if(line.startsWith('>')){flush();role='outer';ring=[];}
  else if(line.startsWith('# @H'))role='hole';
  else if(line.startsWith('# @P'))role='outer';
  else if(line.trim()&&!line.startsWith('#')){const p=line.trim().split(/\s+/).map(Number);if(p.length<2||!p.every(Number.isFinite)||Math.abs(p[0])>180.000001||Math.abs(p[1])>90)throw Error('Invalid geographic coordinate');ring??=[];ring.push(p.slice(0,2));}
 }flush();return polygons;
}
export function unwrapRing(ring,pole){
 const out=[[...ring[0]]];for(const p of ring.slice(1)){const prev=out.at(-1)[0];out.push([p[0]+360*Math.round((prev-p[0])/360),p[1]]);}
 const delta=out.at(-1)[0]-out[0][0];
 if(Math.abs(delta)>180){if(pole!==-90&&pole!==90)throw Error('Pole-enclosing ring without declared hemisphere');out.push([out.at(-1)[0],pole],[out[0][0],pole],[...out[0]]);}
 else out[out.length-1]=[...out[0]];
 return out;
}
/** Clip longitude strips and translate them; polar closure is a CRS operation,
 * not a newly inferred ice boundary. Keep all source islands and interior rings. */
export function splitAtDateline(polygons,pole){
 const output=[];for(const polygon of polygons){const shell=unwrapRing(polygon[0],pole),xs=shell.map(p=>p[0]),center=(Math.min(...xs)+Math.max(...xs))/2;
  const holes=polygon.slice(1).map(r=>{const a=unwrapRing(r,pole),v=a.map(p=>p[0]),offset=360*Math.round((center-(Math.min(...v)+Math.max(...v))/2)/360);return a.map(([x,y])=>[x+offset,y]);});
  const low=Math.floor((Math.min(...xs)+180)/360),high=Math.floor((Math.max(...xs)+180)/360);
  for(let k=low;k<=high;k++){const west=-180+360*k,east=180+360*k,box=[[[west,-90],[east,-90],[east,90],[west,90],[west,-90]]];const parts=clipping.intersection([shell,...holes],box);for(const p of parts)output.push(p.map(r=>r.map(([x,y])=>[x-360*k,y])));}
 }return output;
}
/** One physical ice extent per region: remove internal overlaps without simplifying outlines. */
export function dissolveMargins(polygons){return polygons.length?clipping.union(...polygons):[];}
export function civilYearFromBP(age){const y=1950-age;return y<=0?y-1:y;}
export function main(){
 const owner=join(root,'Tierra/Cuaternario/PaleoMIST-1.0'),meta=read(join(owner,'fuentes.json')),manifest=read(join(root,'public/data/manifest.json')),samples=[];
 for(const age of[...new Set(meta.entries.map(e=>e.ageBP))].sort((a,b)=>a-b)){
  const features=[];for(const e of meta.entries.filter(e=>e.ageBP===age)){const b=readFileSync(join(owner,e.file));if(sha(b)!==e.sha256)throw Error('Original margin checksum '+e.file);const original=parseGMT(b.toString('utf8')),coordinates=dissolveMargins(splitAtDateline(original,e.region==='Antarctica'?-90:undefined));features.push({type:'Feature',id:`ice-${e.region}-${age}`,geometry:{type:'MultiPolygon',coordinates},properties:{model:meta.model,region:e.region,ageBP:age,referenceYear:civilYearFromBP(age),source:meta.source,license:meta.license,canonicalFile:'Tierra/Cuaternario/PaleoMIST-1.0/'+e.file,originalSha256:e.sha256}});}
  const file=`ice-margins-paleomist-${age}.geojson`,raw=Buffer.from(JSON.stringify({type:'FeatureCollection',features})+'\n');writeFileSync(join(root,'public/data',file),raw);samples.push({file,ageBP:age,referenceYear:civilYearFromBP(age),features:features.length});manifest.entries=manifest.entries.filter(e=>e.file!==file);manifest.entries.push({file,format:'dated-ice-margin-model',source:meta.author,model:meta.model,url:meta.source,doi:meta.doi,license:meta.license,version:'Historicmap '+read(join(root,'package.json')).version,ageBP:age,referenceYear:civilYearFromBP(age),temporalStepYears:meta.temporalStepYears,features:features.length,bytes:raw.length,sha256:sha(raw),transform:'Original WGS84 GMT polygon shells/holes; longitude unwrapping, polar closure, clipping at the antimeridian and union of overlapping same-region ice components. No coordinate simplification; no sea-ice or mountain-glacier completeness claim.'});
 }
 const index={format:'ice-margin-model-index',model:meta.model,source:meta.source,article:meta.article,license:meta.license,referenceEpoch:1950,temporalStepYears:meta.temporalStepYears,consultationStart:civilYearFromBP(Math.max(...samples.map(s=>s.ageBP))),modelCoverageBP:meta.modelCoverageBP??[0,Math.max(...samples.map(s=>s.ageBP))],publishedMaxStepYears:Math.max(...samples.slice(1).map((s,i)=>s.ageBP-samples[i].ageBP)),samples,note:'Dated model references at2500-year steps, selected by nearest model age with older tie-break. Not annual observations, sea ice, all mountain glaciers, palaeocoasts or a simulation of yearly retreat.'};const file='ice-model-index.json',raw=Buffer.from(JSON.stringify(index)+'\n');writeFileSync(join(root,'public/data',file),raw);manifest.entries=manifest.entries.filter(e=>e.file!==file);manifest.entries.push({file,format:index.format,source:meta.author,url:meta.source,license:meta.license,version:'Historicmap '+read(join(root,'package.json')).version,records:samples.length,bytes:raw.length,sha256:sha(raw)});writeFileSync(join(root,'public/data/manifest.json'),JSON.stringify(manifest,null,2)+'\n');console.log('Ice samples',samples.length,'original margins',meta.entries.length);
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))main();
