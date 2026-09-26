import json,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_experiment_label_mapping_replays():
 a=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_infection_experiment_labels.py')],text=True))
 assert a==json.loads((R/'results/infection_experiment_labels.json').read_text())
 assert a['experiment_count']==15 and all(n==3 for n in a['five_source_label_group_counts'].values())
 assert a['gate_credit']['fetched_and_used_accession_datasets']==0
