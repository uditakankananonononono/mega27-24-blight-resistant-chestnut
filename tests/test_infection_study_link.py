import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_assay_source_not_reference():
 a=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/check_infection_study_link.py')],text=True))
 assert a==json.loads((R/'results/infection_study_link.json').read_text())
 assert a['infection_project']=='PRJCA009200' and a['linked_gsa_study']=='CRA006690'
 assert a['alignment_reference_project']=='PRJNA527178'
 assert a['gate_credit']['fetched_and_used_accession_datasets']==0
