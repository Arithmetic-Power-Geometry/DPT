"""P04 preregistration-ready illustrative coordinate calculations; not empirical validation."""
from dataclasses import dataclass
from math import isfinite
from typing import Sequence

@dataclass(frozen=True)
class Coordinates:
    dc: float
    signed_change: float
    qc: float
    expansion: float

def coordinate(costs: Sequence[float], weights: Sequence[float], baseline_bits: float, revised_bits: float) -> Coordinates:
    if not costs or len(costs) != len(weights):
        raise ValueError('Require same nonzero number of costs and weights')
    values = [*costs, *weights, baseline_bits, revised_bits]
    if not all(isfinite(x) for x in values):
        raise ValueError('Non-finite measurement')
    if any(x < 0 for x in costs) or any(w < 0 for w in weights):
        raise ValueError('Negative costs or weights')
    if baseline_bits < 0 or revised_bits < 0:
        raise ValueError('Negative description length')
    if abs(sum(weights) - 1) > 1e-9:
        raise ValueError('Weights must sum to one')
    dc = sum(c*w for c,w in zip(costs,weights))
    delta = baseline_bits-revised_bits
    return Coordinates(dc,delta,max(0.0,delta),max(0.0,-delta))

def sensitivity(costs, weight_scenarios, baseline_scenarios, revised_scenarios):
    if not weight_scenarios or not baseline_scenarios or not revised_scenarios:
        raise ValueError('Nonempty scenarios required')
    results = [coordinate(costs,w,b,r) for w in weight_scenarios for b in baseline_scenarios for r in revised_scenarios]
    return {'dc_interval':[min(x.dc for x in results),max(x.dc for x in results)],
            'signed_interval':[min(x.signed_change for x in results),max(x.signed_change for x in results)],
            'qc_interval':[min(x.qc for x in results),max(x.qc for x in results)],
            'expansion_interval':[min(x.expansion for x in results),max(x.expansion for x in results)],
            'scenario_count':len(results)}
