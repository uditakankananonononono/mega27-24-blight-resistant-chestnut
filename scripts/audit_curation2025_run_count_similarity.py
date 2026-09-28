"""Replay predeclared run/BioSample correlation descriptive QC on deposited gene counts."""
from pathlib import Path
from collections import defaultdict
import csv,gzip,hashlib,json,math,numpy as np
R=Path(__file__).resolve().parents[1]
meta=json.loads((R/'results/curation2025_all_expression_sample_units.json').read_text())
records={r['run']:r for r in meta['run_records']}
header=json.loads((R/'data/sources/curation2025_expression_headers.json').read_text())
files=sorted((R/'data/sources/curation2025_raw_count_matrices').glob('count_raw_*.txt.gz'))
assert len(files)==3
out={'source_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
'zip_sha256_verified_at_extraction':'4d67d18df6b5fff6f80c5ceb8b002e39a892a993205fcf644cb5596e6a7d1f11',
'predeclared_question':'prereg/2026-09-28-run-versus-biosample-count-similarity.md',
'layouts':{},'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
def describe(x):
 if not x:return {'count':0}
 a=np.array(x,dtype=float)
 return {'count':len(a),'min':float(a.min()),'q25':float(np.quantile(a,.25)),
         'median':float(np.median(a)),'q75':float(np.quantile(a,.75)),'max':float(a.max())}
for file in files:
 layout=file.name.removeprefix('count_raw_').removesuffix('.txt.gz')
 key=f'gene_expression/all_exp_raw/{file.name}'
 labels=header[key]
 assert labels[0]=='gene'
 runs=[x.split('_')[0] for x in labels[1:]]
 assert len(runs)==len(set(runs)) and all(records[k]['matrix_layout']==layout for k in runs)
 with gzip.open(file,'rt') as stream:
  reader=csv.reader(stream,delimiter='\t')
  assert next(reader)==labels
  raw=[];genes=[]
  for row in reader:
   assert len(row)==len(labels) and row[0] and row[0] not in genes
   vals=np.array(row[1:],dtype=np.float64)
   assert np.isfinite(vals).all() and (vals>=0).all() and (vals==np.floor(vals)).all()
   genes.append(row[0]);raw.append(np.log1p(vals))
 assert len(genes)==len(set(genes))==33991
 a=np.stack(raw,axis=0)
 cor=np.corrcoef(a,rowvar=False)
 assert np.isfinite(cor).all()
 projects=defaultdict(lambda:{'same_biosample':[],'different_biosample':[]})
 for i in range(len(runs)):
  for j in range(i+1,len(runs)):
   r1,r2=records[runs[i]],records[runs[j]]
   if r1['bioproject']!=r2['bioproject']:continue
   typ='same_biosample' if r1['biosample']==r2['biosample'] else 'different_biosample'
   projects[r1['bioproject']][typ].append(float(cor[i,j]))
 detail={}
 for name,groups in sorted(projects.items()):
  same=describe(groups['same_biosample']);different=describe(groups['different_biosample'])
  detail[name]={'run_columns':sum(records[r]['bioproject']==name for r in runs),
                'distinct_biosamples':len({records[r]['biosample'] for r in runs if records[r]['bioproject']==name}),
                'same_biosample':same,'different_biosample':different,
                'median_same_minus_different':same['median']-different['median'] if same['count'] and different['count'] else None}
 out['layouts'][layout]={'source_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
                         'gene_rows':len(genes),'run_columns':len(runs),'project_pairs':detail,
                         'total_same_biosample_pairs':sum(v['same_biosample']['count'] for v in detail.values()),
                         'total_different_biosample_pairs':sum(v['different_biosample']['count'] for v in detail.values())}
out['limits']=['Correlations of processed count columns across genes are descriptive QC, not independent biological replication or resistance analysis.',
 'Run pairs sharing samples or projects are dependent; no inferential p-value or classifier is fit.',
 'The source matrices are extracted processed Figshare members, not 213 individually fetched raw-read FASTQ payloads.',
 'The 213 matrix columns span species, tissues, projects and preparations; no pooled cross-project biological contrast is claimed.']
print(json.dumps(out,indent=2,sort_keys=True))
