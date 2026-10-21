import * as maplibregl from 'maplibre-gl';
import { type GeoJSONSource, type ExpressionSpecification, type MapGeoJSONFeature } from 'maplibre-gl';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url';
import { createIcons, ArrowRight, ChevronDown, Compass, Database, ExternalLink, Globe2, Info, Layers, Map as MapIcon, MapPin, Maximize, Minimize, Mountain, Pause, Play, Search, SkipBack, SkipForward, X } from 'lucide';
import 'maplibre-gl/dist/maplibre-gl.css';
import './style.css';
import { anchors, clamp, eraName, formatYear, positionToYear, PRESENT, snapshotFor, yearToPosition, type Snapshot } from './time';
import { chapterFor, chapters, places } from './catalog';
import type { FeatureCollection } from 'geojson';
import packageInfo from '../package.json';
import { aboutContent } from './about';

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
      <div class="layers"><button id="political-layer" class="layer-button active" aria-pressed="true"><span class="layer-icon">${icon('map')}</span><span><strong>Territorios</strong><small id="territory-description">Países y fronteras</small></span><span class="layer-indicator"></span></button><button id="physical-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('mountain')}</span><span><strong>Relieve actual</strong><small>Sombreado topográfico</small></span><span class="layer-indicator"></span></button><button id="places-layer" class="layer-button" aria-pressed="false"><span class="layer-icon">${icon('map-pin')}</span><span><strong>Lugares de referencia</strong><small>Selección introductoria</small></span><span class="layer-indicator"></span></button></div>
    </section>
    <div id="selection" class="selection-card" hidden><button id="close-selection" class="icon-button" aria-label="Cerrar selección">${icon('x')}</button><span class="eyebrow">EN EL MAPA</span><h2 id="selection-title"></h2><p id="selection-text"></p></div>
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
let political = true, physical = true, showPlaces = false;
let ready = false, activeKey = '', requestNumber = 0;
let abort: AbortController | undefined;
let loaded: FeatureCollection = { type:'FeatureCollection', features:[] };
const empty: FeatureCollection = { type:'FeatureCollection', features:[] };
let snapshot: Snapshot = snapshotFor(year);
let playFrame = 0, lastFrame = 0;
const palette = ['#78938a','#af9c77','#658e98','#9c887a','#9ba783','#b39c80','#7b929d','#a6a386','#8f9c8d','#9e8883','#819c9f','#b5a48a'];
const colorExpression: ExpressionSpecification = ['match', ['get','color'], 0,palette[0],1,palette[1],2,palette[2],3,palette[3],4,palette[4],5,palette[5],6,palette[6],7,palette[7],8,palette[8],9,palette[9],10,palette[10],11,palette[11], '#829c90'];
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
maplibregl.setWorkerUrl(workerUrl);
const map = new maplibregl.Map({container:'map', center:[23,22], zoom:1.65, minZoom:0.2, maxZoom:7, attributionControl:{compact:true}, renderWorldCopies:false, style:{version:8, glyphs:'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf', sources:{}, layers:[{id:'ocean',type:'background',paint:{'background-color':'#17323b'}}]}, canvasContextAttributes:{antialias:true}, fadeDuration:reduced?0:200});
map.addControl(new maplibregl.ScaleControl({maxWidth:100,unit:'metric'}),'bottom-right');
map.on('load', () => {
  map.setProjection({type:projection});
  map.setSky({'sky-color':'#182c32','horizon-color':'#8fa9a3','fog-color':'#101e22','sky-horizon-blend':0.6,'horizon-fog-blend':0.6,'fog-ground-blend':0.2});
  // Subpixel render tolerance avoids overflowing GPU segments on dense coastlines.
  // The full-resolution source coordinates remain unchanged in public/data.
  map.addSource('territories',{type:'geojson',data:empty,tolerance:0.2,maxzoom:7,generateId:true,attribution:'<a href="https://www.naturalearthdata.com/">Natural Earth</a> · <a href="https://github.com/aourednik/historical-basemaps">A. Ourednik · GPL-3.0</a> · <a href="https://doi.org/10.1016/j.gsf.2024.101922">Cao et al. 2024 · CC BY 4.0</a>'});
  map.addLayer({id:'territory-fill',type:'fill',source:'territories',paint:{'fill-color':colorExpression,'fill-opacity':0.88}});
  map.addSource('dem',{type:'raster-dem',tiles:['https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'],tileSize:256,maxzoom:12,encoding:'terrarium',attribution:'Relieve: © Mapzen / AWS Open Data'});
  map.addLayer({id:'relief',type:'hillshade',source:'dem',layout:{visibility:'none'},paint:{'hillshade-shadow-color':'#102c2b','hillshade-highlight-color':'#fff3c8','hillshade-exaggeration':0.6}});
  map.addLayer({id:'territory-line',type:'line',source:'territories',paint:{'line-color':'#182b2b','line-width':['interpolate',['linear'],['zoom'],0,0.35,5,1.2],'line-opacity':0.85}});
  map.addLayer({id:'territory-selected',type:'line',source:'territories',filter:['==',['id'],-1],paint:{'line-color':'#f6d99c','line-width':2}});
  map.addLayer({id:'territory-labels',type:'symbol',source:'territories',minzoom:2.5,layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':['interpolate',['linear'],['zoom'],2,10,5,13],'text-max-width':7,'text-padding':12},paint:{'text-color':'#e5e5ce','text-halo-color':'#24413c','text-halo-width':1}});
  map.addSource('places',{type:'geojson',data:empty});
  map.addLayer({id:'place-circles',type:'circle',source:'places',paint:{'circle-radius':5,'circle-color':'#f2d394','circle-stroke-color':'#152b30','circle-stroke-width':2}});
  map.addLayer({id:'place-labels',type:'symbol',source:'places',layout:{'text-field':['get','name'],'text-font':['Noto Sans Regular'],'text-size':12,'text-offset':[0,1.4]},paint:{'text-color':'#fff1cf','text-halo-color':'#102329','text-halo-width':1.5}});
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
map.on('click','territory-fill',event=>{const feature=event.features?.[0];if(feature) selectFeature(feature);});
map.on('mouseenter','territory-fill',()=>{map.getCanvas().style.cursor='pointer';});
map.on('mouseleave','territory-fill',()=>{map.getCanvas().style.cursor='';});
map.on('click','place-circles',event=>{
  const p=event.features?.[0]?.properties;
  const place=places.find(v=>v.name===p?.name);
  if(!place) return;
  $('#selection').hidden=false;
  $('#selection-title').textContent=place.name;
  $('#selection-text').textContent=place.description;
});

function selectFeature(feature: MapGeoJSONFeature) {
  $('#selection').hidden=false;
  $('#selection-title').textContent=feature.properties.name;
  const precision=feature.properties.precision;
  $('#selection-text').textContent=snapshot.kind==='modern'?'Geometría de Natural Earth, escala 1:10 millones. La representación no resuelve disputas territoriales ni acredita vigencia diaria.':`Instantánea: ${formatYear(snapshot.year)}. ${snapshot.kind==='geological'?'Reconstrucción tectónica CAO2024; no es una costa observada.':`Área histórica o cultural. Precisión de origen: ${precision ? `${precision}/3` : 'sin clasificar'}. Requiere contraste historiográfico.`}`;
  map.setFilter('territory-selected',['==',['id'],feature.id ?? -1]);
}
let toastTimer: ReturnType<typeof setTimeout>;
function toast(text:string){ $('#toast').textContent=text;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,6000); }
function status(text:string,error=false){$('#map-status').textContent=text;$('.status-dot').classList.toggle('error',error);$('#retry').hidden=!error;}

async function refreshMap(force=false) {
  snapshot=snapshotFor(year);
  const key=snapshot.file ?? `concept-${year < -1800000000 ? 'early':'human'}`;
  const concept=snapshot.kind==='concept';
  $('#concept').hidden=!concept;
  $('#map').style.visibility=concept?'hidden':'visible';
  $('#physical-layer').toggleAttribute('disabled',snapshot.kind!=='modern');
  $('#political-layer').toggleAttribute('disabled',concept);
  $('#places-layer').toggleAttribute('disabled',year < -10000);
  $('#territory-description').textContent=snapshot.kind==='geological'?'Masas continentales reconstruidas':snapshot.kind==='modern'?'Países y fronteras':'Áreas políticas y culturales';
  $('#concept').classList.toggle('human-era',year > -1800000000);
  $('#concept-caption').textContent=year < -1800000000?'ESCENA CONCEPTUAL · SIN GEOMETRÍA RECONSTRUIDA':'CARTOGRAFÍA PREHISTÓRICA PENDIENTE · SIN ÁREAS HUMANAS INFERIDAS';
  applyLayers();
  if(!ready) return;
  if(key===activeKey&&!force) return;
  const current=++requestNumber;
  const previousKind=activeKey.startsWith('coastlines-')?'geological':'other';
  activeKey=key;
  delete $('#map').dataset.rendered;
  if(snapshot.kind==='geological'&&previousKind!=='geological')map.jumpTo({center:[0,15],zoom:1.5});
  abort?.abort();
  (map.getSource('territories') as GeoJSONSource).setData(empty);
  loaded=empty;
  $('#selection').hidden=true;
  if(concept){status('Contexto documental · sin cartografía disponible');return;}
  status(`Cargando instantánea de ${formatYear(snapshot.year)}…`);
  abort=new AbortController();
  try {
    const response=await fetch(`${import.meta.env.BASE_URL}data/${snapshot.file}`,{signal:abort.signal});
    if(!response.ok) throw new Error(String(response.status));
    const data:FeatureCollection=await response.json();
    if(current!==requestNumber) return;
    await (map.getSource('territories') as GeoJSONSource).setData(data);
    if(current!==requestNumber) return;
    loaded=data;
    const label=snapshot.kind==='modern'?'Natural Earth · 1:10m · referencia contemporánea':`${snapshot.kind==='geological'?'CAO2024 · reconstrucción':'Fronteras aproximadas'} · ${formatYear(snapshot.year)}`;
    status(label);
  } catch(error) {
    if(current!==requestNumber || (error instanceof DOMException && error.name==='AbortError')) return;
    activeKey='';status('No se ha podido cargar esta instantánea.',true);
  }
}
function applyLayers(){
  $('#political-layer').classList.toggle('active',political);$('#political-layer').setAttribute('aria-pressed',String(political));
  $('#physical-layer').classList.toggle('active',physical&&snapshot.kind==='modern');$('#physical-layer').setAttribute('aria-pressed',String(physical&&snapshot.kind==='modern'));
  $('#places-layer').classList.toggle('active',showPlaces);$('#places-layer').setAttribute('aria-pressed',String(showPlaces));
  if(!ready)return;
  map.setPaintProperty('territory-fill','fill-color',political?colorExpression:'#819c88');
  map.setLayoutProperty('territory-line','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  map.setPaintProperty('territory-fill','fill-opacity',snapshot.kind==='geological'?1:0.88);
  map.setPaintProperty('territory-fill','fill-antialias',snapshot.kind!=='geological');
  map.setLayoutProperty('territory-labels','visibility',political&&snapshot.kind!=='geological'?'visible':'none');
  map.setLayoutProperty('relief','visibility',physical&&snapshot.kind==='modern'?'visible':'none');
  const points:FeatureCollection={type:'FeatureCollection',features:showPlaces&&year>=-10000?places.filter(p=>year>=p.start&&year<=p.end).map(p=>({type:'Feature',geometry:{type:'Point',coordinates:p.coordinates},properties:{name:p.name}})):[]};
  (map.getSource('places') as GeoJSONSource).setData(points);
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
  position=yearToPosition(year);
  const chapter=chapterFor(year);
  $('#year').textContent=formatYear(year);$('#era').textContent=eraName(year);
  $('#story-title').textContent=chapter.title;$('#story-text').textContent=chapter.text;
  $('#story-source span').textContent=chapter.sourceLabel;($('#story-source') as HTMLAnchorElement).href=chapter.source;
  renderRuler(); void refreshMap();
  if(save)persistLocation();
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
function stopPlay(){cancelAnimationFrame(playFrame);playFrame=0;lastFrame=0;$('#play').setAttribute('aria-pressed','false');$('#play').setAttribute('aria-label','Reproducir recorrido');$('#play').innerHTML=icon('play');createIcons({icons});}
function play(now:number){if(!lastFrame)lastFrame=now;const next=position+(now-lastFrame)/1000*0.22;lastFrame=now;updateYear(positionToYear(next));if(next>=anchors.length-1)stopPlay();else playFrame=requestAnimationFrame(play);}
$('#play').onclick=()=>{if(playFrame){stopPlay();return;}if(year===PRESENT)updateYear(anchors[0]);$('#play').setAttribute('aria-pressed','true');$('#play').setAttribute('aria-label','Pausar recorrido');$('#play').innerHTML=icon('pause');createIcons({icons});playFrame=requestAnimationFrame(play);};
$('#previous').onclick=()=>{stopPlay();updateYear(anchors[Math.max(0,Math.ceil(position)-1)]);};
$('#next').onclick=()=>{stopPlay();updateYear(anchors[Math.min(anchors.length-1,Math.floor(position)+1)]);};
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
    const matches=loaded.features.filter(f=>String(f.properties?.name).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(q)).slice(0,30);
    $('#search-results').replaceChildren();
    if(!matches.length)$('#search-results').textContent='Sin resultados en esta instantánea. Prueba otra fecha o nombre. Los nombres históricos conservan el idioma de la fuente.';
    matches.forEach(feature=>{const button=document.createElement('button');button.textContent=String(feature.properties?.name);button.onclick=()=>{if(feature.geometry.type==='Polygon'||feature.geometry.type==='MultiPolygon'){
      const coordinates=feature.geometry.type==='Polygon'?feature.geometry.coordinates[0]:feature.geometry.coordinates.flatMap(p=>p[0]);
      const valid=coordinates.filter(c=>Number.isFinite(c[0])&&Number.isFinite(c[1]));
      if(valid.length){const lng=valid.reduce((sum,c)=>sum+c[0],0)/valid.length;const lat=valid.reduce((sum,c)=>sum+c[1],0)/valid.length;map.flyTo({center:[lng,clamp(lat,-80,80)],zoom:3.5,duration:reduced?0:1000});}
    }$('#selection').hidden=false;$('#selection-title').textContent=String(feature.properties?.name);$('#selection-text').textContent=`Cartografía de referencia: ${formatYear(snapshot.year)}. Consulta las fuentes para conocer sus límites de precisión.`;modal.close();};$('#search-results').append(button);});
  };$('#search-input').oninput=search;search();
};
function sources(){openModal('FUENTES Y METODOLOGÍA',`<h2>La precisión también es saber qué desconocemos.</h2><p class="modal-intro">Esta primera versión integra 26 instantáneas. La regla selecciona la más próxima dentro de cada dominio; no interpola fronteras ni simula movimientos entre ellas. La fecha cartográfica está siempre visible junto al mapa.</p><div class="source-item"><h3>01 · El presente</h3><p>Natural Earth Admin 0 a 1:10 millones, 258 entidades cartográficas. Geometrías originales sin simplificación en la importación. Es cartografía global generalizada: el detalle local y la vigencia diaria de fronteras están pendientes.</p><a target="_blank" rel="noopener" href="https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/">Natural Earth · dominio público ↗</a></div><div class="source-item"><h3>02 · Sociedades y territorios</h3><p>13 instantáneas de Historical Basemaps, de 10.000 a. C. a 2010. Incluyen áreas culturales, dependencias y límites aproximados. No representan ocupación humana exhaustiva ni soberanía exclusiva. El relieve moderno se desactiva en el pasado.</p><a target="_blank" rel="noopener" href="https://github.com/aourednik/historical-basemaps">A. Ourednik · GPL-3.0 ↗</a></div><div class="source-item"><h3>03 · Continentes en movimiento</h3><p>12 reconstrucciones de 1 a 1.800 Ma mediante GPlates, modelo CAO2024. Contornos continentales reconstruidos; no son paleocostas exactas ni reconstrucciones de biomas, atmósfera o nivel del mar. La incertidumbre aumenta hacia el pasado.</p><a target="_blank" rel="noopener" href="https://doi.org/10.1016/j.gsf.2024.101922">Cao et al. (2024) · CC BY 4.0 ↗</a></div><div class="source-item"><h3>04 · Más allá de los datos</h3><p>Antes de 1.800 Ma se presenta una escena conceptual sin continentes inventados. Entre 1 Ma y 10.000 a. C. la cartografía está pendiente. Los homininos, las migraciones, las glaciaciones y las batallas requieren capas documentadas adicionales. No se presentan como funciones completadas.</p></div><p class="modal-intro">Escala temporal adaptativa, con intervalos no uniformes. Periodización orientativa; no universal. Cada descarga y su huella SHA-256 figuran en el manifiesto del repositorio.</p>`);}
$('#sources-button').onclick=sources;
$('#about-button').onclick=()=>openModal('ACERCA DE HISTORICMAP',aboutContent(VERSION,import.meta.env.BASE_URL),'about-dialog');
document.addEventListener('keydown',event=>{if(event.key==='Escape'){$('#selection').hidden=true;if(!$('#layers-panel').hidden)closeLayers(true);stopPlay();}if(event.code==='Space'&&!modal.open&&event.target===document.body){event.preventDefault();$('#play').click();}});
function restore(){const params=new URLSearchParams(location.hash.slice(1));const y=Number(params.get('year')??PRESENT);if(params.get('view')==='mercator')projection='mercator';else projection='globe';projectionControl();if(ready)map.setProjection({type:projection});updateYear(Number.isFinite(y)?y:PRESENT,false);}
window.addEventListener('hashchange',restore);restore();
