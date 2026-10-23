"""Fill documented CShapes omissions with unchanged Natural Earth reference geometry.

These are explicit modern reference outlines, not newly surveyed historical borders.
No successor state is retrojected. Dates are independence/Compact commencement,
not UN admission; the 1970 floor is separately labelled.
"""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(file):return json.loads((ROOT/'public/data'/file).read_text(encoding='utf-8'))
world=read('countries.geojson');profiles=read('profiles.json')['countries']
codes=['AND','LIE','MCO','SMR','VAT','ATG','DMA','GRD','KNA','LCA','VCT','SYC','STP','NRU','KIR','TUV','VUT','WSM','TON','MHL','FSM','PLW','SAH']
# Date and source refer to political existence, not the contemporary coastline.
state='https://history.state.gov/countries/'
dates={
    'ATG':('1981-11-01',state+'antigua-barbuda'),
    'DMA':('1978-11-03',state+'dominica'),
    'GRD':('1974-02-07',state+'grenada'),
    'KNA':('1983-09-19',state+'saint-kitts-nevis'),
    'LCA':('1979-02-22',state+'saint-lucia'),
    'VCT':('1979-10-27',state+'saint-vincent-grenadines'),
    'SYC':('1976-06-29',state+'seychelles'),
    'STP':('1975-07-12',state+'sao-tome-and-principe'),
    'NRU':('1968-01-31','https://www.nauru.gov.nr/parliament-of-naoero/about-parliament/how-was-parliament-established.aspx'),
    'KIR':('1979-07-12',state+'kiribati'),
    'TUV':('1978-10-01',state+'tuvalu'),
    'VUT':('1980-07-30',state+'vanuatu'),
    'WSM':('1962-01-01',state+'samoa'),
    'TON':('1970-06-04',state+'tonga'),
    'MHL':('1986-10-21',state+'marshall-islands'),
    'FSM':('1986-11-03',state+'micronesia'),
    'PLW':('1994-10-01',state+'palau'),
}
features=[]
for i,code in enumerate(codes):
    f=copy.deepcopy(next(f for f in world['features'] if f['properties']['code']==code))
    p=f['properties'];profile=profiles.get(code,{})
    existence,source=dates.get(code,('1970-01-01','https://www.un.org/en/about-us/growth-in-un-membership'))
    start=max('1970-01-01',existence)
    if code=='SAH':
        start='1975-11-14'
        source='https://www.un.org/dppa/decolonization/en/nsgt/western-sahara'
    p.update(start=start,end='2019-12-31',coverageStartIsFloor=code in ['AND','LIE','MCO','SMR','VAT','NRU','WSM'],existenceDate=dates[code][0] if code in dates else None,entityCode='ESH' if code=='SAH' else code,
        originalName=profile.get('englishName',p['name']),capital=profile.get('capital',''),
        caplong=(profile.get('coordinates') or [None,None])[0],caplat=(profile.get('coordinates') or [None,None])[1],
        status='non-self-governing' if code=='SAH' else 'independent',
        politicalStatus='Territorio no autónomo; estatus final pendiente' if code=='SAH' else 'Estado independiente',
        ownerName='',source=source,territorialReference=True,
        note='Contorno de referencia contemporánea Natural Earth 1:10m; entidad ausente de la selección CShapes. No representa levantamientos históricos ni cambios costeros menores.'+
            (' La condición de territorio no autónomo y las autoridades rivales no equivalen a una atribución de soberanía. En 1975 seguía existiendo administración española transitoria; la retirada española terminó el 26 de febrero de 1976. La RASD no se proclamó hasta 1976.' if code=='SAH' else '')+
            (' El inicio de 1970 es el límite de cobertura del suplemento, no una fecha de independencia.' if code in ['AND','LIE','MCO','SMR','VAT','NRU','WSM'] else '')+
            (' La asociación libre con Estados Unidos entró en vigor en 1986; el Consejo de Seguridad terminó formalmente el fideicomiso en 1990 (S/RES/683).' if code in ['MHL','FSM'] else ''),
        geometrySource='https://www.naturalearthdata.com/about/terms-of-use/')
    f['id']=900000+i;features.append(f)
out={'type':'FeatureCollection','metadata':{'prepared':'2026-10-23','scope':'1970–2019; explicit modern reference outline supplements','license':'Natural Earth public domain; institutional factual chronology','notes':'1970-01-01 is the coverage floor for pre-existing states, not independence. Later states begin at documented independence/Compact dates. Western Sahara starts at the CShapes omission in November 1975 and is not equated with the later SADR. Admission to the UN is not used as a universal independence date.'},'features':features}
(ROOT/'public/data/historical-supplements.geojson').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
print(f'Prepared {len(features)} explicit contemporary-reference historical supplements.')
