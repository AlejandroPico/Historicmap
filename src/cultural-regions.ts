import type{Feature,FeatureCollection,Geometry,Position}from'geojson';
import{windows,reviewedThrough,segments}from'../public/data/cultural-index.json';
const coverage={windows,reviewedThrough};
import{escapeHtml as esc}from'./profiles';
import{formatYear}from'./time';
export type RegionalRecord={key:string;ownerKey:string;contextKey:string;name:string;originalNames:string[];kind:string;region:string;start:number;end:number;sourceYear:number;source:string;sourceLicense:string;dateBasis:string;interpretation:string;spatialUncertainty:string;temporalUncertainty:string;references:{title:string;url:string}[];politicalKeys:string[];color:string;focus:number[];reviewStatus:string;pending:string[];sourceGrouping:string[];endIsReviewBoundary?:boolean;temporalMode?:string;continuityNote?:string;reviewedOn?:string;evidenceThrough?:number};
export const regionalCoverage=coverage;
export function hasRegionalCoverage(year:number){return coverage.windows.some(w=>w.start<=year&&year<=w.end);}
export function regionalAsset(year:number){return segments.find(s=>s.start<=year&&year<=s.end)?.file;}
export function regionsAt(data:FeatureCollection,year:number,political:FeatureCollection):FeatureCollection{
 const represented=new Set(political.features.map(f=>String(f.properties?.identityKey??f.properties?.entityCode??'')));
 return {...data,features:data.features.filter(f=>{const p=f.properties as RegionalRecord;return p.start<=year&&year<=p.end&&(p.kind!=='polity-reference'||!p.politicalKeys.some(k=>represented.has(k)));}).sort((a,b)=>(a.properties?.displayPriority??0)-(b.properties?.displayPriority??0))};
}
const ringCache=new WeakMap<Position[],{xs:number[];west:number;east:number;south:number;north:number}>();
function ringContains(ring:Position[],point:Position){
 // Unwrap the entire ring consistently before positioning the query.
 let cached=ringCache.get(ring);
 if(!cached){const xs=[ring[0][0]];let west=xs[0],east=xs[0],south=ring[0][1],north=south;
  for(let i=1;i<ring.length;i++){const x=ring[i][0]+360*Math.round((xs[i-1]-ring[i][0])/360);xs.push(x);west=Math.min(west,x);east=Math.max(east,x);south=Math.min(south,ring[i][1]);north=Math.max(north,ring[i][1]);}
  cached={xs,west,east,south,north};ringCache.set(ring,cached);
 }
 const longitudes=cached.xs,center=(cached.west+cached.east)/2;
 let inside=false;const x=point[0]+360*Math.round((center-point[0])/360),y=point[1];
 if(x<cached.west||x>cached.east||y<cached.south||y>cached.north)return false;
 for(let i=0,j=ring.length-1;i<ring.length;j=i++){
  const a=ring[i],b=ring[j],ax=longitudes[i],bx=longitudes[j];
  const cross=(x-ax)*(b[1]-a[1])-(y-a[1])*(bx-ax);
  if(Math.abs(cross)<1e-9&&x>=Math.min(ax,bx)&&x<=Math.max(ax,bx)&&y>=Math.min(a[1],b[1])&&y<=Math.max(a[1],b[1]))return true;
  if((a[1]>y)!==(b[1]>y)&&x<(bx-ax)*(y-a[1])/(b[1]-a[1])+ax)inside=!inside;
 }return inside;
}
export function containsLocation(geometry:Geometry,point:Position){
 const polygons=geometry.type==='Polygon'?[geometry.coordinates]:geometry.type==='MultiPolygon'?geometry.coordinates:[];
 return polygons.some(p=>ringContains(p[0],point)&&!p.slice(1).some(r=>ringContains(r,point)));
}
/** Political entities come first; full regional originals remain selectable underneath. */
export function entitiesAt(point:Position,political:FeatureCollection,regional:FeatureCollection):Feature[]{
 const seen=new Set<string>();return [...political.features,...regional.features.filter(f=>f.properties?.kind==='polity-reference'),...regional.features.filter(f=>f.properties?.kind!=='polity-reference').reverse()].filter(f=>{
  if(!containsLocation(f.geometry,point))return false;
  const key=String(f.properties?.contextKey??f.properties?.identityKey??f.properties?.entityCode??f.properties?.name??f.id);
  if(seen.has(key))return false;seen.add(key);return true;
 });
}
export function regionalCard(p:RegionalRecord,year:number,available:boolean){
 return `<div class="regional-card"><p class="regional-type">${p.temporalMode==='historical-area-context'?'Área histórica · última referencia disponible':p.temporalMode==='traditional-area-undated'?'Área tradicional · datación local pendiente':p.kind==='polity-reference'?'Poder político · referencia cartográfica':'Pueblo / región cultural · límites aproximados'}</p>${!available?`<p class="selection-unavailable">Sin representación activa para esta fecha. ${year>coverage.reviewedThrough?'La revisión cultural posterior a '+coverage.reviewedThrough+' está pendiente; esto no indica desaparición de sus habitantes.':'Consulta las fases y la evidencia: ausencia de un contorno no acredita despoblación.'}</p>`:''}<div class="country-content"><section class="country-pane"><h3>${esc(p.region)}</h3><p>${esc(p.interpretation)}</p>${p.evidenceThrough!==undefined&&year>p.evidenceThrough?`<p class="profile-note regional-future">Consulta de una referencia histórica más allá de${p.evidenceThrough}; no hay observaciones futuras para${year}.</p>`:''}<dl class="country-facts">${p.reviewedOn?`<div><dt>Revisión documental</dt><dd>${esc(p.reviewedOn)}</dd></div>`:''}<div><dt>Fecha consultada</dt><dd>${year}</dd></div><div><dt>Referencia espacial</dt><dd>Mapa de ${p.sourceYear<0?formatYear(p.sourceYear):p.sourceYear} · aproximación regional</dd></div><div><dt>Ventana de consulta</dt><dd>${p.start}–${p.end}${p.endIsReviewBoundary?' · límite de revisión':''}</dd></div><div><dt>Fechas</dt><dd>${esc(p.dateBasis)}</dd></div></dl><h3>Alcance e incertidumbre</h3><p class="regional-review">${p.reviewStatus==='current-continuity-spatial-extent-unverified'?'Continuidad cultural contrastada; extensión contemporánea y desplazamientos pendientes de delimitación.':p.reviewStatus==='historical-reference-current-extent-unverified'?'Se conserva evidencia histórica; no es un mapa de distribución actual de población.':p.reviewStatus==='traditional-area-local-chronology-pending'?'Área tradicional sin cronología local suficiente: no es una frontera observada en el año consultado.':p.reviewStatus==='source-reference-awaiting-independent-regional-validation'?'Referencia de compilación; contraste regional independiente pendiente.':'Bibliografía regional contrastada; delimitación espacial todavía aproximada.'}</p><p>${esc(p.spatialUncertainty)}</p><p>${esc(p.temporalUncertainty)}</p>${p.continuityNote?`<p>${esc(p.continuityNote)}</p>`:''}<p class="profile-note">La extensión de referencia no es una frontera soberana ni demuestra ocupación uniforme o exclusiva. Una entidad política superpuesta no hace desaparecer este registro.</p><details><summary>Nombre en el mapa de origen</summary><p>${p.originalNames.map(esc).join(' · ')}</p>${p.sourceGrouping.length?`<p>Agrupación en la fuente: ${p.sourceGrouping.map(esc).join(' · ')}. No se extrapola automáticamente a otras fechas.</p>`:''}</details><details><summary>Trabajo documental pendiente</summary><ul>${p.pending.map(esc).map(t=>`<li>${t}</li>`).join('')}</ul></details><h3>Fuentes</h3>${p.references.map(r=>`<p><a class="profile-source" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.title)} ↗</a></p>`).join('')}<p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">Geometría original · ${p.sourceYear<0?formatYear(p.sourceYear):p.sourceYear} · ${esc(p.sourceLicense)} ↗</a></p></section></div></div>`;
}
