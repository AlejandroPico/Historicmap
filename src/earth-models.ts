import { tx } from './i18n';
import phanda from '../Tierra/Fanerozoico/phanda.json' with {type:'json'};
import reference from '../Tierra/Fanerozoico/referencia-audiovisual.json' with {type:'json'};
import{deepAge}from'./deep-earth';
import{yearFromAge}from'./dates';
import type{PlanetField,PlanetRecord}from'./planet';
import{prehistoricCO2,iceCoreCO2}from'./ice-core-co2';
export type EvidencePolicy='reconstruction'|'video';
export const physicalSources={phanda:{name:tx('earthModels.juddEtAl2024Phanda'),url:'https://doi.org/10.1126/science.adk3705',retrieved:'2026-11-02',version:phanda.commit},'video-scenario':{name:tx('earthModels.algolEscenarioNumericoAudiovisual'),url:reference.url,retrieved:'2026-11-02',version:tx('earthModels.t31PuntosSeleccionadosReferenciaIlustrativa')},'ice-core-co2':{name:tx('earthModels.bereiterEtAl2015Co'),url:iceCoreCO2.source,retrieved:'2026-11-02',version:tx('earthModels.compuestoOriginalDe1901MuestrasEdad')}};
export const phandaBins=phanda.bins;
export function phandaAt(year:number){const age=deepAge(year);return age>=7?phanda.bins.find(b=>age>b.youngestMa&&age<=b.oldestMa):undefined;}
export function videoScenarioAt(year:number){const age=deepAge(year);return age>=7&&age<=4540.01?reference.samples.reduce((a,b)=>Math.abs(a.ageMa-age)<=Math.abs(b.ageMa-age)?a:b):undefined;}
export function physicalRecord(field:PlanetField,year:number,policy:EvidencePolicy='reconstruction'):PlanetRecord|undefined{
 const core=policy==='reconstruction'&&field==='carbonDioxide'?prehistoricCO2(year):undefined;
 if(core)return{id:'ice-core-co2-'+core.ageBP,field,value:core.co2ppm/10000,unit:'%',reference:{basis:'BP1950',ageYears:core.ageBP},availableFromYear:Math.ceil(yearFromAge(iceCoreCO2.rows.at(-1)!.ageBP)),validUntilYear:-10001,evidence:'observation-synthesis',quantity:'volume-fraction',uncertainty:{minus:core.sigmaPpm/10000,plus:core.sigmaPpm/10000,description:iceCoreCO2.error},method:tx('earthModels.compuestoAntarticoBereiter2015MuestraReal',{co2ppm:core.co2ppm,ageBP:core.ageBP,sigmaPpm:core.sigmaPpm}),sourceId:'ice-core-co2',scope:'nearest-published-gas-sample',interpolation:'none'};
 const p=policy==='reconstruction'?phandaAt(year):undefined;
 if(p&&(field==='meanTemperature'||field==='carbonDioxide')){
  const values=field==='meanTemperature'?p.temperature:p.co2ppm,scale=field==='carbonDioxide'?1/10000:1;
  return{id:'phanda-'+field+'-'+p.stage,field,value:values['50']*scale,unit:field==='meanTemperature'?'°C':'%',reference:{basis:'Ma',ageMa:p.referenceMa,nominalEpoch:1950},availableFromYear:yearFromAge(p.oldestMa*1e6),validUntilYear:yearFromAge(p.youngestMa*1e6)-1,evidence:'model',quantity:field==='meanTemperature'?'global-mean-surface-temperature':'volume-fraction',uncertainty:{minus:(values['50']-values['16'])*scale,plus:(values['84']-values['50'])*scale,description:tx('earthModels.medianaYPercentiles1684De')},method:tx('earthModels.phandaIntervaloPropioMaMediana',{youngestMa:p.youngestMa,oldestMa:p.oldestMa,stage:p.stage}),sourceId:'phanda',scope:'published-reconstruction-bin',interpolation:'none'};
 }
 const s=videoScenarioAt(year);if(!s)return;
 let value:number|{min:number;max:number}|null|undefined=field==='meanTemperature'?s.temperatureC:field==='solarDay'?s.solarDayHours:(s.gases as Partial<Record<string,number>>)[field];
 if(value===undefined||value===null)return;
 if(value===0&&field!=='meanTemperature'&&field!=='solarDay')value={min:0,max:.005};
 return{id:'video-scenario-'+field+'-'+s.seconds,field,value,unit:field==='meanTemperature'?'°C':field==='solarDay'?'h':'%',reference:{basis:'Ma',ageMa:s.ageMa,nominalEpoch:1950},availableFromYear:yearFromAge(s.ageMa*1e6),evidence:'illustrative-scenario',quantity:field==='meanTemperature'?'author-temperature-scenario':field==='solarDay'?'author-solar-day-scenario':'author-gas-fraction',uncertainty:null,method:tx('earthModels.escenarioDelAutorMuestraS',{seconds:s.seconds,ageMa:s.ageMa,dayRaw:s.dayRaw}),sourceId:'video-scenario',scope:'illustrative-author-reference',interpolation:'none'};
}
