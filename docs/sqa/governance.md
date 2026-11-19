# Governance / ARB Workflow

## Metadata
| Key | Value |
| --- | --- |
| ID | GOV-001 |
| CrossReference | [BC-001], [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | [8163226] |

---

## Purpose

Defines how this project applies Quality Criteria (QC) checklists to real artifact instances, producing SQA Review Records and Go/No-Go decisions. It supports the Business Case objective O3 (proof by tests and checks) and the concern CN-002 of S01 that every step is planned, reviewed and traceable.

## ARB Review Workflow

1. **Submission** — S01, as owner, submits an instance for review and names the checklist of its type (`framework/qc/*/qc-*.md`).
2. **QC Checklist Review** — the Responsible reviewer applies the checklist criterion by criterion.
3. **Review Record** — the reviewer documents the outcome as an SQA Review Record (`RC-*` under `docs/sqa/reviews/`).
4. **Go/No-Go Decision** — the Accountable role for the artifact category (S01) decides; contested or cross-cutting cases escalate to the ARB Chair (S01).
5. **Sign-off** — S01, as the Accountable role, sets the status. On **Go**, the artifact's `## Version History` gets an `Accepted` row (the previous row becomes `Deprecated`). On **Go-with-conditions**, the status stays `Proposed` until the action items are closed. On **No-Go**, the status stays `Proposed` and the artifact returns to its owner for rework, or becomes `Rejected` when S01 refuses the change for good.
6. **Traceability Update** — S01 updates the Traceability Matrix ([TM-001]) with the instance and its `RC-*` reference.

## RACI by Artifact Category

| Artifact Category | Responsible (runs the review) | Accountable (Go/No-Go owner) | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Strategic (Stakeholder Analysis, Business Case) | S01 | S01 | S02 | S03 |
| Process/Business (Project Plan, Milestones/Gateways) | S01 | S01 | S02 | S03 |
| Governance and traceability (Governance, Traceability Matrix) | S01 | S01 | S02 | S03 |
| Design decisions (Architecture Decision Record) | S01 | S01 | S02 | S03 |
| Source code (Python source and tests) | S01 | S01 | S02 | S03 |
| Documentation (README, wiki) | S01 | S01 | S02 | S03 |

Cross-cutting escalations and disputed verdicts are Accountable to the ARB Chair (S01), overriding the category-level Accountable role.

## Escalation Rules

- A **No-Go** verdict, or any disagreement between the Responsible reviewer and the category's Accountable owner, escalates to the ARB Chair (S01).
- A reviewer may not review an instance they authored. The one exception is autonomous mode: the author may act as stand-in for a reviewer or an Accountable role, recorded as `Stand-in for <S-ID>` and `Mode: autonomous, not independent`; the Product Owner's acceptance of the plan in chat is the authorisation for it. A criterion that only a person can confirm stays Pending until S01 confirms it in chat; the confirmation is recorded in the review record.
- Repeated No-Go verdicts (2 or more) on the same artifact type trigger a review of the corresponding `QC-*` checklist itself.
- A blocking finding gives No-Go. A risk exception for it needs an approver who is neither the author nor the owner; as the project has one decision-maker, no risk exception is available, and a blocking finding is always fixed.

## Cadence

- Reviews are triggered per artifact instance as it is produced or revised, at the latest at the Go/No-Go decision date of its gateway in [PP-001].
- QC checklists belong to the framework and are reviewed there.
- The process relied on is the review checklist process of the framework ([PRC-001]); the Traceability Matrix is [TM-001].

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[TM-001]: ./traceability-matrix.md
[PRC-001]: ../../framework/process/review-checklist-process.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
