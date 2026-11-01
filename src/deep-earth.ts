import catalog from '../Tierra/Precambrico/escenarios.json' with {type:'json'};
import bibliography from '../Tierra/Precambrico/fuentes.json' with {type:'json'};
import {yearFromAge} from './dates';
export interface DeepScene {id:string;title:string;oldestMa:number;youngestMa:number;mode:string;ocean:string;land:string;landFraction:number;atmosphere:string;life:string;ice:string|null;article:string;sourceIds:string[];geometry:string;visualStatus:string}
export const deepScenes=catalog.scenes as DeepScene[];
export const deepSources=bibliography.sources;
export const deepAge=(year:number)=>(1950-(year<0?year+1:year))/1e6;
export function deepSceneAt(year:number){const age=deepAge(year);return deepScenes.find(s=>age<=s.oldestMa&&age>s.youngestMa);}
export function deepIceAt(year:number){const scene=deepSceneAt(year);if(!scene)return null;return scene.ice??catalog.regionalIce.find(r=>deepAge(year)<=r.oldestMa&&deepAge(year)>r.youngestMa)?.id??null;}
/** Polar areas beyond the Mercator texture must honour the same ice control. */
export function deepBackground(year:number,showIce=true){const scene=deepSceneAt(year);return scene?(showIce&&deepIceAt(year)==='snowball'?'#d8e7e7':scene.ocean):undefined;}
export const sceneYear=(scene:DeepScene)=>Math.max(-4540000000,yearFromAge((scene.oldestMa+scene.youngestMa)*.5e6));
/** These are visual design colours; the source ICS colour is never overwritten. */
const colours:Record<string,string>={Hadean:'#b75b2c',Archean:'#226f75',Eoarchean:'#487b96',Paleoarchean:'#488f75',Mesoarchean:'#a88938',Neoarchean:'#7c668d',Proterozoic:'#405e9b',Paleoproterozoic:'#a86a3d',Mesoproterozoic:'#2f8887',Neoproterozoic:'#77639b',Siderian:'#8d5944',Rhyacian:'#6d7d39',Orosirian:'#3e8095',Statherian:'#8b5684',Calymmian:'#387d7c',Ectasian:'#9b7e30',Stenian:'#5271a5',Tonian:'#7862a5',Cryogenian:'#578caa',Ediacaran:'#55856c'};
export const chronologyDisplayColor=(id:string,source:string)=>colours[id]??source;
