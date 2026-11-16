import { tx } from './i18n';
type Context={from:number;to:number;title:string;text:string;source:string;entities?:string[]};
const us='https://history.state.gov/milestones/';
export const recentContexts:Context[]=[
 {from:1900,to:1913,title:tx('recentContext.unMundoDeImperios'),text:tx('recentContext.losImperiosColonialesAdministranExtensos'),source:'https://icr.ethz.ch/data/cshapes/'},
 {from:1914,to:1918,title:tx('recentContext.laPrimeraGuerraMundial'),text:tx('recentContext.laGuerraTransformaEuropaY'),source:us+'1914-1920/wwi'},
 {from:1919,to:1935,title:tx('recentContext.lasFronterasDeEntreguerras'),text:tx('recentContext.losTratadosDePazY'),source:us+'1914-1920/paris-peace'},
 {from:1936,to:1937,title:tx('recentContext.espanaDosBandosEnGuerra'),text:tx('recentContext.laGuerraCivilEspanolaDivide'),source:'https://www.ign.es/web/resources/docs/IGNCnig/ANE/Capitulos/06_Historicaloverview_2024.pdf'},
 {from:1938,to:1938,title:tx('recentContext.europaEn1938'),text:tx('recentContext.laExpansionDeLaAlemania'),source:'https://encyclopedia.ushmm.org/content/en/article/german-prewar-expansion'},
 {from:1939,to:1939,title:tx('recentContext.laGuerraComienzaEnEuropa'),text:tx('recentContext.alemaniaInvadePoloniaEnSeptiembre'),source:'https://encyclopedia.ushmm.org/content/en/article/invasion-of-poland-fall-1939'},
 {from:1940,to:1940,title:tx('recentContext.laExpansionDeLaOcupacion'),text:tx('recentContext.alemaniaOcupaDinamarcaNoruegaLos'),source:'https://encyclopedia.ushmm.org/content/en/article/german-invasion-of-western-europe-may-1940'},
 {from:1941,to:1941,title:tx('recentContext.unaGuerraMundial'),text:tx('recentContext.laInvasionAlemanaDeLa'),source:'https://encyclopedia.ushmm.org/content/en/article/world-war-ii-in-europe'},
 {from:1942,to:1942,title:tx('recentContext.elMundoEnGuerra1942'),text:tx('recentContext.laAlemaniaNaziDominaGran'),source:'https://encyclopedia.ushmm.org/content/en/map/german-administration-of-europe-1942'},
 {from:1943,to:1944,title:tx('recentContext.elRetrocesoDelEje'),text:tx('recentContext.losAvancesAliadosYSovieticos'),source:'https://encyclopedia.ushmm.org/content/en/article/world-war-ii-in-europe'},
 {from:1945,to:1948,title:tx('recentContext.elFinalDeLaGuerra'),text:tx('recentContext.laDerrotaDelEjeAbre'),source:us+'1945-1952/occupation-germany'},
 {from:1949,to:1955,title:tx('recentContext.estadosBloquesYNuevasFronteras'),text:tx('recentContext.laDivisionDeAlemaniaEl'),source:'https://icr.ethz.ch/data/cshapes/'},
 {from:1956,to:1956,title:tx('recentContext.suezYElSinai'),text:tx('recentContext.laCrisisDeSuezLleva'),source:us+'1953-1960/suez'},
 {from:1957,to:1966,title:tx('recentContext.laDescolonizacionTransformaElMundo'),text:tx('recentContext.numerososTerritoriosDeAfricaY'),source:'https://www.un.org/dppa/decolonization/en/about'},
 {from:1967,to:1978,title:tx('recentContext.fronterasYTerritoriosOcupados'),text:tx('recentContext.trasLaGuerraDe1967'),source:us+'1961-1968/arab-israeli-war-1967'},
 {from:1979,to:1981,title:tx('recentContext.laPazEntreEgiptoE'),text:tx('recentContext.elTratadoDe1979Inicia'),source:us+'1977-1980/camp-david'},
 {from:1982,to:1988,title:tx('recentContext.elSinaiVuelveALa'),text:tx('recentContext.laRetiradaPrincipalIsraeliDel'),source:'https://sis.gov.eg/es/egipto/fiestas-y-ocasiones/aniversario-del-regreso-de-taba-a-la-soberan%C3%ADa-egipcia/'},
 {from:1989,to:1991,title:tx('recentContext.elFinalDelOrdenBipolar'),text:tx('recentContext.laReunificacionAlemanaEn1990'),source:us+'1989-1992/collapse-soviet-union'},
 {from:1992,to:2010,title:tx('recentContext.nuevosEstadosYReorganizacionTerritorial'),text:tx('recentContext.laDisolucionDeYugoslaviaLa'),source:'https://icr.ethz.ch/data/cshapes/'},
 {from:2011,to:2013,title:tx('recentContext.unNuevoEstadoSudanDel'),text:tx('recentContext.sudanDelSurSeIndependiza'),source:'https://www.un.org/en/about-us/member-states/south-sudan'},
 {from:2014,to:2019,title:tx('recentContext.crimeaSoberaniaYOcupacion'),text:tx('recentContext.desde2014CrimeaApareceComo'),source:'https://press.un.org/en/2014/ga11493.doc.htm'},
 {from:2020,to:9999,title:tx('recentContext.elMundoContemporaneo'),text:tx('recentContext.paisesCapitalesGrandesCiudadesE'),source:'https://data.worldbank.org/'}
];
export function recentContext(year:number){const c=recentContexts.find(c=>year>=c.from&&year<=c.to);return c?{...c,sourceLabel:year>=2020?tx('recentContext.bancoMundialIndicadores'):tx('recentContext.contextoYDocumentacion')}:undefined;}
export function entityContext(name:string,year:number):{text:string;source:string}|undefined{
 if(/United States|Estados Unidos/.test(name)&&year>=2020)return {text:tx('recentContext.estadosUnidosEsUnaRepublica'),source:'https://www.usa.gov/states-and-territories'};
 if(/India|Pakistan|Bangladesh/.test(name)&&year>=1900&&year<=1947)return {text:year<1947?tx('recentContext.laIndiaBritanicaSeEncuentra'):tx('recentContext.indiaYPakistanAlcanzanLa'),source:'https://www.nationalarchives.gov.uk/education/resources/indian-independence/'};
 if(/Germany|German|Alemania/.test(name)&&year>=1933&&year<=1948)return {text:year<1945?tx('recentContext.alemaniaEstaBajoLaDictadura'):tx('recentContext.trasLaDerrotaDe1945'),source:'https://encyclopedia.ushmm.org/content/en/article/world-war-ii-in-europe'};
 if(/Egypt|Israel|Syria|Gaza|West Bank|Palestine/.test(name)&&year>=1948)return {text:year<1967?tx('recentContext.elConflictoArabeIsraeliDe'):year<=1981?tx('recentContext.laGuerraDe1967Da'):tx('recentContext.elSinaiSeEncuentraBajo'),source:us+'1961-1968/arab-israeli-war-1967'};
 if(/Ukraine|Russia|Ucrania|Rusia/.test(name)&&year>=2014)return {text:tx('recentContext.laOnuReafirmaLaSoberania'),source:'https://press.un.org/en/2014/ga11493.doc.htm'};
 return undefined;
}
