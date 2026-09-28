"""Resolve the matrix-only RNA-seq run against ENA and neighboring study records."""
from pathlib import Path
import csv,hashlib,json,re,collections
R=Path(__file__).resolve().parents[1]
source=R/'data/sources'
files={
 'extra_run':source/'curation2025_extra_SRR21681158_ena.tsv',
 'renamed_run':source/'curation2025_renamed_SRR8383229_ena.tsv',
 'source_study':source/'curation2025_PRJNA883560_ena_runs.tsv',
 'figshare_header':source/'curation2025_expression_headers.json',
 'supp_crosswalk':R/'results/curation2025_supplement_expression_crosswalk.json'}
def read(p):
 with p.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
a,b=read(files['extra_run']),read(files['renamed_run'])
study=read(files['source_study'])
assert len(a)==len(b)==1 and len(study)==30
assert a[0]['run_accession']=='SRR21681158' and a[0]['study_accession']=='PRJNA883560'
assert a[0]['sample_alias']=='Z90' and a[0]['library_strategy']=='RNA-Seq'
assert b[0]['run_accession']=='SRR8383229' and b[0]['sample_alias']=='SHW-Gall-A2'
headers=json.loads(files['figshare_header'].read_text())
cols=set(headers['gene_expression/all_exp_fpkm.txt.gz'][1:])
assert all(q['run_accession'] in cols for q in study)
assert a[0]['run_accession'] in cols and 'SRR8383229_SHW_Gall_A2' in cols
cross=json.loads(files['supp_crosswalk'].read_text())
assert cross['prefix_normalized_matrix_only']==[a[0]['run_accession']]
print(json.dumps({'ena_run_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR21681158&result=read_run&fields=run_accession%2Csample_accession%2Csample_alias%2Csample_title%2Cstudy_accession%2Clibrary_strategy%2Cscientific_name&format=tsv',
 'ena_study_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA883560&result=read_run&fields=run_accession%2Csample_accession%2Csample_alias%2Csample_title%2Clibrary_strategy&format=tsv',
 'figshare_dataset_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
 'archived_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()},
 'matrix_only_ena_record':a[0],'suffix_label_ena_record':b[0],
 'study_run_count':len(study),'study_run_overlap_with_matrix':sum(q['run_accession'] in cols for q in study),
 'finding':'The matrix-only SRR21681158 is a live ENA Castanea mollissima RNA-Seq run (sample SAMN30971621, alias Z90, study PRJNA883560); all 30 study run IDs appear in the Figshare expression matrix, but this particular run lacks a Supplementary Table 1 row. The suffix-labeled SRR8383229 resolves with matching SHW-Gall-A2 context.',
 'limits':['ENA metadata corroborates public run identity and study context, not the matrix values or raw-read payload quality.',
           'The source does not explain S1 omission, and one run ID is not necessarily one independent biological specimen; do not call the run invalid.',
           'No genotype, phenotypic resistance, strongest comparator, biological discovery or gate credit.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
