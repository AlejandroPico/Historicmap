"""Conservative interior observations where sources disagree on accessions.

These records deliberately leave the disputed transition years unresolved.
Local identifiers represent documented people, not an invented Wikidata match.
"""
import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];p=ROOT/'scripts/review-018-authorities.json';d=json.loads(p.read_text(encoding='utf8'))
rows=[
 ('WADAI-SALIH-DERET','Salih Deret','Kolak / soberano de Wadai',1800,1802),
 ('WADAI-YUSUF-KHARIFAIN','Yusuf Kharifain','Kolak / soberano de Wadai',1814,1828),
 ('WADAI-ABD-AL-AZIZ','Abd al-Aziz','Kolak / soberano de Wadai',1830,1833),
 ('WADAI-MUHAMMAD-SHARIF','Muhammad Sharif · Izz ad-Din','Kolak / soberano de Wadai',1844,1857),
 ('WADAI-ALI','Ali ibn Muhammad Sharif','Kolak / soberano de Wadai',1859,1873),
 ('WADAI-YUSUF-II','Yusuf II','Kolak / soberano de Wadai',1875,1897),
 ('WADAI-IBRAHIM-I','Ibrahim I','Kolak / soberano de Wadai',1899,1900),
 ('BORNU-UMAR-KURA','Umar Kura','Dirigente de facto de Bornu',1838,1845),
 ('BORNU-UMAR-KURA','Umar Kura','Shehu de Bornu',1847,1852),
 ('BORNU-UMAR-KURA','Umar Kura','Shehu de Bornu',1855,1880),
]
d['africanRecords']=[r for r in d.get('africanRecords',[]) if not r.get('interiorObservation')]
for q,name,role,a,b in rows:
 wadai=q.startswith('WADAI-');key='HIST-Q1132786' if wadai else 'HIST-Q1139762';source='https://en.wikipedia.org/wiki/List_of_rulers_of_Wadai' if wadai else 'https://en.wikipedia.org/wiki/Umar_Kura'
 note='Observaciones anuales interiores, no fechas de acceso o cese. '
 note+='Las cronologías difieren en varias sucesiones, especialmente1834–1843; no se rellenan esos años por interpolación.' if wadai else 'Se distingue el poder de facto anterior a1846 del título de shehu. Excluido el interregno de1853–1854.'
 d['africanRecords'].append(dict(key=key,interiorObservation=True,term=dict(person=q,name=name,role=role,start=f'{a}-01-01',end=f'{b}-12-31',precision=9,source=source,note=note)))
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n');print('Retained',len(rows),'conservative African authority observations')
