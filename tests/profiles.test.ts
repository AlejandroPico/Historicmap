import {readFileSync} from 'node:fs';
import {describe,it,expect} from 'vitest';
import {profileFor,observation,type ProfileData} from '../src/profiles';
const data:ProfileData=JSON.parse(readFileSync(new URL('../public/data/profiles.json',import.meta.url),'utf8'));
describe('country metadata joins',()=>{
 it('does not let dependencies or disputed territories overwrite their associated state',()=>{
  for(const [code,name] of [['BRA','Brazil'],['FRA','France'],['AUS','Australia'],['KAZ','Kazakhstan']])expect(profileFor(data,code)?.englishName).toBe(name);
  for(const [territory,state] of [['BRI','BRA'],['CLP','FRA'],['ATC','AUS'],['CSI','AUS'],['IOA','AUS'],['KAB','KAZ']]){
   expect(profileFor(data,territory)).not.toBe(profileFor(data,state));
   expect(observation(profileFor(data,territory),'gdp',2026)).toBeUndefined();
   expect(observation(profileFor(data,state),'gdp',2026)).toBeDefined();
  }
 });
 it('retains only explicit equivalent-entity aliases',()=>{
  for(const [map,iso] of [['PSX','PSE'],['SDS','SSD'],['SAH','ESH'],['KOS','XKX'],['ALD','ALA']])expect(profileFor(data,map)).toBe(data.countries[iso]);
  expect(profileFor(data,'-99')).toBeUndefined();
 });
});
