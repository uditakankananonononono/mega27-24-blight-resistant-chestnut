import json,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_reference_not_infection_assay():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/check_reference_not_assay.py')],text=True))
 assert actual==json.loads((R/'results/reference_not_assay.json').read_text())
 assert actual['library_strategy_counts']=={'Hi-C':2,'RNA-Seq':20,'WGS':250}
 assert actual['infection_assay_run_ids_from_this_citation']==[]
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
