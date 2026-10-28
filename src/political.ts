import {isoYear} from './dates';
import type {FeatureCollection} from 'geojson';
import {hashColor,territorialEntityCode} from './history';
import influenceCatalogue from '../public/data/political-influence.json';
import type {ProfileData} from './profiles';
import {historicalFamily,historicalColor} from './historical-palette';

export type PoliticalInfluence={id:string;keys:string[];power:string;start:string;end:string;kind:string;source:string;note:string;hatchScope?:'national-reference';label?:string};
export const politicalInfluences=influenceCatalogue.records as PoliticalInfluence[];
export function influenceFor(key:string,year:number){
  const date=`${isoYear(year)}-12-31`;
  return politicalInfluences.find(r=>r.keys.includes(key)&&r.start<=date&&r.end>date);
}
/** A stable tint identifies a dependency without erasing its separate identity. */
export function dependencyColor(color:string,key:string,soft=false){
  const amount=(soft ? .37 : .18)+(hashColor(key)%5)*.025;
  return '#'+[1,3,5].map(i=>Math.round(parseInt(color.slice(i,i+2),16)*(1-amount)+255*amount).toString(16).padStart(2,'0')).join('');
}

const palette=['#78938a','#af9c77','#658e98','#9c887a','#9ba783','#b39c80','#7b929d','#a6a386','#8f9c8d','#9e8883','#819c9f','#b5a48a'];
const families:Record<string,string>={
  'United States of America':'USA','United States':'USA','Estados Unidos':'USA',
  'Egypt':'EGY','Egipto':'EGY',
  'Spain':'ESP','España':'ESP','Kingdom of Spain':'ESP','Spanish Empire':'ESP','First Spanish Republic':'ESP','Francoist Spain':'ESP',
  'Second Spanish Republic':'ESP-REPUBLIC','Spanish Nationalists':'ESP-NATIONALIST',
  'Germany (Prussia)':'DEU','German Federal Republic':'DEU','German Democratic Republic':'DDR','Nazi Germany':'DEU','German Empire':'DEU','Kingdom of Prussia':'PRUSSIA',
  'Russia (Soviet Union)':'RUS','Russian Empire':'RUS','Union of Soviet Socialist Republics':'USSR',
  'France':'FRA','Francia':'FRA','Kingdom of France':'FRA','French First Republic':'FRA','French Directory':'FRA','French Consulate':'FRA','First French Empire':'FRA','Bourbon Kingdom of France':'FRA','July Monarchy':'FRA','French Second Republic':'FRA','Second French Empire':'FRA','French Third Republic':'FRA','French Fourth Republic':'FRA','French Fifth Republic':'FRA','Vichy France':'FRA-VICHY','Free French':'FRA-FREE',
  'United Kingdom':'GBR','Reino Unido':'GBR','Kingdom of Great Britain':'GBR','British Empire':'GBR',
  'Imperio alemán':'DEU','Alemania nazi':'DEU','Alemania':'DEU','Unión Soviética':'USSR','Imperio ruso':'RUS','Rusia soviética':'USSR','Rusia':'RUS','Italia':'ITA',
  'China':'CHN','Republic of China':'ROC','Communist Party of China':'CHN-COMMUNIST','Qing dynasty':'QING','Qing Dynasty':'QING',
  'Japan':'JPN','Empire of Japan':'JPN','Japón':'JPN','Italy/Sardinia':'ITA','Kingdom of Italy':'ITA','Italy':'ITA',
  'Independent State of Croatia':'CROATIA-CLIENT',
  'Austria-Hungary':'AUT-HUN','Austria-Hungría':'AUT-HUN','Turkey (Ottoman Empire)':'OTT','Ottoman Empire':'OTT','Imperio otomano':'OTT',
};
export function entityKey(p:Record<string,unknown>,year:number):string{
  if(p.identityKey)return String(p.identityKey);
  const name=String(p.originalName??p.country_name??p.name??'');
  let key=families[name]??historicalFamily(name)??String(p.code||p.wikidata||name);
  const codes:Record<string,string>={SSD:'SDS',XKX:'KOS',PSE:'PSX',ESH:'SAH'};
  key=codes[key]??key;
  if((p.gwcode===365||name==='Russia (Soviet Union)')&&year>=1922&&year<=1990)key='USSR';
  if(key==='ESP'&&year>=1931&&year<=1938)key='ESP-REPUBLIC';
  if(key==='CHN'&&year<1949)key=year>=1912?'ROC':'QING';
  if(name==='Turkey (Ottoman Empire)'&&year>=1923)key='TUR';
  if(key==='EGY'&&year>=1958&&year<=1960)key='UAR';
  return key;
}
/** Editorial colors identify political regimes, never inferred solely from a flag. */
export function regimeColor(key:string,year:number):string{
  switch(key){
    case 'DEU':return year>=1933&&year<=1944?'#50545a':year<=1917?'#747d89':year<=1932?'#8f886f':'#728b8f';
    case 'DDR':return year<1949?'#bd625d':'#a75558';
    case 'USSR':return '#c74743';
    case 'CHN-COMMUNIST':return year>=1949?'#d5b34b':'#a6784d';
    case 'RUS':return year<=1916?'#74966e':year<=1921?'#b95c54':'#9c7b9f';
    case 'RUE':return '#74966e';
    case 'CASTILE-COUNTY':return '#b39a73';case 'BUYID':return '#8ba394';case 'NORMANDY-DUCHY':return '#9c9e80';case 'ENGLAND':return year<1066?(year===1013||year>=1016&&year<=1041?'#ad9b76':'#789a9c'):historicalColor(key)??palette[hashColor(key)];case 'NORTHERN-SONG':return '#d1ba7f';case 'ARAGON-KINGDOM':return '#bda275';case 'PORTUGAL-COUNTY':return '#ae9680';case 'YUAN':return '#b6a476';case 'NORTHERN-YUAN':return '#c4b68c';case 'ILKHANATE':return '#a6aa83';case 'GOLDEN-HORDE':return '#ab9962';case 'GORYEO':return '#a99d6f';case 'MONGOL-EMPIRE':return '#b8aa79';case 'CHAGATAI':return '#aeb082';case 'NICAEA':return '#8163a5';case 'EPIRUS':return '#9a7baa';case 'LATIN-EMPIRE':return '#ab8c57';case 'CASTILE-KINGDOM':return '#c3a04f';case 'LEON-KINGDOM':return '#b2916e';case 'SOUTHERN-SONG':return '#c5ad72';case 'JIN-JURCHEN':return '#b39a60';case 'BYZANTINE':return '#70539c';case 'TREBIZOND':return '#8c6ba7';case 'BURGUNDY-DUCHY':return '#95616f';case 'GRANADA-EMIRATE':return '#a46159';case 'CASTILE':return '#c3a04f';case 'ARAGON':return '#c9ab62';case 'MUSCOVY':return '#7d9b72';case 'AZTEC':return '#8f7d53';case 'INCA':case 'NEO-INCA':return '#ad815f';case 'SUR':return '#9c8b62';case 'MING':return '#b16b55';case 'SOUTHERN-MING':return '#c68b70';case 'LATER-JIN':return '#a88a4d';case 'ENGLISH-COMMONWEALTH':return '#82936b';case 'SAADI':return '#aa775b';
    case 'BRA-EMPIRE':return '#b69852';
    case 'BRA':return year>=1889&&year<=1899?'#659a7e':historicalColor(key)??palette[hashColor(key)];
    case 'JOS':return '#bfa76a';
    case 'PRUSSIA':return '#627d9b';
    case 'AUSTRIAN-EMPIRE':return '#b8a367';
    case 'TWO-SICILIES':return '#b1a786';
    case 'PAPAL-STATES':return '#c7b777';
    case 'TEXAS':return '#709bab';
    case 'HTI':return year>=1849&&year<=1858?'#9c7188':historicalColor(key)??palette[hashColor(key)];
    case 'HAW-KINGDOM':return '#9b7b9e';
    case 'HAW-PROVISIONAL':return '#9c9281';
    case 'HAW-REPUBLIC':return '#a38b61';
    case 'HAW':return '#749aba';
    case 'RPR':return '#8d9c82';
    case 'RSR':return regimeColor('USSR',year);
    case 'YKM':return '#718db5';
    case 'USA':return '#4e89bd';
    case 'PRT':return year<=1909?'#5b8596':year<=1925?'#5b9b7c':year<=1973?'#638d73':'#71a895';
    case 'GBR':return '#b2789b';
    case 'CHN':return '#d5b34b';case 'ROC':return '#ddbe64';case 'QING':return '#bb9a46';
    case 'JPN':return year<=1945?'#c47b70':'#bd9d91';
    case 'FRA':return year<=1791?'#b9b4a1':year<=1794?'#789bab':year<=1799?'#6599ac':year<=1803?'#4b8baa':year<=1813?'#387cc1':year<=1829?'#adab91':year<=1847?'#7a9fbc':year<=1851?'#669ab9':year<=1869?'#456fa8':year<=1940?'#6796ad':year<=1945?'#5c91ad':year<=1957?'#729daa':'#6a9db1';
    case 'FRA-FREE':return '#528fbc';case 'FRA-VICHY':return '#9598a1';
    case 'ESP-REPUBLIC':return '#9b688f';case 'ESP-NATIONALIST':return '#b7914e';
    case 'ESP':return year>=1820&&year<=1822?'#b7a966':year>=1823&&year<=1832?'#a78a53':year===1873?'#a57a9c':year>=1923&&year<=1929?'#8f9365':year<=1930?'#c3a04f':year<=1975?'#b7914e':'#c2a880';
    case 'ITA':return year>=1922&&year<=1943?'#646f5d':year<=1945?'#8daa8c':'#75a38e';
    case 'PRUSSIA':return '#6f8290';case 'CROATIA-CLIENT':return '#96999d';
    case 'AUT-HUN':return '#ac8c64';case 'OTT':return '#9b5b64';
    case 'SVK-1939':return '#999ca1';
    default:return historicalColor(key)??palette[hashColor(key)];
  }
}
export function politicalData(data:FeatureCollection,year:number,profiles?:ProfileData):FeatureCollection{
  const colorFamilies=new Map(data.features.filter(f=>f.properties?.colorFamily).map(f=>[String(f.properties!.identityKey),String(f.properties!.colorFamily)]));
  const sovereignNames=new Map<string,string>();
  const sovereignLabels=new Map<string,string>();
  for(const f of data.features){const p=f.properties??{};if(p.status==='independent'||!p.status){const key=entityKey(p,year);if(p.name)sovereignLabels.set(key,String(p.name));for(const name of [p.name,p.originalName,...(profiles&&year>=2020?[p.group]:[])])if(name)sovereignNames.set(String(name),key);}}
  return {...data,features:data.features.map(f=>{
    const p=f.properties??{};const identityKey=entityKey(p,year);
    const profile=profiles&&year>=2020?profiles.countries[profiles.codes?.[p.code]??p.code]:undefined;
    // Only the source's dependency classification, never a disputed claimant
    // or the modern sovereign of an unrelated historical territory.
    const modernOwner=profile?.territoryType==='Dependency'&&profile.sovereign?sovereignNames.get(profile.sovereign):undefined;
    const modernDependency=!!modernOwner&&modernOwner!==identityKey;
    const parent=p.parentName??(year<1789&&!p.status&&p.group&&p.group!==p.name?p.group:undefined);
    const ownerKey=p.collectiveAdministration?identityKey:modernDependency?modernOwner!:p.administratorKey?String(p.administratorKey):p.status&&p.status!=='independent'&&p.ownerName?sovereignNames.get(String(p.ownerName))??entityKey({name:p.ownerName},year):parent?sovereignNames.get(String(parent))??entityKey({name:parent},year):identityKey;
    const name=identityKey==='FRA'&&(!p.parentName||p.parentName===p.originalName)&&!p.status&&year<1886?frenchName(year):p.name;
    const influence=influenceFor(identityKey,year);
    const dependent=!p.collectiveAdministration&&(modernDependency||!!(p.status&&p.status!=='independent'&&p.ownerName)||!!parent&&parent!==p.originalName);
    const power=influence?.power??ownerKey;
    const baseColor=regimeColor(colorFamilies.get(power)??(power===identityKey&&p.colorFamily?String(p.colorFamily):power),year);
    const controlInfluence=!!influence&&['occupation','intervention'].includes(influence.kind);
    const tinted=influence?dependencyColor(baseColor,identityKey,influence.kind==='bloc'||influence.kind==='military-support'):dependent?dependencyColor(baseColor,identityKey):baseColor;
    const politicalColor=p.status==='source-reference'?'#8b9188':controlInfluence?regimeColor(ownerKey,year):tinted;
    return {...f,properties:{...p,name,identityKey,entityCode:p.entityCode??territorialEntityCode(p,year),politicalColor,...(dependent&&ownerKey!==identityKey?{administratorKey:ownerKey}:{}),...(controlInfluence?{controlInfluenceColor:tinted}:{}),...(influence?{dominantPower:power,influenceKind:influence.kind,influenceNote:influence.note,influenceSource:influence.source,influenceHatchScope:influence.hatchScope,influenceLabel:influence.label}:modernDependency?{dominantPower:ownerKey,influenceKind:'dependency',influenceNote:`Dependencia vinculada a ${sovereignLabels.get(ownerKey)??profile!.sovereign} según la referencia contemporánea de Natural Earth incorporada en 2026. El matiz indica vinculación administrativa; conserva identidad y datos propios.`,influenceSource:'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/'}:{})}};
  })};
}
/** Country outlines are an explicitly labelled documentary reference here,
 * never a reconstruction of local fronts or proof of uniform foreign control. */
export function nationalInfluenceHatching(data:FeatureCollection,year:number):FeatureCollection{
 return {type:'FeatureCollection',features:data.features.filter(f=>f.properties?.influenceHatchScope==='national-reference').map((f,i)=>{
  const p=f.properties!,controlColor=regimeColor(String(p.dominantPower),year),occupiedColor=regimeColor(String(p.identityKey),year);
  return {...f,id:`national-influence-${i}`,properties:{...p,controller:p.dominantPower,occupiedKey:p.identityKey,occupiedName:p.name,occupiedColor,controlColor,patternKey:`${controlColor}:${occupiedColor}`,name:p.influenceLabel??p.name,referenceScope:'national-reference',note:p.influenceNote,source:p.influenceSource}};
 })};
}
function frenchName(year:number){
  return `Francia · ${year<=1791?'monarquía':year<=1794?'Primera República':year<=1799?'Directorio':year<=1803?'Consulado':year<=1813?'Primer Imperio':year<=1829?'Restauración':year<=1847?'Monarquía de Julio':year<=1851?'Segunda República':year<=1869?'Segundo Imperio':'Tercera República'}`;
}
