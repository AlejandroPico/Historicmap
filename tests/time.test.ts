import { describe, it, expect } from 'vitest';
import { anchors, eraName, formatYear, positionToYear, snapshotFor, yearToPosition } from '../src/time';
describe('adaptive chronological navigation',()=>{
  it('round-trips geological, prehistoric and historical anchors',()=>{for(const y of anchors)expect(positionToYear(yearToPosition(y))).toBe(y);});
  it('remains monotonic across unequal intervals and clamps its endpoints',()=>{let last=anchors[0];for(let p=0;p<=19;p+=.01){const y=positionToYear(p);expect(y).toBeGreaterThanOrEqual(last);last=y;}expect(positionToYear(-10)).toBe(anchors[0]);expect(positionToYear(200)).toBe(2026);});
  it('never returns the civil year zero',()=>expect(positionToYear(yearToPosition(0))).toBe(1));
  it('never substitutes modern borders for geological or uncovered prehistoric dates',()=>{expect(snapshotFor(-200000000)).toEqual({kind:'geological',year:-200000000,file:'coastlines-200.geojson'});expect(snapshotFor(-300000).kind).toBe('concept');expect(snapshotFor(-4540000000).kind).toBe('concept');});
  it('discloses the actual snapshot date instead of inventing intermediate borders',()=>{expect(snapshotFor(117).year).toBe(100);expect(snapshotFor(2025).year).toBe(2010);expect(snapshotFor(2026).kind).toBe('modern');expect(snapshotFor(-3000).file).toBe('world_bc3000.geojson');});
  it('formats dates and periods for Spanish readers',()=>{expect(formatYear(-4540000000)).toBe('4,54 Ga');expect(formatYear(-200000000)).toBe('200 Ma');expect(formatYear(100)).toBe('100 d. C.');expect(eraName(-3000)).toBe('Edad Antigua');});
});
