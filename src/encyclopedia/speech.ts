// Lectura en voz alta con la síntesis de voz del navegador (Web Speech API).
// El reproductor vive en la cabecera fija de la enciclopedia: anterior · reproducir/pausa · siguiente · detener · ajustes
// (velocidad y voz). Lee la página entera o desde el texto seleccionado; durante la lectura, pulsar un párrafo salta a él.
import { speakable } from './speech-text';

const BLOCKS = 'h1, .encyclopedia-lead, .enc-body h2, .enc-body h3, .enc-body h4, .enc-body p, .enc-body li, .enc-body dt, .enc-body dd, .enc-composition h2, .enc-composition h3, .enc-composition h4, .enc-composition h5, .enc-composition p, .enc-composition li';
const SKIP = 'figure, .enc-infobox, nav, details:not([open]) > :not(summary), .enc-scale, .enc-chart, .enc-tl, .enc-map, .enc-succession';
const VOICE_KEY = 'historicmap-voice', RATE_KEY = 'historicmap-voice-rate';

interface State { article: HTMLElement | null; blocks: HTMLElement[]; index: number; part: number; parts: string[]; active: boolean; paused: boolean; rate: number; voice: string; token: number }
const read = (k: string) => { try { return localStorage.getItem(k) ?? ''; } catch { return ''; } };
const write = (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* sin almacenamiento */ } };
const state: State = { article: null, blocks: [], index: 0, part: 0, parts: [], active: false, paused: false, rate: Number(read(RATE_KEY)) || 1, voice: read(VOICE_KEY), token: 0 };
export const speechSupported = () => typeof window !== 'undefined' && 'speechSynthesis' in window && typeof SpeechSynthesisUtterance !== 'undefined';

let lastSelected: Node | null = null, pressingPlay = false;
if (typeof document !== 'undefined') {
  // Al pulsar «reproducir» el navegador puede deshacer la selección: se recuerda la última selección del artículo.
  document.addEventListener('pointerdown', e => { pressingPlay = !!(e.target as Element | null)?.closest?.('[data-tts="play"]'); setTimeout(() => { pressingPlay = false; }, 600); }, true);
  document.addEventListener('selectionchange', () => {
    const sel = document.getSelection();
    if (sel && !sel.isCollapsed && sel.anchorNode && (sel.anchorNode.parentElement ?? sel.anchorNode as Element)?.closest?.('#encyclopedia-article')) lastSelected = sel.anchorNode;
    else if (!pressingPlay) lastSelected = null;
  });
}

const ICON = {
  prev: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5v14M19 5 9 12l10 7z"/></svg>',
  next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 5v14M5 5l10 7-10 7z"/></svg>',
  play: '<svg class="enc-ico-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg><svg class="enc-ico-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z"/></svg>',
  stop: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6.5" y="6.5" width="11" height="11" rx="1.5"/></svg>',
  gear: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>'
};
/** Marcado del reproductor de la cabecera. */
export function playerMarkup() {
  if (!speechSupported()) return '';
  return `<div class="enc-player" role="group" aria-label="Lectura en voz alta" data-state="idle">
<button data-tts="prev" class="enc-pl-side" aria-label="Párrafo anterior" title="Párrafo anterior">${ICON.prev}</button>
<button data-tts="play" class="enc-pl-main" aria-label="Leer en voz alta" title="Leer en voz alta (desde el texto seleccionado, si lo hay)">${ICON.play}<span class="enc-pl-eq" aria-hidden="true"><i></i><i></i><i></i><i></i></span></button>
<button data-tts="next" class="enc-pl-side" aria-label="Párrafo siguiente" title="Párrafo siguiente">${ICON.next}</button>
<button data-tts="stop" class="enc-pl-side" aria-label="Detener la lectura" title="Detener">${ICON.stop}</button>
<button data-tts="settings" class="enc-pl-side" aria-label="Velocidad y voz" title="Velocidad y voz" aria-expanded="false">${ICON.gear}</button>
<div class="enc-pl-pop" hidden><label>Velocidad <select data-tts-rate>${[0.8, 0.9, 1, 1.15, 1.3, 1.5, 1.75].map(r => `<option value="${r}"${r === state.rate ? ' selected' : ''}>${String(r).replace('.', ',')}×</option>`).join('')}</select></label><label>Voz <select data-tts-voice><option value="">Automática (español)</option></select></label></div>
</div>`;
}
function fillVoices() {
  const select = document.querySelector<HTMLSelectElement>('[data-tts-voice]'); if (!select || !speechSupported()) return;
  const voices = speechSynthesis.getVoices(); if (!voices.length) return;
  const es = voices.filter(v => v.lang.toLowerCase().startsWith('es')), other = voices.filter(v => !v.lang.toLowerCase().startsWith('es'));
  const opt = (v: SpeechSynthesisVoice) => `<option value="${v.name.replace(/"/g, '&quot;')}"${v.name === state.voice ? ' selected' : ''}>${v.name.replace(/</g, '&lt;')} · ${v.lang}</option>`;
  select.innerHTML = `<option value="">Automática (español)</option>${es.length ? `<optgroup label="Español">${es.map(opt).join('')}</optgroup>` : ''}${other.length ? `<optgroup label="Otros idiomas">${other.map(opt).join('')}</optgroup>` : ''}`;
}
if (typeof window !== 'undefined' && speechSupported()) speechSynthesis.addEventListener?.('voiceschanged', fillVoices);

function voice() {
  const voices = speechSynthesis.getVoices();
  return voices.find(v => v.name === state.voice) ?? voices.find(v => v.lang === 'es-ES' && /natural|google|online|neural/i.test(v.name)) ?? voices.find(v => v.lang === 'es-ES') ?? voices.find(v => v.lang.startsWith('es'));
}
/** Divide un párrafo en frases de longitud moderada: algunos motores cortan las locuciones muy largas. */
function split(text: string) {
  const sentences = text.replace(/\s+/g, ' ').match(/[^.!?;:]+(?:[.!?;:](?!\d))*\s*/g) ?? [text];
  const out: string[] = []; let cur = '';
  for (const s of sentences) { if ((cur + s).length > 220 && cur) { out.push(cur.trim()); cur = ''; } cur += s; }
  if (cur.trim()) out.push(cur.trim());
  return out;
}
function collect(root: HTMLElement) {
  return [...root.querySelectorAll<HTMLElement>(BLOCKS)].filter(el => !el.closest(SKIP) && el.innerText.trim().length > 1 && !(el.tagName === 'LI' && el.querySelector('p')));
}
function paint() {
  const player = document.querySelector<HTMLElement>('.enc-player');
  if (player) {
    player.dataset.state = !state.active ? 'idle' : state.paused ? 'paused' : 'playing';
    player.style.setProperty('--enc-progress', String(state.blocks.length ? (state.index + 1) / state.blocks.length : 0));
    const play = player.querySelector('[data-tts="play"]');
    play?.setAttribute('aria-label', !state.active ? 'Leer en voz alta' : state.paused ? 'Continuar la lectura' : 'Pausar la lectura');
    play?.setAttribute('aria-pressed', String(state.active && !state.paused));
  }
  document.querySelectorAll('.enc-speaking').forEach(el => el.classList.remove('enc-speaking'));
  if (state.active && state.blocks[state.index]) state.blocks[state.index].classList.add('enc-speaking');
}
function speakCurrent(token: number) {
  if (token !== state.token || !state.active) return;
  const block = state.blocks[state.index];
  if (!block) { stopSpeech(); return; }
  if (state.part === 0) { state.parts = split(speakable(block.innerText.trim())); block.scrollIntoView({ block: 'center', behavior: 'smooth' }); paint(); }
  const u = new SpeechSynthesisUtterance(state.parts[state.part] ?? '');
  const v = voice(); u.lang = v?.lang ?? 'es-ES'; u.rate = state.rate; if (v) u.voice = v;
  u.onend = () => { if (token !== state.token) return; state.part++; if (state.part >= state.parts.length) { state.part = 0; state.index++; } speakCurrent(token); };
  u.onerror = () => { if (token === state.token) { state.part = 0; state.index++; speakCurrent(token); } };
  speechSynthesis.speak(u);
}
function startAt(index: number) {
  speechSynthesis.cancel();
  state.token++; state.index = Math.min(Math.max(0, index), Math.max(0, state.blocks.length - 1)); state.part = 0; state.active = true; state.paused = false;
  speakCurrent(state.token);
}
function prepare() {
  state.article = document.querySelector<HTMLElement>('#encyclopedia-article .enc-page');
  state.blocks = state.article ? collect(state.article) : [];
}
export function stopSpeech() {
  if (!speechSupported()) return;
  state.token++; state.active = false; state.paused = false; speechSynthesis.cancel(); paint();
}
/** Gestiona los clics de la enciclopedia relacionados con la lectura. Devuelve true si lo ha atendido. */
export function handleSpeechClick(target: Element): boolean {
  if (!speechSupported()) return false;
  const button = target.closest<HTMLElement>('[data-tts]'), action = button?.dataset.tts;
  if (action === 'settings') { const pop = button!.parentElement!.querySelector<HTMLElement>('.enc-pl-pop')!; pop.hidden = !pop.hidden; button!.setAttribute('aria-expanded', String(!pop.hidden)); if (!pop.hidden) fillVoices(); return true; }
  if (action === 'stop') { stopSpeech(); return true; }
  if (action === 'prev' || action === 'next') {
    if (!state.active) { prepare(); startAt(action === 'next' ? 1 : 0); }
    else startAt(state.index + (action === 'next' ? 1 : -1));
    return true;
  }
  if (action === 'play') {
    if (state.active && !state.paused) { speechSynthesis.pause(); state.paused = true; paint(); return true; }
    if (state.active && state.paused) { speechSynthesis.resume(); state.paused = false; paint(); return true; }
    prepare(); if (!state.article) return true;
    const sel = window.getSelection(); let start = 0;
    const anchor = sel && !sel.isCollapsed && sel.anchorNode ? sel.anchorNode : lastSelected;
    lastSelected = null;
    if (anchor && state.article.contains(anchor)) {
      const node = anchor.nodeType === 1 ? anchor as Element : anchor.parentElement!;
      const i = state.blocks.findIndex(b => b.contains(node));
      start = i >= 0 ? i : Math.max(0, state.blocks.findIndex(b => !!(node.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING)));
    }
    startAt(start); return true;
  }
  if (state.active && target.closest('#encyclopedia-article') && !target.closest('a, button, select, input, summary')) {
    const block = target.closest<HTMLElement>(BLOCKS); const i = block ? state.blocks.indexOf(block) : -1;
    if (i >= 0) { startAt(i); return true; }
  }
  if (!target.closest('.enc-player')) document.querySelectorAll<HTMLElement>('.enc-pl-pop').forEach(p => { if (!p.hidden) { p.hidden = true; p.parentElement?.querySelector('[data-tts="settings"]')?.setAttribute('aria-expanded', 'false'); } });
  return false;
}
/** Cambios de velocidad o de voz. */
export function handleSpeechChange(target: Element) {
  const rate = target.closest<HTMLSelectElement>('[data-tts-rate]'), voiceSel = target.closest<HTMLSelectElement>('[data-tts-voice]');
  if (rate) { state.rate = Number(rate.value) || 1; write(RATE_KEY, String(state.rate)); }
  else if (voiceSel) { state.voice = voiceSel.value; write(VOICE_KEY, state.voice); }
  else return false;
  if (state.active && !state.paused) startAt(state.index);
  return true;
}
/** Tras pintar una página: detiene la lectura anterior. */
export function resetSpeech() { stopSpeech(); }
