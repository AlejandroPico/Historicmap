import type {Feature} from 'geojson';
import {displayLabel} from './map-presentation';
import type {CountryAnchor} from './selection';
import {escapeHtml as esc,type ProfileData} from './profiles';
import {identityFor,type IdentityData} from './identities';
import {metrics,metricOptions,seriesFor,valueAt,formatMetric,trendChart,type IndicatorData} from './country-workspace';

export type ComparisonState={mode:'dates'|'countries';a:number;b:number;metric:string;pinned:CountryAnchor[]};
export type ComparisonSnapshot={anchor:CountryAnchor;year:number;feature?:Feature};
export const anchorId=(a:CountryAnchor)=>a.uid||a.key||`${a.code}:${a.originalName}`;
export function comparisonShell(state:ComparisonState,year:number,profiles:ProfileData,data:IndicatorData){
 return `<div class="comparison-modes" aria-label="Tipo de comparación"><button data-comparison-mode="dates" aria-pressed="${state.mode==='dates'}">Entre fechas</button><button data-comparison-mode="countries" aria-pressed="${state.mode==='countries'}">Entre países</button></div>${state.mode==='dates'?`<form id="comparison-dates" class="comparison-dates"><label>Fecha A<input id="comparison-a" type="number" min="-10000" max="${new Date().getFullYear()}" required value="${state.a}"></label><label>Fecha B<input id="comparison-b" type="number" min="-10000" max="${new Date().getFullYear()}" required value="${state.b}"></label><button class="secondary-button" type="submit">Comparar fechas</button></form>`:`<p>Fija países y selecciona otro en el mapa o el buscador. Se comparan en ${year}, con un máximo de cuatro entidades.</p><div class="pinned-countries">${state.pinned.map((a,i)=>`<span>${esc(displayLabel(a.name))}<button data-unpin-country="${i}" aria-label="Quitar ${esc(displayLabel(a.name))} de la comparación">×</button></span>`).join('')||'<small>Aún no hay países fijados.</small>'}</div><button class="text-action" id="clear-comparison">Vaciar comparación</button>`}<label class="workspace-field">Indicador del gráfico<select id="comparison-metric">${metricOptions(data,state.metric)}</select></label><div id="comparison-results" aria-live="polite"><p class="profile-note">Preparando comparación…</p></div>`;
}
export function comparisonMarkup(snapshots:ComparisonSnapshot[],state:ComparisonState,profiles:ProfileData,data:IndicatorData,identities:IdentityData,base:string,year:number){
 const catalogue=metrics(data),metric=catalogue[state.metric]??catalogue.population;
 const names=snapshots.map(s=>`${displayLabel(s.feature?.properties?.name??s.anchor.name)} · ${s.year}`);
 const header=snapshots.map((s,i)=>{
  const p=s.feature?.properties,id=p?identityFor(p,s.year,identities):undefined;
  return `<article class="comparison-summary"><h3>${esc(names[i])}</h3>${id?.flag?`<img src="${esc(base+id.flag.file)}" width="54" height="36" alt="Bandera de ${esc(names[i])}"><a class="media-credit" href="${esc(id.flag.url)}" target="_blank" rel="noopener">${esc(id.flag.attribution||id.flag.artist||id.flag.title)} · ${esc(id.flag.license)} ↗</a>`:''}${p?`<p>${esc(p.politicalStatus??'Registro territorial')} ${p.capital?`· ${esc(p.capital)}`:''}</p><ul>${id!.leaders.map(l=>`<li>${esc(displayLabel(l.name))}<small>${esc(l.role)} · ${esc(l.start)} — ${esc(l.end)}</small></li>`).join('')}</ul><a class="profile-source" href="${esc(p.geometrySource??p.source??'https://www.naturalearthdata.com/')}" target="_blank" rel="noopener">Fuente territorial ↗</a>`:'<p>Entidad sin representación activa en esta fecha. No se usan las cifras ni las autoridades de un Estado sucesor.</p>'}<button class="secondary-button" data-jump-year="${s.year}" data-entity-key="${esc(s.anchor.key)}" data-entity-name="${esc(s.anchor.name)}">Ver en el mapa</button></article>`;
 }).join('');
 const rows=Object.entries(catalogue).map(([key,m])=>{
  const values=snapshots.map(s=>s.feature?valueAt(seriesFor(s.feature.properties?.code,key,profiles,data),s.year):undefined);
  const delta=state.mode==='dates'&&values[0]&&values[1]?values[1][1]-values[0][1]:undefined;
  const d=delta===undefined?'—':`${delta>0?'+':''}${formatMetric(delta,{...m,unit:m.unit.startsWith('%')?'puntos porcentuales'+m.unit.slice(1):m.unit})}`;
  return `<tr><th scope="row"><a href="${esc(m.source)}" target="_blank" rel="noopener" title="${esc(m.description)}">${esc(m.label)} ↗</a></th>${values.map(o=>`<td>${o?`${esc(formatMetric(o[1],m))}<small>Dato de ${o[0]}</small>`:'<span class="data-missing">Sin dato</span>'}</td>`).join('')}${state.mode==='dates'?`<td>${esc(d)}</td>`:''}</tr>`;
 }).join('');
 const colors=['var(--chart-1)','var(--chart-2)','var(--chart-3)','var(--chart-4)'];
 const plot=trendChart(snapshots.map((s,i)=>({name:names[i],color:colors[i%colors.length],values:s.feature?seriesFor(s.feature.properties?.code,state.metric,profiles,data).filter(([y])=>y<=s.year):[]})),metric,Math.max(year,...snapshots.map(s=>s.year)));
 let geometry='';
 if(state.mode==='dates'&&snapshots[0]?.feature&&snapshots[1]?.feature){
  const equal=JSON.stringify(snapshots[0].feature.geometry)===JSON.stringify(snapshots[1].feature.geometry);
  geometry=`<p class="profile-note">${equal?'La fuente conserva el mismo contorno en ambas fechas.':'La fuente registra contornos diferentes en estas fechas. Usa «Ver en el mapa» para alternarlos.'} Esta comparación no certifica todos los cambios de frontera ni el control militar.</p>`;
 }
 return `<div class="comparison-summaries">${header}</div>${geometry}<div class="comparison-table-wrap" tabindex="0" aria-label="Tabla comparativa desplazable"><table class="comparison-table"><caption>Observaciones disponibles; año real visible y retraso máximo de cinco años.</caption><thead><tr><th scope="col">Indicador</th>${names.map(n=>`<th scope="col">${esc(n)}</th>`).join('')}${state.mode==='dates'?'<th scope="col">Diferencia B − A</th>':''}</tr></thead><tbody>${rows}</tbody></table></div>${plot}`;
}
