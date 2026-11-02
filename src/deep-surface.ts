import type{FeatureCollection,Position}from'geojson';
import{deepIceAt,type DeepScene}from'./deep-earth';
const rgb=(hex:string)=>[parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16)];
const mix=(a:number[],b:number[],t:number)=>a.map((v,i)=>v*(1-t)+b[i]*t);
/** Smooth, periodic 3-D field on the sphere: no random change when a date is revisited. */
function noise(x:number,y:number,z:number){const a=Math.floor(x),b=Math.floor(y),c=Math.floor(z),smooth=(t:number)=>t*t*(3-2*t),u=smooth(x-a),v=smooth(y-b),w=smooth(z-c);const hash=(i:number,j:number,k:number)=>{let n=Math.imul(i,374761393)^Math.imul(j,668265263)^Math.imul(k,2147483647);n=Math.imul(n^(n>>>13),1274126177);return((n^(n>>>16))>>>0)/2147483647-1};const lerp=(p:number,q:number,t:number)=>p+(q-p)*t;return lerp(lerp(lerp(hash(a,b,c),hash(a+1,b,c),u),lerp(hash(a,b+1,c),hash(a+1,b+1,c),u),v),lerp(lerp(hash(a,b,c+1),hash(a+1,b,c+1),u),lerp(hash(a,b+1,c+1),hash(a+1,b+1,c+1),u),v),w);}
function field(x:number,y:number,z:number){return noise(x*3,y*3,z*3)+.5*noise(x*7+19,y*7-8,z*7+5)+.25*noise(x*17-6,y*17+14,z*17);}
export function drawDeepSurface(canvas:HTMLCanvasElement,scene:DeepScene,year:number,coast?:FeatureCollection,showIce=true,optics:'standard'|'ferruginous'='standard'){
 const w=canvas.width,h=canvas.height,ctx=canvas.getContext('2d')!,pixels=ctx.createImageData(w,h),ocean=rgb(scene.ocean),land=rgb(scene.land);
 let mask:Uint8ClampedArray|undefined;
 if(coast?.features.length){
  const c=document.createElement('canvas');c.width=w;c.height=h;const m=c.getContext('2d')!;m.fillStyle='#fff';
  const point=(p:Position)=>[(p[0]+180)/360*w,(1-Math.log(Math.tan(Math.PI/4+Math.max(-85.051,Math.min(85.051,p[1]))*Math.PI/360))/Math.PI)/2*h];
  for(const f of coast.features){const polys=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.type==='MultiPolygon'?f.geometry.coordinates:[];
   for(const poly of polys){m.beginPath();for(const ring of poly){ring.forEach((p,i)=>{const[x,y]=point(p);if(i===0)m.moveTo(x,y);else m.lineTo(x,y)});m.closePath();}m.fill('evenodd');}}
  mask=m.getImageData(0,0,w,h).data;
 }
 const ice=showIce?deepIceAt(year):null;
 for(let py=0;py<h;py++){
  const lat=Math.atan(Math.sinh(Math.PI*(1-2*(py+.5)/h))),cl=Math.cos(lat),z=Math.sin(lat);
  for(let px=0;px<w;px++){
   const lon=((px+.5)/w*2-1)*Math.PI,x=cl*Math.cos(lon),y=cl*Math.sin(lon),n=field(x,y,z),fine=field(x*5+2,y*5-3,z*5+7),i=(py*w+px)*4;
   const continental=mask?mask[i+3]/255:n>(1.55-scene.landFraction*3.5)?1:0;
   let c:number[];
   if(scene.mode==='magma'||scene.mode==='cooling'){
    const ridge=Math.abs(n+.22*Math.sin(fine*4));const heat=scene.mode==='magma'?.48+.52*Math.max(0,1-ridge*1.5):Math.max(0,1-ridge*7);
    c=mix(scene.mode==='magma'?[115,29,12]:[28,22,24],[244,81,15],Math.min(1,heat*.95));if(heat>.7)c=mix(c,[255,216,112],(heat-.7)*2.7);
    c=c.map(v=>v*(.85+fine*.08));
   }else{
    c=continental>.4?land.map(v=>v*(.83+n*.08+fine*.045)):ocean.map(v=>v*(.92+n*.028+fine*.025));
    if(mask&&continental>0&&continental<.9)c=mix(ocean,land,continental);
    if(ice){
     const rugged=n*.13+fine*.055;
     const cap=ice==='snowball'?.97:ice==='antarctic'?Math.max(0,(-z-.86+rugged)*8):ice==='gondwana'?Math.max(0,(-z-.52+rugged)*4)*(continental>.4?1:.22):ice==='huronian'?Math.max(0,(Math.abs(z)-.57+rugged)*3):continental>.5&&n>.3&&fine>.2?.65:0;
     if(cap>0){const frost=Math.min(1,cap+fine*(ice==='snowball'?.015:.10));c=mix(c,[216+fine*3,231+fine*2,231+fine*2],Math.max(0,frost));}
    }
    const age=(1950-(year<0?year+1:year))/1e6;
    if(age>=2500&&age<=3400)c=mix(c,[173,101,51],.24+Math.max(0,fine)*.08);
    if(optics==='ferruginous'&&age>=2100&&age<=2600&&continental<.5)c=mix(c,[157,62,37],.74);
   }
   pixels.data[i]=Math.max(0,Math.min(255,c[0]));pixels.data[i+1]=Math.max(0,Math.min(255,c[1]));pixels.data[i+2]=Math.max(0,Math.min(255,c[2]));pixels.data[i+3]=255;
  }
 }
 ctx.putImageData(pixels,0,0);
}
