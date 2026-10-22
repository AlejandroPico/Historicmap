import type {Feature, FeatureCollection, MultiPolygon, Polygon, Position} from 'geojson';
export type Period = {fid:number; gwcode:number; country_name:string; start:string; end:string; status:string; owner:string; capname:string; caplong:number; caplat:number; b_def:number};
type TopologyGeometry = {type:'Polygon'|'MultiPolygon';arcs:number[][]|number[][][];properties:Period};
export type HistoryTopology = {type:'Topology';arcs:Position[][];objects:{countries:{geometries:TopologyGeometry[]}}};
export const statuses:Record<string,string>={independent:'Estado independiente',colony:'Colonia',protectorate:'Protectorado',occupied:'Territorio ocupado',mandate:'Mandato', 'N/A':'Estatus no clasificado'};
const names:Record<string,string>={'United States of America':'Estados Unidos','United Kingdom':'Reino Unido','France':'Francia','India':'India','Egypt':'Egipto','Israel':'Israel','Palestine':'Palestina','Gaza':'Gaza','West Bank':'Cisjordania','Syria':'Siria','Japan':'Japón','Italy/Sardinia':'Italia','China':'China','French West Africa':'África Occidental Francesa','Algeria':'Argelia','French Guyana':'Guayana Francesa','French Polynesia':'Polinesia Francesa','Reunion':'Reunión','Germany (Prussia)':'Alemania','German Federal Republic':'República Federal de Alemania','German Democratic Republic':'República Democrática Alemana','Austria-Hungary':'Austria-Hungría','Austria':'Austria','Hungary':'Hungría','Czechoslovakia':'Checoslovaquia','Poland':'Polonia','Spain':'España','Portugal':'Portugal','Netherlands':'Países Bajos','Belgium':'Bélgica','Ireland':'Irlanda','Rumania':'Rumanía','Russia (Soviet Union)':'Rusia','Ukraine':'Ucrania','Yugoslavia':'Yugoslavia','South Sudan':'Sudán del Sur','Sudan':'Sudán','Turkey (Ottoman Empire)':'Turquía','Iran (Persia)':'Irán','Morocco':'Marruecos','Tunisia':'Túnez','Libya':'Libia','German Togoland':'Togo alemán','Kamerun':'Camerún alemán','British Togoland':'Togo británico','British Cameroons':'Camerún británico'};
const aliases:Record<string,string>={'United States of America':'USA','United Kingdom':'GBR','Germany (Prussia)':'DEU','German Federal Republic':'DEU','German Democratic Republic':'DDR','Italy/Sardinia':'ITA','Russia (Soviet Union)':'RUS','Rumania':'ROU','Macedonia (FYROM/North Macedonia)':'MKD','Congo':'COG','Congo, Democratic Republic of (Zaire)':'COD','Iran (Persia)':'IRN','Turkey (Ottoman Empire)':'TUR','Egypt':'EGY','Gambia':'GMB','Cote D\'Ivoire':'CIV','Burkina Faso (Upper Volta)':'BFA','Tanzania (Tanganyika)':'TZA','Swaziland (Eswatini)':'SWZ','Madagascar (Malagasy)':'MDG','Zimbabwe (Rhodesia)':'ZWE','Korea, Republic of':'KOR','Korea, People\'s Republic of':'PRK','Kyrgyz Republic':'KGZ','Laos':'LAO','Vietnam (Annam/Cochin China/Tonkin)':'VNM','Myanmar (Burma)':'MMR','Sri Lanka (Ceylon)':'LKA','Cambodia (Kampuchea)':'KHM','East Timor':'TLS','Surinam':'SUR','French Guyana':'GUF','Palestine':'PSE','West Bank':'PSE','Gaza':'PSE','Taiwan':'TWN','Bahamas':'BHS','Venezuela':'VEN','Bolivia':'BOL','Belarus (Byelorussia)':'BLR','Cape Verde':'CPV','Brunei':'BRN','New Zealand':'NZL'};
export function historicName(p:Period,year:number){
  if(p.gwcode===365)return year<=1916?'Imperio ruso':year<1922?'Rusia soviética':year<=1990?'Unión Soviética':'Rusia';
  if(p.country_name==='Germany (Prussia)')return year<=1917?'Imperio alemán':year===1918?'Alemania · transición republicana':year<=1932?'Alemania · República de Weimar':'Alemania nazi';
  if(p.country_name==='German Democratic Republic'&&year<1949)return 'Alemania · zona de ocupación soviética';
  if(p.country_name==='German Federal Republic')return year<1949?'Alemania · zonas de ocupación occidentales':year>=1990?'Alemania':'República Federal de Alemania';
  if(p.country_name==='Turkey (Ottoman Empire)'&&year<1923)return 'Imperio otomano';
  return names[p.country_name]??p.country_name;
}
export function hashColor(value:string){let n=0;for(const c of value)n=(n*31+c.charCodeAt(0))|0;return Math.abs(n)%12;}
const norm=(s:string)=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z]/g,'');
export function isoFor(p:Period,year:number,modernNames:Map<string,string>){
  if(p.status!=='independent'||(p.gwcode===365&&year<1992)||p.country_name==='Yugoslavia'||p.country_name==='Czechoslovakia'||p.country_name==='Austria-Hungary'||p.country_name==='German Democratic Republic')return '';
  return aliases[p.country_name]??modernNames.get(norm(p.country_name))??'';
}
export const normalizedName=norm;
export function periodsAt(topology:HistoryTopology,year:number){const date=`${year}-12-31`;return topology.objects.countries.geometries.filter(g=>g.properties.start<=date&&g.properties.end>=date);}
export function decodeGeometry(topology:HistoryTopology,g:TopologyGeometry):Polygon|MultiPolygon{
  const arc=(n:number)=>{const coordinates=topology.arcs[n<0?~n:n];return n<0?[...coordinates].reverse():coordinates;};
  const ring=(indices:number[])=>indices.flatMap((n,i)=>i?arc(n).slice(1):arc(n));
  return g.type==='Polygon'?{type:'Polygon',coordinates:(g.arcs as number[][]).map(ring)}:{type:'MultiPolygon',coordinates:(g.arcs as number[][][]).map(p=>p.map(ring))};
}
export function historyAt(topology:HistoryTopology,year:number,modernNames:Map<string,string>=new Map(),geometryCache=new Map<number,Polygon|MultiPolygon>()):FeatureCollection{
  const active=periodsAt(topology,year);
  const byCode=new Map(active.map(g=>[String(g.properties.gwcode),g.properties]));
  const geometryFor=(g:TopologyGeometry)=>{let geometry=geometryCache.get(g.properties.fid);if(!geometry){geometry=decodeGeometry(topology,g);geometryCache.set(g.properties.fid,geometry);}return geometry;};
  return {type:'FeatureCollection',features:active.map(g=>{
    const p=g.properties;
    // Sinai and Golan occupation is represented separately, not as sovereign incorporation.
    let geometry=g;
    if(year>=1967&&['Egypt','Israel','Syria'].includes(p.country_name))geometry=topology.objects.countries.geometries.find(a=>a.properties.country_name===p.country_name&&a.properties.start<='1966-12-31'&&a.properties.end>='1966-12-31')??g;
    const name=historicName(p,year);
    const owner=p.status==='independent'?name:byCode.has(p.owner)?historicName(byCode.get(p.owner)!,year):`Potencia ${p.owner}`;
    return {type:'Feature',id:p.fid,geometry:geometryFor(geometry),properties:{...p,name,originalName:p.country_name,code:isoFor(p,year,modernNames),group:owner,color:hashColor(p.owner),capital:p.capname,ownerName:owner,politicalStatus:statuses[p.status]??p.status,source:'https://icr.ethz.ch/data/cshapes/'}} as Feature;
  })};
}
export function historicalCapitals(data:FeatureCollection):FeatureCollection{
  const seen=new Set<string>();
  return {type:'FeatureCollection',features:data.features.flatMap(f=>{
    const p=f.properties!;const key=`${p.caplong}:${p.caplat}`;
    if(!p.capname||!Number.isFinite(p.caplong)||seen.has(key))return[];
    seen.add(key);return [{type:'Feature',geometry:{type:'Point',coordinates:[p.caplong,p.caplat]},properties:{name:p.capname,country:p.name,capital:true,rank:p.status==='independent'?1:4,note:`Capital o sede administrativa de ${p.name} en el registro histórico consultado.`,source:p.source}} as Feature];
  })};
}
