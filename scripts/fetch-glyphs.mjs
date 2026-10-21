import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const version='601ae60796ceceda2cbd2ed3d2ea92d17a84be4b';
const upstream=`https://raw.githubusercontent.com/maplibre/demotiles/${version}/font/Noto%20Sans%20Regular/`;
const root=new URL('../public/fonts/',import.meta.url);
await mkdir(new URL('Noto Sans Regular/',root),{recursive:true});
const ranges=new Set([0,256]);
for(const file of JSON.parse(await readFile(new URL('../public/data/manifest.json',import.meta.url))).entries.filter(e=>e.file.endsWith('.geojson')||e.file==='history.topojson')){
 const data=JSON.parse(await readFile(new URL('../public/data/'+file.file,import.meta.url)));
 const props=data.features?.map(f=>f.properties)??data.objects.countries.geometries.map(g=>g.properties);
 for(const p of props)for(const s of [p.name,p.capname,p.country_name])for(const c of String(s??'')){
   const point=c.codePointAt(0);if(point<=65535)ranges.add(Math.floor(point/256)*256);
 }
}
const entries=[];
for(const n of [...ranges].sort((a,b)=>a-b)){
 const file=`${n}-${n+255}.pbf`,url=upstream+file;
 const response=await fetch(url);if(!response.ok)throw Error(`${response.status}: ${url}`);
 const bytes=Buffer.from(await response.arrayBuffer());
 await writeFile(new URL('Noto Sans Regular/'+file,root),bytes);
 entries.push({file:'Noto Sans Regular/'+file,url,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')});
}
const license=await fetch(upstream+'LICENSE.md');if(!license.ok)throw Error('Missing font license');
await writeFile(new URL('Noto Sans Regular/LICENSE.md',root),await license.text());
await writeFile(new URL('manifest.json',root),JSON.stringify({source:'MapLibre demo glyphs; generated using OpenMapTiles/fonts Noto Sans sources',version,license:'SIL-OFL-1.1',transform:'Unmodified PBF ranges needed by bundled labels (BMP). No font rasterization or outline changes.',entries},null,2)+'\n');
console.log(`Stored ${entries.length} local glyph ranges with source checksums and license.`);
