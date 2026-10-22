import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../public/data/',import.meta.url);
const manifest=JSON.parse(await readFile(new URL('manifest.json',root)));
for(const file of ['spanish-civil-war.geojson','identities.json']){
 const bytes=await readFile(new URL(file,root));const data=JSON.parse(bytes);
 const entry={file,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),...(file==='identities.json'?{
  format:'dated-political-identities',countries:Object.keys(data.countries).length,records:Object.values(data.countries).reduce((n,c)=>n+c.leaders.length,0),source:'Wikidata CC0 statements, focal institutional chronology and Wikimedia Commons media',version:`Retrieved ${data.retrieved}; Historicmap curation 0.4`,url:'https://www.wikidata.org/',license:data.license,transform:'P6/P35 qualified statements and dated P39 officeholders, with focal authorities. No undated incumbent retrojected. Per-media licenses and checksums in public/media/manifest.json. Past year-end reference; present capped at retrieval date; no future extrapolation.'
 }:{
  features:data.features.length,source:'Cliopatria, Tyk / Té y kriptonita, Natural Earth',version:'Cliopatria 5f433377139a6eeaeacbdc894b70f8805b72c8b5; Tyk SVG revision 2016-12-21; Natural Earth pinned countries',url:'https://commons.wikimedia.org/wiki/File:GCE-Frente_en_oct_1937.svg',license:'CC-BY-4.0 (1936, 1938, 1939); CC-BY-SA-3.0 (1937); Natural Earth public domain',coverage:'1936/1939',transform:'Dated Spanish factions. Original interior fronts of Cliopatria 1936/1938 joined to Natural Earth European Spain coast. Tyk October 1937 front georeferenced with 15 control points (mean residual 4954m, minimum registration uncertainty 10km). Republic complement; no invented province assignments, overlap or gaps. 1939 victory. Full transformation, SVG checksum and attribution in embedded metadata and docs/SPANISH-CIVIL-WAR.md.'
 })};
 manifest.entries=manifest.entries.filter(e=>e.file!==file);manifest.entries.push(entry);
}
manifest.entries.sort((a,b)=>a.file.localeCompare(b.file));
await writeFile(new URL('manifest.json',root),JSON.stringify(manifest,null,2)+'\n');
console.log('Registered political identities and Spanish fronts; each retains its own license.');
