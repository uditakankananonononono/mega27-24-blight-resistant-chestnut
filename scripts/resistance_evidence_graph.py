"""Prototype typed evidence graph that refuses unsupported blight resistance inference."""
from pathlib import Path
import json,collections,hashlib,itertools
R=Path(__file__).resolve().parents[1]
source=R/'results/curation2025_all_expression_sample_units.json'
source_obj=json.loads(source.read_text())
record={r['run']:r for r in source_obj['run_records']}
assert len(record)==213
# No verified VCF-manifest-label to BioSample link or per-BioSample blight phenotype is in the archived source set.
verified_vcf_to_biosample={}
verified_blight_phenotypes={}
def query(runs,vcf_label=None):
 if runs=='all':runs=list(sorted(record))
 assert runs and len(set(runs))==len(runs) and all(r in record for r in runs)
 biosample={record[r]['biosample'] for r in runs}
 species={record[r]['scientific_name'] for r in runs}
 projects={record[r]['bioproject'] for r in runs}
 repeats=[list(pair) for pair in itertools.combinations(sorted(runs),2) if record[pair[0]]['biosample']==record[pair[1]]['biosample']]
 phenotype_covered=all(b in verified_blight_phenotypes for b in biosample)
 genotype_bridge=(vcf_label is not None and verified_vcf_to_biosample.get(vcf_label) in biosample)
 return {'run_count':len(runs),'biosample_count':len(biosample),'species_count':len(species),
         'species':sorted(species),'project_count':len(projects),'same_biosample_run_pair_count':len(repeats),
         'same_biosample_run_pairs':repeats if len(repeats)<=10 else None,
         'mollissima_only_eligible':species=={'Castanea mollissima'},
         'resistance_association_eligible':phenotype_covered and species=={'Castanea mollissima'},
         'genotype_expression_bridge_verified':bool(genotype_bridge),
         'refusals':(["mixed_species_for_mollissima_only" ] if species!={'Castanea mollissima'} else [])+
                    (["missing_per_biosample_blight_phenotype"] if not phenotype_covered else [])+
                    (["unverified_vcf_to_biosample_bridge"] if vcf_label and not genotype_bridge else [])}
cases=json.loads((R/'data/evidence_graph_cases.json').read_text())
results=[]
for x in cases:
 r=query(x['runs'],x.get('vcf_manifest_label'))
 assert (r['run_count'],r['biosample_count'],r['species_count'])==(x['expected_run_count'],x['expected_biosample_count'],x['expected_species_count'])
 results.append({'case_id':x['id'],**r})
print(json.dumps({'source_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
 'sra_runinfo_url':'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo',
 'source_crosswalk_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'cases':results,
 'interpretation':'The typed evidence graph prevents run-column pseudo-replication, mixed-species cohort inference and genotype-to-expression or resistance links absent source crosswalks.',
 'limits':['All six cases are hand-constructed after metadata inspection and have no independent held-out labels or biological resistance phenotypes.',
           'No genotype-expression or blight-phenotype mapping was established; all resistance conclusions abstain by design.',
           'Evidence graphs and BioSample metadata normalization have prior art; this prototype has not established algorithmic novelty or a fair comparator win.',
           'Source runinfo records are metadata; no raw accession read payloads were fetched.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
