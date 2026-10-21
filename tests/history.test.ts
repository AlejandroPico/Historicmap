import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {historyAt,periodsAt,historicalCapitals,type HistoryTopology} from '../src/history';
import {observation,profileFor,type ProfileData} from '../src/profiles';
import type {FeatureCollection} from 'geojson';
const json=(f:string)=>JSON.parse(readFileSync(new URL('../public/data/'+f,import.meta.url),'utf8'));
const topology:HistoryTopology=json('history.topojson');
const overlays:FeatureCollection=json('territorial-overlays.geojson');
const war:FeatureCollection=json('ww2.geojson');
const profiles:ProfileData=json('profiles.json');
const active=(name:string,year:number)=>historyAt(topology,year).features.find(f=>f.properties?.originalName===name)!;
describe('annual territorial audit',()=>{
 it('resolves country code differences without merging unknown territorial identities',()=>{
   const current:FeatureCollection=json('countries.geojson');
   expect(profiles.countries['-99']).toBeUndefined();
   for(const f of current.features)expect(profileFor(profiles,f.properties!.code),f.properties!.name).toBeDefined();
   expect(profileFor(profiles,'KOS')?.series.population?.length).toBeGreaterThan(0);
 });
 it('has one active period per entity for each year 1900–2019',()=>{
   for(let year=1900;year<=2019;year++){
     const rows=periodsAt(topology,year).map(g=>g.properties);
     expect(rows.length,`coverage ${year}`).toBeGreaterThan(140);
     expect(new Set(rows.map(p=>p.gwcode)).size,`duplicate entity ${year}`).toBe(rows.length);
     expect(rows.find(p=>p.country_name==='United States of America')?.capname).toBe('Washington');
   }
 });
 it('keeps prewar Germany and Poland distinct from postwar entities',()=>{
   expect(active('Germany (Prussia)',1942).properties?.name).toBe('Alemania nazi');
   expect(historyAt(topology,1942).features.some(f=>f.properties?.originalName==='German Democratic Republic')).toBe(false);
   expect(active('German Democratic Republic',1945).properties?.name).toContain('zona de ocupación');
   expect(active('German Democratic Republic',1950).properties?.name).toBe('República Democrática Alemana');
   expect(active('German Federal Republic',1990).properties?.name).toBe('Alemania');
   const germany=war.features.filter(f=>f.properties?.originalName==='Nazi Germany');
   for(let y=1938;y<=1944;y++)expect(germany.filter(f=>f.properties!.start<=y&&f.properties!.end>=y)).toHaveLength(1);
   expect(new Set(germany.map(f=>JSON.stringify(f.geometry))).size).toBe(germany.length);
 });
 it('represents British India, French Algeria and their independence',()=>{
   expect(active('India',1946).properties).toMatchObject({status:'colony',ownerName:'Reino Unido'});
   expect(active('India',1947).properties).toMatchObject({status:'independent',capital:'New Delhi (Delhi)'});
   expect(active('Algeria',1961).properties?.ownerName).toBe('Francia');
   expect(active('Algeria',1963).properties?.status).toBe('independent');
   expect(active('Egypt',1915).properties).toMatchObject({status:'protectorate',ownerName:'Reino Unido'});
   expect(active('Egypt',1923).properties?.status).toBe('independent');
 });
 it('preserves Egyptian/Syrian territory and separates occupation geometry',()=>{
   expect(active('Egypt',1968).geometry).toEqual(active('Egypt',1966).geometry);
   expect(active('Israel',1968).geometry).toEqual(active('Israel',1966).geometry);
   expect(active('Syria',1968).geometry).toEqual(active('Syria',1966).geometry);
   const at=(y:number)=>overlays.features.filter(f=>f.properties!.start<=y&&f.properties!.end>=y).map(f=>f.properties!.uid);
   expect(at(1966)).not.toContain('sinai');expect(at(1967)).toContain('sinai');
   expect(at(1981)).toContain('sinai-withdrawal');expect(at(1982)).not.toContain('sinai-withdrawal');
   expect(at(2013)).not.toContain('crimea');expect(at(2014)).toContain('crimea');
   expect(overlays.features.find(f=>f.properties!.uid==='crimea')?.properties?.note).toContain('Territorio de Ucrania');
 });
 it('uses historic capitals and includes the contemporary world city network',()=>{
   const capitals=historicalCapitals(historyAt(topology,1942));expect(capitals.features.length).toBeGreaterThan(120);
   expect(capitals.features.some(f=>f.properties?.name==='Washington')).toBe(true);
   const cities:FeatureCollection=json('cities.geojson');expect(cities.features).toHaveLength(323);
   for(const code of ['USA','RUS','JPN','CHN','IND'])expect(cities.features.some(f=>f.properties?.code===code&&f.properties?.capital)).toBe(true);
   expect(cities.features.some(f=>f.properties?.name==='Nueva York')).toBe(true);
 });
 it('never substitutes future statistics or unrelated successor-state observations',()=>{
   expect(observation(profiles.countries.USA,'gdp',1942)).toBeUndefined();
   const o=observation(profiles.countries.USA,'gdp',2026);expect(o?.[0]).toBeLessThanOrEqual(2026);expect(o?.[1]).toBeGreaterThan(1e12);
   expect(active('Russia (Soviet Union)',1980).properties?.code).toBe('');
   expect(observation({name:'test',capital:'',series:{population:[[2027,100],[2020,50]]}},'population',2026)).toBeUndefined();
 });
 it('preserves a reported zero instead of treating it as missing',()=>{
   expect(observation({name:'test',capital:'',series:{urban:[[2025,0]]}},'urban',2026)).toEqual([2025,0]);
 });
});
