import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_curation2025_table1_scope():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_curation2025_table1_scope.py')],text=True))
 assert d==json.loads((R/'results/curation2025_table1_scope.json').read_text())
 c=d['checks']
 assert c['table1_genome_rows']==8 and c['table1_rows_with_data_record']==6
 assert len(c['table1_rows_without_data_record'])==2
 assert c['all_printed_accessions_resolve_somehow'] is True
 assert c['dra012289_study_lookup_empty_but_runs_resolve'] is True
 assert c['prjna46687_zero_read_runs_in_portal'] is True
 assert c['vanuxem_spelling']['mismatch'] is True
 o=c['dra012289_organism_scope']
 assert o['c_crenata_runs']==5 and o['hybrid_runs']==141 and o['c_sativa_runs']==1
 ena=c['ena_resolution']
 assert ena['PRJNA527178']['run_rows']==272 and ena['PRJNA540917']['run_rows']==737
 assert ena['PRJNA559042']['run_rows']==3 and ena['PRJNA769510']['run_rows']==9
 assert all(v==0 for v in d['gate_credit'].values())
