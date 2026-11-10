import unittest
from operational_measurement import run
class OperationalTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=run()
 def test_three_trajectories(self):self.assertEqual(self.o["n_trajectories"],3)
 def test_one_task(self):self.assertEqual(self.o["n_independent_tasks"],1)
 def test_claim_lengths(self):self.assertEqual([r["claim_utf8_bytes"] for r in self.o["rows"]],[120,700,104])
 def test_signed_changes(self):self.assertEqual([r["naive_signed_change_bits"] for r in self.o["rows"]],[96,-4544,224])
 def test_tokens(self):self.assertEqual([r["estimated_tokens"] for r in self.o["rows"]],[606,934,96])
 def test_unverified(self):self.assertEqual(self.o["n_verified_outcomes"],0)
 def test_no_dc_qc(self):self.assertEqual(self.o["historical_DC_QC_pairs"],0)
if __name__=="__main__":unittest.main()
