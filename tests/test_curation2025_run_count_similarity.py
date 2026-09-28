from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_processed_count_similarity_replay():
 result=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_curation2025_run_count_similarity.py')],text=True))
 assert result==json.loads((R/'results/curation2025_run_count_similarity.json').read_text())
 assert sum(x['run_columns'] for x in result['layouts'].values())==213
 assert all(x['gene_rows']==33991 for x in result['layouts'].values())
 assert result['layouts']['PE']['project_pairs']['PRJNA883560']['same_biosample']['count']==30
 assert result['layouts']['SS']['project_pairs']['PRJNA912750']['same_biosample']['count']==15
 assert result['gate_credit']['fetched_and_used_accession_datasets']==0
