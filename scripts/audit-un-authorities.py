"""Compare acquired current authority names with the UN Protocol primary list.

The PDF remains an ignored acquisition artifact. Names are used as factual data;
no UN logo, document layout or photographs are redistributed. Extraction checks
country/office columns, and audit output is reviewed before any curation.
"""
import datetime,difflib,json,pathlib,re,unicodedata
ROOT=pathlib.Path(__file__).resolve().parents[1];CACHE=ROOT/'.cache/identities'
def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def clean(s):
    s=s.replace('\u2060','').replace('\n',' ')
    for a in ['His Excellency','Her Excellency','His Majesty','Her Majesty','Son Excellence','Sa Majesté','Excelentísimo Señor','Excelentísima Señora','Seine Exzellenz','Sua Excelência','Son Altesse','His Royal Highness','Her Royal Highness']:
        s=s.replace(a,'')
    return re.sub(r'\b(Mr|Ms|Dr|Mrs|King|Queen|Sir|Dame|Monsieur|Madame|le Roi|la Reine|Sultan|Emir|Monseigneur)\.?\s*','',s).strip()
natural=json.loads((ROOT/'.cache/natural-countries.json').read_text(encoding='utf8'))
mapping={}
for f in natural['features']:
    p=f['properties'];key=p['ADM0_A3']
    for field in ['NAME','NAME_EN','NAME_LONG','FORMAL_EN','BRK_NAME']:
        if p.get(field):mapping[norm(p[field])]=key
for name,key in {'Bolivia (Plurinational State of)':'BOL','Brunei Darussalam':'BRN','Congo':'COG','Côte d’Ivoire':'CIV','Czechia':'CZE','Democratic People’s Republic of Korea':'PRK','Democratic Republic of the Congo':'COD','Iran (Islamic Republic of)':'IRN','Lao People’s Democratic Republic':'LAO','Micronesia (Federated States of)':'FSM','Naoero':'NRU','Republic of Korea':'KOR','Republic of Moldova':'MDA','Russian Federation':'RUS','Türkiye':'TUR','United Kingdom of Great Britain and Northern Ireland':'GBR','United Republic of Tanzania':'TZA','United States of America':'USA','Venezuela (Bolivarian Republic of)':'VEN','Viet Nam':'VNM','State of Palestine':'PSX','Holy See':'VAT','Syrian Arab Republic':'SYR'}.items():mapping[norm(name)]=key
data=json.loads((ROOT/'public/data/identities.json').read_text(encoding='utf8'))['countries']
rows=json.loads((CACHE/'un-leaders-20261022.json').read_text(encoding='utf8'));out=[]
for row in rows:
    key=mapping.get(norm(row['country']));c=data.get(key,{})
    for office in ['state','government']:
        name=clean(row[office]);nn=norm(name)
        if not nn or nn in ['noprimeminister','sameasheadofstate','asheadofstate','sameasheadstate']:continue
        candidates=[l for l in c.get('leaders',[]) if l['start']<='2026-10-22' and l['end']>='2026-10-20']
        def score(l):
            n=norm(l['name']);return max(difflib.SequenceMatcher(None,n,nn).ratio(),len(n)/len(nn) if n and n in nn else 0)
        best=max(candidates,key=score,default=None)
        out.append(dict(country=row['country'],key=key,office=office,name=name,date=row[office+'Date'],match=best['name'] if best else None,person=best['person'] if best else None,score=round(score(best),3) if best else 0))
(CACHE/'un-comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('UN offices',len(out),'low similarity',sum(r['score']<.58 for r in out))
for row in out:
    if row['score']<.58:print(json.dumps(row,ensure_ascii=True))
