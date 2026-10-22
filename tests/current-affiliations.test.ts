import {describe,it,expect} from 'vitest';
import {CURRENT_CONFLICTS,currentConflicts} from '../src/current-affiliations';
describe('observaciones contemporáneas de conflictos',()=>{
  it('conserva contextos documentados sin inferir guerras por pertenencia a alianzas', () => {
    expect(currentConflicts('USA', 2026).some(conflict => conflict.id === 'iran-2026')).toBe(true);
    expect(currentConflicts('SDN', 2026).some(conflict => conflict.id === 'sudan-2026')).toBe(true);
    expect(currentConflicts('ESP', 2026)).toEqual([]);
    expect(currentConflicts('UKR', 2025)).toEqual([]);
    expect(currentConflicts('YEM', 2027)).toEqual([]);
    expect(CURRENT_CONFLICTS.every(conflict => conflict.source.startsWith('https://') && conflict.referenceDate <= '2026-10-22')).toBe(true);
  });
});
