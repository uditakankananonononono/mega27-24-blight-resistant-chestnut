"""Check source-linked assay accession, distinguishing it from the alignment reference."""
from pathlib import Path
import hashlib,json
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parents[1]
article=R/'data/sources/pmc9901152.xml'
project=R/'data/sources/PRJCA009200_ngdc.html'
r=ET.parse(article).getroot(); p=[' '.join(x.itertext()) for x in r.findall('.//p')]
assert any('PRJCA009200' in x and 'sequencing data' in x.lower() for x in p)
assert any('PRJNA527178' in x and 'reference genome' in x.lower() for x in p)
h=project.read_text()
assert 'PRJCA009200' in h and 'CRA006690' in h and 'RNA-Seq of Chinese chestnut' in h
result={'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9901152/',
 'project_page':'https://ngdc.cncb.ac.cn/bioproject/browse/PRJCA009200',
 'infection_project':'PRJCA009200','linked_gsa_study':'CRA006690','alignment_reference_project':'PRJNA527178',
 'sha256':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [article,project]},
 'limitations':['GSA run page unavailable from current fetch (source not available); no raw data or run metadata from CRA006690 fetched','Article reports 15 cDNA libraries, not 15 independently verified accession records','No hypothesis test, benchmark, resistance claim or scientific discovery'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
