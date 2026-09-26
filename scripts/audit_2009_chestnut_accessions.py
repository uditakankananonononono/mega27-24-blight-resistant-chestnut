"""Check ENA experiment metadata against the published 2009 chestnut sample list."""
import csv,hashlib,json
from pathlib import Path
from lxml import etree
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/SRX001799-1808_ena_runs.tsv'
rows=list(csv.DictReader(p.open(),delimiter='\t'))
assert len(rows)==14
experiments={}
for row in rows:
 k=row['experiment_accession'];assert not k in experiments or experiments[k]==row['scientific_name']
 experiments[k]=row['scientific_name']
assert len(experiments)==10 and sorted(set(experiments.values()))==['Castanea dentata','Castanea mollissima']
experiment_rows=list(csv.DictReader((R/'data/sources/SRX001799-1808_ena_experiments.tsv').open(),delimiter='\t'))
assert len(experiment_rows)==10
titles={x['experiment_accession']:x['experiment_title'] for x in experiment_rows}
assert 'Castanea dentata' in titles['SRX001799'] and 'Castanea mollissima canker' in titles['SRX001804']
article=etree.parse(str(R/'data/sources/pmc2688492.xml'))
sec=article.xpath("//sec[title[contains(.,'454 sequence from Canker')]]")[0]
text=' '.join(' '.join(sec.itertext()).split())
assert 'Chinese chestnut canker' in text and 'SRX001804 and SRX001799' in text
result={'article_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC2688492/', 'ena_report_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRX001799&result=read_run&fields=run_accession,experiment_accession,sample_accession,study_accession,library_strategy,scientific_name,fastq_ftp,fastq_bytes&format=tsv', 'ena_metadata_sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'article_xml_sha256':hashlib.sha256((R/'data/sources/pmc2688492.xml').read_bytes()).hexdigest(),'ena_experiment_metadata_sha256':hashlib.sha256((R/'data/sources/SRX001799-1808_ena_experiments.tsv').read_bytes()).hexdigest(),'ena_experiment_metadata_url':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRX001804&result=read_experiment&fields=experiment_accession,run_accession,sample_accession,experiment_title,sample_title,scientific_name,study_accession&format=tsv','original_experiment_titles_at_canker_accessions':{k:titles[k] for k in ('SRX001804','SRX001799')},'experiment_count':len(experiments),'run_count':len(rows),'article_canker_accession_order':['SRX001804','SRX001799'],'ena_species_at_article_canker_accessions':{k:experiments[k] for k in ('SRX001804','SRX001799')},'observation':'2009 article canker paragraph maps its American then Chinese libraries to SRX001804 then SRX001799, but ENA original experiment titles and species labels give Chinese then American; do not assign canker-condition sample identity from this paragraph alone.','limits':['10 experiments include non-study experiment IDs SRX001802/1803/1807/1808; 14 runs are metadata only, not independently fetched read datasets','454 EST and old canker samples are not directly comparable to 2023 15-library early infection RNA-seq without measured harmonization','ENA original experiment titles map SRX001804 to Chinese canker and SRX001799 to American, but paper paragraph reverses their species correspondence; corrected publication or author clarification needed to resolve discrepancy'], 'gate_credit':{'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
