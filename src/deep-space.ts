// Espacio y atmósfera del tiempo profundo (solo en el globo): fondo estrellado que se desplaza al girar la Tierra y
// halo atmosférico alrededor del limbo, con color según la época (resplandor del magma, calima anaranjada del Arcaico,
// azul tras la oxigenación, blanco azulado en las glaciaciones globales) y sombreado esférico (luz rasante y penumbra)
// sobre el disco. Son elementos HTML detrás y encima del lienzo del mapa,
// que es transparente fuera del globo; no tocan los datos ni las capas del atlas.
import type { Map as MapLibreMap } from 'maplibre-gl';
import type { DeepScene } from './deep-earth';

interface Space { stars: HTMLDivElement; aura: HTMLDivElement; shade: HTMLDivElement; map: MapLibreMap; on: boolean }
let space: Space | undefined;

/** Azulejo de estrellas determinista (sin azar entre visitas): tres tamaños, tonos fríos y cálidos y una banda tenue. */
function starTile() {
  const size = 1024, c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d')!;
  let seed = 20261115; const rnd = () => { seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0; return seed / 4294967296; };
  for (let i = 0; i < 2600; i++) {                                    // banda de la galaxia: polvo de estrellas débiles en diagonal
    const t = rnd(), off = (rnd() + rnd() + rnd() - 1.5) * 150, x = t * size, y = (size * .15 + t * size * .7 + off + size) % size;
    g.fillStyle = `rgba(190,205,255,${.05 + rnd() * .12})`; g.fillRect(x, y, 1, 1);
  }
  for (let i = 0; i < 1500; i++) {
    const x = rnd() * size, y = rnd() * size, m = rnd(), r = m > .992 ? 1.5 : m > .93 ? 1 : .6, a = m > .992 ? .95 : .25 + rnd() * .55;
    const tint = rnd(), col = tint > .85 ? '255,214,170' : tint > .6 ? '200,220,255' : '255,255,255';
    if (r > 1.2) { const halo = g.createRadialGradient(x, y, 0, x, y, 5); halo.addColorStop(0, `rgba(${col},.35)`); halo.addColorStop(1, `rgba(${col},0)`); g.fillStyle = halo; g.fillRect(x - 5, y - 5, 10, 10); }
    g.fillStyle = `rgba(${col},${a})`; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill();
  }
  return c.toDataURL('image/png');
}

function place() {
  if (!space?.on) return;
  const { map, aura, stars, shade } = space, center = map.getCenter();
  const c = map.project(center), limb = map.project([center.lng, center.lat >= 0 ? center.lat - 90 : center.lat + 90]);
  const r = Math.hypot(limb.x - c.x, limb.y - c.y);
  if (!Number.isFinite(r) || r < 8) { aura.style.opacity = shade.style.opacity = '0'; return; }
  const d = r * 3;                                                     // el limbo queda al 66,67 % del degradado
  aura.style.opacity = '1'; aura.style.width = aura.style.height = `${d}px`; aura.style.transform = `translate(${c.x - d / 2}px,${c.y - d / 2}px)`;
  shade.style.opacity = '1'; shade.style.width = shade.style.height = `${r * 2}px`; shade.style.transform = `translate(${c.x - r}px,${c.y - r}px)`;
  stars.style.backgroundPosition = `${-center.lng * 2.2}px ${center.lat * 2.2}px`;
}

/** Activa, colorea u oculta el espacio y el halo según la escena y la proyección. */
export function updateDeepSpace(map: MapLibreMap, scene: DeepScene | undefined, age: number, ice: string | null, globe: boolean) {
  const host = map.getContainer();
  if (!space) {
    const stars = document.createElement('div'), aura = document.createElement('div'), shade = document.createElement('div');
    shade.className = 'deep-shade'; shade.setAttribute('aria-hidden', 'true');
    stars.className = 'deep-stars'; aura.className = 'deep-aura'; stars.setAttribute('aria-hidden', 'true'); aura.setAttribute('aria-hidden', 'true');
    stars.style.backgroundImage = `url(${starTile()})`;
    host.prepend(aura); host.prepend(stars);
    map.getCanvas().after(shade);                                     // sobre el lienzo, bajo marcadores y controles
    space = { stars, aura, shade, map, on: false };
    map.on('move', place); map.on('resize', place);
  }
  const on = !!scene && globe; space.on = on; host.classList.toggle('deep-space', on);
  if (!on || !scene) return;
  const magma = scene.mode === 'magma', cooling = scene.mode === 'cooling';
  const [rgb, strength, reach] = magma ? ['255,138,36', .95, 1] : cooling ? ['226,84,34', .5, .7]
    : ice === 'snowball' ? ['196,228,246', .62, .55] : age >= 2500 && age <= 3400 ? ['222,152,92', .55, .6]
    : age > 3400 ? ['196,196,186', .42, .5] : age > 2400 ? ['150,186,214', .46, .5] : ['104,170,255', .55, .5];
  space.aura.style.setProperty('--aura', rgb as string); space.aura.style.setProperty('--aura-a', String(strength)); space.aura.style.setProperty('--aura-reach', String(reach));
  space.aura.dataset.glow = space.shade.dataset.glow = magma ? 'magma' : cooling ? 'cooling' : 'air';
  place();
}
