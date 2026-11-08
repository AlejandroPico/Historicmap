// Texto «para el oído»: convierte unidades, símbolos y cifras de la enciclopedia en palabras que la
// síntesis de voz pronuncia bien, sin tocar lo que se ve en pantalla (que mantiene Ma, Ga, ±, CO₂…).

const SUB: Record<string, string> = { '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9' };
const SUP: Record<string, string> = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': 'menos ' };

/** Unidades que solo se leen como palabra si van detrás de una cifra. */
const UNITS: [RegExp, string][] = [
  [/Ga\b/g, 'miles de millones de años'], [/Gyr\b/g, 'miles de millones de años'], [/Ma\b/g, 'millones de años'], [/Myr\b/g, 'millones de años'],
  [/ka\b/g, 'mil años'], [/kyr\b/g, 'mil años'], [/años? BP\b/g, 'años antes del presente'], [/BP\b/g, 'antes del presente'], [/b2k\b/g, 'antes del año 2000'],
  [/a\.\s?C\./g, 'antes de Cristo'], [/d\.\s?C\./g, 'después de Cristo'],
  [/km²/g, 'kilómetros cuadrados'], [/km³/g, 'kilómetros cúbicos'], [/m²/g, 'metros cuadrados'], [/m³/g, 'metros cúbicos'], [/cm³/g, 'centímetros cúbicos'],
  [/km\/s\b/g, 'kilómetros por segundo'], [/km\/h\b/g, 'kilómetros por hora'], [/cm\/año/g, 'centímetros por año'], [/mm\/año/g, 'milímetros por año'],
  [/km\b/g, 'kilómetros'], [/cm\b/g, 'centímetros'], [/mm\b/g, 'milímetros'], [/µm\b/g, 'micras'], [/μm\b/g, 'micras'], [/nm\b/g, 'nanómetros'], [/m\b/g, 'metros'],
  [/°C/g, "grados"], [/K\b/g, 'kelvin'], [/‰/g, 'por mil'], [/%/g, 'por ciento'], [/ppmv?\b/g, 'partes por millón'], [/ppb\b/g, 'partes por mil millones'],
  [/GPa\b/g, 'gigapascales'], [/MPa\b/g, 'megapascales'], [/kbar\b/g, 'kilobares'], [/bar\b/g, 'bares'], [/atm\b/g, 'atmósferas'],
  [/µT\b/g, 'microteslas'], [/μT\b/g, 'microteslas'], [/nT\b/g, 'nanoteslas'], [/TW\b/g, 'teravatios'], [/W\/m²/g, 'vatios por metro cuadrado'],
  [/g\/cm³/g, 'gramos por centímetro cúbico'], [/kg\b/g, 'kilogramos'], [/Gt\b/g, 'gigatoneladas'], [/t\b/g, 'toneladas'], [/UA\b/g, 'unidades astronómicas'], [/h\b/g, 'horas']
];
const SYMBOLS: [RegExp, string][] = [
  [/±/g, ' más o menos '], [/≈|∼|~/g, ' aproximadamente '], [/≤/g, ' menor o igual que '], [/≥/g, ' mayor o igual que '], [/</g, ' menos de '], [/>/g, ' más de '],
  [/×/g, ' por '], [/→/g, ' a '], [/·/g, ', '], [/δ/g, 'delta '], [/Δ/g, 'incremento de '], [/µ|μ/g, 'micro'], [/°/g, ' grados'], [/\s—\s|—/g, ', ']
];
const FORMULAS: [RegExp, string][] = [
  [/\bCO2\b/g, 'ce o dos'], [/\bO2\b/g, 'o dos'], [/\bO3\b/g, 'ozono'], [/\bN2\b/g, 'ene dos'], [/\bH2O\b/g, 'agua'], [/\bH2S\b/g, 'sulfuro de hidrógeno'],
  [/\bH2\b/g, 'hache dos'], [/\bCH4\b/g, 'metano'], [/\bNH3\b/g, 'amoníaco'], [/\bSO2\b/g, 'dióxido de azufre'], [/\bFe2\+/g, 'hierro dos más'], [/\bFe3\+/g, 'hierro tres más'],
  [/\bU-Pb\b/g, 'uranio-plomo'], [/\bAr-Ar\b/g, 'argón-argón'], [/\bSm-Nd\b/g, 'samario-neodimio'], [/\bLu-Hf\b/g, 'lutecio-hafnio'], [/\bRb-Sr\b/g, 'rubidio-estroncio'],
  [/\bGSSP\b/g, 'ge ese ese pe'], [/\bGSSA\b/g, 'ge ese ese a'], [/\bICS\b/g, 'i ce ese'], [/\bIUGS\b/g, 'i u ge ese'], [/\bMIF-S\b/g, 'eme i efe ese'], [/\bBIF\b/g, 'bif']
];

export function speakable(input: string): string {
  let s = input.replace(/[₀-₉]/g, c => SUB[c]);
  for (const [re, txt] of FORMULAS) s = s.replace(re, txt);
  // Miles con punto (4.031, 12.606, 1.000.000): se eliminan los puntos para que no se lean como decimales.
  s = s.replace(/\b\d{1,3}(?:\.\d{3})+\b/g, m => m.replace(/\./g, ''));
  // Intervalos entre cifras: «2.500–2.400» → «2500 a 2400».
  s = s.replace(/(\d)\s*[–-]\s*(\d)/g, '$1 a $2');
  // Unidades tras una cifra (con espacio, espacio duro o sin espacio).
  for (const [re, word] of UNITS) {
    const src = re.source;
    s = s.replace(new RegExp(`(\\d(?:,\\d+)?)[\\s\\u00a0]*${src}`, 'g'), `$1 ${word}`);
  }
  s = s.replace(/[⁰-⁹⁻]+/g, m => ' elevado a ' + [...m].map(c => SUP[c] ?? c).join('') + ' ');
  for (const [re, txt] of SYMBOLS) s = s.replace(re, txt);
  return s.replace(/\s{2,}/g, ' ').replace(/\s+([,.;:])/g, '$1').trim();
}
