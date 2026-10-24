import clipping,{type MultiPolygon as MP,type Polygon as P} from 'polygon-clipping';
import type {Feature,FeatureCollection,Polygon,MultiPolygon} from 'geojson';
type Area=Feature<Polygon|MultiPolygon>;
const area=(f:Feature):f is Area=>f.geometry.type==='Polygon'||f.geometry.type==='MultiPolygon';
const parts=(f:Area):MP=>(f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates) as MP;
const geometry=(f:Feature,c:MP):Area=>({...f,geometry:{type:'MultiPolygon',coordinates:c}});
function box(c:MP){const b=[Infinity,Infinity,-Infinity,-Infinity];for(const p of c)for(const r of p)for(const [x,y] of r){b[0]=Math.min(b[0],x);b[1]=Math.min(b[1],y);b[2]=Math.max(b[2],x);b[3]=Math.max(b[3],y);}return b;}
const overlap=(a:number[],b:number[])=>a[0]<=b[2]&&a[2]>=b[0]&&a[1]<=b[3]&&a[3]>=b[1];

/** Scoped documentary correction; no global island-size filter or raster mask.
 * Clio's1938/1939 German extents contain remote isolated cells and treat parts
 * of the Slovak client as German territory. Retain source components attached
 * to the dated theatre; protect countries not controlled by Germany that year.
 * Original licensed datasets remain immutable. See CENTRAL-EUROPE-1939.md.
 */
export function centralEuropeanControls(base:FeatureCollection,controls:FeatureCollection,year:number):FeatureCollection{
 if(year!==1938&&year!==1939)return controls;
 const areas=base.features.filter(area).map(f=>({f,c:parts(f),key:String(f.properties?.identityKey??'')}));
 const find=(key:string)=>areas.find(a=>a.key===key);
 const austria=find('AUT'),czech=find('CSK'),hungary=find('HUN');
 const protect=(c:MP,allowed:Set<string>)=>{
  const extent=box(c);
  for(const a of areas)if(c.length&&!allowed.has(a.key)&&overlap(extent,box(a.c)))c=clipping.difference(c,a.c);
  return c;
 };
 const prepared=controls.features.map(f=>{
  if(!area(f)||f.properties?.controller!=='DEU')return f;
  const observed=Number(f.properties.start),incorporation=f.properties.kind==='annexation-mask';
  if(observed!==1938&&observed!==1939)return f;
  const allowed=new Set(['DEU','AUT','CSK',...(observed===1939&&!incorporation?['POL']:[])]);
  const references=areas.filter(a=>allowed.has(a.key));
  const original=parts(f),retained=original.filter(p=>references.some(a=>overlap(box([p]),box(a.c))&&clipping.intersection(p as P,a.c).length>0));
  if(!retained.length)return f;
  let corrected=clipping.union(retained,...(austria?[austria.c]:[]));
  // The annual CShapes Czech component is already dated2Nov1938, after
  // Munich/Vienna. Its remaining land (including Olomouc) is not a Sudeten
  // annexation. Protect it in1938 and in the incorporation mask used for1939.
  const borderAllowed=new Set([...allowed].filter(k=>k!=='CSK'||observed===1939&&!incorporation));
  corrected=protect(corrected,borderAllowed);
  return {...geometry(f,corrected),properties:{...f.properties,sourceComponents:original.length,retainedSourceComponents:retained.length,controlCorrection:'central-europe-1938-1939',note:f.properties.note+' Corrección acotada: componentes aislados ajenos al teatro descartados sin umbral de superficie; fronteras de países no controlados protegidas con la base fechada. Austria incorporada completa, no una mancha sobre su antigua ficha.'}};
 });
 if(year!==1939||!czech||!hungary)return {...controls,features:prepared};
 const h=prepared.find(f=>f.properties?.uid==='central-hungary-1939'),s=prepared.find(f=>f.properties?.uid==='central-slovakia-reference-1939');
 if(!h||!s||!area(h)||!area(s))return {...controls,features:prepared};
 const annexation=prepared.find(f=>f.properties?.controller==='DEU'&&f.properties.kind==='annexation-mask');
 // CShapes already records the first Vienna Award. Clio's coarse1939 outline
 // wrongly reaches central Bratislava; use it only for the additional eastern
 // extent outside the Slovak reference, retaining the finer dated boundary.
 const h1939=clipping.union(hungary.c,clipping.difference(clipping.intersection(parts(h),clipping.union(hungary.c,czech.c)),parts(s)));
 let slovakia=clipping.difference(clipping.intersection(parts(s),czech.c),h1939);
 if(annexation&&area(annexation))slovakia=clipping.difference(slovakia,parts(annexation));
 const bohemiaMoravia=clipping.difference(czech.c,slovakia,h1939);
 return {...controls,features:prepared.map(f=>{
  if(f===h)return geometry(f,h1939);
  if(f===s)return geometry(f,slovakia);
  if(area(f)&&f.properties?.controller==='DEU'&&f.properties.kind!=='annexation-mask')return geometry(f,clipping.difference(clipping.union(parts(f),bohemiaMoravia),slovakia,h1939));
  return f;
 })};
}
