import type {FeatureCollection} from 'geojson';
export type Observation=[number,number];
export type Profile={name:string;englishName?:string;official?:string;capital:string;coordinates?:number[];region?:string;continent?:string;subregion?:string;income?:string;territoryType?:string;sovereign?:string;series:Record<string,Observation[]>};
export type ProfileData={retrieved:string;codes?:Record<string,string>;countries:Record<string,Profile>};
export const profileFor=(data:ProfileData,code:string)=>data.countries[data.codes?.[code]??code];
export type Theme='political'|'gdp'|'gdpPerCapita'|'population';
export const themeLabels:Record<Theme,string>={political:'Territorios y dependencias',gdp:'PIB total · US$ corrientes',gdpPerCapita:'PIB por habitante · US$ corrientes',population:'Población · habitantes'};
export function observation(profile:Profile|undefined,metric:string,year:number):Observation|undefined{
  return profile?.series[metric]?.filter(o=>o[0]<=year&&o[0]>=year-5&&Number.isFinite(o[1])&&o[1]>=0).sort((a,b)=>b[0]-a[0])[0];
}
export function thematicData(data:FeatureCollection,profiles:ProfileData,theme:Theme,year:number):FeatureCollection{
  return {...data,features:data.features.map(f=>{
    const p=f.properties??{};const stat=theme==='political'?undefined:observation(profileFor(profiles,p.code),theme,year);
    return {...f,properties:{...p,metric:stat?.[1]??null,metricYear:stat?.[0]??null}};
  })};
}
export const escapeHtml=(value:unknown)=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const number=(n:number,digits=0)=>new Intl.NumberFormat('es',{maximumFractionDigits:digits}).format(n);
export function factRows(p:Profile|undefined,year:number){
  if(!p)return '';
  const metrics=[['population','Población','hab.'],['gdp','PIB nominal','US$'],['gdpPerCapita','PIB por habitante','US$'],['area','Superficie','km²'],['lifeExpectancy','Esperanza de vida','años'],['urban','Población urbana','%']];
  return metrics.flatMap(([key,label,unit])=>{const o=observation(p,key,year);return o?[`<div><dt>${label} <small>${o[0]}</small></dt><dd>${number(o[1],key==='lifeExpectancy'||key==='urban'?1:0)} <span>${unit}</span></dd></div>`]:[];}).join('');
}
export function thematicLegend(data:FeatureCollection,theme:Theme){
  if(theme==='political')return '';
  const years=data.features.flatMap(f=>typeof f.properties?.metricYear==='number'?[f.properties.metricYear]:[]);
  const range=years.length?`${Math.min(...years)}${Math.max(...years)!==Math.min(...years)?'–'+Math.max(...years):''}`:'sin observaciones';
  return `<strong>${themeLabels[theme]}</strong><div class="legend-ramp"></div><div class="legend-extremes"><span>Menor</span><span>Mayor</span></div><small>Banco Mundial · datos ${range}<br>Gris: sin dato · sin extrapolaciones</small>`;
}
