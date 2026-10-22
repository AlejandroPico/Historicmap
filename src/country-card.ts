import type {Snapshot} from './time';
import {formatYear} from './time';
import {escapeHtml as esc,factRows,profileFor,type ProfileData} from './profiles';
import {entityContext} from './recent-context';
import {identityMarkup,type IdentityData} from './identities';

/** The same dated identity and country card is used by map clicks and search. */
export function countryCard(p:Record<string,any>,year:number,snapshot:Snapshot,profiles:ProfileData,identities:IdentityData,base:string){
  const identity=snapshot.kind==='geological'?'':identityMarkup(p,year,identities,base);
  if(['war','dispute','civil-war'].includes(p.kind))return `${identity}<p class="country-context">${esc(p.note)}</p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">Fuentes del control territorial ↗</a>`;
  const profile=profileFor(profiles,p.code);
  const modern=snapshot.kind==='modern';
  const rows=factRows(profile,year);
  const context=entityContext(p.originalName??p.name,year);
  const dated=snapshot.kind==='annual';
  return `${identity}${modern&&profile?.official?`<p class="country-formal">${esc(profile.official)}</p>`:''}<dl class="country-facts">
    ${(modern?profile?.capital:p.capital)?`<div><dt>Capital / sede</dt><dd>${esc(modern?profile?.capital:p.capital)}</dd></div>`:''}
    ${modern&&profile?.region?`<div><dt>Región</dt><dd>${esc(profile.region)}</dd></div>`:''}
    ${p.politicalStatus?`<div><dt>Situación política</dt><dd>${esc(p.politicalStatus)}</dd></div>`:''}
    ${p.ownerName&&p.status!=='independent'?`<div><dt>Potencia administradora</dt><dd>${esc(p.ownerName)}</dd></div>`:''}
    ${p.parentName?`<div><dt>Vinculación en la fuente</dt><dd>${esc(p.parentName)}</dd></div>`:''}
    ${modern&&profile?.income?`<div><dt>Grupo de ingresos actual</dt><dd>${esc(profile.income)}</dd></div>`:''}${rows}</dl>
    ${context?`<p class="country-context">${esc(context.text)}</p><a class="profile-source" href="${context.source}" target="_blank" rel="noopener">Contexto histórico ↗</a>`:''}
    ${dated?`<details class="country-record"><summary>Registro histórico y fuentes</summary><p>Periodo del registro: ${esc(p.start)} a ${esc(p.end)}. ${p.b_def===0?'La fuente clasifica parte de los límites como indefinidos.':''} ${year<1886?'Reconstrucción anual de Cliopatria, sin fecha diaria uniforme.':'Base territorial al 31 de diciembre.'} Las ocupaciones y guerras civiles se consultan en su capa específica.</p><a href="${esc(p.source)}" target="_blank" rel="noopener">${year<1886?'Cliopatria':'CShapes 2.0'} ↗</a></details>`:''}
    ${rows?`<p class="profile-note">Cada cifra indica su año. Series del Banco Mundial; no se recalculan sobre fronteras históricas.</p><a class="profile-source" target="_blank" rel="noopener" href="https://data.worldbank.org/country/${esc(p.code?.toLowerCase())}">Banco Mundial · serie del país ↗</a>`:dated?'<p class="profile-note">Sin indicadores comparables para esta entidad y fecha.</p>':snapshot.kind==='geological'?'<p>Masas continentales reconstruidas con el modelo CAO2024.</p>':!modern?`<p>Área histórica registrada en ${formatYear(snapshot.year)}. ${esc(p.group??'')}.</p>`:'<p>Territorio del atlas contemporáneo. Sin serie estadística para esta entidad.</p>'}`;
}
