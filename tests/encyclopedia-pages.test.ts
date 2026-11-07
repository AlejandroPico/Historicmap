import { describe, expect, it } from 'vitest';
import { splitPage, parseYaml, civilYear, internalLinks, firstParagraph, shardOf, centuryOf } from '../scripts/lib/encyclopedia-format.mjs';
import { compileEncyclopedia } from '../scripts/build-encyclopedia.mjs';
import { render, inline } from '../src/encyclopedia/markdown';
import { geologicalUnits } from '../src/earth-chronology';
import { COMPONENT_NAMES } from '../scripts/lib/encyclopedia-format.mjs';
import { componentNames, component, scaleView, mapSvg, successionChart } from '../src/encyclopedia/components';

describe('formato de páginas de la enciclopedia', () => {
  it('lee la cabecera YAML reducida', () => {
    const { meta, body } = splitPage('---\nid: geo-Jurassic\ntipo: geologia\ntitulo: Jurásico\nalias: [Jurasico, "Edad de los dinosaurios"]\nficha:\n  Duración: 58 Ma\nfuentes:\n  - titulo: ICS\n    url: https://stratigraphy.org\n  - { titulo: B, url: https://b.org }\n---\nTexto [[geo-Triassic|Triásico]].\n');
    expect(meta).toMatchObject({ id: 'geo-Jurassic', alias: ['Jurasico', 'Edad de los dinosaurios'], ficha: { 'Duración': '58 Ma' } });
    expect(meta.fuentes).toEqual([{ titulo: 'ICS', url: 'https://stratigraphy.org' }, { titulo: 'B', url: 'https://b.org' }]);
    expect(internalLinks(body)).toEqual(['geo-Triassic']);
    expect(firstParagraph(body)).toBe('Texto Triásico.');
    expect(parseYaml('a: 1\nb: true\nc: null\nd: "x: y"')).toEqual({ a: 1, b: true, c: null, d: 'x: y' });
  });
  it('convierte fechas civiles y edades geológicas sin año cero', () => {
    expect(civilYear(1943)).toBe(1943);
    expect(civilYear('-0490-09-12')).toBe(-490);
    expect(civilYear('1950 ka')).toBe(-1948051);
    expect(civilYear('201.4 Ma')).toBe(-201398051);
    expect(() => civilYear(0)).toThrow();
    expect(centuryOf(1943)).toBe(19); expect(centuryOf(100)).toBe(0); expect(centuryOf(-1)).toBe(-1); expect(centuryOf(-101)).toBe(-2);
    expect(shardOf('Q1407', 64)).toBe(shardOf('Q1407', 64));
  });
  it('genera HTML seguro con enlaces internos, tablas y bloques', () => {
    expect(inline('<b>[[geo-Jurassic|Jurásico]]</b>')).toBe('&lt;b&gt;<a href="#" class="enc-link" data-encyclopedia-entry="geo-Jurassic">Jurásico</a>&lt;/b&gt;');
    const { html, headings } = render('## Clima\nTexto **fuerte**.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n:::debate Causas\nDos *hipótesis*.\n:::\n\n:::cronologia\n252 Ma | Trampas\n:::');
    expect(headings).toEqual([{ level: 2, text: 'Clima', anchor: 'enc-clima' }]);
    expect(html).toContain('<strong>fuerte</strong>'); expect(html).toContain('<td>2</td>');
    expect(html).toContain('enc-debate'); expect(html).toContain('<em>hipótesis</em>'); expect(html).toContain('<time>252 Ma</time>');
  });
});

describe('compilación de enciclopedia/', () => {
  const build = compileEncyclopedia();
  it('no tiene errores, identificadores repetidos ni enlaces rotos', () => {
    expect(build.errors).toEqual([]);
    const index = JSON.parse(build.files.get('indice.json')!);
    const ids = index.paginas.map((p: { id: string }) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
    for (const p of index.paginas.filter((p: { id: string }) => p.id.startsWith('geo-'))) expect(geologicalUnits.some(u => 'geo-' + u.id === p.id), p.id).toBe(true);
    for (const p of index.paginas) expect(p.resumen.length, p.id).toBeGreaterThan(20);
  });
  it('genera fichas para todos los dirigentes y entidades del atlas', () => {
    expect(build.stats.personas).toBe(12606);
    expect(build.stats.entidades).toBe(2423);
    const names = JSON.parse(build.files.get('nombres.json')!);
    expect(names.length).toBe(12606 + 2423);
    const shard = JSON.parse(build.files.get(`personas/${String(shardOf('Q1407', 64)).padStart(2, '0')}.json`)!);
    expect(shard.Q1407.n).toBe('Tiberio');
    expect(shard.Q1407.m.some((m: string[]) => m[0] === 'ROMAN-EMPIRE-CLASSICAL')).toBe(true);
    const c19 = JSON.parse(build.files.get('mandatos/19.json')!);
    expect(c19.m.length).toBeGreaterThan(1000);
  });
});

describe('componentes visuales', () => {
  it('el compilador y el lector conocen los mismos componentes', () => { expect([...componentNames].sort()).toEqual([...COMPONENT_NAMES].sort()); });
  it('la escala amplía cualquier unidad sin aplastarla', () => {
    const root = scaleView(''); expect(root).toContain('data-scale-zoom="Phanerozoic"'); expect(root).toContain('Toda la historia');
    const meso = scaleView('Mesozoic'); expect(meso).toContain('data-scale-zoom="Jurassic"'); expect(meso).toContain('data-scale-zoom="UpperJurassic"'); expect(meso).toContain('data-encyclopedia-entry="geo-Tithonian"');
    expect(scaleView('UpperJurassic')).toContain('Titoniense');
  });
  it('dibuja gráficos, líneas de tiempo, mapas y sucesiones', () => {
    const chart = component('grafico', 'barras | Prueba | %', { year: 2026 }, 'x; a\nUno; 10\nDos; 20');
    expect(chart).toContain('<rect'); expect(chart).toContain('Uno · a: 10 %');
    const tl = component('linea-tiempo', 'Hitos', { year: 2026 }, '2.5 Ga | Inicio\n717 Ma / 660 Ma | Esturtiana');
    expect(tl).toContain('Esturtiana'); expect(tl).toContain('<rect');
    const spec = JSON.parse(component('mapa', '', { year: 2026 }, '40.4, -3.7 | Madrid\npaíses: ESP').match(/data-enc-map="([^"]+)"/)![1].replace(/&quot;/g, '"'));
    expect(spec).toEqual({ points: [[40.4, -3.7, 'Madrid']], countries: ['ESP'], bbox: null });
    expect(mapSvg({ ESP: 'M0 0L1 1Z' }, spec)).toContain('enc-map-hi');
    expect(successionChart([{ id: 'persona-Q1', name: 'A', role: 'Rey', start: 1000, end: 1010 }, { id: 'persona-Q2', name: 'B', role: 'Rey', start: 1010, end: 1030 }], 'Sucesión')).toContain('persona-Q2');
    expect(component('inexistente', '', { year: 1 })).toContain('no disponible');
  });
});

describe('contenido de la P03 · formación de la Tierra y Arcaico', () => {
  const index = JSON.parse(compileEncyclopedia().files.get('indice.json')!);
  const byId = (id: string) => index.paginas.find((p: { id: string }) => p.id === id);
  it('cada unidad del Hádico y el Arcaico tiene página propia y extensa', () => {
    for (const id of ['geo-Hadean', 'geo-Archean', 'geo-Eoarchean', 'geo-Paleoarchean', 'geo-Mesoarchean', 'geo-Neoarchean']) expect(byId(id)?.palabras, id).toBeGreaterThan(350);
  });
  it('los artículos temáticos cuelgan de su unidad y sustituyen a los heredados', () => {
    const topics = index.paginas.filter((p: { padre: string | null }) => ['geo-Hadean', 'geo-Archean', 'geo-Eoarchean', 'geo-Paleoarchean', 'geo-Mesoarchean', 'geo-Neoarchean'].includes(p.padre ?? ''));
    expect(topics.length).toBeGreaterThanOrEqual(24);
    for (const t of topics) expect(t.palabras, t.id).toBeGreaterThan(500);
    expect(byId('geo-Hadean').reemplaza).toContain('hadean'); expect(byId('geo-Archean').reemplaza).toContain('archean');
    for (const id of ['formation', 'theia', 'luca', 'microbial', 'interior']) expect(byId(id), id).toBeDefined();
  });
});
