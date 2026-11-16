/** Selected current-year conflict observations; memberships live in historical-affiliations.ts. */
import { tx } from './i18n';
export const AFFILIATION_REFERENCE_YEAR=2026;

export interface CurrentConflict {
  id: string;
  title: string;
  text: string;
  countries: readonly string[];
  source: string;
  sourceLabel: string;
  referenceDate: string;
}

/** Selected documented contexts, not an exhaustive register or a legal classification of belligerency. */
export const CURRENT_CONFLICTS: readonly CurrentConflict[] = [
  {
    id: 'ukraine-2026', title: tx('currentAffiliations.guerraDeRusiaContraUcrania'), countries: ['UKR', 'RUS'],
    text: tx('currentAffiliations.laDeclaracionDeDubrovnikDe'),
    source: 'https://vlada.gov.hr/UserDocsImages/Vijesti/2026/Travanj/28_travnja/Political_Declaration_of_the_11th_Three_Seas_Initiative_Summit.pdf', sourceLabel: tx('currentAffiliations.declaracionDeDubrovnik2829'), referenceDate: '2026-04-29',
  },
  {
    id: 'iran-2026', title: tx('currentAffiliations.hostilidadesEntreIranEstadosUnidos'), countries: ['IRN', 'USA', 'ISR'],
    text: tx('currentAffiliations.laMisionInternacionalIndependienteDe'),
    source: 'https://www.unognewsroom.org/teleprompter/en/3270/hrc-63-human-rights-in-iran-21-september-2026/9704',
    sourceLabel: tx('currentAffiliations.onuConsejoDeDerechosHumanos'), referenceDate: '2026-09-21',
  },
  {
    id: 'palestine-2026', title: tx('currentAffiliations.gazaYCisjordania'), countries: ['PSE', 'PSX', 'ISR'],
    text: tx('currentAffiliations.ochaDocumentaLaSituacionHumanitaria'),
    source: 'https://www.un.org/unispal/wp-content/uploads/2026/05/Humanitarian-Situation-Report-_-1-May-2026-_-United-Nations-Office-for-the-Coordination-of-Humanitarian-Affairs-Occupied-Palestinian-Territory.pdf',
    sourceLabel: 'OCHA, informe humanitario, 1 mayo 2026', referenceDate: '2026-05-01',
  },
  {
    id: 'sudan-2026', title: tx('currentAffiliations.conflictoArmadoEnSudan'), countries: ['SDN'],
    text: tx('currentAffiliations.unicefDescribeEnSuBalance'),
    source: 'https://www.unicef.org/sudan/reports/unicef-sudan-humanitarian-mid-year-situation-report-2026',
    sourceLabel: tx('currentAffiliations.unicefSudanBalanceDelPrimer'), referenceDate: '2026-06-30',
  },
  {
    id: 'myanmar-2026', title: tx('currentAffiliations.conflictosArmadosEnMyanmar'), countries: ['MMR'],
    text: tx('currentAffiliations.elPlanHumanitarioDeLa'),
    source: 'https://myanmar.un.org/en/308519-myanmar-humanitarian-needs-and-response-plan-2026',
    sourceLabel: tx('currentAffiliations.onuOchaPlanHumanitarioDe'), referenceDate: '2025-12-10',
  },
  {
    id: 'drc-2026', title: tx('currentAffiliations.conflictoEnElEsteDe'), countries: ['COD'],
    text: tx('currentAffiliations.acnurRegistraEnSuActualizacion'),
    source: 'https://www.unhcr.org/sites/default/files/2026-04/update-eastern-drc-situation-regional-external-update-december-2025-march-2026.pdf',
    sourceLabel: tx('currentAffiliations.acnurActualizacionRegionalDiciembre2025'), referenceDate: '2026-03-31',
  },
  {
    id: 'yemen-2026', title: tx('currentAffiliations.recrudecimientoDeLaGuerraEn'), countries: ['YEM'],
    text: tx('currentAffiliations.elEnviadoEspecialDeLa'),
    source: 'https://dppa.un.org/en/node/136980', sourceLabel: tx('currentAffiliations.enviadoEspecialDeLaOnu'), referenceDate: '2026-10-09',
  },
];

export function currentConflicts(code: string, year: number): CurrentConflict[] {
  return year === AFFILIATION_REFERENCE_YEAR ? CURRENT_CONFLICTS.filter(conflict => conflict.countries.includes(code)) : [];
}
