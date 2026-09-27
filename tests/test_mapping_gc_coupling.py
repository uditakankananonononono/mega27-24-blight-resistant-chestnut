import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_replay_qc_contrasts():
 actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/audit_mapping_gc_coupling.py')],text=True))
 assert actual==json.loads((ROOT/'results/mapping_gc_coupling.json').read_text())
 c=actual['nine_hour_contrasts']
 assert c['all_T9_mapping_below_all_Mock9']
 assert c['mapping_unweighted_T_minus_Mock_percentage_points'] < -5
 assert c['gc_T_minus_Mock_percentage_points'] > .5
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
