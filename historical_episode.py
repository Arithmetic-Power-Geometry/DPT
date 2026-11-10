"""Historical Shannon/Hartley formula demonstration. No inferred historical DC/QC."""
import math,json
from pathlib import Path

def hartley_binary(): return math.log2(2)
def entropy_binary(p):
    if not 0 <= p <= 1: raise ValueError('probability outside [0,1]')
    return -sum(x*math.log2(x) for x in (p,1-p) if x>0)
def diagnostic(p):
    h=entropy_binary(p)
    return {'p':p,'hartley_uniform_bits_per_symbol':1.0,'shannon_entropy_bits_per_symbol':h,'uniform_minus_entropy_bits_per_symbol':1-h,'historical_DC':'NA','historical_QC':'NA'}
def main():
    output={'historical_episode':'Hartley 1928 -> Shannon 1948','cutoff':'1948-07','contemporaneous_sources':['Hartley 1928','Shannon July 1948'], 'documentary_transition':'fixed-alphabet count -> probability-dependent source uncertainty','source_support':'verified primary paper publications, not a reconstructed individual discovery pathway','model_assumptions':'binary memoryless source; p values chosen as synthetic sensitivity scenarios, not measured historical data','scenario_values':[diagnostic(p) for p in [0.5,0.6,0.75,0.9]],'cost_component_status':{k:'NA: no documented contemporaneous quantitative cost evidence' for k in ['evidence','intervention','computation','conceptual','coordination','verification']},'measured_historical_DC_QC':False}
    Path(__file__).with_name('P06_episode_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
