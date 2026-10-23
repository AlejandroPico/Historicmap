"""Bounded, sourced authority corrections for the 1970–1989 expansion.

Default is a read-only review. Pass --apply to merge only this acquisition tag.
No network, portrait downloads, manifest rewriting or unrelated leader removal.
Annual/month bounds are explicitly precision-labelled, never exact handover dates.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = 'curated-americas-africa-0.8'
ANNUAL = ('Fechas con precisión anual: los extremos de calendario delimitan los '
          'años documentados de ejercicio y no acreditan presencia durante todo '
          'el año ni días exactos de toma de posesión o cese.')
MONTHLY = ('Fechas con precisión mensual: los extremos de calendario delimitan '
           'los meses documentados, no días exactos de relevo.')
TERMS = []


def term(country, person, name, role, start, end, source, precision=11, note=''):
    if precision == 9:
        note = (note + ' ' + ANNUAL).strip()
    elif precision == 10:
        note = (note + ' ' + MONTHLY).strip()
    TERMS.append(dict(country=country, person=person, name=name, role=role,
                      start=start, end=end, source=source, precision=precision,
                      curated=True, acquisition=TAG, note=note))


panama = 'https://repositorio.asamblea.gob.pa/bitstream/handle/001/1803/2015_LNB_2015_520_LNB.pdf?isAllowed=y&sequence=1'
term('PAN','Q888447','Demetrio Basilio Lakas','Presidente de la República · jefatura formal del Estado',
     '1969-01-01','1978-12-31',panama,9,
     'Presidencia civil durante el predominio militar de Torrijos; no se confunde con el dirigente de facto. La primera etapa desde 1969 está acreditada también en los registros diplomáticos de visitas de 1970: https://history.state.gov/departmenthistory/visits/panama')
term('PAN','Q888903','Ricardo de la Espriella','Presidente de la República · jefatura formal del Estado',
     '1982-01-01','1984-12-31',panama,9)
term('PAN','Q685368','Jorge Illueca','Presidente de la República · jefatura formal del Estado',
     '1984-01-01','1984-12-31',panama,9,
     'Su ejercicio presidencial en febrero de 1984 consta en el comunicado de Contadora transmitido a la ONU: https://digitallibrary.un.org/record/122375/files/S_SUPP_1984_1--%5EOR_SC_1984_I%5E-EN.pdf')
term('PAN','Q201665','Nicolás Ardito Barletta','Presidente de la República · jefatura formal del Estado',
     '1984-10-11','1985-09-28','https://bdigital.binal.ac.pa/bdp/republicano18.pdf',11,
     'Toma de posesión y dimisión documentadas en la historia republicana conservada por la Biblioteca Nacional de Panamá.')
term('PAN','Q332055','Omar Torrijos','Dirigente militar de facto · Guardia Nacional',
     '1968-01-01','1981-12-31','https://www.clintonlibrary.gov/research/archives/finding-aids/ernesto-balladeres',9,
     'No fue presidente de la República. La autoridad de facto se muestra separada de las presidencias civiles formales.')
term('PAN','Q192667','Manuel Antonio Noriega','Dirigente de facto · Fuerzas de Defensa',
     '1983-01-01','1989-12-31','https://www.archives.gov/files/declassification/iscap/pdf/2016-220-pt-3-release-material-completed.pdf',9,
     'Control militar y político separado de las jefaturas civiles formales; no se le atribuye una presidencia constitucional. Consolidación y pérdida de control dentro de los años extremos.')

term('VEN','Q311323','Rafael Caldera','Presidente de la República · primer mandato',
     '1969-01-01','1974-12-31','https://rafaelcaldera.com/5-anos-de-cambio-1974/',9,
     'Memoria de gestión de la Oficina Central de Información de Venezuela, editada en 1975; no se fusiona con su segundo mandato de los años noventa.')

ecuador = 'https://institutodemocracia.gob.ec/wp-content/uploads/2020/05/libro_Antologia.pdf'
term('ECU','Q707171','José María Velasco Ibarra','Presidente · quinto mandato, constitucional y luego de facto',
     '1968-01-01','1972-12-31','https://repositorio.bce.ec/bitstream/32000/2883/1/8516_.pdf',9,
     'Quinto mandato; el ejercicio posterior al autogolpe de 1970 no equivale a continuidad de las instituciones constitucionales anteriores.')
term('ECU','Q728490','Guillermo Rodríguez Lara','Presidente de facto · Gobierno militar',
     '1972-01-01','1976-12-31',ecuador,9,
     'Su relevo ocurrió en 1976; las fuentes consultadas no se utilizan aquí para resolver discrepancias del día exacto de enero.')
term('ECU','Q734584','Alfredo Poveda Burbano','Presidente del Consejo Supremo de Gobierno · jefatura de facto',
     '1976-01-01','1979-12-31',ecuador,9,
     'Consejo militar integrado también por Guillermo Durán Arcentales y Luis Leoro Franco; el retrato del presidente no convierte el órgano en una presidencia unipersonal. Registro Oficial firmado en septiembre de 1976: https://www.flacso.edu.ec/portal/pnTemp/PageMaster/11hwqj98zeartmawqgfomoxqu8tp3w.pdf')

guatemala = 'https://biblioteca.oj.gob.gt/digitales/56839.pdf'
term('GTM','Q887011','Kjell Eugenio Laugerud García','Presidente de la República',
     '1974-07-01','1978-07-01',guatemala)
term('GTM','Q705460','Fernando Romeo Lucas García','Presidente de la República',
     '1978-07-01','1982-03-23',guatemala)

salvador = 'https://1997-2001.state.gov/background_notes/elsal_0008_bgn.html'
term('SLV','Q880982','Carlos Humberto Romero','Presidente de la República',
     '1977-07-01','1979-10-15','https://www.csj.gob.sv/marco-historico/judicial-acuerdos-de-paz/',11,
     'La Corte Suprema documenta su toma de posesión en julio de 1977; el golpe del 15 de octubre de 1979 está documentado también por la CIDH/ONU: https://digitallibrary.un.org/record/104856/files/E_CN.4_1453-ES.pdf')
term('SLV','SLV-JUNTA-1979','Junta Revolucionaria de Gobierno','Órgano colegiado · jefatura cívico-militar',
     '1979-10-15','1982-05-02',salvador,11,
     'Composición cambiante. La primera junta incluyó a Adolfo Arnoldo Majano, Jaime Abdul Gutiérrez, Guillermo Ungo, Román Mayorga Quirós y Mario Andino. Duarte se incorporó en marzo de 1980; no se atribuye a sus miembros una permanencia idéntica durante todo el órgano.')
term('SLV','Q360283','José Napoleón Duarte','Presidente de la Junta Revolucionaria de Gobierno',
     '1980-12-01','1982-05-31','https://www.icj.org/wp-content/uploads/2013/07/ICJ-Review-26-1981-spa.pdf',10,
     'Presidencia de la junta desde diciembre de 1980, distinta de su presidencia electa de 1984–1989. Informe jurídico contemporáneo de 1981; relevo por Álvaro Magaña en mayo de 1982.')

term('NIC','NIC-JUNTA-1972','Junta Nacional de Gobierno','Órgano colegiado · Poder Ejecutivo formal',
     '1972-05-01','1974-11-30','https://docs.nicaragua.justia.com/nacionales/decretos-legislativos/crease-junta-nacional-de-gobierno-apr-26-1972.pdf',11,
     'Decreto n.º 2, La Gaceta n.º 91 de 26 de abril de 1972. Tres miembros y sustituciones internas; no se inventa un presidente individual ni un retrato del órgano. El predominio de Somoza y el Comité de Emergencia se distinguen de esta jefatura formal.')
term('NIC','NIC-JGRN-1979','Junta de Gobierno de Reconstrucción Nacional','Órgano colegiado · Poder Ejecutivo de transición',
     '1979-07-18','1985-01-10','https://sajurin.enriquebolanos.org/docs/G-1985-01-04.pdf',11,
     'El decreto n.º 1543 regula el relevo de enero de 1985. La instalación de julio de 1979 y su programa están documentados en https://www.unanleon.edu.ni/unan-leon-conmemora-46-anos-de-instalacion-de-la-junta-de-gobierno-de-reconstruccion-nacional/ . Miembros iniciales: Daniel Ortega, Sergio Ramírez, Moisés Hassan, Violeta Barrios de Chamorro y Alfonso Robelo; la composición cambió en 1980–1981. No se presenta como presidencia electa de Ortega desde 1979.')

benin = 'https://digitallibrary.un.org/record/564622/files/S_12294_Rev.1-FR.pdf'
term('BEN','Q881211','Paul-Émile de Souza','Presidente del Directorio militar',
     '1969-12-01','1970-05-31','https://developpement.gouv.bj/media/MEMOIRE_PATRIMOINE_MPD.pdf',10,
     'El inventario ministerial oficial sitúa su ejercicio hasta el 7 de mayo de 1970; se conserva precisión mensual por discrepancias en el comienzo de diciembre de 1969.')
term('BEN','Q336242','Hubert Maga','Presidente del Consejo Presidencial · presidencia rotatoria',
     '1970-05-01','1972-05-31',benin,10,
     'Consejo formado por Maga, Sourou Migan Apithy y Justin Ahomadégbé-Tomêtin. La presidencia de Maga comenzó el 7 de mayo de 1970; Ahomadégbé lo relevó en mayo de 1972.')
term('BEN','Q438852','Justin Ahomadégbé-Tomêtin','Presidente del Consejo Presidencial · presidencia rotatoria',
     '1972-05-01','1972-10-31',benin,10,
     'Depuesto el 26 de octubre de 1972; no se le atribuye el turno completo de dos años previsto por el Consejo.')
term('BEN','Q206719','Mathieu Kérékou','Presidente · régimen militar revolucionario y primera etapa',
     '1972-01-01','1991-12-31','https://dan.gouv.bj/documentheque/fonds-recents',9,
     'Toma del poder el 26 de octubre de 1972. Primera etapa continua hasta abril de 1991, separada de su regreso electoral de 1996; contraste de sucesión: https://srtb.bj/les-chefs-detat-du-benin-depuis-1960-qui-est-qui-et-qui-a-fait-quoi/')
term('NER','Q353198','Seyni Kountché','Presidente del Consejo Militar Supremo · jefatura del Estado',
     '1974-04-15','1987-11-10','https://anp.ne/38eme-anniversaire-de-la-disparition-du-general-seyni-kountche-un-officier-au-destin-singulier/',11,
     'Ordenanza n.º 74-2 de 22 de abril de 1974 y gobiernos sucesivos en la documentación diplomática: https://ambniger-mali.org/images/pdf/Liste-du-gouvernement-successif.pdf')
term('TCD','Q365169','Félix Malloum','Jefe del Estado · Consejo Superior Militar; después presidente',
     '1975-01-01','1979-12-31','https://history.state.gov/historicaldocuments/frus1977-80v17p3/persons',9,
     'Cambio de título a presidente en agosto de 1978; cese el 23 de marzo de 1979. La precisión anual evita convertir discrepancias sobre abril/mayo de 1975 en un día certificado.')
term('LBR','Q294618','Samuel Kanyon Doe','Presidente del Consejo de Redención Popular · jefatura militar del Estado',
     '1980-04-12','1986-01-05','https://www.reaganlibrary.gov/public/digitallibrary/smof/execsec-country/box-002/40-748-12026383-002-050-2018.pdf',11,
     'Jefatura militar anterior a la presidencia constitucional de 1986. La constitución y transición institucional se consultan separadamente: https://judiciary.gov.lr/constitution-of-liberia-2/')
term('SWZ','Q444261','Ntombi Tfwala','Ndlovukati · reina regente',
     '1983-01-01','1986-12-31','https://www.icj.org/wp-content/uploads/2013/10/CIJL-Bulletin-1920-1987-eng.pdf',9,
     'Regencia durante la minoría de Mswati III, antes de su entronización del 25 de abril de 1986; no se confunde con la posterior condición de reina madre. Acto firmado por Ntombi como regente en 1985: https://archive.gazettes.africa/archive/sz/1985/sz-government-gazette-supplement-dated-1985-06-14-no-367.pdf')
term('SLE','Q515657','Siaka Stevens','Primer ministro · Gobierno anterior a la República',
     '1970-01-01','1970-12-31','https://www.congress.gov/91/crecb/1970/04/29/GPO-CRECB-1970-pt10-4-2.pdf',9,
     'Ventana acreditada de 1970 dentro de un mandato más amplio; el registro no pretende fijar su comienzo ni su cese. Su presidencia republicana desde abril de 1971 se conserva por separado.')

rhodesia = 'https://2009-2017.state.gov/outofdate/bgn/zimbabwe/26035.htm'
term('RHO','Q313424','Ian Douglas Smith','Primer ministro de facto · régimen rodesiano no reconocido',
     '1965-11-11','1979-06-01',rhodesia,11,
     'Jefatura del Gobierno autoproclamado; no se presenta como soberanía reconocida ni como dirigente del Zimbabue independiente. Q313424 identifica al político; Q57247212 corresponde a un arqueólogo homónimo y no debe reutilizarse.')
term('RHO','Q318479','Abel Muzorewa','Primer ministro de Zimbabue-Rodesia · Gobierno no reconocido',
     '1979-06-01','1979-12-11',rhodesia,11,
     'El acuerdo interno y las elecciones de 1979 no pusieron fin al conflicto ni produjeron reconocimiento internacional de independencia.')
term('RHO','Q336050','Christopher Soames','Gobernador británico · administración de transición',
     '1979-12-12','1980-04-17','https://publications.parliament.uk/pa/cm200405/cmselect/cmfaff/111/111we03.htm',11,
     'Restablecimiento de la administración británica previo a la independencia del 18 de abril de 1980. No se le atribuye el cargo de presidente rodesiano.')


def apply():
    path = ROOT / 'public/data/identities.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    countries = data['countries']
    countries.setdefault('RHO',dict(qid='Q217169',name='Rodesia · régimen no reconocido',flags=[],leaders=[]))
    missing = sorted({t['country'] for t in TERMS} - countries.keys())
    if missing:
        raise ValueError('Create identities before applying corrections: ' + ', '.join(missing))
    portraits = {leader['person']: leader['portrait']
                for country in countries.values() for leader in country['leaders']
                if leader.get('portrait')}
    for country in countries.values():
        country['leaders'] = [l for l in country['leaders'] if l.get('acquisition') != TAG]
    for record in TERMS:
        leader = {k: v for k, v in record.items() if k != 'country'}
        if leader['person'] in portraits:
            leader['portrait'] = portraits[leader['person']]
        countries[record['country']]['leaders'].append(leader)
    for country in countries.values():
        country['leaders'].sort(key=lambda l: (l['start'], l['name'], l['role']))
    path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    return sum(t['person'] in portraits for t in TERMS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    print(f'{len(TERMS)} bounded terms, {len({t["country"] for t in TERMS})} identities.')
    if args.apply:
        print(f'Applied {TAG}; reused {apply()} licensed portraits; no media altered.')
    else:
        for t in TERMS:
            print(t['country'],t['person'],t['start'],t['end'],f'precision={t["precision"]}',t['name'])
