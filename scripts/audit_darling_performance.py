"""Audit organizer-published Darling performance denominators; no deployment inference."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
SOURCES={'performance':('tacf-performance.html','https://tacf.org/darling-58-performance/'),'discontinuation':('tacf-discontinuation.html','https://tacf.org/tacf-discontinues-development-of-darling-58/')}

def replay():
 pages={}
 for k,(name,url) in SOURCES.items():
  raw=(ROOT/'data/sources'/name).read_bytes()
  text=BeautifulSoup(raw,'html.parser').get_text(' ',strip=True)
  pages[k]={'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'text':text}
 perf,disc=pages['performance']['text'],pages['discontinuation']['text']
 checks={'survivors':r'5 OxO positive survivors of 24 planted.*?19 survivors of 24 planted','height_penalty':r'15% to 25% shorter','identity':r'not from Darling 58, but from a different prototype','discontinued':r'discontinue its development of the Darling 58'}
 quotes={}
 for k,pattern in checks.items():
  text=perf if k in ('survivors','height_penalty') else disc
  m=re.search(pattern,text,re.I)
  if not m:raise ValueError('Original TACF statement missing: '+k)
  quotes[k]=m.group()
 for p in pages.values():p.pop('text')
 return {'sources':pages,'source_claim_checks':quotes,'survival_descriptive':{'oxo_positive_survived':5,'oxo_positive_planted':24,'oxo_negative_survived':19,'oxo_negative_planted':24,'positive_rate':5/24,'negative_rate':19/24,'rate_difference_positive_minus_negative':5/24-19/24},'limits':['These are organizer-reported survival counts at one Virginia Tech field trial, not an independently retrieved underlying individual-tree dataset; unmeasured site and lineage factors prevent causal interpretation.','The source itself says the trees then called Darling 58 were Darling 54 progeny due to identity error. Never aggregate these numbers as verified original Darling 58 performance.','TACF stopped development and support for distribution petitions; these historical data cannot support a current deployment or success claim.','A one-site observational arithmetic contrast is not a fair comparator benchmark, new discovery, 120 individually fetched accession records or a project gate.'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}

if __name__=='__main__':print(json.dumps(replay(),sort_keys=True,indent=2))
