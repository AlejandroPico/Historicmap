import type{FeatureCollection,Position}from'geojson';
import{deepIceAt,type DeepScene}from'./deep-earth';
const rgb=(hex:string)=>[parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16)];
const mix=(a:number[],b:number[],t:number)=>a.map((v,i)=>v*(1-t)+b[i]*t);
/** Smooth, periodic 3-D field on the sphere: no random change when a date is revisited. */
function field(x:number,y:number,z:number){return Math.sin(x*3.4+y*2.1+z*4.8)+.48*Math.sin(x*8.3-y*6.1+z*3.7)+.22*Math.sin(x*18.1+y*13.8-z*15.3)+.08*Math.sin(x*41-y*33+z*29);}
export function drawDeepSurface(canvas:HTMLCanvasElement,scene:DeepScene,year:number,coast?:FeatureCollection,showIce=true){
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
     const cap=ice==='snowball'?0.97:ice==='huronian'?Math.max(0,(Math.abs(z)-.53)*2.5):continental>.5&&n>.5&&fine>.3?.65:0;
     if(cap>0){const frost=Math.min(1,cap+fine*(ice==='snowball'?.015:.10));c=mix(c,[216+fine*3,231+fine*2,231+fine*2],Math.max(0,frost));}
    }
   }
   pixels.data[i]=Math.max(0,Math.min(255,c[0]));pixels.data[i+1]=Math.max(0,Math.min(255,c[1]));pixels.data[i+2]=Math.max(0,Math.min(255,c[2]));pixels.data[i+3]=255;
  }
 }
 ctx.putImageData(pixels,0,0);
}
