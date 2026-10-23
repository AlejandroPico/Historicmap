import catalogue from '../public/data/affiliations.json';

export type AffiliationKind=string;
export type AffiliationCategory='member'|'partner'|'associate'|'suspended'|'other';
export type Membership={code:string;category:Exclude<AffiliationCategory,'other'>;start:string;end?:string;source:string;note?:string;startIsCoverageBoundary?:boolean;territorialApplication?:boolean};
export type Organization={id:string;label:string;type:string;description:string;source:string;formed:string;dissolved?:string;memberships:Membership[]};
export type AffiliationLegendEntry={category:AffiliationCategory;label:string;color:string};
export type AffiliationValue=AffiliationLegendEntry&{source:string;referenceDate:string;start?:string;end?:string;note?:string;startIsCoverageBoundary?:boolean;territorialApplication?:boolean};
const descriptions:Record<AffiliationCategory,string>={member:'Miembro',partner:'Socio',associate:'Asociado',suspended:'Participación suspendida',other:'Otros territorios'};
const colors:Record<AffiliationCategory,string>={member:'#4c8fa0',partner:'#b4bc80',associate:'#8eaf98',suspended:'#b78767',other:'#68777b'};
const categoryOrder:AffiliationCategory[]=['member','associate','partner','suspended'];
const organizations=catalogue.organizations as Organization[];
export const AFFILIATION_KINDS=organizations.map(o=>o.id);
export const AFFILIATIONS:Readonly<Record<string,Organization>>=Object.fromEntries(organizations.map(o=>[o.id,o]));
export const AFFILIATION_TYPES:Record<string,string>={military:'Seguridad y defensa',economic:'Comercio e integración económica',political:'Cooperación política y regional',regional:'Cooperación regional'};
export function affiliationsAvailable(year:number){return year>=catalogue.coverageStart&&year<=catalogue.coverageEnd;}
export function affiliationDate(year:number){return [`${year}-12-31`,catalogue.referenceDate].sort()[0];}
export function organizationActive(kind:string,year:number){
 const o=AFFILIATIONS[kind],date=affiliationDate(year);
 return !!o&&affiliationsAvailable(year)&&o.formed<=date&&(!o.dissolved||o.dissolved>date);
}
const aliases:Record<string,string>={SAH:'ESH',SDS:'SSD',KOS:'XKX',PSX:'PSE'};
const normalized=(code:string)=>aliases[code]??code;
export function membershipsAt(kind:string,year:number):Membership[]{
 if(!organizationActive(kind,year))return [];
 const date=affiliationDate(year);
 return AFFILIATIONS[kind].memberships.filter(m=>m.start<=date&&(!m.end||m.end>date));
}
function value(m:Membership,date:string):AffiliationValue{
 return {category:m.category,label:m.territorialApplication?'Ámbito territorial del tratado':descriptions[m.category],color:colors[m.category],source:m.source,referenceDate:date,start:m.start,end:m.end,note:m.note,startIsCoverageBoundary:m.startIsCoverageBoundary,territorialApplication:m.territorialApplication};
}
/** Membership is observed at annual close, independently of every leader in that year. */
export function affiliationFor(code:string,kind:string,year:number):AffiliationValue|undefined{
 if(!affiliationsAvailable(year)||!AFFILIATIONS[kind])return;
 const m=membershipsAt(kind,year).find(m=>m.code===normalized(code));
 return m?value(m,affiliationDate(year)):{category:'other',label:descriptions.other,color:colors.other,source:AFFILIATIONS[kind].source,referenceDate:affiliationDate(year)};
}
export function affiliationsDuringYear(code:string,kind:string,year:number):AffiliationValue[]{
 if(!affiliationsAvailable(year)||!AFFILIATIONS[kind])return [];
 const first=`${year}-01-01`,last=affiliationDate(year),o=AFFILIATIONS[kind];
 if(o.formed>last||(o.dissolved&&o.dissolved<=first))return [];
 return o.memberships.filter(m=>m.code===normalized(code)&&m.start<=last&&(!m.end||m.end>first)).map(m=>value(m,last));
}
export function affiliationLegend(kind:string,year:number):AffiliationLegendEntry[]{
 if(!affiliationsAvailable(year))return [];
 const categories=new Set(membershipsAt(kind,year).map(m=>m.category));
 return [...categoryOrder.filter(c=>categories.has(c as Membership['category'])).map(c=>({category:c,label:descriptions[c],color:colors[c]})),{category:'other',label:descriptions.other,color:colors.other}];
}
export function affiliationGroups(kind:string,year:number){
 return affiliationLegend(kind,year).filter(c=>c.category!=='other').map(c=>({...c,codes:membershipsAt(kind,year).filter(m=>m.category===c.category).map(m=>m.code)}));
}
export function affiliationSummary(kind:string,year:number){
 if(!organizationActive(kind,year))return 'La organización no está activa al cierre del año consultado.';
 const groups=affiliationGroups(kind,year);
 const memberships=membershipsAt(kind,year),territories=memberships.filter(m=>m.territorialApplication).length;
 const plurals:Record<string,string>={member:'miembros',associate:'asociados',partner:'socios',suspended:'participaciones suspendidas'};
 const partial=/parcial|incomplet/i.test(AFFILIATIONS[kind].description)?' Cobertura de suspensiones históricas parcial.':'';
 const counts=groups.map(c=>`${memberships.filter(m=>m.category===c.category&&!m.territorialApplication).length} ${plurals[c.category]}`);
 if(territories)counts.push(`${territories} ${territories===1?'territorio de aplicación':'territorios de aplicación'}`);
 return `${counts.join(' · ')}. Referencia: ${affiliationDate(year)}.${partial} Notas de cada relación en Datos.`;
}
