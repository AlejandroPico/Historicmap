import catalog from '../Tierra/Planeta/indicadores.json' with {type:'json'};
import ancient from '../Tierra/Precambrico/indicadores.json' with {type:'json'};
import{deepSources}from'./deep-earth';
import{physicalRecord,physicalSources,videoScenarioAt,type EvidencePolicy}from'./earth-models';
export type PlanetField='meanTemperature'|'temperatureAnomaly'|'solarDay'|'siderealRotation'|'oceanArea'|'nitrogen'|'oxygen'|'argon'|'carbonDioxide'|'waterVapor'|'methane'|'ammonia'|'hydrogen'|'helium'|'rockVapor'|'otherGases';
export type PlanetReference={basis:'civil';year:number}|{basis:'BP1950'|'b2k2000';ageYears:number}|{basis:'Ma';ageMa:number;nominalEpoch:number};
export interface PlanetRecord{
 id:string;field:PlanetField;value:number|{min:number;max:number}|null;unit:string;
 reference:PlanetReference;availableFromYear:number;validUntilYear?:number;
 evidence:'observation-synthesis'|'rounded-reference'|'model'|'estimate'|'illustrative-scenario';quantity:string;
 uncertainty:{minus:number;plus:number;description:string}|null;method:string;sourceId:string;scope:string;interpolation:'none';
}
export const planetRecords=[...catalog.records,...ancient.records] as PlanetRecord[];
export const planetSources={...catalog.sources,...Object.fromEntries(Object.entries(deepSources).map(([id,s])=>[id,{...s,version:'Referencia por estudio'}])),...physicalSources} as Record<string,{name:string;url:string;retrieved:string;version:string}>;
export const atmosphereNote=catalog.atmosphereBasis;
export function planetReferenceLabel(reference:PlanetReference){return reference.basis==='civil'?String(reference.year):reference.basis==='Ma'?`${reference.ageMa.toLocaleString('es')} Ma · eje nominal${reference.nominalEpoch}`:`${reference.ageYears.toLocaleString('es')} ${reference.basis}`;}
/** A dated reference is retained with its date; it never becomes a new observation. */
export function planetRecordFor(field:PlanetField,year:number,records=planetRecords,policy:EvidencePolicy='reconstruction'){
 if(!Number.isFinite(year)||year===0)throw Error('Fecha civil inválida');
 if(records===planetRecords&&policy==='video'&&videoScenarioAt(year))return physicalRecord(field,year,policy);
 return records.filter(r=>r.field===field&&r.availableFromYear<=year&&(r.validUntilYear===undefined||year<=r.validUntilYear)).sort((a,b)=>b.availableFromYear-a.availableFromYear)[0]??(records===planetRecords?physicalRecord(field,year,policy):undefined);
}
export function planetValue(record:PlanetRecord|undefined){
 if(!record||record.value===null)return'Sin estimación incorporada';
 const f=(n:number)=>n.toLocaleString('es',{maximumFractionDigits:record.sourceId==='phanda'&&record.field==='meanTemperature'?1:3});
 const value=typeof record.value==='number'?f(record.value):`${f(record.value.min)}–${f(record.value.max)}`;
 const error=record.uncertainty?(record.uncertainty.minus===record.uncertainty.plus?` ± ${f(record.uncertainty.plus)}`:` −${f(record.uncertainty.minus)}/+${f(record.uncertainty.plus)}`):'';
 return`${record.evidence==='rounded-reference'?'≈ ':''}${value}${error} ${record.unit}`;
}
