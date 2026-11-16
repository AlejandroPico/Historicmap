import { tx, language } from './i18n';
import content from '../Tierra/Precambrico/enciclopedia.json' with {type:'json'};
import phanerozoic from '../Tierra/Fanerozoico/enciclopedia.json' with {type:'json'};
import quaternary from '../Tierra/Cuaternario/enciclopedia.json' with {type:'json'};
import review from '../Tierra/Precambrico/revision-video.json' with {type:'json'};
import phanerozoicReview from '../Tierra/Fanerozoico/revision-video.json' with {type:'json'};
import{deepSceneAt,deepSources}from'./deep-earth';
import{geologicalUnits,geologicalAt,humanUnits,humanAt,rankLabels,geologicalRangeLabel,humanChronologySources}from'./earth-chronology';
import{yearFromAge}from'./dates';
import{humanKnowledge,humanArticleForYear}from'./human-knowledge';
import lineages from'../public/data/human-lineages.json'with{type:'json'};
export interface EncyclopediaArticle{id:string;title:string;summary:string;sections:{title:string;text:string}[];sourceIds:string[];related:string[];diagram:string;year:number;videoStart?:number;kind?:string;themeId?:string}
export const curatedArticles=[...content.articles,...phanerozoic.articles,...quaternary.articles,...humanKnowledge.articles] as EncyclopediaArticle[];
const periodThemes:Record<string,string>={Cambrian:'cambrian',Ordovician:'ordovician',Silurian:'silurian',Devonian:'devonian',Carboniferous:'carboniferous',Permian:'permian',Triassic:'triassic',Jurassic:'jurassic',Cretaceous:'cretaceous',Paleogene:'paleogene',Neogene:'neogene',Quaternary:'quaternary'};
/** Artículos heredados agrupados por procedencia (para el índice lateral). */
export const curatedGroups:[string,EncyclopediaArticle[]][]=[[tx('encyclopediaModel.precambrico'),content.articles as EncyclopediaArticle[]],['Fanerozoico',phanerozoic.articles as EncyclopediaArticle[]],['Cuaternario',quaternary.articles as EncyclopediaArticle[]]];
export const reviewedEvents=[...new Map([...review.events,...phanerozoicReview.events,...humanKnowledge.videoReview.events].map(e=>[e.videoId,e])).values()];
export function encyclopediaArticle(id:string):EncyclopediaArticle|undefined{
 const authored=curatedArticles.find(a=>a.id===id);if(authored)return{...authored,kind:tx('encyclopediaModel.articuloTematico')};
 const event=reviewedEvents.find(e=>e.videoId===id);
 if(event){const context=curatedArticles.find(a=>a.id===event.article)!;return{id,title:event.name,summary:tx('encyclopediaModel.referenciaAudiovisualRevisada')+event.note,kind:tx('encyclopediaModel.revisionDelVideoSinEfecto'),year:context.year,diagram:'cycle',sourceIds:event.sourceIds,related:[event.article,'uncertainty'],videoStart:event.videoStart??undefined,sections:[{title:tx('encyclopediaModel.laObservacionDelVideo'),text:tx('encyclopediaModel.elRotuloSeObservoCuando',{v0:event.observedAgeMa.toLocaleString(language)})},{title:tx('encyclopediaModel.decisionDelAtlas'),text:event.note+tx('encyclopediaModel.disposicion')+event.disposition+tx('encyclopediaModel.inventarioConserva')},{title:tx('encyclopediaModel.dondeContinuar'),text:tx('encyclopediaModel.elArticuloRelacionadoExplicaEl')}]};}
 const unit=geologicalUnits.find(u=>'geo-'+u.id===id);
 if(unit){const themes:Record<string,string>={Precambrian:'formation',Hadean:'hadean',Archean:'archean',Eoarchean:'archean',Paleoarchean:'microbial',Mesoarchean:'archean',Neoarchean:'archean',Proterozoic:'proterozoic',Paleoproterozoic:'oxygenation',Mesoproterozoic:'proterozoic',Neoproterozoic:'rodinia',Siderian:'oxygenation',Rhyacian:'ice',Orosirian:'proterozoic',Statherian:'proterozoic',Calymmian:'proterozoic',Ectasian:'proterozoic',Stenian:'rodinia',Tonian:'rodinia',Cryogenian:'ice',Ediacaran:'ediacaran'};let parent=unit;while(parent.parent&&!periodThemes[parent.id]){const next=geologicalUnits.find(u=>u.id===parent.parent);if(!next)break;parent=next;}const theme=curatedArticles.find(a=>a.id===(themes[unit.id]??periodThemes[parent.id]));if(theme)return{...theme,id,year:Math.max(-4540000000,yearFromAge((unit.oldestMa+unit.youngestMa)*.5e6)),themeId:theme.id,title:unit.name,summary:geologicalRangeLabel(unit)+'. '+theme.summary,kind:rankLabels[unit.rank]+tx('encyclopediaModel.contenidoTematico'),sourceIds:[...new Set(['ics',...theme.sourceIds])],related:[...theme.related,...geologicalUnits.filter(u=>u.parent===unit.id).map(u=>'geo-'+u.id)]};}
 if(unit)return{id,title:unit.name,summary:tx('encyclopediaModel.deLaEscalaEstratigrafica',{v0:rankLabels[unit.rank],v1:geologicalRangeLabel(unit)}),year:Math.max(-4540000000,yearFromAge((unit.oldestMa+unit.youngestMa)*.5e6)),kind:tx('encyclopediaModel.fichaCronologica'),diagram:'chronology',sourceIds:['ics'],related:['geologic-ranks',unit.parent?'geo-'+unit.parent:'uncertainty',...geologicalUnits.filter(u=>u.parent===unit.id).map(u=>'geo-'+u.id)],sections:[{title:tx('encyclopediaModel.dondeSeSitua'),text:tx('encyclopediaModel.formaParteDeLosLimites',{name:unit.name,v1:geologicalUnits.find(u=>u.id===unit.parent)?.name??tx('encyclopediaModel.laEscalaGeologica'),v2:geologicalRangeLabel(unit)})},{title:tx('encyclopediaModel.tiempoRocasYLimites'),text:tx('encyclopediaModel.laEstratigrafiaRelacionaRegistrosDe')},{title:tx('encyclopediaModel.queOfreceEstaFicha'),text:tx('encyclopediaModel.estaEsUnaFichaDe')}]};
 const human=humanUnits.find(u=>'human-'+u.id===id);
 if(human)return{id,title:human.name,summary:human.scope,year:human.startYear,kind:tx('encyclopediaModel.referenciaHumanaRegional'),diagram:'chronology',sourceIds:[],related:['uncertainty'],sections:[{title:tx('encyclopediaModel.unaPeriodizacionSituada'),text:tx('encyclopediaModel.seConsultaParaEsUna',{name:human.name,scope:human.scope,precision:human.precision})},{title:tx('encyclopediaModel.comoSeRelacionaConEl'),text:tx('encyclopediaModel.culturasFormasPoliticasTerritoriosY')},{title:'Referencia',text:humanChronologySources[human.sourceId].title}]};
}
export function encyclopediaForYear(year:number){const scene=deepSceneAt(year);if(scene)return scene.article;const thematic=humanArticleForYear(year);if(thematic)return thematic;const human=humanAt(year).find(u=>u.lane==='overview');if(human)return'human-'+human.id;const units=geologicalAt(year);return'geo-'+(units.find(u=>u.rank==='period')??units.find(u=>u.rank==='era')??units.find(u=>u.rank==='eon'))!.id;}
export const encyclopediaIndex=(archive=false)=>[...curatedArticles.map(a=>({id:a.id,title:a.title,group:tx('encyclopediaModel.conceptosYProcesos')})),...geologicalUnits.map(u=>({id:'geo-'+u.id,title:u.name,group:rankLabels[u.rank]})),...humanUnits.map(u=>({id:'human-'+u.id,title:u.name,group:tx('encyclopediaModel.edadesHumanas')})),...(archive?reviewedEvents.map(e=>({id:e.videoId,title:e.name,group:tx('encyclopediaModel.archivoAudiovisual')})):[])];
export function searchEncyclopedia(query:string,archive=false){const norm=(s:string)=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const q=norm(query.trim());return encyclopediaIndex(archive).filter(a=>!q||norm(a.title+' '+a.group+' '+((lineages.taxa.find(t=>'hominin-'+t.key===a.id)as{aliases?:string[]}|undefined)?.aliases??[]).join(' ')).includes(q));}
/** Keep the consulted date when it belongs to the selected entry, not its editorial midpoint. */
export function encyclopediaReferenceYear(article:EncyclopediaArticle,consultedYear:number){
 if(!Number.isInteger(consultedYear)||consultedYear===0)return article.year;
 if(encyclopediaForYear(consultedYear)===article.id)return consultedYear;
 const unit=geologicalUnits.find(u=>'geo-'+u.id===article.id||article.id==='quaternary'&&u.id==='Quaternary');
 if(unit&&consultedYear>=unit.axisOldestYear&&(unit.axisEndYear===null||consultedYear<unit.axisEndYear))return consultedYear;
 const lineage=lineages.taxa.find(t=>'hominin-'+t.key===article.id);
 const age=consultedYear<0?1949-consultedYear:1950-consultedYear;
 if(lineage&&consultedYear<=-10001&&age>=lineage.youngestKa*1000&&age<=lineage.oldestKa*1000)return consultedYear;
 const human=humanUnits.find(u=>'human-'+u.id===article.id);
 if(human&&consultedYear>=human.startYear&&(human.endYear===null||consultedYear<human.endYear))return consultedYear;
 return article.year;
}
export const encyclopediaSources={...deepSources,...humanKnowledge.sources,...quaternary.sources};
