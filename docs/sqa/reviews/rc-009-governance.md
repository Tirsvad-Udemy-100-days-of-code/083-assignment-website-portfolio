# SQA Review Record: GOV-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-009 |
| CrossReference | [GOV-001], [QC-GOV-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | pending |

---

## Artifact Under Review

- Instance reviewed: [GOV-001]
- Checklist used: [QC-GOV-001] and `QC-LANG-001`
- Scope: full review
- Language and domain: en / it
- Language reviewer: none; S01 reads English and knows the IT domain and confirmed criteria 3, 5 and 9 of `QC-LANG-001` in chat on 2026-11-19
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Purpose states what is governed and traces to the Business Case's governance and traceability objectives (a framework-level document that cannot cite project artifacts traces to the governance document it supports instead) | Pass | Purpose cites objective O3 and concern CN-002. |
| 2 | Workflow steps are ordered, and every step names the role that performs it | Pass | Each workflow step names its role (submitter S01, reviewer, Accountable S01). |
| 3 | The RACI covers every in-scope artifact type, with exactly one Accountable per category | Pass | The RACI has six categories covering every in-scope type of [BC-001], each with one Accountable (S01). |
| 4 | Roles are stakeholder IDs taken exactly from the Stakeholder Analysis; no invented role names | Pass | Only S01, S02 and S03 are used. |
| 5 | Each verdict (Go, Go-with-conditions, No-Go) defines the resulting artifact status, using only allowed status values | Pass | Go gives Accepted, Go-with-conditions stays Proposed, No-Go stays Proposed or Rejected. |
| 6 | Disputed or No-Go verdicts have an escalation path to a named stakeholder | Pass | Escalation goes to the ARB Chair, S01. |
| 7 | The reviewer-independence rule can be applied: a named alternate exists when the reviewer is the author | Pass | The stand-in rule names the alternate when the reviewer is the author. |
| 8 | Review cadence is stated for artifact instances and for the checklists themselves | Pass | Cadence states per-instance reviews and that the checklists belong to the framework. |
| 9 | The document links the process artifacts it relies on (traceability matrix, review process, process model) | Pass | Links to [TM-001], [PRC-001] and [PP-001]. |
| 10 | Written without duplicated words or unexplained abbreviations | Pass | Short sentences without duplicated words. |
| 11 | A blocking finding (a `Fail` on a Mandatory criterion, or an open security finding rated High or Critical) gives `No-Go`; `Go-with-conditions` is allowed only for findings that do not block | Pass | Escalation Rules state that a blocking finding gives No-Go. |
| 12 | A risk exception that lets a blocking finding pass names the finding, the owner, an approver who is neither the author nor the owner, an expiry date and the compensating controls; an expired exception is blocking again | Pass | The document states that no risk exception is available, so none can be invalid. |
| 13 | A criterion only a person can confirm stays `Pending` until a named reviewer independent of the author confirms it; the author's own assessment, a stand-in's or an AI author's, never closes it | Pass | The Escalation Rules keep a person-only criterion Pending until S01 confirms it in chat. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | `Language en`, `Domain it` in the Metadata table. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is BCP 47; `it` is in the registry's domain list. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | The content is English throughout. S01 confirmed in chat on 2026-11-19. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | Register is IT Executive English; the text matches it. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | No domain dictionary exists (out of scope in [BC-001]); terms are used consistently. S01 confirmed in chat on 2026-11-19. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, headings, IDs and statuses are English. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | Only one file exists for the artifact; no translated twin. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | No earlier accepted version; language and domain have not changed. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The terms are used correctly. S01 confirmed in chat on 2026-11-19. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Pass | Identifiers such as O, SC, S and MIL are labelled; tool names are product names. |

## Overall Verdict

Go — every Mandatory criterion of `QC-GOV-001` passes, and criteria 3, 5 and 9 of `QC-LANG-001` were confirmed by S01 in chat on 2026-11-19.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[GOV-001]: ../../sqa/governance.md
[QC-GOV-001]: ../../../framework/qc/artifacts/qc-governance.md
