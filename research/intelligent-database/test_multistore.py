import unittest
from multistore import Engine, TEST, evaluate

class MultiStoreSafetyTests(unittest.TestCase):
    def setUp(self): self.engine = Engine()
    def test_cross_tenant_isolation(self):
        # A user must not receive another customer's private record.
        for tenant, query, _, updated, edge in TEST:
            result=self.engine.search(query, tenant, updated, edge)
            if result['answer'] is not None:
                self.assertIn(result['answer'],self.engine.permitted(tenant,updated))
    def test_graph_cannot_cross_tenant(self):
        denied=self.engine.search('linked refund','bob',related_to='R08')
        self.assertTrue(denied['denied'])
        self.assertIsNone(denied['answer'])
    def test_stale_record_excluded(self):
        result=self.engine.search('card tracking guide','public',min_updated=50)
        self.assertNotEqual(result['answer'],'R09')
    def test_graph_path(self):
        result=self.engine.search('associated refund for dispute R08','alice',related_to='R08')
        self.assertEqual(result['answer'],'R03')
    def test_audit_trail(self):
        self.engine.search('card tracking','alice')
        self.assertEqual(self.engine.db.execute('select count(*) from audit').fetchone()[0],1)
    def test_all_12_cases(self):
        rows=evaluate()['rows']
        self.assertEqual(next(r for r in rows if r['method']=='proposed')['correct'],12)

if __name__=='__main__':unittest.main()
