import { tx } from './i18n';
import older from'../public/data/ice-synthesis-index.json'with{type:'json'};
import{iceSampleFor,iceCaption,ageFromYear,iceModel}from'./ice-history';
export interface IceReference{file:string;ageBP:number;referenceYear:number;model:string;source:string;kind:'margin'|'interval-hypothesis';autoVisible?:boolean;youngestKa?:number;oldestKa?:number;label?:string;character?:string;uncertaintyFiles?:string[];scope:string}
export const olderIceModel=older;
export function displayIceSampleFor(year:number):IceReference|undefined{
 const recent=iceSampleFor(year);if(recent)return{...recent,model:iceModel.model,source:iceModel.source,kind:'margin',scope:tx('iceSynthesis.cuatroRegionesContinentalesSinHielo')};
 if(!Number.isInteger(year)||year===0)return;
 const age=ageFromYear(year)/1000,s=older.samples.find(s=>age>=s.youngestKa&&age<s.oldestKa);
 return s?{...s,label:s.folder,kind:'interval-hypothesis',scope:tx('iceSynthesis.sintesisDeMantosContinentalesDel')}:undefined;
}
export function displayIceCaption(year:number){const s=displayIceSampleFor(year);return !s?'':s.kind==='margin'?iceCaption(year):tx('iceSynthesis.kaBp1950NoFrenteDe',{model:s.model,label:s.label,youngestKa:s.youngestKa,oldestKa:s.oldestKa,v4:s.character==='peak-warmth'?tx('iceSynthesis.sintesisDelMomentoCalido'):tx('iceSynthesis.sintesisDeLaExtensionMaxima')});}
export function iceAvailabilityNote(year:number,visible:boolean){
 const reference=displayIceSampleFor(year);
 if(!reference)return tx('iceSynthesis.paleomistTerminaEn80000bp1950Y');
 const state=visible?'':reference.kind==='interval-hypothesis'?tx('iceSynthesis.hipotesisGlacialDisponibleNoActivada'):tx('iceSynthesis.referenciaPaleomistDisponibleNoActivada');
 return state+displayIceCaption(year)+' '+reference.scope+tx('iceSynthesis.noPaleocostaDetallada');
}
