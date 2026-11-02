"""Source integrity and globe-safe scope of the human/climate extension; stdlib only in CI."""
from pathlib import Path
import gzip,hashlib,json,math,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_bytes())

class HumanPart5Tests(unittest.TestCase):
 def test_original_ice_files_keep_their_binary_checksums_and_actual_crs(self):
  originals=read('Tierra/Cuaternario/Batchelor2019/fuentes.json')['originals']
  self.assertEqual(len(originals),181)
  for e in originals:
   b=(ROOT/e['file']).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),e['sha256']);self.assertEqual(len(b),e['bytes'])
  audit=read('Tierra/Cuaternario/Batchelor2019/auditoria-geometrias.json')['records']
  self.assertEqual(len(audit),36)
  mis16=next(r for r in audit if r['file'].endswith('/MIS16_max.shp'))
  self.assertEqual(mis16['sourceCRS'],'EPSG:4326');self.assertGreater(mis16['projectedAreaM2'],30e12)
  self.assertTrue(any(r['outsideNorthernHemisphereAreaM2']>1e12 for r in audit))

 def test_all_variants_are_finite_closed_northern_polygons_and_registered_lossless_resources(self):
  index=read('public/data/ice-synthesis-index.json');manifest={e['file']:e for e in read('public/data/manifest.json')['entries']}
  self.assertEqual(len(index['samples']),12);count=0
  for sample in index['samples']:
   variants=set()
   for file in [sample['file']]+sample['uncertaintyFiles']:
    b=(ROOT/'public/data'/file).read_bytes();self.assertEqual(b[9],255);self.assertEqual(hashlib.sha256(b).hexdigest(),manifest[file]['sha256'])
    raw=gzip.decompress(b);self.assertEqual(len(raw),manifest[file]['uncompressedBytes']);data=json.loads(raw);self.assertEqual(len(data['features']),1)
    f=data['features'][0];variants.add(f['properties']['variant']);self.assertEqual(f['geometry']['type'],'MultiPolygon')
    for polygon in f['geometry']['coordinates']:
     for ring in polygon:
      self.assertEqual(ring[0],ring[-1]);self.assertGreaterEqual(len(ring),4)
      for x,y in ring:self.assertTrue(math.isfinite(x)and math.isfinite(y));self.assertTrue(-180.000001<=x<=180.000001 and 0<=y<=90)
      for (x,y),(xx,yy)in zip(ring,ring[1:]):self.assertTrue(abs(x-xx)<=180.000001 or y==yy==90)
    count+=1
   self.assertEqual(variants,{'best','minimum','maximum'})
  self.assertEqual(count,36)

 def test_co2_preserves_every_published_gas_age_value_and_error(self):
  series=read('public/data/ice-core-co2.json');original=(ROOT/series['originalFile']).read_bytes();self.assertEqual(hashlib.sha256(original).hexdigest(),series['originalSha256'])
  rows=[]
  for line in original.decode('utf-8-sig').splitlines():
   if not line.strip()or line.startswith('#'):continue
   try:age,value,error=map(float,line.split()[:3])
   except ValueError:continue
   rows.append(dict(ageBP=age,co2ppm=value,sigmaPpm=error))
  self.assertEqual(series['rows'],sorted(rows,key=lambda r:r['ageBP']));self.assertEqual(len(rows),1901);self.assertEqual(series['referenceEpoch'],1950)

 def test_entity_owned_knowledge_reproduces_offline(self):
  subprocess.run([sys.executable,str(ROOT/'scripts/prepare-human-knowledge.py'),'--check'],cwd=ROOT,check=True,capture_output=True)
  data=read('public/data/human-knowledge.json');self.assertEqual(len(data['articles']),49)
  for a in data['articles']:
   if 'canonicalFile'in a:
    original=read(a['canonicalFile']);self.assertEqual({k:v for k,v in a.items()if k!='canonicalFile'},original)
  for m in data['images']:
   self.assertTrue(m['canonicalFile'].startswith('Tierra/Humanidad/'));self.assertEqual(hashlib.sha256((ROOT/'public'/m['file']).read_bytes()).hexdigest(),m['sha256'])
