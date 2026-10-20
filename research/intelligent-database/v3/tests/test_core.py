import time,unittest
from pace import Evidence,Principal,Request,Planner
class TestCore(unittest.TestCase):
 def setUp(self):
  self.now=int(time.time()); self.rows=[Evidence('a','order shipment delivered','A',0,self.now,'sql'),Evidence('b','shipment provider ETA','A',0,self.now,'graph'),Evidence('c','shipment secret','B',0,self.now,'sql'),Evidence('d','shipment stale','A',0,self.now-999999,'sql'),Evidence('e','shipment confidential','A',4,self.now,'sql')];self.p=Planner(self.rows,[('a','b'),('a','c'),('a','e')]);self.req=Request('shipment',Principal('A',0),self.now,1000,k=3,requires_multihop=True)
 def test_tenant(self):self.assertNotIn('c',self.p.run(self.req)['audit']['returned_ids'])
 def test_freshness(self):self.assertNotIn('d',self.p.run(self.req)['audit']['returned_ids'])
 def test_clearance(self):self.assertNotIn('e',self.p.run(self.req)['audit']['returned_ids'])
 def test_final_guard_even_diagnostic(self):self.assertNotIn('c',self.p.run(self.req,'lexical_all')['audit']['returned_ids'])
 def test_graph(self):self.assertIn('b',self.p.run(self.req)['audit']['returned_ids'])
 def test_provenance(self):self.assertTrue(all('sha256' in x for x in self.p.run(self.req)['evidence']))
 def test_audit(self):self.assertTrue(self.p.run(self.req)['audit']['policy_checked'])
 def test_abstain(self):
  q=Request('shipment',Principal('nonexistent',0),self.now)
  self.assertTrue(self.p.run(q)['audit']['abstained'])
if __name__=='__main__':unittest.main()
