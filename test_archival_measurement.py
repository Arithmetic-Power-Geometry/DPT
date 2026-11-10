import unittest
from archival_measurement import measurement,stable_bytes,COMPONENTS
class ArchivalArtifactTests(unittest.TestCase):
 def test_source_count(self): self.assertEqual(len(measurement()['source_records']),2)
 def test_duration_month_not_cost(self): self.assertEqual(measurement()['publication_month_interval'],240)
 def test_all_components_missing(self): self.assertTrue(all(x['value'] is None for x in measurement()['cost_components'].values()))
 def test_historical_coords_missing(self):
  x=measurement();self.assertIsNone(x['historical_DC']['value']);self.assertIsNone(x['historical_QC']['value'])
 def test_byte_formula(self):
  for x in measurement()['representation_comparison']:
   self.assertEqual(x['signed_bits_difference'],8*(x['before_byte_count']-x['after_byte_count']))
 def test_negative_control_formula_whitespace(self):
  a=stable_bytes('hartley1928','ascii'); b=a+b'  '; self.assertNotEqual(len(a),len(b))
 def test_three_encodings(self):self.assertEqual(len(measurement()['representation_comparison']),3)
 def test_all_expansion(self):self.assertTrue(all(x['signed_bits_difference']<0 for x in measurement()['representation_comparison']))
if __name__=='__main__':unittest.main()
