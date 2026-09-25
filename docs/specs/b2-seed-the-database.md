# B2 — Seed the database

Spec issue: EPF-MDE/MATHutrice#56. Follows #20. Does not replace it.

## Problem Statement

A maintainer who starts MATHutrice on an empty database sees an empty module list and, on the connexion de développement, three roles with no user to click. There is nothing representative to check a change against. An unused seed path writes a notion key into the UUID column and never copies competences, so training cannot find a notion by its key or a competence by its code.

## Solution

On startup, when the database has no notion, copy the in-code catalogue: the seven notions (key, title, description, a new UUID) and every competence (code, title, level, linked to its notion). Descriptions are the sentences already written for those seven notions. Catalogue scores are not copied.

When `AUTH_MODE=dev`, also create three accounts if the email is not already there: `student.demo@epfedu.fr` (Student), `teacher.demo@epf.fr` (Teacher), `admin.demo@epf.fr` (Admin). The displayed name is derived from the address. When `AUTH_MODE=entra`, copy the catalogue only.

If any notion already exists, change nothing. The copy is one transaction: a failure in the middle leaves the database as it was, so the next startup can try again.

Marks stay as they are today: score 0.50, level moyen, zero attempts, created when someone signs in, once the competences exist.

The smoke test no longer says a fresh database has no notions yet. It says a first startup on an empty database provides the modules. The README is left as it is.

## User Stories

1. As a maintainer, I want an empty database to receive the seven notions at startup, so that the home page lists modules I can check a change against.
2. As a maintainer, I want each notion stored under its catalogue key, so that training can find « Trigonométrie » as `trigonometrie`.
3. As a maintainer, I want each notion to get a new UUID, so that the key is not stored in the identifier column.
4. As a maintainer, I want each notion's description to be the sentence already written for that notion, so that the module page has a description.
5. As a maintainer, I want every competence of those notions copied with its code, title, and level, so that training can look the competence up.
6. As a maintainer, I want catalogue scores left out of the database, so that a 1.0 or 0.0 from the catalogue is not a student's mark.
7. As a maintainer using the connexion de développement, I want `student.demo@epfedu.fr` created as a Student, so that I can open the app as a student in one click.
8. As a maintainer using the connexion de développement, I want `teacher.demo@epf.fr` created as a Teacher, so that I can open the teacher area in one click.
9. As a maintainer using the connexion de développement, I want `admin.demo@epf.fr` created as an Admin, so that I can open the app as an admin in one click.
10. As a maintainer, I want each demo account's name derived from the address, so that the connexion de développement shows « Student Demo », « Teacher Demo », and « Admin Demo ».
11. As a maintainer starting with `AUTH_MODE=entra`, I want no demo accounts, so that a school database does not contain those addresses.
12. As a maintainer whose database already contains a notion, I want startup to leave notions, competences, and users untouched, so that a populated database is not filled again.
13. As a maintainer, I want the copy to commit in one transaction, so that a failure cannot leave a single notion that would block the next startup.
14. As a maintainer, I want an email that already exists to be skipped, so that startup does not fail on a duplicate address when the catalogue is otherwise empty.
15. As a student signing in after the catalogue is present, I want my marks created at sign-in with score 0.50, so that marks still appear the way they do today.
16. As a reader of the smoke test, I want the sentence about a fresh database having no notions yet replaced, so that the check matches a first startup.
17. As a reader of the smoke test, I want it to say that a first startup on an empty database provides the modules, so that I know modules are there without a separate seed step.
18. As a reader of the README, I want it unchanged, so that this version does not reopen the README.

## Implementation Decisions

- The fill runs at startup, after the tables exist. It is the only path. The unused path that writes a notion key into the UUID column is not the mechanism.
- Empty means there is no notion row. One existing notion means do nothing: no missing notion, no missing competence, no demo account.
- Copy the seven notions from the in-code catalogue. `referentiel_key` is the catalogue key. `notion_id` is a new UUID. The description is the sentence already written for that same notion.
- Copy every competence of those notions. `referentiel_code` is the catalogue code. Title and level come from the catalogue. The competence is linked to its notion. Do not copy the catalogue score.
- Demo accounts are created only when `AUTH_MODE=dev`, and only when that email is absent: `student.demo@epfedu.fr` / Student, `teacher.demo@epf.fr` / Teacher, `admin.demo@epf.fr` / Admin. The name is derived from the address the same way the connexion de développement already derives it.
- Notions, competences, and any missing demo accounts commit in one transaction.
- The smoke test sentence that says a fresh database does not have notions yet is rewritten. The README is not rewritten.
- Docs for this version are in English.

## Testing Decisions

- Two seams. Do not start the server, open a browser, or call the LLM endpoint.
- Seam 1: call the startup fill on a temporary database. A good test checks external rows, not the copy mechanism. Empty database and `AUTH_MODE=dev`: the seven notion keys, the competence codes, and the three demo addresses. The same empty database and `AUTH_MODE=entra`: the catalogue, and none of those three addresses. A database that already has a notion: no added notion, competence, or user. Catalogue scores are not stored as marks.
- Seam 2: read the smoke test the way the README test reads the README. The old « fresh database does not have yet » sentence is gone, and a first startup on an empty database is described as providing the modules.
- There is no existing test that talks to the database. The fill test is the prior art for later database checks. The document check follows the README test.

## Out of Scope

- Exercises, conversations, and pre-written marks.
- Changing how the connexion de développement signs someone in.
- The README.
- The package-boundary check and running it in CI.
- Replacing issue #20.

## Further Notes

- This version is the dev-roadmap entry B2. It follows « Seed a usable database when it's empty » (#20) and does not replace it.
- The connexion de développement does not depend on these accounts: the sign-in form still creates a user when you type an address.
- Course work targets `course-2026` (ADR-0001).
