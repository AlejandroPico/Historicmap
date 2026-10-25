"""Bounded Asian, African and Pacific authority research,1880–1899.

Pure/idempotent curate(data). No network, media acquisition, public-data or
manifest mutation. CLI requires an explicit output. Dates are Gregorian where
daily precision is supported. Coverage observations do not invent accessions.
See docs/AUTHORITIES-1880-ASIA-AFRICA.md before integrating map identities.
"""
import argparse
import copy
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIRST, LAST = '1880-01-01', '1899-12-31'
TAG = 'curated-1880-asia-africa-0.13'

SEEDS = {
    'JOS': ('Q28405', 'Corea · reino de Joseon'),
    'KEM': ('Q28233', 'Imperio de Corea'),
    'ZAN': ('Q1774', 'Sultanato de Zanzíbar'),
    'HAW-KINGDOM': ('Q156418', 'Reino de Hawái'),
    'HAW-PROVISIONAL': ('', 'Hawái · Gobierno provisional'),
    'HAW-REPUBLIC': ('Q1057542', 'República de Hawái'),
    'HAW': ('', 'Hawái · administración tras la anexión estadounidense'),
    'ZUL': ('Q13558877', 'Zululandia · monarquía y territorios fragmentados'),
    'HIST-Q1071439': ('Q1071439', 'Reino merina · Madagascar'),
}


def curate(incoming):
    data = copy.deepcopy(incoming)
    cs = data['countries']
    portraits = {l['person']: copy.deepcopy(l['portrait'])
                 for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for c in cs.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    # Existing identifiers/names are preserved; these are only missing seeds.
    for key, (qid, name) in SEEDS.items():
        cs.setdefault(key, dict(qid=qid, name=name, flags=[], leaders=[]))

    def term(key, person, name, role, start, end, source, note='', precision=11,
             start_coverage=False, end_coverage=False):
        assert FIRST <= start <= end <= LAST
        cs.setdefault(key, dict(qid='', name=key, flags=[], leaders=[]))
        # Remove conflicting generic copies only inside the reviewed window.
        # Statements reaching1900 are byte-identical. Two newly curated roles
        # for one person are not erased by this bounded cleanup.
        kept = []
        for old in cs[key]['leaders']:
            if (old['person'] != person or old.get('curated') or
                    old['end'] >= '1900-01-01' or old['start'] > LAST or old['end'] < FIRST):
                kept.append(old)
            elif old['start'] < FIRST:
                earlier = copy.deepcopy(old)
                earlier.update(end='1879-12-31', endIsCoverageBoundary=True)
                kept.append(earlier)
        cs[key]['leaders'] = kept
        row = dict(person=person, name=name, role=role, start=start, end=end,
                   source=source, note=note, precision=precision,
                   curated=True, acquisition=TAG)
        if start_coverage:
            row['startIsCoverageBoundary'] = True
        if end_coverage:
            row['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            row['note'] += ' Los extremos de cobertura delimitan la evidencia o la revisión; no son un nombramiento ni una dimisión.'
        if person in portraits:
            row['portrait'] = copy.deepcopy(portraits[person])
        cs[key]['leaders'].append(row)
        return row

    qing = 'https://english.visitbeijing.com.cn/article/47ON76ql8M0'
    term('QING', 'Q299710', 'Guangxu', 'Emperador de la dinastía Qing', FIRST, LAST, qing,
         'Soberano formal desde1875. Ejercicio personal1889–1898 bajo la influencia deCixi; queda recluido tras la supresión de las reformas de1898. No se confunde título imperial con poder efectivo.',
         start_coverage=True, end_coverage=True)
    term('QING', 'Q47842', 'Cixi', 'Emperatriz viuda · regencia e influencia decisiva', FIRST, '1889-12-31', qing,
         'Regencia durante la minoría deGuangxu; la fuente sitúa el inicio de su gobierno personal en1889 sin fijar aquí el día del traspaso. Precisión anual, no regencia continua hasta1898.',
         precision=9, start_coverage=True, end_coverage=True)
    term('QING', 'Q47842', 'Cixi', 'Emperatriz viuda · restablecimiento del poder efectivo', '1898-12-31', LAST, qing,
         'Restablece el control tras la represión de las reformas de1898. Esta observación al cierre1898 no pretende fechar el golpe en diciembre ni negar su influencia anterior.',
         precision=9, start_coverage=True, end_coverage=True)

    japan = 'https://www.kunaicho.go.jp/kunaicho/kunaicho/kunaicho-nenpyo.html'
    term('JPN', 'Q174231', 'Mutsuhito · emperador Meiji', 'Emperador de Japón', FIRST, LAST, japan,
         'Reinado1867–1912, distinto de las sucesivas jefaturas del Gobierno. Los acontecimientos anteriores a1873 de la cronología japonesa usan otro calendario; la ventana1880–1899 ya es gregoriana.',
         start_coverage=True, end_coverage=True)
    cabinet = 'https://japan.kantei.go.jp/past_cabinet/index.html'
    sanjo = 'https://www.ndl.go.jp/portrait/e/datas/97/?lang=en'
    term('JPN','Q516646','Sanjō Sanetomi','Daijō-daijin · gran ministro de Estado',FIRST,'1885-12-21',sanjo,
         'La Biblioteca Nacional de la Dieta documenta el cargo1871–1885, antes de la creación del gabinete moderno. No se retrotrae el título de primer ministro a1880.',start_coverage=True)
    for person,name,start,end in [
        ('Q174971','Itō Hirobumi','1885-12-22','1888-04-30'),
        ('Q714049','Kuroda Kiyotaka','1888-04-30','1889-10-25'),
        ('Q516646','Sanjō Sanetomi','1889-10-25','1889-12-24'),
        ('Q297636','Yamagata Aritomo','1889-12-24','1891-05-06'),
        ('Q714039','Matsukata Masayoshi','1891-05-06','1892-08-08'),
        ('Q174971','Itō Hirobumi','1892-08-08','1896-08-31'),
        ('Q714049','Kuroda Kiyotaka','1896-08-31','1896-09-18'),
        ('Q714039','Matsukata Masayoshi','1896-09-18','1898-01-12'),
        ('Q174971','Itō Hirobumi','1898-01-12','1898-06-30'),
        ('Q243141','Ōkuma Shigenobu','1898-06-30','1898-11-08'),
        ('Q297636','Yamagata Aritomo','1898-11-08',LAST),
    ]:
        acting = (person,start) in {('Q516646','1889-10-25'),('Q714049','1896-08-31')}
        term('JPN',person,name,'Jefatura del Gobierno · en funciones' if acting else 'Primer ministro de Japón',
             start,end,sanjo if person=='Q516646' else cabinet,
             'La institución del gabinete se crea22/12/1885. Las suplencias y la numeración oficial de gabinetes no son lo mismo; se conserva la fecha de sustitución sin borrar mandatos repetidos.',
             end_coverage=end==LAST)

    korea = 'https://museum.seoul.go.kr/eng/board/NR_boardView.do?bbsCd=1044&seq=20170222133346596'
    term('JOS','Q257425','Gojong','Rey de Joseon',FIRST,'1897-10-11',korea,
         'Rey desde1863. El título imperial corresponde al12/10/1897; no se denomina emperador aGojong en1880 ni se retrotrae el protectorado japonés de1905.',start_coverage=True)
    term('KEM','Q257425','Gojong','Emperador de Corea','1897-10-12',LAST,korea,
         'Proclamación del Imperio deCorea12/10/1897. La adopción de la eraGwangmu y la proclamación estatal tienen cronologías relacionadas, pero no se confunden con una nueva persona.',end_coverage=True)

    siam = 'https://www.unesco.org/en/memory-world/archival-documents-king-chulalongkorns-transformation-siam-1868-1910'
    term('THA','Q158861','Chulalongkorn · Rama V','Rey de Siam',FIRST,LAST,siam,
         'Soberano1868–1910. Los archivos reales documentan reformas y negociaciones bajo presión colonial; los tratados desiguales no equivalen a anexión completa deSiam.',start_coverage=True,end_coverage=True)

    burma = 'https://www.moi.gov.mm/moi:eng/index.php/article/16549'
    term('MMR','Q470986','Thibaw Min','Rey de Birmania · dinastía Konbaung',FIRST,'1885-11-28',burma,
         'Toma británica deMandalay28/11/1885; traslado del rey al exilio al día siguiente. La proclamación de anexión de1886 y la resistencia posterior son hitos diferentes. No se prolonga el Gobierno real hasta su muerte1916.',start_coverage=True)

    afghan = 'https://www.nam.ac.uk/explore/second-afghan-war'
    term('AFG','Q31649','Abdur Rahman Khan','Emir de Afganistán · Gobierno interno y tutela exterior británica','1880-07-31',LAST,afghan,
         'El museo fecha el ofrecimiento del trono en julio1880. La observación al cierre del mes no fija el día de acceso; el acuerdo restringe relaciones exteriores, sin convertir al emir en gobernador británico.',precision=10,start_coverage=True,end_coverage=True)

    iran = 'https://www.iranicaonline.org/articles/iran-ii2-islamic-period-page-5/'
    term('IRN','Q159416','Naser al-Din Shah Qajar','Shah de Persia · dinastía Qajar',FIRST,'1896-05-01',iran,
         'Asesinado1/5/1896 tras un reinado iniciado en1848. La ceremonia y llegada del sucesor aTeherán son posteriores a la sucesión.',start_coverage=True)
    term('IRN','Q467021','Mozaffar al-Din Shah Qajar','Shah de Persia · dinastía Qajar','1896-05-01',LAST,iran,
         'Sucede al soberano asesinado en mayo1896; las ceremonias posteriores no se usan como si fuesen el comienzo de un Estado distinto.',end_coverage=True)
    term('OTT','Q134817','Abdülhamid II','Sultán del Imperio otomano',FIRST,LAST,
         'https://ttk.gov.tr/osmanli-padisahlari/',
         'Soberano1876–1909. La suspensión parlamentaria y las relaciones de vasallaje no permiten atribuir independencia uniforme a todos los territorios del contorno.',start_coverage=True,end_coverage=True)

    congo = 'https://agatha.arch.be/data/ead/BE-A0545_724272_807520/annexes/BE-A0545_724272_807520_fre.ead.pdf'
    term('CFS','Q12967','Leopoldo II','Soberano del Estado Libre del Congo · unión personal','1885-12-31',LAST,congo,
         'El archivo belga distingue autorización parlamentaria30/4/1885 y establecimiento/notificaciones del nuevo Estado. La observación al cierre1885 no fija una fundación31/12 ni autoriza retrotraer este Estado a1880. No es colonia del Estado belga antes1908.',start_coverage=True,end_coverage=True)

    ethiopia = 'https://betamasaheft.awhamburg.de/persons/PRS10378Yohanne/main'
    term('ETH','Q315659','Yohannes IV','Emperador de Etiopía',FIRST,'1889-01-01',ethiopia,
         'La investigación manuscrita documenta actividad imperial1872–1889 y muerte en la batalla deMatamma. Precisión anual: no afirma muerte el1de enero; el cierre del mandato necesita la cronología diaria de la batalla.',precision=9,start_coverage=True,end_coverage=True)
    term('ETH','Q244748','Menelik II','Emperador de Etiopía','1889-12-31',LAST,
         'https://archivesdiplomatiques.diplomatie.gouv.fr/ark:/14366/zr6j7qsh920n',
         'El archivo diplomático conserva el acceso de1889 y el tratado deUcciali2/5/1889; la observación al cierre del año no fija la fecha de proclamación ni coronación. La interpretación italiana de protectorado fue disputada, no una anexión aceptada.',precision=9,start_coverage=True,end_coverage=True)

    madagascar = 'https://www.fjkm.mg/ny-fjkm/tantara-sy-arsiva/histoire-ranavalona-ii/'
    term('HIST-Q1071439','Q240168','Ranavalona II','Reina de Madagascar · monarquía merina',FIRST,'1883-07-13',madagascar,
         'Soberana1868–1883, con Gobierno cotidiano deRainilaiarivony. Su muerte precede al acceso y a la coronación deRanavalonaIII.',start_coverage=True)
    term('HIST-Q1071439','Q233326','Ranavalona III','Reina de Madagascar · después bajo imposición colonial','1883-07-30','1897-02-28',
         'https://www.fjkm.mg/synodamparitany/vaovao-farany/biographie-ranavalona-iii/',
         'La institución malgache distingue el acceso30/7/1883 y el fin28/2/1897. Protectorado1885, invasión1895 y anexión francesa1896 no borran de inmediato la monarquía, abolida por el decreto de1897.')
    term('HIST-Q1071439','Q528996','Rainilaiarivony','Primer ministro del reino de Madagascar',FIRST,'1895-01-01',madagascar,
         'La historia institucional fecha su Gobierno1864–1895. Precisión anual: el extremo normalizado no afirma cese el1de enero. Su autoridad y exilio son distintos de la permanencia nominal de la reina.',precision=9,start_coverage=True,end_coverage=True)

    zulu = 'https://www.nam.ac.uk/explore/zulu-war'
    term('ZUL','Q380403','Cetshwayo kaMpande','Rey zulú depuesto y exiliado · reclamante',FIRST,'1882-12-31',zulu,
         'La monarquía independiente fue suprimida en1879 y el territorio dividido en jefaturas. Esta figura representa la reclamación de la casa real, no Gobierno efectivo de todaZululandia1880–1882.',start_coverage=True,end_coverage=True)
    term('ZUL','Q380403','Cetshwayo kaMpande','Rey restaurado de un territorio zulú reducido','1883-01-31','1884-02-08',
         'https://sahistory.org.za/people/king-cetshwayo',
         'Restitución en enero1883; el inicio observado al cierre del mes no fecha el decreto. Guerra civil y refugio posterior impiden interpretar el cargo como control de todo el contorno.',start_coverage=True)
    term('ZUL','Q888215','Dinuzulu kaCetshwayo','Rey zulú · autoridad territorial disputada','1884-05-20','1887-12-31',
         'https://sahistory.org.za/people/king-cetshwayo',
         'Proclamado20/5/1884 según la biografía del soberano anterior. La anexión británica se produce en1887; el extremo anual no afirma que el Gobierno independiente durara hasta31/12. No se representa como rey de un Estado independiente hasta1913.',precision=9,end_coverage=True)

    brand = 'https://sahistory.org.za/people/johannes-henricus-brand'
    term('ORF','Q1390594','Johannes Henricus Brand','Presidente del Estado Libre de Orange',FIRST,'1888-07-14',brand,
         'Fallece en el cargo14/7/1888; la elección del sucesor y su investidura posterior son hitos separados.',start_coverage=True)
    reitz = 'https://scholar.ufs.ac.za/server/api/core/bitstreams/6759bbf2-4445-49d8-83a5-58847e574705/content'
    term('ORF','Q726327','Francis William Reitz','Presidente del Estado Libre de Orange','1889-01-10','1895-12-11',reitz,
         'La investigación doctoral institucional fecha el mandato10/1/1889–11/12/1895. No confundir con su padre homónimo1810–1881, cuyo identificador es diferente.')
    term('ORF','Q2355196','Marthinus Theunis Steyn','Presidente del Estado Libre de Orange','1896-12-31',LAST,
         'https://www.sacr.fs.gov.za/wp-content/uploads/2012/07/Provincial-Museums-brochure.pdf',
         'ElMuseo de laAntiguaPresidencia documenta la secuenciaBrand/Reitz/Steyn. Ventana desde el cierre1896, no fecha de investidura; no completa las suplencias entre presidentes.',precision=9,start_coverage=True,end_coverage=True)

    tonga = 'https://www.tongatourism.travel/wp-content/uploads/2022/09/Tongatapu-Heritage-Sites.pdf'
    term('TON','Q379840','George Tupou I','Rey de Tonga',FIRST,'1893-01-01',tonga,
         'La documentación patrimonial gubernamental fecha su fallecimiento en1893. Precisión anual, sin afirmar muerte el1de enero. Tonga no era aún el Estado protegido del tratado británico de1900.',precision=9,start_coverage=True,end_coverage=True)
    term('TON','Q379844','George Tupou II','Rey de Tonga','1893-12-31',LAST,tonga,
         'Sucesor en1893; observación al cierre anual sin fabricar fecha de coronación o acceso. La jefatura monárquica local se distingue de la relación exterior británica posterior.',precision=9,start_coverage=True,end_coverage=True)

    cambodia = 'https://tile.loc.gov/storage-services/master/frd/frdcstdy/ca/cambodiacountrys00ross/cambodiacountrys00ross.pdf'
    term('KHM','Q559803','Norodom I','Rey de Camboya · protectorado francés',FIRST,LAST,cambodia,
         'La monarquía conserva el título bajo el tratado de protección de1863. Las imposiciones administrativas de1884 y el reforzamiento del residente francés en1897 restringen su autoridad; no equivalen a que desapareciese toda institución camboyana.',start_coverage=True,end_coverage=True)

    zanzibar = 'https://whc.unesco.org/uploads/nominations/173rev.pdf'
    for person,name,start,end in [
        ('Q703018','Barghash bin Said',FIRST,'1888-01-01'),
        ('Q924354','Khalifa bin Said','1888-12-31','1890-01-01'),
        ('Q423643','Ali bin Said','1890-12-31','1893-01-01'),
        ('Q561747','Hamad bin Thuwaini','1893-12-31','1896-08-25'),
    ]:
        term('ZAN',person,name,'Sultán de Zanzíbar',start,end,zanzibar,
             'La candidatura patrimonial deTanzania documenta la secuencia y los años de los sultanes. Los extremos anuales son observaciones de cobertura, no fechas de acceso o fallecimiento. El protectorado británico desde1890 no convierte al sultán en monarca de una república de1964.',precision=9,start_coverage=True,end_coverage=True)
    war = 'https://sahistory.org.za/article/anglo-zanzibar-war-1896'
    term('ZAN','Q470598','Khalid bin Barghash','Sultán de Zanzíbar · sucesión disputada','1896-08-25','1896-08-27',war,
         'Ocupa el palacio tras la muerte deHamad. La intervención británica del27/8/1896 termina su Gobierno; se conserva este mandato breve y disputado en la ficha anual.')
    term('ZAN','Q928434','Hamoud bin Mohammed','Sultán de Zanzíbar · protectorado británico','1896-08-27',LAST,war,
         'Instalado tras el bombardeo británico del27/8/1896. Título sultánico local y protección británica son funciones diferentes; no se representa soberanía exterior irrestricta.',end_coverage=True)

    hawaii = 'https://www.iolanipalace.org/history/'
    term('HAW-KINGDOM','Q163080','David Kalākaua','Rey de Hawái',FIRST,'1891-01-20',hawaii,
         'Muere enSanFrancisco20/1/1891. La Constitución de1887 restringe su poder; ni el viaje diplomático ni la coronación tardía de1883 son un nuevo acceso al trono.',start_coverage=True)
    term('HAW-KINGDOM','Q107288','Liliʻuokalani','Reina de Hawái','1891-01-20','1893-01-17',hawaii,
         'ElPalacioIolani fecha la sucesión en la muerte de su hermano20/1; la proclamación pública29/1 es distinta. Derrocada17/1/1893; protesta, reclamación posterior y abdicación forzada1895 no prolongan su Gobierno efectivo.')
    national_archives = 'https://www.archives.gov/milestone-documents/joint-resolution-for-annexing-the-hawaiian-islands'
    term('HAW-PROVISIONAL','Q333691','Sanford B. Dole','Presidente del Gobierno Provisional de Hawái','1893-01-17','1894-07-03',national_archives,
         'Gobierno surgido del derrocamiento apoyado por representantes estadounidenses. El reconocimiento unilateral del ministroStevens no convirtió automáticamenteHawái en Estado federado ni anuló la controversia por la restauración de la reina.')
    term('HAW-REPUBLIC','Q333691','Sanford B. Dole','Presidente de la República de Hawái','1894-07-04','1898-08-11',
         'https://libweb.hawaii.edu/digicoll/nupepa_kuokoa/kuokoa_htm/Kuokoa_Essay.pdf',
         'República desde4/7/1894; anexión estadounidense de1898 y organización territorial de1900 son fechas diferentes. No se retrotrae a1893 el título de gobernador territorial.')
    term('HAW','Q333691','Sanford B. Dole','Presidente del Gobierno local de Hawái · transición bajo Estados Unidos','1898-08-12',LAST,
         national_archives,
         'Tras la ceremonia de transferencia12/8/1898 continúa la administración provisional local. ElOrganicAct y el cargo de gobernador territorial corresponden a1900. Esta continuidad administrativa no afirma independencia soberana después de la anexión.',end_coverage=True)

    for c in cs.values():
        c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=pathlib.Path, default=ROOT/'public/data/identities.json')
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    data = curate(json.loads(args.input.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print('Prepared Asian/African/Pacific terms:',sum(l.get('acquisition')==TAG for c in data['countries'].values() for l in c['leaders']))
