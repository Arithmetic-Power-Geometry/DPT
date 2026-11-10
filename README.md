# Discovery Plane Theory: reproducibility materials

Research materials for **Measuring Scientific Question Formation: Discovery Complexity, Representational Change, and a Reproducible Research Protocol** (Mohammad Amir Khusru Akhtar and Anand Nayyar).

The repository accompanies the formal and methodological study of **Discovery Complexity (DC)** and **Question Compression (QC)**. It contains analysis code, source-attributed records, frozen cheminformatics tasks, computational execution logs, and deterministic tests. It is not a dataset of measured historical DC/QC coordinates.

## Contents

| Files | Purpose |
| --- | --- |
| `coordinates.py`, `test_coordinates.py` | Conditional coordinate arithmetic and sensitivity checks |
| `sample_candidates.py`, `test_sampling.py` | Deterministic metadata-screening protocol for DiscoveryBench |
| `historical_episode.py`, `archival_measurement.py`, `historical_sample.py`, `external_outcomes.py` | Documentary cases, source-referenced outcome registers and representation examples |
| `proxy_validation.py`, `baselines.py` | Internal diagnostics for the separate generated-question benchmark |
| `records.csv`, `multitask_audit.py`, `novelty_gate.py`, `results.json`, `novelty_results.json` | Nine source-derived scientific-agent records and descriptive comparisons |
| `frozen_tasks.json`, `instrumented_rdkit.py`, `test_instrumented_rdkit.py` | Six frozen OpenDiscoveryTrace chemistry tasks, RDKit computations and checks |
| `execution_traces.jsonl`, `summary.csv`, `result.json` | Original recorded results: 30 executions per task, 180 traces in total |
| `representation_sensitivity.py`, `representation_sensitivity.csv` | Deterministic representation-length sensitivity |
| `test_*.py` | Software checks and mathematical negative controls |

## Data sources and boundaries

**DiscoveryBench v1.1.0** is archived separately on Zenodo: https://doi.org/10.5281/zenodo.21723918 . Its 1,500 OpenAlex records are *bibliographic screening candidates*, not 1,500 validated discovery episodes. `sample_candidates.py` requires the original archived candidate dataset as input.

The **generated-question proxy benchmark** is a distinct input. The required table is `data/question_coordinates_proxy_1000.csv` inside the separate benchmark ZIP, not within DiscoveryBench. The benchmark ZIP is **not included in this repository**. The benchmark package's bibliographic metadata identifies its separate Zenodo record as https://doi.org/10.5281/zenodo.21736251 (public download availability has not been independently verified here). The proxy-analysis scripts and their tests accept the original ZIP location through the `DPT_BENCHMARK_ZIP` environment variable. Its proxy scores and rubric outcomes do not establish independently measured historical DC/QC or externally validated predictive performance.

The **scientific-agent trajectory records** derive from the public OpenDiscoveryTrace sample files and preserve original Git blob identifiers in `records.csv`. Original task-bank source: https://github.com/aayambansal/OpenDiscoveryTrace . Pending upstream verification is not treated as failure or success.

The **180 recorded computational traces** come from six prewritten cheminformatics tasks (30 repetitions per task); these test task resolution and benchmark-answer agreement, **not** historical question formation. Frozen molecular inputs include source-attributed PubChem identifiers. Recorded wall-clock timings are machine-dependent.

## Reproduction

The computational environment recorded in `result.json` is Python 3.13.5 and RDKit 2025.09.4. Install dependencies in a virtual environment:

```bash
python -m pip install -r requirements.txt
```

For local arithmetic, documentary, and task-resolution checks:

```bash
python -m unittest discover -v
```

The RDKit test suite produces a five-repetition temporary trace. To regenerate the **full 180-run series**, run the following *after* the tests:

```bash
python instrumented_rdkit.py
python representation_sensitivity.py
```

The source task outcomes and structural descriptors should be reproducible with matching RDKit versions; timing values and timestamps will differ. Running scripts may overwrite generated result files. The committed results preserve the recorded study outputs.

For the separately archived datasets, after obtaining the appropriate original archive:

```bash
python sample_candidates.py /path/to/discoverybench_archive.zip
export DPT_BENCHMARK_ZIP=/path/to/generated_question_benchmark.zip
python proxy_validation.py "$DPT_BENCHMARK_ZIP"
python baselines.py "$DPT_BENCHMARK_ZIP"
```

The two archive inputs are different; they must not be substituted for one another. The deterministic sampling key used by `sample_candidates.py` is the literal UTF-8 string `DPT-JOI–v1|` (en dash), matching the supplementary protocol.

## Measurement interpretation

An observed discovery pathway supplies at most an upper bound on a globally defined minimum cost unless admissible-path completeness or an independent matching lower bound is proved. Description-length changes require a fixed decoding and representation convention. Reported historical examples do **not** identify comparable DC/QC coordinate pairs. Pareto and scalarisation examples use established multiobjective mathematics; the experiments do not demonstrate predictive superiority over MDL, search-cost, or conventional Pareto baselines.

## Source citation

Akhtar, M. A. K., and Nayyar, A. *Measuring Scientific Question Formation: Discovery Complexity, Representational Change, and a Reproducible Research Protocol*. Manuscript.

Source-specific links and immutable source identifiers accompany the relevant input and analysis files.

The separately archived datasets are not mirrored in full. If a named upstream archive cannot be obtained, the corresponding analysis should be treated as not independently reproducible from this GitHub repository alone.
