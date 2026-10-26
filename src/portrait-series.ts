import catalogue from '../public/data/portrait-series.json';
import type {Media} from './identities';
export type PortraitRecord={person:string;start:number;end:number;media:Media;photoDate:string|null;dateLabel:string;source:string;note:string};
export type PortraitCatalogue={referenceDate:string;records:PortraitRecord[]};
/** Select only after the office term has been resolved. A portrait window
 * never confers office, and the same person can use distinct mandate images. */
export function portraitAt(person:string,year:number,start:string,end:string,fallback:Media|undefined,data:PortraitCatalogue=catalogue as PortraitCatalogue):Media|undefined{
 const first=Math.max(year,Number(start.slice(0,4))),last=Math.min(year,Number(end.slice(0,4)));
 if(first>last)return fallback;
 const record=data.records.filter(r=>r.person===person&&r.start<=last&&r.end>=first).sort((a,b)=>b.start-a.start)[0];
 if(record)return {...record.media,photoDate:record.photoDate??undefined,photoDateLabel:record.dateLabel};
 return fallback&&data.records.some(r=>r.person===person)?{...fallback,photoDateLabel:'Imagen de referencia · variante de esta etapa pendiente de acreditar'}:fallback;
}
