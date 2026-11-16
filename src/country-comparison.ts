import { tx } from './i18n';
import type {Feature} from 'geojson';
import{PREHISTORY_START}from'./prehistoric-time';
import{cultureLabel}from'./prehistory';
import {displayLabel} from './map-presentation';
import type {CountryAnchor} from './selection';
import {escapeHtml as esc,type ProfileData} from './profiles';
import {identityFor,type IdentityData} from './identities';
import {metrics,metricOptions,seriesFor,valueAt,formatMetric,trendChart,type IndicatorData} from './country-workspace';

export type ComparisonState={mode:'dates'|'countries';a:number;b:number;metric:string;pinned:CountryAnchor[]};
export type ComparisonSnapshot={anchor:CountryAnchor;year:number;feature?:Feature};
export const anchorId=(a:CountryAnchor)=>a.uid||a.key||`${a.code}:${a.originalName}`;
export function comparisonShell(state:ComparisonState,year:number,profiles:ProfileData,data:IndicatorData){
 return `<div class="comparison-modes" aria-label="${tx('countryComparison.tipoDeComparacion')}"><button data-comparison-mode="dates" aria-pressed="${state.mode==='dates'}">${tx('countryComparison.entreFechas')}</button><button data-comparison-mode="countries" aria-pressed="${state.mode==='countries'}">${tx('countryComparison.entrePaises')}</button></div>${state.mode==='dates'?`<form id="comparison-dates" class="comparison-dates"><label>${tx('countryComparison.fechaA')}<input id="comparison-a" type="number" min="${PREHISTORY_START}" max="${new Date().getFullYear()}" required value="${state.a}"></label><label>${tx('countryComparison.fechaB')}<input id="comparison-b" type="number" min="${PREHISTORY_START}" max="${new Date().getFullYear()}" required value="${state.b}"></label><button class="secondary-button" type="submit">${tx('countryComparison.compararFechas')}</button></form>`:`<p>${tx('countryComparison.fijaPaisesYSeleccionaOtro')} ${year}${tx('countryComparison.conUnMaximoDeCuatro')}</p><div class="pinned-countries">${state.pinned.map((a,i)=>`<span>${esc(displayLabel(a.name))}<button data-unpin-country="${i}" aria-label="Quitar ${esc(displayLabel(a.name))} ${tx('countryComparison.deLaComparacion')}">×</button></span>`).join('')||tx('countryComparison.smallAunNoHayPaises')}</div><button class="text-action" id="clear-comparison">${tx('countryComparison.vaciarComparacion')}</button>`}<label class="workspace-field">${tx('countryComparison.indicadorDelGrafico')}<select id="comparison-metric">${metricOptions(data,state.metric)}</select></label><div id="comparison-results" aria-live="polite"><p class="profile-note">${tx('countryComparison.preparandoComparacion')}</p></div>`;
}
export function comparisonMarkup(snapshots:ComparisonSnapshot[],state:ComparisonState,profiles:ProfileData,data:IndicatorData,identities:IdentityData,base:string,year:number){
 const catalogue=metrics(data),metric=catalogue[state.metric]??catalogue.population;
 const names=snapshots.map(s=>`${displayLabel(s.feature?.properties?.name??s.anchor.name)} · ${s.year}`);
 const archaeological=snapshots.every(s=>s.anchor.properties.referenceKind==='archaeological-site');
 const evidenceFields:[string,(p:any)=>string][]=[[tx('countryComparison.intervalosActivos'),p=>p?String(p.evidenceCount??tx('countryComparison.sinDesgloseEnEstaFuente')):tx('countryComparison.sinIntervaloActivo')],[tx('countryComparison.atribucionHumana'),p=>p?.taxa?.join(' · ')||tx('countryComparison.sinAtribucionDetallada')],[tx('countryComparison.culturaMaterial'),p=>p?.cultures?.map(cultureLabel).join(' · ')||tx('countryComparison.sinClasificacionDetallada')]];
 const evidenceRows=archaeological?evidenceFields.map(([label,value])=>`<tr><th scope="row">${label}</th>${snapshots.map(s=>`<td>${esc(value(s.feature?.properties))}</td>`).join('')}${state.mode==='dates'?'<td>—</td>':''}</tr>`).join(''):'';
 const header=snapshots.map((s,i)=>{
  const p=s.feature?.properties,id=p?identityFor(p,s.year,identities):undefined;
  return `<article class="comparison-summary"><h3>${esc(names[i])}</h3>${id?.flag?`<img src="${esc(base+id.flag.file)}" width="54" height="36" alt="${tx('countryComparison.banderaDe')} ${esc(names[i])}"><a class="media-credit" href="${esc(id.flag.url)}" target="_blank" rel="noopener">${esc(id.flag.attribution||id.flag.artist||id.flag.title)} · ${esc(id.flag.license)} ↗</a>`:''}${p?`<p>${esc(p.referenceKind==='archaeological-site'?tx('countryComparison.referenciaArqueologica'):p.politicalStatus??tx('countryComparison.registroTerritorial'))} ${p.capital?`· ${esc(p.capital)}`:''}</p><ul>${id!.leaders.map(l=>`<li>${esc(displayLabel(l.name))}<small>${esc(l.role)} · ${esc(l.start)} — ${esc(l.end)}</small></li>`).join('')}</ul><a class="profile-source" href="${esc(p.geometrySource??p.source??'https://www.naturalearthdata.com/')}" target="_blank" rel="noopener">${p.referenceKind==='archaeological-site'?tx('countryComparison.fuenteDeEvidencia'):tx('countryComparison.fuenteTerritorial')} ↗</a>`:archaeological?tx('countryComparison.pSinIntervaloDeEvidencia'):tx('countryComparison.pEntidadSinRepresentacionActiva')}<button class="secondary-button" data-jump-year="${s.year}" data-entity-key="${esc(s.anchor.key)}" data-entity-name="${esc(s.anchor.name)}">${tx('countryComparison.verEnElMapa')}</button></article>`;
 }).join('');
 const rows=Object.entries(catalogue).map(([key,m])=>{
  const values=snapshots.map(s=>s.feature?valueAt(seriesFor(s.feature.properties?.code,key,profiles,data),s.year):undefined);
  const delta=state.mode==='dates'&&values[0]&&values[1]?values[1][1]-values[0][1]:undefined;
  const d=delta===undefined?'—':`${delta>0?'+':''}${formatMetric(delta,{...m,unit:m.unit.startsWith('%')?'puntos porcentuales'+m.unit.slice(1):m.unit})}`;
  return `<tr><th scope="row"><a href="${esc(m.source)}" target="_blank" rel="noopener" title="${esc(m.description)}">${esc(m.label)} ↗</a></th>${values.map(o=>`<td>${o?`${esc(formatMetric(o[1],m))}<small>${tx('countryComparison.datoDe')} ${o[0]}</small>`:tx('countryComparison.spanClassDataMissingSin')}</td>`).join('')}${state.mode==='dates'?`<td>${esc(d)}</td>`:''}</tr>`;
 }).join('');
 const colors=['var(--chart-1)','var(--chart-2)','var(--chart-3)','var(--chart-4)'];
 const plot=archaeological?'':trendChart(snapshots.map((s,i)=>({name:names[i],color:colors[i%colors.length],values:s.feature?seriesFor(s.feature.properties?.code,state.metric,profiles,data).filter(([y])=>y<=s.year):[]})),metric,Math.max(year,...snapshots.map(s=>s.year)));
 let geometry='';
 if(state.mode==='dates'&&snapshots[0]?.feature&&snapshots[1]?.feature){
  const equal=JSON.stringify(snapshots[0].feature.geometry)===JSON.stringify(snapshots[1].feature.geometry);
  geometry=archaeological?tx('countryComparison.pClassProfileNoteLas'):`<p class="profile-note">${equal?tx('countryComparison.laFuenteConservaElMismo'):tx('countryComparison.laFuenteRegistraContornosDiferentes')} ${tx('countryComparison.estaComparacionNoCertificaTodos')}</p>`;
 }
 return `<div class="comparison-summaries">${header}</div>${geometry}<div class="comparison-table-wrap" tabindex="0" aria-label="${tx('countryComparison.tablaComparativaDesplazable')}"><table class="comparison-table"><caption>${archaeological?tx('countryComparison.referenciasArqueologicasFechadasIntervalosY'):tx('countryComparison.observacionesDisponiblesAnoRealVisible')}</caption><thead><tr><th scope="col">Indicador</th>${names.map(n=>`<th scope="col">${esc(n)}</th>`).join('')}${state.mode==='dates'?'<th scope="col">Diferencia B − A</th>':''}</tr></thead><tbody>${archaeological?evidenceRows:rows}</tbody></table></div>${plot}`;
}
