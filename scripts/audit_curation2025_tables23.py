"""Printed-number integrity replay of Scientific Data 2025 Tables 2 and 3."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
p=root/'data/sources/pmc12103606.xml'; raw=p.read_bytes(); soup=BeautifulSoup(raw,'xml')
tables={t.get('id'):t for t in soup.find_all('table-wrap')}
assert {'Tab2','Tab3'}<=tables.keys()
t2=tables['Tab2'].get_text(' ',strip=True)
t3=tables['Tab3'].get_text(' ',strip=True)
rows=[]
for row in tables['Tab2'].find_all('tr'):
 cells=[c.get_text(' ',strip=True) for c in row.find_all(['td','th'])]
 if len(cells)<4 or not re.search(r'\d+\.\d+%',cells[1]):continue
 nums=[float(x) for x in re.findall(r'\d+\.\d+', ' '.join(cells[1:]))]
 assert len(nums)==5,(cells,nums)
 complete,single,duplicate,fragmented,missing=nums
 rows.append({'genome':cells[0],'complete':complete,'single':single,'duplicated':duplicate,'fragmented':fragmented,'missing':missing,
              'complete_minus_single_duplicate_pct':round(complete-single-duplicate,3),
              'total_minus_100_pct':round(sum((complete,fragmented,missing))-100,3)})
assert len(rows)==8,rows
vals={}
for row in tables['Tab3'].find_all('tr'):
 cells=[c.get_text(' ',strip=True) for c in row.find_all(['td','th'])]
 if len(cells)==3 and cells[0] in ('Total','Common','Specific','Non-matching overlapping'): vals[cells[0]]=cells[1:]
assert all(k in vals for k in ('Total','Common','Specific','Non-matching overlapping'))
rawcounts={k:[int(re.search(r'[\d,]+',v).group().replace(',','')) for v in vals[k]] for k in vals}
assert rawcounts['Common'][0]==rawcounts['Common'][1]
a,b=rawcounts['Total']; shared=rawcounts['Common'][0]
spec_a,spec_b=rawcounts['Specific']; overlap=rawcounts['Non-matching overlapping'][0]
assert rawcounts['Non-matching overlapping'][1]==overlap
assert shared+spec_a+overlap==a and shared+spec_b+overlap==b
printed_pct=[float(re.search(r'\((\d+\.\d+)%\)',v).group(1)) for v in vals['Common']]
computed=[100*shared/a,100*shared/b]
assert all(round(x,3)==y for x,y in zip(computed,printed_pct))
out={'source_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC12103606/',
 'source_sha256':hashlib.sha256(raw).hexdigest(), 'tables':[2,3],
 'checks':{'busco_rows':rows,'busco_max_abs_complete_decomposition_pct':max(abs(r['complete_minus_single_duplicate_pct']) for r in rows),
           'busco_max_abs_total_residual_pct':max(abs(r['total_minus_100_pct']) for r in rows),
           'snp_counts':rawcounts,'snp_totals_decompose_with_nonmatching_overlap':True,
           'snp_printed_common_percentages':printed_pct,'snp_calculated_common_percentages':computed,
           'snp_specific_call_ratio_gatk_to_sentieon':spec_b/spec_a,
           'snp_common_over_union_of_distinct_loci_pct_if_overlap_denominator_assumed':100*shared/(a+b-shared-overlap)},
 'finding':'Both per-caller SNP totals reconcile only after counting the 6,815 non-matching overlapping calls in addition to exact common and specific calls; the two published common percentages also round correctly. The asymmetric caller-specific counts do not establish which calls are true. BUSCO component sums are within displayed rounding precision.',
 'limits':['This is a source-table arithmetic check, not re-calling variants or assessing truth-set accuracy.',
           'The union percentage depends on treating the 6,815 nonmatching overlaps as loci shared between caller lists; this may not equal a variant-allele Jaccard and is descriptive only.',
           'The BUSCO table uses rounded one-decimal percentages, so residuals need not be exactly zero.',
           'No sequence payload fetched or analysed; no accession, audited-derivation, comparator-win, discovery or paper-page gate credit.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
