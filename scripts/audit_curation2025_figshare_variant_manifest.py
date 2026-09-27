"""Audit the public Figshare file inventory, not variant contents."""
from pathlib import Path
import json,hashlib,collections
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/curation2025_figshare_27060067_api.json'
x=json.loads(p.read_text())
files=x['files']
variant=[f for f in files if f['name'].startswith('variant_data_PRJNA540917_') and f['name'].endswith('.vcf.gz')]
labels=[f['name'].removeprefix('variant_data_PRJNA540917_').removesuffix('_QL.vcf.gz') for f in variant]
dups=sorted((name,n) for name,n in collections.Counter(labels).items() if n>1)
assert len(files)==102 and len(variant)==98
out={'source_url':x['url_public_html'],'api_url':x['url'],
     'metadata_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'api_file_count':len(files),'variant_files_prjna540917':len(variant),
     'distinct_variant_filename_labels':len(set(labels)),
     'duplicate_filename_labels':dups,
     'other_files':[{'name':f['name'],'size':f['size']} for f in files if f not in variant],
     'total_manifest_bytes':sum(f['size'] for f in files),
     'finding':'The Figshare metadata lists 98 PRJNA540917 per-sample-named variant VCF files but fewer distinct sample labels because one filename repeats. This is a file-level inventory, not the paper’s 330 resequencing-sample ledger or evidence that all 330 payloads were deposited as VCFs.',
     'limits':['Figshare API metadata only; no large variant files downloaded or genotypes examined',
               'Repeated filenames may be separate Figshare file entries or versions; do not infer duplicated biological samples',
               'File count and labels are not individually fetched-and-used sequencing accessions, no comparator or discovery credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
