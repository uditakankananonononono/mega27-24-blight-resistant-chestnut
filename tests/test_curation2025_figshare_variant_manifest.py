import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_variant_manifest():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_curation2025_figshare_variant_manifest.py')],text=True))
 assert x==json.loads((ROOT/'results/curation2025_figshare_variant_manifest.json').read_text())
 assert x['variant_files_prjna540917']==98
 assert x['distinct_variant_filename_labels']==97
 assert x['duplicate_filename_labels']==[['SM_20',2]]
