/** A right-button double click, excluding rotation drags and touch gestures. */
export function installNorthGesture(canvas:HTMLCanvasElement,resetNorth:()=>void){
 let down:{id:number;x:number;y:number}|undefined,last:{time:number;x:number;y:number}|undefined;
 const rightMouse=(e:PointerEvent|MouseEvent)=>e.button===2&&(!('pointerType'in e)||!e.pointerType||e.pointerType==='mouse');
 const clear=()=>{down=undefined;last=undefined;};
 const start=(e:PointerEvent)=>{if(rightMouse(e))down={id:e.pointerId,x:e.clientX,y:e.clientY};else clear();};
 const move=(e:PointerEvent)=>{if(down&&e.pointerId===down.id&&Math.hypot(e.clientX-down.x,e.clientY-down.y)>6)clear();};
 const end=(e:PointerEvent)=>{
  if(!down||e.pointerId!==down.id||!rightMouse(e))return;
  if(Math.hypot(e.clientX-down.x,e.clientY-down.y)>6){clear();return;}
  const click={time:e.timeStamp,x:e.clientX,y:e.clientY};down=undefined;
  if(last&&click.time-last.time<=500&&Math.hypot(click.x-last.x,click.y-last.y)<=8){last=undefined;resetNorth();}else last=click;
 };
 const context=(e:MouseEvent)=>{if(rightMouse(e))e.preventDefault();};
 canvas.addEventListener('pointerdown',start);canvas.addEventListener('pointermove',move);canvas.addEventListener('pointerup',end);canvas.addEventListener('pointercancel',clear);canvas.addEventListener('pointerleave',clear);canvas.addEventListener('contextmenu',context);
 return()=>{canvas.removeEventListener('pointerdown',start);canvas.removeEventListener('pointermove',move);canvas.removeEventListener('pointerup',end);canvas.removeEventListener('pointercancel',clear);canvas.removeEventListener('pointerleave',clear);canvas.removeEventListener('contextmenu',context);};
}
