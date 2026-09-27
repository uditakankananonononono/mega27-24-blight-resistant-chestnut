import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_tables23():
 actual=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_curation2025_tables23.py')],text=True))
 assert actual==json.loads((ROOT/'results/curation2025_tables23.json').read_text())
 assert len(actual['checks']['busco_rows'])==8
 assert actual['checks']['snp_totals_decompose_with_nonmatching_overlap']
 assert actual['checks']['snp_printed_common_percentages']==[99.943,97.435]
