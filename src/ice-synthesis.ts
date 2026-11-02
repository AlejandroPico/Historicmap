import older from'../public/data/ice-synthesis-index.json'with{type:'json'};
import{iceSampleFor,iceCaption,ageFromYear,iceModel}from'./ice-history';
export interface IceReference{file:string;ageBP:number;referenceYear:number;model:string;source:string;kind:'margin'|'interval-hypothesis';autoVisible?:boolean;youngestKa?:number;oldestKa?:number;label?:string;character?:string;uncertaintyFiles?:string[];scope:string}
export const olderIceModel=older;
export function displayIceSampleFor(year:number):IceReference|undefined{
 const recent=iceSampleFor(year);if(recent)return{...recent,model:iceModel.model,source:iceModel.source,kind:'margin',scope:'Cuatro regiones continentales · sin hielo marino ni cobertura completa de glaciares de montaña'};
 if(!Number.isInteger(year)||year===0)return;
 const age=ageFromYear(year)/1000,s=older.samples.find(s=>age>=s.youngestKa&&age<s.oldestKa);
 return s?{...s,label:s.folder,kind:'interval-hypothesis'}:undefined;
}
export function displayIceCaption(year:number){const s=displayIceSampleFor(year);return !s?'':s.kind==='margin'?iceCaption(year):`${s.model} · ${s.label}, ${s.youngestKa}–${s.oldestKa} ka BP1950. ${s.character==='peak-warmth'?'Síntesis del momento cálido':'Síntesis de la extensión máxima dentro del intervalo'}, no frente de este año. Sólo hemisferio norte; no incorpora Antártida ni hielo marino.`;}
