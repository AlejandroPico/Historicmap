// Lectura en voz alta con la síntesis de voz del navegador (Web Speech API).
// «Escuchar» lee la página entera o, si hay texto seleccionado, desde ese punto. Durante la lectura,
// pulsar cualquier párrafo salta a él. La pausa y la velocidad se controlan desde la barra del artículo.

const BLOCKS = 'h1, .encyclopedia-lead, .enc-body h2, .enc-body h3, .enc-body h4, .enc-body p, .enc-body li, .enc-body dt, .enc-body dd, .enc-composition h2, .enc-composition h3, .enc-composition h4, .enc-composition h5, .enc-composition p, .enc-composition li';
const SKIP = 'figure, .enc-infobox, nav, details:not([open]) > :not(summary), .enc-scale, .enc-chart, .enc-tl, .enc-map, .enc-succession';

interface State { root: HTMLElement | null; blocks: HTMLElement[]; index: number; part: number; parts: string[]; active: boolean; paused: boolean; rate: number; token: number }
const state: State = { root: null, blocks: [], index: 0, part: 0, parts: [], active: false, paused: false, rate: 1, token: 0 };
let lastSelected: Node | null = null, pressingPlay = false;
if (typeof document !== 'undefined') {
  // Al pulsar «Escuchar» el navegador puede deshacer la selección: se recuerda la última selección del artículo.
  document.addEventListener('pointerdown', e => { pressingPlay = !!(e.target as Element | null)?.closest?.('[data-tts="play"]'); setTimeout(() => { pressingPlay = false; }, 600); }, true);
  document.addEventListener('selectionchange', () => {
    const sel = document.getSelection();
    if (sel && !sel.isCollapsed && sel.anchorNode && (sel.anchorNode.parentElement ?? sel.anchorNode as Element)?.closest?.('#encyclopedia-article')) lastSelected = sel.anchorNode;
    else if (!pressingPlay) lastSelected = null;
  });
}
export const speechSupported = () => typeof window !== 'undefined' && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';

function voice() {
  const voices = speechSynthesis.getVoices();
  return voices.find(v => v.lang === 'es-ES' && /natural|google|online/i.test(v.name)) ?? voices.find(v => v.lang === 'es-ES') ?? voices.find(v => v.lang.startsWith('es'));
}
/** Divide un párrafo en frases de longitud moderada: algunos motores cortan las locuciones muy largas. */
function split(text: string) {
  const sentences = text.replace(/\s+/g, ' ').match(/[^.!?;:]+[.!?;:]*\s*/g) ?? [text];
  const out: string[] = []; let cur = '';
  for (const s of sentences) { if ((cur + s).length > 220 && cur) { out.push(cur.trim()); cur = ''; } cur += s; }
  if (cur.trim()) out.push(cur.trim());
  return out;
}
function collect(root: HTMLElement) {
  return [...root.querySelectorAll<HTMLElement>(BLOCKS)].filter(el => !el.closest(SKIP) && el.innerText.trim().length > 1 && !(el.tagName === 'LI' && el.querySelector('p')));
}
function controls() {
  const root = state.root?.closest('#encyclopedia-article') ?? document;
  return { play: root.querySelector<HTMLButtonElement>('[data-tts="play"]'), stop: root.querySelector<HTMLButtonElement>('[data-tts="stop"]') };
}
function paint() {
  const { play, stop } = controls();
  if (play) { play.textContent = !state.active ? '▶ Escuchar' : state.paused ? '▶ Continuar' : '❚❚ Pausa'; play.setAttribute('aria-pressed', String(state.active && !state.paused)); }
  if (stop) stop.hidden = !state.active;
  document.querySelectorAll('.enc-speaking').forEach(el => el.classList.remove('enc-speaking'));
  if (state.active && state.blocks[state.index]) state.blocks[state.index].classList.add('enc-speaking');
}
function speakCurrent(token: number) {
  if (token !== state.token || !state.active) return;
  const block = state.blocks[state.index];
  if (!block) { stopSpeech(); return; }
  if (state.part === 0) { state.parts = split(block.innerText.trim()); block.scrollIntoView({ block: 'center', behavior: 'smooth' }); paint(); }
  const u = new SpeechSynthesisUtterance(state.parts[state.part] ?? '');
  u.lang = 'es-ES'; u.rate = state.rate; const v = voice(); if (v) u.voice = v;
  u.onend = () => { if (token !== state.token) return; state.part++; if (state.part >= state.parts.length) { state.part = 0; state.index++; } speakCurrent(token); };
  u.onerror = () => { if (token === state.token) { state.part = 0; state.index++; speakCurrent(token); } };
  speechSynthesis.speak(u);
}
function startAt(index: number) {
  speechSynthesis.cancel();
  state.token++; state.index = Math.max(0, index); state.part = 0; state.active = true; state.paused = false;
  speakCurrent(state.token);
}
export function stopSpeech() {
  if (!speechSupported()) return;
  state.token++; state.active = false; state.paused = false; speechSynthesis.cancel(); paint();
}
/** Gestiona los clics de la enciclopedia relacionados con la lectura. Devuelve true si lo ha atendido. */
export function handleSpeechClick(target: Element, article: HTMLElement): boolean {
  if (!speechSupported()) return false;
  const button = target.closest<HTMLElement>('[data-tts]');
  if (button?.dataset.tts === 'stop') { stopSpeech(); return true; }
  if (button?.dataset.tts === 'play') {
    if (state.active && !state.paused) { speechSynthesis.pause(); state.paused = true; paint(); return true; }
    if (state.active && state.paused) { speechSynthesis.resume(); state.paused = false; paint(); return true; }
    state.root = article.querySelector<HTMLElement>('.enc-page') ?? article; state.blocks = collect(state.root);
    const sel = window.getSelection(); let start = 0;
    const anchor = sel && !sel.isCollapsed && sel.anchorNode ? sel.anchorNode : lastSelected;
    lastSelected = null;
    if (anchor && state.root.contains(anchor)) {
      const node = anchor.nodeType === 1 ? anchor as Element : anchor.parentElement!;
      const i = state.blocks.findIndex(b => b.contains(node));
      start = i >= 0 ? i : Math.max(0, state.blocks.findIndex(b => !!(node.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING)));
    }
    startAt(start); return true;
  }
  if (state.active && !target.closest('a, button, select, input, summary')) {
    const block = target.closest<HTMLElement>(BLOCKS); const i = block ? state.blocks.indexOf(block) : -1;
    if (i >= 0) { startAt(i); return true; }
  }
  return false;
}
export function handleSpeechRate(target: Element) {
  const select = target.closest<HTMLSelectElement>('[data-tts-rate]'); if (!select) return false;
  state.rate = Number(select.value) || 1;
  if (state.active && !state.paused) startAt(state.index);
  return true;
}
/** Tras pintar una página: detiene la lectura anterior y oculta los controles si el navegador no tiene voz. */
export function resetSpeech(article: HTMLElement) {
  stopSpeech();
  const group = article.querySelector<HTMLElement>('.enc-tts'); if (group && !speechSupported()) group.hidden = true;
  const rate = article.querySelector<HTMLSelectElement>('[data-tts-rate]'); if (rate) rate.value = String(state.rate);
}
