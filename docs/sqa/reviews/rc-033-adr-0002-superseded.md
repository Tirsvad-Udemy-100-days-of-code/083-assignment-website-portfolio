# SQA Review Record: ADR-0002

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-033 |
| CrossReference | [ADR-0002], [QC-ADR-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Superseded by ADR-0003: the web layer is Flask with Jinja templates; the SQLite storage, the read-only server and the safety rules are kept<br>Verdict Go (RC-033) | pending |

---

## Artifact Under Review

- Instance reviewed: [ADR-0002]
- Checklist used: [QC-ADR-001]
- Scope: status change after ADR-0003
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The ID (`ADR-NNNN`, 4-digit) matches the filename number and is unique and sequential | Pass | ID and file name are unchanged. |
| 2 | Context states the problem, the forces (cost, risk, constraints) and the options evaluated | Pass | Context is unchanged. |
| 3 | At least two options were considered, or the absence of alternatives is justified | Pass | Four options are evaluated; unchanged. |
| 4 | Decision is stated in one or two unhedged sentences and matches one of the evaluated options | Pass | The Decision is unchanged. |
| 5 | Consequences list both Positive and Negative outcomes | Pass | Consequences is unchanged. |
| 6 | Quality-attribute impacts (performance, security, portability, etc.) are named where the decision affects them | Pass | Unchanged. |
| 7 | Affected Artifacts are listed as links, and each is also in CrossReference | Pass | [ADR-0003] is now in CrossReference and linked. |
| 8 | Status changes are recorded as new Version History rows with a Change summary and Commit link; retained rows are never rewritten | Pass | The status change is a new Version History row with a Change summary and the earlier row is kept. |
| 9 | A superseded or deprecated ADR names its successor, and the successor links back | Pass | The record is superseded for the web layer and its status and Change name ADR-0003, which links back. |
| 10 | Written in business or technical language of the domain, with no unexplained abbreviations | Pass | Unchanged; no unexplained abbreviations. |
| 11 | Status is one of `Proposed`, `Accepted`, `Rejected`, `Deprecated` or `Superseded by ADR-NNNN`, and every Version History row uses only these | Pass | Status is `Superseded by ADR-0003`, an allowed value. |

## Overall Verdict

Go — every Mandatory criterion of `QC-ADR-001` passes.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[ADR-0002]: ../../adr/adr-0002-sqlite-storage-and-dynamic-site.md
[QC-ADR-001]: ../../../framework/qc/artifacts/qc-adr.md
