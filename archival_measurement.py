"""Source-anchored, analyst-normalized formula artifact measurements.

This script does NOT estimate historical DC, historical QC or question-search infima.
Both expressions were transcribed into a shared analyst-defined notation from
Hartley 1928 and Shannon 1948; they are not verbatim historical formula strings.
"""
import hashlib
import json
import math
import zlib
from pathlib import Path

SOURCES = {
    "hartley1928": {
        "title": "Transmission of Information", "author": "R. V. L. Hartley",
        "year": 1928, "month": 7, "journal": "Bell System Technical Journal",
        "volume": 7, "issue": 3, "pages": "535--563",
        "doi": "10.1002/j.1538-7305.1928.tb01236.x",
        "publisher_url": "https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1928.tb01236.x",
    },
    "shannon1948": {
        "title": "A Mathematical Theory of Communication", "author": "Claude E. Shannon",
        "year": 1948, "month": 7, "journal": "Bell System Technical Journal",
        "volume": 27, "issue": 3, "pages": "379--423",
        "doi": "10.1002/j.1538-7305.1948.tb01338.x",
        "publisher_url": "https://doi.org/10.1002/j.1538-7305.1948.tb01338.x",
    },
}
MODELS = {
    "hartley1928": {"ascii": "H=n*log2(s)", "latex": r"H=n\log_2(s)", "structured": {"measure": "H", "operation": "logarithm", "arguments": ["symbol_count", "selection_count"]}},
    "shannon1948": {"ascii": "H=-sum_i(p_i*log2(p_i))", "latex": r"H=-\sum_i p_i\log_2(p_i)", "structured": {"measure": "H", "operation": "probability_weighted_negative_logarithm", "arguments": ["source_probabilities"]}},
}
COMPONENTS = ["evidence_acquisition", "experimental_intervention", "computational_work", "conceptual_transformation", "coordination", "verification"]

def stable_bytes(key, mode):
    v=MODELS[key][mode]
    if mode=="structured":
        v=json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(",",":"))
    return v.encode("utf-8")

def measurement():
    observations=[]
    for mode in ("ascii","latex","structured"):
        a,b=stable_bytes("hartley1928",mode),stable_bytes("shannon1948",mode)
        observations.append({
            "encoding": mode, "before_byte_count": len(a), "after_byte_count": len(b),
            "signed_byte_difference":len(a)-len(b),
            "signed_bits_difference":8*(len(a)-len(b)),
            "positive_part_bits":max(0,8*(len(a)-len(b))),
            "expansion_bits":max(0,8*(len(b)-len(a))),
            "before_sha256":hashlib.sha256(a).hexdigest(),
            "after_sha256":hashlib.sha256(b).hexdigest(),
        })
    return {
      "evidence":"Dated published conceptual model transition, not observed question generation",
      "source_records":SOURCES,
      "publication_month_interval":240,
      "interval_interpretation":"20 calendar years between two dated publication months; NOT a discovery effort or DC bound",
      "cost_components":{name:{"value":None,"status":"historical resource input not quantified"} for name in COMPONENTS},
      "historical_DC":{"value":None,"reason":"no identified admissible procedure cost distribution, cost units or global lower bound"},
      "historical_QC":{"value":None,"reason":"no matched, historically frozen representation pair or encoding"},
      "representation_comparison":observations,
      "representation_interpretation":"measured bytes of ANALYST-NORMALIZED FORMULA ARTIFACTS; NOT matched historical R/R_q, NOT DPT QC",
      "reproducibility":"UTF-8 byte length of exact strings defined in archived Python source, canonical JSON with sorted keys, no hidden model fitting",
      "inference":"A representation-length difference can be computed, but the source evidence does not identify the historical coordinate; alternative formulas do not by themselves demonstrate equivalent model class or semantics",
    }

if __name__=="__main__":
    p=Path(__file__).with_name("archival_measurements.json")
    p.write_text(json.dumps(measurement(),indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(measurement()["representation_comparison"],indent=2))
