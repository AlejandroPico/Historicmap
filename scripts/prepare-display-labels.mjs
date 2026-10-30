/** Compile entity-owned Spanish labels without rewriting historical source names. */
import{readFileSync,writeFileSync,readdirSync,existsSync}from'node:fs';import{createHash}from'node:crypto';
const labels={},owners={};
for(const dir of readdirSync('Países',{withFileTypes:true}).filter(d=>d.isDirectory()).sort((a,b)=>a.name<b.name?-1:a.name>b.name?1:0)){
 const file='Países/'+dir.name+'/rotulos.json';if(!existsSync(file))continue;
 const data=JSON.parse(readFileSync(file,'utf8'));if(!data.key||data.language!=='es'||!data.source)throw Error('Invalid label provenance '+file);
 for(const[from,to]of Object.entries(data.labels??{})){
  if(typeof to!=='string'||!to.trim())throw Error('Empty display label '+file);
  if(labels[from]&&labels[from]!==to)throw Error('Conflicting display label '+from);
  labels[from]=to;owners[from]??=file;
 }
}
const ordered=object=>Object.fromEntries(Object.entries(object).sort(([a],[b])=>a<b?-1:a>b?1:0));
const output={format:'entity-display-labels',language:'es',labels:ordered(labels),owners:ordered(owners)};
const raw=JSON.stringify(output,null,2)+'\n',file='public/data/display-labels.json';
if(!existsSync(file)||readFileSync(file,'utf8')!==raw)writeFileSync(file,raw);
const path='public/data/manifest.json',manifest=JSON.parse(readFileSync(path,'utf8'));
const entry={file:'display-labels.json',format:output.format,source:'Entity-owned Spanish editorial labels',url:'https://github.com/AlejandroPico/Historicmap/tree/main/Pa%C3%ADses',license:'CC0-1.0 (editorial translations)',version:'Historicmap '+JSON.parse(readFileSync('package.json','utf8')).version,records:Object.keys(labels).length,bytes:Buffer.byteLength(raw),sha256:createHash('sha256').update(raw).digest('hex')};
manifest.entries=manifest.entries.filter(e=>e.file!==entry.file).concat(entry);const text=JSON.stringify(manifest,null,2)+'\n';if(readFileSync(path,'utf8')!==text)writeFileSync(path,text);
console.log('Spanish display labels:',Object.keys(labels).length);
