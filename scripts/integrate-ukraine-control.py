"""Clip the independently licensed prepared control observations to Natural Earth land.

Input is the output of prepare-ukraine-2022-svg.py; no CShapes geometry enters
this BY-SA derivative. This is an explicit preparation step, never a build download.
"""
import json,pathlib,sys,hashlib,argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.cache/python-packages'))
from shapely.geometry import shape,mapping,Point
from shapely.ops import unary_union
from shapely import make_valid
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input',type=pathlib.Path,required=True);parser.add_argument('--output',type=pathlib.Path,required=True);args=parser.parse_args()
nefile=ROOT/'public/data/countries.geojson';ne=json.loads(nefile.read_text(encoding='utf8'))
land=unary_union([make_valid(shape(f['geometry'])) for f in ne['features'] if f['properties']['code'] in ['UKR','RUS']])
data=json.loads(args.input.read_text(encoding='utf8'))
for f in data['features']:
 g=make_valid(shape(f['geometry'])).intersection(land)
 if g.geom_type=='GeometryCollection':g=unary_union([p for p in g.geoms if p.geom_type in ['Polygon','MultiPolygon']])
 assert not g.is_empty and g.is_valid
 for city,xy in [('Mariupol',(37.55,47.10)),('Melitopol',(35.37,46.85)),('Simferopol',(34.10,44.95))]:assert g.covers(Point(xy)),(f['properties']['start'],city)
 for city,xy in [('Kyiv',(30.52,50.45)),('Lviv',(24.03,49.84)),('Odesa',(30.73,46.48))]:assert not g.covers(Point(xy)),(f['properties']['start'],city)
 f['geometry']=mapping(g);p=f['properties'];p.update(name='Control ruso en Ucrania',note='Observación cartográfica fechada del control ruso; no soberanía ni totalidad de los óblasts reclamados. Incertidumbre de georreferenciación mínima de 7 km; no permite atribuir localidades situadas junto al frente. En 2026 se conserva la referencia del 17/12/2025, no un frente actualizado al día de consulta.',geometryLandClip='Natural Earth 1:10m, dominio público; ninguna geometría CShapes',inputSha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),landSha256=hashlib.sha256(nefile.read_bytes()).hexdigest())
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
print('Prepared',len(data['features']),'dated land-clipped observations; city checks passed')
