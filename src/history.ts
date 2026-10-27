import {isoYear} from './dates';
import type {Feature, FeatureCollection, MultiPolygon, Polygon, Position} from 'geojson';
export type Period = {fid:number; gwcode:number; country_name:string; start:string; end:string; status:string; owner:string; capname:string; caplong:number; caplat:number; b_def:number};
type TopologyGeometry = {type:'Polygon'|'MultiPolygon';arcs:number[][]|number[][][];properties:Period};
export type HistoryTopology = {type:'Topology';arcs:Position[][];objects:{countries:{geometries:TopologyGeometry[]}}};
export const statuses:Record<string,string>={independent:'Estado independiente',colony:'Colonia',protectorate:'Protectorado',occupied:'Territorio ocupado',mandate:'Mandato', 'N/A':'Estatus no clasificado'};
const names:Record<string,string>={'United States of America':'Estados Unidos','United Kingdom':'Reino Unido','France':'Francia','India':'India','Egypt':'Egipto','Israel':'Israel','Palestine':'Palestina','Gaza':'Gaza','West Bank':'Cisjordania','Syria':'Siria','Japan':'Japón','Italy/Sardinia':'Italia','China':'China','French West Africa':'África Occidental Francesa','Algeria':'Argelia','French Guyana':'Guayana Francesa','French Polynesia':'Polinesia Francesa','Reunion':'Reunión','Germany (Prussia)':'Alemania','German Federal Republic':'República Federal de Alemania','German Democratic Republic':'República Democrática Alemana','Austria-Hungary':'Austria-Hungría','Austria':'Austria','Hungary':'Hungría','Czechoslovakia':'Checoslovaquia','Poland':'Polonia','Spain':'España','Portugal':'Portugal','Netherlands':'Países Bajos','Belgium':'Bélgica','Ireland':'Irlanda','Rumania':'Rumanía','Russia (Soviet Union)':'Rusia','Ukraine':'Ucrania','Yugoslavia':'Yugoslavia','South Sudan':'Sudán del Sur','Sudan':'Sudán','Turkey (Ottoman Empire)':'Turquía','Iran (Persia)':'Irán','Morocco':'Marruecos','Tunisia':'Túnez','Libya':'Libia','German Togoland':'Togo alemán','Kamerun':'Camerún alemán','British Togoland':'Togo británico','British Cameroons':'Camerún británico'};
const aliases:Record<string,string>={'United States of America':'USA','United Kingdom':'GBR','Germany (Prussia)':'DEU','German Federal Republic':'DEU','German Democratic Republic':'DDR','Italy/Sardinia':'ITA','Russia (Soviet Union)':'RUS','Rumania':'ROU','Macedonia (FYROM/North Macedonia)':'MKD','Congo':'COG','Congo, Democratic Republic of (Zaire)':'COD','Iran (Persia)':'IRN','Turkey (Ottoman Empire)':'TUR','Egypt':'EGY','Gambia':'GMB','Cote D\'Ivoire':'CIV','Burkina Faso (Upper Volta)':'BFA','Tanzania (Tanganyika)':'TZA','Swaziland (Eswatini)':'SWZ','Madagascar (Malagasy)':'MDG','Zimbabwe (Rhodesia)':'ZWE','Korea, Republic of':'KOR','Korea, People\'s Republic of':'PRK','Kyrgyz Republic':'KGZ','Laos':'LAO','Vietnam (Annam/Cochin China/Tonkin)':'VNM','Vietnam, Democratic Republic of':'VNM','Myanmar (Burma)':'MMR','Sri Lanka (Ceylon)':'LKA','Cambodia (Kampuchea)':'KHM','East Timor':'TLS','Surinam':'SUR','French Guyana':'GUF','Palestine':'PSE','West Bank':'PSE','Gaza':'PSE','Taiwan':'TWN','Bahamas':'BHS','Venezuela':'VEN','Bolivia':'BOL','Belarus (Byelorussia)':'BLR','Cape Verde':'CPV','Brunei':'BRN','New Zealand':'NZL'};
export function historicName(p:Period,year:number){
  if(p.country_name==='Danzig')return 'Ciudad Libre de Danzig';
  if(p.country_name==='China'&&year>=1912&&year<1949)return 'República de China';
  if(p.country_name==='China'&&year<1912)return 'Imperio Qing';
  if(p.country_name==='Serbia'&&year<1918)return 'Reino de Serbia';
  if(p.country_name==='Montenegro'&&year<1918)return year<1910?'Principado de Montenegro':'Reino de Montenegro';
  if(p.country_name==='Morocco'&&year<1912)return 'Sultanato de Marruecos';
  if(p.country_name==='Korea')return year<1905?'Imperio de Corea':year<1910?'Imperio de Corea · protectorado japonés':'Corea bajo administración japonesa';
  if(p.country_name==='Congo, Democratic Republic of (Zaire)'&&year<1908)return 'Estado Libre del Congo';
  if(p.country_name==='Congo, Democratic Republic of (Zaire)'&&year<1960)return 'Congo Belga';
  if(['Transvaal','Orange Free State'].includes(p.country_name)&&year>=1902)return p.country_name==='Transvaal'?'Colonia del Transvaal':'Colonia del Río Orange';
  if(p.country_name==='Yugoslavia'&&year<1945)return year<1929?'Reino de los serbios, croatas y eslovenos':'Reino de Yugoslavia';
  if(p.country_name==='Malaysia'&&year>=1957&&year<1963)return 'Federación de Malaya';
  if(p.gwcode===365)return year<=1916?'Imperio ruso':year<1922?'Rusia soviética':year<=1990?'Unión Soviética':'Rusia';
  if(p.country_name==='Germany (Prussia)')return year<=1917?'Imperio alemán':year===1918?'Alemania · transición republicana':year<=1932?'Alemania · República de Weimar':'Alemania nazi';
  if(p.country_name==='German Democratic Republic'&&year<1949)return 'Alemania · zona de ocupación soviética';
  if(p.country_name==='German Federal Republic')return year<1949?'Alemania · zonas de ocupación occidentales':year>=1990?'Alemania':'República Federal de Alemania';
  if(p.country_name==='Turkey (Ottoman Empire)'&&year<1923)return year===1922?'Turquía · Gobierno de la Gran Asamblea':'Imperio otomano';
  if(p.country_name==='Yugoslavia'&&year>=1992)return year>=2003?'Serbia y Montenegro':'República Federal de Yugoslavia';
  if(p.country_name==='Yemen (Arab Republic of Yemen)'&&year>=1962)return year>=1990?'Yemen':'República Árabe de Yemen · Yemen del Norte';
  if(p.country_name==="Yemen, People's Republic of")return year<1970?'República Popular de Yemen del Sur':'República Democrática Popular de Yemen · Yemen del Sur';
  if(p.country_name==='Vietnam, Democratic Republic of')return year<1975?'República Democrática de Vietnam · Vietnam del Norte':year===1975?'Vietnam · control del norte, unificación pendiente':'Vietnam';
  if(p.country_name==='Vietnam, Republic of')return 'República de Vietnam · Vietnam del Sur';
  if(p.country_name==='Spanish Sahara')return 'Sáhara Español';
  if(p.country_name==='Zimbabwe (Rhodesia)'&&year>=1965)return year<1979?'Rodesia · régimen no reconocido':year===1979?'Rodesia del Sur · transición a la independencia':'Zimbabue';
  if(p.country_name==='Macedonia (FYROM/North Macedonia)')return year>=2019?'Macedonia del Norte':'República de Macedonia';
  if(p.country_name==='Congo, Democratic Republic of (Zaire)')return year>=1971&&year<1997?'Zaire':'República Democrática del Congo';
  return names[p.country_name]??p.country_name;
}
export function hashColor(value:string){let n=0;for(const c of value)n=(n*31+c.charCodeAt(0))|0;return Math.abs(n)%12;}
const norm=(s:string)=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z]/g,'');
export function isoFor(p:Period,year:number,modernNames:Map<string,string>){
  if(p.country_name==='China'&&year<1949)return '';
  if(p.country_name==='Turkey (Ottoman Empire)'&&year<1923||['Serbia','Montenegro'].includes(p.country_name)&&year<1918||p.country_name==='Korea')return '';
  if(p.status!=='independent'||(p.gwcode===365&&year<1991)||p.country_name==='Yugoslavia'||p.country_name==='Czechoslovakia'||p.country_name==='Austria-Hungary'||p.country_name==='German Democratic Republic')return '';
  if(p.country_name==='Yemen (Arab Republic of Yemen)')return year>=1990?'YEM':'';
  if(p.country_name==="Yemen, People's Republic of"||p.country_name==='Vietnam, Republic of'||(p.country_name==='Vietnam, Democratic Republic of'&&year<1976)||(p.country_name==='Zimbabwe (Rhodesia)'&&year<1980))return '';
  if(p.country_name==='Bosnia-Herzegovina')return 'BIH';
  if(p.country_name==='Kosovo')return 'KOS';
  return aliases[p.country_name]??modernNames.get(norm(p.country_name))??'';
}
/** Historical identity is separate from a successor's statistical ISO code. */
export function territorialEntityCode(p:Record<string,any>,year:number):string{
  if(p.identityKey==='SVK-1939'||p.entityCode==='SVW')return 'SVW';
  const name=p.originalName??p.country_name??p.name;
  if(name==='Danzig')return 'DAN';
  if(name==='Tibet')return 'TIB';
  if(name==='China'&&year<1912)return 'QNG';
  if(name==='Austria-Hungary')return 'AUH';
  if(name==='Russia (Soviet Union)'&&year<1917)return 'RUE';
  if(name==='Turkey (Ottoman Empire)'&&year<1922)return 'OTT';
  if(name==='Serbia'&&year<1918)return 'SRK';
  if(name==='Montenegro'&&year<1918)return 'MNK';
  if(name==='Korea'&&year<1910)return 'KEM';
  if(name==='Congo, Democratic Republic of (Zaire)'&&year<1908)return 'CFS';
  if(name==='Transvaal')return 'TRV';
  if(name==='Orange Free State')return 'ORF';
  if(name==='Morocco')return 'MAR';
  if(name==='China'&&year>=1912&&year<1949)return 'ROC';
  if(name==='Russia (Soviet Union)'&&year>=1917&&year<1922)return 'RSR';
  if(name==='Yugoslavia'&&year<1945)return 'YKM';
  if(name==='Malaysia'&&year>=1957&&year<1963)return 'MAL';
  if(name==='Yemen (Arab Republic of Yemen)'&&year<1962)return 'YMK';
  if(name==='Tanzania (Tanganyika)'&&year<1964)return 'TAN';
  if(name==='Zanzibar')return 'ZAN';
  if(name==='Russia (Soviet Union)'&&year>=1922&&year<=1990)return 'SUN';
  if(name==='Yugoslavia')return year<=1991?'YUG':'SCG';
  if(name==='Czechoslovakia')return 'CSK';
  if(name==='German Democratic Republic')return 'DDR';
  if(name==='Yemen (Arab Republic of Yemen)'&&year>=1962&&year<1990)return 'YAR';
  if(name==="Yemen, People's Republic of")return 'YPR';
  if(name==='Vietnam, Democratic Republic of'&&year<1976)return 'VDR';
  if(name==='Vietnam, Republic of')return year<1955?'VSV':'RVN';
  if(name==='Zimbabwe (Rhodesia)'&&year>=1965&&year<1980)return 'RHO';
  if(name==='Spanish Sahara')return 'ESH';
  const aliases:Record<string,string>={SAH:'ESH',SDS:'SSD',KOS:'XKX',PSX:'PSE'};
  // A dated historical identity can have no statistical ISO code. Context and
  // institutions still use its explicit entity code; this does not assign any
  // observations of a modern successor to the historical polity.
  if(p.entityCode)return aliases[p.entityCode]??String(p.entityCode);
  return aliases[p.code]??p.code??'';
}
export const normalizedName=norm;
export function periodsAt(topology:HistoryTopology,year:number){const date=`${isoYear(year)}-12-31`;return topology.objects.countries.geometries.filter(g=>{
  const p=g.properties;
  // Retain the original record and correct only its observed validity. The
  // treaty was implemented in1920 and annexation occurred in1939, not1938.
  const start=p.country_name==='Danzig'?'1920-11-15':p.start,end=p.country_name==='Danzig'?'1939-08-31':p.end;
  return start<=date&&end>=date;
});}
export function decodeGeometry(topology:HistoryTopology,g:TopologyGeometry):Polygon|MultiPolygon{
  const arc=(n:number)=>{const coordinates=topology.arcs[n<0?~n:n];return n<0?[...coordinates].reverse():coordinates;};
  const ring=(indices:number[])=>indices.flatMap((n,i)=>i?arc(n).slice(1):arc(n));
  return g.type==='Polygon'?{type:'Polygon',coordinates:(g.arcs as number[][]).map(ring)}:{type:'MultiPolygon',coordinates:(g.arcs as number[][][]).map(p=>p.map(ring))};
}
export function historyAt(topology:HistoryTopology,year:number,modernNames:Map<string,string>=new Map(),geometryCache=new Map<number,Polygon|MultiPolygon>()):FeatureCollection{
  const active=periodsAt(topology,year);
  const byCode=new Map(active.map(g=>[String(g.properties.gwcode),g.properties]));
  const geometryFor=(g:TopologyGeometry)=>{let geometry=geometryCache.get(g.properties.fid);if(!geometry){geometry=decodeGeometry(topology,g);geometryCache.set(g.properties.fid,geometry);}return geometry;};
  const result:FeatureCollection={type:'FeatureCollection',features:active.map(g=>{
    const p=g.properties;
    // Sinai and Golan occupation is represented separately, not as sovereign incorporation.
    let geometry=g;
    if(year>=1967&&['Egypt','Israel','Syria'].includes(p.country_name))geometry=topology.objects.countries.geometries.find(a=>a.properties.country_name===p.country_name&&a.properties.start<='1966-12-31'&&a.properties.end>='1966-12-31')??g;
    // Keep internationally recognized Ukrainian territory in the base. The
    // separately dated Crimea overlay shows occupation, not recognized cession.
    if(year>=2014&&['Ukraine','Russia (Soviet Union)'].includes(p.country_name))geometry=topology.objects.countries.geometries.find(a=>a.properties.country_name===p.country_name&&a.properties.start<='2013-12-31'&&a.properties.end>='2013-12-31')??g;
    const name=historicName(p,year);
    const owner=p.status==='independent'?name:byCode.has(p.owner)?historicName(byCode.get(p.owner)!,year):`Potencia ${p.owner}`;
    const code=isoFor(p,year,modernNames),entityCode=territorialEntityCode({...p,code},year);
    const identityKey=entityCode==='SUN'?'USSR':entityCode==='AUH'?'AUT-HUN':entityCode==='QNG'?'QING':entityCode==='SCG'&&year<2003?'FRY':['RUE','RPR','OTT','SRK','MNK','KEM','CFS','TRV','ORF','MAR','YUG','YKM','RSR','ROC','DAN','TIB','SCG','CSK','DDR','YAR','YPR','VDR','RVN','VSV','MAL','RHO','YMK','TAN','ZAN'].includes(entityCode)?entityCode:undefined;
    const capital=p.country_name==='Zimbabwe (Rhodesia)'&&year<1982||p.country_name==='Federation of Rhodesia and Nyasaland'?'Salisbury':p.country_name==='Tanzania (Tanganyika)'&&year<1974?'Dar es Salaam':p.country_name==='Equatorial Guinea'&&year<1973?'Santa Isabel':p.capname;
    const temporalNote=p.country_name==='Vietnam, Democratic Republic of'&&year===1975?'CShapes agrupa todo Vietnam desde mayo de 1975 por control territorial. La unificación estatal formal fue el 2 de julio de 1976; este contorno no distingue la administración provisional del sur.':entityCode==='RHO'?(year===1979?'En diciembre de 1979 se restableció la administración británica durante la transición; Zimbabue accedió a la independencia el 18 de abril de 1980. El estatus independiente de CShapes describe el régimen previo de facto, no su reconocimiento internacional.':'Declaración unilateral de independencia de 1965 bajo un régimen de minoría blanca no reconocido por la ONU; no equivale al Estado independiente de Zimbabue de 1980.'):undefined;
    const politicalStatus=entityCode==='DAN'?'Ciudad libre autónoma bajo protección de la Sociedad de Naciones':entityCode==='TIB'?'Gobierno tibetano de facto · soberanía disputada':entityCode==='RHO'?(year===1979?'Administración británica de transición al cierre anual':'Régimen de facto no reconocido internacionalmente'):statuses[p.status]??p.status;
    return {type:'Feature',id:p.fid,geometry:geometryFor(geometry),properties:{...p,name:entityCode==='VSV'?'Estado de Vietnam':entityCode==='YMK'?'Reino Mutawakkilita de Yemen':entityCode==='TAN'?'Tanganica':entityCode==='ZAN'?'Zanzíbar':name,originalName:p.country_name,code:['YMK','TAN','ZAN','MAL'].includes(entityCode)?'':code,entityCode,identityKey,group:owner,color:hashColor(p.owner),capital,capname:capital,...(p.country_name==='Tanzania (Tanganyika)'&&year<1974?{caplong:39.28,caplat:-6.81}:{}),ownerName:owner,politicalStatus,note:temporalNote,source:'https://icr.ethz.ch/data/cshapes/'}} as Feature;
  })};
  for(const f of result.features)if(f.properties?.entityCode==='DAN')Object.assign(f.properties,{identityKey:'DAN',status:'free-city',ownerName:'',group:'Ciudad Libre de Danzig',start:'1920-11-15',end:'1939-08-31',sourceStart:f.properties.start,sourceEnd:'1938-08-31',...(year===1938?{boundaryCorrection:'danzig-1938'}:{}),note:'Ciudad libre desde15/11/1920; ocupación e incorporación alemana en septiembre1939. Se corrige la terminación1938 del registro de fuente, conservando su polígono. La tutela de la Sociedad de Naciones no equivale a soberanía alemana o polaca.',territorySource:'https://www.bundesarchiv.de/themen-entdecken/online-entdecken/themenbeitraege/die-stadt-danzig-im-nationalsozialismus/'});
  if(year>=1905&&year<1910)for(const f of result.features)if(f.properties?.originalName==='Korea')Object.assign(f.properties,{sourceStatus:f.properties.status,sourceOwnerName:f.properties.ownerName,status:'protectorate',ownerName:'Japón',politicalStatus:'Imperio coreano bajo protectorado japonés impuesto',note:'Acuerdo impuesto17/11/1905; se conserva la autoridad imperial local hasta la anexión de1910. Protectorado y anexión son fases distintas. Se corrige el estatus independiente de la fuente, sin modificar su contorno.',territorySource:'https://www.jacar.go.jp/english/exhibition/nichiro/19051117.htm'});
  if(year>=1900&&year<1912)for(const f of result.features)if(f.properties?.originalName==='Morocco')Object.assign(f.properties,{sourceStatus:f.properties.status,status:'independent',code:'MAR',politicalStatus:'Sultanato independiente · soberanía disputada durante la crisis sucesoria',capital:'Fez',capname:'Fez',caplong:-5,caplat:34.05,note:'El estatus N/A del inventario no significa desaparición del sultanato. El protectorado se establece en1912; la intervención extranjera y las proclamaciones rivales anteriores se describen en el contexto, sin convertirlas en una anexión total.',territorySource:'https://history.state.gov/historicaldocuments/frus1908/papers'});
  if(year<1908)for(const f of result.features)if(f.properties?.entityCode==='CFS')Object.assign(f.properties,{sourceStatus:f.properties.status,sourceOwnerName:f.properties.ownerName,status:'independent',code:'',ownerName:'Estado Libre del Congo',group:'Estado Libre del Congo',politicalStatus:'Estado bajo soberanía personal de Leopoldo II',note:'Entidad separada del Estado belga hasta15/11/1908. Se corrige la clasificación colonial de la fuente sin modificar el contorno; el dominio de LeopoldoII no equivale a un territorio sin población ni a legitimidad del régimen colonial.',territorySource:'https://www.arch.be/index.php?a=2022-09-26-opnieuw-op-zijn-plaats-het-verdrag-tot-afstand-van-de-onafhankelijke-congostaat-aan-belgie&l=nl&m=nieuws&r=alle-nieuwsberichten'});
  if(year>=1902&&year<1910)for(const f of result.features)if(f.properties&&['TRV','ORF'].includes(f.properties.entityCode))Object.assign(f.properties,{sourceStatus:f.properties.status,sourceOwnerName:f.properties.ownerName,status:'colony',code:'',ownerName:'Reino Unido',politicalStatus:'Colonia británica · posterior a la Paz de Vereeniging',note:'La paz de31/5/1902 termina la guerra y somete las antiguas repúblicas a la Corona británica; el autogobierno posterior no equivale a independencia. El contorno original de la fuente se conserva: no representa los frentes diarios de1900–1902.',territorySource:'https://www.nam.ac.uk/explore/boer-war'});
  // CShapes aggregates the western zones under one owner code. That must not
  // turn joint occupation into sole US administration or a US national flag.
  if(year>=1945&&year<=1948)for(const f of result.features)if(f.properties?.originalName==='German Federal Republic')Object.assign(f.properties,{sourceOwnerName:f.properties.ownerName,collectiveAdministration:true,status:'occupation-zones',ownerName:'Estados Unidos, Reino Unido y Francia · administraciones de ocupación',group:'Administraciones aliadas de ocupación',politicalStatus:'Zonas occidentales de ocupación aliada',territorySource:'https://digitallibrary.un.org/record/669294/files/E_CN.4_W.19-EN.pdf?ln=en'});
  // CShapes keeps two components during the union. Render a single dated entity;
  // the unchanged source polygons remain available in history.topojson.
  if(year>=1958&&year<=1960){
    const egypt=result.features.find(f=>f.properties?.originalName==='Egypt'),syria=result.features.find(f=>f.properties?.originalName==='Syria');
    if(egypt&&syria){
      const polygons=(f:Feature)=>f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
      result.features=result.features.filter(f=>f!==egypt&&f!==syria);
      result.features.push({...egypt,geometry:{type:'MultiPolygon',coordinates:[...polygons(egypt),...polygons(syria)]},properties:{...egypt.properties,name:'República Árabe Unida',identityKey:'UAR',entityCode:'UAR',code:'',note:'Unión de Egipto y Siria de 1958 a septiembre de 1961. Componentes CShapes agrupados para representar la entidad común; no se heredan estadísticas del Egipto o Siria actuales.',territorySource:'https://untreaty.un.org/ilc/documentation/english/a_cn4_210.pdf'}});
    }
  }
  return result;
}
export function historicalCapitals(data:FeatureCollection):FeatureCollection{
  const seen=new Set<string>();
  return {type:'FeatureCollection',features:data.features.flatMap(f=>{
    const p=f.properties!;const key=`${p.caplong}:${p.caplat}`;
    if(!p.capname||!Number.isFinite(p.caplong)||seen.has(key))return[];
    seen.add(key);return [{type:'Feature',geometry:{type:'Point',coordinates:[p.caplong,p.caplat]},properties:{name:p.capname,country:p.name,code:p.code,entityCode:p.entityCode,identityKey:p.identityKey,capital:true,rank:p.status==='independent'?1:4,note:`Capital o sede administrativa de ${p.name} en el registro histórico consultado.`,source:p.source}} as Feature];
  })};
}

/** Add date-bounded reference contours without extending independent successors backwards. */
export function withHistoricalSupplements(data:FeatureCollection,year:number,supplements:FeatureCollection,preSaharaPartition:FeatureCollection):FeatureCollection{
  const date=`${isoYear(year)}-12-31`;
  const features=data.features.map(f=>{
    const code=f.properties?.code;
    // CShapes incorporates claimed Saharan sectors into MAR/MRT in 1975.
    // Keep the UN territory separate in this base; no berm/front is invented.
    const separateSahara=year>=1975&&(code==='MAR'||(code==='MRT'&&year<=1978));
    const reference=separateSahara?preSaharaPartition.features.find(a=>a.properties?.code===code):undefined;
    if(!reference)return f;
    return {...f,geometry:reference.geometry,properties:{...f.properties,territorialReference:true,geometrySource:'https://icr.ethz.ch/data/cshapes/',geometrySourceLabel:'CShapes 2.0 · contorno de 1974',referenceYear:1974,territorySource:'https://www.un.org/dppa/decolonization/en/nsgt/western-sahara',note:'Contorno CShapes de 1974 conservado como referencia para separar el Sáhara Occidental, cuyo estatus sigue pendiente ante la ONU. No reconstruye líneas históricas de control ni la partición administrada por Marruecos y Mauritania; las reclamaciones no se convierten en cesiones soberanas.'}};
  });
  const existing=new Set(features.map(f=>f.properties?.entityCode));
  features.push(...supplements.features.filter(f=>f.properties!.start<=date&&f.properties!.end>=date&&!existing.has(f.properties!.entityCode)));
  return {...data,features};
}
