from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_all_expression_sample_units():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_all_expression_sample_units.py')],text=True))
    assert x==json.loads((R/'results/curation2025_all_expression_sample_units.json').read_text())
    assert (x['matrix_columns'],x['resolved_run_accessions'],x['distinct_biosample_accessions'])==(213,213,180)
    assert x['runs_per_biosample_distribution']=={'1':163,'2':4,'3':12,'6':1}
    assert x['layout_units']=={'PE':{'distinct_biosamples':128,'run_columns':156},'SE':{'distinct_biosamples':51,'run_columns':51},'SS':{'distinct_biosamples':1,'run_columns':6}}
    assert x['biosamples_shared_across_layouts']==[]
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
