import { describe, it, expect } from 'vitest';
import { anchors, eraName, formatYear, positionToYear, snapshotFor, yearToPosition, PRESENT, systemYear, playbackYear } from '../src/time';
describe('adaptive chronological navigation',()=>{
  it('round-trips geological, prehistoric and historical anchors',()=>{for(const y of anchors)expect(positionToYear(yearToPosition(y))).toBe(y);});
  it('remains monotonic across unequal intervals and clamps its endpoints',()=>{let last=anchors[0];for(let p=0;p<=anchors.length-1;p+=.01){const y=positionToYear(p);expect(y).toBeGreaterThanOrEqual(last);last=y;}expect(positionToYear(-10)).toBe(anchors[0]);expect(positionToYear(200)).toBe(PRESENT);});
  it('never returns the civil year zero',()=>expect(positionToYear(yearToPosition(0))).toBe(1));
  it('never substitutes modern borders for geological or uncovered prehistoric dates',()=>{expect(snapshotFor(-200000000)).toEqual({kind:'geological',year:-200000000,file:'coastlines-200.geojson'});expect(snapshotFor(-300000).kind).toBe('concept');expect(snapshotFor(-4540000000).kind).toBe('concept');});
  it('selects dated country periods instead of a nearest postwar snapshot',()=>{expect(snapshotFor(117).year).toBe(100);for(let y=1900;y<2020;y++)expect(snapshotFor(y)).toEqual({kind:'annual',year:y,file:'history.topojson'});for(let y=2020;y<=PRESENT;y++)expect(snapshotFor(y).kind).toBe('modern');expect(snapshotFor(-3000).file).toBe('world_bc3000.geojson');});
  it('reads the device year and advances recent history one year at a time',()=>{expect(systemYear(new Date(2028,6,1))).toBe(2028);expect(PRESENT).toBe(new Date().getFullYear());expect(playbackYear(1941)).toBe(1942);expect(playbackYear(PRESENT)).toBe(PRESENT);});
  it('formats dates and periods for Spanish readers',()=>{expect(formatYear(-4540000000)).toBe('4,54 Ga');expect(formatYear(-200000000)).toBe('200 Ma');expect(formatYear(100)).toBe('100 d. C.');expect(eraName(-3000)).toBe('Edad Antigua');});
});
