"""Fill documented CShapes omissions with unchanged Natural Earth reference geometry.

These are explicit modern reference outlines, not newly surveyed historical borders.
No unknown successor state is retrojected. Palau's independence is dated separately.
"""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(file):return json.loads((ROOT/'public/data'/file).read_text(encoding='utf-8'))
world=read('countries.geojson');profiles=read('profiles.json')['countries']
codes=['AND','LIE','MCO','SMR','VAT','ATG','DMA','GRD','KNA','LCA','VCT','SYC','STP','NRU','KIR','TUV','VUT','WSM','TON','MHL','FSM','PLW','SAH']
features=[]
for i,code in enumerate(codes):
    f=copy.deepcopy(next(f for f in world['features'] if f['properties']['code']==code))
    p=f['properties'];profile=profiles.get(code,{})
    start='1994-10-01' if code=='PLW' else '1990-01-01'
    source='https://history.state.gov/countries/palau' if code=='PLW' else 'https://www.un.org/en/about-us/growth-in-un-membership'
    if code=='SAH':source='https://www.un.org/dppa/decolonization/en/nsgt/western-sahara'
    p.update(start=start,end='2019-12-31',entityCode='ESH' if code=='SAH' else code,
        originalName=profile.get('englishName',p['name']),capital=profile.get('capital',''),
        caplong=(profile.get('coordinates') or [None,None])[0],caplat=(profile.get('coordinates') or [None,None])[1],
        status='non-self-governing' if code=='SAH' else 'independent',
        politicalStatus='Territorio no autónomo; estatus final pendiente' if code=='SAH' else 'Estado independiente',
        ownerName='',source=source,territorialReference=True,
        note='Contorno de referencia contemporánea Natural Earth 1:10m; entidad ausente de la selección CShapes. No representa levantamientos históricos ni cambios costeros menores.'+
            (' La condición de territorio no autónomo y las autoridades rivales no equivalen a una atribución de soberanía.' if code=='SAH' else ''),
        geometrySource='https://www.naturalearthdata.com/about/terms-of-use/')
    f['id']=900000+i;features.append(f)
out={'type':'FeatureCollection','metadata':{'prepared':'2026-10-22','scope':'1990–2019; explicit modern reference outline supplements','license':'Natural Earth public domain; institutional factual chronology','notes':'1990-01-01 is the coverage floor, not an independence date. Palau starts at actual 1994 independence. Admission to the UN is not used as a universal independence date.'},'features':features}
(ROOT/'public/data/historical-supplements.geojson').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
print(f'Prepared {len(features)} explicit contemporary-reference historical supplements.')
