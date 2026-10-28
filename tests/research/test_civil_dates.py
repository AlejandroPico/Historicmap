import importlib.util,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from civil_dates import date_key,year_text,period_name,check_window

class CivilDates(unittest.TestCase):
 def test_order_across_era(self):
  dates=['-0100-01-01','-0001-12-31','0001-01-01','2026-10-28']
  self.assertEqual(sorted(reversed(dates),key=date_key),dates)
 def test_no_zero(self):
  for value in ['0000-01-01','-0000-01-01']:
   with self.assertRaises(ValueError):date_key(value)
  with self.assertRaises(ValueError):year_text(0)
 def test_signed_civil_year(self):
  self.assertEqual(year_text(-1),'-0001');self.assertEqual(year_text(1),'0001')
 def test_explicit_era_filenames(self):
  self.assertEqual(period_name(-100,-1),'bc0100-bc0001');self.assertEqual(period_name(1,99),'0001-0099')
 def test_single_era_bounds(self):
  check_window(-100,-1);check_window(1,99)
  for start,end in [(-100,0),(-1,1),(0,99),(-100,-101),(-100,1),(1,101)]:
   with self.assertRaises(ValueError):check_window(start,end)

if __name__=='__main__':unittest.main()
