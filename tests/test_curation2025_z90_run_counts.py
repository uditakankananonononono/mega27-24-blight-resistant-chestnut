from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_z90_run_counts():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_z90_run_counts.py')],text=True))
    assert x==json.loads((R/'results/curation2025_z90_run_counts.json').read_text())
    assert x['gene_count_rows']==33991 and len(x['pairwise'])==3
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
