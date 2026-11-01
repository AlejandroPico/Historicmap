import catalog from '../Tierra/Planeta/indicadores.json' with {type:'json'};
export type PlanetField='meanTemperature'|'temperatureAnomaly'|'solarDay'|'siderealRotation'|'oceanArea'|'nitrogen'|'oxygen'|'argon'|'carbonDioxide'|'waterVapor'|'methane'|'ammonia'|'hydrogen'|'helium'|'rockVapor'|'otherGases';
export type PlanetReference={basis:'civil';year:number}|{basis:'BP1950'|'b2k2000';ageYears:number}|{basis:'Ma';ageMa:number;nominalEpoch:number};
export interface PlanetRecord{
 id:string;field:PlanetField;value:number|{min:number;max:number}|null;unit:string;
 reference:PlanetReference;availableFromYear:number;validUntilYear?:number;
 evidence:'observation-synthesis'|'rounded-reference'|'model'|'estimate';quantity:string;
 uncertainty:{minus:number;plus:number;description:string}|null;method:string;sourceId:string;scope:string;interpolation:'none';
}
export const planetRecords=catalog.records as PlanetRecord[];
export const planetSources=catalog.sources as Record<string,{name:string;url:string;retrieved:string;version:string}>;
export const atmosphereNote=catalog.atmosphereBasis;
export function planetReferenceLabel(reference:PlanetReference){return reference.basis==='civil'?String(reference.year):reference.basis==='Ma'?`${reference.ageMa.toLocaleString('es')} Ma · eje nominal${reference.nominalEpoch}`:`${reference.ageYears.toLocaleString('es')} ${reference.basis}`;}
/** A dated reference is retained with its date; it never becomes a new observation. */
export function planetRecordFor(field:PlanetField,year:number,records=planetRecords){
 if(!Number.isFinite(year)||year===0)throw Error('Fecha civil inválida');
 return records.filter(r=>r.field===field&&r.availableFromYear<=year&&(r.validUntilYear===undefined||year<=r.validUntilYear)).sort((a,b)=>b.availableFromYear-a.availableFromYear)[0];
}
export function planetValue(record:PlanetRecord|undefined){
 if(!record||record.value===null)return'Sin estimación incorporada';
 const f=(n:number)=>n.toLocaleString('es',{maximumFractionDigits:3});
 const value=typeof record.value==='number'?f(record.value):`${f(record.value.min)}–${f(record.value.max)}`;
 const error=record.uncertainty?(record.uncertainty.minus===record.uncertainty.plus?` ± ${f(record.uncertainty.plus)}`:` −${f(record.uncertainty.minus)}/+${f(record.uncertainty.plus)}`):'';
 return`${record.evidence==='rounded-reference'?'≈ ':''}${value}${error} ${record.unit}`;
}
