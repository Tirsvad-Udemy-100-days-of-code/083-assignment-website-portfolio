# Stakeholder Analysis: Website Portfolio

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | [8163226] |

---

## Purpose

This analysis names the people who have an interest in the Website Portfolio project, classifies each by power and interest, and records what each of them needs from the result. It gives every other project document the stakeholder IDs it uses for owners and reviewers. The method is the Power/Interest grid: a stakeholder with high power and high interest is managed closely, a stakeholder with low power and high interest is kept informed, and a stakeholder with low power and low interest is monitored. Concerns are written in business language and mapped to a FURPS+ attribute.

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen | Course participant: Product Owner, developer and reviewer | Self (Udemy course participant) | HIGH | HIGH | Manage Closely | A finished, reviewed portfolio project that shows planning, structure, tests and documentation. |
| S02 | Udemy course participants | Fellow learners who share code and compare solutions | Udemy course community | LOW | HIGH | Keep Informed | Readable, runnable code that uses the assignment's function names, and README instructions to run it. |
| S03 | GitHub viewers | Visitors who browse the repository for ideas | Public (GitHub and git host visitors) | LOW | LOW | Monitor | A clear repository description, topics and README, and no runtime dependencies to install. |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** S01 decides scope, writes the code and reviews every artifact, so power is high. The result is a portfolio entry for job interviews, so interest is high. S01 is the Product Owner, the developer and the reviewer; a stand-in review in autonomous mode is recorded as not independent.
- **Keep Informed (S02):** Course participants cannot change the project, so power is low. They are the audience for whom the code is written and they compare solutions with it, so interest is high. They are informed through the README and the wiki.
- **Monitor (S03):** Repository viewers cannot change the project and look at it briefly, so power and interest are low. Their first impression comes from the repository description, topics and README, which the project keeps clear without further engagement.
- **Keep Satisfied:** no stakeholder falls in this quadrant.

## Primary Concerns and FURPS+ Mapping

| Concern ID | Stakeholder | Concern | FURPS+ attribute |
| --- | --- | --- | --- |
| CN-001 | S01 | The result is a complete, working portfolio site for the Day 83 assignment, built from a list of projects. | Functionality |
| CN-002 | S01 | Every step is planned, reviewed and traceable, and every change reaches `main` through a pull request per milestone. | Supportability |
| CN-003 | S01 | The code is proven by automated tests and a local static-analysis scan before every push. | Reliability |
| CN-004 | S02 | The code is readable, one concern per module, and uses the assignment's function names `home`, `about` and `load_from_json`. | Supportability |
| CN-005 | S02 | The README and the wiki show how to create a `.venv`, upgrade pip, run the site and run the tests, on Windows and Linux. | Usability |
| CN-006 | S02 | Each build step is explained, with what it teaches and a screenshot, in English, Danish and Bahasa Malaysia. | Usability |
| CN-007 | S03 | The repository has a description, topics and a README that explain the project at a glance. | Usability |
| CN-008 | S03 | Nothing has to be installed to run the project beyond Python. | Implementation constraint (no runtime dependencies) |
| CN-009 | S02 | The lecture is summarised, not copied: no lecture screenshot, text or video is published. | Legal constraint |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| CM-001 | Chat with S01 | Once per run, then at the end | Plan for acceptance; end-of-run summary with every stand-in decision | Plan acceptance, MIL-004 |
| CM-002 | Pull request on the git host | One per milestone | Changes, review records and closed issues | MIL-001 to MIL-004 |
| CM-003 | README and wiki (English, Danish, Bahasa Malaysia) | Updated at each milestone that changes behaviour | How to set up, run and test; what each step teaches | MIL-004 |
| CM-004 | Repository description and topics | Once | Description and at least five topics | MIL-001 |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S02 expects the idea's Flask application, while S03 and the Business Case require no runtime dependencies. | S02, S03 | Build the site with the standard library, keep the idea's function names and data file, and record the decision in ADR-0001. |
| S01 wants the course lecture reflected in the documents, while CN-009 forbids copying it. | S01, S02 | Summarise the lecture in the wiki in the author's own words; take every screenshot from this project's own output. |
| S01 acts as author and reviewer in autonomous mode. | S01 | The review record states the stand-in and says `Mode: autonomous, not independent`; S01 challenges any decision in the end-of-run summary. |

## Traceability Analysis

### Stakeholder to Actor Mapping

No use cases are modelled ([BC-001] Out of Scope), so no actor mapping exists. Every stakeholder uses the project through the repository, the README and the wiki.

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | CN-001 | O1, O2 |
| S01 | CN-002 | O3, O6 |
| S01 | CN-003 | O3, O6 |
| S02 | CN-004 | O1, O3 |
| S02 | CN-005 | O4 |
| S02 | CN-006 | O5 |
| S02 | CN-009 | O5 |
| S03 | CN-007 | O6 |
| S03 | CN-008 | O1, O4 |

## Sign-Off

| Stakeholder | Decision | Date |
| --- | --- | --- |
| S01 | Go, by stand-in review RC-002 | 2026-11-19 |

---

[BC-001]: ./business-case.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
