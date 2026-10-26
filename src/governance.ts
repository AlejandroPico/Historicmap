import forms from '../public/data/governance.json';
import regimes from '../public/data/regimes-of-world.json';
import type {FeatureCollection} from 'geojson';
import {escapeHtml as esc} from './profiles';

export type GovernmentTag={id:string;label:string;group:string;parents:string[]};
export type GovernmentRecord={keys:string[];start:number;end:number;tags:string[];source:string;sourceLabel:string;note?:string;priority?:number};
export const governmentTags=forms.taxonomy as GovernmentTag[];
const byTag=new Map(governmentTags.map(t=>[t.id,t]));
const byKey=new Map<string,GovernmentRecord[]>();
for(const r of forms.records as GovernmentRecord[])for(const key of r.keys)byKey.set(key,[...(byKey.get(key)??[]),r]);
const regimeSeries=regimes.series as Record<string,number[][]>;
export function expandGovernmentTags(tags:string[]):string[]{
 const result=new Set<string>();
 const add=(id:string)=>{if(result.has(id)||!byTag.has(id))return;result.add(id);for(const p of byTag.get(id)!.parents)add(p);};
 tags.forEach(add);return [...result];
}
const aliases:Record<string,string>={SUN:'USSR',AUH:'AUT-HUN',QNG:'QING',SSD:'SDS',ESH:'SAH',XKX:'KOS',PSE:'PSX'};
export function governmentFor(p:Record<string,any>,year:number){
 const raw=String(p.identityKey??p.entityCode??p.code??p.wikidata??'');const key=aliases[raw]??(byKey.has(raw)?raw:byKey.has('HIST-'+raw)?'HIST-'+raw:raw);
 const available=(byKey.get(key)??[]).filter(r=>r.start<=year&&r.end>=year);
 const overrides=available.filter(r=>r.priority);const records=overrides.length?overrides:available;
 const tags=records.flatMap(r=>r.tags);
 const dependent=!!p.administratorKey&&p.administratorKey!==key||['colony','protectorate','mandate','dependency','company-rule','contested-colony'].includes(String(p.status));
 if(dependent){tags.push('dependency');if(['colony','protectorate','mandate','company-rule'].includes(p.status))tags.push(p.status);}
 if(p.controlComponent&&p.kind==='war'||p.status==='occupied')tags.push('occupation');
 const observation=!dependent?regimeSeries[key]?.find(([a,b])=>a<=year&&b>=year)?.[2]:undefined;
 const regimeTag=observation===0?'closed-autocracy':observation===1?'electoral-autocracy':observation===2?'electoral-democracy':observation===3?'liberal-democracy':undefined;
 if(regimeTag)tags.push(regimeTag);
 if(!records.length&&!regimeTag)tags.push('unclassified');
 const expanded=expandGovernmentTags(tags);
 const leaf=expanded.filter(t=>!expanded.some(other=>byTag.get(other)?.parents.includes(t)));
 return {key,tags:expanded,labels:leaf.map(t=>byTag.get(t)!.label),records,regimeTag,regimeYear:regimeTag?year:undefined,dependent,known:!expanded.includes('unclassified')};
}
export function withGovernance(data:FeatureCollection,year:number):FeatureCollection{
 return {...data,features:data.features.map(f=>{const g=governmentFor(f.properties??{},year);return {...f,properties:{...f.properties,governmentTags:g.tags,governmentStatus:g.known?'documented':'unclassified',governmentReferenceYear:g.regimeYear??year}};})};
}
export function governmentCounts(data:FeatureCollection){
 const counts=new Map<string,Set<string>>();
 for(const f of data.features){const p=f.properties??{},key=String(p.identityKey??p.entityCode??f.id);for(const t of p.governmentTags??[]) {const set=counts.get(t)??new Set<string>();set.add(key);counts.set(t,set);}}
 return new Map([...counts].map(([k,v])=>[k,v.size]));
}
export function governanceMarkup(p:Record<string,any>,year:number){
 const g=governmentFor(p,year);
 const documented=g.tags.filter(t=>t!=='unclassified'&&t!==g.regimeTag&&!g.tags.some(other=>byTag.get(other)?.parents.includes(t)));
 const observations=g.records.length?`<div class="government-tags">${documented.map(id=>`<button class="secondary-button" data-government-filter="${esc(id)}">${esc(byTag.get(id)!.label)}</button>`).join('')}</div>`:'<p>Forma institucional pendiente de documentar para esta fecha.</p>';
 const assessment=g.regimeTag?`<p class="government-regime"><strong>${esc(byTag.get(g.regimeTag)!.label)}</strong> · observación de ${year}</p><a class="profile-source" href="${regimes.source}" target="_blank" rel="noopener">V-Dem / Regimes of the World · edición2026 ↗</a>`:g.dependent?'<p class="profile-note">Territorio dependiente: no se atribuye automáticamente la evaluación democrática del Estado administrador.</p>':year>regimes.endYear?`<p class="profile-note">La serie de evaluación política llega a ${regimes.endYear}; no se extrapola al año consultado.</p>`:'';
 const sources=[...new Map(g.records.map(r=>[r.source,r])).values()];
 return `<section class="government-record"><h3>Forma política · ${year}</h3>${observations}${assessment}${sources.map(r=>`<p class="profile-note">${esc(r.note??'Clasificación con vigencia documentada.')}</p><a class="profile-source" href="${esc(r.source)}" target="_blank" rel="noopener">${esc(r.sourceLabel)} ↗</a>`).join('')}<p class="profile-note">Forma institucional y evaluación del régimen son dimensiones distintas. Las etiquetas conservan su fecha y fuente.</p></section>`;
}
