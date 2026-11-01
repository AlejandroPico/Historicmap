import{readFileSync}from'node:fs';
import{regionalCoverage}from'../src/cultural-regions';
import{ANNUAL_CONSULTATION_START}from'../src/time';
const read=(file:string)=>JSON.parse(readFileSync(file,'utf8'));
const manifest=read('public/data/manifest.json'),regional=read('public/data/cultural-index.json');
export const firstPoliticalYear=Math.min(...manifest.entries.filter((e:any)=>e.format==='dated-entity-resolution').map((e:any)=>e.coverageStart));
// Archaeological consultation may precede the first dated state outline.
// Below the floor, a reference can be historical or conceptual; older period tests
// must assert absence of annual consultation rather than a permanent snapshot type.
export const firstAnnualYear=ANNUAL_CONSULTATION_START;
export const firstRegionalYear=Math.min(...regionalCoverage.windows.map((w:any)=>w.start));
if(!Number.isFinite(firstAnnualYear)||!Number.isFinite(firstPoliticalYear)||!Number.isFinite(firstRegionalYear))throw Error('Missing temporal coverage inventory');
export function culturalDossiersForSource(year:number):any[]{
 const suffix='-Y'+String(year).padStart(4,'0')+'.json';
 const files=new Set<string>([...regional.records.map((r:any)=>r.canonicalFile),...regional.excluded.map((r:any)=>r.file)].filter((f:string)=>f.endsWith(suffix)));
 return [...files].map(read);
}
