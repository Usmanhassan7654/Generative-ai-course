import unittest
from experiment import prepare,evaluate
from photos import run

class TestV5(unittest.TestCase):
    def test_disjoint_split(self):
        _,_,_,tr,va,te=prepare('digits'); self.assertFalse(set(tr)&set(va) or set(tr)&set(te) or set(va)&set(te))
    def test_all_predictions_accounted_for(self):
        r=evaluate('digits'); self.assertEqual(sum(r['route_counts'].values()),r['split']['test'])
    def test_every_route_has_audit_trace(self):
        r=evaluate('digits'); self.assertTrue(all('attempts' in t and 'image_sha256' in t for t in r['traces']))
    def test_no_ground_truth_in_attempts(self):
        r=evaluate('digits'); self.assertTrue(all('truth' not in a for t in r['traces'] for a in t['attempts']))
    def test_photos_count(self):
        r=run();self.assertEqual(r['n_test_augmented'],56)
if __name__=='__main__':unittest.main()
