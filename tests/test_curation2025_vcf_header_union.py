from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]

def test_header_union_replay():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_vcf_header_union.py')],text=True))
    assert x==json.loads((R/'results/curation2025_vcf_header_union.json').read_text())
    assert [f['sample_column_count'] for f in x['aggregate_vcf_headers']]==[173,61]
    assert x['per_label_vcf_file_count']==98 and x['per_label_unique_labels']==97
    assert x['gbs_rs60_overlap']==x['gbs_per_label_overlap']==[]
    assert x['rs60_per_label_overlap']==['SZ_15']
    assert len(x['union_labels'])==x['distinct_union_labels']==330
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
