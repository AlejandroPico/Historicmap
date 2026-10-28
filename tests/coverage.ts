import{readFileSync}from'node:fs';
const read=(file:string)=>JSON.parse(readFileSync(file,'utf8'));
const manifest=read('public/data/manifest.json'),regional=read('public/data/cultural-index.json');
export const firstAnnualYear=Math.min(...manifest.entries.filter((e:any)=>e.format==='dated-entity-resolution').map((e:any)=>e.coverageStart));
export const firstRegionalYear=Math.min(...regional.windows.map((w:any)=>w.start));
if(!Number.isFinite(firstAnnualYear)||!Number.isFinite(firstRegionalYear))throw Error('Missing temporal coverage inventory');
export function culturalDossiersForSource(year:number):any[]{
 const suffix='-Y'+String(year).padStart(4,'0')+'.json';
 const files=new Set<string>([...regional.records.map((r:any)=>r.canonicalFile),...regional.excluded.map((r:any)=>r.file)].filter((f:string)=>f.endsWith(suffix)));
 return [...files].map(read);
}
