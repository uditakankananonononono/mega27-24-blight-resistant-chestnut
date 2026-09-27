"""Cross-check one linked ENA project runs versus distinct samples and library strategies."""
from pathlib import Path
import csv,collections,hashlib,json
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/curation2025_PRJNA540917_ena_run_samples.tsv'
rows=list(csv.DictReader(p.open(),delimiter='\t'))
assert len(rows)==737
run={r['run_accession'] for r in rows}
sample={r['sample_accession'] for r in rows}
assert len(run)==len(sample)==len(rows)
counts=dict(sorted(collections.Counter(r['library_strategy'] for r in rows).items()))
assert counts=={'Hi-C':1,'WGA':522,'WGS':214}
out={'paper_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
     'ena_report_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA540917&result=read_run&fields=run_accession%2Csample_accession%2Csample_title%2Clibrary_strategy&format=tsv',
     'report_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'report_run_rows':len(rows),'distinct_run_accessions':len(run),'distinct_sample_accessions':len(sample),
     'library_strategy_counts':counts,'paper_printed_curated_resequencing_samples':330,
     'interpretation':'In the linked PRJNA540917 study, the current ENA report holds 737 runs and 737 distinct sample accession labels; 522 entries are library strategy WGA, 214 WGS, and one Hi-C. The paper’s 330 curated resequencing samples have a different curation denominator, and no article-level sample manifest in this check selects them from the 737.',
     'limits':['Single project metadata report, not 737 individually fetched read payloads or genotype analyses',
               'ENA library strategy labels are archival metadata; WGA/WGS labels alone do not establish article inclusion/exclusion',
               'No phenotypic resistance labels, genotype validation, comparator, discovery or gate credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
