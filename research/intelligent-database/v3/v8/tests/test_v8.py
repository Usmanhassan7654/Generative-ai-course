import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from v8 import EvidenceStore,Request,decide,dataset,evaluate
class Tests(unittest.TestCase):
    def setup(self,sql='delivered',doc='delivered',event='delivered',field='status',graph=None,event_time=999):
        s=EvidenceStore();s.put('s','1','A',field,sql,'sql');s.put('d','1','A',field,doc,'document',995)
        if graph:s.put('g','1','A',field,graph,'graph',995)
        if event:s.put('e','1','A',field,event,'event',event_time)
        return s,Request('A','1',field)
    def test_matching_quorum(self):
        r=decide(*self.setup(),method='v8');self.assertEqual(r['reason'],'verified_quorum');self.assertEqual(r['answer'],'delivered')
    def test_reconcile_sql_error(self):
        r=decide(*self.setup(sql='delayed'),method='v8');self.assertEqual(r['answer'],'delivered');self.assertEqual(r['reason'],'event_reconciled')
    def test_unsubstantiated_event_abstains(self):
        r=decide(*self.setup(sql='delayed',doc='processing',event='delivered'),method='v8');self.assertEqual(r['status'],'abstain')
    def test_stale_event_abstains(self):
        r=decide(*self.setup(sql='delayed',event_time=100),method='v8');self.assertEqual(r['status'],'abstain')
    def test_cross_tenant_abstains(self):
        s,q=self.setup();bad=Request('B',q.order,q.field);self.assertEqual(decide(s,bad)['status'],'abstain')
    def test_clearance_abstains(self):
        s=EvidenceStore();s.put('s','1','A','status','delivered','sql',1000,2);self.assertEqual(decide(s,Request('A','1','status',clearance=0))['status'],'abstain')
    def test_graph_disagreement_escalation(self):
        r=decide(*self.setup(sql='Amir',doc='Amir',event='Nadia',field='driver',graph='Nadia'),method='v8');self.assertEqual(r['answer'],'Nadia')
    def test_reproducibility(self):
        self.assertEqual(evaluate(25,9)['methods'],evaluate(25,9)['methods'])
if __name__=='__main__':unittest.main()
