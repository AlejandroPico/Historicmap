import knowledge from '../public/data/human-knowledge.json' with {type:'json'};
import{escapeHtml as esc}from'./profiles';
export const humanKnowledge=knowledge;
export function humanArticleForYear(year:number){
 if(year< -7000000||year> -3000)return;
 return year< -4200000?'hominin-origins':year< -2600000?'australopithecines':year< -600000?'early-homo-world':year< -100000?'human-diversity':year< -12000?'human-dispersals':'neolithic-transition';
}
export function humanPhoto(article:string,compact=false,referenceOnly=false){
 const m=knowledge.images.find(m=>m.articleIds.includes(article));if(!m)return'';
 return`<figure class="human-fossil-photo ${compact?'compact':''}"><img src="${import.meta.env.BASE_URL+m.file}" alt="${esc(m.alt)}" loading="lazy"><figcaption>${referenceOnly?'<strong>Imagen de referencia del linaje.</strong> ':''}${esc(m.caption)} <a href="${esc(m.page)}" target="_blank" rel="noopener">${esc(m.credit)} ↗</a> · <a href="${esc(m.licenseUrl)}" target="_blank" rel="noopener">${esc(m.license)}</a></figcaption></figure>`;
}
export function reviewedSiteContext(names:string[]){return knowledge.siteReviews.contexts.filter(c=>c.names.some(n=>names.includes(n)));}
