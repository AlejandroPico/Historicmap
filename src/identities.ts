import {escapeHtml as esc} from './profiles';

export type Media={file:string;title:string;url:string;artist:string;license:string;licenseUrl?:string;credit?:string;attribution?:string;attributionRequired?:boolean;sha256:string;bytes:number};
export type Leader={person:string;name:string;role:string;start:string;end:string;source:string;precision?:number;curated?:boolean;note?:string;portrait?:Media};
type Flag={start:string;end:string;media:Media;source:string};
type Identity={qid:string;name:string;flags:Flag[];leaders:Leader[];notes?:{start:string;end:string;text:string;source:string}[]};
export type IdentityData={retrieved:string;license:string;source:string;countries:Record<string,Identity>};
type Properties=Record<string,unknown>;
const aliases:Record<string,string>={
  'United States of America':'USA','United States':'USA','Estados Unidos':'USA',
  'Spain':'ESP','España':'ESP','Second Spanish Republic':'ESP-REPUBLIC','Spanish Nationalists':'ESP-NATIONALIST','Francoist Spain':'ESP',
  'Germany (Prussia)':'DEU','German Federal Republic':'DEU','Germany':'DEU','Nazi Germany':'DEU','German Empire':'DEU','Weimar Republic':'DEU',
  'German Democratic Republic':'DDR','East Germany':'DDR',
  'Russia (Soviet Union)':'RUS','Soviet Union':'USSR','USSR':'USSR',
  'United Kingdom':'GBR','France':'FRA','First French Empire':'FRA','French Consulate':'FRA','French Directory':'FRA','French First Republic':'FRA',
  'Bourbon Kingdom of France':'FRA','Second French Empire':'FRA','French Third Republic':'FRA','French Second Republic':'FRA',
  'Japan':'JPN','Empire of Japan':'JPN','China':'CHN','Republic of China':'CHN','Italy/Sardinia':'ITA','Kingdom of Italy':'ITA',
};
const focalQids:Record<string,string>={Q30:'USA',Q29:'ESP',Q183:'DEU',Q16957:'DDR',Q15180:'USSR',Q159:'RUS',Q142:'FRA',Q148:'CHN',Q17:'JPN',Q38:'ITA',Q145:'GBR'};
export function identityKey(p:Properties,year:number,data:IdentityData){
  if(['colony','protectorate','mandate'].includes(String(p.status)))return '';
  let key=String(p.identityKey??p.controller??'');
  if(!key||!data.countries[key])key=String(p.code??'');
  if(!key||!data.countries[key])key=aliases[String(p.originalName??p.name)]??'';
  if(!key||!data.countries[key]){
    const q=String(p.wikidata??'');key=focalQids[q]??Object.keys(data.countries).find(k=>data.countries[k].qid===q)??'';
  }
  if(key==='RUS'&&year>=1922&&year<=1990)key='USSR';
  return key;
}
export function referenceDate(year:number,retrieved:string,now=new Date()){
  const today=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  return [`${year}-12-31`,retrieved,today].sort()[0];
}
export function identityFor(p:Properties,year:number,data:IdentityData,now=new Date()){
  const key=identityKey(p,year,data), identity=data.countries[key];
  const date=referenceDate(year,data.retrieved,now);
  const future=year>Number(data.retrieved.slice(0,4))||year>now.getFullYear();
  const valid=(a:{start:string;end:string})=>!future&&a.start<=date&&a.end>=date;
  const note=identity?.notes?.find(valid);
  let leaders=note?[]:identity?.leaders.filter(valid)??[];
  // A curated focal statement takes priority for the same person and office;
  // keep genuinely different offices and heads of state/government separate.
  const curated=leaders.filter(l=>l.curated);
  leaders=leaders.filter(l=>l.curated||!curated.some(c=>c.person===l.person));
  // Consolidate the same officeholder reported by several source properties.
  // Keep distinct authorities (for example Pétain and de Gaulle) separate.
  const authorities=new Map<string,Leader>();
  const score=(l:Leader)=>(l.curated?10:0)+(!l.role.startsWith('Jefatura')?2:0);
  for(const leader of leaders){
    if(/^Q\d+$/.test(leader.name))continue;
    const previous=authorities.get(leader.person);
    if(!previous||score(leader)>score(previous))authorities.set(leader.person,leader);
  }
  leaders=[...authorities.values()];
  const priority=(l:Leader)=>{
    if(/dictador|dictadura|partido|Führer|Poglavnik|SED/i.test(l.role))return 140;
    if(/emperador|rey de Francia/i.test(l.role)&&key==='FRA'&&year<1848)return 130;
    if(['USA','FRA','RUS','CHN'].includes(key)&&(/Jefatura del Estado|Presidente de la República|Presidente de los Estados Unidos/.test(l.role)))return 120;
    if(/Gobierno|gobierno|Primer ministro|Consejo de Ministros|Canciller|canciller/.test(l.role))return 110;
    return 80;
  };
  leaders.sort((a,b)=>priority(b)-priority(a));
  const flag=note?undefined:identity?.flags.filter(valid).sort((a,b)=>b.start.localeCompare(a.start))[0]?.media;
  return {key,date,flag,leaders,note:future?'Los titulares y símbolos posteriores a la fecha de consulta todavía no están documentados.':note?.text,noteSource:note?.source,name:key==='ESP-REPUBLIC'||key==='ESP-NATIONALIST'?identity?.name:undefined};
}
const dateLabel=(date:string,precision=11)=>{
  const [y,m,d]=date.split('-');return precision<10?y:precision===10?`${Number(m)}/${y}`:`${Number(d)}/${Number(m)}/${y}`;
};
export function identityMarkup(p:Properties,year:number,data:IdentityData,baseUrl:string){
  const identity=identityFor(p,year,data);
  const imageUrl=(media:Media)=>baseUrl+media.file;
  const credits=(media:Media)=>{
    const author=media.attribution||(/Unknown author/i.test(media.artist)?'Autor no identificado':media.artist.trim())||media.title;
    return `<a class="media-credit" href="${esc(media.url)}" target="_blank" rel="noopener">${esc(author)}${media.attribution?'':` · ${esc(media.license)}`} ↗</a>`;
  };
  const name=identity.name??String(p.name??'');
  const symbolLabel=identity.flag?.title.includes('Royal Standard')?'Estandarte real · ':['war','dispute'].includes(String(p.kind))?'Autoridad controladora · ':'';
  const flag=identity.flag?`<div class="identity-header"><img class="historic-flag" src="${esc(imageUrl(identity.flag))}" alt="Bandera de ${esc(name)} correspondiente a la fecha consultada" width="96" height="64"><span>${esc(name)}<br><small>${esc(symbolLabel)}${esc(year===new Date().getFullYear()?'Referencia consultada':`31 diciembre ${year}`)}</small></span></div><details class="flag-credit"><summary>Fuente de la bandera</summary>${credits(identity.flag)}</details>`:'';
  const leaders=identity.leaders.map(l=>`<article class="leader-card">${l.portrait?`<img class="leader-portrait" src="${esc(imageUrl(l.portrait))}" alt="Retrato de ${esc(l.name)}" width="100" height="128" loading="lazy">`:''}<div class="leader-details"><span class="leader-role">${esc(l.role)}</span><h3 class="leader-name">${esc(l.name)}</h3><span class="leader-term">${dateLabel(l.start,l.precision)} — ${l.end===data.retrieved?'en el registro consultado':dateLabel(l.end,l.precision)}</span>${l.note?`<p>${esc(l.note)}</p>`:''}<a class="profile-source" href="${esc(l.source)}" target="_blank" rel="noopener">Biografía y mandato ↗</a></div>${l.portrait?`<div class="portrait-credit">${credits(l.portrait)}</div>`:''}</article>`).join('');
  const empty=identity.note?`<p class="identity-note">${esc(identity.note)}</p>${identity.noteSource?`<a class="profile-source" href="${esc(identity.noteSource)}" target="_blank" rel="noopener">Administración de ocupación ↗</a>`:''}`:!identity.leaders.length?'<p class="identity-note">Dirigente pendiente de documentación para esta entidad y fecha.</p>':'';
  return `<section class="political-identity" aria-label="Bandera y autoridades de la época" data-identity="${esc(identity.key)}">${flag}${leaders}${empty}</section>`;
}
