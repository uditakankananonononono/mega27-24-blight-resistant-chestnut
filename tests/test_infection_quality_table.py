import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_quality_table_replays():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_infection_quality_table.py')],text=True))
 assert actual==json.loads((R/'results/infection_quality_table.json').read_text())
 assert actual['sample_count']==15
 assert set(actual['group_summary'])=={'Mock0h','Mock3h','Mock9h','T3h','T9h'}
 assert actual['reported_vs_calculated_mapping_max_absolute_percentage_points']<.005
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
