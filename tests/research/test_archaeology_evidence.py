import pathlib,sys,unittest,json,copy
ROOT=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from archaeology_evidence import check_archaeology
from civil_dates import check_window
class ArchaeologicalEvidence(unittest.TestCase):
 def test_five_digit_dates_and_nested_evidence_keep_the_political_limit(self):
  paths=list((ROOT/'Países').glob('*/arqueologia/bc10000-bc6001.json'));self.assertEqual(len(paths),20)
  for p in paths:check_archaeology(json.loads(p.read_text(encoding='utf8')))
  with self.assertRaises(ValueError):check_window(-10000,-6001)
 def test_all_canonical_references_and_separate_political_limit(self):
  paths=list((ROOT/'Países').glob('*/arqueologia.json'));self.assertEqual(len(paths),22)
  for p in paths:check_archaeology(json.loads(p.read_text(encoding='utf8')))
  with self.assertRaises(ValueError):check_window(-6000,-3001)
 def test_forbids_assumed_heads_national_flags_and_borders(self):
  p=next((ROOT/'Países').glob('*/arqueologia.json'));d=json.loads(p.read_text(encoding='utf8'))
  for field in ['leaders','symbols','entityRules']:
   bad=copy.deepcopy(d);bad[field]=[{'invented':True}]
   with self.assertRaises(ValueError):check_archaeology(bad)
 def test_dates_and_sites_cannot_launder_unsupported_certainty(self):
  p=next((ROOT/'Países').glob('*/arqueologia.json'));d=json.loads(p.read_text(encoding='utf8'))
  for field,value in [('capital',True),('coordinates',[181,10]),('source','')]:
   bad=copy.deepcopy(d);bad['places'][0][field]=value
   with self.assertRaises(ValueError):check_archaeology(bad)
  bad=copy.deepcopy(d);bad['coverageEnd']=0
  with self.assertRaises(ValueError):check_archaeology(bad)
 def test_unknown_context_types_are_rejected_before_publication(self):
  p=next(p for p in(ROOT/'Países').glob('*/arqueologia.json')if json.loads(p.read_text(encoding='utf8')).get('contexts'));d=json.loads(p.read_text(encoding='utf8'))
  for field in ['type','confidence']:
   bad=copy.deepcopy(d);bad['contexts'][0].pop(field)
   with self.assertRaises(ValueError):check_archaeology(bad)
if __name__=='__main__':unittest.main()
