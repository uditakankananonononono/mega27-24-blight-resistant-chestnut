import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_figshare_archive_headers():
    result=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_curation2025_figshare_expression.py')],text=True))
    assert result==json.loads((ROOT/'results/curation2025_figshare_expression.json').read_text())
    assert result['raw_matrix_sample_total']==213
    assert result['raw_fpkm_correlation_column_identifiers_match']
