import type {FeatureCollection} from 'geojson';

export type EntityResolution={coverageStart:number;coverageEnd:number;qidKeys:Record<string,string>;names:Record<string,string>;records:{names:string[];key:string;label:string;entityCode:string;admin:string;status:string;start:number;end:number;source:string;note:string}[]};

/** Date-scoped identity repair over unchanged source contours. A source label
 * such as Haiti's old Empire must not select an emperor in the1880 republic. */
export function resolve1880(data:FeatureCollection,year:number,catalogue:EntityResolution):FeatureCollection{
 if(year<catalogue.coverageStart||year>catalogue.coverageEnd)return data;
 return {...data,features:data.features.map(f=>{
  const p=f.properties??{},sourceName=String(p.originalName??p.name??''),early=year<1886;
  const rule=catalogue.records.find(r=>r.names.includes(sourceName)&&r.start<=year&&r.end>=year);
  if(!early&&!rule)return f;
  const key=rule?.key??catalogue.qidKeys[String(p.wikidata??'')];
  const label=rule?.label??catalogue.names[key]??p.name;
  const status=rule?.status??p.status??'source-polity';
  const owner=rule?.admin?catalogue.names[rule.admin]??rule.admin:undefined;
  const note=[p.note,rule?.note,early?'Geometría de síntesis Cliopatria sin día uniforme; la corrección de identidad no certifica todos sus límites ni su periodización.':''].filter(Boolean).join(' ');
  return {...f,properties:{...p,sourceName,sourceWikidata:p.wikidata,
   name:label,identityKey:key??p.identityKey,entityCode:rule?.entityCode??(early?key:p.entityCode),
   code:early||['BRA-EMPIRE','JOS','HAW-KINGDOM','HAW-PROVISIONAL','HAW-REPUBLIC','HAW'].includes(key)?'':p.code,
   ...(early?{status}:{}),...(rule?.admin?{status,administratorKey:rule.admin,localAuthorityKey:key,ownerName:owner,group:owner}:{}),
   ...(rule?{identityCorrection:'dated-1880-1899',identitySource:rule.source}:{}),
   ...(status==='source-reference'?{politicalStatus:'Contorno de fuente con cronología sin resolver'}:{}),note,
   ...(early&&!rule?.admin?{parentName:''}:{}),
  }};
 })};
}
