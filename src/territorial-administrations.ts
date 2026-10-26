import catalogue from '../public/data/territorial-administrations.json';
import extension from '../public/data/historical-1880-administrations.json';
export type Administration={id:string;names:string[];codes:string[];admin:string;localKey:string;start:string;end:string|null;label:string;note:string;source:string;headOfStateOnly:boolean};
export function administrationFor(p:Record<string,any>,year:number):Administration|undefined{
 if(p.collectiveAdministration)return; // A grouped occupation is not a single national administrator.
 if(year<1500||year>Number(catalogue.referenceDate.slice(0,4)))return;
 const name=String(p.originalName??p.country_name??p.name??''),code=String(p.entityCode||p.code||'');
 const record=[...extension.records,...catalogue.records].find(r=>(r.names.includes(name)||(r.codes as string[]).includes(code))&&r.start<=`${year}-12-31`&&(!r.end||r.end>`${year}-01-01`));
 if(record)return record;
 // A retained card's source administrator is evidence only inside that source
 // interval, never before the colony is attested or after this observation.
 if(typeof p.start==='number'&&year<p.start||typeof p.end==='number'&&year>p.end)return;
 if(p.administratorKey&&p.administratorKey!==p.identityKey)return {id:'source-administration',names:[name],codes:[code],admin:p.administratorKey,localKey:p.localAuthorityKey??p.code??'',start:year<1900?'1500-01-01':catalogue.coverageStart,end:null,label:'Autoridades del Estado administrador',note:'La relación administrativa procede de la cartografía de esta fecha. Los cargos estatales no equivalen a gobernadores territoriales; la serie local todavía puede ser parcial.',source:p.source??'https://icr.ethz.ch/data/cshapes/',headOfStateOnly:false};
}
export function dayBefore(date:string){const d=new Date(date+'T12:00:00Z');d.setUTCDate(d.getUTCDate()-1);return d.toISOString().slice(0,10);}
