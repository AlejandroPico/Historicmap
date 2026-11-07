// Markdown de la enciclopedia → HTML. Subconjunto propio, sin dependencias:
// títulos ##–####, párrafos, negrita/cursiva/código, enlaces externos, enlaces internos [[id|texto]],
// listas (con un nivel de anidación), tablas, citas, imágenes y bloques «:::tipo».
import { LINK_PATTERN } from '../../scripts/lib/encyclopedia-format.mjs';

export const esc = (s: unknown) => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!));

export interface RenderOptions {
  /** Título visible de una página interna (para enlaces sin texto). */
  title?: (id: string) => string | undefined;
  /** URL de un medio de enciclopedia/medios. */
  media?: (path: string) => string | undefined;
  /** Crédito HTML de un medio local. */
  credit?: (path: string) => string | undefined;
  /** Componentes visuales registrados para «:::componente nombre». */
  component?: (name: string, args: string, content?: string) => string;
  /** Desplaza el nivel de los títulos al componer páginas hijas. */
  headingOffset?: number;
  /** Prefijo de anclas para no repetir identificadores al componer. */
  anchorPrefix?: string;
}

export interface Heading { level: number; text: string; anchor: string }

export function slug(s: string) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }

export function inline(text: string, o: RenderOptions = {}) {
  const stash: string[] = [];
  const keep = (html: string) => `\u0000${stash.push(html) - 1}\u0000`;
  let s = text.replace(/`([^`]+)`/g, (_, c) => keep(`<code>${esc(c)}</code>`));
  s = s.replace(LINK_PATTERN, (_m, id: string, label?: string) => keep(`<a href="#" class="enc-link" data-encyclopedia-entry="${esc(id)}">${esc(label ?? o.title?.(id) ?? id)}</a>`));
  s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, (_m, label: string, url: string) => keep(`<a href="${esc(url)}" target="_blank" rel="noopener">${esc(label)}</a>`));
  s = esc(s);
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/(^|[^*])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>');
  return s.replace(/\u0000(\d+)\u0000/g, (_, i) => stash[Number(i)]);
}

function table(lines: string[], o: RenderOptions) {
  const cells = (l: string) => l.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
  const head = cells(lines[0]), align = cells(lines[1]).map(c => c.endsWith(':') ? (c.startsWith(':') ? 'center' : 'right') : '');
  const row = (l: string, tag: string) => `<tr>${cells(l).map((c, i) => `<${tag}${align[i] ? ` style="text-align:${align[i]}"` : ''}>${inline(c, o)}</${tag}>`).join('')}</tr>`;
  return `<div class="enc-table"><table><thead>${row(lines[0], 'th')}</thead><tbody>${lines.slice(2).map(l => row(l, 'td')).join('')}</tbody></table></div>`;
}

function list(lines: string[], o: RenderOptions): string {
  const ordered = /^\d+\.\s/.test(lines[0].trim());
  const items: { text: string; sub: string[] }[] = [];
  for (const l of lines) {
    if (/^\s{2,}/.test(l) && items.length) items[items.length - 1].sub.push(l.replace(/^\s{2,4}/, ''));
    else items.push({ text: l.trim().replace(/^([-*]|\d+\.)\s+/, ''), sub: [] });
  }
  const tag = ordered ? 'ol' : 'ul';
  return `<${tag}>${items.map(i => `<li>${inline(i.text, o)}${i.sub.length ? list(i.sub, o) : ''}</li>`).join('')}</${tag}>`;
}

function special(kind: string, arg: string, content: string[], o: RenderOptions) {
  if (kind === 'componente') return o.component?.(arg.split(/\s+/)[0], arg.split(/\s+/).slice(1).join(' ')) ?? '';
  if (!['nota', 'debate', 'clave', 'curiosidad', 'cita', 'cronologia', 'datos'].includes(kind)) return o.component?.(kind, arg, content.join('\n')) ?? '';
  if (kind === 'cronologia') return `<ol class="enc-timeline">${content.filter(l => l.trim()).map(l => { const [date, ...rest] = l.replace(/^[-*]\s*/, '').split('|'); return `<li><time>${inline(date.trim(), o)}</time><span>${inline(rest.join('|').trim(), o)}</span></li>`; }).join('')}</ol>`;
  if (kind === 'datos') return `<dl class="enc-data">${content.filter(l => l.includes(':')).map(l => { const i = l.indexOf(':'); return `<div><dt>${inline(l.slice(0, i).replace(/^[-*]\s*/, '').trim(), o)}</dt><dd>${inline(l.slice(i + 1).trim(), o)}</dd></div>`; }).join('')}</dl>`;
  const label = arg || ({ nota: 'Nota', debate: 'Evidencias y debate', clave: 'Idea clave', curiosidad: 'Curiosidad', cita: '' } as Record<string, string>)[kind] || '';
  return `<aside class="enc-callout enc-${esc(kind)}">${label ? `<strong>${esc(label)}</strong>` : ''}${render(content.join('\n'), o).html}</aside>`;
}

/** Renderiza Markdown y devuelve HTML y títulos (para la tabla de contenidos). */
export function render(source: string, o: RenderOptions = {}): { html: string; headings: Heading[] } {
  const lines = source.replace(/\r\n/g, '\n').split('\n');
  const out: string[] = [], headings: Heading[] = [];
  let i = 0, para: string[] = [];
  const flush = () => { if (para.length) { out.push(`<p>${inline(para.join(' '), o)}</p>`); para = []; } };
  while (i < lines.length) {
    const line = lines[i], t = line.trim();
    if (!t) { flush(); i++; continue; }
    const fence = /^:::\s*([a-z][a-z-]*)\s*(.*)$/.exec(t);
    if (fence) {
      flush(); const content: string[] = []; i++;
      let depth = 0;
      while (i < lines.length) { const l = lines[i].trim(); if (/^:::\s*[a-z]/.test(l)) depth++; else if (l === ':::') { if (!depth) break; depth--; } content.push(lines[i]); i++; }
      i++; out.push(special(fence[1], fence[2].trim(), content, o)); continue;
    }
    const h = /^(#{2,4})\s+(.+)$/.exec(t);
    if (h) {
      flush(); const level = Math.min(6, h[1].length + (o.headingOffset ?? 0)), text = h[2].trim(), anchor = (o.anchorPrefix ?? 'enc-') + slug(text);
      headings.push({ level: h[1].length, text, anchor });
      out.push(`<h${level} id="${esc(anchor)}">${inline(text, o)}</h${level}>`); i++; continue;
    }
    if (t.startsWith('|') && lines[i + 1]?.trim().match(/^\|?\s*:?-{2,}/)) {
      flush(); const rows: string[] = []; while (i < lines.length && lines[i].trim().startsWith('|')) rows.push(lines[i++]);
      out.push(table(rows, o)); continue;
    }
    if (/^([-*]|\d+\.)\s/.test(t)) {
      flush(); const rows: string[] = [];
      while (i < lines.length && lines[i].trim() && (/^([-*]|\d+\.)\s/.test(lines[i].trim()) || /^\s{2,}/.test(lines[i]))) rows.push(lines[i++]);
      out.push(list(rows, o)); continue;
    }
    if (t.startsWith('>')) {
      flush(); const rows: string[] = []; while (i < lines.length && lines[i].trim().startsWith('>')) rows.push(lines[i++].trim().replace(/^>\s?/, ''));
      out.push(`<blockquote>${render(rows.join('\n'), o).html}</blockquote>`); continue;
    }
    const img = /^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)$/.exec(t);
    if (img) {
      flush(); const src = /^https?:/.test(img[2]) ? img[2] : o.media?.(img[2]);
      const credit = /^https?:/.test(img[2]) ? undefined : o.credit?.(img[2]);
      if (src) out.push(`<figure class="enc-figure"><img src="${esc(src)}" alt="${esc(img[1])}" loading="lazy">${img[3] || credit ? `<figcaption>${img[3] ? inline(img[3], o) : ''}${credit ? ` <span class="enc-credit">${credit}</span>` : ''}</figcaption>` : ''}</figure>`);
      i++; continue;
    }
    para.push(t); i++;
  }
  flush();
  return { html: out.join('\n'), headings };
}
