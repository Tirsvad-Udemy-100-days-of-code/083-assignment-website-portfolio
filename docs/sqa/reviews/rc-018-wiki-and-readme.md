# SQA Review Record: Wiki and README of MIL-004

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-018 |
| CrossReference | [QC-WIKI-001], [MIL-004] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go for the repository content; criterion 14 is Pending the host | pending |

---

## Artifact Under Review

- Instance reviewed: the wiki in `docs/wiki/` (ten pages in three languages, the sidebar and the footer) and `README.md`
- Checklist used: [QC-WIKI-001]; the README was also checked with `framework/scripts/check-readme.sh`, which passes
- Scope: full review
- Language and domain: en (authoritative), da and ms (translations)
- Language reviewer: none yet; the Danish and Bahasa Malaysia texts were not read by a native reader, so the language check of those pages stays Pending, as task 4 and 5 of [MIL-004] say
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | The wiki has a `_Sidebar.md`, because the host lists subpages only through it | Pass | `docs/wiki/_Sidebar.md` exists. |
| 2 | The sidebar starts with the wiki's title in bold, then one list of the pages in the primary language (English), `Home` first | Pass | The sidebar starts with `**Portfolio Website**`, then one list of the ten English pages, `Home` first. |
| 3 | The page list holds a link to every English page of the wiki, and no link points to a page that does not exist | Pass | A script check found a sidebar link for all ten English pages and no link to a missing page, in every page of every language. |
| 4 | A `**Related**` section follows the page list only when the wiki has related wikis (for example the checklists wiki for a framework wiki); each entry is a link to that wiki's Home. A wiki with nothing related has no such section | Pass | The wiki has no related wiki, so the sidebar has no `Related` section. |
| 5 | A `**Languages**` section is the last section of the sidebar. It has one line per language, the language written in that language, linking to that language's `Home` page | Pass | `**Languages**` is the last section: `English: [Home](Home)`, `Dansk: [Hjem](Home-da)`, `Bahasa Malaysia: [Laman Utama](Home-ms)`. |
| 6 | The sidebar does not repeat the page list per language | Pass | The page list appears once. |
| 7 | A sidebar produced by a generator carries a comment that says so and names the generator; the generator is changed, not the page | Pass | The sidebar is written by hand, not generated, so no generator comment applies. |
| 8 | The wiki has a `Languages` line on each page (criterion 11), so the sidebar is not the only way to switch language | Pass | Every page starts with the language line. |
| 9 | Every wiki exists in English and, as a minimum, in the language the project's registry names as the PO language; further languages are added on top, never instead of English | Pass | English, Danish and Bahasa Malaysia exist; the registry lists `en, da and ms`. |
| 10 | Every English page has a page in each other language of the wiki: the page sets are identical | Pass | Ten English pages, ten Danish and ten Bahasa Malaysia pages; a script check found no page missing. |
| 11 | Every page starts with the language line, with the current language in bold and a link to the same page in each other language | Pass | Every page starts with the language line with the current language in bold and links to the same page in the other languages. |
| 12 | A page in a language other than English is named `<Page>-<code>.md`, with a BCP 47 code; English has no suffix | Pass | Translations are named `<Page>-da.md` and `<Page>-ms.md`; English has no suffix. |
| 13 | Code blocks, commands, file names and IDs stay in English in every language | Pass | Code blocks, commands, file names and IDs are the same in the three languages. |
| 14 | The sidebar, every page and every link were checked on the published wiki after the change, not only in the repository | Pending | Can only be checked on the host after the merge (MIL-004 criterion 9); it is repeated there and this record is updated. |
| 15 | A change to the layout rules (sections, order, naming) is made in the generator or template and in this checklist's source rules together | Pass | Not applicable: no generator or template changed; the sidebar rules were followed as written. |
| 16 | The wiki folder (`docs/wiki/`) is flat: every page, `Home.md` and `_Sidebar.md` included, is directly in it, and languages are told apart by file name, never by a subfolder | Pass | All 32 files are directly in `docs/wiki/`, no subfolder. |

## Other Checks

- Every step page has its screenshot, taken from this project's own output by `docs/tools/capture_screenshots.py` in Docker; the README shows the same images (MIL-004 criterion 4).
- The wiki links to the images of the `main` branch, so the pictures show once the branch is merged.
- The lecture summary is written in the author's own words; no lecture text, picture or video is in the repository (criterion 5).
- A search of the tracked files finds no name of the drafting tools (criterion 7).

## Overall Verdict

Go for the repository content: every Mandatory criterion of `QC-WIKI-001` that can be checked in the repository passes. Criterion 14 is Pending until the published wiki is checked after the merge; the Danish and Bahasa Malaysia language checks stay Pending for a native reader.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| Check the sidebar, every page and every link on the published wiki, then update this record | S01 | after the merge of MIL-004 |
| Have a native reader confirm the Danish and Bahasa Malaysia pages | S01 | when a reader is available |

---

[QC-WIKI-001]: ../../../framework/qc/artifacts/qc-wiki.md
[MIL-004]: ../../milestones/mil-004-documentation-and-wrap-up.md
