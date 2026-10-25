"""Extend the1939 client identity only to the newly displayed1940–1944 window.

Pure/idempotent; preserves the prior1939 documentary statements and media.
Institutional evidence: USHMM president's chronology and UPN's edition of
Stefan Tiso's diary with his5September1944 appointment/oath.
"""
import copy
import json
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
TAG = 'slovak-continuity-0.12.1'
PRESIDENT = 'https://encyclopedia.ushmm.org/content/en/article/jozef-tiso-1'
GOVERNMENT = 'https://www.upn.gov.sk/publikacie_web/pamat-naroda/pamat-naroda-04-2006.pdf'
TUKA = 'https://www.upn.sk/publikacie_web/pamat-naroda/pamat-naroda-03-2017.pdf'

def curate(incoming):
    d = copy.deepcopy(incoming)
    c = d['countries']['SVK-1939']
    portraits = {l['person']: l['portrait'] for country in d['countries'].values()
                 for l in country['leaders'] if l.get('portrait')}
    c['leaders'] = [l for l in c['leaders'] if l.get('acquisition') != TAG]
    for flag in c['flags']:
        if flag['media']['title'] == 'Flag of Slovakia (1939–1945).svg':
            flag.update(end='1944-12-31',coverageEndIsBoundary=True)
            flag['note'] = 'Símbolo documentado para los cierres1939–1944; el extremo de cobertura no es una derogación. No acredita fronteras o reconocimiento.'
    for l in c['leaders']:
        if l['person'] == 'Q367181':
            l.update(end='1944-09-05',endIsCoverageBoundary=False,endSource=TUKA)
            l['note'] = 'El acta parlamentaria sitúa el nombramiento del gabinete el28/10/1939. UPN documenta la dimisión el5/9/1944. No se atribuye aTuka la presidencia posterior deŠtefanTiso.'
    for person,name,role,start,end,source,note,boundary in [
        ('Q154346','Jozef Tiso','Presidente de la República Eslovaca','1940-01-01','1944-12-31',PRESIDENT,
         'Continuidad presidencial documentada porUSHMM entre1939 y1945; el mandato comenzó el26/10/1939 según la fuente institucional ya incorporada. Los extremos1940/1944 delimitan esta ampliación, no nombramiento o cese. La ocupación alemana desde1944 restringe el poder del régimen.',True),
        ('Q392383','Štefan Tiso','Primer ministro de la República Eslovaca','1944-09-05','1944-12-31',GOVERNMENT,
         'La edición institucional del diario reproduce el nombramiento y juramento del5/9/1944. El extremo de diciembre sólo delimita cobertura; el Gobierno continuó en1945. Es una persona distinta del presidenteJozefTiso.',False),
    ]:
        l = dict(person=person,name=name,role=role,start=start,end=end,source=source,note=note,
                 precision=11,curated=True,acquisition=TAG,endIsCoverageBoundary=True)
        if boundary:
            l['startIsCoverageBoundary'] = True
        if person in portraits:
            l['portrait'] = copy.deepcopy(portraits[person])
        c['leaders'].append(l)
    c['leaders'].sort(key=lambda l:(l['start'],l['name']))
    return d

if __name__ == '__main__':
    p=ROOT/'public/data/identities.json'
    p.write_text(json.dumps(curate(json.loads(p.read_text(encoding='utf8'))),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
