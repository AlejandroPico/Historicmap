// Explicit, cached data refresh; builds never contact these services.
import {readFile, writeFile, mkdir} from 'node:fs/promises';
const cache=new URL('../.cache/',import.meta.url);
await mkdir(cache,{recursive:true});
const manifest=JSON.parse(await readFile(new URL('../public/data/manifest.json',import.meta.url)));
const version=manifest.entries.find(e=>e.file==='countries.geojson').version;
const jobs=[
  ['natural-countries.json',`https://raw.githubusercontent.com/nvkelso/natural-earth-vector/${version}/geojson/ne_10m_admin_0_countries.geojson`],
  ['natural-places.json',`https://raw.githubusercontent.com/nvkelso/natural-earth-vector/${version}/geojson/ne_10m_populated_places.geojson`],
  ['wb-countries.json','https://api.worldbank.org/v2/es/country?format=json&per_page=400'],
  ...['SP.POP.TOTL','NY.GDP.MKTP.CD','NY.GDP.PCAP.CD','SP.DYN.LE00.IN','SP.URB.TOTL.IN.ZS','AG.SRF.TOTL.K2'].map(id=>[`wb-${id}.json`,`https://api.worldbank.org/v2/country/all/indicator/${id}?source=2&date=1960:${new Date().getFullYear()}&format=json&per_page=24000`])
];
for(let i=0;i<jobs.length;i+=3) await Promise.all(jobs.slice(i,i+3).map(async([file,url])=>{
  try {await readFile(new URL(file,cache)); console.log(`Cached ${file}`);return;} catch{}
  for(let attempt=0;attempt<4;attempt++)try{
    const response=await fetch(url,{signal:AbortSignal.timeout(180000)});
    if(!response.ok)throw Error(`${response.status}: ${url}`);
    const data=await response.json();
    if(Array.isArray(data)&&data[0]?.pages>1)throw Error('Unexpected pagination; raise per_page');
    await writeFile(new URL(file,cache),JSON.stringify(data));
    await writeFile(new URL(`${file}.source.json`,cache),JSON.stringify({url,version: file.startsWith('wb-')?data[0].lastupdated??new Date().toISOString().slice(0,10):version,retrieved:new Date().toISOString()}));
    console.log(`Downloaded ${file}`);break;
  }catch(error){if(attempt===3)throw error;await new Promise(resolve=>setTimeout(resolve,1000*(attempt+1)));}
}));
