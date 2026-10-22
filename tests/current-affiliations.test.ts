import { describe, expect, it } from 'vitest';
import {
  AFFILIATIONS, AFFILIATION_KINDS, affiliationFor, affiliationLegend, CURRENT_CONFLICTS, currentConflicts,
} from '../src/current-affiliations';

describe('agrupaciones de referencia de 2026', () => {
  it('mantiene las categorías oficiales y no duplica países dentro de una agrupación', () => {
    expect(AFFILIATIONS.nato.categories[0].codes).toHaveLength(32);
    expect(AFFILIATIONS.eu.categories[0].codes).toHaveLength(27);
    expect(AFFILIATIONS.brics.categories.map(category => category.codes.length)).toEqual([11, 10]);
    expect(AFFILIATIONS.threeSeas.categories.map(category => category.codes.length)).toEqual([13, 4, 6]);
    for (const kind of AFFILIATION_KINDS) {
      const codes = AFFILIATIONS[kind].categories.flatMap(category => [...category.codes]);
      expect(new Set(codes).size).toBe(codes.length);
      expect(codes.every(code => /^[A-Z]{3}$/.test(code))).toBe(true);
    }
  });

  it('distingue miembros, socios y candidatos sin trasladar la pertenencia a dependencias', () => {
    expect(affiliationFor('SWE', 'nato', 2026)?.category).toBe('member');
    expect(affiliationFor('FIN', 'nato', 2026)?.category).toBe('member');
    expect(affiliationFor('GRL', 'nato', 2026)?.category).toBe('other');
    expect(affiliationFor('GBR', 'eu', 2026)?.category).toBe('other');
    expect(affiliationFor('UKR', 'eu', 2026)?.category).toBe('other');
    expect(affiliationFor('SAU', 'brics', 2026)?.category).toBe('member');
    expect(affiliationFor('VNM', 'brics', 2026)?.category).toBe('partner');
    expect(affiliationFor('TUR', 'brics', 2026)?.category).toBe('other');
    expect(affiliationFor('UKR', 'threeSeas', 2026)?.category).toBe('associate');
    expect(affiliationFor('ITA', 'threeSeas', 2026)?.category).toBe('partner');
    expect(affiliationFor('GRC', 'threeSeas', 2026)?.category).toBe('member');
  });

  it('no retroproyecta ni prorroga una instantánea de 2026', () => {
    for (const kind of AFFILIATION_KINDS) {
      for (const year of [1942, 2025, 2027, 2028]) {
        expect(affiliationFor('USA', kind, year)).toBeUndefined();
        expect(affiliationLegend(kind, year)).toEqual([]);
      }
      const legend = affiliationLegend(kind, 2026);
      expect(legend.at(-1)?.category).toBe('other');
      expect(new Set(legend.map(entry => entry.color)).size).toBe(legend.length);
      expect(affiliationFor('ESP', kind, 2026)?.source).toMatch(/^https:\/\//);
    }
  });

  it('conserva contextos documentados sin inferir guerras por pertenencia a alianzas', () => {
    expect(currentConflicts('USA', 2026).some(conflict => conflict.id === 'iran-2026')).toBe(true);
    expect(currentConflicts('SDN', 2026).some(conflict => conflict.id === 'sudan-2026')).toBe(true);
    expect(currentConflicts('ESP', 2026)).toEqual([]);
    expect(currentConflicts('UKR', 2025)).toEqual([]);
    expect(currentConflicts('YEM', 2027)).toEqual([]);
    expect(CURRENT_CONFLICTS.every(conflict => conflict.source.startsWith('https://') && conflict.referenceDate <= '2026-10-22')).toBe(true);
  });
});
