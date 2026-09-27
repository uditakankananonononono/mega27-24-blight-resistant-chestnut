"""Accession-scope audit of the 2025 Scientific Data chestnut curation paper Table 1.

Parses the archived article XML Table 1 (eight collected Castanea genomes) and
replays each printed data-record accession against archived live ENA portal
reports fetched 2026-09-27. Source-selection QC only; no sequence payload,
no biological inference.
"""
from pathlib import Path
import hashlib, json
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parents[1]
xml=R/'data/sources/pmc12103606.xml'
sha=hashlib.sha256(xml.read_bytes()).hexdigest()
root=ET.parse(xml).getroot()
rows=[]
for tw in root.iter('table-wrap'):
    if (tw.findtext('label') or '').strip()=='Table 1':
        trs=list(tw.iter('tr'))
        header=[' '.join(''.join(td.itertext()).split()) for td in trs[0]]
        assert header==['Genome','Total length (Mb)','N50 length (Mb)','Data records']
        for tr in trs[1:]:
            cells=[' '.join(''.join(td.itertext()).split()) for td in tr]
            rows.append({'genome':cells[0],'total_length_mb':float(cells[1]),
                         'n50_mb':None if cells[2]=='NA' else float(cells[2]),
                         'data_record':cells[3] if len(cells)>3 else None})
assert len(rows)==8
expected=['PRJNA527178','PRJNA540917','PRJNA46687','PRJNA559042','DRA012289','PRJNA769510',None,None]
assert [r['data_record'] for r in rows]==expected

def read_tsv(p):
    lines=p.read_text().splitlines()
    if not lines: return [],[]
    return lines[0].split('\t'),[dict(zip(lines[0].split('\t'),x.split('\t'))) for x in lines[1:] if x.strip()]

accs=['PRJNA527178','PRJNA540917','PRJNA46687','PRJNA559042','PRJNA769510','DRA012289']
ena={}
for a in accs:
    sh,study=read_tsv(R/f'data/sources/curation2025_{a}_ena_study.tsv')
    rh,runs=read_tsv(R/f'data/sources/curation2025_{a}_ena_runs.tsv')
    entry={'study_rows':len(study),'run_rows':len(runs),
           'study_title':study[0].get('study_title') if study else None,
           'first_public':study[0].get('first_public') if study else None,
           'resolves_as_study':len(study)>0,'resolves_via_read_run':len(runs)>0}
    ena[a]=entry
hdr,named=read_tsv(R/'data/sources/curation2025_DRA012289_ena_runs_named.tsv')
orgs={}
for x in named: orgs[x['scientific_name']]=orgs.get(x['scientific_name'],0)+1
samples=len({x['sample_accession'] for x in named})
ena['DRA012289']['run_organism_counts']=orgs
ena['DRA012289']['distinct_samples']=samples

checks={
 'table1_genome_rows':len(rows),
 'table1_rows_with_data_record':sum(1 for r in rows if r['data_record']),
 'table1_rows_without_data_record':[r['genome'] for r in rows if not r['data_record']],
 'ena_resolution':ena,
 'all_printed_accessions_resolve_somehow':all(ena[a]['resolves_as_study'] or ena[a]['resolves_via_read_run'] for a in accs),
 'dra012289_study_lookup_empty_but_runs_resolve':(not ena['DRA012289']['resolves_as_study']) and ena['DRA012289']['resolves_via_read_run'],
 'prjna46687_zero_read_runs_in_portal':ena['PRJNA46687']['run_rows']==0,
 'vanuxem_spelling':{'paper_cultivar':'Vanuxem','ena_study_title_contains':'Vanexum',
    'mismatch': 'Vanuxem' not in (ena['PRJNA46687']['study_title'] or '')},
 'dra012289_organism_scope':{'c_crenata_runs':orgs.get('Castanea crenata',0),
    'hybrid_runs':orgs.get('Castanea sativa x Castanea crenata',0),
    'c_sativa_runs':orgs.get('Castanea sativa',0),'distinct_samples':samples,
    'paper_row_describes':'C. crenata cv. Ginyose genome'},
 'total_length_mb_range':[min(r['total_length_mb'] for r in rows),max(r['total_length_mb'] for r in rows)],
}
out={'paper':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
 'journal':'Scientific Data (2025)','source_file':xml.name,'sha256':sha,
 'ena_fetched':'2026-09-27 (archived TSVs in data/sources/curation2025_*)',
 'table1_rows':rows,'checks':checks,
 'limits':['Metadata-level accession scope check only; no genome assembly or read payload downloaded or analysed',
  'ENA portal state as of 2026-09-27; run counts and titles can change as archives are updated',
  'A resolving accession does not prove the record holds the exact assembly the table row describes; PRJNA46687 has zero read_run rows in the portal, consistent with an assembly-era record, and its assembly was not fetched',
  'Run counts are portal rows, not the 330 resequenced accessions the paper text describes separately'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
