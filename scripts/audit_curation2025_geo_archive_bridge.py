"""Cross-check four archived GEO series sample titles with Figshare column IDs."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
headers=R/'data/sources/curation2025_expression_headers.json'
archive=set(json.loads(headers.read_text())['gene_expression/all_exp_fpkm.txt.gz'][1:])
series=[]
for accession in ['GSE284510','GSE284516','GSE284517','GSE284518']:
    path=R/f'data/sources/curation2025_{accession}_geo_esummary.json'
    document=json.loads(path.read_text())
    record=document['result'][document['result']['uids'][0]]
    assert record['accession']==accession
    samples=[]
    for sample in record['samples']:
        match=re.match(r'^(SRR\d+)_',sample['title'])
        assert match,(accession,sample)
        samples.append({'geo_sample':sample['accession'],'title_run_prefix':match[1],
                        'in_figshare_expression_header':match[1] in archive})
    assert len(samples)==int(record['n_samples'])
    series.append({'accession':accession,'geo_sample_count':len(samples),'samples':samples,
                   'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
all_rows=[row for s in series for row in s['samples']]
matched={r['title_run_prefix'] for r in all_rows if r['in_figshare_expression_header']}
out={'paper_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
     'figshare_url':'https://springernature.figshare.com/articles/dataset/Comprehensive_curation_and_validation_of_genomic_datasets_for_chestnut/27060067',
     'figshare_header_sha256':hashlib.sha256(headers.read_bytes()).hexdigest(),
     'geo_series':series,'geo_rows':len(all_rows),'unique_title_run_prefixes':len(set(r['title_run_prefix'] for r in all_rows)),
     'geo_title_prefixes_in_figshare':len(matched),'figshare_columns_not_named_by_these_geo_rows':len(archive-matched),
     'finding':'Each GEO sample title in the four cited series begins with an SRR label; these title prefixes can be cross-checked against Figshare’s 213 expression columns. This is a GEO-title to archive-header bridge, not a full 213-record provenance map.',
     'limits':['GEO title prefixes are descriptive metadata, not verified GEO-to-SRA provider relations',
               'Archive headers and GEO esummaries only; no read payload, expression values or person-level linkage',
               'No individual accession-use, comparator, discovery, derivation or paper-page credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
