import { tx } from './i18n';
import{planetRecordFor,planetRecords,planetValue,planetReferenceLabel,planetSources,type PlanetField,type PlanetRecord}from'./planet';
import{deepSceneAt,deepIceAt,deepAge}from'./deep-earth';
import{phandaAt,videoScenarioAt,type EvidencePolicy}from'./earth-models';
import{escapeHtml as esc}from'./profiles';
export type PlanetTab='planet'|'sources';
const names:Partial<Record<PlanetField,string>>={meanTemperature:tx('planetCard.temperaturaMediaGlobal'),temperatureAnomaly:tx('planetCard.anomaliaDeTemperatura'),solarDay:tx('planetCard.diaSolar'),siderealRotation:tx('planetCard.rotacionSiderea'),oceanArea:tx('planetCard.superficieOceanica'),nitrogen:tx('planetCard.nitrogenoN'),oxygen:tx('planetCard.oxigenoO'),argon:tx('planetCard.argonAr'),carbonDioxide:tx('planetCard.dioxidoDeCarbonoCo'),waterVapor:tx('planetCard.vaporDeAgua'),methane:tx('planetCard.metanoCh'),ammonia:tx('planetCard.amoniacoNh'),hydrogen:tx('planetCard.hidrogenoH'),helium:tx('planetCard.helioHe'),rockVapor:tx('planetCard.vaporDeSilicatos'),otherGases:tx('planetCard.otrosGases')};
const gases:PlanetField[]=['rockVapor','nitrogen','oxygen','argon','carbonDioxide','waterVapor','methane','ammonia','hydrogen','helium','otherGases'];
const kind=(r:PlanetRecord)=>r.evidence==='illustrative-scenario'?tx('planetCard.escenarioAudiovisual'):r.evidence==='model'?tx('planetCard.reconstruccionPublicada'):r.evidence==='rounded-reference'?tx('planetCard.referenciaAproximada'):tx('planetCard.estimacionPublicada');
export function planetCard(year:number,tab:PlanetTab,policy:EvidencePolicy='reconstruction'){
 const get=(field:PlanetField)=>planetRecordFor(field,year,planetRecords,policy),scene=deepSceneAt(year),data=gases.map(f=>({field:f,record:get(f)})).filter(x=>x.record);
 const detail=(r:PlanetRecord)=>`<details><summary>${tx('planetCard.procedenciaYRango')}</summary><p>${esc(r.method)}</p><a href="${planetSources[r.sourceId].url}" target="_blank" rel="noopener">${esc(planetSources[r.sourceId].name)} ↗</a></details>`;
 const metric=(field:PlanetField)=>{const r=get(field);return r?`<article class="planet-metric" data-indicator="${field}" data-source="${r.sourceId}" data-reference-year="${r.reference.basis==='civil'?r.reference.year:''}"><span>${names[field]}</span><strong>${r.evidence==='illustrative-scenario'?'≈ ':''}${esc(planetValue(r))}</strong><small>${kind(r)} · ${esc(planetReferenceLabel(r.reference))}</small>${detail(r)}</article>`:''};
 if(tab==='sources'){
  const used=[...new Set([...Object.keys(names).map(f=>get(f as PlanetField)?.sourceId),...(scene?.sourceIds??[])].filter((id):id is string=>!!id))];
  return`<p>${tx('planetCard.referenciasUtilizadasEnEstaFecha')}</p>${used.map(id=>planetSources[id]?`<a class="planet-source" href="${planetSources[id].url}" target="_blank" rel="noopener">${esc(planetSources[id].name)} ↗</a>`:'').join('')}<p>${tx('planetCard.losIntervalosYPercentilesNo')}</p>`;
 }
 const old=!!videoScenarioAt(year),published=phandaAt(year);
 const controls=old?`<label class="planet-model-control" for="planet-evidence">${tx('planetCard.datosMostrados')}<select id="planet-evidence"><option value="reconstruction" ${policy==='reconstruction'?'selected':''}>${tx('planetCard.modelosPublicadosReferenciaDisponible')}</option><option value="video" ${policy==='video'?'selected':''}>${tx('planetCard.compararEscenarioDelVideo')}</option></select></label>`:'';
 const temp=get('meanTemperature')?'meanTemperature':get('temperatureAnomaly')?'temperatureAnomaly':undefined;
 const day=get('solarDay')?'solarDay':get('siderealRotation')?'siderealRotation':undefined;
 const numeric=`<div class="planet-metrics">${temp?metric(temp):''}${day?metric(day):''}${get('oceanArea')?metric('oceanArea'):''}</div>`;
 const atmosphere=data.length?`<h3>${tx('planetCard.composicionAtmosferica')}</h3><div class="atmosphere-bars">${data.map(({field,record})=>{const r=record!,n=typeof r.value==='number'?r.value:r.value?.max??0;return`<article data-indicator="${field}" data-source="${r.sourceId}"><div><span>${names[field]}</span><strong>${r.evidence==='illustrative-scenario'&&typeof r.value==='object'?'&lt;0,005 %':esc(planetValue(r))}</strong></div><meter min="0" max="100" value="${n}" aria-label="${names[field]}"></meter><small>${kind(r)}</small>${detail(r)}</article>`}).join('')}</div><p class="profile-note">${tx('planetCard.barrasEnPorcentajeSinReajustar')}</p>`:tx('planetCard.pClassProfileNoteNo');
 const context=scene?`<section class="deep-context" data-deep-context="${scene.id}"><h3>${esc(scene.title)}</h3><p>${esc(scene.life)}</p><p>${scene.mode==='magma'?tx('planetCard.superficieDominadaPorMaterialFundido'):scene.mode==='cooling'?tx('planetCard.enfriamientoYCortezaEnFormacion'):tx('planetCard.oceanosYMasasContinentalesModelo')}.</p>${deepIceAt(year)?`<p>${tx('planetCard.hielo')} ${esc(deepIceAt(year)!)} ${tx('planetCard.distribucionInterpretativaNoContornoMedido')}</p>`:''}<button data-encyclopedia-entry="${scene.article}">${tx('planetCard.explicacionCompleta')}</button></section>`:'';
 const optics=scene&&deepAge(year)>=2100&&deepAge(year)<=2600?tx('planetCard.buttonClassSecondaryButtonId'):'';
 return`${controls}${numeric}${!day&&old?tx('planetCard.pClassProfileNoteLa'):''}${published&&policy==='reconstruction'?tx('planetCard.pClassProfileNoteTemperatura'):''}${atmosphere}${context}${optics}`;
}
