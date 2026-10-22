import * as maplibregl from 'maplibre-gl';
import { type GeoJSONSource, type ExpressionSpecification, type MapGeoJSONFeature } from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url';
import { createIcons, ArrowRight, ChevronDown, Compass, Database, ExternalLink, Globe2, Info, Layers, Map as MapIcon, MapPin, Maximize, Minimize, Mountain, Pause, Play, Search, SkipBack, SkipForward, X } from 'lucide';
import 'maplibre-gl/dist/maplibre-gl.css';
import './style.css';
import { anchors, clamp, eraName, formatYear, positionToYear, PRESENT, snapshotFor, yearToPosition, playbackYear, type Snapshot } from './time';
import { chapterFor, chapters, places } from './catalog';
import type { FeatureCollection } from 'geojson';
import packageInfo from '../package.json';
import { aboutContent } from './about';
import { annualData, asset, modernCities, overlaysFor } from './data';
import { historicalCapitals } from './history';
import { escapeHtml as esc, thematicData, thematicLegend, profileFor, type ProfileData, type Theme } from './profiles';
import { recentContext } from './recent-context';
import { sourceDiff } from './source-diff';
import { politicalData } from './political';
import { countryCard } from './country-card';
import { methodologyContent } from './methodology';
import { identityFor, type IdentityData } from './identities';

const VERSION = packageInfo.version;
const icons = { ArrowRight, ChevronDown, Compass, Database, ExternalLink, Globe2, Info, Layers, Map:MapIcon, MapPin, Maximize, Minimize, Mountain, Pause, Play, Search, SkipBack, SkipForward, X };
const $ = <T extends HTMLElement = HTMLElement>(selector: string) => document.querySelector<T>(selector)!;
const icon = (name: string) => `<i data-lucide="${name}" aria-hidden="true"></i>`;
const app = $('#app');
app.innerHTML = `
  <main class="atlas">
    <div id="map" aria-label="Mapa interactivo de la Tierra"></div>
    <div id="concept" class="concept" hidden><div class="primordial"><div class="planet"></div></div><span id="concept-caption"></span></div>
    <div class="map-shade"></div>
    <nav class="toolbar" aria-label="Herramientas del atlas">
      <button id="search-button" class="icon-button" title="Buscar un territorio" aria-label="Buscar un territorio">${icon('search')}</button>
      <button id="projection-button" class="icon-button" title="Ver mapa 2D" aria-label="Ver mapa 2D" data-view="globe">${icon('map')}</button>
      <button id="layers-button" class="icon-button" title="Capas del atlas" aria-label="Capas del atlas" aria-controls="layers-panel" aria-expanded="false">${icon('layers')}</button>
      <button id="sources-button" class="icon-button" title="Base de datos, fuentes y metodología" aria-label="Base de datos, fuentes y metodología">${icon('database')}</button>
      <button id="fullscreen" class="icon-button" title="Pantalla completa" aria-label="Pantalla completa">${icon('maximize')}</button>
      <button id="about-button" class="icon-button" title="Acerca de Historicmap" aria-label="Acerca de Historicmap">${icon('info')}</button>
    </nav>
    <aside class="story-panel" aria-label="Contexto de la época">
      <button id="chapters-button" class="chapter-trigger">${icon('compass')} Explorar épocas ${icon('chevron-down')}</button>
      <div class="story-content"><div class="eyebrow"><span class="live-dot"></span><span id="era"></span></div><h1 id="story-title"></h1><p id="story-text"></p><a id="story-source" target="_blank" rel="noopener noreferrer" class="source-link">${icon('external-link')}<span></span></a></div>
    </aside>
    <section id="layers-panel" class="layers-panel" role="dialog" aria-labelledby="layers-title" hidden>
      <div class="popover-head"><h2 id="layers-title">Capas del atlas</h2><button id="close-layers" class="icon-button" aria-label="Cerrar capas">${icon('x')}</button></div>
      <div class="layers"><button id="political-layer" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('map')}</span><span><strong>Territorios</strong><small id="territory-description">Países y fronteras</small></span><span class="layer-indicator"></span></button><button id="physical-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('mountain')}</span><span><strong>Relieve actual</strong><small>Sombreado topográfico</small></span><span class="layer-indicator"></span></button><button id="places-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('map-pin')}</span><span><strong>Capitales y grandes ciudades</strong><small>Capitales fechadas en el pasado</small></span><span class="layer-indicator"></span></button><button id="occupations-layer" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('layers')}</span><span><strong>Ocupaciones y disputas</strong><small>Control territorial y guerras civiles</small></span><span class="layer-indicator"></span></button><label class="theme-control" for="theme-select">Color del mapa<select id="theme-select"><option value="political">Territorios y dependencias</option><option value="gdp">PIB total</option><option value="gdpPerCapita">PIB por habitante</option><option value="population">Población</option></select><small id="theme-help">Indicadores del Banco Mundial desde 1960.</small></label></div>
    </section>
    <div id="selection" class="selection-card" hidden><button id="close-selection" class="icon-button" aria-label="Cerrar selección">${icon('x')}</button><span class="eyebrow" id="selection-date">EN EL MAPA</span><h2 id="selection-title"></h2><div id="selection-text"></div></div>
    <aside id="map-legend" class="map-legend" aria-label="Leyenda del mapa" hidden></aside>
    <div class="map-status"><span class="status-dot"></span><span id="map-status" role="status" aria-live="polite">Preparando cartografía…</span><button id="retry" hidden>Reintentar</button></div>
    <section class="time-dock" aria-label="Navegación temporal">
      <div id="ruler" class="ruler" role="slider" tabindex="0" aria-label="Fecha del atlas. Arrastra para desplazarte; rueda o teclas más y menos para cambiar la escala" aria-valuemin="0" aria-valuemax="1900"><div id="ruler-track"></div><div class="fixed-cursor"><div class="cursor-line"></div></div><div class="ruler-fade left"></div><div class="ruler-fade right"></div></div>
      <div class="time-focus"><button id="date-button" class="date-heading" title="Ir a una fecha"><span id="year"></span>${icon('chevron-down')}</button><div class="playback"><button id="previous" class="icon-button" aria-label="Época anterior">${icon('skip-back')}</button><button id="play" class="play-button" aria-label="Reproducir recorrido" aria-pressed="false">${icon('play')}</button><button id="next" class="icon-button" aria-label="Época siguiente">${icon('skip-forward')}</button></div></div>
      <span id="time-scale" title="Rueda sobre la regla para ampliar o reducir la escala">ESCALA ADAPTATIVA</span>
    </section>
    <dialog id="modal" aria-labelledby="modal-label"><div class="modal-head"><span id="modal-label" class="eyebrow"></span><button id="close-modal" class="icon-button" aria-label="Cerrar ventana">${icon('x')}</button></div><div id="modal-body"></div></dialog>
    <div id="toast" role="status" hidden></div>
  </main>`;
createIcons({icons});

let year = PRESENT;
let projection: 'globe' | 'mercator' = 'globe';
let spacing = 230;
let position = yearToPosition(year);
let political = true, physical = true, showPlaces = false, showOccupations = true;
let theme:Theme='political';
let ready = false, activeKey = '', requestNumber = 0;
let desiredKey='', refreshPromise:Promise<void>=Promise.resolve(), renderQueue:Promise<void>=Promise.resolve();
let profiles:ProfileData={retrieved:'',countries:{}};
let cityData:FeatureCollection={type:'FeatureCollection',features:[]}, overlayData:FeatureCollection={type:'FeatureCollection',features:[]};
let territorySignature='', citySignature='';
let referenceLandOn=false;
let committedData:FeatureCollection={type:'FeatureCollection',features:[]}, committedDomain='', overlaySignature='';
let loaded: FeatureCollection = { type:'FeatureCollection', features:[] };
const empty: FeatureCollection = { type:'FeatureCollection', features:[] };
let snapshot: Snapshot = snapshotFor(year);
let playing=false, playGeneration=0;
let identityData:IdentityData;
const colorExpression: ExpressionSpecification = ['coalesce',['get','politicalColor'],'#829c90'];
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
maplibregl.setWorkerUrl(workerUrl);
const glyphsUrl=new URL('fonts/',new URL(import.meta.env.BASE_URL,document.baseURI)).href+'{fontstack}/{range}.pbf';
const map = new maplibregl.Map({container:'map', center:[23,22], zoom:1.65, minZoom:0.2, maxZoom:7, attributionControl:{compact:true}, renderWorldCopies:false, style:{version:8, glyphs:glyphsUrl, sources:{}, layers:[{id:'ocean',type:'background',paint:{'background-color':'#17323b'}}]}, canvasContextAttributes:{antialias:true}, fadeDuration:reduced?0:200});
map.addControl(new maplibregl.ScaleControl({maxWidth:100,unit:'metric'}),'bottom-right');
map.on('load', () => {
  map.setProjection({type:projection});
  map.setSky({'sky-color':'#182c32','horizon-color':'#8fa9a3','fog-color':'#101e22','sky-horizon-blend':0.6,'horizon-fog-blend':0.6,'fog-ground-blend':0.2});
  map.addSource('reference-land',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7});
  map.addLayer({id:'reference-land',type:'fill',source:'reference-land',paint:{'fill-color':'#6c7776','fill-opacity':1}});
  // Subpixel render tolerance avoids overflowing GPU segments on dense coastlines.
  // The full-resolution source coordinates remain unchanged in public/data.
  map.addSource('territories',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7,attribution:'<a href="https://www.naturalearthdata.com/">Natural Earth</a> · <a href="https://icr.ethz.ch/data/cshapes/">CShapes · CC BY-NC-SA 4.0</a> · <a href="https://github.com/aourednik/historical-basemaps">A. Ourednik · GPL-3.0</a> · <a href="https://doi.org/10.1016/j.gsf.2024.101922">Cao et al. 2024 · CC BY 4.0</a>'});
  map.addLayer({id:'territory-fill',type:'fill',source:'territories',paint:{'fill-color':colorExpression,'fill-opacity':0.88}});
  map.addSource('dem',{type:'raster-dem',tiles:['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],tileSize:256,maxzoom:12,encoding:'terrarium',attribution:'Relieve: © Mapzen / AWS Open Data'});
  map.addLayer({id:'relief',type:'hillshade',source:'dem',layout:{visibility:'none'},paint:{'hillshade-shadow-color':'#102c2b','hillshade-highlight-color':'#fff3c8','hillshade-exaggeration':0.6}});
  map.addLayer({id:'territory-line',type:'line',source:'territories',paint:{'line-color':'#182b2b','line-width':['interpolate',['linear'],['zoom'],0,0.35,5,1.2],'line-opacity':0.85}});
  map.addLayer({id:'territory-selected',type:'line',source:'territories',filter:['==',['id'],-1],paint:{'line-color':'#f6d99c','line-width':2}});
  map.addSource('occupations',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7,attribution:'<a href="https://github.com/Seshat-Global-History-Databank/cliopatria">Cliopatria · CC BY 4.0</a> · <a href="https://commons.wikimedia.org/wiki/File:GCE-Frente_en_oct_1937.svg">Tyk / Té y kriptonita · CC BY-SA 3.0</a>'});
  map.addLayer({id:'occupation-fill',type:'fill',source:'occupations',paint:{'fill-color':['get','controlColor'],'fill-opacity':1}});
  map.addLayer({id:'occupation-line',type:'line',source:'occupations',paint:{'line-color':'#c6c8ba','line-width':0.85,'line-opacity':0.75}});
  map.addLayer({id:'territory-labels',type:'symbol',source:'territories',minzoom:2.5,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':['interpolate',['linear'],['zoom'],2,10,5,13],'text-max-width':7,'text-padding':12},paint:{'text-color':'#e5e5ce','text-halo-color':'#24413c','text-halo-width':1}});
  map.addSource('places',{type:'geojson',data:empty});
  map.addLayer({id:'place-circles',type:'circle',source:'places',minzoom:1.4,paint:{'circle-radius':['case',['==',['get','capital'],true],4,2.5],'circle-color':'#f2d394','circle-stroke-color':'#152b30','circle-stroke-width':1.5}});
  map.addLayer({id:'place-labels',type:'symbol',source:'places',minzoom:1.4,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':11,'text-offset':[0,1.1],'symbol-sort-key':['coalesce',['get','rank'],5],'text-padding':8},paint:{'text-color':'#fff1cf','text-halo-color':'#102329','text-halo-width':1.5}});
  ready = true; void refreshMap(true);
});
map.on('error',(event) => {
  if (event.error?.message?.includes('WebGL')) toast('El navegador no ha podido iniciar WebGL. Prueba con aceleración gráfica activada.');
  else if (physical) toast('No se ha podido cargar parte del relieve en línea. La cartografía local sigue disponible.');
});
map.on('webglcontextlost',()=>toast('Se ha perdido la conexión gráfica. Recarga la página para recuperar el mapa.'));
map.on('idle',()=>{
  if(loaded.features.length && map.queryRenderedFeatures({layers:['territory-fill']}).length) $('#map').dataset.rendered=activeKey;
});
map.on('click',event=>{
  if(!ready||$('#map').getAttribute('aria-busy')==='true'||$('#map').dataset.loadedYear!==String(year))return;
  const place=showPlaces?map.queryRenderedFeatures(event.point,{layers:['place-circles']})[0]:undefined;
  const occupation=showOccupations?map.queryRenderedFeatures(event.point,{layers:['occupation-fill']})[0]:undefined;
  const feature=place??occupation??map.queryRenderedFeatures(event.point,{layers:['territory-fill']})[0];
  if(feature)selectFeature(feature);
});
map.on('mouseenter','territory-fill',()=>{map.getCanvas().style.cursor='pointer';});
map.on('mouseleave','territory-fill',()=>{map.getCanvas().style.cursor='';});
function selectFeature(feature:{properties:MapGeoJSONFeature['properties']|null;id?:string|number}) {
  if($('#map').getAttribute('aria-busy')==='true'||$('#map').dataset.loadedYear!==String(year))return;
  stopPlay();
  const p=feature.properties??{};
  $('#selection').hidden=false;
  $('#selection-title').textContent=p.name;
  $('#selection-date').textContent=year>=1789?`${year} · ${snapshot.kind==='modern'?'MUNDO CONTEMPORÁNEO':'CONTEXTO HISTÓRICO'}`:formatYear(year);
  if(p.rank!==undefined&&p.country){
    $('#selection-text').innerHTML=`<p>${esc(p.capital?'Capital o sede administrativa':'Gran ciudad')} · ${esc(p.country)}</p><p>${esc(p.note??'Localización urbana de referencia contemporánea. La selección reúne capitales y grandes centros urbanos de todo el mundo.')}</p><a class="profile-source" href="${esc(p.source)}" target="_blank" rel="noopener">Fuente del lugar ↗</a>`;return;
  }
  const identity=identityFor(p,year,identityData);
  if(identity.name)$('#selection-title').textContent=identity.name;
  $('#selection-text').innerHTML=countryCard(p,year,snapshot,profiles,identityData,import.meta.env.BASE_URL);
  map.setFilter('territory-selected',['==',['id'],feature.id ?? -1]);
}
let toastTimer: ReturnType<typeof setTimeout>;
function toast(text:string){ $('#toast').textContent=text;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,6000); }
function status(text:string,error=false){$('#map-status').textContent=text;$('.status-dot').classList.toggle('error',error);$('#retry').hidden=!error;}

function refreshMap(force=false):Promise<void> {
  snapshot=snapshotFor(year);
  const target={...snapshot}, targetYear=year, targetTheme=theme;
  const displayKey=target.kind==='annual'?`history-${targetYear}`:target.file??`concept-${year < -1800000000 ? 'early':'human'}`;
  const key=`${displayKey}:${targetYear}:${theme}`;
  const concept=snapshot.kind==='concept';
  $('#concept').hidden=!concept;
  $('#map').style.visibility=concept?'hidden':'visible';
  $('#physical-layer').toggleAttribute('disabled',snapshot.kind!=='modern');
  $('#political-layer').toggleAttribute('disabled',concept);
  $('#places-layer').toggleAttribute('disabled',year < -10000);
  $('#occupations-layer').toggleAttribute('disabled',year<1789);
  $('#theme-select').toggleAttribute('disabled',year<1960||snapshot.kind==='geological');
  $('#territory-description').textContent=snapshot.kind==='geological'?'Masas continentales reconstruidas':snapshot.kind==='modern'?'Países y fronteras':snapshot.kind==='annual'?'Territorios y dependencias fechados':'Áreas políticas y culturales';
  $('#concept').classList.toggle('human-era',year > -1800000000);
  $('#concept-caption').textContent=year < -1800000000?'ESCENA CONCEPTUAL · SIN GEOMETRÍA RECONSTRUIDA':'CARTOGRAFÍA PREHISTÓRICA PENDIENTE · SIN ÁREAS HUMANAS INFERIDAS';
  if(!ready) return Promise.resolve();
  // Stop requesting contemporary elevation as soon as the requested era changes.
  map.setLayoutProperty('relief','visibility',physical&&snapshot.kind==='modern'?'visible':'none');
  if(key===desiredKey&&!force) return refreshPromise;
  const current=++requestNumber;
  const previousKind=activeKey.startsWith('coastlines-')?'geological':'other';
  desiredKey=key;
  delete $('#map').dataset.rendered;
  $('#map').setAttribute('aria-busy','true');
  $('#map').dataset.loadStage='fetch';
  $('#search-button').toggleAttribute('disabled',true);
  if(snapshot.kind==='geological'&&previousKind!=='geological')map.jumpTo({center:[0,15],zoom:1.5});
  $('#selection').hidden=true;
  if(concept){activeKey=displayKey;loaded=empty;$('#map-legend').hidden=true;$('#map').setAttribute('aria-busy','false');status('Contexto documental · sin cartografía disponible');return Promise.resolve();}
  status(`Cargando ${formatYear(target.year)}…${loaded.features.length?' · se conserva el mapa anterior':''}`);
  refreshPromise=(async()=>{
    try {
      const [rawData,profileData,points,overlays,identities,referenceLand]=await Promise.all([
        target.kind==='annual'?annualData(targetYear):asset<FeatureCollection>(target.file!),
        asset<ProfileData>('profiles.json'),
        target.kind==='modern'?modernCities():Promise.resolve(empty),
        targetYear>=1789?overlaysFor(targetYear):Promise.resolve(empty),
        asset<IdentityData>('identities.json'),
        targetYear>=1789&&targetYear<1886?asset<FeatureCollection>('countries.geojson'):Promise.resolve(empty)
      ]);
      if(current!==requestNumber)return;
      const data=politicalData(rawData,targetYear);
      const themed=thematicData(data,profileData,targetTheme,targetYear);
      const signature=target.kind==='annual'||target.kind==='modern'?data.features.map(f=>`${f.id}:${f.properties?.name}:${f.properties?.politicalColor}:${f.properties?.identityKey}`).join('|'):target.file!;
      const commit=async()=>{
        if(current!==requestNumber)return;
        $('#map').dataset.loadStage='territories';
        const referenceOn=referenceLand.features.length>0;
        if(referenceOn!==referenceLandOn){await (map.getSource('reference-land') as GeoJSONSource).setData(referenceLand);referenceLandOn=referenceOn;}
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
        const overlayKey=overlays.features.map(f=>f.properties?.uid).join('|');
        if(overlayKey!==overlaySignature){await (map.getSource('occupations') as GeoJSONSource).setData(overlays);overlaySignature=overlayKey;}
        if(current!==requestNumber)return;
        loaded=themed;profiles=profileData;identityData=identities;overlayData=overlays;activeKey=displayKey;
        // Statistics change paint only: do not re-index or tessellate coastlines for a new number.
        if(targetTheme!=='political')for(const f of themed.features)if(f.id!==undefined)map.setFeatureState({source:'territories',id:f.id},{metric:f.properties?.metric??null});
        cityData=target.kind==='modern'?points:target.kind==='annual'?historicalCapitals(data):{type:'FeatureCollection',features:places.filter(p=>targetYear>=p.start&&targetYear<=p.end).map(p=>({type:'Feature',geometry:{type:'Point',coordinates:p.coordinates},properties:{name:p.name,note:p.description,country:'Yacimiento / ciudad histórica',rank:1}}))};
        applyLayers();
        $('#map').dataset.loadedYear=String(targetYear);
        $('#map').setAttribute('aria-busy','false');
        $('#search-button').toggleAttribute('disabled',false);
        $('#map').dataset.loadStage='ready';
        const label=target.kind==='modern'?`Natural Earth · referencia contemporánea 2026${targetYear!==2026?` · consulta ${targetYear}`:''}`:target.kind==='annual'?`${targetYear<1886?'Cliopatria · síntesis anual':'CShapes · 31 dic'} ${targetYear} · ${data.features.length} territorios`:`${target.kind==='geological'?'CAO2024 · reconstrucción':'Fronteras aproximadas'} · ${formatYear(target.year)}`;
        status(label);
        // Idle may have fired while committing overlays; rendered means the active source is visible.
        if(map.queryRenderedFeatures({layers:['territory-fill']}).length)$('#map').dataset.rendered=activeKey;
      };
      renderQueue=renderQueue.then(commit,commit);await renderQueue;
    } catch {
      if(current!==requestNumber)return;
      desiredKey='';$('#map').setAttribute('aria-busy','false');status('No se ha podido cargar la fecha. Se conserva el mapa anterior.',true);stopPlay();
    }
  })();
  return refreshPromise;
}
function applyLayers(){
  $('#political-layer').classList.toggle('active',political);$('#political-layer').setAttribute('aria-pressed',String(political));
  $('#physical-layer').classList.toggle('active',physical&&snapshot.kind==='modern');$('#physical-layer').setAttribute('aria-pressed',String(physical&&snapshot.kind==='modern'));
  $('#places-layer').classList.toggle('active',showPlaces);$('#places-layer').setAttribute('aria-pressed',String(showPlaces));
  $('#occupations-layer').classList.toggle('active',showOccupations);$('#occupations-layer').setAttribute('aria-pressed',String(showOccupations));
  if(!ready)return;
  const thresholds=theme==='gdp'?[1e10,1e11,1e12,1e13]:theme==='population'?[1e6,1e7,1e8,1e9]:[1000,5000,15000,50000];
  const thematic:ExpressionSpecification=['case',['==',['feature-state','metric'],null],'#6c7776',['interpolate',['linear'],['coalesce',['feature-state','metric'],0],0,'#294b52',thresholds[0],'#3d777b',thresholds[1],'#8ab29c',thresholds[2],'#dac48a',thresholds[3],'#d98355']];
  map.setPaintProperty('territory-fill','fill-color',political?(theme==='political'?colorExpression:thematic):'#819c88');
  map.setLayoutProperty('territory-line','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  map.setPaintProperty('territory-fill','fill-opacity',snapshot.kind==='geological'||theme==='political'?1:0.88);
  map.setPaintProperty('territory-fill','fill-antialias',snapshot.kind!=='geological');
  map.setLayoutProperty('territory-labels','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  map.setLayoutProperty('relief','visibility',physical&&snapshot.kind==='modern'?'visible':'none');
  for(const id of ['occupation-fill','occupation-line'])map.setLayoutProperty(id,'visibility',showOccupations&&year>=1789?'visible':'none');
  const nextCitySignature=showPlaces?JSON.stringify(cityData):'';
  if(nextCitySignature!==citySignature){citySignature=nextCitySignature;void (map.getSource('places') as GeoJSONSource).setData(showPlaces?cityData:empty);}
  $('#map').dataset.places=String(showPlaces?cityData.features.length:0);
  $('#map').dataset.overlays=String(showOccupations?overlayData.features.length:0);
  const controls=[...new Map(overlayData.features.map(f=>[f.properties!.controller,f.properties!])).values()];
  const labels:Record<string,string>={DEU:'Alemania',JPN:'Japón',ITA:'Italia',USSR:'URSS','CROATIA-CLIENT':'Croacia · cliente','FRA-VICHY':'Vichy · colaboracionista','CHN-COMMUNIST':'China · comunistas','ESP-REPUBLIC':'España · republicanos','ESP-NATIONALIST':'España · sublevados',RUS:'Rusia',ISR:'Israel','AUT-HUN':'Austria-Hungría',OTT:'Imperio otomano'};
  const controlLegend=showOccupations&&controls.length?`<div class="control-legend"><strong>Control territorial · síntesis anual</strong><div class="control-swatches">${controls.map(p=>`<span><i style="background:${p.controlColor}"></i>${esc(labels[p.controller]??p.name)}</span>`).join('')}</div><small>Colores sólidos por potencia o bando.<br>Aliados: identidad propia. Dependientes: tono claro.<br>Fecha y fuentes en cada ficha.</small></div>`:'';
  $('#map-legend').innerHTML=(political?thematicLegend(loaded,theme):'')+controlLegend+(year>=1789&&year<1886?'<small>Gris: sin entidad en el inventario histórico.<br>Fondo costero de referencia contemporánea.</small>':'');
  $('#map-legend').hidden=!$('#map-legend').innerHTML;
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
  const chapter=recentContext(year)??chapterFor(year);
  $('#year').textContent=formatYear(year);$('#era').textContent=eraName(year);
  $('#story-title').textContent=chapter.title;$('#story-text').textContent=chapter.text;
  $('#story-source span').textContent=chapter.sourceLabel;($('#story-source') as HTMLAnchorElement).href=chapter.source;
  renderRuler(); const refreshed=refreshMap();
  if(save)persistLocation();
  return refreshed;
}
let rulerKey='';
function renderRuler(){
  const track=$('#ruler-track');
  const width=$('#ruler').clientWidth;
  const key=`${spacing}:${Math.floor(position*spacing/120)}:${width}`;
  if(rulerKey!==key){
    rulerKey=key;
    const fragment=document.createDocumentFragment();
    const left=position-(width/2+240)/spacing, right=position+(width/2+240)/spacing;
    const tick=(y:number,major:boolean)=>{
      if(y===0)return;
      const p=yearToPosition(y);
      if(p<left||p>right)return;
      const element=document.createElement('div');element.className=`tick ${major?'major':'minor'}`;element.style.left=`${p*spacing}px`;
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
    track.replaceChildren(fragment);
  }
  track.style.transform=`translateX(${width/2-position*spacing}px)`;
  $('#ruler').dataset.scale=String(spacing);
  $('#ruler').setAttribute('aria-valuenow',String(Math.round(position*100)));
  $('#ruler').setAttribute('aria-valuetext',`${formatYear(year)}, ${eraName(year)}`);
}
let startX=0,startPosition=0,dragging=false;
const ruler=$('#ruler');
ruler.addEventListener('pointerdown',event=>{stopPlay();dragging=true;startX=event.clientX;startPosition=position;ruler.setPointerCapture(event.pointerId);ruler.classList.add('dragging');});
ruler.addEventListener('pointermove',event=>{if(dragging)updateYear(positionToYear(startPosition-(event.clientX-startX)/spacing));});
for(const type of ['pointerup','pointercancel'])ruler.addEventListener(type,()=>{dragging=false;ruler.classList.remove('dragging');});
function zoomRuler(factor:number){stopPlay();spacing=clamp(Math.round(spacing*factor),96,4800);if(dragging){dragging=false;ruler.classList.remove('dragging');}renderRuler();}
$('.time-dock').addEventListener('wheel',event=>{event.preventDefault();event.stopPropagation();const units=event.deltaMode===1?16:event.deltaMode===2?ruler.clientHeight:1;zoomRuler(Math.exp(-clamp((event.deltaY||event.deltaX)*units,-240,240)*.0025));},{passive:false});
ruler.addEventListener('keydown',event=>{const keys:Record<string,number>={ArrowLeft:-24/spacing,ArrowRight:24/spacing,PageUp:-ruler.clientWidth*.8/spacing,PageDown:ruler.clientWidth*.8/spacing};if(event.key in keys){event.preventDefault();stopPlay();updateYear(positionToYear(position+keys[event.key]));}else if(event.key==='Home'){event.preventDefault();stopPlay();updateYear(anchors[0]);}else if(event.key==='End'){event.preventDefault();stopPlay();updateYear(PRESENT);}else if(['+','=','-','_'].includes(event.key)){event.preventDefault();zoomRuler(['+','='].includes(event.key)?1.25:1/1.25);}});
new ResizeObserver(renderRuler).observe(ruler);
function stopPlay(){playing=false;playGeneration++;$('#play').setAttribute('aria-pressed','false');$('#play').setAttribute('aria-label','Reproducir recorrido');$('#play').innerHTML=icon('play');createIcons({icons});}
async function play(generation:number){
  await refreshMap();
  while(playing&&generation===playGeneration){
    await new Promise(resolve=>setTimeout(resolve,year>=1789?850:350));
    if(!playing||generation!==playGeneration)return;
    if(year>=PRESENT){stopPlay();return;}
    // Advance only after the previous map has finished committing to the renderer.
    await updateYear(playbackYear(year));
  }
}
$('#play').onclick=()=>{if(playing){stopPlay();return;}if(year===PRESENT)void updateYear(1900);playing=true;const generation=++playGeneration;$('#play').setAttribute('aria-pressed','true');$('#play').setAttribute('aria-label','Pausar recorrido');$('#play').innerHTML=icon('pause');createIcons({icons});void play(generation);};
$('#previous').onclick=()=>{stopPlay();void updateYear(year>=1789?year-1:anchors[Math.max(0,Math.ceil(position)-1)]);};
$('#next').onclick=()=>{stopPlay();void updateYear(year>=1789?Math.min(PRESENT,year+1):anchors[Math.min(anchors.length-1,Math.floor(position)+1)]);};
function projectionControl(){const label=projection==='globe'?'Ver mapa 2D':'Ver globo 3D';$('#projection-button').dataset.view=projection;$('#projection-button').setAttribute('aria-label',label);$('#projection-button').title=label;$('#projection-button').innerHTML=icon(projection==='globe'?'map':'globe-2');createIcons({icons});}
function setProjection(value:'globe'|'mercator') {projection=value;if(ready)map.setProjection({type:value});projectionControl();updateYear(year);}
$('#projection-button').onclick=()=>setProjection(projection==='globe'?'mercator':'globe');
$('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{toast('La pantalla completa no está disponible en esta ventana.');}};
document.addEventListener('fullscreenchange',()=>{const full=!!document.fullscreenElement;$('#fullscreen').innerHTML=icon(full?'minimize':'maximize');$('#fullscreen').setAttribute('aria-label',full?'Salir de pantalla completa':'Pantalla completa');$('#fullscreen').title=full?'Salir de pantalla completa':'Pantalla completa';createIcons({icons});});
function closeLayers(focus=false){$('#layers-panel').hidden=true;$('#layers-button').setAttribute('aria-expanded','false');if(focus)$('#layers-button').focus();}
$('#layers-button').onclick=()=>{const open=$('#layers-panel').hidden;$('#layers-panel').hidden=!open;$('#layers-button').setAttribute('aria-expanded',String(open));if(open)$('#close-layers').focus();};
$('#close-layers').onclick=()=>closeLayers(true);
document.addEventListener('pointerdown',event=>{const target=event.target as Node;if(!$('#layers-panel').hidden&&!$('#layers-panel').contains(target)&&!$('#layers-button').contains(target))closeLayers();});
$('#political-layer').onclick=()=>{political=!political;applyLayers();};$('#physical-layer').onclick=()=>{physical=!physical;applyLayers();};$('#places-layer').onclick=()=>{showPlaces=!showPlaces;applyLayers();};
$('#occupations-layer').onclick=()=>{showOccupations=!showOccupations;applyLayers();};
$('#theme-select').onchange=()=>{stopPlay();political=true;theme=$<HTMLSelectElement>('#theme-select').value as Theme;void refreshMap(true);};
$('#close-selection').onclick=()=>{$('#selection').hidden=true;if(ready)map.setFilter('territory-selected',['==',['id'],-1]);};
$('#retry').onclick=()=>void refreshMap(true);

const modal=$<HTMLDialogElement>('#modal');
function openModal(label:string,html:string,kind=''){stopPlay();closeLayers();modal.className=kind;$('#modal-label').textContent=label;$('#modal-body').innerHTML=html;modal.showModal();createIcons({icons});}
$('#close-modal').onclick=()=>modal.close();modal.addEventListener('click',e=>{if(e.target===modal){const r=modal.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)modal.close();}});
$('#chapters-button').onclick=()=>{
  openModal('EXPLORAR ÉPOCAS','<h2>Una Tierra. Toda su historia.</h2><p class="modal-intro">Elige un punto de partida y continúa tu viaje con la regla temporal.</p><div class="chapters-grid"></div>');
  chapters.forEach(chapter=>{const button=document.createElement('button');button.className='chapter-card';const small=document.createElement('small');small.textContent=formatYear(chapter.year);const strong=document.createElement('strong');strong.textContent=chapter.label;button.append(small,strong);button.onclick=()=>{updateYear(chapter.year);modal.close();};$('.chapters-grid').append(button);});
};
$('#date-button').onclick=()=>{openModal('IR A UNA FECHA',`<h2>Encuentra tu momento.</h2><form id="date-form"><label for="date-input">Año (negativo para a. C.)</label><input id="date-input" type="number" min="${anchors[0]}" max="${PRESENT}" value="${year}" required step="1"><p class="modal-intro">Por ejemplo: −3000, 100 o −200000000. Ga = miles de millones de años; Ma = millones de años. El año cero no se utiliza.</p><button class="primary-button" type="submit">Explorar fecha ${icon('arrow-right')}</button></form>`);$('#date-form').onsubmit=e=>{e.preventDefault();const n=Number($<HTMLInputElement>('#date-input').value);if(!Number.isFinite(n)||n===0){$<HTMLInputElement>('#date-input').setCustomValidity('Introduce un año distinto de cero.');$<HTMLInputElement>('#date-input').reportValidity();return;}updateYear(n);modal.close();};$('#date-input').oninput=()=> $<HTMLInputElement>('#date-input').setCustomValidity('');};
$('#search-button').onclick=()=>{
  openModal('BUSCAR EN ESTA INSTANTÁNEA','<h2>Todo lugar tiene una historia.</h2><label for="search-input">Nombre del territorio</label><input id="search-input" type="search" placeholder="España, Rome, Han…" autocomplete="off"><div id="search-results" class="search-results"></div>');
  const search=()=>{
    const q=$<HTMLInputElement>('#search-input').value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
    const matches=[...loaded.features,...(showOccupations?overlayData.features:[])].filter(f=>String(f.properties?.name).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(q)).slice(0,30);
    $('#search-results').replaceChildren();
    if(!matches.length)$('#search-results').textContent='Sin resultados en esta instantánea. Prueba otra fecha o nombre. Los nombres históricos conservan el idioma de la fuente.';
    matches.forEach(feature=>{const button=document.createElement('button');button.textContent=String(feature.properties?.name);button.onclick=()=>{if(feature.geometry.type==='Polygon'||feature.geometry.type==='MultiPolygon'){
      const coordinates=feature.geometry.type==='Polygon'?feature.geometry.coordinates[0]:feature.geometry.coordinates.flatMap(p=>p[0]);
      const valid=coordinates.filter(c=>Number.isFinite(c[0])&&Number.isFinite(c[1]));
      if(valid.length){
        const p=feature.properties!;
        const capital=snapshot.kind==='modern'?profileFor(profiles,p.code)?.coordinates:typeof p.caplong==='number'?[p.caplong,p.caplat]:undefined;
        const lng=capital?.[0]??valid.reduce((sum,c)=>sum+c[0],0)/valid.length;
        const lat=capital?.[1]??valid.reduce((sum,c)=>sum+c[1],0)/valid.length;
        map.flyTo({center:[lng,clamp(lat,-80,80)],zoom:3.5,duration:reduced?0:1000});
      }
    }selectFeature(feature);modal.close();};$('#search-results').append(button);});
  };$('#search-input').oninput=search;search();
};
function sources(){openModal('FUENTES Y METODOLOGÍA',methodologyContent);}
$('#sources-button').onclick=sources;
$('#about-button').onclick=()=>openModal('ACERCA DE HISTORICMAP',aboutContent(VERSION,import.meta.env.BASE_URL),'about-dialog');
document.addEventListener('keydown',event=>{if(event.key==='Escape'){$('#selection').hidden=true;if(!$('#layers-panel').hidden)closeLayers(true);stopPlay();}if(event.code==='Space'&&!modal.open&&event.target===document.body){event.preventDefault();$('#play').click();}});
function restore(){const params=new URLSearchParams(location.hash.slice(1));const y=Number(params.get('year')??PRESENT);if(params.get('view')==='mercator')projection='mercator';else projection='globe';projectionControl();if(ready)map.setProjection({type:projection});updateYear(Number.isFinite(y)?y:PRESENT,false);}
window.addEventListener('hashchange',restore);restore();
