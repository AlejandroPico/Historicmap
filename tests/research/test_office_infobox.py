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
 def test_single_regnal_year_is_an_annual_window_not_a_biographical_lifetime(self):
  r=m.extract('{{Infobox royalty|succession=King|reign=757|birth_date=700|death_date=760}}');self.assertEqual(r[0]['parsed'],dict(start='0757-01-01',end='0757-12-31',precision=9))
  self.assertEqual(m.extract('{{Infobox person|birth_date=757|death_date=760}}'),[])
 def test_shared_year_and_spaced_dash_in_an_explicit_reign(self):
  r=m.extract('{{Infobox royalty|succession=Emperor|reign=8 July – 25 July 710}}');self.assertEqual(r[0]['parsed']['start'],'0710-07-08')
  r=m.extract('{{Infobox royalty|succession=King|reign={{circa}} 664{{spaced ndash}}713}}');self.assertEqual(r[0]['parsed']['end'],'0713-12-31')
 def test_dotted_era_markers_are_office_dates(self):
  r=m.extract('{{Infobox royalty|succession=King of Goguryeo|reign=September 618 – October 642 A.D.}}');self.assertEqual(r[0]['parsed']['start'],'0618-09-01')
  r=m.extract('{{Infobox royalty|succession=King|reign=593 – 636 C.E}}');self.assertEqual(r[0]['parsed']['end'],'0636-12-31')
 def test_worded_reign_range_stays_separate_from_personal_dates(self):
  r=m.extract('{{Infobox royalty|succession=Ruler of Bulgars|reign=667 to 690 CE|birth_date=620|death_date=692}}');self.assertEqual(r[0]['parsed']['start'],'0667-01-01');self.assertEqual(r[0]['parsed']['end'],'0690-12-31')
 def test_wrapped_date_is_not_replaced_by_a_short_designation(self):
  r=m.extract('{{Infobox royalty|succession=Eastern Roman emperor|reign=13 August 582 – {{nowr|27 November 602}}|reign_type=Augustus|reign1=5 August 582 – 13 August 582|reign_type1=Caesar}}');self.assertEqual(r[0]['parsed']['end'],'0602-11-27');self.assertEqual(r[1]['reignType'],'Caesar')
 def test_shared_year_in_month_first_reign_and_compact_circa_end(self):
  r=m.extract('{{Infobox royalty|succession=Emperor of Northern Wei|reign=April 2 – May 17, 528}}');self.assertEqual(r[0]['parsed']['start'],'0528-04-02')
  r=m.extract("{{Infobox royalty|succession=Ajaw of Tikal|reign=April 19, 511-c.527}}");self.assertEqual(r[0]['parsed']['end'],'0527-12-31')
 def test_shared_year_with_coregency_annotation_and_asymmetric_spaces(self):
  r=m.extract('{{Infobox royalty|succession=Roman emperor in the West|reign=8 February – 2 September 421 (with Honorius)}}');self.assertEqual(r[0]['parsed']['start'],'0421-02-08');self.assertEqual(r[0]['parsed']['end'],'0421-09-02')
  r=m.extract('{{Infobox royalty|succession=King|reign=c. 497- 537 CE}}');self.assertEqual(r[0]['parsed']['start'],'0497-01-01')
 def test_spaced_nowrap_keeps_exact_augustus_dates_and_caesar_dignity(self):
  r=m.extract('{{Infobox royalty|succession=Roman emperor|reign=9 September 337 – {{no wrap|3 November 361}}|reign_type=Augustus|reign1=8 November 324 – {{nowrap|9 September 337}}|reign_type1=Caesar}}')
  self.assertEqual(r[0]['parsed']['start'],'0337-09-09');self.assertEqual(r[0]['parsed']['end'],'0361-11-03');self.assertEqual(r[1]['reignType'],'Caesar')
 def test_early_common_era_years_and_dash_template(self):
  r=m.extract('{{Infobox royalty|succession=Roman emperor|reign=28 January 98{{snds}}9 August 117}}')
  self.assertEqual(r[0]['parsed']['start'],'0098-01-28');self.assertEqual(r[0]['parsed']['end'],'0117-08-09')
  r=m.extract('{{Infobox royalty|succession=King|reign=70-106 AD}}');self.assertEqual(r[0]['parsed']['start'],'0070-01-01')
  r=m.extract('{{Infobox royalty|succession=Emperor|reign=9 April 88 – 13 February 106}}');self.assertEqual(r[0]['parsed']['start'],'0088-04-09')
 def test_short_years_do_not_parse_bce_as_ce_or_accept_zero(self):
  r=m.extract('{{Infobox royalty|succession=King|reign=57–54 BC}}');self.assertIsNone(r[0]['parsed'])
  r=m.extract('{{Infobox royalty|succession=King|reign=0}}');self.assertIsNone(r[0]['parsed'])
  r=m.extract('{{Infobox royalty|succession=King|reign=1–9}}');self.assertEqual(r[0]['parsed']['end'],'0009-12-31')
  r=m.extract('{{Infobox person|birth_date=1|death_date=99}}');self.assertEqual(r,[])
if __name__=='__main__':unittest.main()
