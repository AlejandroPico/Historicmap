import importlib.util,pathlib,unittest
spec=importlib.util.spec_from_file_location('dates',pathlib.Path(__file__).resolve().parents[2]/'scripts/authority-identity-dates.py');dates=importlib.util.module_from_spec(spec);spec.loader.exec_module(dates)
def entity(year,precision=9,**extra):return {'claims':{'P570':[{'mainsnak':{'datavalue':{'value':dict(time=year+'-00-00T00:00:00Z',precision=precision,**extra)}}}]}}
class IdentityDates(unittest.TestCase):
 def test_century_is_not_an_exact_death_year(self):self.assertIsNone(dates.precise_life_year(entity('-0900',7),'P570'))
 def test_signed_year_is_retained(self):self.assertEqual(dates.precise_life_year(entity('-0912'),'P570'),-912)
 def test_uncertain_and_missing_dates_are_not_rejections(self):
  self.assertIsNone(dates.precise_life_year(entity('-0912',before=10),'P570'));self.assertIsNone(dates.precise_life_year({},'P570'))
if __name__=='__main__':unittest.main()
