"""A specific reviewed permission must not broaden the automatic image policy."""
import importlib.util,pathlib,sys,unittest
SCRIPTS=pathlib.Path(__file__).resolve().parents[2]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('portrait_acquisition',SCRIPTS/'acquire-century-portraits.py')
portrait=importlib.util.module_from_spec(spec);spec.loader.exec_module(portrait)
class PortraitPermissions(unittest.TestCase):
 def test_explicit_author_grant_is_scoped_to_the_reviewed_file(self):
  self.assertFalse(portrait.reusable_license('Copyrighted free use','unreviewed.jpg',{'reviewed.jpg'}))
  self.assertTrue(portrait.reusable_license('Copyrighted free use','reviewed.jpg',{'reviewed.jpg'}))
  self.assertFalse(portrait.reusable_license('No restrictions','reviewed.jpg',{'reviewed.jpg'}))
  self.assertFalse(portrait.reusable_license('All rights reserved','reviewed.jpg',{'reviewed.jpg'}))
 def test_existing_public_domain_and_cc_permissions_remain_supported(self):
  for label in['Public domain','CC0','CC BY-SA 4.0','CC-BY-3.0']:
   self.assertTrue(portrait.reusable_license(label,'other.jpg',set()))
