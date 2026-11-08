import { describe, expect, it } from 'vitest';
import { speakable } from '../src/encyclopedia/speech-text';

describe('texto para la lectura en voz alta', () => {
  it('pronuncia las unidades geológicas sin cambiar el texto visible', () => {
    expect(speakable('4.031 ± 3 Ma')).toBe('4031 más o menos 3 millones de años');
    expect(speakable('hace 3,6 Ga')).toBe('hace 3,6 miles de millones de años');
    expect(speakable('unos 11,7 ka')).toBe('unos 11,7 mil años');
    expect(speakable('de 2.500–2.400 Ma')).toBe('de 2500 a 2400 millones de años');
  });
  it('quita los separadores de miles para que no se lean como decimales', () => {
    expect(speakable('12.606 dirigentes y 1.000.000 de años')).toBe('12606 dirigentes y 1000000 de años');
    expect(speakable('0,005 %')).toBe('0,005 por ciento');
  });
  it('lee símbolos, fórmulas y otras unidades', () => {
    expect(speakable('CO₂ ≈ 400 ppm')).toBe('ce o dos aproximadamente 400 partes por millón');
    expect(speakable('1.600 °C y 360 GPa')).toBe('1600 grados y 360 gigapascales');
    expect(speakable('5.100 km² en 490 a. C.')).toBe('5100 kilómetros cuadrados en 490 antes de Cristo');
    expect(speakable('3 × 10⁻⁴ PAL')).toBe('3 por 10 elevado a menos 4 PAL');
  });
});
