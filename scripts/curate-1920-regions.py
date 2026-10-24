"""Documentary 1920–1949 windows for monarchies and historical territories.

Does not invent investiture dates where only an annual interval was verified.
No network/media writes. See docs/AUTHORITIES-1920-REGIONS.md.
"""
import argparse, copy, datetime, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'curated-1920-regions-0.11'
FIRST, LAST = '1920-01-01', '1949-12-31'
DAN = 'https://gdansk.gedanopedia.pl/gdansk/?title=SENAT_II_WOLNEGO_MIASTA_GDA%C5%83SKA_1920%E2%80%931939'
TIB = 'https://www.jstor.org/stable/jj.8501027'
NPL = 'https://tile.loc.gov/storage-services/master/frd/copr/Nepal.pdf'
RANA = 'https://nepalindata.com/media/resources/items/0/b1982_Nepal_Mandala--Cultural_Study_of_Kathmandu_Valley_vol_1_Text_by__CvYy5M9.pdf'
IRN = 'https://www.iranicaonline.org/articles/ahmad-shah-qajar-1909-1925-the-seventh-and-last-ruler-of-the-qajar-dynasty/'
ROWS = [
 ('TWN','Q699698','Yan Xishan','Primer ministro de la República de China','1949-06-13','1950-03-10','https://history.ey.gov.tw/en/director/?director=28',11,False,False,'Cronología del Ejecutivo:13/6/1949–10/3/1950. Se corrige la antigua ventana conservadora que terminaba en febrero y se descarta una afirmación genérica que lo confundía con el presidente. Nombramiento, formación del gabinete y ejercicio pueden tener fechas distintas.'),
 ('ROC','Q699698','Yan Xishan','Primer ministro de la República de China','1949-06-13','1949-12-31','https://history.ey.gov.tw/en/director/?director=28',11,False,True,'El Ejecutivo documenta13/6/1949–10/3/1950. Se recorta esta clave continental al límite de revisión, sin afirmar dimisión en diciembre; el mandato completo se conserva enTWN.'),
 # Annual windows are coverage bounds, not January investitures/December deaths.
 ('DAN','Q215275','Heinrich Sahm','Presidente del Senado de la Ciudad Libre','1920-12-07','1931-01-08',DAN,11,False,False,'Se distingue la elección del6/12 de la primera sesión del7/12/1920. Ciudad autónoma bajo protección de la Sociedad de Naciones, no colonia alemana ni polaca.'),
 ('DAN','Q89594','Ernst Ziehm','Presidente del Senado de la Ciudad Libre','1931-01-09','1933-06-19',DAN,11,False,False,'Identidad del político1867–1962; no el oficial de submarinos homónimo.'),
 ('DAN','Q213809','Hermann Rauschning','Presidente del Senado de la Ciudad Libre','1933-06-20','1934-11-01',DAN,10,False,True,'La bibliografía difiere entre23y24/11 para el relevo. Se detiene esta ventana antes de ambas fechas sin inventar un cese el1/11.'),
 ('DAN','Q213826','Arthur Greiser','Presidente del Senado de la Ciudad Libre','1934-12-01','1939-08-22',DAN,10,True,True,'Ventana posterior a las fechas discrepantes28/29de noviembre para el acceso. El nuevo cargo de Forster del23/8/1939 y la anexión del1/9 son hechos distintos; el cierre no es dimisión acreditada.'),
 ('TIB','Q25238','Thubten Gyatso · XIII Dalái Lama','Autoridad temporal y espiritual del Gobierno tibetano','1920-01-01','1933-12-17','https://api.repository.cam.ac.uk/server/api/core/bitstreams/b3eff21d-d4e2-4645-935d-e58464ec5d57/content',11,True,False,'Gobierno de facto y soberanía disputada. Se usa la fecha de fallecimiento17/12/1933 del estudio conservado en Cambridge.'),
 ('TIB','Q957784','Jamphel Yeshe Gyaltsen · Reting','Regente del Gobierno tibetano','1934-12-31','1940-12-31',TIB,9,True,True,'Resolución anual contrastada; los límites son una ventana interior de la regencia1934–1941, no nombramiento ni dimisión. La entronización infantil delXIV Dalái Lama en1940 no equivale a asumir plenos poderes políticos.'),
 ('TIB','Q957724','Ngawang Sungrab Thutob · Taktra','Regente del Gobierno tibetano','1941-12-31','1949-12-31',TIB,9,True,True,'Regencia desde1941; ventana anual de revisión. No se infiere que elXIV Dalái Lama ejerciese ya plenos poderes políticos.'),
 ('RSI','Q23559','Benito Mussolini','Jefe de la República Social Italiana · régimen dependiente de Alemania','1943-12-31','1944-12-31','https://dgagaeta.cultura.gov.it/public/uploads/documents/Fonti/54e34c352130a.pdf',9,True,True,'Ventana interior de la entidad1943–1945. La creación institucional se distingue del frente militar: no hay un contorno propio de laRSI validado en esta entrega.'),
 ('ETH','Q148524','Zewditu','Emperatriz de Etiopía','1920-01-01','1929-12-31','https://betamasaheft.awhamburg.de/persons/PRS10671Zawditu/main',9,True,True,'Ventana interior del reinado1916–1930. La fecha de muerte de una ficha secundaria difiere de la cronología biográfica; no se adopta aquí esa fecha. Tafari ejercía además la regencia.'),
 ('ETH','Q41178','Haile Selassie · Tafari Makonnen','Regente de Etiopía','1920-01-01','1929-12-31','https://1997-2001.state.gov/background_notes/ethiopia_0398_bgn.html',9,True,True,'Regencia durante el reinado de Zewditu; no emperador todavía. Ventana interior, no fechas de nombramiento.'),
 ('ETH','Q41178','Haile Selassie','Emperador de Etiopía · en el exilio durante la ocupación italiana','1930-12-31','1949-12-31','https://jfk.artifacts.archives.gov/people/610/his-imperial-majesty-haile-selassie',9,True,True,'Emperador desde1930; la ocupación italiana1936–1941 y el exilio no se presentan como ejercicio efectivo en todo el territorio. El mapa de control y la continuidad del título son ámbitos distintos.'),
 ('IRN','Q317799','Ahmad Shah Qajar','Shah de Irán · dinastía Qajar','1920-01-01','1925-10-31',IRN,11,True,False,'La deposición parlamentaria del31/10/1925 no equivale a la coronación del sucesor.'),
 ('IRN','Q182921','Reza Shah Pahlavi','Shah de Irán · dinastía Pahlavi','1925-12-12','1941-09-16',IRN,11,False,False,'La Asamblea Constituyente confiere la corona12/12/1925; la coronación de1926 es posterior. Abdicación en1941 separada de la de su hijo.'),
 ('AFG','Q153620','Amanullah Khan','Emir de Afganistán','1920-01-01','1925-12-31','https://www.loc.gov/item/2002344691/',9,True,True,'Título de emir antes de adoptar el de rey en1926. Ventana interior del gobierno1919–1929; el límite no es un cese.'),
 ('NPL','Q381928','Tribhuvan','Rey de Nepal · jefatura formal del Estado','1920-01-01','1949-12-31',NPL,9,True,True,'Reinado1911–1955; los primeros ministros Rana concentraban el poder efectivo durante esta ventana. El exilio de1950 y la restauración posterior quedan fuera de este tramo.'),
 ('NPL','Q1061786','Chandra Shumsher Jung Bahadur Rana','Primer ministro Rana · ejercicio efectivo del Gobierno','1920-01-01','1929-11-26','https://nepalica.hadw-bw.de/nepal/ontologies/viewitem/306',11,True,False,'Mandato desde27/6/1901; el inicio1920 delimita esta revisión, no la investidura.'),
 ('NPL','Q1132119','Bhim Shumsher Jung Bahadur Rana','Primer ministro Rana · ejercicio efectivo del Gobierno','1929-12-31','1931-12-31',RANA,9,True,True,'Ventana interior del mandato1929–1932 según la tabla de sucesión. No acredita fechas diarias de relevo.'),
 ('NPL','Q1132112','Juddha Shumsher Jung Bahadur Rana','Primer ministro Rana · ejercicio efectivo del Gobierno','1932-12-31','1944-12-31',RANA,9,True,True,'Ventana interior del mandato1932–1945; no se inventa una investidura al comienzo del año.'),
 ('NPL','Q2268133','Padma Shumsher Jung Bahadur Rana','Primer ministro Rana · ejercicio efectivo del Gobierno','1945-12-31','1947-12-31',RANA,9,True,True,'Ventana interior del mandato1945–1948; el siguiente mandato de Mohan ya consta separadamente.'),
 ('YMK','Q163945','Yahya Muhammad Hamid ed-Din','Imán del Yemen · posteriormente rey','1920-01-01','1948-02-17','https://history.state.gov/historicaldocuments/frus1950v05/d755',11,True,False,'La fuente diplomática fecha su asesinato17/2/1948. El título regio no se retroproyecta a toda la etapa del imanato.'),
 ('YMK','Q400961','Ahmad bin Yahya','Imán y rey del Yemen','1948-04-01','1949-12-31','https://history.state.gov/historicaldocuments/frus1950v05/d755',10,True,True,'La fuente confirma sucesión tras una breve guerra civil, pero no fija aquí el día de acceso. Abril es comienzo conservador de cobertura, no investidura; el gobierno revolucionario intermedio de1948 queda pendiente de ficha propia.'),
 ('TUR','Q5152','Mustafa Kemal Atatürk','Presidente de la Gran Asamblea Nacional · Gobierno de Ankara','1921-01-25','1923-10-28','https://www.ktb.gov.tr/TR-96329/1922.html',11,True,False,'Ámbito del Gobierno de Ankara anterior a la República. No se le atribuye presidencia republicana antes del29/10/1923 ni el título de primer ministro durante toda esta etapa.'),
 ('ALB','Q984363','Mustafa Merlika Kruja','Primer ministro de Albania bajo ocupación italiana','1941-12-03','1943-01-04','https://www.kryeministria.al/historia/',11,False,False,'Cronología del Consejo de Ministros albanés. Cargo local de un régimen bajo ocupación, distinto del rey italiano y de un Gobierno albanés independiente.'),
 ('CHN-COMMUNIST','Q5816','Mao Zedong','Presidente del Gobierno Central de la República Soviética China','1931-12-31','1934-12-31','https://www.marxists.org/reference/archive/mao/works/collected-works-pdf/volume-3.pdf',9,True,True,'Ventana de cobertura del Gobierno soviético de Jiangxi desde1931. Edición documental de sus escritos y avisos del Comité Ejecutivo Central, no fuente neutral para sus afirmaciones políticas. No equivale todavía a presidencia de la República Popular ni a soberanía efectiva sobre toda China.'),
]


def curate(incoming):
    data = copy.deepcopy(incoming)
    cs = data['countries']
    portraits = {l['person']: copy.deepcopy(l['portrait']) for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for c in cs.values():
        c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    for key, qid, name in [('DAN','Q216173','Ciudad Libre de Danzig'),('TIB','Q2444884','Gobierno tibetano de facto'),('RSI','Q153660','República Social Italiana')]:
        cs.setdefault(key, dict(flags=[], leaders=[]))
        cs[key].update(qid=qid, name=name)
    # An acquired, year-precision claim reaching1Jan1950 survived the reviewed
    # premiership at a shared endpoint and reintroduced a false presidency.
    # The Executive Yuan now supplies the complete, independently dated term.
    for key in ['ROC','TWN']:
        cs[key]['leaders']=[l for l in cs[key]['leaders'] if not(l['person']=='Q699698' and l['start']<'1951-01-01' and l['end']>='1949-01-01')]
    # Generic country claims conflate Turkey's presidents with heads of government.
    # Preserve their real presidential offices and the separately acquired premiers.
    for q in ['Q5152', 'Q183297']:
        cs['TUR']['leaders'] = [l for l in cs['TUR']['leaders'] if not (l['person']==q and l['role']=='Jefatura del Gobierno' and '1923-10-29'<=l['start']<='1949-12-31')]
    for key,q,name,role,start,end,source,precision,lo,hi,note in ROWS:
        kept=[]
        for old in cs[key]['leaders']:
            if old['person']!=q or old['end']<start or old['start']>end:
                kept.append(old); continue
            if old['start']<start:
                before=copy.deepcopy(old);before.update(end=(datetime.date.fromisoformat(start)-datetime.timedelta(days=1)).isoformat(),endIsCoverageBoundary=True);kept.append(before)
            if old['end']>end:
                after=copy.deepcopy(old);after.update(start=(datetime.date.fromisoformat(end)+datetime.timedelta(days=1)).isoformat(),startIsCoverageBoundary=True);kept.append(after)
        term=dict(person=q,name=name,role=role,start=start,end=end,source=source,precision=precision,curated=True,acquisition=TAG,note=note)
        if lo:term['startIsCoverageBoundary']=True
        if hi:term['endIsCoverageBoundary']=True
        if q in portraits:term['portrait']=copy.deepcopy(portraits[q])
        cs[key]['leaders']=[*kept,term]
    for c in cs.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    return data


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=pathlib.Path,default=ROOT/'public/data/identities.json')
    parser.add_argument('--output',type=pathlib.Path)
    args=parser.parse_args();result=curate(json.loads(args.input.read_text(encoding='utf8')))
    (args.output or args.input).write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    print('Prepared',len(ROWS),'regional documentary windows.')
