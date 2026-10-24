"""Acquire1900–1919 in an isolated staging catalogue, then merge that window only.

The shared acquisition engine can update records outside its requested window.
Running it against a disposable copy prevents reinstating rejected later claims
or rewriting current/Sahara curations during this historical extension.
"""
import copy, importlib.util, json, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
FIRST,LAST,TAG='1900-01-01','1919-12-31','historical-0.12'
SEEDS={
 'RUE':('Q34266','Imperio ruso'),
 'AUT-HUN':('Q28513','Austria-Hungría'),
 'OTT':('Q12560','Imperio otomano'),
 'QING':('Q8733','Dinastía Qing'),
 'RPR':('Q139319','Gobierno Provisional / República Rusa'),
}

def read(path):return json.loads(path.read_text(encoding='utf8'))
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')

def merge_window(current,staged):
    result=copy.deepcopy(current)
    portraits={l['person']:copy.deepcopy(l['portrait']) for c in current['countries'].values() for l in c['leaders'] if l.get('portrait')}
    for c in result['countries'].values():c['leaders']=[l for l in c['leaders'] if l.get('acquisition')!=TAG]
    for key,country in staged['countries'].items():
        if key not in result['countries']:
            result['countries'][key]=dict(qid=country['qid'],name=country['name'],flags=[],leaders=[])
        existing=result['countries'][key]['leaders']
        for old in country['leaders']:
            if old.get('acquisition')!=TAG or old['start']>LAST or old['end']<FIRST:continue
            term=copy.deepcopy(old);term.update(start=max(FIRST,old['start']),end=min(LAST,old['end']))
            if term['start']!=old['start']:term.update(startIsCoverageBoundary=True,sourceStart=old['start'])
            if term['end']!=old['end']:term.update(endIsCoverageBoundary=True,sourceEnd=old['end'])
            if term['start']!=old['start'] or term['end']!=old['end']:
                term['note']=(term.get('note','')+' Ventana de adquisición1900–1919; los extremos de cobertura no son nombramientos ni dimisiones.').strip()
            if term['person'] in portraits:term['portrait']=copy.deepcopy(portraits[term['person']])
            if not any(l['person']==term['person'] and l['role']==term['role'] and l['start']==term['start'] and l['end']==term['end'] for l in existing):existing.append(term)
        existing.sort(key=lambda l:(l['start'],l['name'],l['role']))
    result['historicalRetrieved']=staged.get('historicalRetrieved',current.get('historicalRetrieved'))
    return result


if __name__=='__main__':
    spec=importlib.util.spec_from_file_location('historical_acquisition',ROOT/'scripts/enrich-1970-authorities.py')
    h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    staging=ROOT/'.cache/acquire-1900/public'
    for folder in ['data','media']:(staging/folder).mkdir(parents=True,exist_ok=True)
    data=read(ROOT/'public/data/identities.json')
    for key,(qid,name) in SEEDS.items():data['countries'].setdefault(key,dict(qid=qid,name=name,flags=[],leaders=[]))
    save(staging/'data/identities.json',data)
    save(staging/'media/manifest.json',read(ROOT/'public/media/manifest.json'))
    h.OUT=staging;h.START=FIRST;h.PERIOD_END=LAST;h.ACQUISITION=TAG
    h.LIFETIMES.update({'RUE':('1721-11-02','1917-03-15'),'AUT-HUN':('1867-05-29','1918-11-12'),'OTT':('1299-01-01','1922-11-01'),'QING':('1644-01-01','1912-02-12'),'RPR':('1917-03-15','1917-11-06'),'RSR':('1917-11-07','1922-12-29'),'ROC':('1912-01-01','1949-12-31'),'YKM':('1918-12-01','1945-11-28'),'VNM':('1976-07-02',h.TODAY),'VSV':('1949-06-14','1955-10-25'),'MAL':('1948-02-01','1963-09-15'),'UAR':('1958-02-22','1961-09-28')})
    h.acquire(skip_media=True)
    current=read(ROOT/'public/data/identities.json');staged=read(staging/'data/identities.json')
    result=merge_window(current,staged)
    assert result==merge_window(result,staged),'Window merge must be idempotent'
    # All pre-existing statements with exercise in1920+ remain exactly intact.
    for key,c in current['countries'].items():
        assert [l for l in c['leaders'] if l['end']>= '1920-01-01']==[l for l in result['countries'][key]['leaders'] if l['end']>='1920-01-01'],key
        assert c['flags']==result['countries'][key]['flags'],key
    save(ROOT/'public/data/identities.json',result)
    print('Merged isolated1900–1919 acquisition; later terms and all flags unchanged.',flush=True)
