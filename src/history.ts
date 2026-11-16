import { tx } from './i18n';
import {isoYear} from './dates';
import type {Feature, FeatureCollection, MultiPolygon, Polygon, Position} from 'geojson';
export type Period = {fid:number; gwcode:number; country_name:string; start:string; end:string; status:string; owner:string; capname:string; caplong:number; caplat:number; b_def:number};
type TopologyGeometry = {type:'Polygon'|'MultiPolygon';arcs:number[][]|number[][][];properties:Period};
export type HistoryTopology = {type:'Topology';arcs:Position[][];objects:{countries:{geometries:TopologyGeometry[]}}};
export const statuses:Record<string,string>={independent:tx('history.estadoIndependiente'),colony:'Colonia',protectorate:'Protectorado',occupied:tx('history.territorioOcupado'),mandate:'Mandato', 'N/A':tx('history.estatusNoClasificado')};
const names:Record<string,string>={'United States of America':tx('history.estadosUnidos'),'United Kingdom':tx('history.reinoUnido'),'France':'Francia','India':'India','Egypt':'Egipto','Israel':'Israel','Palestine':'Palestina','Gaza':'Gaza','West Bank':'Cisjordania','Syria':'Siria','Japan':tx('history.japon'),'Italy/Sardinia':'Italia','China':'China','French West Africa':tx('history.africaOccidentalFrancesa'),'Algeria':'Argelia','French Guyana':tx('history.guayanaFrancesa'),'French Polynesia':tx('history.polinesiaFrancesa'),'Reunion':tx('history.reunion'),'Germany (Prussia)':'Alemania','German Federal Republic':tx('history.republicaFederalDeAlemania'),'German Democratic Republic':tx('history.republicaDemocraticaAlemana'),'Austria-Hungary':tx('history.austriaHungria'),'Austria':'Austria','Hungary':tx('history.hungria'),'Czechoslovakia':'Checoslovaquia','Poland':'Polonia','Spain':tx('history.espana'),'Portugal':'Portugal','Netherlands':tx('history.paisesBajos'),'Belgium':tx('history.belgica'),'Ireland':'Irlanda','Rumania':tx('history.rumania'),'Russia (Soviet Union)':'Rusia','Ukraine':'Ucrania','Yugoslavia':'Yugoslavia','South Sudan':tx('history.sudanDelSur'),'Sudan':tx('history.sudan'),'Turkey (Ottoman Empire)':tx('history.turquia'),'Iran (Persia)':tx('history.iran'),'Morocco':'Marruecos','Tunisia':tx('history.tunez'),'Libya':'Libia','German Togoland':tx('history.togoAleman'),'Kamerun':tx('history.camerunAleman'),'British Togoland':tx('history.togoBritanico'),'British Cameroons':tx('history.camerunBritanico')};
const aliases:Record<string,string>={'United States of America':'USA','United Kingdom':'GBR','Germany (Prussia)':'DEU','German Federal Republic':'DEU','German Democratic Republic':'DDR','Italy/Sardinia':'ITA','Russia (Soviet Union)':'RUS','Rumania':'ROU','Macedonia (FYROM/North Macedonia)':'MKD','Congo':'COG','Congo, Democratic Republic of (Zaire)':'COD','Iran (Persia)':'IRN','Turkey (Ottoman Empire)':'TUR','Egypt':'EGY','Gambia':'GMB','Cote D\'Ivoire':'CIV','Burkina Faso (Upper Volta)':'BFA','Tanzania (Tanganyika)':'TZA','Swaziland (Eswatini)':'SWZ','Madagascar (Malagasy)':'MDG','Zimbabwe (Rhodesia)':'ZWE','Korea, Republic of':'KOR','Korea, People\'s Republic of':'PRK','Kyrgyz Republic':'KGZ','Laos':'LAO','Vietnam (Annam/Cochin China/Tonkin)':'VNM','Vietnam, Democratic Republic of':'VNM','Myanmar (Burma)':'MMR','Sri Lanka (Ceylon)':'LKA','Cambodia (Kampuchea)':'KHM','East Timor':'TLS','Surinam':'SUR','French Guyana':'GUF','Palestine':'PSE','West Bank':'PSE','Gaza':'PSE','Taiwan':'TWN','Bahamas':'BHS','Venezuela':'VEN','Bolivia':'BOL','Belarus (Byelorussia)':'BLR','Cape Verde':'CPV','Brunei':'BRN','New Zealand':'NZL'};
export function historicName(p:Period,year:number){
  if(p.country_name==='Danzig')return tx('history.ciudadLibreDeDanzig');
  if(p.country_name==='China'&&year>=1912&&year<1949)return tx('history.republicaDeChina');
  if(p.country_name==='China'&&year<1912)return tx('history.imperioQing');
  if(p.country_name==='Serbia'&&year<1918)return tx('history.reinoDeSerbia');
  if(p.country_name==='Montenegro'&&year<1918)return year<1910?tx('history.principadoDeMontenegro'):tx('history.reinoDeMontenegro');
  if(p.country_name==='Morocco'&&year<1912)return tx('history.sultanatoDeMarruecos');
  if(p.country_name==='Korea')return year<1905?tx('history.imperioDeCorea'):year<1910?tx('history.imperioDeCoreaProtectoradoJapones'):tx('history.coreaBajoAdministracionJaponesa');
  if(p.country_name==='Congo, Democratic Republic of (Zaire)'&&year<1908)return tx('history.estadoLibreDelCongo');
  if(p.country_name==='Congo, Democratic Republic of (Zaire)'&&year<1960)return tx('history.congoBelga');
  if(['Transvaal',tx('history.orangeFreeState')].includes(p.country_name)&&year>=1902)return p.country_name==='Transvaal'?tx('history.coloniaDelTransvaal'):tx('history.coloniaDelRioOrange');
  if(p.country_name==='Yugoslavia'&&year<1945)return year<1929?tx('history.reinoDeLosSerbiosCroatas'):tx('history.reinoDeYugoslavia');
  if(p.country_name==='Malaysia'&&year>=1957&&year<1963)return tx('history.federacionDeMalaya');
  if(p.gwcode===365)return year<=1916?tx('history.imperioRuso'):year<1922?tx('history.rusiaSovietica'):year<=1990?tx('history.unionSovietica'):'Rusia';
  if(p.country_name==='Germany (Prussia)')return year<=1917?tx('history.imperioAleman'):year===1918?tx('history.alemaniaTransicionRepublicana'):year<=1932?tx('history.alemaniaRepublicaDeWeimar'):tx('history.alemaniaNazi');
  if(p.country_name==='German Democratic Republic'&&year<1949)return tx('history.alemaniaZonaDeOcupacionSovietica');
  if(p.country_name==='German Federal Republic')return year<1949?tx('history.alemaniaZonasDeOcupacionOccidentales'):year>=1990?'Alemania':tx('history.republicaFederalDeAlemania');
  if(p.country_name==='Turkey (Ottoman Empire)'&&year<1923)return year===1922?tx('history.turquiaGobiernoDeLaGran'):tx('history.imperioOtomano');
  if(p.country_name==='Yugoslavia'&&year>=1992)return year>=2003?tx('history.serbiaYMontenegro'):tx('history.republicaFederalDeYugoslavia');
  if(p.country_name==='Yemen (Arab Republic of Yemen)'&&year>=1962)return year>=1990?'Yemen':tx('history.republicaArabeDeYemenYemen');
  if(p.country_name==="Yemen, People's Republic of")return year<1970?tx('history.republicaPopularDeYemenDel'):tx('history.republicaDemocraticaPopularDeYemen');
  if(p.country_name==='Vietnam, Democratic Republic of')return year<1975?tx('history.republicaDemocraticaDeVietnamVietnam'):year===1975?tx('history.vietnamControlDelNorteUnificacion'):'Vietnam';
  if(p.country_name==='Vietnam, Republic of')return tx('history.republicaDeVietnamVietnamDel');
  if(p.country_name==='Spanish Sahara')return tx('history.saharaEspanol');
  if(p.country_name==='Zimbabwe (Rhodesia)'&&year>=1965)return year<1979?tx('history.rodesiaRegimenNoReconocido'):year===1979?tx('history.rodesiaDelSurTransicionA'):'Zimbabue';
  if(p.country_name==='Macedonia (FYROM/North Macedonia)')return year>=2019?tx('history.macedoniaDelNorte'):tx('history.republicaDeMacedonia');
  if(p.country_name==='Congo, Democratic Republic of (Zaire)')return year>=1971&&year<1997?'Zaire':tx('history.republicaDemocraticaDelCongo');
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
    if(year>=2014&&['Ukraine',tx('history.russiaSovietUnion')].includes(p.country_name))geometry=topology.objects.countries.geometries.find(a=>a.properties.country_name===p.country_name&&a.properties.start<='2013-12-31'&&a.properties.end>='2013-12-31')??g;
    const name=historicName(p,year);
    const owner=p.status==='independent'?name:byCode.has(p.owner)?historicName(byCode.get(p.owner)!,year):`Potencia ${p.owner}`;
    const code=isoFor(p,year,modernNames),entityCode=territorialEntityCode({...p,code},year);
    const identityKey=entityCode==='SUN'?'USSR':entityCode==='AUH'?'AUT-HUN':entityCode==='QNG'?'QING':entityCode==='SCG'&&year<2003?'FRY':['RUE','RPR','OTT','SRK','MNK','KEM','CFS','TRV','ORF','MAR','YUG','YKM','RSR','ROC','DAN','TIB','SCG','CSK','DDR','YAR','YPR','VDR','RVN','VSV','MAL','RHO','YMK','TAN','ZAN'].includes(entityCode)?entityCode:undefined;
    const capital=p.country_name==='Zimbabwe (Rhodesia)'&&year<1982||p.country_name==='Federation of Rhodesia and Nyasaland'?'Salisbury':p.country_name==='Tanzania (Tanganyika)'&&year<1974?tx('history.darEsSalaam'):p.country_name==='Equatorial Guinea'&&year<1973?tx('history.santaIsabel'):p.capname;
    const temporalNote=p.country_name==='Vietnam, Democratic Republic of'&&year===1975?tx('history.cshapesAgrupaTodoVietnamDesde'):entityCode==='RHO'?(year===1979?tx('history.enDiciembreDe1979Se'):tx('history.declaracionUnilateralDeIndependenciaDe')):undefined;
    const politicalStatus=entityCode==='DAN'?tx('history.ciudadLibreAutonomaBajoProteccion'):entityCode==='TIB'?tx('history.gobiernoTibetanoDeFactoSoberania'):entityCode==='RHO'?(year===1979?tx('history.administracionBritanicaDeTransicionAl'):tx('history.regimenDeFactoNoReconocido')):statuses[p.status]??p.status;
    return {type:'Feature',id:p.fid,geometry:geometryFor(geometry),properties:{...p,name:entityCode==='VSV'?tx('history.estadoDeVietnam'):entityCode==='YMK'?tx('history.reinoMutawakkilitaDeYemen'):entityCode==='TAN'?'Tanganica':entityCode==='ZAN'?tx('history.zanzibar'):name,originalName:p.country_name,code:['YMK','TAN','ZAN','MAL'].includes(entityCode)?'':code,entityCode,identityKey,group:owner,color:hashColor(p.owner),capital,capname:capital,...(p.country_name==='Tanzania (Tanganyika)'&&year<1974?{caplong:39.28,caplat:-6.81}:{}),ownerName:owner,politicalStatus,note:temporalNote,source:'https://icr.ethz.ch/data/cshapes/'}} as Feature;
  })};
  for(const f of result.features)if(f.properties?.entityCode==='DAN')Object.assign(f.properties,{identityKey:'DAN',status:'free-city',ownerName:'',group:tx('history.ciudadLibreDeDanzig'),start:'1920-11-15',end:'1939-08-31',sourceStart:f.properties.start,sourceEnd:'1938-08-31',...(year===1938?{boundaryCorrection:'danzig-1938'}:{}),note:tx('history.ciudadLibreDesde15111920'),territorySource:'https://www.bundesarchiv.de/themen-entdecken/online-entdecken/themenbeitraege/die-stadt-danzig-im-nationalsozialismus/'});
  if(year>=1905&&year<1910)for(const f of result.features)if(f.properties?.originalName==='Korea')Object.assign(f.properties,{sourceStatus:f.properties.status,sourceOwnerName:f.properties.ownerName,status:'protectorate',ownerName:tx('history.japon'),politicalStatus:tx('history.imperioCoreanoBajoProtectoradoJapones'),note:tx('history.acuerdoImpuesto17111905Se'),territorySource:'https://www.jacar.go.jp/english/exhibition/nichiro/19051117.htm'});
  if(year>=1900&&year<1912)for(const f of result.features)if(f.properties?.originalName==='Morocco')Object.assign(f.properties,{sourceStatus:f.properties.status,status:'independent',code:'MAR',politicalStatus:tx('history.sultanatoIndependienteSoberaniaDisputadaDurante'),capital:'Fez',capname:'Fez',caplong:-5,caplat:34.05,note:tx('history.elEstatusNADel'),territorySource:'https://history.state.gov/historicaldocuments/frus1908/papers'});
  if(year<1908)for(const f of result.features)if(f.properties?.entityCode==='CFS')Object.assign(f.properties,{sourceStatus:f.properties.status,sourceOwnerName:f.properties.ownerName,status:'independent',code:'',ownerName:tx('history.estadoLibreDelCongo'),group:tx('history.estadoLibreDelCongo'),politicalStatus:tx('history.estadoBajoSoberaniaPersonalDe'),note:tx('history.entidadSeparadaDelEstadoBelga'),territorySource:'https://www.arch.be/index.php?a=2022-09-26-opnieuw-op-zijn-plaats-het-verdrag-tot-afstand-van-de-onafhankelijke-congostaat-aan-belgie&l=nl&m=nieuws&r=alle-nieuwsberichten'});
  if(year>=1902&&year<1910)for(const f of result.features)if(f.properties&&['TRV','ORF'].includes(f.properties.entityCode))Object.assign(f.properties,{sourceStatus:f.properties.status,sourceOwnerName:f.properties.ownerName,status:'colony',code:'',ownerName:tx('history.reinoUnido'),politicalStatus:tx('history.coloniaBritanicaPosteriorALa'),note:tx('history.laPazDe3151902'),territorySource:'https://www.nam.ac.uk/explore/boer-war'});
  // CShapes aggregates the western zones under one owner code. That must not
  // turn joint occupation into sole US administration or a US national flag.
  if(year>=1945&&year<=1948)for(const f of result.features)if(f.properties?.originalName==='German Federal Republic')Object.assign(f.properties,{sourceOwnerName:f.properties.ownerName,collectiveAdministration:true,status:'occupation-zones',ownerName:tx('history.estadosUnidosReinoUnidoY'),group:tx('history.administracionesAliadasDeOcupacion'),politicalStatus:tx('history.zonasOccidentalesDeOcupacionAliada'),territorySource:'https://digitallibrary.un.org/record/669294/files/E_CN.4_W.19-EN.pdf?ln=en'});
  // CShapes keeps two components during the union. Render a single dated entity;
  // the unchanged source polygons remain available in history.topojson.
  if(year>=1958&&year<=1960){
    const egypt=result.features.find(f=>f.properties?.originalName==='Egypt'),syria=result.features.find(f=>f.properties?.originalName==='Syria');
    if(egypt&&syria){
      const polygons=(f:Feature)=>f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
      result.features=result.features.filter(f=>f!==egypt&&f!==syria);
      result.features.push({...egypt,geometry:{type:'MultiPolygon',coordinates:[...polygons(egypt),...polygons(syria)]},properties:{...egypt.properties,name:tx('history.republicaArabeUnida'),identityKey:'UAR',entityCode:'UAR',code:'',note:tx('history.unionDeEgiptoYSiria'),territorySource:'https://untreaty.un.org/ilc/documentation/english/a_cn4_210.pdf'}});
    }
  }
  return result;
}
export function historicalCapitals(data:FeatureCollection):FeatureCollection{
  const seen=new Set<string>();
  return {type:'FeatureCollection',features:data.features.flatMap(f=>{
    const p=f.properties!;const key=`${p.caplong}:${p.caplat}`;
    if(!p.capname||!Number.isFinite(p.caplong)||seen.has(key))return[];
    seen.add(key);return [{type:'Feature',geometry:{type:'Point',coordinates:[p.caplong,p.caplat]},properties:{name:p.capname,country:p.name,code:p.code,entityCode:p.entityCode,identityKey:p.identityKey,capital:true,rank:p.status==='independent'?1:4,note:tx('history.capitalOSedeAdministrativaDe',{name:p.name}),source:p.source}} as Feature];
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
    return {...f,geometry:reference.geometry,properties:{...f.properties,territorialReference:true,geometrySource:'https://icr.ethz.ch/data/cshapes/',geometrySourceLabel:tx('history.cshapes20ContornoDe'),referenceYear:1974,territorySource:'https://www.un.org/dppa/decolonization/en/nsgt/western-sahara',note:tx('history.contornoCshapesDe1974Conservado')}};
  });
  const existing=new Set(features.map(f=>f.properties?.entityCode));
  features.push(...supplements.features.filter(f=>f.properties!.start<=date&&f.properties!.end>=date&&!existing.has(f.properties!.entityCode)));
  return {...data,features};
}
