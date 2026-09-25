# B4 — Fix the one boundary violation

Spec issue: UlyssouLV/MATHutrice_COMPLEXWEBSERVICES#14. Recreated from EPF-MDE/MATHutrice#32. Follows EPF-MDE/MATHutrice#32. Does not replace it.

## Problem Statement

The package-boundary tooling is already wired on `course-2026`: `tach check` passes, and `scripts/check_cycles.py` reads the real import graph. One violation remains red on purpose until this version:

`mathutrice.fonctions_python` ↔ `mathutrice.lacune_evaluation`

`LLM_as_Evaluator` still imports `REFERENTIEL` from `mathutrice.fonctions_python.main`, and `main` still imports `LLM_as_Evaluator` (today behind a function-local import that only hides the cycle from humans, not from the checker). `REFERENTIEL` already lives in `mathutrice/fonctions_python/referentiel.py`, but that file is still inside `fonctions_python`, so fixing the evaluator's import alone would leave a package-level cycle as long as `main` depends on `lacune_evaluation`.

Until `check_cycles` is green, contributors cannot trust the check as a gate, and later work on package interfaces starts from a graph that is still broken in one place.

## Solution

Break that single package cycle by moving the shared catalogue value to a **loose** module at the root package level — `mathutrice/referentiel.py` — which both sides may depend on without forming a package↔package cycle. Point `lacune_evaluation` at that module. Keep `REFERENTIEL` re-exported from `main` so existing callers (`app`, `session_generator`, …) need not change. Hoist the now-unjustified function-local import of `LLM_as_Evaluator` in `main` to module level. Lock the green cycle check with an automated test.

No behaviour change, no new public interface beyond the module move, no CI, no rewrite of `app.py`'s lazy imports, no plant-and-revert demo.

## User Stories

1. As a contributor, I want `uv run python scripts/check_cycles.py` to exit cleanly, so that the import graph has no package-level cycle.
2. As a contributor, I want `REFERENTIEL` to live in `mathutrice.referentiel` (loose under the root package), so that both `fonctions_python` and `lacune_evaluation` can depend on it without a package cycle.
3. As a contributor, I want `lacune_evaluation` to import `REFERENTIEL` from `mathutrice.referentiel`, so that it no longer reaches into `fonctions_python.main`.
4. As a contributor, I want `main` to keep re-exporting `REFERENTIEL`, so that existing `from mathutrice.fonctions_python.main import REFERENTIEL` call sites keep working.
5. As a contributor, I want imports that still pointed at `mathutrice.fonctions_python.referentiel` updated to the new path, so that the old module path is gone after the move.
6. As a contributor, I want the `LLM_as_Evaluator` import in `main` at module level once the cycle is gone, so that the real dependency is visible and the "local import for cycle" comment disappears.
7. As a maintainer, I want the file move committed as a rename, so that `git log --follow` still finds `referentiel.py`.
8. As a maintainer, I want an automated test that fails if a package-level import cycle returns, so that the green `check_cycles` result stays locked.
9. As a maintainer, I want application behaviour unchanged, so that this version is a graph fix, not a rewrite.
10. As a maintainer, I want the root README and `mathutrice/README.md` left as they are, so that this version does not reopen documentation.
11. As a maintainer, I want `tach check` left alone (already green), so that this version does not widen the lock beyond the cycle criterion.

## Implementation Decisions

- **Move `referentiel.py` to `mathutrice/referentiel.py`.** Loose modules at the root package level are outside the package tier that `check_cycles` collapses; both packages may depend on them without forming a package↔package cycle.
- **`lacune_evaluation` imports `from mathutrice.referentiel import REFERENTIEL`.** That is the edge that must leave `fonctions_python`.
- **`main` re-exports `REFERENTIEL`.** Call sites that already import it from `main` stay; only the move path and the cycle edge change.
- **Update in-package imports** of `mathutrice.fonctions_python.referentiel` (e.g. `main`, `catalogue_seed`) to `mathutrice.referentiel`.
- **Hoist** the function-local `LLM_as_Evaluator` import in `main` to module level and drop the cycle comment.
- **File move as git rename**, separate in spirit from import rewrites where practical.
- **Behaviour unchanged.** No function renamed, no signature altered, no new interface required of callers beyond the relocated module.
- **Docs unchanged.** Root README and `mathutrice/README.md` already describe the checks.

## Testing Decisions

One seam. Do not start the server, open a browser, or call the LLM endpoint.

- **Seam — no package-level import cycle.** An automated test under `tests/` fails if `scripts/check_cycles.py` would fail (same criterion the script enforces). `tach check` is not part of this lock.

Prior art: packaging lock in `tests/test_packaging.py`; document checks in `tests/test_readme.py`.

## Out of Scope

- **CI.** Running the boundary check in CI is the later roadmap entry (« Plus tard — The boundary check runs in CI »).
- **Rewriting function-local imports in `app.py`.** Design work; belongs with broader architecture (#29 / later), not this fix.
- **Planting a deliberate violation then reverting it.** Not required on this fork.
- **Locking `tach check` in tests.** Already green; not this version's criterion.
- **Introducing package `__init__` public surfaces / deep-module interfaces.** Constraint already documented; designing those surfaces is separate.
- **Any change to behaviour, signatures, configuration, or defaults.**
- **Rewriting the README or `mathutrice/README.md`.**

## Further Notes

- This version is the dev-roadmap entry B4. It follows « Make the package structure explicit and enforced » (#32) and does not replace it.
- The check (`tach`, `check_cycles`) is already wired upstream on `course-2026`; B4 fixes the one remaining cycle and locks that result.
- Course work targets `course-2026` (ADR-0001).
