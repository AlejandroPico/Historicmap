// Explicit WDI acquisition. Builds and atlas visits do not contact external services.
// Country keys are WDI keys already present in profiles.json, never regional aggregates.
import {readFile, writeFile, mkdir, rename} from 'node:fs/promises';

const root = new URL('../', import.meta.url);
const cache = new URL('.cache/country-indicators/', root);
await mkdir(cache, {recursive: true});
const profiles = JSON.parse(await readFile(new URL('public/data/profiles.json', root), 'utf8'));
const referenceDate = process.env.ATLAS_REFERENCE_DATE || '2026-10-23';
if (!/^\d{4}-\d{2}-\d{2}$/.test(referenceDate)) throw Error('Invalid ATLAS_REFERENCE_DATE');
const maxYear = Number(referenceDate.slice(0, 4));
const minimumYear = 1960;
const refresh = process.argv.includes('--refresh');
const definitions = [
  ['gdpGrowth','NY.GDP.MKTP.KD.ZG','Crecimiento real del PIB','%','economy','Variación anual del PIB a precios constantes; no es crecimiento del PIB nominal.',true],
  ['inflation','FP.CPI.TOTL.ZG','Inflación de precios de consumo','%','economy','Variación anual del índice de precios de consumo; puede ser negativa (deflación).',true],
  ['unemployment','SL.UEM.TOTL.ZS','Desempleo (estimación OIT)','%','economy','Porcentaje de la población activa; estimación modelizada de la OIT.'],
  ['exports','NE.EXP.GNFS.ZS','Exportaciones de bienes y servicios','% del PIB','economy','Valor de las exportaciones de bienes y servicios como porcentaje del PIB; puede superar el 100 %.'],
  ['imports','NE.IMP.GNFS.ZS','Importaciones de bienes y servicios','% del PIB','economy','Valor de las importaciones de bienes y servicios como porcentaje del PIB; puede superar el 100 %.'],
  ['agriculture','NV.AGR.TOTL.ZS','Agricultura, silvicultura y pesca','% del PIB','economy','Valor añadido del sector; la suma de sectores no equivale necesariamente al 100 % por impuestos y ajustes.'],
  ['industry','NV.IND.TOTL.ZS','Industria, incluida construcción','% del PIB','economy','Valor añadido industrial, incluida la construcción.'],
  ['services','NV.SRV.TOTL.ZS','Servicios','% del PIB','economy','Valor añadido del sector servicios.'],
  ['centralGovernmentDebt','GC.DOD.TOTL.GD.ZS','Deuda del gobierno central','% del PIB','economy','Deuda del gobierno central, no deuda de todas las administraciones públicas. Cobertura institucional y años desiguales.'],
  ['currentAccount','BN.CAB.XOKA.GD.ZS','Saldo por cuenta corriente','% del PIB','economy','Saldo de transacciones corrientes con el exterior; un valor negativo indica déficit.',true],
  ['investment','NE.GDI.TOTL.ZS','Formación bruta de capital','% del PIB','economy','Adquisiciones menos disposiciones de activos producidos, incluidas variaciones de existencias; puede ser negativa. No inversión extranjera directa.',true],
  ['density','EN.POP.DNST','Densidad de población','habitantes/km²','society','Habitantes por kilómetro cuadrado de superficie terrestre, según la definición territorial de la fuente.'],
  ['literacy','SE.ADT.LITR.ZS','Alfabetización adulta','%','society','Población de 15 años o más que puede leer y escribir una frase breve sobre su vida cotidiana; observaciones no anuales en muchos países.'],
  ['secondaryEnrollment','SE.SEC.ENRR','Matriculación secundaria bruta','%','society','Alumnado de secundaria de cualquier edad dividido por población de la edad oficial; puede superar el 100 %. No es tasa neta ni graduación.'],
  ['internet','IT.NET.USER.ZS','Uso de Internet','%','society','Personas que han utilizado Internet en los últimos tres meses, como porcentaje de la población.'],
  ['fertility','SP.DYN.TFRT.IN','Fecundidad total','hijos por mujer','society','Número de hijos que tendría una mujer bajo las tasas de fecundidad por edad del periodo.'],
  ['netMigration','SM.POP.NETM','Migración neta','personas','society','Inmigrantes menos emigrantes en el periodo anual publicado; conserva signo y estimaciones de la fuente.',true],
  ['under5Mortality','SH.DYN.MORT','Mortalidad de menores de cinco años','por 1.000 nacidos vivos','society','Probabilidad por mil de morir antes de cumplir cinco años bajo las tasas del año; estimación, no recuento de defunciones.'],
  ['electricity','EG.ELC.ACCS.ZS','Acceso a electricidad','%','society','Porcentaje de población con acceso a electricidad; no mide continuidad ni calidad del suministro.'],
  ['gini','SI.POV.GINI','Desigualdad de ingresos (Gini)','índice 0–100','society','Índice de Gini de renta o consumo según encuesta; 0 igualdad y 100 desigualdad máximas. Conceptos y encuestas no son idénticos entre países.'],
  ['armedForces','MS.MIL.TOTL.P1','Personal de las fuerzas armadas','personas','defense','Personal militar en servicio activo, incluidas fuerzas paramilitares cuando cumplen la definición de la fuente. No es una clasificación de capacidad militar.'],
  ['armedForcesLabor','MS.MIL.TOTL.TF.ZS','Personal militar sobre población activa','%','defense','Personal de las fuerzas armadas como porcentaje de la población activa. La serie puede terminar años antes de la consulta.'],
];

async function acquired(name, url, textMode = false, attempts = 4) {
  const file = new URL(name, cache);
  if (!refresh) {
    try {
      const envelope = JSON.parse(await readFile(file, 'utf8'));
      if (envelope.url === url) return envelope;
    } catch {}
  }
  for (let attempt = 0; attempt < attempts; attempt++) {
    try {
      const response = await fetch(url, {signal: AbortSignal.timeout(textMode ? 30000 : 120000)});
      if (!response.ok) throw Error(`${response.status}: ${url}`);
      const data = textMode ? await response.text() : await response.json();
      const envelope = {url, retrieved: new Date().toISOString(), data};
      await writeFile(file, JSON.stringify(envelope) + '\n');
      return envelope;
    } catch (error) {
      if (attempt === attempts - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1200 * (attempt + 1)));
    }
  }
}

async function licensedPage(indicator, source) {
  try { return await acquired(`${indicator}-license.json`,source,true,1); }
  catch {
    // The public indicator frontend occasionally returns 504; the official glossary
    // independently publishes License Type and License URL for the same series.
    return acquired(`${indicator}-glossary-license.json`,`https://databank.worldbank.org/metadataglossary/world-development-indicators/series/${indicator}`,true,2);
  }
}

const wbCountries = await acquired('countries.json','https://api.worldbank.org/v2/country?format=json&per_page=400');
if (!Array.isArray(wbCountries.data?.[1]) || wbCountries.data[0].pages !== 1) throw Error('Invalid country response');
const allowed = new Set(wbCountries.data[1].filter(row => row.region?.id !== 'NA' && profiles.countries[row.id]).map(row => row.id));
const indicators = {};
const countries = {};
const sources = [];
const audit = [];
const excludedObservations = [];
let observations = 0;

// Two bounded downloads at once; write output only after every indicator passed validation.
for (let offset = 0; offset < definitions.length; offset += 2) {
  await Promise.all(definitions.slice(offset, offset + 2).map(async ([key, indicator, label, unit, section, description, allowNegative = false]) => {
    const source = `https://data.worldbank.org/indicator/${indicator}`;
    const dataUrl = `https://api.worldbank.org/v2/country/all/indicator/${indicator}?source=2&date=${minimumYear}:${maxYear}&format=json&per_page=25000`;
    const metadataUrl = `https://api.worldbank.org/v2/indicator/${indicator}?source=2&format=json`;
    const [raw, metadata, page] = await Promise.all([
      acquired(`${indicator}-${maxYear}.json`, dataUrl),
      acquired(`${indicator}-metadata.json`, metadataUrl),
      licensedPage(indicator, source),
    ]);
    // WDI contains third-party restricted indicators (notably SIPRI); never assume a global license.
    const plainPage = page.data.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ');
    if (!/License(?: Type)?\s*:?\s*(?:CC BY-4\.0|CC BY 4\.0)/i.test(plainPage)) throw Error(`No explicit CC BY-4.0 license for ${indicator}`);
    if (!Array.isArray(raw.data?.[1]) || raw.data[0].pages !== 1) throw Error(`Invalid/paginated data for ${indicator}`);
    const meta = metadata.data?.[1]?.find(item => item.id === indicator && item.source?.id === '2');
    if (!meta) throw Error(`No source-2 metadata for ${indicator}`);
    let count = 0;
    let first = maxYear;
    let last = minimumYear;
    const codes = new Set();
    const forecastRejected = [];
    for (const row of raw.data[1]) {
      const code = row.countryiso3code;
      if (!allowed.has(code) || row.value === null) continue;
      const year = Number(row.date);
      if (!Number.isInteger(year) || year < minimumYear || year > maxYear || !Number.isFinite(row.value)) throw Error(`Invalid observation ${indicator}/${code}/${row.date}`);
      if (row.obs_status === 'F') { forecastRejected.push(`${code}:${year}`); continue; }
      if (row.value < 0 && !allowNegative) {
        excludedObservations.push({metric:key,indicator,code,year,value:row.value,reason:'Valor negativo inesperado para esta magnitud; pendiente de contraste. Se conserva aquí y no se publica como observación validada.'});
        continue;
      }
      const series = (countries[code] ??= {})[key] ??= [];
      if (series.some(item => item[0] === year)) throw Error(`Duplicate ${indicator}/${code}/${year}`);
      series.push([year,row.value]);
      first = Math.min(first,year); last = Math.max(last,year); count++; codes.add(code);
    }
    if (count === 0) throw Error(`No valid observations for ${indicator}`);
    indicators[key] = {label,unit,section,source,indicator,description,allowNegative,license:'CC BY-4.0',licenseUrl:'https://creativecommons.org/licenses/by/4.0/',metadata:metadataUrl,provider:meta.sourceOrganization || 'World Bank · World Development Indicators',validity:{from:first,to:last},retrieved:raw.retrieved,version:raw.data[0].lastupdated || null};
    sources.push({indicator,url:dataUrl,metadata:metadataUrl,licenseSource:page.url,licenseVerified:page.retrieved,retrieved:raw.retrieved,version:raw.data[0].lastupdated || null});
    audit.push({key,indicator,countries:codes.size,observations:count,from:first,to:last,forecastRowsExcluded:forecastRejected.length});
    observations += count;
    console.log(`${key}: ${codes.size} countries, ${count} observations, ${first}–${last}`);
  }));
}

const sortedCountries = Object.fromEntries(Object.keys(countries).sort().map(code => [code,Object.fromEntries(definitions.filter(([key]) => countries[code][key]).map(([key]) => [key,countries[code][key].sort((a,b) => b[0]-a[0])]))]));
const output = {retrieved:new Date().toISOString(),referenceDate,source:'World Bank · World Development Indicators (source 2)',license:'CC BY-4.0; World Bank additional dataset terms',licenseUrl:'https://www.worldbank.org/ext/en/legal/terms-conditions/datasets',range:{from:minimumYear,to:maxYear},indicators:Object.fromEntries(definitions.map(([key]) => [key,indicators[key]])),sources:sources.sort((a,b) => a.indicator.localeCompare(b.indicator)),excludedObservations,countries:sortedCountries};
const target = new URL('public/data/country-indicators.json',root);
const temporary = new URL('public/data/country-indicators.json.tmp',root);
await writeFile(temporary,JSON.stringify(output)+'\n');
await rename(temporary,target);
await writeFile(new URL('audit.json',cache),JSON.stringify({countries:Object.keys(sortedCountries).length,indicators:definitions.length,observations,indicatorsAudit:audit.sort((a,b) => a.key.localeCompare(b.key))},null,2)+'\n');
console.log(`Saved ${Object.keys(sortedCountries).length} country/economy keys, ${definitions.length} indicators, ${observations} observations.`);
