import {describe,it,expect} from 'vitest';
import {readFileSync} from 'node:fs';
import {historyAt,historicalCapitals,normalizedName,type HistoryTopology} from '../src/history';
import {anchorFor,matchingFeature} from '../src/selection';
import {seriesFor,valueAt,metrics,trendChart,type IndicatorData} from '../src/country-workspace';
import {countryTimeline,recordsFor,relatedEntities,type CountryHistory} from '../src/country-history';
import {countryCard} from '../src/country-card';
import type {IdentityData} from '../src/identities';
import type {ProfileData} from '../src/profiles';
import {comparisonMarkup} from '../src/country-comparison';
const read=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const profiles:ProfileData=read('profiles.json'),identities:IdentityData=read('identities.json'),indicators:IndicatorData=read('country-indicators.json'),history:CountryHistory=read('country-history.json'),topology:HistoryTopology=read('history.topojson');
const names=new Map<string,string>(Object.entries(profiles.countries).flatMap(([code,p])=>[p.name,p.englishName,p.official].filter(Boolean).map(n=>[normalizedName(n!),code] as [string,string])));
const at=(year:number)=>historyAt(topology,year,names);
describe('persistent country workspace',()=>{
 it('tracks a country across changing period IDs without replacing extinct entities with successors',()=>{
  const a=at(1990),b=at(2000),esp=a.features.find(f=>f.properties?.code==='ESP')!;
  const anchor=anchorFor(esp.properties!,1990,identities);
  expect(matchingFeature(anchor,b,2000,identities)?.properties?.code).toBe('ESP');
  const soviet=anchorFor(a.features.find(f=>f.properties?.identityKey==='USSR')!.properties!,1990,identities);
  expect(matchingFeature(soviet,at(1992),1992,identities)).toBeUndefined();
  expect(matchingFeature(soviet,a,1990,identities)?.properties?.identityKey).toBe('USSR');
  const control=read('recent-control.geojson').features[0];
  expect(matchingFeature(anchorFor(control.properties,1990,identities),b,2000,identities)).toBeUndefined();
  const paris=anchorFor({name:'París',country:'France',code:'FRA',rank:1},2026,identities);
  expect(matchingFeature(paris,historicalCapitals(a),1990,identities)?.properties?.country).toBe('Francia');
 });
 it('retains signed observations, real years and historical identity boundaries',()=>{
  const values=seriesFor('USA','gdpGrowth',profiles,indicators);
  expect(values.some(([y,v])=>y===2009&&v<0)).toBe(true);
  expect(valueAt(values,2009)?.[0]).toBe(2009);
  expect(valueAt([[2000,1]],2006)).toBeUndefined();
  expect(seriesFor('USSR','population',profiles,indicators)).toEqual([]);
  expect(seriesFor('SDS','armedForces',profiles,indicators)).toEqual(seriesFor('SSD','armedForces',profiles,indicators));
  expect(valueAt(seriesFor('USA','armedForces',profiles,indicators),2026)).toBeUndefined();
 });
 it('charts gaps without connecting them and never includes future observations',()=>{
  const chart=trendChart([{name:'Example',color:'#ffffff',values:[[1990,-2],[1992,3],[1993,4],[2000,9]]}],metrics(indicators).gdpGrowth,1993);
  expect(chart).toContain('data-jump-year="1990"');expect(chart).toContain('data-jump-year="1993"');
  expect(chart).not.toContain('data-jump-year="2000"');expect(chart.match(/<circle /g)).toHaveLength(3);
  expect(chart).toMatch(/d="M[^"]*M[^"]*L/);
  expect(chart).toContain('class="chart-zero"');expect(chart).toContain('role="group"');
 });
 it('offers sourced successor navigation and institutional records with exclusive ends',()=>{
  expect(relatedEntities('USSR',history)).toHaveLength(15);
  expect(relatedEntities('CSK',history).map(r=>r.to.key).sort()).toEqual(['CZE','SVK']);
  expect(history.relations.every(r=>identities.countries[r.from.key]&&identities.countries[r.to.key])).toBe(true);
  for(const r of history.records.filter(r=>r.end))expect(recordsFor(r.keys[0],r.section,Number(r.end!.slice(0,4))+1,history)).not.toContain(r);
 });
 it('keeps all sections available when the country is absent, with no successor statistics',()=>{
  const p=at(1990).features.find(f=>f.properties?.identityKey==='USSR')!.properties!;
  const markup=countryCard(p,1992,{kind:'annual',year:1992},profiles,identities,'/',{available:false,key:'USSR',history,indicators});
  expect(markup).toContain('entidad no tiene una representación territorial activa');
  expect(markup).toContain('data-entity-key="RUS"');expect(markup).toContain('id="tab-comparison"');
  expect(markup).not.toContain('Retrato de');
  const finalYear=countryCard(p,1991,{kind:'annual',year:1991},profiles,identities,'/',{available:false,key:'USSR',history,indicators});
  expect(finalYear).toContain('Gorbachov');
  const russia=countryCard({code:'RUS',name:'Rusia'},1990,{kind:'annual',year:1990},profiles,identities,'/',{available:false,key:'RUS',history,indicators});
  expect(russia).not.toContain('Retrato de Mijaíl Gorbachov');
 });
 it('builds an event chronology from dated sources rather than present-day memberships',()=>{
  const p=at(1990).features.find(f=>f.properties?.identityKey==='USSR')!.properties!;
  const entries=countryTimeline(p,1990,identities,history);
  expect(entries.some(e=>e.title.includes('Gorbachov'))).toBe(true);
  expect(entries.every(e=>e.source.startsWith('https://'))).toBe(true);
  expect(entries.some(e=>e.title.includes('OTAN'))).toBe(false);
 });
 it('compares percentage-of-GDP observations in percentage points with their actual years',()=>{
  const small:ProfileData={retrieved:'2026-10-23',countries:{USA:{name:'Estados Unidos',capital:'Washington',series:{exports:[[2000,30],[2010,20]]}}}};
  const p={code:'USA',name:'Estados Unidos'},anchor=anchorFor(p,2010,identities),feature={type:'Feature' as const,properties:p,geometry:{type:'Point' as const,coordinates:[0,0]}};
  const html=comparisonMarkup([{anchor,year:2000,feature},{anchor,year:2010,feature}],{mode:'dates',a:2000,b:2010,metric:'exports',pinned:[]},small,indicators,identities,'/',2010);
  expect(html).toContain('-10 puntos porcentuales del PIB');expect(html).toContain('Dato de 2000');expect(html).toContain('Dato de 2010');
 });
});
