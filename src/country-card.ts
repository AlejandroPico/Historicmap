import type {Snapshot} from './time';
import {formatYear} from './time';
import {escapeHtml as esc,factRows,profileFor,type ProfileData} from './profiles';
import {entityContext,recentContext} from './recent-context';
import {chapterFor} from './catalog';
import {identityFor,identityMarkup,type IdentityData} from './identities';
import {AFFILIATION_KINDS,AFFILIATIONS,affiliationFor,currentConflicts} from './current-affiliations';

/** One selected feature, with identical tabs for search and map clicks. */
export function countryCard(p:Record<string,any>,year:number,snapshot:Snapshot,profiles:ProfileData,identities:IdentityData,base:string){
  if(snapshot.kind==='geological')return '<p>Masas continentales reconstruidas con el modelo CAO2024.</p>';
  const profile=profileFor(profiles,p.code),modern=snapshot.kind==='modern',dated=snapshot.kind==='annual';
  const rows=factRows(profile,year),context=entityContext(p.originalName??p.name,year),period=recentContext(year)??chapterFor(year);
  const control=['war','dispute','civil-war'].includes(p.kind),identity=identityFor(p,year,identities);
  const memberships=AFFILIATION_KINDS.flatMap(kind=>{const a=affiliationFor(p.code,kind,year);return a&&a.category!=='other'?[`<div><dt>${esc(AFFILIATIONS[kind].label)}</dt><dd><a href="${esc(a.source)}" target="_blank" rel="noopener">${esc(a.label)} ↗</a></dd></div>`]:[];}).join('');
  const facts=`${modern&&profile?.official?`<p class="country-formal">${esc(profile.official)}</p>`:''}<dl class="country-facts">
    ${(modern?profile?.capital:p.capital)?`<div><dt>Capital / sede</dt><dd>${esc(modern?profile?.capital:p.capital)}</dd></div>`:''}
    ${modern&&profile?.region?`<div><dt>Región</dt><dd>${esc(profile.region)}</dd></div>`:''}
    ${p.politicalStatus?`<div><dt>Situación política</dt><dd>${esc(p.politicalStatus)}</dd></div>`:''}
    ${p.ownerName&&p.status!=='independent'?`<div><dt>Potencia administradora</dt><dd>${esc(p.ownerName)}</dd></div>`:''}
    ${p.parentName?`<div><dt>Vinculación en la fuente</dt><dd>${esc(p.parentName)}</dd></div>`:''}
    ${modern&&profile?.income?`<div><dt>Grupo de ingresos</dt><dd>${esc(profile.income)}</dd></div>`:''}${memberships}${rows}</dl>
    ${rows?`<p class="profile-note">Cada cifra indica su año. Series del Banco Mundial; no se recalculan sobre fronteras históricas.</p><a class="profile-source" target="_blank" rel="noopener" href="https://data.worldbank.org/country/${esc(p.code?.toLowerCase())}">Banco Mundial · serie del país ↗</a>`:'<p class="profile-note">Sin indicadores comparables documentados para esta entidad y fecha.</p>'}`;
  const story=`<p class="context-year">${formatYear(year)}</p>${identity.leaders.length?`<p>Durante ${year}, los mandatos documentados de esta entidad incluyen a ${identity.leaders.map(l=>`${esc(l.name)} (${esc(l.role)})`).join('; ')}. Las fechas individuales se consultan en Autoridades.</p>`:''}${control?`<p>${esc(p.note)}</p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">Fuentes del control territorial ↗</a>`:''}
    ${context?`<p class="country-context">${esc(context.text)}</p><a class="profile-source" href="${esc(context.source)}" target="_blank" rel="noopener">Contexto del país ↗</a>`:''}
    ${period?`<h3>El mundo en este periodo</h3><p>${esc(period.text)}</p><a class="profile-source" href="${esc(period.source)}" target="_blank" rel="noopener">${esc(period.sourceLabel)} ↗</a>`:!context&&!control?`<p>Área histórica registrada en ${formatYear(snapshot.year)}. ${esc(p.group??'')}</p>`:''}
    ${dated?`<details class="country-record"><summary>Registro territorial</summary><p>Periodo: ${esc(p.start)} a ${esc(p.end)}. ${p.b_def===0?'Parte de los límites se clasifica como indefinida.':''} ${year<1886?'Reconstrucción anual de Cliopatria, sin fecha diaria uniforme.':'Base territorial al 31 de diciembre.'}</p><a href="${esc(p.source)}" target="_blank" rel="noopener">${year<1886?'Cliopatria':'CShapes 2.0'} ↗</a></details>`:''}`;
  const conflicts=currentConflicts(p.code,year);
  const wars=`${control?`<p>${esc(p.note)}</p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">Registro territorial ↗</a>`:''}${conflicts.map(c=>`<article class="conflict-record"><h3>${esc(c.title)}</h3><p>${esc(c.text)}</p><a class="profile-source" href="${esc(c.source)}" target="_blank" rel="noopener">${esc(c.sourceLabel)} · ${esc(c.referenceDate)} ↗</a></article>`).join('')}${!conflicts.length&&!control?'<p>No hay un conflicto documentado en esta ficha para el año consultado.</p>':''}<p class="profile-note">La cobertura de conflictos es parcial. La ausencia de registros no equivale a ausencia de guerra. Las alianzas tampoco implican participación en un conflicto.</p>`;
  const tabs=[['authorities','Autoridades',identityMarkup(p,year,identities,base,'authorities')],['facts','Datos',facts],['context','Contexto',story],['conflicts','Conflictos',wars]];
  return `${identityMarkup(p,year,identities,base,'header')}<div class="country-tabs" role="tablist" aria-label="Ficha del país">${tabs.map(([id,label],i)=>`<button id="tab-${id}" role="tab" aria-controls="pane-${id}" aria-selected="${i===0}" tabindex="${i===0?0:-1}">${label}</button>`).join('')}</div>${tabs.map(([id,,html],i)=>`<section id="pane-${id}" class="country-pane" role="tabpanel" aria-labelledby="tab-${id}" tabindex="0" ${i===0?'':'hidden'}>${html}</section>`).join('')}`;
}
