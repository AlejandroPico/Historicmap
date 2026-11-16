import { tx, language } from './i18n';
import chronology from '../Tierra/Cuaternario/cronologia.json' with {type:'json'};
import {yearFromAge} from './dates';
export {yearFromAge} from './dates';
import index from '../public/data/ice-model-index.json' with {type:'json'};
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
export function iceCaption(year:number){const s=iceSampleFor(year);return s?tx('iceHistory.referenciaBp1950ModeloConMuestras',{model:index.model,v1:formatYear(s.referenceYear),v2:s.ageBP.toLocaleString(language)}):'';}
export function prehistoricClimate(year:number){return chronology.holocene.subdivisions.find(p=>year>=yearFromAge(p.age,p.epoch))?.label??tx('iceHistory.pleistocenoTardio');}
