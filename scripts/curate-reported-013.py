"""Pure corrections for explicitly reported identities/dates in0.13.

The1880 acquisition preserves1900+; these deliberate exceptions are a separate
review requested by the owner, not a side effect of extending the window.
"""
import copy,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
TAG='reported-authorities-0.13'
EXCLUSIONS=json.loads((ROOT/'scripts/authority-exclusions.json').read_text(encoding='utf8'))
MEDIA_EXCLUSIONS=json.loads((ROOT/'scripts/media-exclusions.json').read_text(encoding='utf8'))

def curate(incoming):
    d=copy.deepcopy(incoming);cs=d['countries']
    photos={l['person']:copy.deepcopy(l['portrait']) for c in cs.values() for l in c['leaders'] if l.get('portrait')}
    for key,c in cs.items():
        c['leaders']=[l for l in c['leaders'] if not any(l['person']==e['person'] and key in e['countries'] for e in EXCLUSIONS)]
        for l in c['leaders']:
            if l.get('portrait') and any(e['person']==l['person'] and e['title']==l['portrait']['title'] for e in MEDIA_EXCLUSIONS):l.pop('portrait')
    def term(key,person,name,role,start,end,source,note):
        cs[key]['leaders']=[l for l in cs[key]['leaders'] if not (l['person']==person and (l.get('acquisition')==TAG or l['start']>='2022-01-01'))]
        l=dict(person=person,name=name,role=role,start=start,end=end,source=source,note=note,precision=11,curated=True,acquisition=TAG)
        if end==d['retrieved']:l['endIsCoverageBoundary']=True
        if person in photos and not any(e['person']==person and e['title']==photos[person]['title'] for e in MEDIA_EXCLUSIONS):l['portrait']=copy.deepcopy(photos[person])
        cs[key]['leaders'].append(l)
    term('IRQ','Q115579547','Nizar Amidi','Presidente de la República','2026-04-11',d['retrieved'],
         'https://iq.parliament.iq/en/2026/04/11/first-deputy-speaker-congratulates-mr-nizar-amidi-on-winning-the-confidence-of-the-council-of-representatives-and-his-election-as-president-of-the-republic/',
         'El Parlamento documenta la elección11/4/2026. Se elimina la atribución desde2022, correspondiente a otro cargo. El inicio representa el acto electoral documentado, no una fecha de otro ministerio.')
    term('IRQ','Q139573306','Ali Falih al-Zaidi','Primer ministro','2026-05-14',d['retrieved'],
         'https://iq.parliament.iq/en/2026/05/14/council-of-representatives-votes-on-the-ministerial-curriculum-and-grants-confidence-to-the-government-of-mr-ali-al-zaydi/',
         'Confianza parlamentaria y juramento14/5/2026. La nominación27/4 no es el inicio del Gobierno; la entrega ceremonial16/5 es otro acto. La identidad y el retrato se contrastan por fuentes institucionales, no por elP18 vandalizado.')
    term('IRQ','Q3700793',"Mohammed Shia' Al Sudani",'Primer ministro','2022-10-27','2026-05-13',
         'https://iq.parliament.iq/en/2026/05/14/council-of-representatives-votes-on-the-ministerial-curriculum-and-grants-confidence-to-the-government-of-mr-ali-al-zaydi/',
         'Se conserva el inicio de octubre2022 documentado en el catálogo y se termina la ventana antes del juramento del nuevo Gobierno. No se prolonga como titular vigente hasta la fecha de consulta ni hasta la entrega ceremonial posterior.')
    term('MOZ','Q6761049','Maria Benvinda Delfina Levi','Primera ministra','2025-01-17',d['retrieved'],
         'https://www.inm.gov.mz/pt-br/content/suplemento-n%C2%BA-1-de-170125-pag-38-1-4-br-n%C2%BA-13-boletim-da-rep%C3%BAblica-i-serie',
         'Nombramiento por despacho62/2025 publicado17/1/2025; toma de posesión18/1. No se normaliza su acceso al1de enero. La fotografía grupal, si se conserva como referencia, no es un retrato individual.')
    for l in cs['VNM']['leaders']:
        if l['person']=='Q57407' and l['start']<='2016-04-02' and l['end']>'2016-04-02':
            l.update(end='2016-04-02',endSource='https://en.baochinhphu.vn/state-president-tran-dai-quang-passes-away-11133211.htm',dateCorrection=TAG)
            l['note']='Se corrige el cese deTrươngTấnSang al relevo deTrầnĐạiQuang elegido2/4/2016, no julio. Ambos aparecen en la ficha anual con su intervalo.'
    for c in cs.values():c['leaders'].sort(key=lambda l:(l['start'],l['name'],l['role']))
    return d

if __name__=='__main__':
    p=ROOT/'public/data/identities.json';d=curate(json.loads(p.read_text(encoding='utf8')))
    p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
