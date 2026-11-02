import type {FeatureCollection,Feature,Polygon,MultiPolygon} from 'geojson';
import pc from 'polygon-clipping';
import catalogue from '../public/data/human-lineages.json' with {type:'json'};
import {escapeHtml as esc} from './profiles';
import {formatYear} from './time';
import{humanPhoto}from'./human-knowledge';
export const lineageCatalogue=catalogue;
const empty=():FeatureCollection=>({type:'FeatureCollection',features:[]});
const cache=new Map<string,{areas:FeatureCollection;overlaps:FeatureCollection}>();
const coords=(f:Feature)=>f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
/** Full source areas remain selectable; disjoint intersection cells carry only a visual coexistence pattern. */
export function distributionsAt(raw:FeatureCollection,year:number){
 const active=raw.features.filter(f=>f.properties!.start<=year&&year<=f.properties!.end);
 if(!active.length)return{areas:empty(),overlaps:empty()};
 const key=active.map(f=>f.id).join('|');const previous=cache.get(key);if(previous)return previous;
 const groups=new Map<string,Feature[]>();for(const f of active){const k=f.properties!.lineage;groups.set(k,[...(groups.get(k)??[]),f]);}
 const areas:Feature[]=[];
 for(const[k,rows]of [...groups].sort(([a],[b])=>a.localeCompare(b))){const [first,...rest]=rows.map(coords),geometry=pc.union(first as any,...rest as any[]),p=rows[0].properties!;
  areas.push({type:'Feature',id:'distribution-'+k+'@'+rows.map(f=>f.id).join('.'),geometry:{type:'MultiPolygon',coordinates:geometry},properties:{...p,groupIds:[p.group],regionLabels:[...new Set(rows.map(f=>f.properties!.regionLabel))],phaseSources:[...new Set(rows.map(f=>f.properties!.source))],start:Math.min(...rows.map(f=>f.properties!.start)),end:Math.max(...rows.map(f=>f.properties!.end)),taxonGroups:[p.group],originalNames:[p.name],coexistence:[]}});
 }
 type Cell={geometry:any;members:string[]};let cells:Cell[]=[];
 for(const f of areas){const geom=coords(f);let remainder:any=geom;const next:Cell[]=[];
  for(const c of cells){const overlap=pc.intersection(c.geometry,geom as any),outside=pc.difference(c.geometry,geom as any);if(outside.length)next.push({...c,geometry:outside});if(overlap.length)next.push({geometry:overlap,members:[...c.members,f.properties!.lineage]});remainder=pc.difference(remainder,c.geometry);}
  if(remainder.length)next.push({geometry:remainder,members:[f.properties!.lineage]});cells=next;
 }
 const overlaps:Feature[]=cells.filter(c=>c.members.length>1).map((c,i)=>({type:'Feature',id:'shared-'+i+'@'+key,geometry:{type:'MultiPolygon',coordinates:c.geometry},properties:{members:c.members,groups:c.members.map(k=>areas.find(f=>f.properties!.lineage===k)!.properties!.group),colors:c.members.map(k=>areas.find(f=>f.properties!.lineage===k)!.properties!.color),meaning:'Solapamiento de reconstrucciones; no prueba de guerra o dominio'}}));
 // Derive names from actual intersection cells, never mere shared chronology.
 for(const f of areas)f.properties!.coexistence=[...new Set(overlaps.filter(o=>o.properties!.members.includes(f.properties!.lineage)).flatMap(o=>o.properties!.members).filter((k:string)=>k!==f.properties!.lineage))];
 const result={areas:{type:'FeatureCollection' as const,features:areas},overlaps:{type:'FeatureCollection' as const,features:overlaps}};cache.set(key,result);if(cache.size>16)cache.delete(cache.keys().next().value!);return result;
}
export function coexistencePattern(colors:string[],focus=-1,size=24){
 const palette=focus<0?colors:[colors[focus],colors[focus],...colors.filter((_,i)=>i!==focus)];const data=new Uint8Array(size*size*4);
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){const h=palette[Math.floor(((x+y)%size)*palette.length/size)];data.set([1,3,5].map(i=>parseInt(h.slice(i,i+2),16)).concat(255),(y*size+x)*4);}
 return{width:size,height:size,data};
}
export const distributionCoast=(year:number)=>year> -500000?'countries.geojson':`coastlines-${Math.min(7,Math.max(1,Math.floor((-year+500000)/1000000)))}.geojson`;
export function distributionCard(p:Record<string,any>,year:number,available=true){
 const d=catalogue.taxa.find(t=>t.key===p.lineage);if(!d)return'';
 const coexist=(p.coexistence??[]).map((k:string)=>catalogue.taxa.find(t=>t.key===k)?.name??k);
 return`<div class="regional-card human-distribution-card"><div class="regional-badge"><span style="background:${esc(d.color)}"></span><strong>${esc(d.name)}</strong></div><div class="country-content"><section class="country-pane">${!available?'<p class="selection-unavailable">Sin área representada en esta fecha. La ficha se conserva; el límite de consulta no equivale a extinción.</p>':''}${humanPhoto('hominin-'+d.key,true)}<button class="human-article-link" data-encyclopedia-entry="hominin-${d.key}">Leer sobre ${esc(d.name)} →</button><h3>Distribución estimada</h3><p>${esc(d.note)}</p><dl class="country-facts"><div><dt>Fecha consultada</dt><dd>${formatYear(year)}</dd></div><div><dt>Clasificación</dt><dd>${esc(d.classification)}</dd></div><div><dt>Registro aproximado</dt><dd>${d.oldestKa.toLocaleString('es')}–${d.youngestKa.toLocaleString('es')} ka</dd></div><div><dt>Regiones representadas</dt><dd>${esc((p.regionLabels??[]).join(' · '))}</dd></div></dl><p class="profile-note">${esc(d.dateBasis)} Coordenadas fósiles de referencia actual; costas según el modelo y su fecha. Estas manchas no representan países, densidad o dominio.</p><h3>Coexistencia y contacto</h3><p>${coexist.length?esc(coexist.join(' · '))+'. Las franjas muestran solapamiento regional de las reconstrucciones.':'No hay solapamientos entre las áreas activas representadas para este grupo.'} No se deducen guerras, exterminios o jerarquías a partir de un solapamiento. El grosor puede destacar el grupo filtrado; no expresa superioridad.</p><h3>Referencias fósiles</h3><p>${esc(d.fossils.map(f=>f.name).join(' · ')||'Consultar los yacimientos y registros arqueológicos del mapa.')}</p><h3>Fuentes</h3>${[...d.references,...(p.phaseSources??[]).map((url:string)=>({title:'Evidencia de la fase regional',url}))].map(r=>`<p><a class="profile-source" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.title)} ↗</a></p>`).join('')}<p class="profile-note">Delimitación regional aproximada. No hay una frontera biológica exacta ni una ocupación uniforme o continua acreditada.</p></section></div></div>`;
}
export function distributionLegend(data:FeatureCollection){return data.features.length?`<div class="human-distribution-legend"><strong>Distribución humana estimada</strong>${data.features.map(f=>`<span class="human-range-key"><i style="background:${esc(f.properties!.color)}"></i>${esc(f.properties!.name)}</span>`).join('')}<small>Franjas: regiones compartidas de las reconstrucciones; no guerras. Límites aproximados; puntos: evidencias localizadas.</small></div>`:'';}
export const lineageInventory=()=>`<details class="lineage-inventory"><summary>${catalogue.taxa.length} entradas de especies y linajes</summary><p>No existe un recuento taxonómico único. Las clasificaciones alternativas no se dibujan como poblaciones independientes.</p>${catalogue.taxa.map(t=>`<p><button data-encyclopedia-entry="hominin-${t.key}">${esc(t.name)} →</button><small>${esc(t.classification)} · ${t.oldestKa.toLocaleString('es')}–${t.youngestKa.toLocaleString('es')} ka</small></p>`).join('')}</details>`;
