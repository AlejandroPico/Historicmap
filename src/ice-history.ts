import chronology from '../Tierra/Cuaternario/cronologia.json';
import {yearFromAge} from './dates';
export {yearFromAge} from './dates';
import index from '../public/data/ice-model-index.json';
import {formatYear} from './time';

/** Model ages use BP1950; civil chronology has no year zero. */
export function ageFromYear(year:number){if(year===0||!Number.isFinite(year))throw Error('Invalid civil year');return year<0?1949-year:1950-year;}
export const HOLOCENE_START=yearFromAge(chronology.holocene.age,chronology.holocene.epoch);
export const iceModel=index;
export function iceSampleFor(year:number){
 if(!Number.isInteger(year)||year===0||year<index.consultationStart)return undefined;
 const age=Math.max(0,ageFromYear(year));
 return index.samples.reduce((a,b)=>Math.abs(b.ageBP-age)<Math.abs(a.ageBP-age)||Math.abs(b.ageBP-age)===Math.abs(a.ageBP-age)&&b.ageBP>a.ageBP?b:a);
}
export function iceCaption(year:number){const s=iceSampleFor(year);return s?`${index.model} · referencia ${formatYear(s.referenceYear)} (${s.ageBP.toLocaleString('es')} BP1950). Modelo con muestras cada 2.500–5.000 años; muestra más cercana, sin interpolación anual.`:'';}
export function prehistoricClimate(year:number){return chronology.holocene.subdivisions.find(p=>year>=yearFromAge(p.age,p.epoch))?.label??'Pleistoceno tardío';}
