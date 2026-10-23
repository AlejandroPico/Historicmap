import {escapeHtml as esc,profileFor,type ProfileData,type Observation} from './profiles';

export type MetricSection='economy'|'society'|'defense'|'territory';
export type Indicator={label:string;unit:string;section:MetricSection;source:string;indicator:string;description:string;allowNegative?:boolean;provider?:string;license?:string};
export type IndicatorData={retrieved:string;referenceDate:string;source:string;license:string;indicators:Record<string,Indicator>;countries:Record<string,Record<string,Observation[]>>};
export const emptyIndicators:IndicatorData={retrieved:'',referenceDate:'',source:'',license:'',indicators:{},countries:{}};
export const baseIndicators:Record<string,Indicator>={
 population:{label:'Población',unit:'habitantes',section:'society',indicator:'SP.POP.TOTL',source:'https://data.worldbank.org/indicator/SP.POP.TOTL',description:'Población total de la serie del país.'},
 gdp:{label:'PIB nominal',unit:'US$ corrientes',section:'economy',indicator:'NY.GDP.MKTP.CD',source:'https://data.worldbank.org/indicator/NY.GDP.MKTP.CD',description:'Precios corrientes; las variaciones incorporan precios y tipos de cambio.'},
 gdpPerCapita:{label:'PIB por habitante',unit:'US$ corrientes',section:'economy',indicator:'NY.GDP.PCAP.CD',source:'https://data.worldbank.org/indicator/NY.GDP.PCAP.CD',description:'PIB nominal dividido por la población; no equivale al ingreso personal.'},
 area:{label:'Superficie',unit:'km²',section:'territory',indicator:'AG.SRF.TOTL.K2',source:'https://data.worldbank.org/indicator/AG.SRF.TOTL.K2',description:'Superficie de la serie estadística, no calculada sobre el polígono histórico.'},
 lifeExpectancy:{label:'Esperanza de vida',unit:'años',section:'society',indicator:'SP.DYN.LE00.IN',source:'https://data.worldbank.org/indicator/SP.DYN.LE00.IN',description:'Esperanza de vida al nacer, ambos sexos.'},
 urban:{label:'Población urbana',unit:'%',section:'society',indicator:'SP.URB.TOTL.IN.ZS',source:'https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS',description:'Porcentaje urbano según las definiciones nacionales.'}
};
export function metrics(data:IndicatorData){return {...baseIndicators,...data.indicators};}
export function seriesFor(code:string,metric:string,profiles:ProfileData,data:IndicatorData):Observation[]{
 const canonical=profiles.codes?.[code]??code;
 const profile=profileFor(profiles,code);
 // No profile/code means no series: dissolved states do not inherit successors.
 if(!profile)return [];
 const definition=metrics(data)[metric];
 return (profile.series[metric]??data.countries[canonical]?.[metric]??[]).filter(([y,v])=>Number.isInteger(y)&&Number.isFinite(v)&&(v>=0||definition?.allowNegative)).sort((a,b)=>a[0]-b[0]);
}
export function valueAt(series:Observation[],year:number):Observation|undefined{return series.filter(([y])=>y<=year&&y>=year-5).at(-1);}
export function formatMetric(value:number,definition:Indicator){
 const digits=definition.unit==='habitantes'||definition.unit==='personas'?0:definition.unit.includes('US$')?0:Math.abs(value)<100?2:1;
 return `${new Intl.NumberFormat('es',{maximumFractionDigits:digits}).format(value)} ${definition.unit}`;
}
export function metricRows(code:string,section:MetricSection,year:number,profiles:ProfileData,data:IndicatorData){
 return Object.entries(metrics(data)).filter(([,m])=>m.section===section).map(([key,m])=>{
  const o=valueAt(seriesFor(code,key,profiles,data),year);
  return `<div><dt><a href="${esc(m.source)}" target="_blank" rel="noopener" title="${esc(m.description)}">${esc(m.label)} ↗</a>${o?` <small>${o[0]}</small>`:''}</dt><dd>${o?esc(formatMetric(o[1],m)):'<span class="data-missing">Sin dato para esta fecha</span>'}</dd></div>`;
 }).join('');
}
export function metricOptions(data:IndicatorData,selected:string,section?:MetricSection){return Object.entries(metrics(data)).filter(([,m])=>!section||m.section===section).map(([key,m])=>`<option value="${esc(key)}" ${selected===key?'selected':''}>${esc(m.label)} · ${esc(m.unit)}</option>`).join('');}
export function trendChart(lines:{name:string;color:string;values:Observation[]}[],definition:Indicator,year:number){
 const clipped=lines.map(l=>({...l,values:l.values.filter(([y])=>y<=year)})),all=clipped.flatMap(l=>l.values);
 if(!all.length)return '<p class="profile-note">No hay observaciones documentadas hasta el año consultado.</p>';
 const first=Math.min(...all.map(o=>o[0])),last=Math.max(...all.map(o=>o[0]));
 let low=Math.min(...all.map(o=>o[1])),high=Math.max(...all.map(o=>o[1]));if(low===high){const pad=Math.max(1,Math.abs(low)*.1);low-=pad;high+=pad;}
 const x=(y:number)=>38+(y-first)/Math.max(1,last-first)*278,y=(v:number)=>132-(v-low)/(high-low)*104;
 const paths=clipped.map(l=>{
  let previous=-Infinity;let path='';for(const o of l.values){path+=`${o[0]===previous+1?'L':'M'}${x(o[0]).toFixed(2)},${y(o[1]).toFixed(2)} `;previous=o[0];}
  return `<path d="${path}" fill="none" stroke="${l.color}" stroke-width="2"/>${l.values.map(o=>`<circle cx="${x(o[0]).toFixed(2)}" cy="${y(o[1]).toFixed(2)}" r="2.8" fill="${l.color}" role="button" tabindex="0" data-jump-year="${o[0]}" aria-label="${esc(l.name)}: ${o[0]}, ${esc(formatMetric(o[1],definition))}. Ver año"><title>${esc(l.name)} · ${o[0]} · ${esc(formatMetric(o[1],definition))}</title></circle>`).join('')}`;
 }).join('');
 const table=clipped.map(l=>`<tbody><tr><th colspan="2">${esc(l.name)}</th></tr>${l.values.map(o=>`<tr><td><button class="text-action" data-jump-year="${o[0]}">${o[0]}</button></td><td>${esc(formatMetric(o[1],definition))}</td></tr>`).join('')}</tbody>`).join('');
 const compact=(value:number)=>esc(new Intl.NumberFormat('es',{notation:'compact',maximumFractionDigits:1}).format(value));
 const zero=low<0&&high>0?`<path d="M38 ${y(0).toFixed(2)}H316" class="chart-zero"/><text x="4" y="${(y(0)+3).toFixed(2)}">0</text>`:'';
 return `<figure class="trend-chart"><figcaption>${esc(definition.label)} <small>${esc(definition.unit)}</small></figcaption><svg viewBox="0 0 340 160" role="group" aria-label="${esc(definition.label)} de ${first} a ${last}. Valores disponibles en la tabla."><path d="M38 22V132H316" class="chart-axis"/>${zero}<text x="38" y="153">${first}</text><text x="285" y="153">${last}</text><text x="38" y="15">${compact(high)}</text><text x="2" y="136">${compact(low)}</text>${paths}</svg><div class="chart-legend">${clipped.map(l=>`<span><i style="background:${l.color}"></i>${esc(l.name)}</span>`).join('')}</div><details><summary>Ver observaciones y fechas</summary><table class="series-table"><caption>${esc(definition.label)} · sin interpolar años ausentes</caption>${table}</table></details><p class="profile-note">Banco Mundial · World Development Indicators.${definition.provider?` Proveedor: ${esc(definition.provider)}`:''}${definition.license?` · ${esc(definition.license)}`:''}</p><a class="profile-source" href="${esc(definition.source)}" target="_blank" rel="noopener">Definición y fuente del indicador ↗</a></figure>`;
}
export function indicatorSection(code:string,name:string,section:MetricSection,year:number,profiles:ProfileData,data:IndicatorData,metric?:string){
 const selected=metric&&metrics(data)[metric]?.section===section?metric:Object.keys(metrics(data)).find(k=>metrics(data)[k].section===section)??'population';
 return `<dl class="country-facts">${metricRows(code,section,year,profiles,data)}</dl><p class="profile-note">Última observación disponible hasta ${year}, con un retraso máximo de cinco años. Las series conservan el ámbito territorial de su fuente.</p><label class="workspace-field">Evolución<select data-trend-section="${section}">${metricOptions(data,selected,section)}</select></label>${trendChart([{name,color:'var(--chart-1)',values:seriesFor(code,selected,profiles,data)}],metrics(data)[selected],year)}`;
}
