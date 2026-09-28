"""Inspect three deposited count columns sharing one ENA sample accession."""
from pathlib import Path
import csv,gzip,hashlib,json,math,statistics
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/curation2025_PRJNA883560_Z90_three_run_counts.tsv.gz'
with gzip.open(p,'rt') as f:
 reader=csv.DictReader(f,delimiter='\t')
 ids=['SRR21681158','SRR21681184','SRR21681185']
 assert reader.fieldnames==['gene']+ids
 genes=[];vectors=[[],[],[]]
 for row in reader:
  genes.append(row['gene'])
  for i,k in enumerate(ids):
   v=float(row[k]);assert math.isfinite(v) and v>=0 and v.is_integer()
   vectors[i].append(int(v))
assert len(genes)==len(set(genes))==33991
sums=[sum(v) for v in vectors]
zeros=[sum(q==0 for q in v) for v in vectors]
logs=[[math.log1p(q) for q in v] for v in vectors]
corr={}
for i in range(3):
 for j in range(i+1,3):
  key=ids[i]+'__'+ids[j]
  corr[key]={'pearson_log1p':statistics.correlation(logs[i],logs[j]),
             'exactly_equal_gene_counts':sum(a==b for a,b in zip(vectors[i],vectors[j]))}
x={'figshare_dataset_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
   'figshare_file_url':'https://ndownloader.figshare.com/files/49310509',
   'source_zip_sha256':'4d67d18df6b5fff6f80c5ceb8b002e39a892a993205fcf644cb5596e6a7d1f11',
   'source_zip_figshare_md5':'34132bf8c0f62cdc30fda9537ef30d06',
   'source_member':'gene_expression/all_exp_raw/count_raw_PE.txt.gz',
   'three_column_extract_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
   'same_ena_sample_accession':'SAMN30971621','same_ena_sample_alias':'Z90',
   'run_ids':ids,'gene_count_rows':len(genes),
   'column_sums':dict(zip(ids,sums)), 'zero_count_rows':dict(zip(ids,zeros)),
   'pairwise':corr,
   'finding':'These three distinct count columns are labeled as three runs but share one ENA sample accession. The matrix-only run is a non-identical count column for the same accession as two supplement-annotated runs, not a new uniquely accessioned biological specimen.',
   'limits':['Processed distributed gene counts, not individually fetched underlying RNA-seq FASTQ read payloads or independently measured samples.',
             'Pairwise count correlation within one ENA sample cannot establish cross-sample replication, differential expression or resistance biology.',
             'The source does not explain whether runs were technical lanes or another design; do not assume they are independent biological replicates.',
             'No strongest comparator, novel biological discovery, 120-accession dataset or project gate credit.'],
   'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(x,indent=2,sort_keys=True))
