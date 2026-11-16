import { tx } from './i18n';
import {isoYear,compareDates,dateYear} from './dates';
import {escapeHtml as esc} from './profiles';
import {identityKey,formatMandateDate,type IdentityData} from './identities';
import {historicalEvents} from './historical-context';
import {AFFILIATIONS,AFFILIATION_KINDS} from './historical-affiliations';
import {territorialEntityCode} from './history';

export type EntityLink={id:string;from:{key:string;name:string;year:number};to:{key:string;name:string;year:number};date:string;type:string;label:string;note?:string;source:string;sourceLabel:string};
export type CountryRecord={id:string;keys:string[];start:string;end?:string;precision?:number;section:'institutions'|'history'|'territory'|'society'|'economy'|'defense'|'relations';title:string;text:string;source:string;sourceLabel:string;fields?:{label:string;value:string;unit?:string;referenceDate?:string;source?:string}[];places?:{name:string;longitude:number;latitude:number;source:string;note?:string}[]};
export type CountryHistory={retrieved:string;referenceDate:string;relations:EntityLink[];records:CountryRecord[]};
export const emptyHistory:CountryHistory={retrieved:'',referenceDate:'',relations:[],records:[]};
export function relatedEntities(key:string,data:CountryHistory){return data.relations.filter(r=>r.from.key===key||r.to.key===key);}
export function relationshipMarkup(key:string,data:CountryHistory){
 const relations=relatedEntities(key,data);
 return relations.length?`<div class="entity-links">${relations.map(r=>{
  const target=r.from.key===key?r.to:r.from;
  return `<article><small>${esc(r.date)} · ${esc(r.label)}</small><button class="entity-jump" data-entity-key="${esc(target.key)}" data-entity-name="${esc(target.name)}" data-jump-year="${target.year}">${esc(target.name)} <span>${target.year} ↗</span></button>${r.note?`<p>${esc(r.note)}</p>`:''}<a class="profile-source" href="${esc(r.source)}" target="_blank" rel="noopener">${esc(r.sourceLabel)} ↗</a></article>`;
 }).join('')}</div>`:tx('countryHistory.pClassProfileNoteNo');
}
export function recordsFor(key:string,section:CountryRecord['section'],year:number,data:CountryHistory){
 const last=[`${isoYear(year)}-12-31`,data.referenceDate].sort(compareDates)[0],first=`${isoYear(year)}-01-01`;
 if(compareDates(first,data.referenceDate)>0)return [];
 return data.records.filter(r=>r.keys.includes(key)&&r.section===section&&compareDates(r.start,last)<=0&&(!r.end||compareDates(r.end,first)>0));
}
export function recordMarkup(records:CountryRecord[]){return records.map(r=>`<article class="conflict-record"><h3>${esc(r.title)}</h3><p>${esc(r.text)}</p>${r.fields?.length?`<dl class="country-facts">${r.fields.map(f=>`<div><dt>${esc(f.label)}${f.referenceDate?` <small>${esc(f.referenceDate)}</small>`:''}</dt><dd>${esc(f.value)}${f.unit?` ${esc(f.unit)}`:''}${f.source?` <a class="profile-source" href="${esc(f.source)}" target="_blank" rel="noopener">${tx('countryHistory.fuente')}</a>`:''}</dd></div>`).join('')}</dl>`:''}${r.places?.map(p=>`<p><button class="text-action" data-locate-longitude="${p.longitude}" data-locate-latitude="${p.latitude}">${esc(p.name)} ${tx('countryHistory.verLugar')}</button>${p.note?` · ${esc(p.note)}`:''}<a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">${tx('countryHistory.fuenteDelLugar')}</a></p>`).join('')??''}<small>${esc(r.start)}${r.end?tx('countryHistory.hastaAntesDe',{v0:esc(r.end)}):''}</small><a class="profile-source" href="${esc(r.source)}" target="_blank" rel="noopener">${esc(r.sourceLabel)} ↗</a></article>`).join('');}
export type TimelineEntry={id:string;date:string;type:string;title:string;source:string;detail?:string;precision?:number};
export function countryTimeline(p:Record<string,any>,year:number,identities:IdentityData,history:CountryHistory):TimelineEntry[]{
 const key=String(p.workspaceKey??identityKey(p,year,identities)),country=identities.countries[key];
 const code=({USSR:'SUN',FRY:'SCG',SCG:'SCG',SDS:'SSD',SAH:'ESH',KOS:'XKX',PSX:'PSE'} as Record<string,string>)[key]??territorialEntityCode(p,year);
 const result:TimelineEntry[]=[];
 for(const l of country?.leaders??[])result.push({id:`leader:${l.person}:${l.role}:${l.start}`,date:l.start,type:'authorities',precision:l.precision,title:`${l.name} · ${l.role}`,detail:`${l.startIsCoverageBoundary?tx('countryHistory.enEjercicioAlInicioDe')+l.start:l.start} — ${l.end}${l.endIsCoverageBoundary?tx('countryHistory.limiteDeCoberturaNoCese'):l.endIsUpperBound?tx('countryHistory.ceseMaximoDocumentado'):''}`,source:l.source});
 for(const f of country?.flags??[])result.push({id:`flag:${f.start}:${f.media.file}`,date:f.start,type:'symbols',title:tx('countryHistory.simboloOBanderaDocumentada'),detail:f.media.title,source:f.source});
 for(const e of historicalEvents.filter(e=>e.countries.includes(code)))result.push({id:e.id,date:e.start,precision:e.precision,type:e.type==='conflict'?'conflicts':'history',title:e.title,detail:e.text,source:e.source});
 for(const kind of AFFILIATION_KINDS){
  const org=AFFILIATIONS[kind];
  for(const m of org.memberships.filter(m=>m.code===code)){
   const label={member:'miembro',partner:'socio',associate:'asociado',suspended:tx('countryHistory.participacionSuspendida')}[m.category];
   result.push({id:`org:${kind}:${m.start}:${m.category}`,date:m.start,type:'relations',title:`${org.label} · ${label}`,detail:m.startIsCoverageBoundary?tx('countryHistory.presenteAlInicioDeLa'):m.note,source:m.source});
   if(m.end)result.push({id:`org:${kind}:${m.end}:end`,date:m.end,type:'relations',title:tx('countryHistory.finDelIntervaloDeParticipacion',{label:org.label}),detail:m.note,source:m.source});
  }
 }
 for(const r of relatedEntities(key,history))result.push({id:r.id,date:r.date,type:'territory',title:r.label,detail:r.note,source:r.source});
 for(const r of history.records.filter(r=>r.keys.includes(key)))result.push({id:r.id,date:r.start,precision:r.precision,type:r.section==='institutions'?'history':r.section,title:r.title,detail:r.text,source:r.source});
 const limit=[identities.retrieved,history.referenceDate||identities.retrieved].sort(compareDates).at(-1)!;
 return [...new Map(result.filter(e=>/^-?\d{4}-\d{2}-\d{2}$/.test(e.date)&&compareDates(e.date,limit)<=0).map(e=>[e.id,e])).values()].sort((a,b)=>compareDates(b.date,a.date)||a.title.localeCompare(b.title));
}
export function timelineMarkup(p:Record<string,any>,year:number,identities:IdentityData,history:CountryHistory,filter='all',future=false,expanded=false){
 const all=countryTimeline(p,year,identities,history),entries=all.filter(e=>(future||compareDates(e.date,`${isoYear(year)}-12-31`)<=0)&&(filter==='all'||e.type===filter));
 const shown=expanded?entries:entries.slice(0,35);
 return `<div class="timeline-controls"><label class="workspace-field">Acontecimientos<select id="timeline-filter">${[['all','Todos'],['authorities','Autoridades'],['symbols',tx('countryHistory.simbolos')],['territory','Territorio'],['relations','Relaciones'],['history',tx('countryHistory.institucionesEHistoria')],['conflicts','Conflictos']].map(([v,label])=>`<option value="${v}" ${v===filter?'selected':''}>${label}</option>`).join('')}</select></label><label class="workspace-check"><input type="checkbox" id="timeline-future" ${future?'checked':''}> ${tx('countryHistory.incluirRegistrosPosterioresA')} ${year}</label></div><p class="profile-note">${entries.length} ${tx('countryHistory.registrosDocumentadosPulsaUnaFecha')}</p><ol class="country-timeline">${shown.map(e=>`<li><button class="timeline-date" data-jump-year="${dateYear(e.date)}">${esc(formatMandateDate(e.date,e.precision))}</button><h3>${esc(e.title)}</h3>${e.detail?`<p>${esc(e.detail)}</p>`:''}<a class="profile-source" href="${esc(e.source)}" target="_blank" rel="noopener">${tx('countryHistory.fuente')}</a></li>`).join('')}</ol>${!entries.length?tx('countryHistory.pNoHayAcontecimientosDocumentados'):''}${!expanded&&entries.length>shown.length?`<button class="secondary-button" id="timeline-expand">${tx('countryHistory.verLos')} ${entries.length} registros</button>`:''}`;
}
