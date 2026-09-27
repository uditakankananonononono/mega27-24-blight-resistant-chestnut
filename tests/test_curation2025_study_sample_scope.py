from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_study_sample_scope():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_curation2025_study_sample_scope.py')],text=True))
 assert x==json.loads((ROOT/'results/curation2025_study_sample_scope.json').read_text())
 assert x['distinct_run_accessions']==x['distinct_sample_accessions']==737
 assert x['library_strategy_counts']=={'Hi-C':1,'WGA':522,'WGS':214}
