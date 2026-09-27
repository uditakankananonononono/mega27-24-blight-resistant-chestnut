import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_geo_archive_bridge():
    actual=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_curation2025_geo_archive_bridge.py')],text=True))
    assert actual==json.loads((ROOT/'results/curation2025_geo_archive_bridge.json').read_text())
    assert actual['geo_title_prefixes_in_figshare']==32
    assert actual['figshare_columns_not_named_by_these_geo_rows']==181
