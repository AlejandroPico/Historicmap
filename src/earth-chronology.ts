import ics from '../Tierra/Cronologia/ics-2026-06.json' with {type:'json'};
import human from '../Tierra/Cronologia/edades-humanas.json' with {type:'json'};

export type GeologicalRank='group'|'eon'|'era'|'period'|'subperiod'|'epoch'|'age';
export interface GeologicalUnit {
 id:string;name:string;rank:GeologicalRank;parent:string|null;oldestMa:number;youngestMa:number;color:string;
 formal:boolean;gsspRatified:boolean;axisOldestYear:number;axisEndYear:number|null;timeBasis:string;source:string;axisSource?:string;
 numericalUncertaintyMa:{oldest:number|null;youngest:number|null};
}
export interface HumanUnit {id:string;name:string;startYear:number;endYear:number|null;lane:'overview'|'regional'|'transformation';scope:string;sourceId:string;color:string;priority:number;formal:boolean;precision:string}
export const geologicalUnits=ics.units as GeologicalUnit[];
export const humanUnits=human.units as HumanUnit[];
export const humanChronologySources=human.sources as Record<string,{title:string;url:string}>;
export const chronologyVersion=ics.version;
export const chronologyNote=human.note;
export const rankLabels:Record<GeologicalRank,string>={group:'Agrupación contextual',eon:'Eón',era:'Era',period:'Periodo',subperiod:'Subperiodo',epoch:'Época',age:'Edad'};
const order:GeologicalRank[]=['group','eon','era','period','subperiod','epoch','age'];
export function geologicalAt(year:number){
 if(!Number.isFinite(year)||year===0)throw Error('La cronología civil no contiene año cero');
 return geologicalUnits.filter(u=>year>=u.axisOldestYear&&(u.axisEndYear===null||year<u.axisEndYear)).sort((a,b)=>order.indexOf(a.rank)-order.indexOf(b.rank));
}
export function humanAt(year:number){return humanUnits.filter(u=>year>=u.startYear&&(u.endYear===null||year<u.endYear));}
export function geologicalAgeLabel(ma:number){return ma>=1000?`${(ma/1000).toLocaleString('es',{maximumFractionDigits:4})} Ga`:ma>=1?`${ma.toLocaleString('es',{maximumFractionDigits:4})} Ma`:`${(ma*1000).toLocaleString('es',{maximumFractionDigits:3})} ka`;}
export function geologicalRangeLabel(unit:GeologicalUnit){
 if(unit.axisSource){const b2k=(y:number)=>`${((1999-y)/1000).toLocaleString('es',{maximumFractionDigits:3})} ka b2k2000`;return`${b2k(unit.axisOldestYear)} — ${unit.axisEndYear===null?'actualidad':b2k(unit.axisEndYear)}`;}
 const edge=(ma:number,error:number|null)=>{
  if(error===null)return geologicalAgeLabel(ma);
  const factor=ma>=1000?1000:ma>=1?1:.001,unit=ma>=1000?'Ga':ma>=1?'Ma':'ka';
  const n=(v:number)=>(v/factor).toLocaleString('es',{maximumFractionDigits:6});return`${n(ma)} ± ${n(error)} ${unit}`;
 };
 return`${edge(unit.oldestMa,unit.numericalUncertaintyMa.oldest)} — ${unit.youngestMa?edge(unit.youngestMa,unit.numericalUncertaintyMa.youngest):'actualidad'}`;
}
/** Local zoom controls emphasis; the geological interval does not actually end. */
export function geologicalEmphasis(year:number,visibleYears:number){
 const q=geologicalUnits.find(u=>u.id==='Quaternary')!;
 if(year<q.axisOldestYear)return 1;
 return Math.max(0,Math.min(1,(Math.log10(Math.max(1,visibleYears))-4.7)/1.4));
}
