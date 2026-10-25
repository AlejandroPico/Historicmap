/** Exact-source transfer, avoiding fragments from intersecting different coastlines. */
import {readFileSync,writeFileSync} from 'node:fs';
import {historyAt,normalizedName} from '../src/history';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8'));
const topology=read('history.topojson'),profiles=read('profiles.json');
const names=new Map<string,string>(Object.entries<any>(profiles.countries).flatMap(([code,p])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
const features=[1898,1899].map(year=>{
 const f=historyAt(topology,year,names).features.find(f=>f.properties?.originalName==='Hawaii');
 if(!f)throw Error('Missing dated Hawaii source '+year);
 const uid='hawaii-incorporation-'+year;
 return {...f,id:uid,properties:{...f.properties,uid,controller:'USA',identityKey:'USA',relation:'incorporation',kind:'war',start:year,end:year,
  name:'Incorporación de Hawái a Estados Unidos',geometrySource:'https://icr.ethz.ch/data/cshapes/',
  source:'https://www.archives.gov/milestone-documents/joint-resolution-for-annexing-the-hawaiian-islands',
  note:'Transferencia12/8/1898 bajo la resolución de anexión, distinta de la fecha6/7 del registroCShapes. Se usa exactamente la geometríaCShapes fechada del territorio, sin cruzarla con la referenciaCliopatria anterior. Incorporación territorial, no admisión como Estado federado. Sin franjas de ocupación.'}};
});
writeFileSync('public/data/historical-1880-control.geojson',JSON.stringify({type:'FeatureCollection',features,metadata:{license:'CShapes2.0 CC BY-NC-SA4.0',method:'Exact dated source geometry transfer; source topology unchanged.'}})+'\n');
console.log('Prepared exact dated Hawaii incorporations1898/1899.');
