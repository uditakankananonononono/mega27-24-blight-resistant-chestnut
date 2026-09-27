import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_fastq_url_head_check():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_infection_fastq_url_check.py')],text=True))
 assert d==json.loads((R/'results/infection_fastq_url_check.json').read_text())
 assert d['urls_status_200']==30 and d['urls_byte_count_exact_match']==30
 assert d['distinct_md5_values']==30 and d['runs']==15
 assert d['gate_credit']['fetched_and_used_accession_datasets']==0
