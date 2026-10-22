import type {FeatureCollection} from 'geojson';
import {hashColor,territorialEntityCode} from './history';

const palette=['#78938a','#af9c77','#658e98','#9c887a','#9ba783','#b39c80','#7b929d','#a6a386','#8f9c8d','#9e8883','#819c9f','#b5a48a'];
const families:Record<string,string>={
  'United States of America':'USA','United States':'USA','Estados Unidos':'USA',
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
  let key=families[name]??String(p.code||p.wikidata||name);
  const codes:Record<string,string>={SSD:'SDS',XKX:'KOS',PSE:'PSX',ESH:'SAH'};
  key=codes[key]??key;
  if((p.gwcode===365||name==='Russia (Soviet Union)')&&year>=1922&&year<=1990)key='USSR';
  if(key==='ESP'&&year>=1931&&year<=1938)key='ESP-REPUBLIC';
  if(key==='CHN'&&year<1949)key=year>=1912?'ROC':'QING';
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
    case 'USA':return '#4e89bd';
    case 'GBR':return '#a78baf';
    case 'CHN':return '#d5b34b';case 'ROC':return '#ddbe64';case 'QING':return '#bb9a46';
    case 'JPN':return year<=1945?'#c47b70':'#bd9d91';
    case 'FRA':return year<=1791?'#b9b4a1':year<=1794?'#789bab':year<=1799?'#6599ac':year<=1803?'#4b8baa':year<=1814?'#387cc1':year<=1829?'#adab91':year<=1847?'#7a9fbc':year<=1851?'#669ab9':year<=1869?'#456fa8':year<=1940?'#6796ad':year<=1945?'#5c91ad':year<=1957?'#729daa':'#6a9db1';
    case 'FRA-FREE':return '#528fbc';case 'FRA-VICHY':return '#9598a1';
    case 'ESP-REPUBLIC':return '#9b688f';case 'ESP-NATIONALIST':return '#b7914e';
    case 'ESP':return year===1873?'#a57a9c':year>=1923&&year<=1929?'#8f9365':year<=1930?'#b9a365':year<=1975?'#b7914e':'#c2a880';
    case 'ITA':return year>=1922&&year<=1943?'#788b65':'#8daa8c';
    case 'PRUSSIA':return '#6f8290';case 'CROATIA-CLIENT':return '#96999d';
    case 'AUT-HUN':return '#ac8c64';case 'OTT':return '#8f9b6c';
    default:return palette[hashColor(key)];
  }
}
export function politicalData(data:FeatureCollection,year:number):FeatureCollection{
  return {...data,features:data.features.map(f=>{
    const p=f.properties??{};const identityKey=entityKey(p,year);
    const ownerKey=p.status&&p.status!=='independent'?entityKey({name:p.ownerName},year):p.parentName?entityKey({name:p.parentName},year):identityKey;
    const name=identityKey==='FRA'&&(!p.parentName||p.parentName===p.originalName)&&!p.status&&year<1886?frenchName(year):p.name;
    return {...f,properties:{...p,name,identityKey,entityCode:p.entityCode??territorialEntityCode(p,year),politicalColor:regimeColor(ownerKey,year)}};
  })};
}
function frenchName(year:number){
  return `Francia · ${year<=1791?'monarquía':year<=1794?'Primera República':year<=1799?'Directorio':year<=1803?'Consulado':year<=1814?'Primer Imperio':year<=1829?'Restauración':year<=1847?'Monarquía de Julio':year<=1851?'Segunda República':year<=1869?'Segundo Imperio':'Tercera República'}`;
}
