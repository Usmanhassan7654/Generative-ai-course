import unittest
from .benchmark import corpus,evaluate
from .auto_router import Store,AdaptiveRouter,Doc
class RouterTests(unittest.TestCase):
    def test_train_predict(self):
        rows,tr,te=corpus();r=AdaptiveRouter();r.fit(tr,Store(rows));self.assertIn(r.predict(te[0][0]),('exact','semantic','graph'))
    def test_tenant_isolation(self):
        s=Store([Doc('a','secret card',tenant='B'),Doc('b','card',tenant='A')]);self.assertNotIn('a',s.retrieve('card','semantic',tenant='A'))
    def test_stale_exclusion(self):
        s=Store([Doc('a','card',updated=0),Doc('b','card',updated=1000)]);self.assertNotIn('a',s.retrieve('card','semantic'))
    def test_guard_on_graph_neighbor(self):
        s=Store([Doc('a','card delivery',refs=('b',)),Doc('b','private',tenant='B')]);self.assertNotIn('b',s.retrieve('card delivery','graph'))
    def test_benchmark_full(self):
        r=evaluate();self.assertEqual(r['test_n'],60)
if __name__=='__main__':unittest.main()
