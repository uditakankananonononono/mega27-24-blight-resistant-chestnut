from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
def test_matrix_only_run():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_matrix_only_run.py')],text=True))
    assert x==json.loads((R/'results/curation2025_matrix_only_run.json').read_text())
    assert (x['study_run_count'],x['study_run_overlap_with_matrix'])==(30,30)
    assert x['matrix_only_ena_record']['sample_accession']=='SAMN30971621'
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
