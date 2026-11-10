import unittest,sys
sys.path.insert(0,'.')
from sample_candidates import select
class TestSampling(unittest.TestCase):
 def rows(self):
  return [{'candidate_id':f'id{i}','requested_domain':'Physics','publication_year':'1970','is_retracted':'False','title':f'Title {i}','openalex_id':f'W{i}','subfield':'Optics'} for i in range(6)]
 def test_determinism(self):
  a,_=select(self.rows(),3);b,_=select(list(reversed(self.rows())),3);self.assertEqual(a,b)
 def test_impact_not_used(self):
  a=self.rows();x,_=select(a,3)
  for r in a:r['cited_by_count']='999999999';r['fwci']='99'
  y,_=select(a,3);self.assertEqual(x,y)
 def test_retracted_excluded(self):
  a=self.rows();a[0]['is_retracted']='True';x,_=select(a,10);self.assertNotIn('id0',[r['candidate_id'] for r in x])
 def test_missing_title_excluded(self):
  a=self.rows();a[0]['title']='';x,_=select(a,10);self.assertNotIn('id0',[r['candidate_id'] for r in x])
 def test_no_discovery_labels(self):
  x,_=select(self.rows(),3);self.assertTrue(all(r['episode_type']=='UNDETERMINED' and r['reconstructable']=='UNASSESSED' for r in x))
if __name__=='__main__':unittest.main()
