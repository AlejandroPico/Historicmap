"""Bounded1880 audit-gap curation. Pure/idempotent; no network or public writes.

Only1880..1899 rows are added. Existing flags, portraits and every record
reaching1900 remain intact. CLI requires an explicit output path.
Evidence, precision decisions and unresolved polity gaps are documented in
../docs/AUTHORITIES-1880-GAPS.md.
"""
import argparse
import copy
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIRST, EARLY_LAST, LAST = '1880-01-01', '1885-12-31', '1899-12-31'
TAG = 'curated-1880-audit-gaps-0.13'


def curate(incoming):
    data = copy.deepcopy(incoming)
    countries = data['countries']
    portraits = {l['person']:copy.deepcopy(l['portrait'])
                 for c in countries.values() for l in c['leaders'] if l.get('portrait')}
    for c in countries.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]

    def term(key, person, name, role, start, end, source, note,
             precision=11, start_coverage=False, end_coverage=False):
        assert FIRST <= start <= end <= LAST
        countries.setdefault(key, dict(qid=key[5:] if key.startswith('HIST-Q') else '',
                                       name=key, flags=[], leaders=[]))
        row = dict(person=person, name=name, role=role, start=start, end=end,
                   source=source, note=note, precision=precision,
                   curated=True, acquisition=TAG)
        if start_coverage: row['startIsCoverageBoundary'] = True
        if end_coverage: row['endIsCoverageBoundary'] = True
        if start_coverage or end_coverage:
            row['note'] += ' Los extremos de cobertura delimitan esta observación o revisión; no representan un nombramiento ni un cese.'
        if person in portraits: row['portrait'] = copy.deepcopy(portraits[person])
        countries[key]['leaders'].append(row)
        return row

    nepal_transition = 'https://eprints.soas.ac.uk/33911/1/11015636.pdf'
    term('NPL','Q2523476','Surendra Bikram Shah','Rey de Nepal · autoridad real formal',FIRST,'1881-05-31',nepal_transition,
         'La investigación de archivos diplomáticos sitúa el fallecimiento en mayo1881. Se observa hasta el cierre de ese mes, sin afirmar muerte el31. El Gobierno efectivo corresponde a los primeros ministros Rana.',precision=10,start_coverage=True,end_coverage=True)
    term('NPL','Q886987','Prithvi Bir Bikram Shah','Rey de Nepal · autoridad real formal','1881-05-31',LAST,
         'https://searcharchives.bl.uk/catalog/041-003939737',
         'El archivo fotográfico de la British Library confirma reinado1881–1911; la investigación de SOAS sitúa la sucesión en mayo1881. El inicio normalizado al cierre del mes no es una fecha diaria de acceso; la coronación de diciembre es otro acto.',precision=10,start_coverage=True,end_coverage=True)
    term('NPL','Q593609','Ranodip Singh Kunwar','Primer ministro de Nepal · Gobierno Rana',FIRST,'1885-01-01',
         'https://opmcm.gov.np/pages/former-prime-ministers/',
         'La oficina del primer ministro conserva su período en Bikram Sambat y la British Library identifica el mandato1877–1885. Límite anual observado, sin fingir cese el1de enero. Bir Shumsher tiene su serie posterior propia.',precision=9,start_coverage=True,end_coverage=True)

    morocco = 'https://fr.diplomatie.ma/fr/histoire-du-maroc-rois-et-dynasties'
    term('MAR','Q496845','Hassan I','Sultán de Marruecos · dinastía alauí',FIRST,'1894-01-01',morocco,
         'La representación diplomática marroquí confirma la sucesión de1894. La presión comercial y diplomática extranjera no equivale al protectorado posterior de1912. Extremo anual normalizado, no fecha exacta de muerte.',precision=9,start_coverage=True,end_coverage=True)
    term('MAR','Q307132','Abdelaziz','Sultán de Marruecos · dinastía alauí','1894-12-31',LAST,morocco,
         'Sucesor de HassanI en1894. Esta observación no fija una entronización31/12 ni atribuye al menor todo el ejercicio cotidiano del Gobierno; la regencia deBaAhmed necesita registro propio.',precision=9,start_coverage=True,end_coverage=True)
    term('OMN','Q580930','Turki bin Said Al Busaidi','Sultán de Mascate y Omán',FIRST,'1888-06-04',
         'https://www.qdl.qa/en/archive/81055/vdc_100023373225.0x0000b7',
         'El informe diplomático contemporáneo registra fallecimiento4/6/1888. El posterior reconocimiento británico deFaisal es un proceso diferente de la sucesión local; la negociación exterior no acredita control uniforme del interior omaní.',start_coverage=True)

    sarawak = 'https://museum.sarawak.gov.my/web/subpage/webpage_view/290'
    term('HIST-Q1658411','Q1065104','Charles Brooke','Rajá de Sarawak',FIRST,EARLY_LAST,sarawak,
         'El Museo de Sarawak acredita el Gobierno1868–1917. Ventana de observación1880–1885; no significa que abandonara el cargo en1885 ni que todo el contorno posterior ya estuviese incorporado. Las ampliaciones de Baram y Limbang tienen cronologías propias.',start_coverage=True,end_coverage=True)
    johor = 'https://royal.johor.my/salasilah-kesultanan-johor/'
    term('HIST-Q1150344','Q2637695','Abu Bakar','Maharajá de Johor',FIRST,'1885-12-10',johor,
         'Gobierna desde1862 como temenggong y desde1868 como maharajá. La genealogía de la Casa Real distingue reconocimiento del título sultánico11/12/1885, proclamación13/2/1886 y coronación29/7/1886. No se llama sultán a su cargo de1880.',start_coverage=True)
    term('HIST-Q1150344','Q2637695','Abu Bakar','Gobernante de Johor · título sultánico reconocido','1885-12-11',EARLY_LAST,johor,
         'El título reconocido en diciembre1885 precede a la proclamación y coronación de1886. La observación se limita al tramo cartográfico temprano; no afirma fin del reinado.',end_coverage=True)
    term('HIST-Q1317579','Q4207009','Abdul Hamid Halim Shah','Sultán de Kedah','1882-01-01',EARLY_LAST,
         'https://mmk.kedah.gov.my/sejarah/',
         'La asamblea de Kedah fecha el reinado1882–1943, mientras el consejo religioso da1881–1943. La observación empieza en1882 para no inventar el día del relevo. El sultán anteriorZainalRashidII de1879–1881 requiere completar su identidad y cronología.',precision=9,start_coverage=True,end_coverage=True)
    term('HIST-Q213467','Q12710154','Syed Ahmad Jamalullail','Rajá de Perlis',FIRST,EARLY_LAST,
         'https://dymm.perlis.gov.my/index.php/info-diraja/salasilah-diraja?start=2',
         'La Casa Real de Perlis documenta el reinado1873–1897. Se limita la observación a1880–1885; no implica cese en1885. La relación tributaria conSiam y la coronación enBangkok no eliminan la autoridad local.',start_coverage=True,end_coverage=True)

    kashmir = 'https://ikashmir.net/historicaldocuments/14.html'
    term('HIST-Q2571484','Q3694970','Ranbir Singh','Maharajá de Jammu y Cachemira',FIRST,'1885-09-12',kashmir,
         'El despacho virreinal de1885 informa que el fallecimiento se comunicó por telegrama el12/9. La autoridad principesca y la supremacía británica se mantienen separadas. No se identifica aRanbir con otros gobernantes homónimos.',start_coverage=True)
    term('HIST-Q2571484','Q2842349','Pratap Singh','Maharajá de Jammu y Cachemira','1885-09-14',EARLY_LAST,
         'https://ikashmir.net/historicaldocuments/9.html',
         'La carta original del virrey14/9/1885 reconoce y confirma la sucesión tras la muerte del padre. El inicio de esta observación es la fecha del documento, no afirma que la sucesión o el acceso sólo ocurrieran el14. La instalación de un residente británico no lo convierte en monarca británico.',start_coverage=True,end_coverage=True)
    term('HIST-Q722071','Q1920707','Mensa Bonsu','Asantehene · soberano ashanti',FIRST,'1883-03-08',
         'https://encyclopaediaafricana.com/mensa-bonsu/',
         'La investigación biográfica deIvorWilks documenta la deposición8/3/1883. No se prolonga el mandato hasta su fallecimiento1896. La inestabilidad de1883–1885 requiere registrar autoridades y consejos propios, no un sucesor ficticio continuo.',start_coverage=True)
    term('HIST-Q1679856','Q12521177','Thaha Syaifuddin','Sultán depuesto de Jambi · resistencia del interior',FIRST,EARLY_LAST,
         'https://portalbpsdm.jambiprov.go.id/artikel/buku-sastra/sejarah-sultan-thaha-saifuddin-pahlawan-nasional-jambi/',
         'Tras la toma neerlandesa del palacio en1858 ejerce resistencia y Gobierno del interior hasta1904. No equivale a control uniforme deJambi ni se borra la existencia de sultanes reconocidos por los neerlandeses. La serie de estos últimos sigue pendiente.',start_coverage=True,end_coverage=True)
    term('HIST-Q190165','Q962950','Oun Kham','Rey de Luang Prabang · relación tributaria con Siam',FIRST,EARLY_LAST,
         'https://archive.lib.cmu.ac.th/full/T/2011/sudev21111cl_ch2.pdf',
         'La investigación deChiangMai sitúa al rey en el período anterior al saqueo de1887 y a las intervenciones francesas. Se usa sólo la ventana estable1880–1885: las fuentes discrepan en los años iniciales y la relación entre regencia y reinado posterior. No atribuye independencia exterior plena.',start_coverage=True,end_coverage=True)

    transvaal = 'https://sahistory.org.za/article/first-anglo-boer-war'
    term('TRV','Q244407','Paul Kruger','Miembro del triunvirato boer · Gobierno restaurado disputado','1880-12-13','1883-05-08',transvaal,
         'Proclamación de restauración13/12/1880 tras ocupación británica de1877. Comparte el poder conJoubert yPretorius; no es aún presidente electo individual ni supone control boer uniforme durante la guerra. Las leyes de1882 identifican al triunvirato y aKruger como vicepresidente.')
    term('TRV','Q244407','Paul Kruger','Presidente de la República Sudafricana · Transvaal','1883-05-09',LAST,
         'https://sahistory.org.za/dated-event/paul-kruger-elected-president',
         'Elegido16/4/1883, juramento9/5/1883. Las reelecciones posteriores renuevan el mandato sin cambiar la identidad personal; se acota esta serie a1899 conservando literalmente los registros de1900 en adelante.',end_coverage=True)

    vietnam = 'https://scov.gov.vn/dat-nuoc-con-nguoi/tom-tat-bien-nien-su-vn/xxii.-nha-nguyen-143-nam-1802-1945-quoc-hieu-viet-nam-tu-minh-mang-la-dai-nam-kinh-do-hue-thua-thien-phan-2-.html'
    # Annual precision avoids converting lunar/era dates into invented days.
    for key,ceiling in [('HIST-Q6500483',EARLY_LAST),('VNM',LAST)]:
        def vn(person,name,role,start,end,source,note,precision=9):
            if start>ceiling:return
            term(key,person,name,role,start,min(end,ceiling),source,note,
                 precision=precision,start_coverage=True,end_coverage=True)
        vn('Q466976','Tự Đức','Emperador de Đại Nam · dinastía Nguyễn',FIRST,'1883-01-01',vietnam,
           'La cronología institucional acredita reinado1847–1883. El límite anual normalizado no representa fallecimiento el1de enero; las fechas lunares de los sucesores breves no se convierten sin evidencia adicional.')
        for person,name in [('Q534019','Dục Đức'),('Q465598','Hiệp Hòa')]:
            vn(person,name,'Emperador de Đại Nam · sucesión breve de1883','1883-01-01','1883-12-31',vietnam,
               'Observación del mandato breve documentado en1883; los dos extremos sólo delimitan el año de evidencia, no un reinado de doce meses. La ficha debe conservar la precisión anual y el carácter de sucesión breve.')
        vn('Q465593','Kiến Phúc','Emperador de Đại Nam · dinastía Nguyễn','1883-12-31','1884-01-01',vietnam,
           'Mandato entre1883 y1884. Los extremos de cobertura anual no significan reinado de dos días; falta reconciliar calendarios y documentación de acceso y muerte antes de fijar días.')
        vn('Q447616','Hàm Nghi','Emperador de Đại Nam · después dirigente de resistencia','1884-12-31','1885-12-31',
           'https://hue.gov.vn/Du-dia-chi/tb/Thua-Thien-Hue-dau-tranh-chong-thuc-dan-Phap-1885-1916-516945',
           'Soberano1884–1885 que sale deHuế tras la caída de julio1885 y encabezaCầnVương. Esta observación no afirma que su Gobierno de la capital durara hasta31/12 ni que toda resistencia terminase ese año.')
        vn('Q342476','Đồng Khánh','Emperador de Đại Nam · bajo tutela francesa','1885-09-19','1889-01-28',
           'https://hue.gov.vn/Du-dia-chi/tb/Thua-Thien-Hue-dau-tranh-chong-thuc-dan-Phap-1885-1916-516945',
           'Entonización19/9/1885 documentada por el Gobierno deHuế; fallecimiento28/1/1889 corroborado por el Museo Nacional de Historia. Monarquía formal bajo el protectorado, no independencia exterior ni administración única de todaCochinchina.',11)
        vn('Q465059','Thành Thái','Emperador de Đại Nam · monarquía bajo tutela francesa','1889-12-31',LAST,
           'https://vnmh.com.vn/vi/Articles/3098/15571/hoang-dje-thanh-thai-vi-vua-yeu-nuoc-cua-vuong-trieu-nguyen.html',
           'ElMuseoNacional deHistoria acredita reinado1889–1907 y la sucesión tras la muerte deĐồngKhánh. La observación empieza al cierre1889 sin inventar una entronización31/12; la serie de1900 en adelante se conserva intacta.')

    for c in countries.values():
        c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    return data


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=pathlib.Path,default=ROOT/'public/data/identities.json')
    p.add_argument('--output',type=pathlib.Path,required=True)
    args=p.parse_args()
    data=curate(json.loads(args.input.read_text(encoding='utf8')))
    args.output.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print('Prepared bounded audit-gap terms:',sum(l.get('acquisition')==TAG for c in data['countries'].values() for l in c['leaders']))
