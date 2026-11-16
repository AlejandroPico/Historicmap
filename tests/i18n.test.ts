import { describe, expect, it } from 'vitest';
import { execFileSync } from 'node:child_process';
import { tx, language, BASE_LANGUAGE } from '../src/i18n';

describe('internacionalización', () => {
  it('todas las claves usadas en el código existen en el idioma base', () => {
    expect(() => execFileSync('node', ['scripts/check-i18n.mjs'], { stdio: 'pipe' })).not.toThrow();
  });
  it('resuelve textos y sustituye marcadores', () => {
    expect(BASE_LANGUAGE).toBe('es');
    expect(language).toBe('es');
    expect(tx('main.verMapa2d')).toBe('Ver mapa 2D');
    expect(tx('clave.inexistente')).toBe('clave.inexistente');
  });
});
