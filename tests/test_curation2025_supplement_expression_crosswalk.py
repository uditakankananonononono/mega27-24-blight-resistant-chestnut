from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_supplement_expression_crosswalk():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_supplement_expression_crosswalk.py')],text=True))
    assert x==json.loads((R/'results/curation2025_supplement_expression_crosswalk.json').read_text())
    assert (x['supplement_distinct_run_ids'],x['figshare_fpkm_columns'])==(212,213)
    assert x['prefix_normalized_matrix_only']==['SRR21681158']
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
