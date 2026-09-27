"""Triangulate independent file-index rows with primary GSA experiment labels.

The index is a secondary mirror. No sequencing payload is downloaded or interpreted.
"""
import csv,hashlib,json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=R/'data/sources/CRA006690_seqout_run_files.tsv'
labels=json.loads((R/'results/infection_experiment_labels.json').read_text())
expected={r['experiment_accession']:r['source_label'] for r in labels['experiments']}
rows=list(csv.DictReader(source.open(newline=''),delimiter='\t'))
by_experiment=collections.defaultdict(list)
for row in rows:by_experiment[row['experiment_accession']].append(row)
assert set(by_experiment)==set(expected) and len(rows)==30
out=[]
for exp,parts in sorted(by_experiment.items()):
 assert len(parts)==2 and len({p['run_accession'] for p in parts})==1
 assert all(p['library_layout']=='PAIRED' for p in parts)
 assert len({p['filename'] for p in parts})==2
 assert all(p['fastq_url'].startswith('https://download.cncb.ac.cn/gsa2/CRA006690/') for p in parts)
 out.append({'experiment':exp,'source_label':expected[exp],'run':parts[0]['run_accession'],
  'files':[{'filename':p['filename'],'bytes':int(p['fastq_bytes']),'md5':p['fastq_md5'],'url':p['fastq_url']} for p in parts]})
assert len({r['run'] for r in out})==15
print(json.dumps({'primary_experiment_url':labels['experiment_search_url'],
 'secondary_index_url':'https://seqout.org/api/project/CRA006690/runs/download',
 'secondary_index_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'experiments':len(out),'distinct_runs':len({r['run'] for r in out}),'advertised_fastq_files':len(rows),
 'advertised_fastq_bytes':sum(f['bytes'] for r in out for f in r['files']),
 'mapping':out,
 'limits':['Run and file map comes from a third-party index, matched against 15 primary GSA experiment IDs and labels; direct primary run metadata not accessible to this fetch.','Only one file URL HEAD-checked independently; remaining URLs and MD5 values not verified against primary records or payload.','No FASTQ reads downloaded, so accession-data gate count stays zero; neither the labels nor metadata establish a biological result.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
