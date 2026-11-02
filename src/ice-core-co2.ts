import series from'../public/data/ice-core-co2.json'with{type:'json'};
import{ageFromYear}from'./ice-history';
export const iceCoreCO2=series;
/** Gas age is calendar BP1950. Return the real nearest measurement, never an annual interpolation. */
export function iceCoreAtAge(ageBP:number){
 if(!Number.isFinite(ageBP)||ageBP<series.rows[0].ageBP||ageBP>series.rows.at(-1)!.ageBP)return;
 let lo=0,hi=series.rows.length-1;while(lo<hi){const mid=(lo+hi)>>>1;if(series.rows[mid].ageBP<ageBP)lo=mid+1;else hi=mid;}
 const after=series.rows[lo],before=series.rows[Math.max(0,lo-1)];return Math.abs(before.ageBP-ageBP)<=Math.abs(after.ageBP-ageBP)?before:after;
}
export function prehistoricCO2(year:number){return Number.isInteger(year)&&year<=-10001?iceCoreAtAge(ageFromYear(year)):undefined;}
