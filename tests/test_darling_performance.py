import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_organizer_claims_and_denominators_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/audit_darling_performance.py')],text=True))
 assert actual==json.loads((ROOT/'results/darling_performance_audit.json').read_text())
 v=actual['survival_descriptive']
 assert v['oxo_positive_planted']==v['oxo_negative_planted']==24
 assert v['rate_difference_positive_minus_negative']==-14/24
 assert 'Darling 58' in actual['source_claim_checks']['identity']
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
