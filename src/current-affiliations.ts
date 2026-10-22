/** Selected current-year conflict observations; memberships live in historical-affiliations.ts. */
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
    id: 'ukraine-2026', title: 'Guerra de Rusia contra Ucrania', countries: ['UKR', 'RUS'],
    text: 'La declaración de Dubrovnik de abril de 2026 documenta la continuidad de la guerra de Rusia contra Ucrania. Este contexto no reconstruye las líneas del frente ni modifica las fronteras reconocidas.',
    source: 'https://vlada.gov.hr/UserDocsImages/Vijesti/2026/Travanj/28_travnja/Political_Declaration_of_the_11th_Three_Seas_Initiative_Summit.pdf', sourceLabel: 'Declaración de Dubrovnik, 28–29 abril 2026', referenceDate: '2026-04-29',
  },
  {
    id: 'iran-2026', title: 'Hostilidades entre Irán, Estados Unidos e Israel', countries: ['IRN', 'USA', 'ISR'],
    text: 'La misión internacional independiente de la ONU informó al Consejo de Derechos Humanos sobre la campaña militar de Estados Unidos e Israel contra Irán iniciada el 28 de febrero de 2026 y sus consecuencias para la población civil.',
    source: 'https://www.unognewsroom.org/teleprompter/en/3270/hrc-63-human-rights-in-iran-21-september-2026/9704',
    sourceLabel: 'ONU, Consejo de Derechos Humanos, 21 septiembre 2026', referenceDate: '2026-09-21',
  },
  {
    id: 'palestine-2026', title: 'Gaza y Cisjordania', countries: ['PSE', 'PSX', 'ISR'],
    text: 'OCHA documenta la situación humanitaria, el desplazamiento, las restricciones de acceso y la violencia en el territorio palestino ocupado. Las condiciones de Gaza y Cisjordania se describen por separado en el informe.',
    source: 'https://www.un.org/unispal/wp-content/uploads/2026/05/Humanitarian-Situation-Report-_-1-May-2026-_-United-Nations-Office-for-the-Coordination-of-Humanitarian-Affairs-Occupied-Palestinian-Territory.pdf',
    sourceLabel: 'OCHA, informe humanitario, 1 mayo 2026', referenceDate: '2026-05-01',
  },
  {
    id: 'sudan-2026', title: 'Conflicto armado en Sudán', countries: ['SDN'],
    text: 'UNICEF describe en su balance de enero a junio de 2026 la continuidad del conflicto y sus efectos sobre el desplazamiento, la alimentación, la salud y los servicios esenciales.',
    source: 'https://www.unicef.org/sudan/reports/unicef-sudan-humanitarian-mid-year-situation-report-2026',
    sourceLabel: 'UNICEF Sudán, balance del primer semestre de 2026', referenceDate: '2026-06-30',
  },
  {
    id: 'myanmar-2026', title: 'Conflictos armados en Myanmar', countries: ['MMR'],
    text: 'El plan humanitario de la ONU para 2026 identifica los conflictos armados, el desplazamiento y las restricciones de acceso entre los factores de la crisis, agravada por desastres y deterioro económico.',
    source: 'https://myanmar.un.org/en/308519-myanmar-humanitarian-needs-and-response-plan-2026',
    sourceLabel: 'ONU/OCHA, plan humanitario de Myanmar para 2026', referenceDate: '2025-12-10',
  },
  {
    id: 'drc-2026', title: 'Conflicto en el este de la República Democrática del Congo', countries: ['COD'],
    text: 'ACNUR registra en su actualización regional de diciembre de 2025 a marzo de 2026 violencia de grupos armados, desplazamiento y riesgos graves de protección en Kivu del Norte y Kivu del Sur.',
    source: 'https://www.unhcr.org/sites/default/files/2026-04/update-eastern-drc-situation-regional-external-update-december-2025-march-2026.pdf',
    sourceLabel: 'ACNUR, actualización regional, diciembre 2025–marzo 2026', referenceDate: '2026-03-31',
  },
  {
    id: 'yemen-2026', title: 'Recrudecimiento de la guerra en Yemen', countries: ['YEM'],
    text: 'El enviado especial de la ONU informó al Consejo de Seguridad el 9 de octubre de 2026 de una nueva extensión de las hostilidades y del deterioro humanitario, con combates en varios frentes.',
    source: 'https://dppa.un.org/en/node/136980', sourceLabel: 'Enviado especial de la ONU, 9 octubre 2026', referenceDate: '2026-10-09',
  },
];

export function currentConflicts(code: string, year: number): CurrentConflict[] {
  return year === AFFILIATION_REFERENCE_YEAR ? CURRENT_CONFLICTS.filter(conflict => conflict.countries.includes(code)) : [];
}
