import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_run_route_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_infection_run_route.py')],text=True))
 assert actual==json.loads((R/'results/infection_run_route.json').read_text())
 assert actual['experiments']==actual['distinct_runs']==15
 assert actual['advertised_fastq_files']==30
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
