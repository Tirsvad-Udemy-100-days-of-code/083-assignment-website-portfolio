# Traceability Matrix

## Metadata
| Key | Value |
| --- | --- |
| ID | TM-001 |
| CrossReference | [BC-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Added RC-012 for the MIL-003 source | [53db60c] |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Added RC-013 to RC-016 for the amended BC, SA, PP and MIL-004 | [ec90c2b] |

---

## Purpose

Tracks backward/forward links between artifact instances so that the Business Case's
cross-artifact traceability success criterion is measurable. A row is added or
updated whenever an artifact instance is created or reviewed.

## Traceability Table

| Artifact Instance | Type | Language | Domain | Upstream (Backward Link) | Downstream (Forward Link) | Last Reviewed (RC-ID) |
| --- | --- | --- | --- | --- | --- | --- |
| [BC-001] | BC | en | it | - | [SA-001], [PP-001], [ADR-0001] | RC-013 |
| [SA-001] | SA | en | it | [BC-001] | [PP-001], [GOV-001] | RC-014 |
| [PP-001] | PP | en | it | [BC-001], [SA-001] | [MIL-001], [MIL-002], [MIL-003], [MIL-004] | RC-015 |
| [MIL-001] | MIL | en | it | [PP-001] | [MIL-002] | RC-004 |
| [MIL-002] | MIL | en | it | [MIL-001] | [MIL-003] | RC-005 |
| [MIL-003] | MIL | en | it | [MIL-002] | [MIL-004] | RC-006 |
| [MIL-004] | MIL | en | it | [MIL-003] | - | RC-016 |
| [ADR-0001] | ADR | - | - | [BC-001], [SA-001] | - | RC-008 |
| [GOV-001] | GOV | en | it | [BC-001], [SA-001] | - | RC-009 |
| Python source (`src/`, `tests/`) | PY | - | - | [MIL-001], [MIL-002], [MIL-003] | - | RC-010, RC-011, RC-012 |

## Concern Coverage

| Concern (CN-ID) | Views that answer it | Decisions (ADR) | Quality check (TP) | Status |
| --- | --- | --- | --- | --- |
| CN-001 | [MIL-002], [MIL-003] | [ADR-0001] | - | Covered |
| CN-002 | [PP-001], [GOV-001] | - | - | Covered |
| CN-003 | [MIL-001], [MIL-002], [MIL-003] | - | - | Covered |
| CN-004 | [MIL-002], [MIL-003] | [ADR-0001] | - | Covered |
| CN-005 | [MIL-004] | - | - | Covered |
| CN-006 | [MIL-004] | - | - | Covered |
| CN-007 | [MIL-001], [MIL-004] | - | - | Covered |
| CN-008 | [MIL-001] | [ADR-0001] | - | Covered |
| CN-009 | [MIL-004] | - | - | Covered |

## Open Inconsistencies

| # | Views | Inconsistency | Found in (RC-ID) | Status | Resolved in |
| --- | --- | --- | --- | --- | --- |
| - | - | None | - | Closed | - |

## Coverage Notes

No test plan, use case or design artifact exists: the product is too small to justify them ([BC-001] Out of Scope). In Upstream, `-` means foundational; in Downstream, `-` means nothing is built on it yet; in Last Reviewed, `-` means no `RC-*` exists yet. The matrix has no checklist, so it is accepted by S01 as the plan was accepted.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[MIL-001]: ../milestones/mil-001-project-setup.md
[MIL-002]: ../milestones/mil-002-core-domain-and-use-cases.md
[MIL-003]: ../milestones/mil-003-site-generation-and-preview.md
[MIL-004]: ../milestones/mil-004-documentation-and-wrap-up.md
[ADR-0001]: ../adr/adr-0001-standard-library-site-generator.md
[GOV-001]: ./governance.md
[6367a3b]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/6367a3b727ed74d5ac4bf9fb8c4ffe15b92cfb85
[53db60c]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/53db60c1a016b07abf9b27b093f0501591ae69c5
[ec90c2b]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/ec90c2bed831675a94f868e0bc74743b2aed547b
