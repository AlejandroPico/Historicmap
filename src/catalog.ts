import { tx } from './i18n';
import {PRESENT} from './time';
export type Chapter = { year: number; label: string; title: string; text: string; source: string; sourceLabel: string };
export const chapters: Chapter[] = [
  {year: -4540000000, label: tx('catalog.elOrigen'), title: tx('catalog.unPlanetaEnFormacion'), text: tx('catalog.laTierraSeFormaHace'), source: 'https://science.nasa.gov/earth/facts/', sourceLabel: 'NASA · Earth facts'},
  {year: -4500000000, label: tx('catalog.tierraYLuna'), title: tx('catalog.laHipotesisDeTheia'), text: tx('catalog.laHipotesisDelGranImpacto'), source: 'https://science.nasa.gov/moon/formation/', sourceLabel: 'NASA · Moon formation'},
  {year: -3500000000, label: tx('catalog.vidaTemprana'), title: tx('catalog.lasPrimerasHuellasDeVida'), text: tx('catalog.elRegistroDeLaVida'), source: 'https://astrobiology.nasa.gov/research/life-detection/about/', sourceLabel: 'NASA · Astrobiology'},
  {year: -1000000000, label: 'Rodinia', title: tx('catalog.unMundoQueSeReune'), text: tx('catalog.losModelosDePlacasPermiten'), source: 'https://doi.org/10.1016/j.gsf.2024.101922', sourceLabel: tx('catalog.caoEtAl2024')},
  {year: -300000000, label: 'Pangea', title: tx('catalog.laTierraDeLosSupercontinentes'), text: tx('catalog.lasMasasContinentalesSeReunen'), source: 'https://doi.org/10.1016/j.gsf.2024.101922', sourceLabel: tx('catalog.caoEtAl2024')},
  {year: -200000000, label: 'Mesozoico', title: tx('catalog.losContinentesSeSeparan'), text: tx('catalog.duranteElMesozoicoProgresaLa'), source: 'https://gwsdoc.gplates.org/models/', sourceLabel: 'GPlates · CAO2024'},
  {year: -66000000, label: tx('catalog.t66MillonesDeAnos'), title: tx('catalog.unCambioDeEra'), text: tx('catalog.elLimiteEntreElCretacico'), source: 'https://www.stratigraphy.org/chart', sourceLabel: tx('catalog.internationalCommissionOnStratigraphy')},
  {year: -300000, label: tx('catalog.origenesHumanos'), title: tx('catalog.unaHistoriaDeMuchasHumanidades'), text: tx('catalog.homoSapiensApareceEnAfrica'), source: 'https://humanorigins.si.edu/evidence/human-fossils/species/homo-sapiens', sourceLabel: tx('catalog.smithsonianHumanOrigins')},
  {year: -10000, label: tx('catalog.primerasComunidades'), title: tx('catalog.nuevasFormasDeHabitar'), text: tx('catalog.lasComunidadesHumanasTransformanSus'), source: 'https://github.com/aourednik/historical-basemaps', sourceLabel: 'Historical Basemaps · A. Ourednik'},
  {year: -3000, label: tx('catalog.primerasCiudades'), title: tx('catalog.ciudadesRedesYPrimerosEstados'), text: tx('catalog.enMesopotamiaYOtrasRegiones'), source: 'https://github.com/aourednik/historical-basemaps', sourceLabel: 'Historical Basemaps · A. Ourednik'},
  {year: 100, label: tx('catalog.mundoAntiguo'), title: tx('catalog.unMundoDeImperiosY'), text: tx('catalog.romaLosHanYMuchas'), source: 'https://github.com/aourednik/historical-basemaps', sourceLabel: 'Historical Basemaps · A. Ourednik'},
  {year: 1000, label: tx('catalog.mundoMedieval'), title: tx('catalog.muchosCentrosMuchasHistorias'), text: tx('catalog.reinosCiudadesYRedesComerciales'), source: 'https://github.com/aourednik/historical-basemaps', sourceLabel: 'Historical Basemaps · A. Ourednik'},
  {year: 1492, label: tx('catalog.conexionesGlobales'), title: tx('catalog.unPlanetaCadaVezMas'), text: tx('catalog.elFinalDelSigloXv'), source: 'https://github.com/aourednik/historical-basemaps', sourceLabel: 'Historical Basemaps · A. Ourednik'},
  {year: 1789, label: tx('catalog.laRevolucionFrancesa'), title: tx('catalog.revolucionesYNuevosRegimenes'), text: tx('catalog.laCronologiaAnualEstaDisponible'), source: 'https://github.com/Seshat-Global-History-Databank/cliopatria', sourceLabel: tx('catalog.cliopatriaReconstruccionAnual')},
  {year: 1800, label: tx('catalog.mundoContemporaneo'), title: tx('catalog.territoriosEnTransformacion'), text: tx('catalog.revolucionesImperiosYNuevasConfiguraciones'), source: 'https://github.com/Seshat-Global-History-Databank/cliopatria', sourceLabel: tx('catalog.cliopatriaReconstruccionAnual')},
  {year: PRESENT, label: tx('catalog.elPresente'), title: tx('catalog.laTierraQueCompartimos'), text: tx('catalog.exploraPaisesCapitalesYSeries'), source: 'https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries/', sourceLabel: tx('catalog.naturalEarthReferenciaContemporanea')},
];
export function chapterFor(year: number) { return [...chapters].reverse().find(c => year >= c.year) ?? chapters[0]; }
export const places = [
  {name: 'Uruk', coordinates: [45.637,31.324], start: -4000, end: 500, description: tx('catalog.centroUrbanoDeMesopotamiaCoordenada'), source: 'https://whc.unesco.org/en/list/1481/'},
  {name: 'Roma', coordinates: [12.492,41.890], start: -500, end: 1899, description: tx('catalog.ciudadDeReferenciaDelMundo'), source: 'https://whc.unesco.org/en/list/91/'},
  {name: 'Çatalhöyük', coordinates: [32.827,37.667], start: -7400, end: -6200, description: tx('catalog.yacimientoNeoliticoDeAnatoliaFechas'), source: 'https://whc.unesco.org/en/list/1405/'},
];
