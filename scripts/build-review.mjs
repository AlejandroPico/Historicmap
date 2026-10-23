import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {periodsAt,historicName} from '../src/history.ts';
const json=async file=>JSON.parse(await readFile(new URL('../public/data/'+file,import.meta.url)));
const [topology,early,controls,spanish,supplements,recentControl]=await Promise.all(['history.topojson','early-modern.geojson','historical-control.geojson','spanish-civil-war.geojson','historical-supplements.geojson','recent-control.geojson'].map(json));
const currentYear=new Date().getFullYear();
let previous=new Set();
const rows=[];
for(let year=1789;year<=currentYear;year++){
 if(year>2019){rows.push(`| ${year} | 258 | Natural Earth, referencia incorporada en 2026 | Sin serie independiente de control efectivo para este año. |`);continue;}
 const clio=year<1886;
 const active=clio?early.features.filter(f=>f.properties.start<=year&&f.properties.end>=year).map(f=>({id:f.id,name:f.properties.name})):periodsAt(topology,year).map(g=>({id:g.properties.fid,name:historicName(g.properties,year)}));
 const reference=year>=1950?supplements.features.filter(f=>f.properties.start<=`${year}-12-31`&&f.properties.end>=`${year}-12-31`):[];
 active.push(...reference.map(f=>({id:f.id,name:f.properties.name+' · contorno de referencia'})));
 if(!active.length||new Set(active.map(p=>p.id)).size!==active.length)throw Error(`Missing or duplicate records in ${year}`);
 const changed=active.filter(p=>!previous.has(p.id));
 const checksum=createHash('sha256').update(active.map(p=>p.id).sort().join(',')).digest('hex').slice(0,12);
 const changes=year===1789?'Estado inicial':changed.length?changed.map(p=>p.name).join(', '):'Sin cambio de registro en la fuente; no prueba ausencia de cambios históricos';
 const control=[...controls.features,...spanish.features,...recentControl.features].filter(f=>f.properties.start<=year&&f.properties.end>=year);
 rows.push(`| ${year} | ${active.length} | ${clio?'Cliopatria · síntesis anual':'CShapes · 31 diciembre'}${reference.length?` + ${reference.length} contornos de referencia`:''} · ${checksum} | ${changes.replaceAll('|','/')} ${control.length?`**+ ${control.length} registros de control/guerras civiles.**`:''} |`);
 previous=new Set(active.map(p=>p.id));
}
const method=await readFile(new URL('../docs/REVIEW-METHOD.md',import.meta.url),'utf8');
await writeFile(new URL('../docs/ANNUAL-REVIEW.md',import.meta.url),`# Revisión anual 1789–${currentYear}\n\n${method}\n\n## Inventario año por año\n\n| Año | Territorios | Fuente / huella | Cambios y estado de revisión |\n| --- | ---: | --- | --- |\n${rows.join('\n')}\n`);
console.log(`Audited ${currentYear-1788} annual selections, 1789–${currentYear}; source limits recorded.`);
