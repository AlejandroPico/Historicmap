import importlib.util,pathlib,unittest
P=pathlib.Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('office',P/'scripts/office-infobox.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class OfficeInfoboxTests(unittest.TestCase):
 def test_nested_title_and_bibliography_do_not_replace_the_office(self):
  text='{{Infobox royalty\n| succession = King of Goryeo\n| reign = 997 – 2 March 1009\n| module = {{Infobox Korean name|title=Korean name}}\n| birth_date=980\n}}\n{{cite book|title=Other title}}'
  r=m.extract(text);self.assertEqual(r[0]['office'],'King of Goryeo');self.assertEqual(r[0]['parsed']['start'],'0997-01-01')
 def test_explicit_office_pairs_and_templates(self):
  r=m.extract('{{Infobox officeholder|office=Kanpaku|term_start={{start date|0941|01|01}}|term_end=9 September 949|birth_date=880|death_date=949}}')
  self.assertEqual(len(r),1);self.assertEqual(r[0]['parsed']['start'],'0941-01-01');self.assertEqual(r[0]['office'],'Kanpaku')
 def test_multiple_reigns_and_no_lifetime_fallback(self):
  r=m.extract('{{Infobox royalty|title=King of León|reign=956–958<br>960–966|birth_date=932|death_date=966}}')
  self.assertEqual([v['parsed']['start']for v in r],['0956-01-01','0960-01-01'])
  self.assertEqual(m.extract('{{Infobox person|name=Name|birth_date=900|death_date=999}}'),[])
 def test_circa_and_multiline_footnotes(self):
  r=m.extract('{{Infobox royalty|succession=Ruler|reign={{circa}}13 August 961<ref>one\nline</ref> – 1 January 976}}')
  self.assertEqual(r[0]['parsed']['start'],'0961-08-13')
 def test_abbreviated_years_and_circa_ranges(self):
  r=m.extract('{{Infobox royalty|succession=King|reign=953–77}}');self.assertEqual(r[0]['parsed']['end'],'0977-12-31')
  r=m.extract('{{Infobox royalty|succession=Emperor|reign={{circa|936|939 CE}}}}');self.assertEqual(r[0]['parsed']['end'],'0939-12-31')
 def test_line_break_between_endpoints_is_one_reign(self):
  r=m.extract('{{Infobox royalty|succession=Emperor|reign=20 January 842 –<br>24 September 867}}');self.assertEqual(len(r),1);self.assertEqual(r[0]['parsed']['end'],'0867-09-24')
 def test_capitalized_circa_and_explicit_succession_template(self):
  r=m.extract('{{Infobox royalty|succession=King|reign={{Circa|886}} – 899}}');self.assertEqual(r[0]['parsed']['start'],'0886-01-01')
  text='{{Infobox Korean name|hanja=Name}} {{s-hou|House||||809}} {{s-ttl|title=King of [[Balhae]]|years=794–809}}'
  self.assertEqual(m.extract(text),[]);r=m.extract(text,include_succession=True);self.assertEqual(r[0]['office'],'King of Balhae');self.assertEqual(r[0]['parsed']['start'],'0794-01-01')
if __name__=='__main__':unittest.main()
