# SQA Review Record: MIL-006

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-031 |
| CrossReference | [MIL-006], [QC-MIL-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Flask decision: the dynamic site is a Flask application with Jinja templates; new criteria on templates, escaping, the pinned dependency and the layer contract; new tasks 1 to 5 and 7; the documents move to ADR-0003 (ADR-0003)<br>Verdict Go (RC-031) | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-006]
- Checklist used: [QC-MIL-001] and `QC-LANG-001`
- Scope: full review after the Flask decision of S01 (ADR-0003)
- Language and domain: en / it
- Language reviewer: none; S01 reads English and knows the IT domain and confirmed criteria 3, 5 and 9 of `QC-LANG-001` in chat on 2026-11-19
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | A concrete deliverable is defined for every gate | Pass | The Deliverable names the Flask application, the Jinja templates, the pinned dependency, the removals, the documents and ADR-0003. |
| 2 | Explicit Go/No-Go criteria are stated for each gate | Pass | Thirteen Go / No-Go criteria are objectively checkable: a running-server test for freshness and routes, a hostile-text test for escaping, hostile-path tests, header and read-only checks, an inspection of `pyproject.toml`, a search for removed code and an import-linter contract. |
| 3 | Dependencies on other milestones are explicitly mapped | Pass | The dependency on [MIL-005] and its reason are stated. |
| 4 | Each milestone is traceable to a Business Case objective or KPI | Pass | The Traceability table maps to O1, O10, O4, O5, SC1 to SC6, SC10, SC11, CN-008, CN-012 and CN-013. |
| 5 | Milestone owner and approving reviewer are identified | Pass | Owner S01 and approving reviewer S01. |
| 6 | Milestone has a defined target date consistent with project constraints | Pass | The Target Date 2026-11-25 is unchanged and equals the decision date in [PP-001]. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | `Language en`, `Domain it` in the Metadata table. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is BCP 47; `it` is in the registry's domain list. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | The content is English throughout. S01 confirmed the wording and terms of these documents in chat on 2026-11-19 and accepted the plan for the Flask change in chat; S01 may challenge the stand-in review in the end-of-run summary. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | Register is IT Executive English; the text matches it. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | No domain dictionary exists (out of scope in [BC-001]); terms are used consistently. S01 confirmed the wording and terms of these documents in chat on 2026-11-19 and accepted the plan for the Flask change in chat; S01 may challenge the stand-in review in the end-of-run summary. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, headings, IDs and statuses are English. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | Only one file exists for the artifact; no translated twin. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | No earlier accepted version; language and domain have not changed. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The terms are used correctly. S01 confirmed the wording and terms of these documents in chat on 2026-11-19 and accepted the plan for the Flask change in chat; S01 may challenge the stand-in review in the end-of-run summary. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Pass | Identifiers such as O, SC, S and MIL are labelled; tool names are product names. |

## Overall Verdict

Go — every Mandatory criterion of `QC-MIL-001` passes, and criteria 3, 5 and 9 of `QC-LANG-001` were confirmed by S01 in chat on 2026-11-19.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[MIL-006]: ../../milestones/mil-006-dynamic-site-and-cleanup.md
[QC-MIL-001]: ../../../framework/qc/artifacts/qc-milestones-gateways.md
