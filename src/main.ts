import{readableRulerLabels}from'./ruler-labels';
import{PREHISTORY_START,isPrehistoric,hasHumanEvidence,humanGroups,humanGroupCounts,humanLegend,cultureLabel}from'./prehistory';
import {prehistoricClimate} from './ice-history';
import{displayIceSampleFor as iceSampleFor,displayIceCaption as iceCaption,iceAvailabilityNote}from'./ice-synthesis';
import{iceEnabledFor,climateContext,type IceMode}from'./ice-automatic';
import{distributionsAt,coexistencePattern,distributionCoast,distributionCard,distributionLegend,lineageInventory}from'./human-distributions';
import{displayLabel}from'./map-presentation';
import{chronologyBands,chronologyBandsMarkup}from'./chronology-bands';
import{planetCard,type PlanetTab}from'./planet-card';
import type{EvidencePolicy}from'./earth-models';
import{deepSceneAt,deepIceAt,deepSources,deepBackground}from'./deep-earth';
import{drawDeepSurface}from'./deep-surface';
import{formatEventDate}from'./dates';
import * as maplibregl from 'maplibre-gl';
import { type GeoJSONSource, type ExpressionSpecification, type MapGeoJSONFeature } from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url';
import { createIcons, ArrowRight, BookOpen, ChevronDown, Database, Funnel, Globe2, Info, Layers, Map as MapIcon, MapPin, Maximize, Minimize, Mountain, Orbit, Pause, Play, Search, SkipBack, SkipForward, Sun, Sunset, Moon, Contrast, X } from 'lucide';
import 'maplibre-gl/dist/maplibre-gl.css';
import './style.css';
import './planet.css';
import './encyclopedia.css';
import { anchors, clamp, eraName, formatYear, positionToYear, PRESENT, snapshotFor, yearToPosition, playbackYear, navigationYear, type Snapshot } from './time';
import { places } from './catalog';
import type { FeatureCollection } from 'geojson';
import packageInfo from '../package.json';
import { aboutContent } from './about';
import {installNorthGesture} from './north-gesture';
import { annualData, asset, modernCities, overlaysFor } from './data';
import { datedPlaces } from './historical-places';
import {hasRegionalCoverage,regionalAssets,regionsAt,entitiesAt,regionalCard,regionalCoverage,type RegionalRecord} from './cultural-regions';
import { escapeHtml as esc, thematicData, thematicLegend, profileFor, type ProfileData, type Theme } from './profiles';
import { sourceDiff } from './source-diff';
import {withRenderIds,RENDER_ID} from './render-feature-id';
import { politicalData, nationalInfluenceHatching } from './political';
import {withGovernance,governmentTags,governmentCounts} from './governance';
import {conflictPointsFor} from './conflict-points';
import {controlledMap} from './control-loader';
import {occupationPattern} from './occupation-pattern';
import { countryCard } from './country-card';
import {anchorFor,matchingFeature,canonicalFeature,type CountryAnchor} from './selection';
import {emptyIndicators,type IndicatorData} from './country-workspace';
import {emptyHistory,type CountryHistory} from './country-history';
import {anchorId,comparisonShell,comparisonMarkup,type ComparisonState} from './country-comparison';
import { identityFor, type IdentityData } from './identities';
import { appearances,appearanceLabels,appearanceIcons,palettes,resolveAppearance,storedAppearance } from './appearance';
import {AFFILIATION_KINDS,AFFILIATIONS,affiliationLegend,affiliationGroups,affiliationSummary,affiliationsAvailable,type AffiliationKind} from './historical-affiliations';

const VERSION = packageInfo.version;
const icons = { ArrowRight, BookOpen, ChevronDown, Database, Funnel, Globe2, Info, Layers, Map:MapIcon, MapPin, Maximize, Minimize, Mountain, Orbit, Pause, Play, Search, SkipBack, SkipForward, Sun, Sunset, Moon, Contrast, X };
const $ = <T extends HTMLElement = HTMLElement>(selector: string) => document.querySelector<T>(selector)!;
const icon = (name: string) => `<i data-lucide="${name}" aria-hidden="true"></i>`;
function visibilityControls(scope:'layer'|'filter'){
  return `<button id="political-${scope}" data-visibility="political" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('map')}</span><span><strong>Cartografía política</strong><small id="${scope==='layer'?'territory-description':'political-filter-help'}">Países y fronteras</small></span><span class="layer-indicator"></span></button><button id="cultural-${scope}" data-visibility="cultural" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('globe-2')}</span><span><strong>Pueblos, culturas y yacimientos</strong><small id="${scope==='layer'?'cultural-help':'cultural-filter-help'}">Referencias documentadas; prioridad política</small></span><span class="layer-indicator"></span></button><button id="human-ranges-${scope}" data-visibility="human-ranges" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('globe-2')}</span><span><strong>Distribución humana</strong><small>Áreas estimadas y regiones compartidas</small></span><span class="layer-indicator"></span></button>`;
}
const organizationSections=[['Defensa y seguridad',['military','cooperation-security']],['Integración y comercio',['economic','trade','political-economic']],['Cooperación política y regional',['political','cooperation','infrastructure']]] as const;
const organizationOptions=organizationSections.map(([label,types])=>`<optgroup label="${label}">${AFFILIATION_KINDS.filter(kind=>(types as readonly string[]).includes(AFFILIATIONS[kind].type)).map(kind=>`<option value="${kind}" title="${esc(AFFILIATIONS[kind].description)}">${esc(AFFILIATIONS[kind].label)}</option>`).join('')}</optgroup>`).join('');
const app = $('#app');
app.innerHTML = `
  <main class="atlas">
    <div id="map" aria-label="Mapa interactivo de la Tierra"></div>
    <div id="concept" class="concept" hidden><span id="concept-caption"></span></div>
    <div class="map-shade"></div>
    <nav class="toolbar" aria-label="Herramientas del atlas">
      <button id="search-button" class="icon-button" title="Buscar un territorio" aria-label="Buscar un territorio" aria-controls="search-panel" aria-expanded="false">${icon('search')}</button>
      <button id="encyclopedia-button" class="icon-button" title="Enciclopedia" aria-label="Enciclopedia" aria-haspopup="dialog" aria-expanded="false">${icon('book-open')}</button>
      <button id="projection-button" class="icon-button" title="Ver mapa 2D" aria-label="Ver mapa 2D" data-view="globe">${icon('map')}</button>
      <button id="filters-button" class="icon-button" title="Filtros del atlas" aria-label="Filtros del atlas" aria-controls="filters-panel" aria-expanded="false">${icon('funnel')}</button>
      <button id="layers-button" class="icon-button" title="Capas del atlas" aria-label="Capas del atlas" aria-controls="layers-panel" aria-expanded="false">${icon('layers')}</button>
      <button id="planet-button" class="icon-button" title="Planeta y atmósfera" aria-label="Planeta y atmósfera" aria-controls="planet-panel" aria-expanded="false">${icon('orbit')}</button>
      <button id="sources-button" class="icon-button" title="Base de datos y fuentes" aria-label="Base de datos y fuentes" aria-controls="sources-panel" aria-expanded="false">${icon('database')}</button>
      <button id="fullscreen" class="icon-button" title="Pantalla completa" aria-label="Pantalla completa">${icon('maximize')}</button>
      <button id="appearance-button" class="icon-button" aria-label="Tema automático">${icon('contrast')}</button>
      <button id="about-button" class="icon-button" title="Acerca de Historicmap" aria-label="Acerca de Historicmap">${icon('info')}</button>
    </nav>
    <section id="search-panel" class="search-panel" role="dialog" aria-labelledby="search-title" hidden>
      <div class="popover-head"><h2 id="search-title">Buscar un territorio</h2><button id="close-search" class="icon-button" aria-label="Cerrar búsqueda">${icon('x')}</button></div>
      <div class="search-body"><label for="search-input">Nombre del territorio</label><input id="search-input" type="search" placeholder="País o territorio…" autocomplete="off" aria-controls="search-results"><p id="search-scope" class="profile-note"></p><div id="search-results" class="search-results"></div></div>
    </section>
    <section id="sources-panel" class="sources-panel" role="dialog" aria-labelledby="sources-title" hidden>
      <div class="popover-head"><h2 id="sources-title">Datos y fuentes</h2><button id="close-sources" class="icon-button" aria-label="Cerrar fuentes">${icon('x')}</button></div>
      <div class="source-summary"><div class="map-status"><span class="status-dot"></span><span id="map-status" role="status" aria-live="polite">Preparando cartografía…</span><button id="retry" hidden>Reintentar</button></div><p id="source-reference"></p><div id="source-links"></div><p id="source-scope"></p><a class="profile-source" href="https://github.com/AlejandroPico/Historicmap/blob/main/docs/SOURCES.md" target="_blank" rel="noopener">Catálogo, licencias y metodología ↗</a><details class="map-credits"><summary>${icon('info')} Créditos del mapa</summary><div id="map-attributions"></div></details></div>
    </section>
    <section id="filters-panel" class="filters-panel" role="dialog" aria-labelledby="filters-title" hidden>
      <div class="popover-head"><h2 id="filters-title">Filtros del atlas</h2><button id="close-filters" class="icon-button" aria-label="Cerrar filtros">${icon('x')}</button></div>
      <div class="layers">${visibilityControls('filter')}<div id="human-filter-block" hidden><label for="human-group-select">Evidencias y grupos humanos</label><select id="human-group-select"><option value="">Todos los grupos</option></select><small>Las atribuciones siguen las fuentes; los límites de las áreas son estimados.</small>${lineageInventory()}</div><label class="theme-control" for="government-select">Forma política y régimen<select id="government-select"><option value="">Todas las formas</option></select><div id="government-empty" class="active-filter-note" hidden></div><small id="government-help">Clasificaciones fechadas; las categorías no documentadas se indican.</small></label><label class="theme-control" for="theme-select">Color del mapa<select id="theme-select"><option value="political">Territorios y dependencias</option><option value="gdp">PIB total</option><option value="gdpPerCapita">PIB por habitante</option><option value="population">Población</option></select><small id="theme-help">Indicadores del Banco Mundial desde 1960.</small></label><label class="theme-control" for="affiliation-select">Alianzas y organizaciones<select id="affiliation-select"><option value="">Sin superposición</option>${organizationOptions}</select><small id="affiliation-help">Altas, bajas y categorías documentadas · 1880–2026.</small></label></div>
    </section>
    <section id="layers-panel" class="layers-panel" role="dialog" aria-labelledby="layers-title" hidden>
      <div class="popover-head"><h2 id="layers-title">Capas del atlas</h2><button id="close-layers" class="icon-button" aria-label="Cerrar capas">${icon('x')}</button></div>
      <div class="layers">${visibilityControls('layer')}<button id="chronology-layer" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('orbit')}</span><span><strong>Etapas del cronograma</strong><small>Mostrar eras, períodos y edades en la regla</small></span><span class="layer-indicator"></span></button><button id="chronology-colors" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('orbit')}</span><span><strong>Colores del cronograma</strong><small>Etapas geológicas y periodizaciones humanas</small></span><span class="layer-indicator"></span></button><button id="ice-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">❄</span><span><strong>Mantos de hielo</strong><small id="ice-help">Reconstrucción fechada · PaleoMIST 1.0</small></span><span class="layer-indicator"></span></button><label class="theme-control" for="ice-mode">Hielo<select id="ice-mode"><option value="auto">Automático según reconstrucción</option><option value="on">Mostrar modelo disponible</option><option value="off">Ocultar hielo</option></select></label><button id="ice-uncertainty" class="layer-button" aria-pressed="false" hidden><span class="layer-icon">❄</span><span><strong>Incertidumbre del hielo</strong><small>Contornos mínimo y máximo de la hipótesis publicada</small></span><span class="layer-indicator"></span></button><button id="physical-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('mountain')}</span><span><strong>Relieve de referencia</strong><small>Topografía contemporánea · desde 10.000 a. C.</small></span><span class="layer-indicator"></span></button><button id="places-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('map-pin')}</span><span><strong>Capitales, ciudades y yacimientos</strong><small id="places-help">Capitales, cortes y sedes fechadas</small></span><span class="layer-indicator"></span></button><button id="occupations-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('layers')}</span><span><strong>Ocupaciones y disputas</strong><small id="occupations-help">Franjas y puntos de conflictos documentados</small></span><span class="layer-indicator"></span></button></div>
    </section>
    <div id="selection" class="selection-card" hidden><button id="close-selection" class="icon-button" aria-label="Cerrar selección">${icon('x')}</button><span class="eyebrow" id="selection-date">EN EL MAPA</span><h2 id="selection-title"></h2><button id="selection-encyclopedia" class="encyclopedia-entity-link" hidden>${icon('book-open')}<span>Historia y dirigentes en la enciclopedia</span></button><p id="selection-status" role="status" hidden></p><div id="selection-alternatives" hidden></div><div id="selection-text"></div></div>
    <section id="planet-panel" class="planet-panel" role="dialog" aria-labelledby="planet-title" hidden>
      <div class="planet-heading"><div><span class="eyebrow">EL PLANETA EN EL TIEMPO</span><h2 id="planet-title">Tierra</h2><span id="planet-date"></span></div><button id="close-planet" class="icon-button" aria-label="Cerrar planeta">${icon('x')}</button></div>
      <div class="planet-tabs" role="tablist" aria-label="Información planetaria"><button id="planet-tab-planet" role="tab" aria-controls="planet-content" aria-selected="true" data-planet-tab="planet">Planeta</button><button id="planet-tab-sources" role="tab" aria-controls="planet-content" aria-selected="false" tabindex="-1" data-planet-tab="sources">Fuentes</button></div>
      <div id="planet-content" class="planet-content" role="tabpanel" aria-labelledby="planet-tab-planet" tabindex="0"></div>
    </section>
    <aside id="map-legend" class="map-legend" aria-label="Leyenda del mapa" hidden></aside>
    <section class="time-dock" aria-label="Navegación temporal">
      <div id="ruler" class="ruler" role="slider" tabindex="0" aria-label="Fecha del atlas. Arrastra para desplazarte; rueda o teclas más y menos para cambiar la escala" aria-valuemin="0" aria-valuemax="1900"><div id="chronology-bands" class="chronology-bands" role="group" aria-label="Etapas del cronograma"></div><div id="ruler-track"></div><div class="fixed-cursor"><div class="cursor-line"></div></div><div class="ruler-fade left"></div><div class="ruler-fade right"></div></div>
      <div class="time-focus"><button id="date-button" class="date-heading" title="Ir a una fecha"><span id="year"></span>${icon('chevron-down')}</button><div class="playback"><button id="previous" class="icon-button" aria-label="Época anterior">${icon('skip-back')}</button><button id="play" class="play-button" aria-label="Reproducir recorrido" aria-pressed="false" aria-busy="true">${icon('play')}</button><button id="next" class="icon-button" aria-label="Época siguiente">${icon('skip-forward')}</button><span id="playback-status" class="playback-status" role="status" aria-live="polite" aria-atomic="true"></span></div></div>
    </section>
    <dialog id="modal" aria-labelledby="modal-label"><div class="modal-head"><span id="modal-label" class="eyebrow"></span><button id="close-modal" class="icon-button" aria-label="Cerrar ventana">${icon('x')}</button></div><div id="modal-body"></div></dialog>
    <div id="toast" role="status" hidden></div>
  </main>`;
createIcons({icons});

let year = PRESENT;
let projection: 'globe' | 'mercator' = 'globe';
let spacing = 230;
let position = yearToPosition(year);
let political = true, physical = false, showPlaces = false, showOccupations = false, showRegional = true, showHumanRanges = true;
let humanFilter='';
let iceMode:IceMode='auto';
let showIceUncertainty=false;
let activePlanetTab:PlanetTab='planet';
let chronologyColored=true,chronologyVisible=true;
let planetPolicy:EvidencePolicy='reconstruction',earthOptics:'standard'|'ferruginous'='standard';
try{chronologyVisible=localStorage.getItem('historicmap-chronology-visible')!=='off';}catch{}
try{chronologyColored=localStorage.getItem('historicmap-chronology-colors')!=='off';}catch{}
function updateChronologyColors(){
 $('.time-dock').dataset.chronologyColors=String(chronologyColored);
 $('#chronology-colors').setAttribute('aria-pressed',String(chronologyColored));
 $('#chronology-colors').classList.toggle('active',chronologyColored);
}
updateChronologyColors();
function renderPlanet(){
 $('#planet-date').textContent=formatYear(year);
 $('#planet-panel').dataset.year=String(year);
 if($('#planet-panel').hidden)return;
 const pane=$('#planet-content'),scroll=pane.scrollTop;
 const open=[...pane.querySelectorAll<HTMLDetailsElement>('details[open]')].map(d=>d.closest<HTMLElement>('[data-indicator],[data-geological-unit]')?.dataset.indicator??d.closest<HTMLElement>('[data-geological-unit]')?.dataset.geologicalUnit).filter(Boolean);
 pane.innerHTML=planetCard(year,activePlanetTab,planetPolicy);
 const optics=pane.querySelector('#earth-optics');if(optics){optics.setAttribute('aria-pressed',String(earthOptics==='ferruginous'));optics.textContent=earthOptics==='standard'?'Comparar variante rojiza del agua':'Volver al aspecto de referencia';}
 pane.querySelectorAll<HTMLDetailsElement>('details').forEach(d=>{const holder=d.closest<HTMLElement>('[data-indicator],[data-geological-unit]');if(holder&&open.includes(holder.dataset.indicator??holder.dataset.geologicalUnit))d.open=true;});pane.scrollTop=scroll;
}
function closePlanet(focus=false){$('#planet-panel').hidden=true;$('#planet-button').setAttribute('aria-expanded','false');if(focus)$('#planet-button').focus();}
function selectPlanetTab(tab:PlanetTab,focus=false){
 activePlanetTab=tab;
 document.querySelectorAll<HTMLButtonElement>('[data-planet-tab]').forEach(b=>{const selected=b.dataset.planetTab===tab;b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1;if(selected&&focus)b.focus();});
 $('#planet-content').setAttribute('aria-labelledby','planet-tab-'+tab);$('#planet-content').scrollTop=0;renderPlanet();
}
let distributionData:FeatureCollection={type:'FeatureCollection',features:[]},sharedData:FeatureCollection={type:'FeatureCollection',features:[]};
let sharedSignature='',distributionSignature='',referenceLandKey='',highlightedDistributionId:string|number|undefined;
let theme:Theme='political';
let affiliation:AffiliationKind|''='';
let appearance=storedAppearance();
let ready = false, activeKey = '', requestNumber = 0;
let desiredKey='', refreshPromise:Promise<void>=Promise.resolve(), renderQueue:Promise<void>=Promise.resolve();
let profiles:ProfileData={retrieved:'',countries:{}};
let cityData:FeatureCollection={type:'FeatureCollection',features:[]}, overlayData:FeatureCollection={type:'FeatureCollection',features:[]};
let territorySignature='', citySignature='',regionalSignature='';
let regionalData:FeatureCollection={type:'FeatureCollection',features:[]};
let selectionLocation:number[]|undefined,selectionAlternatives:FeatureCollection['features']=[];
let highlightedRegionalId:string|number|undefined;
let referenceLandOn=false;
let conflictData:FeatureCollection={type:'FeatureCollection',features:[]},conflictSignature='';
let governmentFilter='',governmentOptionsSignature='';
let committedData:FeatureCollection={type:'FeatureCollection',features:[]}, committedDomain='', overlaySignature='';
let loaded: FeatureCollection = { type:'FeatureCollection', features:[] };
const empty: FeatureCollection = { type:'FeatureCollection', features:[] };
let snapshot: Snapshot = snapshotFor(year);
let playing=false, playGeneration=0;
let identityData:IdentityData;
let indicatorData:IndicatorData=emptyIndicators,countryHistory:CountryHistory=emptyHistory;
let selectedAnchor:CountryAnchor|undefined,activeCountryTab='authorities',selectionGeneration=0;
let timelineFilter='all',timelineFuture=false,timelineExpanded=false;
const trendSelections:Record<string,string>={};
const comparison:ComparisonState={mode:'dates',a:Math.max(PREHISTORY_START,year-10)||-1,b:Math.max(PREHISTORY_START,year)||-1,metric:'population',pinned:[]};
let refreshSearch=()=>{};
function visiblePoliticalData():FeatureCollection{return {...loaded,features:(!political&&snapshot.kind!=='geological')?[]:loaded.features.filter(f=>!governmentFilter||(f.properties?.governmentTags??[]).includes(governmentFilter))};}
const colorExpression: ExpressionSpecification = ['coalesce',['get','politicalColor'],'#829c90'];
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
maplibregl.setWorkerUrl(workerUrl);
const glyphsUrl=new URL('fonts/',new URL(import.meta.env.BASE_URL,document.baseURI)).href+'{fontstack}/{range}.pbf';
const map = new maplibregl.Map({container:'map', center:[23,22], zoom:1.65, minZoom:0.2, maxZoom:7, attributionControl:false, renderWorldCopies:false, style:{version:8, glyphs:glyphsUrl, sources:{}, layers:[{id:'ocean',type:'background',paint:{'background-color':palettes[resolveAppearance(appearance)].ocean}}]}, canvasContextAttributes:{antialias:true}, fadeDuration:reduced?0:200});
const removeNorthGesture=installNorthGesture(map.getCanvas(),()=>map.resetNorth({duration:reduced?0:350}));
map.once('remove',removeNorthGesture);
const recordCamera=()=>{$('#map').dataset.camera=JSON.stringify({center:map.getCenter().toArray(),zoom:map.getZoom(),bearing:map.getBearing(),pitch:map.getPitch()});};
map.on('moveend',recordCamera);recordCamera();
map.addControl(new maplibregl.ScaleControl({maxWidth:100,unit:'metric'}),'bottom-left');
function applyAppearance(){
  const resolved=resolveAppearance(appearance),palette=palettes[resolved];
  document.documentElement.dataset.appearance=resolved;document.documentElement.dataset.appearanceMode=appearance;
  document.documentElement.style.setProperty('--background',palette.background);
  const next=appearances[(appearances.indexOf(appearance)+1)%appearances.length];
  const label=`Tema: ${appearanceLabels[appearance]}. Cambiar a ${appearanceLabels[next]}`;
  $('#appearance-button').innerHTML=icon(appearanceIcons[appearance]);$('#appearance-button').setAttribute('aria-label',label);$('#appearance-button').title=label;
  if(ready){map.setPaintProperty('ocean','background-color',deepBackground(year,iceMode!=='off')??palette.ocean);map.setSky({'sky-color':palette.background,'horizon-color':palette.horizon,'fog-color':palette.background,'sky-horizon-blend':0.6,'horizon-fog-blend':0.6,'fog-ground-blend':0.2});}
  createIcons({icons});
}
$('#appearance-button').onclick=()=>{appearance=appearances[(appearances.indexOf(appearance)+1)%appearances.length];try{localStorage.setItem('historicmap-appearance',appearance);}catch{}applyAppearance();};
applyAppearance();setInterval(()=>{if(appearance==='auto')applyAppearance();},60000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&appearance==='auto')applyAppearance();});
const deepCanvas=document.createElement('canvas');deepCanvas.width=1024;deepCanvas.height=1024;
let deepSurfaceKey='';
function paintDeepSurface(targetYear:number,coast?:FeatureCollection){
 const scene=deepSceneAt(targetYear);map.setPaintProperty('ocean','background-color',deepBackground(targetYear,iceMode!=='off')??palettes[resolveAppearance(appearance)].ocean);map.setLayoutProperty('deep-surface','visibility',scene?'visible':'none');
 $('.atlas').classList.toggle('deep-time',!!scene);$('#map').dataset.deepScene=scene?.id??'';
 if(!scene){deepSurfaceKey='';$('#map').dataset.deepIce='';$('#map').dataset.deepIceVisible='false';$('#map').dataset.deepGeometry='';return;}
 const key=scene.id+':'+deepIceAt(targetYear)+':'+iceMode+':'+earthOptics+':'+(coast?.features.length?activeKey:'illustrative');
 if(key!==deepSurfaceKey){drawDeepSurface(deepCanvas,scene,targetYear,coast,iceMode!=='off',earthOptics);deepSurfaceKey=key;$('#map').dataset.deepCoastReference=coast?.features.length?activeKey:'illustrative';const source=map.getSource('deep-surface')as maplibregl.CanvasSource;source.play();map.once('render',()=>source.pause());}
 $('#map').dataset.earthOptics=earthOptics;
 $('#map').dataset.deepGeometry=coast?.features.length?'dated-model':'illustrative';$('#map').dataset.deepIce=deepIceAt(targetYear)??'';$('#map').dataset.deepIceVisible=String(!!deepIceAt(targetYear)&&iceMode!=='off');
}
function showEncyclopedia(entry?:string){stopPlay();const at=year;void import('./encyclopedia').then(m=>m.openEncyclopedia(at,y=>{void updateYear(y)},entry)).catch(()=>status('No se pudo abrir la enciclopedia. Vuelve a intentarlo.',true));}
$('#encyclopedia-button').onclick=()=>showEncyclopedia();
app.addEventListener('click',event=>{const link=(event.target as Element).closest<HTMLElement>('[data-encyclopedia-entry]');if(link&&link.tagName==='A')event.preventDefault();if(link&&!(link.classList.contains('chronology-band')&&event.detail>0))showEncyclopedia(link.dataset.encyclopediaEntry)});
map.on('load', () => {
  map.setProjection({type:projection});
  map.setSky({'sky-color':'#182c32','horizon-color':'#8fa9a3','fog-color':'#101e22','sky-horizon-blend':0.6,'horizon-fog-blend':0.6,'fog-ground-blend':0.2});
  map.addSource('deep-surface',{type:'canvas',canvas:deepCanvas,animate:false,coordinates:[[-180,85.051129],[180,85.051129],[180,-85.051129],[-180,-85.051129]]});
  map.addLayer({id:'deep-surface',type:'raster',source:'deep-surface',layout:{visibility:'none'},paint:{'raster-fade-duration':0}});
  map.addSource('reference-land',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7});
  map.addLayer({id:'reference-land',type:'fill',source:'reference-land',paint:{'fill-color':'#6c7776','fill-opacity':1}});
  map.addSource('cultural-regions',{type:'geojson',data:empty,promoteId:RENDER_ID,tolerance:0.2,maxzoom:7,attribution:'<a href="https://github.com/aourednik/historical-basemaps">Regiones culturales · A. Ourednik · GPL-3.0</a>'});
  map.addLayer({id:'cultural-fill',type:'fill',source:'cultural-regions',filter:['==',['get','kind'],'cultural-region'],paint:{'fill-color':['get','color'],'fill-opacity':1}});
  map.addLayer({id:'regional-polity-fill',type:'fill',source:'cultural-regions',filter:['==',['get','kind'],'polity-reference'],paint:{'fill-color':['get','color'],'fill-opacity':1}});
  map.addLayer({id:'cultural-line',type:'line',source:'cultural-regions',paint:{'line-color':'#536254','line-width':0.6,'line-opacity':0.65,'line-dasharray':[2,3]}});
  map.addSource('human-ranges',{type:'geojson',data:empty,promoteId:RENDER_ID,tolerance:0.2,maxzoom:7,attribution:'<a href="https://github.com/AlejandroPico/Historicmap/tree/main/Tierra/Humanidad">Distribución humana · síntesis regional con fuentes</a>'});
  map.addSource('human-shared',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7});
  map.addLayer({id:'human-range-fill',type:'fill',source:'human-ranges',paint:{'fill-color':['get','color'],'fill-opacity':0.86}});
  map.addLayer({id:'human-range-shared',type:'fill',source:'human-shared',paint:{'fill-pattern':['get','patternKey'],'fill-opacity':1}});
  map.addLayer({id:'human-range-line',type:'line',source:'human-ranges',paint:{'line-color':'#334744','line-width':0.7,'line-opacity':0.7,'line-dasharray':[3,2]}});
  map.addLayer({id:'human-range-selected',type:'line',source:'human-ranges',paint:{'line-color':'#fff0bf','line-width':2,'line-opacity':['case',['boolean',['feature-state','selected'],false],1,0]}});
  map.addLayer({id:'human-range-labels',type:'symbol',source:'human-ranges',minzoom:1.8,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':12,'text-padding':14,'text-max-width':12},paint:{'text-color':'#fff4d5','text-halo-color':'#273d3d','text-halo-width':1.2}});
  // Subpixel render tolerance avoids overflowing GPU segments on dense coastlines.
  // The full-resolution source coordinates remain unchanged in public/data.
  map.addSource('territories',{type:'geojson',data:empty,promoteId:RENDER_ID,tolerance:0.2,maxzoom:7,attribution:'<a href="https://www.naturalearthdata.com/">Natural Earth</a> · <a href="https://icr.ethz.ch/data/cshapes/">CShapes · CC BY-NC-SA 4.0</a> · <a href="https://github.com/aourednik/historical-basemaps">A. Ourednik · GPL-3.0</a> · <a href="https://doi.org/10.1016/j.gsf.2024.101922">Cao et al. 2024 · CC BY 4.0</a>'});
  map.addLayer({id:'territory-fill',type:'fill',source:'territories',paint:{'fill-color':colorExpression,'fill-opacity':0.88}});
  map.addSource('dem',{type:'raster-dem',tiles:['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],tileSize:256,maxzoom:12,encoding:'terrarium',attribution:'Relieve: © Mapzen / AWS Open Data'});
  map.addLayer({id:'relief',type:'hillshade',source:'dem',layout:{visibility:'none'},paint:{'hillshade-shadow-color':'#102c2b','hillshade-highlight-color':'#fff3c8','hillshade-exaggeration':0.6}});
  map.addSource('ice-margins',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7,attribution:'<a href="https://doi.pangaea.de/10.1594/PANGAEA.905800">Gowan et al. · PaleoMIST</a> · <a href="https://doi.org/10.1038/s41467-019-11601-2">Batchelor et al.2019 · hipótesis de hielo boreal</a>'});
  const bestIce:any=['==',['coalesce',['get','variant'],'best'],'best'];
  map.addLayer({id:'ice-fill',type:'fill',source:'ice-margins',filter:bestIce,layout:{visibility:'none'},paint:{'fill-color':'#d9f0f2','fill-opacity':1}});
  map.addLayer({id:'ice-line',type:'line',source:'ice-margins',filter:bestIce,layout:{visibility:'none'},paint:{'line-color':'#84b8c7','line-width':0.8}});
  for(const variant of['minimum','maximum'])map.addLayer({id:'ice-'+variant,type:'line',source:'ice-margins',filter:['==',['get','variant'],variant],layout:{visibility:'none'},paint:{'line-color':variant==='minimum'?'#5198bb':'#e8faff','line-width':1.3,'line-dasharray':variant==='minimum'?[2,2]:[5,3]}});
  map.addLayer({id:'territory-line',type:'line',source:'territories',paint:{'line-color':'#182b2b','line-width':['interpolate',['linear'],['zoom'],0,0.35,5,1.2],'line-opacity':0.85}});
  map.addLayer({id:'territory-selected',type:'line',source:'territories',paint:{'line-color':'#f6d99c','line-width':2,'line-opacity':['case',['boolean',['feature-state','selected'],false],1,0]}});
  map.addSource('occupations',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7,attribution:'<a href="https://github.com/Seshat-Global-History-Databank/cliopatria">Cliopatria · CC BY 4.0</a> · <a href="https://commons.wikimedia.org/wiki/File:GCE-Frente_en_oct_1937.svg">Tyk / Té y kriptonita · CC BY-SA 3.0</a>'});
  map.addLayer({id:'occupation-fill',type:'fill',source:'occupations',paint:{'fill-pattern':['get','patternKey'],'fill-opacity':1}});
  map.addLayer({id:'occupation-line',type:'line',source:'occupations',paint:{'line-color':'#c6c8ba','line-width':0.85,'line-opacity':0.75}});
  map.addLayer({id:'territory-labels',type:'symbol',source:'territories',minzoom:2.5,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':['interpolate',['linear'],['zoom'],2,10,5,13],'text-max-width':7,'text-padding':12},paint:{'text-color':'#e5e5ce','text-halo-color':'#24413c','text-halo-width':1}});
  map.addLayer({id:'cultural-selected',type:'line',source:'cultural-regions',paint:{'line-color':'#f6d99c','line-width':2,'line-dasharray':[3,2],'line-opacity':['case',['boolean',['feature-state','selected'],false],1,0]}});
  map.addLayer({id:'cultural-labels',type:'symbol',source:'cultural-regions',minzoom:2.2,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':['interpolate',['linear'],['zoom'],2,9,5,11],'text-max-width':11,'text-padding':12},paint:{'text-color':'#e9e3c9','text-halo-color':'#435048','text-halo-width':1}},'territory-labels');
  map.addLayer({id:'human-evidence-circles',type:'circle',source:'cultural-regions',filter:['==',['geometry-type'],'Point'],paint:{'circle-radius':['interpolate',['linear'],['zoom'],0,4,5,7],'circle-color':['match',['get','taxonGroup'],humanGroups[0].id,humanGroups[0].color,...humanGroups.slice(1).flatMap(g=>[g.id,g.color]),'#a9b3ad'] as ExpressionSpecification,'circle-stroke-color':'#152b30','circle-stroke-width':1.3}});
  map.addLayer({id:'human-evidence-labels',type:'symbol',source:'cultural-regions',minzoom:3.5,filter:['==',['geometry-type'],'Point'],layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':11,'text-offset':[0,1.1],'text-padding':9},paint:{'text-color':'#fff1cf','text-halo-color':'#102329','text-halo-width':1.5}});
  map.addSource('places',{type:'geojson',data:empty});
  map.addLayer({id:'place-circles',type:'circle',source:'places',minzoom:0,paint:{'circle-radius':['case',['==',['get','capital'],true],4,2.5],'circle-color':'#f2d394','circle-stroke-color':'#152b30','circle-stroke-width':1.5}});
  map.addLayer({id:'place-labels',type:'symbol',source:'places',minzoom:1,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':11,'text-offset':[0,1.1],'symbol-sort-key':['coalesce',['get','rank'],5],'text-padding':8},paint:{'text-color':'#fff1cf','text-halo-color':'#102329','text-halo-width':1.5}});
  map.addSource('conflict-points',{type:'geojson',data:empty});
  map.addLayer({id:'conflict-circles',type:'circle',source:'conflict-points',paint:{'circle-radius':['case',['==',['get','kind'],'battle'],4.5,6],'circle-color':['case',['==',['get','kind'],'battle'],'#e39675','#bda1e5'],'circle-stroke-color':'#172932','circle-stroke-width':1.7}});
  map.addLayer({id:'conflict-labels',type:'symbol',source:'conflict-points',minzoom:2,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':11,'text-offset':[0,1.15],'text-max-width':17},paint:{'text-color':'#ffe3ce','text-halo-color':'#182b31','text-halo-width':1.6}});
  ready = true; applyAppearance();void refreshMap(true);
});
map.on('error',(event) => {
  if (event.error?.message?.includes('WebGL')) toast('El navegador no ha podido iniciar WebGL. Prueba con aceleración gráfica activada.');
  else if (physical) toast('No se ha podido cargar parte del relieve en línea. La cartografía local sigue disponible.');
});
map.on('webglcontextlost',()=>toast('Se ha perdido la conexión gráfica. Recarga la página para recuperar el mapa.'));
map.on('idle',()=>{
  $('#map').dataset.cameraReady='true';
  $('#map').dataset.visibilityRendered=`${political}:${showRegional}`;
  $('#map').dataset.humanEvidence=String(regionalData.features.filter(f=>f.properties?.evidenceRecords).length);
  $('#map').dataset.humanEvidenceRendered=String(map.queryRenderedFeatures({layers:['human-evidence-circles']}).length);
  if($('#map').getAttribute('aria-busy')==='true')return;
  // An ocean or a region without a sovereign polygon is still a loaded view.
  if((loaded.features.length||regionalData.features.length||isPrehistoric(year)||deepSceneAt(year))&&$('#map').dataset.loadedYear===String(year)&&map.isSourceLoaded('territories')&&(!hasRegionalCoverage(year)||map.isSourceLoaded('cultural-regions'))) $('#map').dataset.rendered=activeKey;
  // Keep the indicator through tile replacement, not only the JSON download.
  if($('#map').dataset.loadedYear===String(year))setPlaybackLoading(false,year);
  const visibleHatching=showOccupations?map.queryRenderedFeatures({layers:['occupation-fill']}):[];
  $('#map').dataset.hatchingRendered=String(visibleHatching.length);
  $('#map').dataset.nationalHatchingRendered=String(visibleHatching.filter(f=>f.properties?.referenceScope==='national-reference').length);
  $('#map').dataset.placesRendered=String(showPlaces?map.queryRenderedFeatures({layers:['place-circles']}).length:0);
  $('#map').dataset.conflictsRendered=String(showOccupations?map.queryRenderedFeatures({layers:['conflict-circles']}).length:0);
});
map.on('movestart',()=>{$('#map').dataset.cameraReady='false';});
map.on('click',event=>{
  if(!ready||$('#map').getAttribute('aria-busy')==='true'||$('#map').dataset.loadedYear!==String(year)||$('#map').dataset.rendered!==activeKey)return;
  const conflict=showOccupations?map.queryRenderedFeatures(event.point,{layers:['conflict-circles']})[0]:undefined;
  const human=showRegional&&hasHumanEvidence(year)?map.queryRenderedFeatures(event.point,{layers:['human-evidence-circles']})[0]:undefined;
  const humanFeature=canonicalFeature(human,regionalData);if(humanFeature){selectFeature(humanFeature,event.lngLat.toArray());return;}
  const place=showPlaces?map.queryRenderedFeatures(event.point,{layers:['place-circles']})[0]:undefined;
  const feature=conflict?canonicalFeature(conflict,conflictData):place?canonicalFeature(place,cityData):canonicalFeature(political||snapshot.kind==='geological'?map.queryRenderedFeatures(event.point,{layers:['territory-fill']})[0]:undefined,loaded);
  const alternatives=entitiesAt([event.lngLat.lng,event.lngLat.lat],visiblePoliticalData(),visibleRegions());
  if(feature||alternatives.length)selectFeature(feature??alternatives[0],[event.lngLat.lng,event.lngLat.lat]);
});
map.on('mouseenter','human-range-fill',()=>{map.getCanvas().style.cursor='pointer';});
map.on('mouseleave','human-range-fill',()=>{map.getCanvas().style.cursor='';});
map.on('mouseenter','territory-fill',()=>{map.getCanvas().style.cursor='pointer';});
map.on('mouseleave','territory-fill',()=>{map.getCanvas().style.cursor='';});
function selectFeature(feature:{properties:MapGeoJSONFeature['properties']|null;id?:string|number},location?:number[]) {
  if($('#map').getAttribute('aria-busy')==='true'||$('#map').dataset.loadedYear!==String(year))return;
  stopPlay();
  const next=anchorFor(feature.properties??{},year,identityData);
  if(!selectedAnchor||anchorId(next)!==anchorId(selectedAnchor)){activeCountryTab='authorities';const content=document.querySelector('.country-content');if(content)content.scrollTop=0;timelineExpanded=false;comparison.a=Math.max(PREHISTORY_START,year-10)||-1;comparison.b=Math.max(PREHISTORY_START,year)||-1;}
  selectionLocation=location??feature.properties?.focus;selectedAnchor=next;renderSelection();
}
let highlightedId:string|number|undefined;
function highlightFeature(id?:string|number){
  if(!ready||id===highlightedId)return;
  // A filter change reparses source tiles. During an incremental date update
  // that can pair a new feature index with an older tile payload. Selection is
  // paint state only: it must not trigger another geometry/layout update.
  if(highlightedId!==undefined)map.removeFeatureState({source:'territories',id:highlightedId},'selected');
  highlightedId=id;
  if(id!==undefined)map.setFeatureState({source:'territories',id},{selected:true});
}
function highlightDistribution(id?:string|number){if(highlightedDistributionId!==undefined)map.removeFeatureState({source:'human-ranges',id:highlightedDistributionId},'selected');highlightedDistributionId=id;if(id!==undefined)map.setFeatureState({source:'human-ranges',id},{selected:true});}
function visibleRegions():FeatureCollection{return{type:'FeatureCollection',features:[...(showRegional?regionalData.features:[]),...(showRegional&&showHumanRanges?distributionData.features.filter(f=>!humanFilter||f.properties?.group===humanFilter):[])]};}
function closeSelection(){selectedAnchor=undefined;selectionLocation=undefined;selectionGeneration++;$('#selection').hidden=true;highlightFeature();highlightRegion();highlightDistribution();}
function highlightRegion(id?:string|number){if(highlightedRegionalId!==undefined)map.removeFeatureState({source:'cultural-regions',id:highlightedRegionalId},'selected');highlightedRegionalId=id;if(id!==undefined)map.setFeatureState({source:'cultural-regions',id},{selected:true});}
function renderAlternatives(){selectionAlternatives=selectionLocation?entitiesAt(selectionLocation,visiblePoliticalData(),visibleRegions()):[];const panel=$('#selection-alternatives');panel.hidden=selectionAlternatives.length<2;panel.innerHTML=panel.hidden?'':`<span>En este lugar</span><div>${selectionAlternatives.map((f,i)=>`<button class="text-action" data-overlap-entity="${i}" aria-pressed="${selectedAnchor?.properties.contextKey?f.properties?.contextKey===selectedAnchor.properties.contextKey:!f.properties?.contextKey&&(f.properties?.identityKey??f.properties?.entityCode??f.properties?.name)===(selectedAnchor?.key||selectedAnchor?.name)}">${esc(String(f.properties?.name))}<small>${f.properties?.kind==='archaeological-reference'?'Yacimiento o evidencia':f.properties?.contextKey?(f.properties.kind==='human-range'?'Distribución humana':f.properties.kind==='polity-reference'?'Referencia política':'Región cultural'):'Entidad política'}</small></button>`).join('')}</div>`;}
$('#selection-alternatives').onclick=e=>{const b=(e.target as Element).closest<HTMLElement>('[data-overlap-entity]');if(b){const f=selectionAlternatives[Number(b.dataset.overlapEntity)];if(f)selectFeature(f,selectionLocation);}};
function renderSelection(){
  if(!selectedAnchor||!identityData||$('#map').getAttribute('aria-busy')==='true')return;
  const top=document.querySelector('.country-content')?.scrollTop??0;
  selectionGeneration++;
  const feature=matchingFeature(selectedAnchor,selectedAnchor.place?{type:'FeatureCollection',features:[...cityData.features,...conflictData.features]}:selectedAnchor.uid?overlayData:{type:'FeatureCollection',features:[...loaded.features,...regionalData.features,...distributionData.features,...cityData.features.filter(f=>f.properties?.sovereignSeat)]},year,identityData);
  const p=feature?.properties??selectedAnchor.properties;
  $('#selection').hidden=false;$('#selection').setAttribute('aria-busy','false');$('#selection-status').hidden=true;
  $('#selection-title').textContent=displayLabel(feature?(p.contextKey?p.name:identityFor(p,year,identityData).name??p.name??'Área del mapa'):selectedAnchor.name||'Área del mapa');
  {const identityKey=feature&&!p.contextKey?identityFor(p,year,identityData).key:undefined,link=$<HTMLButtonElement>('#selection-encyclopedia');if(identityKey&&identityData.countries[identityKey]?.leaders?.length){link.hidden=false;link.dataset.encyclopediaEntry='entidad-'+identityKey.replace(/[^A-Za-z0-9-]/g,'-')}else{link.hidden=true;delete link.dataset.encyclopediaEntry}}
  $('#selection-date').textContent=`${formatYear(year)} · ${feature?(p.referenceKind==='archaeological-site'?'YACIMIENTO Y CONTEXTO ARQUEOLÓGICO':'FICHA DEL TERRITORIO'):'ENTIDAD SIN REPRESENTACIÓN ACTIVA'}`;
  $('#selection').dataset.entity=selectedAnchor.key||selectedAnchor.originalName;
  $('#selection').dataset.year=String(year);
  if(selectedAnchor.place&&p.conflictId){
    $('#selection-date').textContent=`${formatYear(year)} · EPISODIO DOCUMENTADO`;
    $('#selection-text').innerHTML=`<h3>${esc(p.kind==='battle'?'Batalla o episodio localizado':'Referencia regional de un conflicto')}</h3><p>${esc(formatEventDate(String(p.start),p.precision??11)+' — '+formatEventDate(String(p.end),p.precision??11))}</p><p>${esc(p.note)}</p>${!feature?'<p class="profile-note">El episodio no está activo en el año consultado; se conserva su ficha.</p>':''}<a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">${esc(p.sourceLabel)} ↗</a>`;
  }else if(selectedAnchor.place){
    $('#selection-text').innerHTML=feature?`<p>${esc(p.referenceKind==='archaeological-site'?'Yacimiento o centro documentado':p.capital?'Capital o sede administrativa':'Gran ciudad')} · ${esc(p.country)}</p><p>${esc(p.note??'Localización urbana de referencia contemporánea.')}</p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">Fuente del lugar ↗</a>`:`<p>No hay un registro de este lugar en la capa de ${formatYear(year)}. La ficha se conserva para continuar el recorrido.</p>`;
  }else if(p.contextKey){
    $('#selection-date').textContent=`${formatYear(year)} · ${p.kind==='human-range'?'DISTRIBUCIÓN HUMANA ESTIMADA':p.kind==='polity-reference'?'REFERENCIA POLÍTICA':'REGIÓN CULTURAL'}`;
    $('#selection-text').innerHTML=p.kind==='human-range'?distributionCard(p,year,Boolean(feature)):regionalCard(p as RegionalRecord,year,Boolean(feature));
  }else{
    $('#selection-text').innerHTML=countryCard(p,year,snapshot,profiles,identityData,import.meta.env.BASE_URL,{indicators:indicatorData,history:countryHistory,available:Boolean(feature),key:selectedAnchor.key,timelineFilter,timelineFuture,timelineExpanded,trends:trendSelections});
    const tab=document.getElementById('tab-'+activeCountryTab);if(tab)activateCountryTab(tab);
    const pinned=comparison.pinned.some(a=>anchorId(a)===anchorId(selectedAnchor!));
    const pin=document.getElementById('pin-country');if(pin){pin.textContent=pinned?'Fijado para comparar':'Fijar para comparar';pin.setAttribute('aria-pressed',String(pinned));}
    if(activeCountryTab==='comparison')void renderComparison();
  }
  highlightFeature(!p.contextKey&&!selectedAnchor.uid&&!selectedAnchor.place&&!p.sovereignSeat?feature?.id:undefined);
  highlightRegion(p.contextKey&&p.kind!=='human-range'?feature?.id:undefined);highlightDistribution(p.kind==='human-range'?feature?.id:undefined);renderAlternatives();
  const content=document.querySelector('.country-content');if(content)content.scrollTop=top;
}
async function regionalRawAt(y:number):Promise<FeatureCollection>{const sets=await Promise.all(regionalAssets(y).map(file=>asset<FeatureCollection>(file)));return{type:'FeatureCollection',features:sets.flatMap(d=>d.features)};}
async function featureAt(anchor:CountryAnchor,targetYear:number){
  const target=snapshotFor(targetYear);if(target.kind==='concept'||target.kind==='geological')return undefined;
  if(target.kind==='prehistoric')return matchingFeature(anchor,regionsAt(await regionalRawAt(targetYear),targetYear,empty),targetYear,identityData);
  const raw=target.kind==='annual'?await annualData(targetYear):await asset<FeatureCollection>(target.file!);
  const data=anchor.uid?await overlaysFor(targetYear):(await controlledMap(politicalData(raw,targetYear,target.kind==='modern'?profiles:undefined),targetYear>=-3000?await overlaysFor(targetYear):empty,targetYear)).territories;
  const regions=hasHumanEvidence(targetYear)?regionsAt(await regionalRawAt(targetYear),targetYear,data):empty;
  return matchingFeature(anchor,{type:'FeatureCollection',features:[...data.features,...datedPlaces(data,targetYear).features.filter(f=>f.properties?.sovereignSeat),...regions.features]},targetYear,identityData);
}
async function renderComparison(){
  if(!selectedAnchor||selectedAnchor.place||$('#map').getAttribute('aria-busy')==='true'||!document.getElementById('country-comparison'))return;
  const generation=++selectionGeneration,anchor=selectedAnchor;
  $('#country-comparison').innerHTML=comparisonShell(comparison,year,profiles,indicatorData);
  const selectedYear=year;
  const anchors=comparison.mode==='dates'?[anchor,anchor]:[...comparison.pinned,...(comparison.pinned.some(a=>anchorId(a)===anchorId(anchor))?[]:[anchor])].slice(0,4);
  const dates=comparison.mode==='dates'?[comparison.a,comparison.b]:anchors.map(()=>selectedYear);
  try{
    const selections=await Promise.all(anchors.map(async(a,i)=>({anchor:a,year:dates[i],feature:await featureAt(a,dates[i])})));
    if(generation!==selectionGeneration||!document.getElementById('comparison-results'))return;
    $('#comparison-results').innerHTML=comparisonMarkup(selections,comparison,profiles,indicatorData,identityData,import.meta.env.BASE_URL,selectedYear);
  }catch{if(generation===selectionGeneration&&document.getElementById('comparison-results'))$('#comparison-results').innerHTML='<p>No se pudo cargar la comparación. Cambia una fecha o el indicador para reintentar.</p>';}
}
async function navigateEntity(key:string,name:string,targetYear:number){
  stopPlay();
  selectedAnchor={key,name,originalName:name,code:'',uid:'',place:false,country:'',properties:{name,identityKey:key,workspaceKey:key},year:targetYear};
  await updateYear(targetYear);renderSelection();
}
let toastTimer: ReturnType<typeof setTimeout>;
function toast(text:string){ $('#toast').textContent=text;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,6000); }
function status(text:string,error=false){$('#map-status').textContent=text;$('.status-dot').classList.toggle('error',error);$('#retry').hidden=!error;$('#sources-button').classList.toggle('has-error',error);}
function setPlaybackLoading(busy:boolean,targetYear=year,error=false){
  const button=$('#play');
  if(button.getAttribute('aria-busy')===String(busy)&&(!busy||button.dataset.loadingYear===String(targetYear)))return;
  button.setAttribute('aria-busy',String(busy));
  if(busy)button.dataset.loadingYear=String(targetYear);else delete button.dataset.loadingYear;
  button.title=busy?`Cargando mapa de ${formatYear(targetYear)}…`:error?'No se pudo cargar la fecha solicitada':playing?'Pausar recorrido':'Reproducir recorrido';
  $('#playback-status').textContent=busy?`Cargando mapa de ${formatYear(targetYear)}…`:error?'No se pudo cargar la fecha. Se conserva el mapa anterior.':`Mapa actualizado a ${formatYear(targetYear)}.`;
}
function reliefAvailable(){return year>=-10000&&snapshot.kind!=='concept'&&snapshot.kind!=='geological';}
function updateSources(){
  const credits=Object.values(map.getStyle()?.sources??{}).flatMap(source=>'attribution' in source&&typeof source.attribution==='string'?[source.attribution]:[]);
  $('#map-attributions').innerHTML=[...new Set(credits)].join('<br>');
  const source=hasHumanEvidence(year)?['Poblamiento y evidencias','https://github.com/AlejandroPico/Historicmap/blob/main/docs/RESEARCH-bc100000.md']:year<-3000&&year>=-10000?['Poblamiento y arqueología','https://github.com/AlejandroPico/Historicmap/blob/main/docs/RESEARCH-bc10000.md']:snapshot.kind==='modern'?['Natural Earth','https://www.naturalearthdata.com/']:snapshot.kind==='annual'?(year<1886?['Cliopatria','https://github.com/Seshat-Global-History-Databank/cliopatria']:['CShapes 2.0','https://icr.ethz.ch/data/cshapes/']):snapshot.kind==='geological'?['Cao et al. 2024','https://doi.org/10.1016/j.gsf.2024.101922']:['Atlas histórico · A. Ourednik','https://github.com/aourednik/historical-basemaps'];
  if(snapshot.kind==='concept'){source[0]=year < -1800000000?'NASA · formación planetaria':'Smithsonian · evolución humana';source[1]=year < -1800000000?'https://science.nasa.gov/earth/facts/':'https://humanorigins.si.edu/';}
  $('#source-reference').textContent=`Fecha consultada: ${formatYear(year)}.${year>=-3000?` Autoridades adquiridas: ${identityData?.retrieved??'cargando'}.`:''}`;
  $('#source-links').innerHTML=`<a href="${source[1]}" target="_blank" rel="noopener">${source[0]} ↗</a>${year>=-3000?' · <a href="https://data.worldbank.org/" target="_blank" rel="noopener">Indicadores WDI ↗</a> · <a href="https://www.wikidata.org/" target="_blank" rel="noopener">Autoridades ↗</a>':''}${affiliation?` · <a href="${esc(AFFILIATIONS[affiliation].source)}" target="_blank" rel="noopener">${esc(AFFILIATIONS[affiliation].label)} ↗</a>`:''}`;
  $('#source-scope').textContent=hasHumanEvidence(year)?'Yacimientos y ventanas de evidencia, no ocupaciones continuas, fronteras humanas o rutas exactas. Atribuciones biológicas y culturales según las fuentes. Costa contemporánea de referencia.':year<-3000&&year>=-10000?'Comunidades y yacimientos con fechas aproximadas; sin fronteras nacionales ni gobernantes supuestos. Costa contemporánea de referencia.':snapshot.kind==='modern'?'Cartografía de referencia 2026. Las cifras y las membresías conservan sus propias fechas. Imágenes: autor y licencia en cada ficha.':snapshot.kind==='annual'?'Base territorial al cierre anual; contornos de referencia identificados en las fichas. Control con fecha propia. Mandatos de todo el año y membresías al cierre.':'Reconstrucción según la fecha y el alcance del modelo; no es una observación directa.';
  if(hasRegionalCoverage(year)){$('#source-links').innerHTML+=' · <a href="https://github.com/AlejandroPico/Historicmap/blob/main/docs/CULTURAL-MODERN-REVIEW.md" target="_blank" rel="noopener">Pueblos y regiones ↗</a>';$('#source-scope').textContent+=` Regiones culturales: ventanas de consulta ${regionalCoverage.windows.map(w=>w.start+'–'+w.end).join(', ')}; no son fronteras anuales. Las fichas distinguen testimonio espacial, incertidumbre y fechas.`;}
  if(iceEnabledFor(year,iceMode)&&iceSampleFor(year)){$('#source-links').innerHTML+=` · <a href="${iceSampleFor(year)!.source}" target="_blank" rel="noopener">${esc(iceSampleFor(year)!.model)} · hielo ↗</a>`;$('#source-scope').textContent+=' '+iceAvailabilityNote(year,true);}
  if(year>=-10000&&year<-3000)$('#source-scope').textContent+=' '+prehistoricClimate(year)+'. Límite del Holoceno: 11.700 años antes de 2000, no BP1950. La expansión humana es muy anterior a 10000 a. C.';
  if(isPrehistoric(year)&&iceSampleFor(year)&&!iceEnabledFor(year,iceMode))$('#source-scope').textContent+=' '+iceAvailabilityNote(year,false);
  if(isPrehistoric(year)&&!iceSampleFor(year))$('#source-scope').textContent+=' '+iceAvailabilityNote(year,false);
  if(physical&&reliefAvailable())$('#source-scope').textContent+=' Relieve contemporáneo de referencia; no reconstruye altitudes ni costas antiguas.';
  if(governmentFilter)$('#source-links').innerHTML+=' · <a href="https://ourworldindata.org/grapher/political-regime" target="_blank" rel="noopener">Formas políticas / V-Dem ↗</a>';
  if(isPrehistoric(year)){if(distributionCoast(year)!=='countries.geojson')$('#source-scope').textContent=$('#source-scope').textContent!.replace('Costa contemporánea de referencia.','Costas CAO2024 de referencia; fecha del modelo '+distributionCoast(year).match(/\d+/)?.[0]+'Ma. Coordenadas de los fósiles actuales, sin rotación retrospectiva individual.');$('#source-scope').textContent+=' '+climateContext(year)+' Distribuciones regionales estimadas; sus franjas no acreditan guerras ni dominio.';}
  if(snapshot.kind==='concept')$('#source-scope').textContent='Escena conceptual y contexto documental; no hay geometría reconstruida para esta fecha.';
  $('#source-links').innerHTML+=' · <a href="https://stratigraphy.org/ICSchart/ChronostratChart2026-06.pdf" target="_blank" rel="noopener">Cronología ICS2026/06 ↗</a>';
  const deep=deepSceneAt(year);if(deep){$('#source-links').insertAdjacentHTML('beforeend',deep.sourceIds.map(id=>{const s=deepSources[id as keyof typeof deepSources];return `<a href="${s.url}" target="_blank" rel="noopener">${esc(s.name)} ↗</a>`}).join(''));$('#source-scope').textContent+=' Textura y clima visual ilustrativos; no porcentajes de gases ni contornos glaciales observados. Referencias y discrepancias en la enciclopedia.';}
}

function refreshMap(force=false):Promise<void> {
  snapshot=snapshotFor(year);
  const target={...snapshot}, targetYear=year, targetTheme=theme;
  const displayKey=target.kind==='prehistoric'?`prehistory-${targetYear}`:target.kind==='annual'?`history-${targetYear}`:target.file??`concept-${year < -1800000000 ? 'early':'human'}`;
  const targetIce=iceEnabledFor(targetYear,iceMode)?iceSampleFor(targetYear):undefined;
  const iceKey=targetIce?targetIce.file+(showIceUncertainty&&targetIce.uncertaintyFiles?':range':''):'off';
  const targetLand=target.kind==='prehistoric'?distributionCoast(targetYear):'countries.geojson';
  const key=`${displayKey}:${targetYear}:${theme}:ice-${iceKey}`;
  $('#ice-layer').toggleAttribute('disabled',!iceSampleFor(year)&&!deepIceAt(year));
  const concept=snapshot.kind==='concept';$('.atlas').classList.toggle('deep-time',!!deepSceneAt(year));
  $('#concept').hidden=!concept;
  $('#map').style.visibility='visible';
  $('#physical-layer').toggleAttribute('disabled',!reliefAvailable());
  $('#affiliation-select').toggleAttribute('disabled',!affiliationsAvailable(year));
  for(const control of document.querySelectorAll('[data-visibility=political]'))control.toggleAttribute('disabled',concept||snapshot.kind==='geological');
  $('#places-layer').toggleAttribute('disabled',year < -10000);
  $('#occupations-layer').toggleAttribute('disabled',year<-3000);
  $('#theme-select').toggleAttribute('disabled',year<1960||snapshot.kind==='geological');
  $('#territory-description').textContent=snapshot.kind==='geological'?'Masas continentales reconstruidas':snapshot.kind==='modern'?'Países y fronteras':snapshot.kind==='annual'?(year<-3000?'Poderes y centros documentados':'Territorios y dependencias fechados'):'Áreas políticas y culturales';
  $('#concept').classList.toggle('human-era',year > -1800000000);
  $('#concept-caption').textContent=year < -1800000000?'ESCENA CONCEPTUAL · SIN GEOMETRÍA RECONSTRUIDA':'CARTOGRAFÍA PREHISTÓRICA PENDIENTE · SIN ÁREAS HUMANAS INFERIDAS';
  if(!ready){setPlaybackLoading(true,targetYear);return Promise.resolve();}
  // Stop requesting contemporary elevation as soon as the requested era changes.
  map.setLayoutProperty('relief','visibility',physical&&reliefAvailable()?'visible':'none');
  if(key===desiredKey&&!force){applyLayers();updateSources();if($('#map').dataset.loadedYear===String(year))renderSelection();return refreshPromise;}
  const current=++requestNumber;
  const previousKind=activeKey.startsWith('coastlines-')?'geological':'other';
  desiredKey=key;
  delete $('#map').dataset.rendered;
  $('#map').setAttribute('aria-busy','true');
  setPlaybackLoading(true,targetYear);
  $('#map').dataset.loadStage='fetch';
  $('#search-button').toggleAttribute('disabled',true);
  if(snapshot.kind==='geological'&&previousKind!=='geological'||concept&&committedDomain!=='concept')map.jumpTo({center:[0,15],zoom:1.5});
  if(selectedAnchor){$('#selection').setAttribute('aria-busy','true');$('#selection-status').hidden=true;}
  if(!$('#search-panel').hidden)$('#search-results').textContent='Actualizando territorios…';
  highlightFeature();
  if(concept){
   const commit=async()=>{if(current!==requestNumber)return;
    if(committedDomain!=='concept')for(const [id,source]of Object.entries(map.getStyle().sources))if(source.type==='geojson')await(map.getSource(id)as GeoJSONSource).setData(empty);
    if(current!==requestNumber)return;
    activeKey=displayKey;loaded=empty;cityData=empty;overlayData=empty;regionalData=empty;distributionData=empty;sharedData=empty;committedDomain='concept';committedData=empty;
    territorySignature='';citySignature='';regionalSignature='';distributionSignature='';sharedSignature='';overlaySignature='';referenceLandKey='';referenceLandOn=false;
    for(const name of ['overlays','humanRanges','humanShared','humanEvidence','conflictEvents','places'])$('#map').dataset[name]='0';$('#map').dataset.iceFile='off';$('#map').dataset.iceAgeBp='';$('#map').dataset.iceVisible='false';$('#map').dataset.iceModel='';$('#map').dataset.iceUncertainty='false';
    $('#map-legend').hidden=true;$('#map').dataset.loadedYear=String(targetYear);$('#map').dataset.territories='0';$('#map').dataset.culturalRegions='0';$('#map').dataset.referenceLand='false';
    applyLayers();paintDeepSurface(targetYear);$('#map').setAttribute('aria-busy','false');$('#map').dataset.loadStage='ready';setPlaybackLoading(false,targetYear);
    status('Escenario precámbrico · geometría ilustrativa');updateSources();renderSelection();refreshSearch();map.triggerRepaint();
   };renderQueue=renderQueue.then(commit,commit);refreshPromise=renderQueue;return refreshPromise;
  }
  status(`Cargando ${formatYear(target.year)}…${loaded.features.length?' · se conserva el mapa anterior':''}`);
  updateSources();
  refreshPromise=(async()=>{
    try {
      const [rawData,profileData,points,overlays,identities,referenceLand,indicators,historyDetails,regionalRaw,iceMargins,rawDistributions]=await Promise.all([
        target.kind==='prehistoric'?Promise.resolve(empty):target.kind==='annual'?annualData(targetYear):asset<FeatureCollection>(target.file!),
        asset<ProfileData>('profiles.json'),
        target.kind==='modern'?modernCities():Promise.resolve(empty),
        targetYear>=-3000?overlaysFor(targetYear):Promise.resolve(empty),
        asset<IdentityData>('identities.json'),
        target.kind!=='geological'?asset<FeatureCollection>(targetLand):Promise.resolve(empty),
        asset<IndicatorData>('country-indicators.json'),asset<CountryHistory>('country-history.json'),regionalRawAt(targetYear),targetIce?Promise.all([targetIce.file,...(showIceUncertainty?targetIce.uncertaintyFiles??[]:[])].map(file=>asset<FeatureCollection>(file))).then(rows=>({type:'FeatureCollection' as const,features:rows.flatMap(r=>r.features)})):Promise.resolve(empty),target.kind==='prehistoric'?asset<FeatureCollection>('human-ranges.geojson'):Promise.resolve(empty)
      ]);
      if(current!==requestNumber)return;
      const composed=await controlledMap(politicalData(rawData,targetYear,target.kind==='modern'?profileData:undefined),overlays,targetYear);
      if(current!==requestNumber)return;
      const regional=withRenderIds(regionsAt(regionalRaw,targetYear,composed.territories),'regions');
      const distribution=distributionsAt(rawDistributions,targetYear);
      const ranges=withRenderIds(distribution.areas,'human-ranges');
      const data=withRenderIds(withGovernance(composed.territories,targetYear),displayKey),hatching=withGovernance({...composed.occupations,features:[...composed.occupations.features,...nationalInfluenceHatching(composed.territories,targetYear).features]},targetYear);
      const themed=thematicData(data,profileData,targetTheme,targetYear);
      const signature=target.kind==='annual'||target.kind==='modern'?data.features.map(f=>`${f.id}:${f.properties?.name}:${f.properties?.politicalColor}:${f.properties?.controlInfluenceColor}:${f.properties?.identityKey}:${f.properties?.controlRecord}:${f.properties?.governmentTags}`).join('|'):target.file!;
      const commit=async()=>{
        if(current!==requestNumber)return;
        $('#map').dataset.loadStage='ice';
        if($('#map').dataset.iceFile!==iceKey){await (map.getSource('ice-margins') as GeoJSONSource).setData(iceMargins);if(current!==requestNumber)return;$('#map').dataset.iceFile=iceKey;}
        $('#map').dataset.iceAgeBp=targetIce?String(targetIce.ageBP):'';
        $('#map').dataset.iceModel=targetIce?.model??'';
        $('#map').dataset.loadStage='territories';
        const referenceOn=referenceLand.features.length>0;
        if(referenceOn!==referenceLandOn||referenceLandKey!==targetLand){await (map.getSource('reference-land') as GeoJSONSource).setData(referenceLand);referenceLandOn=referenceOn;referenceLandKey=targetLand;}
        $('#map').dataset.referenceLand=String(referenceOn);$('#map').dataset.referenceLandFile=targetLand;
        if(signature!==territorySignature||force){
          const source=map.getSource('territories') as GeoJSONSource;
          if(committedDomain===target.kind&&['annual','modern'].includes(target.kind)){
            const diff=sourceDiff(committedData,data);
            if(diff.add?.length||diff.remove?.length||diff.update?.length)await source.updateData(diff);
          }else await source.setData(data);
          committedData=data;committedDomain=target.kind;territorySignature=signature;
        }
        if(current!==requestNumber)return;
        $('#map').dataset.loadStage='overlays';
        const overlayKey=`${targetYear}:`+hatching.features.map(f=>f.properties?.patternKey).join('|');
        if(overlayKey!==overlaySignature){
          for(const f of hatching.features){const p=f.properties!;if(!map.hasImage(p.patternKey))map.addImage(p.patternKey,occupationPattern(p.controlColor,p.occupiedColor));}
          await (map.getSource('occupations') as GeoJSONSource).setData(hatching);overlaySignature=overlayKey;
        }
        if(current!==requestNumber)return;
        const nextRegionalSignature=regional.features.map(f=>f.id).join('|');
        if(nextRegionalSignature!==regionalSignature){await (map.getSource('cultural-regions') as GeoJSONSource).setData(regional);regionalSignature=nextRegionalSignature;}
        if(current!==requestNumber)return;
        regionalData=regional;$('#map').dataset.culturalRegions=String(regional.features.length);
        const rangeSignature=ranges.features.map(f=>f.id).join('|');
        if(rangeSignature!==distributionSignature){await(map.getSource('human-ranges') as GeoJSONSource).setData(ranges);if(current!==requestNumber)return;distributionSignature=rangeSignature;}
        distributionData=ranges;sharedData=distribution.overlaps;$('#map').dataset.humanRanges=String(ranges.features.length);$('#map').dataset.humanShared=String(sharedData.features.length);
        $('#map').dataset.territories=String(data.features.length);
        loaded=themed;profiles=profileData;identityData=identities;indicatorData=indicators;countryHistory=historyDetails;overlayData=hatching;activeKey=displayKey;
        // Statistics change paint only: do not re-index or tessellate coastlines for a new number.
        if(targetTheme!=='political')for(const f of themed.features)if(f.id!==undefined)map.setFeatureState({source:'territories',id:f.id},{metric:f.properties?.metric??null});
        cityData=target.kind==='prehistoric'?empty:target.kind==='modern'?points:target.kind==='annual'?datedPlaces(data,targetYear):{type:'FeatureCollection',features:places.filter(p=>targetYear>=p.start&&targetYear<=p.end).map(p=>({type:'Feature',geometry:{type:'Point',coordinates:p.coordinates},properties:{name:p.name,note:p.description,country:'Yacimiento / ciudad histórica',rank:1}}))};
        cityData=withGovernance(cityData,targetYear);
        applyLayers();paintDeepSurface(targetYear,target.kind==='geological'?themed:undefined);
        $('#map').dataset.loadedYear=String(targetYear);
        $('#map').setAttribute('aria-busy','false');
        $('#search-button').toggleAttribute('disabled',false);
        $('#map').dataset.loadStage='ready';
        renderSelection();refreshSearch();
        const label=target.kind==='prehistoric'?`Poblamiento y evidencias · ${formatYear(targetYear)} · ${regional.features.length} yacimientos`:targetYear<-3000&&targetYear>=-10000?`Poblamiento y arqueología · ${formatYear(targetYear)} · ${regional.features.length} referencias`:target.kind==='modern'?`Natural Earth · referencia contemporánea 2026${targetYear!==2026?` · consulta ${targetYear}`:''}`:target.kind==='annual'?`${targetYear<1886?'Cliopatria · síntesis anual':targetYear>=1940&&targetYear<=1944?'CShapes + control · síntesis anual':'CShapes + referencias · 31 dic'} ${formatYear(targetYear)} · ${data.features.length} territorios`:`${target.kind==='geological'?'CAO2024 · reconstrucción':'Fronteras aproximadas'} · ${formatYear(target.year)}`;
        status(label);
        updateSources();
        // Source update completion precedes tile replacement. Querying here
        // can address an old tile against the new feature index. Let the next
        // idle frame certify rendered geometry before accepting map clicks.
        map.triggerRepaint();
      };
      renderQueue=renderQueue.then(commit,commit);await renderQueue;
    } catch(error) {
      if(current!==requestNumber)return;
      console.error('Temporal map refresh failed',error);
      desiredKey='';$('#map').setAttribute('aria-busy','false');setPlaybackLoading(false,targetYear,true);if(selectedAnchor){$('#selection').setAttribute('aria-busy','false');$('#selection-status').textContent='La fecha no se pudo cargar. La ficha conserva el año indicado en su cabecera.';$('#selection-status').hidden=false;}status('No se ha podido cargar la fecha. Se conserva el mapa anterior.',true);stopPlay();
    }
  })();
  return refreshPromise;
}
function applyGovernmentFilter(){
 const counts=governmentCounts({type:'FeatureCollection',features:[...loaded.features,...cityData.features.filter(f=>f.properties?.sovereignSeat)]}),signature=String(year)+governmentFilter+JSON.stringify([...counts]);
 const select=$<HTMLSelectElement>('#government-select');
 if(signature!==governmentOptionsSignature){
  governmentOptionsSignature=signature;
  const groups=[...new Set(governmentTags.map(t=>t.group))];
  const available=governmentTags.filter(t=>(counts.get(t.id)??0)>0),emptyActive=!!governmentFilter&&!counts.get(governmentFilter);
  select.innerHTML=`<option value="">${emptyActive?'Elegir otra forma':'Todas las formas'}</option>`+groups.filter(group=>available.some(t=>t.group===group)).map(group=>`<optgroup label="${esc(group)}">${available.filter(t=>t.group===group).map(t=>`<option value="${t.id}">${esc(t.label)} · ${counts.get(t.id)}</option>`).join('')}</optgroup>`).join('');select.value=emptyActive?'':governmentFilter;
  const notice=$('#government-empty');notice.hidden=!emptyActive;notice.innerHTML=emptyActive?`<p>${esc(governmentTags.find(t=>t.id===governmentFilter)?.label??governmentFilter)} no tiene entidades documentadas en ${year}.</p><button class="secondary-button" data-government-filter="">Quitar filtro</button>`:'';
 }
 const active=!!governmentFilter&&political&&snapshot.kind!=='geological';
 select.disabled=snapshot.kind==='geological'||snapshot.kind==='concept';
 const filter:ExpressionSpecification|undefined=active?['in',governmentFilter,['coalesce',['get','governmentTags'],['literal',[]]]]:undefined;
 const signatureFilter=active?governmentFilter:'';
 if($('#map').dataset.governmentFilter!==signatureFilter){
  for(const layer of ['territory-fill','territory-line','territory-labels','occupation-fill','occupation-line','place-circles','place-labels'])map.setFilter(layer,filter);
  $('#map').dataset.governmentFilter=signatureFilter;
 }
 $('#map').dataset.governmentMatches=String(governmentFilter?counts.get(governmentFilter)??0:new Set(loaded.features.map(f=>f.properties?.identityKey??f.properties?.entityCode??f.id)).size);
 $('#government-help').textContent=governmentFilter?`${counts.get(governmentFilter)??0} entidades con esta clasificación en ${year}. Se conserva el filtro al cambiar de fecha.`:'Forma institucional y evaluación política son dimensiones distintas. Las fechas y fuentes se consultan en Instituciones.';
}
function applyLayers(){
  cityData=withGovernance(cityData,year);
  for(const [kind,on]of [['political',political],['cultural',showRegional],['human-ranges',showHumanRanges]]as const)for(const control of document.querySelectorAll(`[data-visibility=${kind}]`)){control.classList.toggle('active',on);control.setAttribute('aria-pressed',String(on));}
  $('#political-filter-help').textContent=$('#territory-description').textContent;
  $('#physical-layer').classList.toggle('active',physical&&reliefAvailable());$('#physical-layer').setAttribute('aria-pressed',String(physical&&reliefAvailable()));
  $('#places-layer').classList.toggle('active',showPlaces);$('#places-layer').setAttribute('aria-pressed',String(showPlaces));
  $('#occupations-layer').classList.toggle('active',showOccupations);$('#occupations-layer').setAttribute('aria-pressed',String(showOccupations));
  $('#ice-layer').classList.toggle('active',iceEnabledFor(year,iceMode));$('#ice-layer').setAttribute('aria-pressed',String(iceEnabledFor(year,iceMode)));$<HTMLSelectElement>('#ice-mode').value=iceMode;$('#map').dataset.iceMode=iceMode;$('#ice-help').textContent=iceSampleFor(year)?(iceMode==='auto'?'Automático · ':'')+(iceSampleFor(year)!.kind==='interval-hypothesis'?iceSampleFor(year)!.label+' · hipótesis de intervalo, no frente anual':'Referencia '+formatYear(iceSampleFor(year)!.referenceYear)+' · muestras de 2.500–5.000 años'):'Sin contorno de hielo incorporado para esta fecha';
  if(!ready)return;
  const iceOn=iceEnabledFor(year,iceMode)&&$('#map').dataset.iceAgeBp===String(iceSampleFor(year)!.ageBP);
  for(const id of ['ice-fill','ice-line'])map.setLayoutProperty(id,'visibility',iceOn?'visible':'none');$('#map').dataset.iceVisible=String(iceOn);
  const olderIce=iceSampleFor(year)?.kind==='interval-hypothesis';$('#ice-uncertainty').hidden=!olderIce;$('#ice-uncertainty').toggleAttribute('disabled',!iceOn);$('#ice-uncertainty').setAttribute('aria-pressed',String(showIceUncertainty));$('#ice-uncertainty').classList.toggle('active',showIceUncertainty);
  for(const id of['ice-minimum','ice-maximum'])map.setLayoutProperty(id,'visibility',iceOn&&olderIce&&showIceUncertainty?'visible':'none');$('#map').dataset.iceUncertainty=String(!!(iceOn&&olderIce&&showIceUncertainty));
  for(const control of document.querySelectorAll('[data-visibility=human-ranges]'))control.toggleAttribute('disabled',!isPrehistoric(year));
  const rangesOn=showRegional&&showHumanRanges&&isPrehistoric(year);
  for(const id of ['human-range-fill','human-range-line','human-range-shared','human-range-selected','human-range-labels'])map.setLayoutProperty(id,'visibility',rangesOn?'visible':'none');
  const rangeFilter:any=humanFilter?['==',['get','group'],humanFilter]:['has','lineage'];
  for(const id of ['human-range-fill','human-range-line','human-range-selected','human-range-labels'])map.setFilter(id,rangeFilter);
  const shared={...sharedData,features:sharedData.features.filter(f=>!humanFilter||f.properties!.groups.includes(humanFilter)).map(f=>{const p=f.properties!,focus=humanFilter&&p.groups.filter((g:string)=>g===humanFilter).length===1?p.groups.indexOf(humanFilter):-1,patternKey='human-shared-'+p.members.join('-')+'-'+focus;if(!map.hasImage(patternKey))map.addImage(patternKey,coexistencePattern(p.colors,focus));return{...f,properties:{...p,patternKey}};})};
  const sharedKey=distributionSignature+':'+humanFilter;
  if(sharedKey!==sharedSignature){(map.getSource('human-shared') as GeoJSONSource).setData(shared);sharedSignature=sharedKey;}
  $('#map').dataset.humanRangesVisible=String(rangesOn);
  const visibilitySignature=`${political}:${showRegional}`;
  if($('#map').dataset.visibilityRendered!==visibilitySignature)delete $('#map').dataset.visibilityRendered;
  const regionalOn=showRegional&&hasRegionalCoverage(year)&&!['concept','geological'].includes(snapshot.kind);
  for(const id of ['cultural-fill','regional-polity-fill','cultural-line','cultural-labels','cultural-selected','human-evidence-circles','human-evidence-labels'])map.setLayoutProperty(id,'visibility',regionalOn?'visible':'none');
  $('#map').dataset.culturalVisible=String(regionalOn);
  const regionalParents=[...new Set(regionalData.features.flatMap(f=>f.properties?.parentContextKeys??[]))];
  map.setFilter('cultural-labels',['all',['==',['geometry-type'],'Polygon'],['!', ['in',['get','contextKey'],['literal',regionalParents]]]]);
  const humanMask:any=['all',['==',['geometry-type'],'Point'],...(humanFilter?[['in',humanFilter,['get','taxonGroups']]]:[])];for(const id of['human-evidence-circles','human-evidence-labels'])map.setFilter(id,humanMask);
  $('#human-filter-block').hidden=!hasHumanEvidence(year);const humanSelect=$<HTMLSelectElement>('#human-group-select'),counts=humanGroupCounts({type:'FeatureCollection',features:[...regionalData.features,...distributionData.features]});humanSelect.innerHTML='<option value="">Todos los grupos</option>'+counts.filter(g=>g.count||g.id===humanFilter).map(g=>`<option value="${g.id}">${g.label} · ${g.count}</option>`).join('');humanSelect.value=humanFilter;
  $('#cultural-help').textContent=isPrehistoric(year)?`${regionalData.features.length} yacimientos · intervalos de evidencia y atribuciones de las fuentes`:hasRegionalCoverage(year)?`${regionalData.features.filter(f=>f.properties?.kind==='cultural-region').length} regiones · referencias ${[...new Set(regionalData.features.filter(f=>f.geometry.type!=='Point').map(f=>f.properties?.sourceYear))].sort((a,b)=>Number(a)-Number(b)).map(y=>Number(y)<0?formatYear(Number(y)):y).join(', ')}`:'Revisión de esta fecha pendiente · no implica desaparición';
  $('#cultural-filter-help').textContent=$('#cultural-help').textContent;
  $('#map').dataset.politicalVisible=String(political&&snapshot.kind!=='geological');
  map.setLayoutProperty('territory-fill','visibility',political||snapshot.kind==='geological'?'visible':'none');
  map.setLayoutProperty('territory-selected','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  applyGovernmentFilter();
  const thresholds=theme==='gdp'?[1e10,1e11,1e12,1e13]:theme==='population'?[1e6,1e7,1e8,1e9]:[1000,5000,15000,50000];
  const thematic:ExpressionSpecification=['case',['==',['feature-state','metric'],null],'#6c7776',['interpolate',['linear'],['coalesce',['feature-state','metric'],0],0,'#d7e9c4',thresholds[0],'#a4c994',thresholds[1],'#6aab7d',thresholds[2],'#398769',thresholds[3],'#15624f']];
  const groups=affiliation?affiliationGroups(affiliation,year):[];
  const politicalPaint:ExpressionSpecification=['coalesce',['get','controlInfluenceColor'],['get','politicalColor'],'#829c90'];
  const membership:ExpressionSpecification=affiliation?(groups.length?['match',['coalesce',['get','entityCode'],['get','code']],...groups.flatMap(c=>[[...c.codes],c.color]),'#68777b'] as unknown as ExpressionSpecification:['literal','#68777b']):colorExpression;
  map.setPaintProperty('territory-fill','fill-color',political?(affiliation?membership:theme==='political'?politicalPaint:thematic):'#819c88');
  map.setLayoutProperty('territory-line','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  map.setPaintProperty('territory-fill','fill-opacity',!political&&hasRegionalCoverage(year)?0:snapshot.kind==='geological'?1:theme==='political'?['case',['==',['get','status'],'source-reference'],0.12,1]:0.88);
  map.setPaintProperty('territory-fill','fill-antialias',snapshot.kind!=='geological');
  map.setLayoutProperty('territory-labels','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  map.setLayoutProperty('relief','visibility',physical&&reliefAvailable()?'visible':'none');
  const controlVisible=showOccupations&&year>=-3000;
  for(const id of ['occupation-fill','occupation-line'])map.setLayoutProperty(id,'visibility',controlVisible?'visible':'none');
  const nextConflicts=year>=-3000?conflictPointsFor(year):empty;const nextConflictSignature=showOccupations?JSON.stringify(nextConflicts):'';
  conflictData=nextConflicts;
  if(nextConflictSignature!==conflictSignature){conflictSignature=nextConflictSignature;void (map.getSource('conflict-points') as GeoJSONSource).setData(controlVisible?conflictData:empty);}
  for(const layer of ['conflict-circles','conflict-labels'])map.setLayoutProperty(layer,'visibility',controlVisible?'visible':'none');
  $('#map').dataset.conflictEvents=String(controlVisible?conflictData.features.length:0);
  $('#occupations-help').textContent=`${overlayData.features.length} franjas y ${conflictData.features.length} puntos documentados en ${year}`;
  const nextCitySignature=showPlaces?JSON.stringify(cityData):'';
  if(nextCitySignature!==citySignature){citySignature=nextCitySignature;void (map.getSource('places') as GeoJSONSource).setData(showPlaces?cityData:empty);}
  $('#map').dataset.places=String(showPlaces?cityData.features.length:0);$('#places-help').textContent=year<-3000?`${cityData.features.length} yacimientos y centros de referencia en ${formatYear(year)}`:`${cityData.features.length} capitales, sedes y ciudades documentadas en ${year}`;
  $('#map').dataset.overlays=String(controlVisible?overlayData.features.length:0);
  const controls=[...new Map(overlayData.features.map(f=>[f.properties!.controller,f.properties!])).values()];
  const labels:Record<string,string>={DEU:'Alemania',JPN:'Japón',ITA:'Italia',USSR:'URSS','CROATIA-CLIENT':'Croacia · cliente','FRA-VICHY':'Vichy · colaboracionista','CHN-COMMUNIST':'China · comunistas','ESP-REPUBLIC':'España · republicanos','ESP-NATIONALIST':'España · sublevados',RUS:'Rusia',ISR:'Israel',IRQ:'Irak','AUT-HUN':'Austria-Hungría',OTT:'Imperio otomano'};
  const nationalReference=overlayData.features.some(f=>f.properties?.referenceScope==='national-reference');
  const controlLegend=controlVisible&&controls.length?`<div class="control-legend"><strong>${nationalReference?'Intervención / presencia · referencia nacional':'Ocupación · síntesis anual'}</strong><div class="control-swatches">${controls.map(p=>`<span><i style="background:${p.controlColor}"></i>${esc(p.controller==='USA'?'EE. UU. / coalición':labels[p.controller]??p.name)}</span>`).join('')}</div><small>${nationalReference?'Franjas: potencia principal y país de referencia.<br>No son frentes, anexión ni control uniforme.':'Franja gruesa: controlador.<br>Franja fina: territorio ocupado.<br>El control no acredita soberanía.'}</small></div>`:'';
  const membershipLegend=affiliation?`<strong>${esc(AFFILIATIONS[affiliation].label)} · ${year}</strong><div class="control-swatches">${affiliationLegend(affiliation,year).map(c=>`<span><i style="background:${c.color}"></i>${esc(c.label)}</span>`).join('')}</div><small>${esc(affiliationSummary(affiliation,year))}</small>`:'';
  const familyLegend=political&&!affiliation&&theme==='political'&&loaded.features.some(f=>f.properties?.influenceKind||['colony','protectorate','mandate'].includes(f.properties?.status))?'<small>Los matices de una familia de color indican una relación documentada. Intervención o apoyo militar no equivalen a soberanía, anexión ni control uniforme.</small>':'';
  const front=loaded.features.find(f=>f.properties?.controlObservationDate)?.properties;
  const frontLegend=front?`<small class="control-observation">Ucrania · referencia cartográfica ${esc(String(front.controlObservationDate).split('-').reverse().join('/'))}<br>Incertidumbre mínima del frente: 7 km.</small>`:'';
  $('#map-legend').innerHTML=(governmentFilter?`<div class="government-legend"><strong>${esc(governmentTags.find(t=>t.id===governmentFilter)?.label??governmentFilter)}</strong><small>${$('#map').dataset.governmentMatches??0} entidades · ${year}</small></div>`:'')+frontLegend+familyLegend+(political?(membershipLegend||thematicLegend(loaded,theme)):'')+controlLegend+(iceEnabledFor(year,iceMode)&&iceSampleFor(year)?`<small class="ice-legend"><strong>Mantos de hielo · referencia modelada</strong><br>${iceCaption(year)}<br>No reconstruye paleocostas ni hielo marino.${iceSampleFor(year)?.kind==='interval-hypothesis'?(showIceUncertainty?'<br><span class="ice-range-key minimum">Azul discontinuo: hipótesis mínima</span><span class="ice-range-key maximum">Claro discontinuo: hipótesis máxima</span>':'<br>Márgenes mínimo/máximo disponibles en Capas.')+' MIS8/10 especialmente inciertos.':''}</small>`:'')+(controlVisible?`<div class="conflict-points-legend"><strong>${conflictData.features.length} conflictos y episodios localizados</strong><small>Coral: batalla o episodio. Violeta: referencia regional.<br>Los puntos no representan frentes ni ocupación. ${nationalReference?'Las franjas nacionales son referencias de intervención o presencia, no frentes locales.' : 'Las franjas de control usan los límites documentados.'}</small></div>`:'')+(rangesOn?distributionLegend({type:'FeatureCollection',features:distributionData.features.filter(f=>!humanFilter||f.properties!.group===humanFilter)}):'')+(showRegional&&hasHumanEvidence(year)?humanLegend({type:'FeatureCollection',features:regionalData.features.filter(f=>!humanFilter||f.properties?.taxonGroups?.includes(humanFilter)||humanFilter==='mixed'&&f.properties?.taxonGroup==='mixed')}):'')+(showRegional&&!isPrehistoric(year)&&hasRegionalCoverage(year)?`<small class="regional-legend">Pueblos y regiones: referencias cartográficas de ${[...new Set(regionalData.features.filter(f=>f.geometry.type!=='Point').map(f=>f.properties?.sourceYear))].sort((a,b)=>Number(a)-Number(b)).map(y=>Number(y)<0?formatYear(Number(y)):y).join(', ')}.<br>Áreas aproximadas; prioridad política y consulta de coincidencias.</small>`:'')+(referenceLandOn?`<small>Gris: sin representación en las capas activas; no significa despoblación.<br>${isPrehistoric(year)&&distributionCoast(year)!=='countries.geojson'?'Costas continentales CAO2024 · referencia modelada, no paleocosta cuaternaria detallada.':'Costa contemporánea de referencia.'}${year>=-10000&&!hasRegionalCoverage(year)?'<br>Revisión cultural de esta fecha pendiente.':''}</small>`:'');
  $('#map-legend').hidden=!$('#map-legend').innerHTML;
  const deep=deepSceneAt(year);map.setLayoutProperty('deep-surface','visibility',deep?'visible':'none');map.setPaintProperty('territory-line','line-opacity',deep?0:0.85);
  if(deep){paintDeepSurface(year,snapshot.kind==='geological'?loaded:undefined);const icy=!!deepIceAt(year)&&iceMode!=='off';$('#ice-layer').classList.toggle('active',icy);$('#ice-layer').setAttribute('aria-pressed',String(icy));$('#ice-help').textContent=deepIceAt(year)?'Escenario glacial ilustrativo, sin contorno reconstruido':'Sin escenario glacial activo';map.setPaintProperty('territory-fill','fill-opacity',0);$('#map-legend').innerHTML=`<strong>${esc(deep.title)}</strong><small>${snapshot.kind==='geological'?'Costas de referencia '+formatYear(snapshot.year):'Geometría ilustrativa, sin posiciones reconstruidas'} · texturas y hielo conceptuales</small><button data-encyclopedia-entry="${deep.article}">Leer en la enciclopedia →</button>`;$('#map-legend').hidden=false;}

}
let lastLocationWrite = -Infinity;
let locationTimer: ReturnType<typeof setTimeout>;
function persistLocation(){
  clearTimeout(locationTimer);
  const commit=()=>{lastLocationWrite=performance.now();history.replaceState(null,'',`#year=${year}&view=${projection}`);};
  const delay=Math.max(0,250-(performance.now()-lastLocationWrite));
  if(delay===0)commit();else locationTimer=setTimeout(commit,delay);
}
function updateYear(next:number,save=true){
  year=clamp(next,anchors[0],PRESENT);if(year===0)year=1;
  if(year<1960){theme='political';$<HTMLSelectElement>('#theme-select').value=theme;}
  position=yearToPosition(year);
  $('#year').textContent=formatYear(year);
  if(!affiliationsAvailable(year)){affiliation='';$<HTMLSelectElement>('#affiliation-select').value='';}
  renderRuler(); renderPlanet(); const refreshed=refreshMap();
  if(save)persistLocation();
  return refreshed;
}
let rulerKey='';
function renderRuler(){
  const track=$('#ruler-track');
  const bands=chronologyBands(year,position,spacing,$('#ruler').clientWidth);
  $('#chronology-bands').innerHTML=chronologyBandsMarkup(bands);
  $('#chronology-bands').hidden=!chronologyVisible;
  document.documentElement.style.setProperty('--chronology-height',chronologyVisible?bands.rows*15+'px':'0px');
  $('#chronology-layer').setAttribute('aria-pressed',String(chronologyVisible));$('#chronology-layer').classList.toggle('active',chronologyVisible);
  $('#chronology-bands').dataset.emphasis=String(bands.emphasis);
  $('#chronology-bands').dataset.mode=bands.emphasis>=.5?'geological':'human';
  const width=$('#ruler').clientWidth;
  const key=`${spacing}:${Math.floor(position*spacing/120)}:${width}`;
  if(rulerKey!==key){
    rulerKey=key;
    const fragment=document.createDocumentFragment();
    const left=position-(width/2+240)/spacing, right=position+(width/2+240)/spacing;
    const drawn=new Set<number>();
    const tick=(y:number,major:boolean)=>{
      if(y===1)major=true;
      if(y===0||drawn.has(y))return;
      const p=yearToPosition(y);
      if(p<left||p>right)return;
      drawn.add(y);const element=document.createElement('div');element.dataset.year=String(y);element.className=`tick ${major?'major':'minor'}`;element.style.left=`${p*spacing}px`;
      if(major){const label=document.createElement('span');label.textContent=formatYear(y);element.append(label);}
      fragment.append(element);
    };
    for(let i=Math.max(0,Math.floor(left));i<Math.min(anchors.length-1,Math.ceil(right));i++){
      const from=anchors[i],to=anchors[i+1];
      const raw=(to-from)*90/spacing;
      const magnitude=10**Math.floor(Math.log10(raw));
      const step=[1,2,5,10].find(n=>n*magnitude>=raw)!*magnitude;
      const minorStep=Math.max(1,step/5);
      const visibleFrom=Math.max(from,from+(left-i)*(to-from));
      const visibleTo=Math.min(to,from+(right-i)*(to-from));
      for(let y=Math.ceil(visibleFrom/minorStep)*minorStep;y<=visibleTo;y+=minorStep){
        tick(Math.round(y),Math.abs(y/step-Math.round(y/step))<1e-6);
      }
    }
    tick(1,true);track.replaceChildren(fragment);
    const labels=[...track.querySelectorAll<HTMLElement>('.tick.major')].map(t=>({year:Number(t.dataset.year),x:parseFloat(t.style.left),width:t.querySelector('span')!.getBoundingClientRect().width}));
    const readable=readableRulerLabels(labels);
    for(const t of track.querySelectorAll<HTMLElement>('.tick.major')){const label=t.querySelector('span')!;t.title=label.textContent!;t.setAttribute('aria-label',label.textContent!);label.hidden=!readable.has(Number(t.dataset.year));}
  }
  track.style.transform=`translateX(${width/2-position*spacing}px)`;
  $('#ruler').dataset.scale=String(spacing);
  $('#ruler').setAttribute('aria-valuenow',String(Math.round(position*100)));
  $('#ruler').setAttribute('aria-valuetext',`${formatYear(year)}, ${eraName(year)}`);
}
let startX=0,startPosition=0,dragging=false,bandPress:string|undefined;
const ruler=$('#ruler');
ruler.addEventListener('pointerdown',event=>{stopPlay();bandPress=(event.target as Element).closest<HTMLElement>('[data-encyclopedia-entry]')?.dataset.encyclopediaEntry;dragging=true;startX=event.clientX;startPosition=position;ruler.setPointerCapture(event.pointerId);ruler.classList.add('dragging');});
ruler.addEventListener('pointermove',event=>{if(dragging&&Math.abs(event.clientX-startX)>4){bandPress=undefined;updateYear(positionToYear(startPosition-(event.clientX-startX)/spacing));}});
for(const type of ['pointerup','pointercancel'])ruler.addEventListener(type,()=>{dragging=false;ruler.classList.remove('dragging');if(type==='pointerup'&&bandPress)showEncyclopedia(bandPress);bandPress=undefined;});
function zoomRuler(factor:number){stopPlay();spacing=clamp(Math.round(spacing*factor),96,4800);if(dragging){dragging=false;ruler.classList.remove('dragging');}renderRuler();}
$('.time-dock').addEventListener('wheel',event=>{event.preventDefault();event.stopPropagation();const units=event.deltaMode===1?16:event.deltaMode===2?ruler.clientHeight:1;zoomRuler(Math.exp(-clamp((event.deltaY||event.deltaX)*units,-240,240)*.0025));},{passive:false});
ruler.addEventListener('keydown',event=>{const keys:Record<string,number>={ArrowLeft:-24/spacing,ArrowRight:24/spacing,PageUp:-ruler.clientWidth*.8/spacing,PageDown:ruler.clientWidth*.8/spacing};if(event.key in keys){event.preventDefault();stopPlay();updateYear(positionToYear(position+keys[event.key]));}else if(event.key==='Home'){event.preventDefault();stopPlay();updateYear(anchors[0]);}else if(event.key==='End'){event.preventDefault();stopPlay();updateYear(PRESENT);}else if(['+','=','-','_'].includes(event.key)){event.preventDefault();zoomRuler(['+','='].includes(event.key)?1.25:1/1.25);}});
new ResizeObserver(renderRuler).observe(ruler);
function stopPlay(){playing=false;playGeneration++;$('#play').setAttribute('aria-pressed','false');$('#play').setAttribute('aria-label','Reproducir recorrido');if($('#play').getAttribute('aria-busy')!=='true')$('#play').title='Reproducir recorrido';$('#play').innerHTML=icon('play');createIcons({icons});}
async function play(generation:number){
  await refreshMap();
  while(playing&&generation===playGeneration){
    await new Promise(resolve=>setTimeout(resolve,year>=-3000?850:350));
    if(!playing||generation!==playGeneration)return;
    if(year>=PRESENT){stopPlay();return;}
    // Advance only after the previous map has finished committing to the renderer.
    await updateYear(playbackYear(year));
  }
}
$('#play').onclick=()=>{if(playing){stopPlay();return;}if(year===PRESENT)void updateYear(1900);playing=true;const generation=++playGeneration;$('#play').setAttribute('aria-pressed','true');$('#play').setAttribute('aria-label','Pausar recorrido');if($('#play').getAttribute('aria-busy')!=='true')$('#play').title='Pausar recorrido';$('#play').innerHTML=icon('pause');createIcons({icons});void play(generation);};
$('#previous').onclick=()=>{stopPlay();void updateYear(navigationYear(year,-1));};
$('#next').onclick=()=>{stopPlay();void updateYear(navigationYear(year,1));};
function projectionControl(){const label=projection==='globe'?'Ver mapa 2D':'Ver globo 3D';$('#projection-button').dataset.view=projection;$('#projection-button').setAttribute('aria-label',label);$('#projection-button').title=label;$('#projection-button').innerHTML=icon(projection==='globe'?'map':'globe-2');createIcons({icons});}
function setProjection(value:'globe'|'mercator') {projection=value;if(ready)map.setProjection({type:value});projectionControl();updateYear(year);}
$('#projection-button').onclick=()=>setProjection(projection==='globe'?'mercator':'globe');
$('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{toast('La pantalla completa no está disponible en esta ventana.');}};
document.addEventListener('fullscreenchange',()=>{const full=!!document.fullscreenElement;$('#fullscreen').innerHTML=icon(full?'minimize':'maximize');$('#fullscreen').setAttribute('aria-label',full?'Salir de pantalla completa':'Pantalla completa');$('#fullscreen').title=full?'Salir de pantalla completa':'Pantalla completa';createIcons({icons});});
function closeFilters(focus=false){$('#filters-panel').hidden=true;$('#filters-button').setAttribute('aria-expanded','false');if(focus)$('#filters-button').focus();}
function closeLayers(focus=false){$('#layers-panel').hidden=true;$('#layers-button').setAttribute('aria-expanded','false');if(focus)$('#layers-button').focus();}
function closeSources(focus=false){$('#sources-panel').hidden=true;$('#sources-button').setAttribute('aria-expanded','false');if(focus)$('#sources-button').focus();}
function closeSearch(focus=false){$('#search-panel').hidden=true;$('#search-button').setAttribute('aria-expanded','false');if(focus)$('#search-button').focus();}
$('#layers-button').onclick=()=>{const open=$('#layers-panel').hidden;$('#layers-panel').hidden=!open;$('#layers-button').setAttribute('aria-expanded',String(open));if(open){closePlanet();closeSources();closeSearch();closeFilters();$('#close-layers').focus();}};
$('#close-layers').onclick=()=>closeLayers(true);
$('#planet-button').onclick=()=>{
 if(!$('#planet-panel').hidden){closePlanet(true);return;}
 closeLayers();closeFilters();closeSources();closeSearch();
 $('#planet-panel').hidden=false;$('#planet-button').setAttribute('aria-expanded','true');renderPlanet();$('#close-planet').focus();
};
$('#close-planet').onclick=()=>closePlanet(true);
$('#chronology-colors').onclick=()=>{chronologyColored=!chronologyColored;try{localStorage.setItem('historicmap-chronology-colors',chronologyColored?'on':'off');}catch{}updateChronologyColors();};
$('#chronology-layer').onclick=()=>{chronologyVisible=!chronologyVisible;try{localStorage.setItem('historicmap-chronology-visible',chronologyVisible?'on':'off');}catch{}renderRuler();};
$('#planet-panel').addEventListener('change',event=>{const target=event.target as HTMLSelectElement;if(target.id==='planet-evidence'){planetPolicy=target.value as EvidencePolicy;renderPlanet();}});
$('#planet-panel').addEventListener('click',event=>{
 const target=event.target as Element,tab=target.closest<HTMLButtonElement>('[data-planet-tab]');
 if(tab)selectPlanetTab(tab.dataset.planetTab as PlanetTab);
 if(target.closest('#earth-optics')){earthOptics=earthOptics==='standard'?'ferruginous':'standard';applyLayers();renderPlanet();}
 const jump=target.closest<HTMLButtonElement>('[data-planet-year]');if(jump){stopPlay();void updateYear(Number(jump.dataset.planetYear));}
});
$('.planet-tabs').addEventListener('keydown',event=>{
 if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
 event.preventDefault();const tabs:PlanetTab[]=['planet','sources'];const i=event.key==='Home'?0:event.key==='End'?1:(tabs.indexOf(activePlanetTab)+1)%2;selectPlanetTab(tabs[i],true);
});
new ResizeObserver(()=>{$('.atlas').style.setProperty('--legend-height',$('#map-legend').hidden?'0px':$('#map-legend').getBoundingClientRect().height+'px');}).observe($('#map-legend'));
$('#filters-button').onclick=()=>{const open=$('#filters-panel').hidden;$('#filters-panel').hidden=!open;$('#filters-button').setAttribute('aria-expanded',String(open));if(open){closePlanet();closeSources();closeSearch();closeLayers();$('#close-filters').focus();}};
$('#close-filters').onclick=()=>closeFilters(true);
document.addEventListener('pointerdown',event=>{const target=event.target as Node;if(!(target as Element).closest('.time-dock,#modal,[data-jump-year]')&&!$('#filters-panel').hidden&&!$('#filters-panel').contains(target)&&!$('#filters-button').contains(target))closeFilters();});
document.addEventListener('pointerdown',event=>{const target=event.target as Node;if(!(target as Element).closest('.time-dock,#modal,[data-jump-year]')&&!$('#layers-panel').hidden&&!$('#layers-panel').contains(target)&&!$('#layers-button').contains(target))closeLayers();});
document.addEventListener('pointerdown',event=>{const target=event.target as Node;if(!(target as Element).closest('.time-dock,#modal,[data-jump-year]')&&!$('#sources-panel').hidden&&!$('#sources-panel').contains(target)&&!$('#sources-button').contains(target))closeSources();});
$('#human-group-select').onchange=()=>{humanFilter=$<HTMLSelectElement>('#human-group-select').value;applyLayers();refreshSearch();};
$('#ice-uncertainty').onclick=()=>{showIceUncertainty=!showIceUncertainty;applyLayers();void refreshMap();};
$('#ice-layer').onclick=()=>{iceMode=deepSceneAt(year)?(iceMode==='off'?'auto':'off'):iceEnabledFor(year,iceMode)?'off':'on';applyLayers();void refreshMap();};
$('#ice-mode').onchange=()=>{iceMode=$<HTMLSelectElement>('#ice-mode').value as IceMode;applyLayers();void refreshMap();};
$('#physical-layer').onclick=()=>{physical=!physical;applyLayers();updateSources();};$('#places-layer').onclick=()=>{showPlaces=!showPlaces;applyLayers();};
app.addEventListener('click',event=>{const button=(event.target as Element).closest<HTMLButtonElement>('[data-visibility]');if(!button||button.disabled)return;if(button.dataset.visibility==='political')political=!political;else if(button.dataset.visibility==='human-ranges')showHumanRanges=!showHumanRanges;else showRegional=!showRegional;applyLayers();renderSelection();refreshSearch();});
$('#occupations-layer').onclick=()=>{showOccupations=!showOccupations;applyLayers();};
$('#theme-select').onchange=()=>{stopPlay();political=true;theme=$<HTMLSelectElement>('#theme-select').value as Theme;affiliation='';$<HTMLSelectElement>('#affiliation-select').value='';void refreshMap();};
$('#government-select').onchange=()=>{stopPlay();governmentFilter=$<HTMLSelectElement>('#government-select').value;applyLayers();refreshSearch();updateSources();};
app.addEventListener('click',e=>{const b=(e.target as Element).closest<HTMLElement>('button[data-government-filter]');if(!b)return;governmentFilter=b.dataset.governmentFilter??'';political=true;$<HTMLSelectElement>('#government-select').value=governmentFilter;applyLayers();refreshSearch();});
$('#affiliation-select').onchange=()=>{stopPlay();affiliation=$<HTMLSelectElement>('#affiliation-select').value as AffiliationKind|'';political=true;theme='political';$<HTMLSelectElement>('#theme-select').value=theme;applyLayers();updateSources();};
function activateCountryTab(tab:HTMLElement,focus=false){
  const changed=activeCountryTab!==tab.id.replace('tab-','');
  activeCountryTab=tab.id.replace('tab-','');
  const parent=$('#selection-text');
  parent.querySelectorAll<HTMLElement>('[role=tab]').forEach(t=>{const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;});
  parent.querySelectorAll<HTMLElement>('[role=tabpanel]').forEach(p=>p.hidden=p.id!==tab.getAttribute('aria-controls'));
  if(changed){const content=parent.querySelector('.country-content');if(content)content.scrollTop=0;}
  if(focus)tab.focus({preventScroll:true});
}
function jumpFromControl(control:Element){
 const y=Number(control.getAttribute('data-jump-year'));if(!Number.isInteger(y)||y===0)return;
 const key=control.getAttribute('data-entity-key');
 if(key)void navigateEntity(key,control.getAttribute('data-entity-name')??key,y);else{stopPlay();void updateYear(y);}
}
$('#selection-text').addEventListener('click',e=>{
 const target=e.target as HTMLElement,tab=target.closest<HTMLElement>('[role=tab]');
 if(tab){activateCountryTab(tab);if(activeCountryTab==='comparison')void renderComparison();return;}
 const jump=target.closest('[data-jump-year]');if(jump){e.preventDefault();jumpFromControl(jump);return;}
 const open=target.closest<HTMLElement>('[data-open-country-tab]');if(open){const t=document.getElementById('tab-'+open.dataset.openCountryTab);if(t){activateCountryTab(t,true);void renderComparison();}return;}
 if(target.closest('#pin-country')&&selectedAnchor){
  const index=comparison.pinned.findIndex(a=>anchorId(a)===anchorId(selectedAnchor!));
  if(index<0){if(comparison.pinned.length===4){toast('La comparación admite cuatro entidades. Quita una para fijar otra.');return;}comparison.pinned.push({...selectedAnchor});}
  comparison.mode='countries';activeCountryTab='comparison';renderSelection();return;
 }
 const mode=target.closest<HTMLElement>('[data-comparison-mode]');if(mode){comparison.mode=mode.dataset.comparisonMode as ComparisonState['mode'];void renderComparison();return;}
 const unpin=target.closest<HTMLElement>('[data-unpin-country]');if(unpin){comparison.pinned.splice(Number(unpin.dataset.unpinCountry),1);void renderComparison();return;}
 if(target.closest('#clear-comparison')){comparison.pinned=[];void renderComparison();return;}
 if(target.closest('#timeline-expand')){timelineExpanded=true;renderSelection();return;}
 const organization=target.closest<HTMLElement>('[data-map-affiliation]');
 if(organization){const id=organization.dataset.mapAffiliation!;if(!affiliationsAvailable(year)||!AFFILIATIONS[id])return;affiliation=id;political=true;theme='political';$<HTMLSelectElement>('#affiliation-select').value=id;$<HTMLSelectElement>('#theme-select').value=theme;applyLayers();updateSources();}
});
$('#selection-text').addEventListener('change',e=>{
 const target=e.target as HTMLInputElement;
 if(target.id==='timeline-filter'){timelineFilter=target.value;timelineExpanded=false;renderSelection();$('#timeline-filter').focus({preventScroll:true});}
 if(target.id==='timeline-future'){timelineFuture=target.checked;renderSelection();$('#timeline-future').focus({preventScroll:true});}
 if(target.dataset.trendSection){trendSelections[target.dataset.trendSection]=target.value;const section=target.dataset.trendSection;renderSelection();document.querySelector<HTMLElement>(`[data-trend-section="${section}"]`)?.focus({preventScroll:true});}
 if(target.id==='comparison-metric'){comparison.metric=target.value;void renderComparison();}
});
$('#selection-text').addEventListener('input',e=>{const input=e.target as HTMLInputElement;if(input.id==='comparison-a'||input.id==='comparison-b')input.setCustomValidity('');});
$('#selection-text').addEventListener('submit',e=>{
 if((e.target as HTMLElement).id!=='comparison-dates')return;e.preventDefault();
 const a=Number($<HTMLInputElement>('#comparison-a').value),b=Number($<HTMLInputElement>('#comparison-b').value);
 if(![a,b].every(y=>Number.isInteger(y)&&y>=PREHISTORY_START&&y<=PRESENT&&y!==0)){const input=$<HTMLInputElement>(a===0?'#comparison-a':'#comparison-b');input.setCustomValidity('Introduce un año distinto de cero dentro del intervalo disponible.');input.reportValidity();return;}
 comparison.a=a;comparison.b=b;void renderComparison();
});
$('#selection-text').addEventListener('keydown',e=>{
  const jump=(e.target as Element).closest('circle[data-jump-year]');if(jump&&(e.key==='Enter'||e.key===' ')){e.preventDefault();jumpFromControl(jump);return;}
  const tab=(e.target as HTMLElement).closest<HTMLElement>('[role=tab]');if(!tab)return;
  const tabs=Array.from($('#selection-text').querySelectorAll<HTMLElement>('[role=tab]')),index=tabs.indexOf(tab);
  const next=e.key==='ArrowRight'?(index+1)%tabs.length:e.key==='ArrowLeft'?(index+tabs.length-1)%tabs.length:e.key==='Home'?0:e.key==='End'?tabs.length-1:-1;
  if(next>=0){e.preventDefault();activateCountryTab(tabs[next],true);}
});
$('#close-selection').onclick=closeSelection;
$('#retry').onclick=()=>void refreshMap(true);

const modal=$<HTMLDialogElement>('#modal');
function openModal(label:string,html:string,kind=''){stopPlay();if(label!=='IR A UNA FECHA'){closeLayers();closeFilters();closeSources();closeSearch();}modal.className=kind;$('#modal-label').textContent=label;$('#modal-body').innerHTML=html;modal.showModal();createIcons({icons});}
$('#close-modal').onclick=()=>modal.close();modal.addEventListener('click',e=>{if(e.target===modal){const r=modal.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)modal.close();}});
$('#date-button').setAttribute('aria-haspopup','dialog');
$('#date-button').setAttribute('aria-expanded','false');
modal.addEventListener('close',()=>$('#date-button').setAttribute('aria-expanded','false'));
$('#date-button').onclick=()=>{
 openModal('IR A UNA FECHA',`<form id="date-form"><label class="date-label" for="date-input">Año (negativo para a. C.)</label><div class="date-entry"><input id="date-input" aria-describedby="date-hint" type="number" min="${anchors[0]}" max="${PRESENT}" value="${year}" required step="1"><button class="primary-button" aria-label="Explorar fecha" type="submit">${icon('arrow-right')}</button></div><small id="date-hint">Negativo para a. C. · Sin año cero</small></form>`,'date-picker');
 $('#date-button').setAttribute('aria-expanded','true');
 const input=$<HTMLInputElement>('#date-input');input.focus();input.select();
 $('#date-form').onsubmit=e=>{e.preventDefault();const n=Number(input.value);if(!Number.isInteger(n)||n===0){input.setCustomValidity('Introduce un año entero distinto de cero.');input.reportValidity();return;}updateYear(n);modal.close();};
 input.oninput=()=>input.setCustomValidity('');
};
$('#search-button').onclick=()=>{
  if(!$('#search-panel').hidden){closeSearch(true);return;}
  stopPlay();closePlanet();closeLayers();closeFilters();closeSources();$('#search-panel').hidden=false;$('#search-button').setAttribute('aria-expanded','true');
  $<HTMLInputElement>('#search-input').value='';$('#search-scope').textContent=`Territorios visibles · ${formatYear(year)}`;
  const search=()=>{
    $('#search-scope').textContent=`Territorios visibles · ${formatYear(year)}`;
    if($('#map').getAttribute('aria-busy')==='true'){$('#search-results').textContent='Actualizando territorios…';return;}
    const q=$<HTMLInputElement>('#search-input').value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
    const matches=[...visiblePoliticalData().features,...visibleRegions().features,...(political?cityData.features.filter(f=>f.properties?.sovereignSeat):[])].filter(f=>!humanFilter||!hasHumanEvidence(year)||f.properties?.taxonGroups?.includes(humanFilter)||humanFilter==='mixed'&&f.properties?.taxonGroup==='mixed').filter(f=>!governmentFilter||f.properties?.referenceKind==='archaeological-site'||f.properties?.contextKey||(f.properties?.governmentTags??[]).includes(governmentFilter)).filter(f=>[f.properties?.name,...(f.properties?.taxa??[]),...(f.properties?.cultures??[]),...(f.properties?.cultures??[]).map(cultureLabel),...humanGroups.filter(g=>f.properties?.taxonGroups?.includes(g.id)).map(g=>g.label),f.properties?.sourceDisplayName,identityData?.countries[String(f.properties?.identityKey??f.properties?.code)]?.name,...(f.properties?.originalNames??[]),...(f.properties?.originalSiteNames??[]),f.properties?.originalName,f.properties?.controlName,profileFor(profiles,f.properties?.code||f.properties?.identityKey)?.name,f.properties?.code].filter(Boolean).join(' ').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(q)).slice(0,q?24:8);
    $('#search-results').replaceChildren();
    if(!matches.length)$('#search-results').textContent=!political&&(!showRegional||!hasRegionalCoverage(year))?'Activa la cartografía política o las áreas culturales para buscar en el mapa.':'Sin resultados en esta instantánea. Prueba otra fecha o nombre. También puedes buscar el nombre original de la fuente.';
    matches.forEach(feature=>{const button=document.createElement('button');button.textContent=displayLabel(feature.properties?.name);button.onclick=()=>{if(feature.geometry.type==='Polygon'||feature.geometry.type==='MultiPolygon'){
      const coordinates=feature.geometry.type==='Polygon'?feature.geometry.coordinates[0]:feature.geometry.coordinates.flatMap(p=>p[0]);
      const valid=coordinates.filter(c=>Number.isFinite(c[0])&&Number.isFinite(c[1]));
      if(valid.length){
        const p=feature.properties!;
        const capital=snapshot.kind==='modern'?profileFor(profiles,p.code)?.coordinates:typeof p.caplong==='number'?[p.caplong,p.caplat]:undefined;
        const lng=p.focus?.[0]??capital?.[0]??valid.reduce((sum,c)=>sum+c[0],0)/valid.length;
        const lat=p.focus?.[1]??capital?.[1]??valid.reduce((sum,c)=>sum+c[1],0)/valid.length;
        map.flyTo({center:[lng,clamp(lat,-80,80)],zoom:3.5,duration:reduced?0:1000});
      }
    }else if(feature.geometry.type==='Point'){map.flyTo({center:feature.geometry.coordinates as [number,number],zoom:5,duration:reduced?0:1000});}selectFeature(feature);closeSearch(true);};$('#search-results').append(button);});
  };refreshSearch=()=>{if(!$('#search-panel').hidden)search();};$('#search-input').oninput=search;search();$('#search-input').focus();
};
$('#close-search').onclick=()=>closeSearch(true);
$('#search-panel').addEventListener('keydown',event=>{
 if(event.key!=='ArrowDown'&&event.key!=='ArrowUp')return;
 const results=Array.from($('#search-results').querySelectorAll('button'));if(!results.length)return;
 event.preventDefault();const index=results.indexOf(document.activeElement as HTMLButtonElement);
 results[event.key==='ArrowDown'?(index+1)%results.length:(index<=0?results.length-1:index-1)].focus();
});
document.addEventListener('pointerdown',event=>{const target=event.target as Node;if(!(target as Element).closest('.time-dock,#modal,[data-jump-year]')&&!$('#search-panel').hidden&&!$('#search-panel').contains(target)&&!$('#search-button').contains(target))closeSearch();});
$('#sources-button').onclick=()=>{const open=$('#sources-panel').hidden;closePlanet();closeLayers();closeFilters();closeSearch();$('#sources-panel').hidden=!open;$('#sources-button').setAttribute('aria-expanded',String(open));if(open)$('#close-sources').focus();};
$('#close-sources').onclick=()=>closeSources(true);
$('#about-button').onclick=()=>openModal('ACERCA DE HISTORICMAP',aboutContent(VERSION,import.meta.env.BASE_URL),'about-dialog');
document.addEventListener('keydown',event=>{if(event.key==='Escape'){if(modal.open||document.querySelector<HTMLDialogElement>('#encyclopedia')?.open)return;if(!$('#planet-panel').hidden){closePlanet(true);return;}if(!$('#search-panel').hidden){closeSearch(true);return;}if(!$('#filters-panel').hidden){closeFilters(true);return;}closeSelection();if(!$('#layers-panel').hidden)closeLayers(true);if(!$('#sources-panel').hidden)closeSources(true);stopPlay();}if(event.code==='Space'&&!modal.open&&event.target===document.body){event.preventDefault();$('#play').click();}});
function restore(){const params=new URLSearchParams(location.hash.slice(1));const y=Number(params.get('year')??PRESENT);if(params.get('view')==='mercator')projection='mercator';else projection='globe';projectionControl();if(ready)map.setProjection({type:projection});updateYear(Number.isFinite(y)?y:PRESENT,false);}
window.addEventListener('hashchange',restore);restore();
