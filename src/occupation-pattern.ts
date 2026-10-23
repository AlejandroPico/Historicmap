/** Seamless diagonal stripes: 3/4 controller, 1/4 occupied territory. */
export function occupationPattern(controller:string,occupied:string,size=16){
 const data=new Uint8Array(size*size*4);
 const rgb=(hex:string)=>[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16));
 const broad=rgb(controller),fine=rgb(occupied);
 for(let y=0;y<size;y++)for(let x=0;x<size;x++)data.set([...((x+y)%size<size/4?fine:broad),255],(y*size+x)*4);
 return {width:size,height:size,data};
}
