"""Cross-check the 2025 curation paper's printed RNA-Seq sample count.

The paper prints that its collection includes 213 RNA-Seq samples and cites
four GEO series. This replays the archived live GEO esummary records (fetched
2026-09-28), sums the per-series sample counts, and compares against the
printed claim. Metadata-level scope audit only.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json, re
ROOT = Path(__file__).resolve().parents[1]
xml = ROOT / 'data/sources/pmc12103606.xml'
raw = xml.read_bytes()
text = BeautifulSoup(raw, 'xml').get_text(' ', strip=True)
assert '213 RNA-Seq samples' in text
printed_series = sorted(set(re.findall(r'GSE28451[0678]', text)))
assert printed_series == ['GSE284510', 'GSE284516', 'GSE284517', 'GSE284518']
series = []
for acc in printed_series:
    f = ROOT / f'data/sources/curation2025_{acc}_geo_esummary.json'
    doc = json.loads(f.read_text())
    key = next(k for k in doc['result'] if k != 'uids')
    rec = doc['result'][key]
    assert rec['accession'] == acc
    series.append({'accession': acc, 'n_samples': int(rec['n_samples']),
                   'title': rec['title'],
                   'esummary_sha256': hashlib.sha256(f.read_bytes()).hexdigest()})
total = sum(s['n_samples'] for s in series)
out = {
 'paper': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
 'article_sha256': hashlib.sha256(raw).hexdigest(),
 'geo_fetched': '2026-09-28 via NCBI eutils esearch+esummary db=gds (archived JSON)',
 'checks': {
   'printed_rnaseq_samples': 213,
   'printed_geo_series_in_text': printed_series,
   'geo_series': series,
   'geo_series_sample_sum': total,
   'geo_series_account_for_printed_total': total == 213,
   'unaccounted_samples': 213 - total},
 'finding': 'The four GEO series cited in the paper text hold 32 samples in total (7+18+6+1) as of 2026-09-28, not the 213 RNA-Seq samples the paper prints for its collection; 181 samples are not accounted for by the cited series. The paper also distributes expression matrices via a Figshare archive, so this is an unresolved scope/provenance gap in the printed records, not proof that 213 samples do not exist.',
 'limits': ['Archive-metadata counts only; no expression matrix or read payload downloaded',
            'GEO sample counts are live values as of 2026-09-28 and can change',
            'The Figshare file inventory was not enumerated in this audit',
            'No accession-payload, derivation, comparator, discovery, or paper-page gate credit'],
 'gate_credit': {'external_services': 0, 'fetched_and_used_accession_datasets': 0, 'audited_derivations': 0, 'paper_pages': 0}}
print(json.dumps(out, indent=2, sort_keys=True))
