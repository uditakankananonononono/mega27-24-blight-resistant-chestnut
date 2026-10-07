# Hash scope notes (2026-10-08 audit)

This sidecar note labels what the hash and checksum fields in the files below actually cover. The data files themselves are unchanged. It is a documentation clarification, not a license verdict and not a source re-admission.

Audited commit: `38139d7568596ac09137c9859f03857d55f90c31`

## `data/sources/CRA006690_head_check.json`
- Lines (verified against the audited commit): 3, 8, 17, 26, 35, 44, 53, 62, 71, 80, 89, 98, 107, 116, 125, 134, 143, 152, 161, 170, 179, 188, 197, 206, 215, 224, 233, 242, 251, 260, 269 (31 lines)
- Scope: The md5 values are advertised by a third-party index and were obtained with HTTP HEAD requests; no payload bytes were downloaded. They are not payload verification.

## `results/curation2025_variant_source_scope.json`
- Lines (verified against the audited commit): 2-3, 11, 13, 28 (5 lines)
- Scope: The ena_report_sha256 hashes an ENA run-report table, not any variant file or FASTQ payload.

## `data/sources/curation2025_figshare_27060067_api.json`
- Lines (verified against the audited commit): 1 (1 lines)
- Scope: supplied_md5 and computed_md5 are publisher (Figshare) API metadata fields. They are not a local download verification by this project.

