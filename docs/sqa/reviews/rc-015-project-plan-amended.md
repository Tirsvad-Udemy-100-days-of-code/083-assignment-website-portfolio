# SQA Review Record: PP-001

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-015 |
| CrossReference | [PP-001], [QC-PP-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Added the LinkedIn link, the profile photo and the project flip cards to the scope coverage and the MIL-004 deliverable; added OI-003<br>Verdict Go (RC-015) | [ec90c2b] |

---

## Artifact Under Review

- Instance reviewed: [PP-001]
- Checklist used: [QC-PP-001] and `QC-LANG-001`
- Scope: full review after the amendment of 2026-11-19 (LinkedIn link, profile photo and project flip cards requested by S01)
- Language and domain: en / it
- Language reviewer: none; S01 reads English and knows the IT domain and confirmed criteria 3, 5 and 9 of `QC-LANG-001` in chat on 2026-11-19
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The plan states its start date, end date and the constraint it must fit | Pass | Start 2026-11-19 and end 2026-11-23 are unchanged. |
| 2 | Every milestone or gateway is listed once with its document, decision date and owner | Pass | Four gateways, each with document, decision date and owner. |
| 3 | Every decision date lies inside the plan's window and is consistent with the dates in the linked `MIL-*` document | Pass | Decision dates still equal the Target Dates of the milestones. |
| 4 | Every in-scope item of the Business Case is delivered at a named gateway (scope coverage) | Pass | Scope Coverage has new rows for the LinkedIn link and photo (O7) and the flip cards (O8), delivered at MIL-004. |
| 5 | Dependencies between gateways are stated, acyclic and consistent with the schedule order | Pass | The chain MIL-001 to MIL-004 is unchanged and acyclic. |
| 6 | The plan states what happens to later gateways and to the end date when a gateway is No-Go | Pass | The No-Go rule is unchanged. |
| 7 | Owners, reviewers and escalation roles use Stakeholder Analysis IDs and match the governance RACI | Pass | Owner S01; no role names. |
| 8 | Planning assumptions are listed with their source, and a changed baseline is recorded with its reason | Pass | Assumptions A1 to A6 are unchanged and have sources. |
| 9 | Plan risks are listed with impact and a mitigation, and trace to Business Case risks where they come from there | Pass | Plan Risks are unchanged; the photo risk is an open issue with an owner and a fallback, OI-003. |
| 10 | Open issues are listed, and none contradicts a statement elsewhere in the plan | Pass | OI-001, OI-002 and OI-003 are current; none contradicts the plan. |
| 11 | Each gateway's main deliverable is stated and matches the deliverable of its `MIL-*` document | Pass | The MIL-004 deliverable in the plan now equals the one in [MIL-004]. |
| 12 | Gateways that deliver user stories name them, and those that do not say why | Pass | The Stories column is unchanged. |
| 13 | The schedule view (table, Gantt) and the dependency view agree with each other | Pass | The Gantt dates are unchanged and agree with the table. |
| 14 | Each gateway is linked to its issue-tracker milestone, or marked as not yet synced | Pass | Every Milestone cell says "not yet synced" in the plan text; the host milestones exist and are linked from the host. |
| 15 | The plan is a singleton: one Project Plan per project, changes recorded in Version History | Pass | One plan; Version History has two rows. |

## Language and Domain Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The Metadata table has a `Language` row and a `Domain` row, and neither is a placeholder | Pass | `Language en`, `Domain it` in the Metadata table. |
| 2 | `Language` is a BCP 47 code and `Domain` is a value from the registry's domain list | Pass | `en` is BCP 47; `it` is in the registry's domain list. |
| 3 | The content (prose and table cells) is written in the stated language | Pass | The content is English throughout. S01 confirmed the wording and terms of these documents in chat on 2026-11-19; the amendment of the same day uses the same terms and S01 may challenge it in the end-of-run summary. |
| 4 | The register matches the one the registry gives for the artifact type | Pass | Register is IT Executive English; the text matches it. |
| 5 | Domain terms are the PO terms of the domain's dictionary, with no synonyms | Pass | No domain dictionary exists (out of scope in [BC-001]); terms are used consistently. S01 confirmed the wording and terms of these documents in chat on 2026-11-19; the amendment of the same day uses the same terms and S01 may challenge it in the end-of-run summary. |
| 6 | Metadata keys, section headings, IDs and statuses are in English | Pass | Metadata keys, headings, IDs and statuses are English. |
| 7 | No translated twin (`<name>.<language>.md`) exists beside the document | Pass | Only one file exists for the artifact; no translated twin. |
| 8 | A change of language or domain since the previous accepted version has a Version History row and was reviewed again | Pass | No earlier accepted version; language and domain have not changed. |
| 9 | A reviewer competent in the domain, and in the language, has confirmed that the domain terms are used correctly | Pass | The terms are used correctly. S01 confirmed the wording and terms of these documents in chat on 2026-11-19; the amendment of the same day uses the same terms and S01 may challenge it in the end-of-run summary. |
| 10 | Abbreviations are spelled out on first use, in the stated language | Pass | Identifiers such as O, SC, S and MIL are labelled; tool names are product names. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PP-001` passes, and criteria 3, 5 and 9 of `QC-LANG-001` were confirmed by S01 in chat on 2026-11-19.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[PP-001]: ../../project-plan.md
[QC-PP-001]: ../../../framework/qc/artifacts/qc-project-plan.md
[ec90c2b]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/ec90c2bed831675a94f868e0bc74743b2aed547b
