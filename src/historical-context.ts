import {isoYear,compareDates,dateYear} from './dates';
import catalogue from '../public/data/historical-context.json';
import {territorialEntityCode} from './history';

export type HistoricalEvent={id:string;title:string;type:'conflict'|'transition';start:string;end?:string;countries:string[];text:string;source:string;sourceLabel:string;note?:string;precision?:number};
export const historicalEvents=catalogue.events as HistoricalEvent[];
export function eventsInYear(year:number,type?:HistoricalEvent['type']):HistoricalEvent[]{
 if(year<catalogue.startYear||year>catalogue.endYear)return [];
 const first=`${isoYear(year)}-01-01`,last=[`${isoYear(year)}-12-31`,catalogue.referenceDate].sort(compareDates)[0];
 return historicalEvents.filter(e=>(!type||e.type===type)&&compareDates(e.start,last)<=0&&(!e.end||compareDates(e.end,first)>0));
}
export function eventsForCountry(p:Record<string,any>,year:number,type?:HistoricalEvent['type']):HistoricalEvent[]{
 const code=territorialEntityCode(p,year);
 const keys=[code,...(code==='COD'&&year<1997?['ZAR']:[])];
 return eventsInYear(year,type).filter(e=>e.countries.some(c=>keys.includes(c)));
}
/** Annual overview changes with the dated inventory; it is not a completeness claim. */
export function annualHighlights(year:number):HistoricalEvent[]{
 return eventsInYear(year).sort((a,b)=>Number(b.start.startsWith(String(year)))-Number(a.start.startsWith(String(year)))||compareDates(a.start,b.start)).slice(0,6);
}
