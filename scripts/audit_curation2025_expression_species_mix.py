"""Replay SRA species labels against the deposited chestnut expression columns."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,openpyxl,re
R=Path(__file__).resolve().parents[1]
cross=R/'results/curation2025_all_expression_sample_units.json'
x=json.loads(cross.read_text())
records=x['run_records']
assert len(records)==213 and len({r['run'] for r in records})==213
species=Counter(r['scientific_name'] for r in records)
assert species=={'Castanea mollissima':209,'Castanea sativa':4}
other=sorted([r for r in records if r['scientific_name']!='Castanea mollissima'],key=lambda r:r['run'])
assert all(r['bioproject']=='PRJNA509688' for r in other)
assert len({r['biosample'] for r in other})==4
supp=R/'data/sources/pmc12103606_supplementary_table1.xlsx'
s=openpyxl.load_workbook(supp,read_only=True,data_only=True).active
rows={}
for values in s.iter_rows(min_row=4,values_only=True):
 if values[0] is not None and re.fullmatch(r'SRR[0-9]+',str(values[0])):
  key=str(values[0]);assert key not in rows;rows[key]=values
assert len(rows)==212
out=[]
for r in other:
 row=rows[r['run']]
 assert row[1]=='bud' and row[2]=='full budburst' and row[4]=='paired end'
 out.append({**r,'supplement_tissue':row[1],'supplement_stage':row[2],'supplement_cultivar':row[3],'supplement_library':row[4]})
assert Counter(v['supplement_cultivar'] for v in out)=={'Madonna':2,'Bouche de Betizac':2}
# Check each metadata row in the same archived SRA CSV payload, not only the prior derived JSON.
raw=[];chunks=sorted((R/'data/sources/curation2025_sra_213_runinfo').glob('*.csv'))
assert len(chunks)==11
for file in chunks:
 with file.open(newline='') as stream:raw.extend(csv.DictReader(stream))
lookup={r['Run']:r for r in raw}
assert len(lookup)==213
for r in out:
 m=lookup[r['run']]
 assert (m['ScientificName'],m['BioProject'],m['BioSample'])==(r['scientific_name'],r['bioproject'],r['biosample'])
print(json.dumps({'article_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
 'figshare_dataset_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
 'sra_source_url':'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo',
 'source_sha256':{'prior_crosswalk':hashlib.sha256(cross.read_bytes()).hexdigest(),
                  'supplement':hashlib.sha256(supp.read_bytes()).hexdigest(),
                  'sra_chunks':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in chunks}},
 'matrix_run_columns':213,'species_labeled_run_columns':dict(sorted(species.items())),
 'species_labeled_distinct_biosamples':dict(sorted(Counter({r['biosample']:r['scientific_name'] for r in records}.values()).items())),
 'non_mollissima_records':out,
 'finding':'Four of 213 distributed expression columns have an SRA Castanea sativa species label, from one BioProject, each a distinct BioSample accession; the linked article supplement annotates them as bud, full budburst, two cultivars.',
 'limits':['The article presents curated datasets across eight Castanea species; the four records are not proof of a curation mistake. They flag mixed species if treating all 213 expression columns as one C. mollissima-only cohort.',
           'One cultivar name may refer to a hybrid; this audit reports only SRA taxonomy labels, not genetic ancestry or a species assay.',
           'Four BioSamples do not establish four independent trees, disease phenotypes or blight-resistance labels.',
           'No read payloads, biological contrast, comparator or new biological discovery is established by this metadata audit.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
