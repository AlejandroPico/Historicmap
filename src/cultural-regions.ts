import { tx } from './i18n';
import{isPrehistoric,hasHumanEvidence,humanEvidenceAt,PREHISTORY_START,PREHISTORY_END}from'./prehistory';
import type{Feature,FeatureCollection,Geometry,Position}from'geojson';
import{windows,reviewedThrough,segments}from'../public/data/cultural-index.json';
const coverage={windows:[{start:PREHISTORY_START,end:PREHISTORY_END},...windows],reviewedThrough};
import{escapeHtml as esc}from'./profiles';
import{formatYear}from'./time';
export type RegionalRecord={key:string;ownerKey:string;contextKey:string;name:string;originalNames:string[];kind:string;region:string;start:number;end:number;sourceYear:number;source:string;sourceLicense:string;dateBasis:string;interpretation:string;spatialUncertainty:string;temporalUncertainty:string;references:{title:string;url:string}[];politicalKeys:string[];color:string;focus:number[];reviewStatus:string;pending:string[];sourceGrouping:string[];endIsReviewBoundary?:boolean;temporalMode?:string;continuityNote?:string;reviewedOn?:string;evidenceThrough?:number};
export const regionalCoverage=coverage;
export function hasRegionalCoverage(year:number){return year!==0&&coverage.windows.some(w=>w.start<=year&&year<=w.end);}
export function regionalAsset(year:number){if(isPrehistoric(year))return'human-evidence.geojson';return segments.find(s=>s.start<=year&&year<=s.end)?.file;}
export function regionalAssets(year:number){const file=regionalAsset(year),files=file?[file]:[];if(hasHumanEvidence(year)&&!files.includes('human-evidence.geojson'))files.push('human-evidence.geojson');if(hasHumanEvidence(year))files.push('hominin-sites.geojson');return files;}
export function regionsAt(data:FeatureCollection,year:number,political:FeatureCollection):FeatureCollection{
 if(isPrehistoric(year))return humanEvidenceAt(data,year);
 const represented=new Set(political.features.map(f=>String(f.properties?.identityKey??f.properties?.entityCode??'')));
 const areas=data.features.filter(f=>{if(f.geometry.type!=='Polygon'&&f.geometry.type!=='MultiPolygon')return false;const p=f.properties as RegionalRecord;return p.start<=year&&year<=p.end&&(p.kind!=='polity-reference'||!p.politicalKeys.some(k=>represented.has(k)));}).sort((a,b)=>(a.properties?.displayPriority??0)-(b.properties?.displayPriority??0));
 return {...data,features:[...areas,...humanEvidenceAt(data,year).features]};
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
 return `<div class="regional-card"><p class="regional-type">${p.temporalMode==='historical-area-context'?tx('culturalRegions.areaHistoricaUltimaReferenciaDisponible'):p.temporalMode==='traditional-area-undated'?tx('culturalRegions.areaTradicionalDatacionLocalPendiente'):p.kind==='polity-reference'?tx('culturalRegions.poderPoliticoReferenciaCartografica'):tx('culturalRegions.puebloRegionCulturalLimitesAproximados')}</p>${!available?`<p class="selection-unavailable">${tx('culturalRegions.sinRepresentacionActivaParaEsta')} ${year>coverage.reviewedThrough?tx('culturalRegions.laRevisionCulturalPosteriorA')+coverage.reviewedThrough+tx('culturalRegions.estaPendienteEstoNoIndica'):tx('culturalRegions.consultaLasFasesYLa')}</p>`:''}<div class="country-content"><section class="country-pane"><h3>${esc(p.region)}</h3><p>${esc(p.interpretation)}</p>${p.evidenceThrough!==undefined&&year>p.evidenceThrough?`<p class="profile-note regional-future">${tx('culturalRegions.consultaDeUnaReferenciaHistorica')}${p.evidenceThrough<0?formatYear(p.evidenceThrough):p.evidenceThrough}${tx('culturalRegions.noHayObservacionesFuturasPara')}${year<0?formatYear(year):year}.</p>`:''}<dl class="country-facts">${p.reviewedOn?`<div><dt>${tx('culturalRegions.revisionDocumental')}</dt><dd>${esc(p.reviewedOn)}</dd></div>`:''}<div><dt>${tx('culturalRegions.fechaConsultada')}</dt><dd>${formatYear(year)}</dd></div><div><dt>${tx('culturalRegions.referenciaEspacial')}</dt><dd>${tx('culturalRegions.mapaDe')} ${p.sourceYear<0?formatYear(p.sourceYear):p.sourceYear} ${tx('culturalRegions.aproximacionRegional')}</dd></div><div><dt>${tx('culturalRegions.ventanaDeConsulta')}</dt><dd>${p.start<0?formatYear(p.start):p.start}–${p.end<0?formatYear(p.end):p.end}${p.endIsReviewBoundary?tx('culturalRegions.limiteDeRevision'):''}</dd></div><div><dt>Fechas</dt><dd>${esc(p.dateBasis)}</dd></div></dl><h3>${tx('culturalRegions.alcanceEIncertidumbre')}</h3><p class="regional-review">${p.reviewStatus==='current-continuity-spatial-extent-unverified'?tx('culturalRegions.continuidadCulturalContrastadaExtensionContemporanea'):p.reviewStatus==='historical-reference-current-extent-unverified'?tx('culturalRegions.seConservaEvidenciaHistoricaNo'):p.reviewStatus==='traditional-area-local-chronology-pending'?tx('culturalRegions.areaTradicionalSinCronologiaLocal'):p.reviewStatus==='source-reference-awaiting-independent-regional-validation'?tx('culturalRegions.referenciaDeCompilacionContrasteRegional'):tx('culturalRegions.bibliografiaRegionalContrastadaDelimitacionEspacial')}</p><p>${esc(p.spatialUncertainty)}</p><p>${esc(p.temporalUncertainty)}</p>${p.continuityNote?`<p>${esc(p.continuityNote)}</p>`:''}<p class="profile-note">${tx('culturalRegions.laExtensionDeReferenciaNo')}</p><details><summary>${tx('culturalRegions.nombreEnElMapaDe')}</summary><p>${p.originalNames.map(esc).join(' · ')}</p>${p.sourceGrouping.length?`<p>${tx('culturalRegions.agrupacionEnLaFuente')} ${p.sourceGrouping.map(esc).join(' · ')}${tx('culturalRegions.noSeExtrapolaAutomaticamenteA')}</p>`:''}</details><details><summary>${tx('culturalRegions.trabajoDocumentalPendiente')}</summary><ul>${p.pending.map(esc).map(t=>`<li>${t}</li>`).join('')}</ul></details><h3>Fuentes</h3>${p.references.map(r=>`<p><a class="profile-source" href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.title)} ↗</a></p>`).join('')}<p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">${tx('culturalRegions.geometriaOriginal')} ${p.sourceYear<0?formatYear(p.sourceYear):p.sourceYear} · ${esc(p.sourceLicense)} ↗</a></p></section></div></div>`;
}
