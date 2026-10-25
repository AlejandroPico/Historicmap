/** Exercise the production acquisition/resolution path with local asset reads. */
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {annualData,overlaysFor} from '../src/data';
import {politicalData} from '../src/political';
import {composeControl} from '../src/control-map';
import {identityFor,type IdentityData} from '../src/identities';
const read=(f:string)=>JSON.parse(readFileSync('public/data/'+f,'utf8'));
globalThis.fetch=async(input:any)=>new Response(readFileSync('public/data/'+String(input).split('/').at(-1)!),{status:200});
const identities:IdentityData=read('identities.json'),profiles=read('profiles.json');
const years:any[]=[],missing:any[]=[],photos=new Map<string,any>(),symbols:any[]=[];
for(let year=1880;year<=1899;year++){
 const base=politicalData(await annualData(year),year,profiles),world=composeControl(base,await overlaysFor(year),year).territories;
 if(process.argv.includes('--inspect')&&[1886,1897,1898].includes(year))console.log(year,base.features.filter(f=>/Hawa|Swazi/i.test(String(f.properties?.originalName))).map(f=>({id:f.id,...f.properties,geometry:undefined})),world.features.filter(f=>f.properties?.identityKey==='HAW').map(f=>({id:f.id,polygons:(f.geometry as any).coordinates.length})));
 let gap=0,withAuthorities=0;
 for(const f of world.features){
  const p=f.properties!,id=identityFor(p,year,identities,new Date(2026,9,25));
  if(!id.leaders.length&&!id.territoryStatus){missing.push({year,name:p.name,sourceName:p.originalName,key:id.key,status:p.status,administrator:p.administratorKey});gap++;}else withAuthorities++;
  if(!id.flag)symbols.push({year,name:p.name,key:id.key});
  for(const l of id.leaders)if(!l.portrait)photos.set(l.person,{person:l.person,name:l.name,key:id.key,year});
 }
 years.push({year,territories:world.features.length,withSomeAuthorityOrDocumentedAbsence:withAuthorities,missingAuthorities:gap});
}
mkdirSync('.cache',{recursive:true});
const result={scope:'Annual production-path availability audit; availability is not a complete office census or geographic front validation.',years,missingAuthorities:missing,missingPortraits:[...photos.values()],missingSymbols:symbols};
writeFileSync('.cache/review-1880.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({countryYears:years.reduce((n,y)=>n+y.territories,0),missingAuthorities:missing.length,missingPortraits:photos.size,missingSymbols:symbols.length,missingNames:[...new Set(missing.map(p=>p.key+': '+p.name))]}));
