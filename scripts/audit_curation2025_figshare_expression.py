"""Audit public Figshare expression archive column inventory, not expression values."""
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
api=ROOT/'data/sources/curation2025_figshare_27060067_api.json'
headers_file=ROOT/'data/sources/curation2025_expression_headers.json'
meta=json.loads(api.read_text())
file=next(x for x in meta['files'] if x['name']=='gene_expression.zip')
# Headers were extracted from the independently downloaded ZIP on 2026-09-28;
# the full 25 MB archive is excluded from git; SHA-256 and Figshare MD5 are pinned.
assert file['computed_md5']=='34132bf8c0f62cdc30fda9537ef30d06'
columns=json.loads(headers_file.read_text())
headers={name:{'column_count':len(cols),'sample_column_count':len(cols)-1,
               'first_column':cols[0], 'sample_labels':cols[1:]}
         for name,cols in columns.items()}
main='gene_expression/all_exp_fpkm.txt.gz'
cor='gene_expression/all_exp_fpkm_corr.txt.gz'
raw={k:v for k,v in headers.items() if '/all_exp_raw/' in k}
main_ids=set(headers[main]['sample_labels'])
raw_ids=[x for v in raw.values() for x in v['sample_labels']]
assert len(raw_ids)==len(set(raw_ids))==213
assert set(raw_ids)==main_ids==set(headers[cor]['sample_labels'])
assert {k.split('/')[-1]:v['sample_column_count'] for k,v in raw.items()}=={'count_raw_PE.txt.gz':156,'count_raw_SE.txt.gz':51,'count_raw_SS.txt.gz':6}
out={'paper_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
     'figshare_url':meta['url_public_html'], 'figshare_api_url':meta['url'],
     'archive_download_url':file['download_url'],'archive_md5':file['computed_md5'],
     'archive_sha256':'4d67d18df6b5fff6f80c5ceb8b002e39a892a993205fcf644cb5596e6a7d1f11',
     'extracted_headers_sha256':hashlib.sha256(headers_file.read_bytes()).hexdigest(),
     'file_inventory_count':len(meta['files']),
     'raw_matrix_sample_columns':{k.split('/')[-1]:v['sample_column_count'] for k,v in raw.items()},
     'raw_matrix_sample_total':len(raw_ids),'fpkm_sample_columns':len(main_ids),
     'correlation_matrix_sample_columns':headers[cor]['sample_column_count'],
     'raw_fpkm_correlation_column_identifiers_match':True,
     'other_reference_matrices':[{'file':k,'sample_columns':v['sample_column_count']} for k,v in headers.items() if '/other/' in k],
     'sample_ids':sorted(main_ids),
     'finding':'The published Figshare expression archive contains 213 unique SRR-labelled sample columns across raw count matrices (156 PE, 51 SE, 6 SS), exactly matching both the 213-column FPKM and correlation matrix header lists. Thus the paper’s 213 expression-column inventory is present in Figshare; the four cited GEO series’ 32 samples do not by themselves inventory that full archive.',
     'limits':['Column inventory and archive integrity only; no gene expression values, phenotype labels or read payloads analyzed',
               'The 213 unique column labels establish an archive-level inventory, not independent biological people or verified accession-payload quality',
               'No comparator, discovery, individual accession-use, or paper-page gate credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
