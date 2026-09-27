"""Compare linked ENA run cardinality with distributed VCF filename labels."""
from pathlib import Path
import csv,collections,json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/curation2025_PRJNA540917_ena_runs.tsv'
a=R/'data/sources/curation2025_figshare_27060067_api.json'
runs=[r['run_accession'] for r in csv.DictReader(p.open(),delimiter='\t')]
assert len(runs)==len(set(runs))==737
meta=json.loads(a.read_text())
files=[f for f in meta['files'] if f['name'].startswith('variant_data_PRJNA540917_')]
labels=[f['name'].removeprefix('variant_data_PRJNA540917_').removesuffix('_QL.vcf.gz') for f in files]
assert len(files)==98 and len(set(labels))==97
out={'paper_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
     'figshare_url':meta['url_public_html'],
     'ena_report_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA540917&result=read_run&fields=run_accession&format=tsv',
     'ena_report_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'figshare_metadata_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),
     'ena_run_count':len(runs),'ena_run_accession_prefix_counts':dict(collections.Counter(r[:5] for r in runs)),
     'figshare_per_label_vcf_file_count':len(files),'figshare_distinct_vcf_filename_labels':len(set(labels)),
     'paper_printed_resequencing_sample_count':330,
     'interpretation':'The linked PRJNA540917 ENA project has 737 run accession rows; the distributed Figshare dataset has 98 per-label VCF file entries but 97 unique labels. Neither denominator is directly the paper’s 330 resequencing samples: one sample can have multiple runs, and aggregate variant files may hold many samples.',
     'limits':['Run accession list was fetched as one report, not 737 individually fetched read payloads',
               'VCF filename labels do not establish per-sample VCF content; no VCF payload downloaded',
               'The run-only report lacks sample labels; a companion richer report now has 737 distinct sample labels, but selection into the paper’s 330 curated records remains unresolved',
               'No biological or variant accuracy inference, comparator, discovery or gate credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
