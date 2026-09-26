"""Classify accession use in the original paper; no organism or sequence design."""
import csv,hashlib,json
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import Counter
R=Path(__file__).resolve().parents[1]
article=R/'data/sources/pmc9901152.xml'; review=R/'data/sources/pmc12103606.xml'; ena=R/'data/sources/PRJNA527178_ena_runs.tsv'
r=ET.parse(article).getroot()
paragraphs=[' '.join(p.itertext()) for p in r.findall('.//p')]
citations=[p for p in paragraphs if 'PRJNA527178' in p]
assert len(citations)>=1 and any('reference genome' in p.lower() for p in citations)
with ena.open() as f: rows=list(csv.DictReader(f,delimiter='\t'))
assert len(rows)==272 and len({x['run_accession'] for x in rows})==272
assert {x['scientific_name'] for x in rows}=={'Castanea mollissima'}
strategy=dict(sorted(Counter(x['library_strategy'] for x in rows).items()))
assert strategy=={'Hi-C':2,'RNA-Seq':20,'WGS':250}
result={'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9901152/',
 'dataset_curation_article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
 'ena':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA527178&result=read_run&fields=run_accession%2Cexperiment_accession%2Csample_accession%2Cstudy_accession%2Clibrary_strategy%2Cscientific_name&format=tsv',
 'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [article,review,ena]},
 'study':'PRJNA527178','run_count':len(rows),'library_strategy_counts':strategy,
 'paper_uses_study_as_reference_genome':True,'infection_assay_run_ids_from_this_citation':[],
 'limitations':['Reference-genome citation is not the paper’s infection assay accession','272 run metadata rows do not mean 272 independently fetched-and-used datasets','No raw reads or infection phenotype results were fetched','Darling 58 efficacy and environmental safety are unresolved and require current primary evidence'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
