import unittest
from v7 import Stores, Query, answer, experiment
class Tests(unittest.TestCase):
    def create(self):
        s=Stores();s.add('O1','A','dispatched','Nadia',1000);s.finish();return s
    def test_valid(self):self.assertEqual(answer(self.create(),Query('A','O1','status O1'))['answer'],'dispatched')
    def test_cross_tenant(self):self.assertEqual(answer(self.create(),Query('B','O1','status O1'))['status'],'abstain')
    def test_expired(self):self.assertEqual(answer(self.create(),Query('A','O1','status O1',as_of=1300,max_age=100))['status'],'abstain')
    def test_conflicting_doc(self):
        s=Stores();s.add('O1','A','dispatched','Nadia',1000,note_state='delayed');s.finish();self.assertEqual(answer(s,Query('A','O1','status O1'))['reason'],'sql_document_disagreement')
    def test_conflicting_graph(self):
        s=Stores();s.add('O1','A','dispatched','Nadia',1000,edge_driver='Imran');s.finish();self.assertEqual(answer(s,Query('A','O1','which driver O1'))['reason'],'sql_graph_disagreement')
    def test_provenance(self):self.assertEqual(len(answer(self.create(),Query('A','O1','status O1'))['evidence_hashes']),2)
    def test_evaluation(self):self.assertIn('verified',experiment(60)['methods'])
if __name__=='__main__':unittest.main()
