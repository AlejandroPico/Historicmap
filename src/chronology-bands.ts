import {geologicalUnits,humanUnits,geologicalEmphasis,rankLabels,type GeologicalRank,type HumanUnit} from './earth-chronology';
import {anchors,PRESENT,yearToPosition,positionToYear} from './time';
import {escapeHtml as esc} from './profiles';
import{chronologyDisplayColor}from'./deep-earth';

export interface Band {id:string;name:string;title:string;color:string;row:number;x:number;width:number;family:'geological'|'human'}
export function chronologyBands(year:number,position:number,spacing:number,width:number){
 const left=position-width/(2*spacing),right=position+width/(2*spacing);
 const from=positionToYear(left),to=positionToYear(right);
 const span=Math.max(1,to-from),emphasis=geologicalEmphasis(year,span);
 const bands:Band[]=[];
 function add(id:string,name:string,title:string,color:string,row:number,start:number,end:number,family:Band['family']){
  const x=Math.max(0,(yearToPosition(Math.max(anchors[0],start))-left)*spacing);
  const edge=Math.min(width,(yearToPosition(Math.min(PRESENT,end))-left)*spacing);
  if(edge>x+.5)bands.push({id,name,title,color,row,x,width:edge-x,family});
 }
 const ranks:GeologicalRank[]=span>500e6?['eon','era','period']:span>50e6?['era','period','epoch']:['period','epoch','age'];
 // Before the Phanerozoic, periods/epochs may not exist; never invent them.
 if(year<geologicalUnits.find(u=>u.id==='Phanerozoic')!.axisOldestYear){ranks.splice(0,3,'eon','era','period');}
 for(const unit of geologicalUnits){
  const row=ranks.indexOf(unit.rank);if(row<0)continue;
  const contextual=unit.rank==='eon'&&unit.parent==='Precambrian'?'Precámbrico · ':'';
  add(unit.id,contextual+unit.name,`${rankLabels[unit.rank]} · ${contextual}${unit.name}${unit.formal?'':' · denominación contextual/informal'} · ICS ${unit.timeBasis}`,unit.color,row,unit.axisOldestYear,unit.axisEndYear??PRESENT,'geological');
 }
 const lanes:HumanUnit['lane'][]=['overview','regional','transformation'];
 for(const [row,lane] of lanes.entries()){
  const units=humanUnits.filter(u=>u.lane===lane&&u.startYear<to&&(u.endYear===null||u.endYear>from));
  const cuts=[...new Set([from,to,...units.flatMap(u=>[Math.max(from,u.startYear),Math.min(to,u.endYear??to)])])].sort((a,b)=>a-b);
  const pieces:{unit:HumanUnit;start:number;end:number}[]=[];
  for(let i=0;i<cuts.length-1;i++){
   const midpoint=(cuts[i]+cuts[i+1])/2;
   const winner=units.filter(u=>u.startYear<=midpoint&&(u.endYear===null||u.endYear>midpoint)).sort((a,b)=>b.priority-a.priority)[0];
   if(!winner)continue;
   const previous=pieces.at(-1);if(previous?.unit.id===winner.id&&previous.end===cuts[i])previous.end=cuts[i+1];else pieces.push({unit:winner,start:cuts[i],end:cuts[i+1]});
  }
  for(const{unit,start,end}of pieces)add(unit.id,unit.name+(unit.lane==='regional'&&unit.scope.includes('Francia')?' · Francia':''),`${unit.name} · ${unit.scope} · ${unit.precision}`,unit.color,row,start,end,'human');
 }
 return{bands,emphasis,span};
}
function ink(color:string){const n=parseInt(color.slice(1),16);return .2126*(n>>16)+.7152*((n>>8)&255)+.0722*(n&255)>145?'#14242c':'#ffffff';}
export function chronologyBandsMarkup(model:ReturnType<typeof chronologyBands>){
 return(['geological','human'] as const).map(family=>{
  const opacity=family==='geological'?model.emphasis:1-model.emphasis;
  const labelled=family==='geological'?model.emphasis>=.5:model.emphasis<.5;
  return `<div class="chronology-family" data-family="${family}" style="opacity:${opacity}" aria-hidden="${!labelled}">${model.bands.filter(b=>b.family===family).map(b=>{const color=chronologyDisplayColor(b.id,b.color),name=b.name.startsWith('Precámbrico · ')&&b.width<165?b.name.replace('Precámbrico · ',''):b.name;return`<button type="button" class="chronology-band" data-unit="${b.id}" data-encyclopedia-entry="${family==='human'?'human-':'geo-'}${b.id}" tabindex="${labelled?0:-1}" aria-label="${esc(b.title)} · Abrir enciclopedia" title="${esc(b.title)}" style="left:${b.x}px;width:${b.width}px;top:${b.row*17}px;--band-color:${color};--band-ink:${ink(color)}">${labelled&&b.width>name.length*6+14?`<span>${esc(name)}</span>`:''}</button>`}).join('')}</div>`;
 }).join('');
}
