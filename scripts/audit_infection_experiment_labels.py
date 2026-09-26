"""Audit GSA search labels for the published 15-library Chinese chestnut study."""
from pathlib import Path
import hashlib,json,re
from html import unescape
from collections import Counter
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/CRA006690_experiments_search.html';h=p.read_text()
records=[]
for m in re.finditer(r'<div class="result_area">',h):
 block=h[m.start():m.start()+2500]
 title=re.search(r'result_context">([^<]+)',block);acc=re.search(r'href="[^"]+/CRA006690/(CRX\d+)"',block)
 if title and acc:records.append({'experiment_accession':acc.group(1),'source_label':unescape(title.group(1))})
assert len(records)==15 and len({x['experiment_accession'] for x in records})==15
counts=dict(sorted(Counter(re.match(r'Cm(0|C3|C9|T3|T9)-',x['source_label']).group(1) for x in records).items()))
assert counts=={'0':3,'C3':3,'C9':3,'T3':3,'T9':3}
result={'search_url':'https://ngdc.cncb.ac.cn/gsa/search?searchTerm=CRA006690',
 'experiment_search_url':'https://ngdc.cncb.ac.cn/gsa/search/getSearchByAccession?searchTerm=CRA006690',
 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'experiment_count':len(records),'five_source_label_group_counts':counts,'experiments':sorted(records,key=lambda x:x['experiment_accession']),
 'limits':['Source labels resemble original article five conditions x three replicates, but exact label semantics not independently validated against run payload','Experiment metadata labels are not 15 fetched sequencing read datasets or new biological evidence','GSA individual experiment detail pages return a client-side shell/SOURCE_NOT_AVAILABLE to current fetch; no run files accessed'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
