from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_variant_source_scope():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_curation2025_variant_source_scope.py')],text=True))
 assert x==json.loads((ROOT/'results/curation2025_variant_source_scope.json').read_text())
 assert x['ena_run_count']==737 and x['figshare_distinct_vcf_filename_labels']==97
