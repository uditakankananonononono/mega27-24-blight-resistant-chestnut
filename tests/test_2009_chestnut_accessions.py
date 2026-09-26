import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_article_ena_discrepancy():
 p=subprocess.run([sys.executable,str(R/'scripts/audit_2009_chestnut_accessions.py')],capture_output=True,text=True,check=True)
 assert json.loads(p.stdout)==json.loads((R/'results/2009_chestnut_accession_screen.json').read_text())
 x=json.loads(p.stdout)
 assert x['ena_species_at_article_canker_accessions']=={'SRX001804':'Castanea mollissima','SRX001799':'Castanea dentata'}
 assert x['gate_credit']['fetched_and_used_accession_datasets']==0
