from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_evidence_graph():
 x=json.loads(subprocess.check_output(['python3',str(R/'scripts/resistance_evidence_graph.py')],text=True))
 assert x==json.loads((R/'results/resistance_evidence_graph.json').read_text())
 assert len(x['cases'])==6
 assert x['cases'][4]['run_count']==213 and x['cases'][4]['biosample_count']==180
 assert all(not c['resistance_association_eligible'] for c in x['cases'])
 assert x['cases'][-1]['genotype_expression_bridge_verified'] is False
 assert x['gate_credit']['fetched_and_used_accession_datasets']==0
