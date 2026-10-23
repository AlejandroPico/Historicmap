import {escapeHtml as esc} from './profiles';
import {administrationFor,dayBefore} from './territorial-administrations';

export type Media={file:string;title:string;url:string;artist:string;license:string;licenseUrl?:string;credit?:string;attribution?:string;attributionRequired?:boolean;sha256:string;bytes:number;display?:'full-frame';caption?:string};
export type Leader={person:string;name:string;role:string;start:string;end:string;source:string;precision?:number;curated?:boolean;note?:string;portrait?:Media;endIsUpperBound?:boolean;startIsCoverageBoundary?:boolean;endIsCoverageBoundary?:boolean;authorityScope?:'local'|'external'};
type Flag={start:string;end:string;media:Media;source:string};
type Identity={qid:string;name:string;flags:Flag[];leaders:Leader[];notes?:{start:string;end:string;text:string;source:string}[];territoryStatus?:{start:string;end:string;text:string;source:string}};
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
  'Yugoslavia':'YUG','Czechoslovakia':'CSK','Yemen (Arab Republic of Yemen)':'YEM',
  'Bosnia-Herzegovina':'BIH','Kosovo':'KOS',
};
const focalQids:Record<string,string>={Q30:'USA',Q29:'ESP',Q183:'DEU',Q16957:'DDR',Q15180:'USSR',Q159:'RUS',Q142:'FRA',Q148:'CHN',Q17:'JPN',Q38:'ITA',Q145:'GBR'};
const identityCodes:Record<string,string>={SSD:'SDS',XKX:'KOS',PSE:'PSX',ESH:'SAH'};
export function identityKey(p:Properties,year:number,data:IdentityData){
  const territory=administrationFor(p,year);
  if(territory?.localKey)return territory.localKey;
  if(['colony','protectorate','mandate'].includes(String(p.status)))return '';
  let key=String(p.identityKey??p.controller??'');
  if(!key||!data.countries[key]){const code=String(p.code??'');key=identityCodes[code]??code;}
  if(!key||!data.countries[key])key=aliases[String(p.originalName??p.name)]??'';
  if(!key||!data.countries[key]){
    // Missing identifiers are not identities: several historical factions have
    // an empty QID. Matching them made unrelated countries inherit Spain.
    const q=String(p.wikidata??'').trim();
    key=/^Q\d+$/.test(q)?focalQids[q]??Object.keys(data.countries).find(k=>data.countries[k].qid===q)??'':'';
  }
  if(key==='RUS'&&year>=1922&&year<=1990)key='USSR';
  return key;
}
export function referenceDate(year:number,retrieved:string,now=new Date()){
  const today=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  return [`${year}-12-31`,retrieved,today].sort()[0];
}
function ownIdentityFor(p:Properties,year:number,data:IdentityData,now=new Date()){
  const key=identityKey(p,year,data), identity=data.countries[key];
  const date=referenceDate(year,data.retrieved,now);
  const future=year>Number(data.retrieved.slice(0,4))||year>now.getFullYear();
  const valid=(a:{start:string;end:string})=>!future&&a.start<=date&&a.end>=date;
  const note=identity?.notes?.find(valid);
  const first=`${year}-01-01`;
  // The map is an annual view. Show every mandate that intersects the year,
  // including short governments and both sides of a handover.
  let leaders=identity?.leaders.filter(l=>!future&&l.start<=date&&l.end>=first)??[];
  // A curated focal statement takes priority for the same person and office;
  // keep genuinely different offices and heads of state/government separate.
  const curated=leaders.filter(l=>l.curated);
  const partyOffice=(l:Leader)=>/partido|PCUS|PCCh|SED|secretario general/i.test(l.role);
  const sameOffice=(a:Leader,b:Leader)=>partyOffice(a)===partyOffice(b);
  // A renewal on a shared handover date is a separate mandate. Source date
  // intervals may include that day at both ends; do not collapse the renewal.
  const overlaps=(a:Leader,b:Leader)=>(a.start<b.end&&b.start<a.end)||(a.start===b.start&&a.end===b.end);
  leaders=leaders.filter(l=>l.curated||!curated.some(c=>c.person===l.person&&sameOffice(c,l)&&overlaps(c,l)));
  // Rejected generic statements must not reintroduce offices that a reviewed
  // record has explicitly separated when the remaining duplicates are merged.
  const annualStatements=leaders;
  // Consolidate the same officeholder reported by several source properties.
  // Keep distinct authorities (for example Pétain and de Gaulle) separate.
  const authorities:Leader[]=[];
  const score=(l:Leader)=>(l.curated?1000:0)+(l.precision??9)*10+(!l.role.startsWith('Jefatura')?2:0)-(l.endIsUpperBound?3:0);
  for(const leader of leaders){
    if(/^Q\d+$/.test(leader.name))continue;
    const index=authorities.findIndex(l=>l.person===leader.person&&sameOffice(l,leader)&&overlaps(l,leader));
    if(index<0)authorities.push(leader);
    else if(score(leader)>score(authorities[index]))authorities[index]=leader;
  }
  leaders=authorities.map(l=>{
    const simultaneous=annualStatements.filter(a=>a.person===l.person&&a.start===l.start&&a.end===l.end);
    if(simultaneous.some(a=>a.role==='Jefatura del Estado')&&simultaneous.some(a=>a.role==='Jefatura del Gobierno'))return {...l,role:l.role.startsWith('Jefatura')?'Jefatura del Estado y del Gobierno':`${l.role} · Estado y Gobierno`};
    return l;
  });
  const priority=(l:Leader)=>{
    if(key==='YUG'&&l.person==='Q9161')return 145;
    if(/dictador|dictadura|partido|de facto|Führer|Poglavnik|SED/i.test(l.role))return 140;
    if(/emperador|rey de Francia/i.test(l.role)&&key==='FRA'&&year<1848)return 130;
    if(['USA','FRA','RUS','CHN'].includes(key)&&(/Jefatura del Estado|Presidente de la República|Presidente de los Estados Unidos/.test(l.role)))return 120;
    if(/Gobierno|gobierno|Primer ministro|Consejo de Ministros|Canciller|canciller/.test(l.role))return 110;
    return 80;
  };
  leaders.sort((a,b)=>priority(b)-priority(a)||Number(b.end>=date)-Number(a.end>=date)||a.start.localeCompare(b.start));
  const flag=note?undefined:identity?.flags.filter(valid).sort((a,b)=>b.start.localeCompare(a.start))[0]?.media;
  const territoryStatus=identity?.territoryStatus&&valid(identity.territoryStatus)?identity.territoryStatus:undefined;
  return {key,date,flag,leaders,territoryStatus,note:future?'Los titulares y símbolos posteriores a la fecha de consulta todavía no están documentados.':note?.text,noteSource:note?.source,name:key==='ESP-REPUBLIC'||key==='ESP-NATIONALIST'?identity?.name:undefined};
}
export function identityFor(p:Properties,year:number,data:IdentityData,now=new Date()){
 const base=ownIdentityFor(p,year,data,now),administration=administrationFor(p,year);
 if(!administration)return {...base,administration:undefined,flagContext:undefined as string|undefined};
 const local=administration.localKey&&data.countries[administration.localKey]?ownIdentityFor({...p,status:'independent',identityKey:administration.localKey},year,data,now):base;
 const state=ownIdentityFor({identityKey:administration.admin},year,data,now);
 const first=`${year}-01-01`,last=state.date,relationEnd=administration.end?dayBefore(administration.end):data.retrieved;
 const external:Leader[]=state.leaders.filter(l=>!administration.headOfStateOnly||/Estado|reina|rey|queen|king/i.test(l.role)).flatMap(l=>{
  const start=[l.start,administration.start].sort().at(-1)!,end=[l.end,relationEnd,data.retrieved].sort()[0];
  if(start>end||start>last||end<first)return[];
  const clippedStart=start!==l.start,clippedEnd=end!==l.end;
  return [{...l,start,end,authorityScope:'external',role:`${l.role} · ${data.countries[administration.admin]?.name??administration.admin}`,startIsCoverageBoundary:l.startIsCoverageBoundary||clippedStart,endIsCoverageBoundary:l.endIsCoverageBoundary||clippedEnd,note:[l.note,clippedStart||clippedEnd?'Tramo de autoridad sobre este territorio: el límite de relación no es un nombramiento o cese en el Estado administrador.':''].filter(Boolean).join(' ')}];
 });
 // A transfer between external administrations within the year must not keep
 // only the earlier administration, or its flag, at the annual close.
 let flagState=state,flagAdmin=administration.admin;
 const successor=String(p.administratorKey??'');
 if(administration.end&&administration.end<=last&&successor&&successor!==administration.admin&&p.status!=='independent'){
  const next=ownIdentityFor({identityKey:successor},year,data,now);
  for(const l of next.leaders){
   const start=[l.start,administration.end].sort().at(-1)!,end=[l.end,data.retrieved].sort()[0];
   if(start<=end&&start<=last&&end>=first)external.push({...l,start,end,authorityScope:'external',role:`${l.role} · ${data.countries[successor]?.name??successor}`,startIsCoverageBoundary:true,note:[l.note,'Tramo posterior a la transferencia administrativa documentada; no nuevo nombramiento ni atribución de soberanía.'].filter(Boolean).join(' ')});
  }
  flagState=next;flagAdmin=successor;
 }
 const localLeaders=local.leaders.map(l=>({...l,authorityScope:'local' as const}));
 const dependentAtReference=flagAdmin!==administration.admin||administration.start<=last&&(!administration.end||administration.end>last);
 const useStateFlag=dependentAtReference&&!local.flag&&!!flagState.flag;
 return {...local,name:base.name,flag:local.flag??(useStateFlag?flagState.flag:undefined),leaders:[...localLeaders,...external],administration,flagContext:useStateFlag?`Símbolo ${flagAdmin==='UNTEA'?'de la administración de Naciones Unidas':'del Estado administrador'} · ${data.countries[flagAdmin]?.name??flagAdmin}`:undefined};
}
const dateLabel=(date:string,precision=11)=>{
  const [y,m,d]=date.split('-');return precision<10?y:precision===10?`${Number(m)}/${y}`:`${Number(d)}/${Number(m)}/${y}`;
};
export {dateLabel as formatMandateDate};
export function identityMarkup(p:Properties,year:number,data:IdentityData,baseUrl:string,part:'all'|'header'|'authorities'='all'){
  const identity=identityFor(p,year,data);
  const imageUrl=(media:Media)=>baseUrl+media.file;
  const credits=(media:Media)=>{
    const author=media.attribution||(/Unknown author/i.test(media.artist)?'Autor no identificado':media.artist.trim())||media.title;
    return `<a class="media-credit" href="${esc(media.url)}" target="_blank" rel="noopener">${esc(author)}${media.attribution?'':` · ${esc(media.license)}`} ↗</a>`;
  };
  const name=identity.name??String(p.name??'');
  const symbolLabel=identity.flagContext?identity.flagContext+' · ':identity.key==='SAH'?'Símbolo de la RASD · ':identity.flag?.title.includes('Royal Standard')?'Estandarte real · ':['war','dispute'].includes(String(p.kind))?'Autoridad controladora · ':'';
  const flag=identity.flag?`<div class="identity-header"><a class="flag-source" href="${esc(identity.flag.url)}" target="_blank" rel="noopener" aria-label="${esc(`Procedencia y licencia del símbolo de ${name}`)}" title="${esc(identity.flag.artist)} · ${esc(identity.flag.license)}"><img class="historic-flag" src="${esc(imageUrl(identity.flag))}" alt="${esc(identity.flagContext??`Bandera de ${name} correspondiente a la fecha consultada`)}" width="96" height="64"></a><span>${esc(name)}<br><small>${esc(symbolLabel)}${esc(`Símbolo al ${dateLabel(identity.date)}`)}</small></span></div>`:'';
  const leaders=identity.leaders.map((l,index)=>`${identity.administration&&(index===0||l.authorityScope!==identity.leaders[index-1].authorityScope)?`<h3 class="authority-group">${l.authorityScope==='external'?'Autoridades del Estado administrador':'Autoridades del territorio'}</h3>`:''}<article class="leader-card${l.portrait?.display==='full-frame'?' full-frame':''}">${l.portrait?`<img class="leader-portrait${l.portrait.display==='full-frame'?' full-frame-photo':''}" src="${esc(imageUrl(l.portrait))}" alt="${esc(l.portrait.caption??`Retrato de ${l.name}`)}" width="100" height="128" loading="lazy">${l.portrait.caption?`<p class="photo-caption">${esc(l.portrait.caption)}</p>`:''}`:''}<div class="leader-details"><span class="leader-role">${esc(l.role)}</span><h3 class="leader-name">${esc(l.name)}</h3>${l.end>=identity.date&&!l.endIsUpperBound&&!l.endIsCoverageBoundary&&(l.precision??11)>=11?`<span class="term-current">${year===new Date().getFullYear()?'En funciones a la referencia':'Al cierre del año'}</span>`:''}<span class="leader-term">${l.startIsCoverageBoundary?'Documentado al inicio de '+dateLabel(l.start,l.precision):dateLabel(l.start,l.precision)} — ${l.endIsCoverageBoundary?'documentado hasta el límite de cobertura ':l.endIsUpperBound?'hasta, como máximo, ':''}${l.end===data.retrieved?`referencia ${dateLabel(data.retrieved)}`:dateLabel(l.end,l.precision)}</span>${l.note?`<p>${esc(l.note)}</p>`:''}<a class="profile-source" href="${esc(l.source)}" target="_blank" rel="noopener">Biografía y mandato ↗</a></div>${l.portrait?`<div class="portrait-credit">${credits(l.portrait)}${l.portrait.display==='full-frame'?`<a class="media-credit" href="${esc(l.portrait.licenseUrl)}" target="_blank" rel="noopener">Licencia de la fotografía ↗</a>`:''}</div>`:''}</article>`).join('');
  const empty=identity.note?`<p class="identity-note">${esc(identity.note)}</p>${identity.noteSource?`<a class="profile-source" href="${esc(identity.noteSource)}" target="_blank" rel="noopener">Contexto institucional y fuente ↗</a>`:''}`:!identity.leaders.length&&!identity.territoryStatus?'<p class="identity-note">Dirigente pendiente de documentación para esta entidad y fecha.</p>':'';
  if(part==='header')return flag;
  const administrationNote=identity.administration?`<div class="identity-note"><strong>${esc(identity.administration.label)}</strong><p>${esc(identity.administration.note)}</p><p>Los cargos rotulados con el Estado administrador corresponden a su ámbito estatal; las autoridades territoriales conservan su propio cargo.</p><a class="profile-source" href="${esc(identity.administration.source)}" target="_blank" rel="noopener">Relación administrativa y fuente ↗</a></div>`:'';
  const annualNote=administrationNote+(identity.leaders.length?`<p class="mandate-reference">Autoridades con mandato durante ${year}. Consulta hasta ${dateLabel(identity.date)}.</p>`:'');
  const territoryNote=identity.territoryStatus?`<p class="identity-note">${esc(identity.territoryStatus.text)}</p><a class="profile-source" href="${esc(identity.territoryStatus.source)}" target="_blank" rel="noopener">Estatus del territorio ↗</a>`:'';
  return `<section class="political-identity" aria-label="Bandera y autoridades de la época" data-identity="${esc(identity.key)}">${part==='all'?flag:''}${territoryNote}${annualNote}${leaders}${empty}</section>`;
}
