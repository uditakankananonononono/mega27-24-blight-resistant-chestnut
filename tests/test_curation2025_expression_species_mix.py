from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_species_mix():
 x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_expression_species_mix.py')],text=True))
 assert x==json.loads((R/'results/curation2025_expression_species_mix.json').read_text())
 assert x['species_labeled_run_columns']=={'Castanea mollissima':209,'Castanea sativa':4}
 assert len({r['biosample'] for r in x['non_mollissima_records']})==4
 assert x['gate_credit']['fetched_and_used_accession_datasets']==0
