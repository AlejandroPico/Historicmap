import {composeControl} from './control-map';
self.onmessage=({data})=>{
 try{self.postMessage({id:data.id,result:composeControl(data.base,data.controls,data.year)});}
 catch(error){self.postMessage({id:data.id,error:error instanceof Error?error.message:String(error)});}
};
