"""Replay complete SRR-column to NCBI BioSample metadata crosswalk."""
from pathlib import Path
import csv,hashlib,json,re,collections
R=Path(__file__).resolve().parents[1]
header=R/'data/sources/curation2025_expression_headers.json'
meta=json.loads(header.read_text())
matrix=meta['gene_expression/all_exp_fpkm.txt.gz'][1:]
assert len(matrix)==len(set(matrix))==213
run_of=lambda label: re.fullmatch(r'[SED]RR\d+(?:_.*)?',label).group().split('_')[0]
run_to_label={run_of(label):label for label in matrix}
assert len(run_to_label)==213
layouts={}
for key in sorted(meta):
 if key.startswith('gene_expression/all_exp_raw/'):
  for label in meta[key][1:]:
   run=run_of(label);assert run not in layouts
   layouts[run]=key.removeprefix('gene_expression/all_exp_raw/count_raw_').removesuffix('.txt.gz')
assert set(layouts)==set(run_to_label)
files=sorted((R/'data/sources/curation2025_sra_213_runinfo').glob('*.csv'))
assert len(files)==11
raw=[]
for f in files:
 with f.open(newline='') as stream:
  rows=list(csv.DictReader(stream))
  assert rows and all(row['Run'] for row in rows)
  raw+=rows
assert len(raw)==213 and len({r['Run'] for r in raw})==213
assert set(r['Run'] for r in raw)==set(run_to_label)
assert all(re.fullmatch(r'SAMN\d+',r['BioSample']) for r in raw)
assert all(r['ScientificName']=='Castanea mollissima' or r['ScientificName'].startswith('Castanea ') for r in raw)
by_sample=collections.defaultdict(list)
for row in raw:by_sample[row['BioSample']].append(row)
assert len(by_sample)==180
by_study=collections.defaultdict(list)
for row in raw:by_study[row['BioProject']].append(row)
assert len(by_study)==14
cross_layout=[sample for sample,group in by_sample.items() if len({layouts[r['Run']] for r in group})>1]
assert not cross_layout
sum_by_layout={key:{'run_columns':sum(layouts[r['Run']]==key for r in raw),
                    'distinct_biosamples':len({r['BioSample'] for r in raw if layouts[r['Run']]==key})}
               for key in sorted(set(layouts.values()))}
assert sum(v['run_columns'] for v in sum_by_layout.values())==213
assert sum(v['distinct_biosamples'] for v in sum_by_layout.values())==180
out={'source_url':'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo',
     'query_chunk_note':'Eleven CSV responses each requested the 20 (last 13) exact run accessions taken from the 213-column archived Figshare expression header. Each response was checked for exact requested Run set before archiving.',
     'figshare_dataset_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
     'figshare_header_sha256':hashlib.sha256(header.read_bytes()).hexdigest(),
     'source_chunks':[{'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files],
     'matrix_columns':len(matrix),'resolved_run_accessions':len(raw),
     'distinct_biosample_accessions':len(by_sample),
     'runs_per_biosample_distribution':dict(sorted(collections.Counter(len(g) for g in by_sample.values()).items())),
     'study_count':len(by_study),
     'study_units':{name:{'runs':len(group),'biosamples':len(set(r['BioSample'] for r in group))} for name,group in sorted(by_study.items())},
     'layout_units':sum_by_layout,'biosamples_shared_across_layouts':cross_layout,
     'run_records':[{'run':r['Run'],'matrix_label':run_to_label[r['Run']],
                     'biosample':r['BioSample'],'bioproject':r['BioProject'],
                     'matrix_layout':layouts[r['Run']],'sra_layout':r['LibraryLayout'],
                     'scientific_name':r['ScientificName']} for r in sorted(raw,key=lambda r:r['Run'])],
     'finding':'All 213 Figshare expression-matrix run columns resolve to NCBI SRA records, but they represent 180 distinct BioSample accessions; repeated run accessions per BioSample must not be counted as independent sample records.',
     'limits':['BioSample accession cardinality is a database-unit count, not proof of 180 independent individual organisms, plant genotypes or resistance phenotypes.',
               'Multiple runs of one BioSample can have nonidentical count vectors; that does not make them independent biological replicates.',
               'The SRA runinfo CSV is metadata; no individually accessioned FASTQ payload was fetched or used in this audit.',
               'This audits distributed RNA-seq column units and does not assess variant sample membership, blight phenotype, strongest comparator or biological discovery.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
