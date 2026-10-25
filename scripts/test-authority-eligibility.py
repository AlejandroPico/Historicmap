"""Offline regressions for real-office claims made about fictional characters."""
import importlib.util,pathlib,unittest
s=importlib.util.spec_from_file_location('eligibility',pathlib.Path(__file__).with_name('authority-eligibility.py'))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def entity(*types):return {'id':'fixture','claims':{'P31':[{'mainsnak':{'datavalue':{'value':{'id':t}}}} for t in types]}}
class Eligibility(unittest.TestCase):
 def test_human(self):self.assertTrue(m.real_authority(entity('Q5')))
 def test_fictional(self):self.assertFalse(m.real_authority(entity('Q95074')))
 def test_conflicting(self):self.assertFalse(m.real_authority(entity('Q5','Q15632617')))
 def test_unknown(self):self.assertFalse(m.real_authority({}))
 def test_reviewed_collective(self):self.assertTrue(m.real_authority({'id':'Q30917'}))
if __name__=='__main__':unittest.main()
