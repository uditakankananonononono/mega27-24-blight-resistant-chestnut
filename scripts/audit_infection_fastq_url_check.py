"""Audit the archived HEAD verification of 30 advertised infection-cohort file URLs.

Replays deterministically from archived records; downloads no payload bytes.
"""
import csv, hashlib, json, re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
tsv=R/'data/sources/CRA006690_seqout_run_files.tsv'
chk=R/'data/sources/CRA006690_head_check.json'
rows=list(csv.DictReader(tsv.open(newline=''),delimiter='\t'))
head=json.loads(chk.read_text())
checks=head['checks']
assert len(rows)==30 and len(checks)==30
index={(r['fastq_url'],int(r['fastq_bytes']),r['fastq_md5']) for r in rows}
recorded={(c['url'],c['advertised_bytes'],c['advertised_md5']) for c in checks}
assert index==recorded, 'archived HEAD record must cover exactly the index rows'
assert all(c['status']==200 for c in checks)
assert all(c['content_length']==c['advertised_bytes'] for c in checks)
md5s=[c['advertised_md5'] for c in checks]
assert len(set(md5s))==30 and all(re.fullmatch(r'[0-9a-f]{32}',m) for m in md5s)
runs={}
for r in rows: runs.setdefault(r['run_accession'],[]).append(r['filename'])
assert len(runs)==15 and all(len(v)==2 for v in runs.values())
result={'index_url':'https://seqout.org/api/project/CRA006690/runs/download',
 'index_sha256':hashlib.sha256(tsv.read_bytes()).hexdigest(),
 'head_check_record_sha256':hashlib.sha256(chk.read_bytes()).hexdigest(),
 'checked_at_utc':head['checked_at_utc'],'method':head['method'],
 'urls_checked':len(checks),'urls_status_200':sum(c['status']==200 for c in checks),
 'urls_byte_count_exact_match':sum(c['content_length']==c['advertised_bytes'] for c in checks),
 'distinct_md5_values':len(set(md5s)),'runs':len(runs),
 'total_advertised_bytes':sum(c['advertised_bytes'] for c in checks),
 'limits':['HEAD metadata only: status and byte length, no payload bytes, no MD5 verification against content',
  'Byte-count agreement shows the index and host agree on file sizes; it does not prove file contents are the study reads or uncorrupted',
  'A live HEAD at one point in time is availability evidence, not permanence; the primary GSA browse route remained unavailable to this fetcher',
  'No accession dataset fetched-and-used, no expression result, no resistance or biology claim'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
