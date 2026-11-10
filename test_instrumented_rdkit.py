import json
import unittest
from pathlib import Path
from rdkit import Chem
from instrumented_rdkit import ROOT, canonical, sha, resolve, independent_benchmark_agreement, run

T={r['task_id']:r for r in json.loads((ROOT/'frozen_tasks.json').read_text())['tasks']}

class InstrumentedResearchChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=run(n_repeats=5)
    def test_provenance(self):self.assertEqual(json.loads((ROOT/'frozen_tasks.json').read_text())['source_git_blob'],'72e28188ff5e2f648f1e477c70443882a534e76e')
    def test_task_selection_unique(self):self.assertEqual(len(T),6)
    def test_five_distinct_compounds(self):self.assertEqual(len(set(t['compound'] for t in T.values())),5)
    def test_all_smiles_parse(self):self.assertTrue(all(Chem.MolFromSmiles(t['smiles']) is not None for t in T.values()))
    def test_validated_ibuprofen_graph(self):self.assertEqual(resolve(T['dd_e02'])['TPSA'],37.3)
    def test_metformin_counts(self):self.assertEqual((resolve(T['dd_e03'])['HBD'],resolve(T['dd_e03'])['HBA']),(3,1))
    def test_sorafenib_three_rings(self):self.assertEqual(resolve(T['dd_e10'])['aromatic_rings'],3)
    def test_atorvastatin_formula(self):self.assertEqual(resolve(T['dd_e08'])['formula'],'C33H35FN2O5')
    def test_pains(self):self.assertEqual(resolve(T['dd_e07'])['PAINS_alert_count'],0)
    def test_three_strict_matches(self):self.assertEqual(self.report['strict_target_matches'],3)
    def test_repetitions_count(self):self.assertEqual(self.report['n_traces'],30)
    def test_zero_nan(self):self.assertTrue(all(t['task_id'] in self.report['outputs'] for t in T.values()))
    def test_output_not_conditioned_on_benchmark_target(self):
        t=dict(T['dd_e08']);x=resolve(t);t['benchmark_target']='Corrupted (negative control)';self.assertEqual(x,resolve(t))
    def test_equivalent_smiles_input(self):
        t=dict(T['dd_e02']);x=resolve(t);t['smiles']=Chem.MolToSmiles(Chem.MolFromSmiles(t['smiles']));self.assertEqual(x,resolve(t))
    def test_raw_question_whitespace_negative_control(self):
        t=T['dd_e02'];q=t['question'];self.assertEqual(resolve(t),resolve({**t,'question':q+' '*20}))
        self.assertEqual(len((q+' '*20).encode())-len(q.encode()),20)
    def test_state_serialization_expansion(self):
        import csv
        with (ROOT/'summary.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertTrue(all(int(r['signed_change_bits'])<0 for r in rows))
    def test_label_disagreement_not_silent(self):
        self.assertEqual(independent_benchmark_agreement(T['dd_e10'],resolve(T['dd_e10']))['status'],'mismatch')
    def test_exact_determinism(self):
        self.assertEqual(sha(canonical(resolve(T['dd_e01']))),sha(canonical(resolve(T['dd_e01']))))

if __name__=='__main__':unittest.main()
