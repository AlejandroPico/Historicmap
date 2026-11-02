import phanda from '../Tierra/Fanerozoico/phanda.json' with {type:'json'};
import reference from '../Tierra/Fanerozoico/referencia-audiovisual.json' with {type:'json'};
import{deepAge}from'./deep-earth';
import{yearFromAge}from'./dates';
import type{PlanetField,PlanetRecord}from'./planet';
import{prehistoricCO2,iceCoreCO2}from'./ice-core-co2';
export type EvidencePolicy='reconstruction'|'video';
export const physicalSources={phanda:{name:'Judd et al.2024 · PhanDA · mediana y percentiles',url:'https://doi.org/10.1126/science.adk3705',retrieved:'2026-11-02',version:phanda.commit},'video-scenario':{name:'Algol · escenario numérico audiovisual',url:reference.url,retrieved:'2026-11-02',version:'31 puntos seleccionados; referencia ilustrativa, no consenso'},'ice-core-co2':{name:'Bereiter et al.2015 · CO₂ en testigos antárticos · NOAA NCEI',url:iceCoreCO2.source,retrieved:'2026-11-02',version:'Compuesto original de1901 muestras; edad del gas BP1950'}};
export const phandaBins=phanda.bins;
export function phandaAt(year:number){const age=deepAge(year);return age>=7?phanda.bins.find(b=>age>b.youngestMa&&age<=b.oldestMa):undefined;}
export function videoScenarioAt(year:number){const age=deepAge(year);return age>=7&&age<=4540.01?reference.samples.reduce((a,b)=>Math.abs(a.ageMa-age)<=Math.abs(b.ageMa-age)?a:b):undefined;}
export function physicalRecord(field:PlanetField,year:number,policy:EvidencePolicy='reconstruction'):PlanetRecord|undefined{
 const core=policy==='reconstruction'&&field==='carbonDioxide'?prehistoricCO2(year):undefined;
 if(core)return{id:'ice-core-co2-'+core.ageBP,field,value:core.co2ppm/10000,unit:'%',reference:{basis:'BP1950',ageYears:core.ageBP},availableFromYear:Math.ceil(yearFromAge(iceCoreCO2.rows.at(-1)!.ageBP)),validUntilYear:-10001,evidence:'observation-synthesis',quantity:'volume-fraction',uncertainty:{minus:core.sigmaPpm/10000,plus:core.sigmaPpm/10000,description:iceCoreCO2.error},method:`Compuesto antártico Bereiter2015, muestra real más cercana: ${core.co2ppm}ppm a${core.ageBP} años BP1950; ±${core.sigmaPpm}ppm (1σ, según la colección). Edad del gas publicada, no edad del hielo. Sin interpolación o extrapolación; no proporciona temperatura global.`,sourceId:'ice-core-co2',scope:'nearest-published-gas-sample',interpolation:'none'};
 const p=policy==='reconstruction'?phandaAt(year):undefined;
 if(p&&(field==='meanTemperature'||field==='carbonDioxide')){
  const values=field==='meanTemperature'?p.temperature:p.co2ppm,scale=field==='carbonDioxide'?1/10000:1;
  return{id:'phanda-'+field+'-'+p.stage,field,value:values['50']*scale,unit:field==='meanTemperature'?'°C':'%',reference:{basis:'Ma',ageMa:p.referenceMa,nominalEpoch:1950},availableFromYear:yearFromAge(p.oldestMa*1e6),validUntilYear:yearFromAge(p.youngestMa*1e6)-1,evidence:'model',quantity:field==='meanTemperature'?'global-mean-surface-temperature':'volume-fraction',uncertainty:{minus:(values['50']-values['16'])*scale,plus:(values['84']-values['50'])*scale,description:'Mediana y percentiles16–84 de PhanDA; no intervalo anual.'},method:`PhanDA, intervalo propio ${p.youngestMa}–${p.oldestMa}Ma (${p.stage}). Mediana y percentiles16–84 de la reconstrucción por asimilación de datos. CO₂ original enppm, convertido a porcentaje por10000. No interpolación anual ni equivalencia entre sus límites y la carta ICS2026.`,sourceId:'phanda',scope:'published-reconstruction-bin',interpolation:'none'};
 }
 const s=videoScenarioAt(year);if(!s)return;
 let value:number|{min:number;max:number}|null|undefined=field==='meanTemperature'?s.temperatureC:field==='solarDay'?s.solarDayHours:(s.gases as Partial<Record<string,number>>)[field];
 if(value===undefined||value===null)return;
 if(value===0&&field!=='meanTemperature'&&field!=='solarDay')value={min:0,max:.005};
 return{id:'video-scenario-'+field+'-'+s.seconds,field,value,unit:field==='meanTemperature'?'°C':field==='solarDay'?'h':'%',reference:{basis:'Ma',ageMa:s.ageMa,nominalEpoch:1950},availableFromYear:yearFromAge(s.ageMa*1e6),evidence:'illustrative-scenario',quantity:field==='meanTemperature'?'author-temperature-scenario':field==='solarDay'?'author-solar-day-scenario':'author-gas-fraction',uncertainty:null,method:`Escenario del autor, muestra${s.seconds}s a${s.ageMa}Ma; punto cercano, no interpolación ni medida. La precisión impresa del vídeo no acredita exactitud. Cero gaseoso redondeado se lee<0,005%. Mezcla húmeda/seca y presión no especificadas; no se normalizan porcentajes. El día procede de «${s.dayRaw}».`,sourceId:'video-scenario',scope:'illustrative-author-reference',interpolation:'none'};
}
