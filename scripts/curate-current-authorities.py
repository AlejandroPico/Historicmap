"""Reviewed current-year corrections after comparing the UN Protocol list.

QIDs checked against linked individual Wikipedia/Wikidata records, not fuzzy
name search. UN dates may lag: individual official sources override that list.
Run before enrich-current-authorities.py; preserves prior annual officeholders.
"""
import datetime,json,pathlib,urllib.request,time
ROOT=pathlib.Path(__file__).resolve().parents[1];CACHE=ROOT/'.cache/identities'
TODAY=datetime.date.today().isoformat();UN='https://www.un.org/dgacm/sites/www.un.org.dgacm/files/Documents_Protocol/hspmfmlist.pdf'
path=ROOT/'public/data/identities.json';data=json.loads(path.read_text(encoding='utf8'));cs=data['countries']
def entity(q):
    p=CACHE/('person-current-'+q+'.json')
    if p.exists():return json.loads(p.read_text(encoding='utf8'))['entities'][q]
    for i in range(4):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request('https://www.wikidata.org/wiki/Special:EntityData/'+q+'.json',headers={'User-Agent':'Historicmap/0.5 (https://github.com/AlejandroPico/Historicmap)'}),timeout=40));p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');return d['entities'][q]
        except Exception:
            if i==3:raise
            time.sleep(2**i)
def qualifier(s,p):
    v=s.get('qualifiers',{}).get(p,[{}])[0].get('datavalue',{}).get('value',{})
    return v['time'].lstrip('+')[:10].replace('-00','-01') if isinstance(v,dict) and v.get('time') else None
gov=[
 ('BFA','Q116056730','Jean Emmanuel Ouédraogo','2024-12-08'),
 ('BDI','Q135650664','Nestor Ntahontuye','2025-08-05'),
 ('TCD','Q126086566','Allamaye Halina','2024-05-24'),
 ('COD','Q117472023','Judith Suminwa Tuluka','2024-04-01'),
 ('GNB','Q96966766','Ilídio Vieira Té','2025-11-29'),
 ('IRQ','Q139573306','Ali Falih al-Zaidi','2026-05-14'),
 ('KWT','Q16151955','Ahmad Abdullah Al-Ahmad Al-Sabah','2024-04-15'),
 ('LAO','Q25999464','Saleumxay Kommasith','2026-10-05'),
 ('MUS','Q57836','Navin Ramgoolam','2024-11-12'),
 ('NPL','Q111772343','Balendra Shah','2026-03-27'),
 ('PER','Q6700615','Luis Galarreta','2026-07-28'),
 ('WSM','Q16734600','Laʻauli Leuatea Schmidt','2025-09-16'),
 ('SEN','Q139921464','Ahmadou Al Aminou Lo','2026-05-25'),
 ('SLB','Q6791373','Matthew Wale','2026-07-08'),
 ('SDN','Q6357939','Kamil Idris','2025-05-31'),
 ('THA','Q16139757','Anutin Charnvirakul','2025-09-07'),
 ('TZA','Q31752753','Mwigulu Nchemba','2026-04-01'),
 ('UZB','Q28002959','Abdulla Aripov','2016-12-14'),
 ('VUT','Q115252004','Jotham Napat','2025-02-11'),
 ('VNM','Q24254499','Lê Minh Hưng','2026-04-07'),
 ('YEM','Q7460973','Shaya al-Zindani','2026-01-15'),
 ('PSX','Q20423278','Mohammad Mustafa','2024-03-31'),
]
state=[
 ('BGD','Q6874839','Mirza Fakhrul Islam Alamgir','2026-09-01'),
 ('FJI','Q6959729','Naiqama Lalabalavu','2024-11-12'),
 ('GNB','Q137049690','Horta Inta-A','2025-11-27'),
 ('HUN','Q788903','András Baka','2026-08-19'),
 ('PSX','Q127998','Mahmoud Abbas','2005-01-15'),
]
overrides={
 'Q135650664':'https://presidence.gov.bi/wp-content/uploads/2025/08/DECRET-PORTANT-NOMINATION-DU-PREMIER-MINISTRE.pdf',
 'Q111772343':'https://www.opmcm.gov.np/minister-detail/',
 'Q20423278':'https://www.un.org/unispal/document/sgreport-assistance-to-the-palestinian-people-20may24/',
 'Q127998':'https://www.un.org/unispal/document/auto-insert-194378/',
 'Q25999464':'https://kpl.gov.la/asean2024/en/detail.aspx?id=107870',
 'Q115252004':'https://pmnec.gov.pg/prime-minister-marape-congratulates-hon-jotham-napat-on-election-as-vanuatus-new-prime-minister/',
}
notes=[]
cs['PSX']['leaders']=[l for l in cs['PSX']['leaders'] if l['person']!='Q34590221']
# Nauru country-item statements left obsolete presidents indefinitely open and
# gave Adeang an erroneous September date. National publications override them.
for l in cs['NRU']['leaders']:
    if l['person']=='Q57543':
        l.update(end='2013-06-11',curated=True,source='https://www.nauru.gov.nr/government-information-office/media-release/baron-waqa-elected-new-president.aspx')
    elif l['person']=='Q109781648':
        l.update(end='2023-10-30',curated=True,endIsUpperBound=True,source='https://justice.gov.nr/wp-content/uploads/2024/12/Nauru-MER-2024-Published-version-1.pdf',note='Moción de censura el 25 de octubre de 2023; el sucesor fue elegido el 30. Esta fecha es el límite superior de la salida, sin equiparar censura y cese efectivo.')
    elif l['person']=='Q58096' and l['start']>='2023-01-01':
        l.update(start='2023-10-30',precision=11,curated=True,source='https://www.nauru.gov.nr/media/198459/gazette_139-24.pdf')
# Both Korean prime ministers overlap 2026. The appointment was approved on
# 3 July 2025; presenting its certificate on 4 July is a separate event.
kim='Q12587400';entity(kim)
if not any(l['person']==kim and l['start']=='2025-07-03' for l in cs['KOR']['leaders']):
    cs['KOR']['leaders'].append(dict(person=kim,name='Kim Min-seok',role='Primer ministro',start='2025-07-03',end='2026-06-30',precision=11,curated=True,source='https://www.korea.net/NewsFocus/policies/view?articleId=274523',note='Nombramiento aprobado el 3 de julio de 2025; entrega de la credencial el 4. Sustituido por Han Seong-sook el 1 de julio de 2026, según KBS World: https://world.kbs.co.kr/service/news_view.htm?Seq_Code=202565&lang=e'))
for l in cs['KOR']['leaders']:
    if l['person']=='Q55082182' and l['start']=='2026-07-01':
        l.update(curated=True,source='https://world.kbs.co.kr/service/news_view.htm?Seq_Code=202565&lang=e')
for l in cs['KAB']['leaders']:
    if l['person']=='Q19861743':l['name']='Konstantín Busygin'
for key,q,start,end in [('NRU','Q560557','2001-03-30','2003-01-09'),('NRU','Q888033','2003-03-10','2003-05-29'),('JEY','Q16196549','2018-06-07','2022-07-12'),('PCN','Q75462006','2020-01-01','2022-12-31')]:
    for l in cs[key]['leaders']:
        if l['person']==q and l['end']==TODAY:
            l.update(start=start,end=end,precision=11,source='https://www.wikidata.org/wiki/'+q)
for start,end in [('2024-01-30','2026-06-19'),('2026-06-30',TODAY)]:
    if not any(l['person']=='Q12057510' and l['start']==start for l in cs['JEY']['leaders']):
        entity('Q12057510');cs['JEY']['leaders'].append(dict(person='Q12057510',name='Lyndon Farnham',role='Ministro principal',start=start,end=end,precision=11,curated=True,source='https://www.statesassembly.je/members/lyndonfarnham'))
if not any(l['person']=='Q16215208' and l['start']=='2026-01-01' for l in cs['PCN']['leaders']):
    cs['PCN']['leaders'].append(dict(person='Q16215208',name='Shawn Christian',role='Alcalde · administración local',start='2026-01-01',end=TODAY,precision=11,curated=True,source='https://static1.squarespace.com/static/6526ff6fef608a3828c13d05/t/6a31714804509f1abf0f883a/1781625160478/Special+Council+minutes+January+12++2026.pdf',note='El acta del Consejo del 12 de enero de 2026 confirma el alcalde; la fecha de inicio anual procede del inventario de titulares.'))
# A draft import used the UN table's erroneous Vanuatu appointment date; the
# congratulatory announcement of 11 February 2025 establishes the correct date.
cs['VUT']['leaders']=[l for l in cs['VUT']['leaders'] if not (l['person']=='Q115252004' and l['start']=='2024-09-30' and l.get('curated'))]
def close_prior(country,person,start,kind):
    generic='Jefatura del Gobierno' if kind=='gov' else 'Jefatura del Estado'
    for old in country['leaders']:
        if old['person']==person or old['start']>=start or old['end']<start:continue
        if old['role']!=generic:continue
        e=entity(old['person']);ends=[]
        for s in e.get('claims',{}).get('P39',[]):
            a=qualifier(s,'P580');b=qualifier(s,'P582')
            if a==old['start'] and b and b<=start:ends.append(b)
        if ends:
            old['end']=max(ends);old['source']='https://www.wikidata.org/wiki/'+old['person']
        else:
            old['end']=(datetime.date.fromisoformat(start)-datetime.timedelta(days=1)).isoformat()
            old['endIsUpperBound']=True
            old['note']=(old.get('note','')+' Fin exacto no determinado: este límite superior queda establecido por el nombramiento del sucesor.').strip()
            notes.append(dict(person=old['person'],end=old['end'],reason='Successor establishes an upper bound; not an exact departure date.'))
for kind,rows in [('gov',gov),('state',state)]:
    for key,q,name,start in rows:
        # Fetching the individual verifies that the QID exists and supplies
        # images later; titles/names are explicitly reviewed above.
        entity(q);country=cs[key];close_prior(country,q,start,kind)
        role='Jefatura del Gobierno' if kind=='gov' else 'Jefatura del Estado'
        old=next((l for l in country['leaders'] if l['person']==q and l['role']==role and l['start']==start),None)
        if old:old.update(name=name,end=TODAY,curated=True,source=overrides.get(q,UN))
        else:country['leaders'].append(dict(person=q,name=name,role=role,start=start,end=TODAY,precision=11,curated=True,source=overrides.get(q,UN)))

# Nepal's early-2026 interim prime minister remains visible in the annual view.
q='Q23842116';entity(q)
if not any(l['person']==q and l['start']=='2025-09-12' for l in cs['NPL']['leaders']):
    cs['NPL']['leaders'].append(dict(person=q,name='Sushila Karki',role='Primera ministra interina',start='2025-09-12',end='2026-03-27',precision=11,curated=True,source='https://www.wikidata.org/wiki/'+q))

# UN's printed Haiti row is stale; the government records the CPT's end.
haiti='https://communication.gouv.ht/communiques/continuite-de-letat-adresse-a-la-nation-du-premier-ministre-apres-le-mandat-du-cpt/'
for l in cs['HTI']['leaders']:
    if l['person']=='Q124846311':l.update(end='2026-02-07',source=haiti)

# Six regents overlap 2026, in three collegiate pairs. Never collapse the pair
# into one president or leave the 2024/2025 holders indefinitely in office.
regency='https://www.reggenzadellarepubblica.sm/pub1/ReggenzaSM/Capitani_Reggenti/Capitani_Reggenti_In_Carica.html'
for l in cs['SMR']['leaders']:
    if l['person'] in ['Q130360479','Q130390817']:l['end']='2025-04-01'
    if l['person'] in ['Q57546','Q1353628']:l['end']='2025-10-01'
for q,name,start,end in [
 ('Q123678970','Matteo Rossi','2025-10-01','2026-04-01'),('Q106519616','Lorenzo Bugli','2025-10-01','2026-04-01'),
 ('Q138650200','Alice Mina','2026-04-01','2026-10-01'),('Q131783131','Vladimiro Selva','2026-04-01','2026-10-01'),
 ('Q141538307','Gerardo Giovagnoli','2026-10-01',TODAY),('Q141531158','William Casali','2026-10-01',TODAY)]:
    entity(q)
    if not any(l['person']==q and l['start']==start for l in cs['SMR']['leaders']):
        cs['SMR']['leaders'].append(dict(person=q,name=name,role='Capitán regente · jefatura colegiada del Estado',start=start,end=end,precision=11,curated=True,source=regency))

# France's first Lecornu appointment ended before his renewed appointment.
# A continuous open statement from 9 September otherwise erases this gap.
lecornu_source='https://www.legifrance.gouv.fr/loda/id/LEGIARTI000052382966'
lecornu=[l for l in cs['FRA']['leaders'] if l['person']=='Q20089181']
for l in lecornu:
    if l['start']=='2025-09-09' and l['end']>='2025-10-10':
        l.update(end='2025-10-06',source='https://www.info.gouv.fr/upload/media/content/0001/15/be79963164e74f2cc3926a68fb2e594e8b6015c0.pdf')
if not any(l['start']=='2025-10-10' for l in lecornu):
    term=dict(person='Q20089181',name='Sébastien Lecornu',role='Primer ministro',start='2025-10-10',end=TODAY,precision=11,curated=True,source=lecornu_source)
    picture=next((l['portrait'] for l in lecornu if l.get('portrait')),None)
    if picture:term['portrait']=picture
    cs['FRA']['leaders'].append(term)

# Universal/multilingual labels can replace separate en/es labels in Wikidata.
# The old importer did not read `mul`, leaving opaque QIDs on some cards.
for country in cs.values():
    for l in country['leaders']:
        if l['name']==l['person']:
            e=entity(l['person']);labels=e.get('labels',{})
            l['name']=next((labels[k]['value'] for k in ['es','en','mul'] if k in labels),l['name'])
    country['leaders'].sort(key=lambda l:(l['start'],l['name']))
path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
(CACHE/'current-curation-upper-bounds.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2),encoding='utf8')
print('Reviewed additions',len(gov)+len(state)+1,'upper-bound end dates',len(notes),flush=True)
