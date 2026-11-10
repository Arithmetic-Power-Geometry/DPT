"""Finite-evidence identifiability counterexamples; standard mathematical constructions."""
from itertools import product
import json
def shortest_path(edges, source="s", target="q"):
    best={source:0}
    for _ in range(len(edges)+1):
        for u,v,c in edges:
            if u in best and best.get(v,float("inf"))>best[u]+c:
                best[v]=best[u]+c
    return best.get(target,float("inf"))
def prefix_free(code):
    vals=list(code.values())
    return len(set(vals))==len(vals) and all(not b.startswith(a) for a,b in product(vals,vals) if a!=b)
def experiment():
    observed=[("s","a",5),("a","q",5)]
    model_a=observed[:]
    model_b=observed+[("s","q",1)]
    code_a={"before":"0","after":"10"}
    code_b={"before":"10","after":"0"}
    assert prefix_free(code_a) and prefix_free(code_b)
    assert shortest_path(model_a)==10 and shortest_path(model_b)==1
    return {"observed_edges":observed,"completion_without_hidden_shortcut":{"DC":10},"completion_with_hidden_shortcut":{"DC":1},"same_observed_evidence":True,"codes":[{"code":code_a,"signed_change_bits":len(code_a["before"])-len(code_a["after"])},{"code":code_b,"signed_change_bits":len(code_b["before"])-len(code_b["after"])}],"coordinate_identifiability_from_partial_record":False}
if __name__=="__main__":
    print(json.dumps(experiment(),indent=2))
