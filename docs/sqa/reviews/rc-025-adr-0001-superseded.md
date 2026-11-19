# SQA Review Record: ADR-0001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-025 |
| CrossReference | [ADR-0001], [QC-ADR-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Superseded by ADR-0002: the static site generator and the JSON data are replaced by SQLite and a dynamic server; the principle of no runtime dependency is kept<br>Verdict Go (RC-025) | [1406a53] |

---

## Artifact Under Review

- Instance reviewed: [ADR-0001]
- Checklist used: [QC-ADR-001]
- Scope: status change after ADR-0002
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The ID (`ADR-NNNN`, 4-digit) matches the filename number and is unique and sequential | Pass | ID ADR-0001 matches the file name and is unchanged. |
| 2 | Context states the problem, the forces (cost, risk, constraints) and the options evaluated | Pass | Context is unchanged. |
| 3 | At least two options were considered, or the absence of alternatives is justified | Pass | Three options are evaluated; unchanged. |
| 4 | Decision is stated in one or two unhedged sentences and matches one of the evaluated options | Pass | The Decision is unchanged. |
| 5 | Consequences list both Positive and Negative outcomes | Pass | Consequences is unchanged. |
| 6 | Quality-attribute impacts (performance, security, portability, etc.) are named where the decision affects them | Pass | Unchanged. |
| 7 | Affected Artifacts are listed as links, and each is also in CrossReference | Pass | [BC-001], [SA-001] and now [ADR-0002] are in CrossReference and linked. |
| 8 | Status changes are recorded as new Version History rows with a Change summary and Commit link; retained rows are never rewritten | Pass | The status change is a new Version History row with a Change summary and the earlier row is kept. |
| 9 | A superseded or deprecated ADR names its successor, and the successor links back | Pass | The record is superseded and its status and Change name ADR-0002, which links back. |
| 10 | Written in business or technical language of the domain, with no unexplained abbreviations | Pass | Unchanged; no unexplained abbreviations. |
| 11 | Status is one of `Proposed`, `Accepted`, `Rejected`, `Deprecated` or `Superseded by ADR-NNNN`, and every Version History row uses only these | Pass | Status is `Superseded by ADR-0002`, an allowed value. |

## Overall Verdict

Go — every Mandatory criterion of `QC-ADR-001` passes.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[ADR-0001]: ../../adr/adr-0001-standard-library-site-generator.md
[QC-ADR-001]: ../../../framework/qc/artifacts/qc-adr.md
[1406a53]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/1406a53bbc208284c38c07a83b3d264ffdea7b00
