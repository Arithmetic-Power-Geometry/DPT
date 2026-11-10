import unittest
from novelty_audit import experiment,shortest_path,prefix_free
class IdentificationTests(unittest.TestCase):
 def test_observed_upper_bound(self):self.assertEqual(shortest_path([("s","a",5),("a","q",5)]),10)
 def test_unobserved_shortcut(self):self.assertEqual(shortest_path([("s","a",5),("a","q",5),("s","q",1)]),1)
 def test_same_observed_evidence(self):self.assertTrue(experiment()["same_observed_evidence"])
 def test_reversible_prefix_codes(self):
  for x in experiment()["codes"]:self.assertTrue(prefix_free(x["code"]))
 def test_sign_reversal(self):self.assertEqual([x["signed_change_bits"] for x in experiment()["codes"]],[-1,1])
 def test_no_inference_of_true_coordinate(self):self.assertFalse(experiment()["coordinate_identifiability_from_partial_record"])
 def test_negative_cost_disallowed_by_model(self):self.assertTrue(all(c>=0 for _,_,c in experiment()["observed_edges"]))
if __name__=="__main__":unittest.main()
