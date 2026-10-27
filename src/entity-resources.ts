import {isoYear} from './dates';
import {escapeHtml as esc} from './profiles';
type Resource={file:string;title:string;source:string;license:string;start:string;end:string;artist?:string};
type Extension={key:string;resources:Resource[]};
const catalogues=import.meta.glob('../Países/*/recursos.json',{eager:true,import:'default'}) as Record<string,Extension>;
const files=import.meta.glob('../Países/*/archivos/*.{mp3,ogg,wav,m4a,pdf}',{eager:true,query:'?url',import:'default'}) as Record<string,string>;
export function entityResources(key:string,year:number){
 const first=`${isoYear(year)}-01-01`,last=`${isoYear(year)}-12-31`;
 return Object.entries(catalogues).filter(([,c])=>c.key===key).flatMap(([path,c])=>c.resources.filter(r=>r.start<=last&&r.end>=first).flatMap(r=>{
  const url=files[path.replace('recursos.json','archivos/'+r.file)];if(!url)return[];
  return [{...r,url}];
 }));
}
export function resourceMarkup(key:string,year:number){
 const resources=entityResources(key,year);if(!resources.length)return '';
 return `<section class="entity-resources"><h3>Himnos y documentos</h3>${resources.map(r=>`<article><h4>${esc(r.title)}</h4>${/\.pdf$/i.test(r.file)?`<a href="${esc(r.url)}" target="_blank" rel="noopener">Abrir documento ↗</a>`:`<audio controls preload="none" src="${esc(r.url)}" aria-label="${esc(r.title)}"></audio>`}<p class="profile-note">${esc(r.start)} — ${esc(r.end)}</p><a class="media-credit" href="${esc(r.source)}" target="_blank" rel="noopener">${esc(r.artist??'Procedencia')} · ${esc(r.license)} ↗</a></article>`).join('')}</section>`;
}
