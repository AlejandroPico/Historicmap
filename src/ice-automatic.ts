import policy from '../public/data/ice-automatic-index.json' with {type:'json'};
import climate from '../public/data/climate-lr04.json' with {type:'json'};
import {ageFromYear} from './ice-history';
import{displayIceSampleFor}from'./ice-synthesis';
export type IceMode='auto'|'on'|'off';
export function iceEnabledFor(year:number,mode:IceMode){const s=displayIceSampleFor(year);return !!s&&mode!=='off'&&(mode==='on'||(s.kind==='interval-hypothesis'?!!s.autoVisible:policy.samples.some(p=>p.ageBP===s.ageBP&&p.autoVisible)));}
export function climateRecordFor(year:number){const ageKa=ageFromYear(year)/1000;if(ageKa<0||ageKa>climate.rows.at(-1)!.ageKa)return undefined;return climate.rows.reduce((a,b)=>Math.abs(b.ageKa-ageKa)<Math.abs(a.ageKa-ageKa)?b:a);}
export function climateContext(year:number){const r=climateRecordFor(year);return r?`Contexto LR04: muestra ${r.ageKa.toLocaleString('es')} ka BP1950, δ¹⁸O ${r.delta18O.toLocaleString('es')} ‰. Combina volumen de hielo y temperatura oceánica profunda; no delimita mantos ni paleocostas.`:year < -100000?'Contexto del Plioceno/Mioceno: no hay reconstrucción de mantos incorporada para esta fecha.':'';}
