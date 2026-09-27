import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_rnaseq_scope():
    actual = json.loads(subprocess.check_output(['python3', str(ROOT / 'scripts/audit_curation2025_rnaseq_scope.py')], text=True))
    assert actual == json.loads((ROOT / 'results/curation2025_rnaseq_scope.json').read_text())
    c = actual['checks']
    assert c['geo_series_sample_sum'] == 32 and c['unaccounted_samples'] == 181
    assert not c['geo_series_account_for_printed_total']
