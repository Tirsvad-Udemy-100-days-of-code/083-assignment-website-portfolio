# SQA Review Record: SA-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-020 |
| CrossReference | [SA-001], [QC-SA-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Added concern CN-012 (SQLite storage and a dynamic site) and updated the communication milestones, at the request of S01<br>Verdict Go (RC-020) | [1406a53] |

---

## Artifact Under Review

- Instance reviewed: [SA-001]
- Checklist used: [QC-SA-001] and `QC-LANG-001`
- Scope: full review after the scope change of S01 (SQLite storage and a dynamic site, ADR-0002)
- Language and domain: en / it
- Language reviewer: none; S01 reads English and knows the IT domain and confirmed criteria 3, 5 and 9 of `QC-LANG-001` in chat on 2026-11-19
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Power/Interest grid is filled for every stakeholder, with no gaps or unclassified entries | Pass | S01, S02 and S03 are classified; no gap. |
| 2 | Each stakeholder is assigned a unique, stable ID (e.g. S01-S11 style) reusable for RACI assignments in other artifacts | Pass | IDs are unchanged and stable. |
| 3 | Roles and organizational context are defined with explicit Power and Interest levels, not just narrative description | Pass | Roles, organisations and levels are explicit. |
| 4 | Communication needs (channel, frequency, deliverable type) are mapped to project phases or milestones | Pass | Communication Requirements CM-001 to CM-003 now name MIL-006 as the last milestone. |
| 5 | Conflicting stakeholder interests are identified with documented mitigation or resolution strategies | Pass | The three conflicts keep their mitigations; S03's no-dependency concern is still met by the standard library `sqlite3`. |
| 6 | Stakeholder concerns are explicitly traced to Business Case objectives | Pass | The new concern CN-012 maps to objectives O9 and O10 in the Business Goal Alignment table. |
| 7 | Primary concerns are expressed in both business language and a recognized quality-attribute mapping (e.g. FURPS+) | Pass | CN-012 has the FURPS+ attribute Functionality. |
| 8 | Document is understandable and navigable by non-technical stakeholders reviewing their own entry | Pass | Plain language, short rows. |
| 9 | Every concern has a stable ID (`CN-NNN`) in the concern register, with the stakeholder who raised it; IDs are never renumbered or reused | Pass | CN-012 is added with the next free ID; CN-001 to CN-011 are not renumbered. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | `Language en`, `Domain it` in the Metadata table. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is BCP 47; `it` is in the registry's domain list. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | The content is English throughout. S01 confirmed the wording and terms of these documents in chat on 2026-11-19 and accepted the plan for the SQLite and dynamic-site change in chat; S01 may challenge the stand-in review in the end-of-run summary. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | Register is IT Professional English; the text matches it. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | No domain dictionary exists (out of scope in [BC-001]); terms are used consistently. S01 confirmed the wording and terms of these documents in chat on 2026-11-19 and accepted the plan for the SQLite and dynamic-site change in chat; S01 may challenge the stand-in review in the end-of-run summary. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, headings, IDs and statuses are English. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | Only one file exists for the artifact; no translated twin. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | No earlier accepted version; language and domain have not changed. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The terms are used correctly. S01 confirmed the wording and terms of these documents in chat on 2026-11-19 and accepted the plan for the SQLite and dynamic-site change in chat; S01 may challenge the stand-in review in the end-of-run summary. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Pass | Identifiers such as O, SC, S and MIL are labelled; tool names are product names. |

## Overall Verdict

Go — every Mandatory criterion of `QC-SA-001` passes, and criteria 3, 5 and 9 of `QC-LANG-001` were confirmed by S01 in chat on 2026-11-19.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[SA-001]: ../../stakeholder-analysis.md
[QC-SA-001]: ../../../framework/qc/artifacts/qc-stakeholder-analysis.md
[1406a53]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/1406a53bbc208284c38c07a83b3d264ffdea7b00
