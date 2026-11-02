export interface RulerLabel {year:number;x:number;width:number}
/** Reserve the BCE/CE seam, then fit labels in screen space; ticks remain untouched. */
export function readableRulerLabels(labels:RulerLabel[],gap=12){
 const accepted:RulerLabel[]=[],years=new Set<number>();
 const sorted=[...labels].sort((a,b)=>Number(b.year===1)-Number(a.year===1)||a.x-b.x);
 for(const label of sorted){
  if(accepted.some(a=>Math.abs(a.x-label.x)<(a.width+label.width)/2+gap))continue;
  accepted.push(label);years.add(label.year);
 }
 return years;
}
