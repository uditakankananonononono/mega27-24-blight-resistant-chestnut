"""Replay descriptive QC contrasts in published 15-library chestnut table."""
from pathlib import Path
import json,hashlib,statistics
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data/sources/12870_2023_4072_MOESM2_ESM.docx'

def replay():
 table=Document(SOURCE).tables[0]
 assert len(table.rows)==16
 rows=[]
 for row in table.rows[1:]:
  label,clean,mapped,q20,q30,gc,reported=(c.text.strip() for c in row.cells)
  g=label.rsplit('-',1)[0]
  assert g in ('Mock0h','Mock3h','Mock9h','T3h','T9h')
  clean,mapped=int(clean),int(mapped)
  rows.append({'label':label,'group':g,'clean':clean,'mapped':mapped,'mapping_pct':100*mapped/clean,'q30_pct':float(q30.rstrip('%')),'gc_pct':float(gc.rstrip('%'))})
 assert len(rows)==15 and len({r['label'] for r in rows})==15
 groups={}
 for g in ('Mock0h','Mock3h','Mock9h','T3h','T9h'):
  items=[r for r in rows if r['group']==g]
  assert len(items)==3
  groups[g]={'n':3,'unweighted_mapping_mean_pct':statistics.mean(r['mapping_pct'] for r in items), 'read_weighted_mapping_pct':100*sum(r['mapped'] for r in items)/sum(r['clean'] for r in items),'mapping_range_pct':[min(r['mapping_pct'] for r in items),max(r['mapping_pct'] for r in items)],'gc_mean_pct':statistics.mean(r['gc_pct'] for r in items),'q30_mean_pct':statistics.mean(r['q30_pct'] for r in items)}
 m,t=groups['Mock9h'],groups['T9h']
 return {'source':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9901152/supplementaryFiles','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'groups':groups,'nine_hour_contrasts':{'mapping_unweighted_T_minus_Mock_percentage_points':t['unweighted_mapping_mean_pct']-m['unweighted_mapping_mean_pct'],'mapping_read_weighted_T_minus_Mock_percentage_points':t['read_weighted_mapping_pct']-m['read_weighted_mapping_pct'],'gc_T_minus_Mock_percentage_points':t['gc_mean_pct']-m['gc_mean_pct'],'q30_T_minus_Mock_percentage_points':t['q30_mean_pct']-m['q30_mean_pct'],'all_T9_mapping_below_all_Mock9':t['mapping_range_pct'][1]<m['mapping_range_pct'][0]},'interpretation_limits':['These are post-hoc, source-table QC contrasts of 3 versus 3 libraries, not independent infection-resistance measurements or an independent cohort.','Higher T9h GC is a co-occurring feature, not evidence that GC explains the mapping difference. Neither the reference, per-read unmapped sequences nor a multivariable batch analysis was examined.','The T9h-versus-Mock9h map gap remains a sensitivity risk for expression claims; the small Q30 contrast alone cannot identify its mechanism.'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}

if __name__=='__main__': print(json.dumps(replay(),sort_keys=True,indent=2))
