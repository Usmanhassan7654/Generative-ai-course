import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiment import decide
class TestVerifier(unittest.TestCase):
 def test_agreement(self):self.assertEqual(decide([.95,.05],[.9,.1],[.15,.85],.75)[1],'agree')
 def test_disagreement_escalation(self):self.assertEqual(decide([.9,.1],[.1,.9],[.05,.95],.75)[1],'verify')
 def test_abstention(self):self.assertTrue(decide([.9,.05,.05],[.05,.9,.05],[.05,.05,.9],.75)[3])
 def test_no_label_access(self):self.assertEqual(len(decide([.9,.1],[.9,.1],[.1,.9])),4)
if __name__=='__main__':unittest.main()
