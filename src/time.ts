/** Civil years, with no year zero; geological dates are approximate years before 1950. */
export const systemYear = (date = new Date()) => date.getFullYear();
export const PRESENT = systemYear();
export const anchors = [-4540000000, -4000000000, -2500000000, -1800000000, -1000000000, -541000000, -300000000, -200000000, -66000000, -2600000, -300000, -10000, -3000, -1000, 100, 1000, 1492, 1800, 1914, PRESENT];
export const clamp = (n: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, n));
export function yearToPosition(year: number): number {
  const y = clamp(year, anchors[0], PRESENT);
  let i = anchors.findIndex((v) => v >= y);
  if (i <= 0) return 0;
  return i - 1 + (y - anchors[i - 1]) / (anchors[i] - anchors[i - 1]);
}
export function positionToYear(position: number): number {
  const p = clamp(position, 0, anchors.length - 1);
  const i = Math.min(Math.floor(p), anchors.length - 2);
  const y = Math.round(anchors[i] + (anchors[i + 1] - anchors[i]) * (p - i));
  return y === 0 ? 1 : y;
}
export function formatYear(year: number): string {
  if (year <= -1000000000) return `${Number((Math.abs(year) / 1e9).toFixed(2)).toLocaleString('es')} Ga`;
  if (year <= -1000000) return `${Number((Math.abs(year) / 1e6).toFixed(2)).toLocaleString('es')} Ma`;
  if (year < 0) return `${Math.abs(year).toLocaleString('es')} a. C.`;
  return `${year.toLocaleString('es', { useGrouping: false })} d. C.`;
}
export function eraName(year: number): string {
  if (year < -4000000000) return 'Hádico';
  if (year < -2500000000) return 'Arcaico';
  if (year < -541000000) return 'Proterozoico';
  if (year < -252000000) return 'Paleozoico';
  if (year < -66000000) return 'Mesozoico';
  if (year < -2600000) return 'Cenozoico';
  if (year < -3000) return 'Prehistoria';
  if (year < 476) return 'Edad Antigua';
  if (year < 1492) return 'Edad Media';
  if (year < 1789) return 'Edad Moderna';
  return 'Edad Contemporánea';
}
export const historicalYears = [-10000, -3000, -1000, -500, 100, 500, 1000, 1492, 1800, 1914, 1945, 1994, 2010];
export const geologicalMa = [1, 20, 66, 100, 200, 300, 400, 541, 750, 1000, 1500, 1800];
export type Snapshot = { kind: 'modern' | 'annual' | 'historical' | 'geological' | 'concept'; year: number; file?: string };
export function snapshotFor(year: number): Snapshot {
  if (year < -1800000000) return { kind: 'concept', year };
  if (year < -1000000) {
    const ma = geologicalMa.reduce((a, b) => Math.abs(a + year / 1e6) <= Math.abs(b + year / 1e6) ? a : b);
    return { kind: 'geological', year: -ma * 1e6, file: `coastlines-${ma}.geojson` };
  }
  if (year < -10000) return { kind: 'concept', year };
  if (year >= 2020) return { kind: 'modern', year, file: 'countries.geojson' };
  if (year >= 900) return { kind: 'annual', year, file: year>=1886?'history.topojson':year>=1789?'early-modern.geojson':year>=1700?'early-modern-1700.geojson':year>=1600?'early-modern-1600.geojson':year>=1500?'early-modern-1500.geojson':year>=1400?'early-modern-1400.geojson':year>=1300?'early-modern-1300.geojson':year>=1200?'early-modern-1200.geojson':year>=1100?'early-modern-1100.geojson':year>=1000?'early-modern-1000.geojson':'early-modern-900.geojson' };
  const y = historicalYears.filter(y=>y<1789).reduce((a, b) => Math.abs(a - year) <= Math.abs(b - year) ? a : b);
  return { kind: 'historical', year: y, file: `world_${y < 0 ? `bc${-y}` : y}.geojson` };
}
export function playbackYear(year:number){return year>=900?Math.min(PRESENT,year+1):positionToYear(yearToPosition(year)+.075);}
