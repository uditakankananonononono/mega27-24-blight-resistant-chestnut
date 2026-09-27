"""Reproduce a Figshare VCF-header label union from two partial HTTP range captures.

The BGZF byte prefixes are deliberately incomplete; no variant body is interpreted.
"""
from pathlib import Path
import hashlib, json, zlib

R = Path(__file__).resolve().parents[1]
article = json.loads((R/'data/sources/curation2025_figshare_27060067_api.json').read_text())
by_name = {f['name']: f for f in article['files']}
inputs = [
    ('variants_data.GBS173.0.85.0.01.vcf.gz', 'curation2025_gbs173_first_65536_bytes.partial.gz'),
    ('variants_data.RS60.0.7_0.03.vcf.gz', 'curation2025_rs60_first_65536_bytes.partial.gz'),
]
groups = {}
files = []
for name, prefix_name in inputs:
    f = by_name[name]
    raw = (R/'data/sources'/prefix_name).read_bytes()
    assert len(raw) == 65536 and raw[:2] == b'\x1f\x8b'
    # A BGZF stream consists of gzip members. The first member contains the
    # header, so a partial prefix suffices; decompression stops before EOF.
    text = zlib.decompressobj(wbits=31).decompress(raw).decode('utf-8')
    headers = [line for line in text.splitlines() if line.startswith('#CHROM\t')]
    assert len(headers) == 1
    fields = headers[0].split('\t')
    assert fields[:9] == ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']
    labels = fields[9:]
    assert labels and len(labels) == len(set(labels))
    groups[name] = set(labels)
    files.append({'figshare_file_id':f['id'], 'source_url':f['download_url'],
                  'range':f'bytes 0-65535/{f["size"]}', 'archived_prefix':prefix_name,
                  'prefix_sha256':hashlib.sha256(raw).hexdigest(),
                  'sample_column_count':len(labels), 'sample_labels':labels})
per_label_names = [f['name'] for f in article['files'] if f['name'].startswith('variant_data_PRJNA540917_') and f['name'].endswith('_QL.vcf.gz')]
assert len(per_label_names) == 98
per_label = {name.removeprefix('variant_data_PRJNA540917_').removesuffix('_QL.vcf.gz') for name in per_label_names}
a,b=groups.values()
union=a|b|per_label
assert len(a)==173 and len(b)==61 and len(per_label)==97 and len(union)==330
out={'figshare_dataset_url':article['url_public_html'], 'figshare_api_url':article['url'],
     'aggregate_vcf_headers':files, 'per_label_vcf_file_count':len(per_label_names),
     'per_label_unique_labels':len(per_label), 'per_label_labels':sorted(per_label),
     'gbs_rs60_overlap':sorted(a&b), 'gbs_per_label_overlap':sorted(a&per_label),
     'rs60_per_label_overlap':sorted(b&per_label),
     'distinct_union_labels':len(union), 'union_labels':sorted(union),
     'finding':'173 GBS column labels + 61 RS column labels + 97 per-file labels - one overlapping SZ_15 label = 330 unique VCF manifest labels.',
     'limits':['This reconciles a Figshare genotype/variant label inventory to the article’s 330 count; it does not establish membership of the 737 ENA samples in this inventory or connect a label to its sample accession.',
               'Only first 65,536 bytes from each aggregate VCF fetched; no complete VCF, genotype or phenotype data analyzed.',
               'Per-label VCF filenames counted from Figshare API metadata, not fetched as payloads; no independent accession or discovery credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
