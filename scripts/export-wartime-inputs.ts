/** Preparation only: export the same dated baseline and source controls as the app. */
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
import {historyAt,withHistoricalSupplements,normalizedName} from '../src/history';
import {politicalData} from '../src/political';
const root=process.cwd(),read=(f:string)=>JSON.parse(readFileSync(resolve(root,'public/data',f),'utf8'));
const topology=read('history.topojson'),profiles=read('profiles.json'),supplements=read('historical-supplements.geojson'),controls=read('historical-control.geojson');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p]:[string,any])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n),code] as [string,string])));
mkdirSync(resolve(root,'.cache/wartime'),{recursive:true});
for(let year=1940;year<=1944;year++){
 const base=politicalData(withHistoricalSupplements(historyAt(topology,year,names),year,supplements,historyAt(topology,1974,names)),year);
 const active=controls.features.filter((f:any)=>f.properties.start<=year&&f.properties.end>=year);
 const incorporation=controls.features.find((f:any)=>f.properties.controller==='DEU'&&f.properties.start===1938);
 active.push({...incorporation,properties:{...incorporation.properties,kind:'annexation-mask'}});
 writeFileSync(resolve(root,`.cache/wartime/input-${year}.json`),JSON.stringify({year,base,controls:{type:'FeatureCollection',features:active}}));
 console.log('Exported',year,base.features.length,'base territories;',active.length,'controls.');
}
