# B3 — Package it

Spec issue: UlyssouLV/MATHutrice_COMPLEXWEBSERVICES#11. Recreated from EPF-MDE/MATHutrice#28. Follows EPF-MDE/MATHutrice#28. Does not replace it.

## Problem Statement

MATHutrice cannot be installed. It can only be *run from the right directory*.

All of the code sits under `generator_test/`, which is used as a source root rather than as a package: `app.py` does `import models` and `from database import engine`, and the documented way to start the app is `cd generator_test && uvicorn app:app`. From anywhere else, the imports do not resolve.

Where that stops working, the code patches `sys.path` at runtime — in `fonctions_python/seed.py`, `fonctions_python/session_generator.py`, `fonctions_python/main.py` and `lacune_evaluation/LLM_as_Evaluator.py`. Two import styles now coexist as a result: most modules say `from fonctions_python.x import …`, while `session_generator.py` and `LLM_as_Evaluator.py` say `from base_generator import …`, `from type_questions.x import …` and `from main import REFERENTIEL`, which resolve *only because* of those patches.

The consequences a contributor meets:

- **Nothing can import the app except the app.** No test suite, no script and no tool can load the code without reproducing the same path tricks. This is why MATHutrice has no tests.
- **Dependencies are unpinned by any standard.** `requirements.txt` lists sixteen pinned packages, but there is no `pyproject.toml`, no lockfile, and nothing declares the Python version to an installer — `.python-version` states 3.14.7 and no tooling enforces it.
- **The import graph cannot be inspected.** Analysis and architecture tools need a single importable root package; they refuse to run against a source directory whose imports depend on runtime path mutation.
- **The order of imports is load-bearing.** `app.py` performs many imports inside functions rather than at module level, which is a workaround for cycles between the application module and the generator modules. Those cycles are invisible until something moves.

## Solution

Make MATHutrice an ordinary installable Python project: one importable root package named `mathutrice`, a `pyproject.toml` that declares its dependencies and its Python version, and absolute imports throughout. After this change, `pip install -e .` followed by `uvicorn mathutrice.app:app` works from the repository root, and every `sys.path` patch is gone.

This is packaging only. No module's interface changes, no behaviour changes, and nothing is restructured beyond what is needed for the code to be importable under a single root.

On `course-2026` that packaging is already present (upstream). This version locks the criteria with automated tests; it does not repeat the file move.

## User Stories

1. As a contributor, I want to install the project with a single standard command, so that I do not have to discover which directory to run from.
2. As a contributor, I want `uvicorn mathutrice.app:app` to start the application from the repository root, so that the start command does not depend on my current directory.
3. As a contributor, I want every import in the codebase to be absolute and rooted at `mathutrice`, so that I can tell where a name comes from by reading the import.
4. As a contributor, I want no module to mutate `sys.path` at runtime, so that imports behave the same however the code was loaded.
5. As a contributor, I want the project's dependencies declared in `pyproject.toml`, so that an installer can resolve them without me reading a separate file.
6. As a contributor, I want a committed lockfile, so that two of us installing on different days get the same versions.
7. As a contributor, I want the required Python version declared to the installer, so that I find out about a mismatch before the application fails at runtime.
8. As a contributor, I want to open a Python REPL anywhere and `import mathutrice.app`, so that I can inspect the application without starting a server.
9. As a contributor, I want to write a test that imports the application, so that automated tests become possible at all.
10. As a contributor, I want the templates and static assets to be found wherever the package is installed from, so that an installed copy renders pages exactly as a source checkout does.
11. As a contributor, I want the database module importable on its own, so that a script or a migration can use it without loading the whole application.
12. As a contributor, I want the seeding script runnable as a module of the package, so that it does not need to patch its own path to find its siblings.
13. As a contributor, I want the evaluation code to import its dependencies by name, so that it stops appending directories to `sys.path` to reach them.
14. As a contributor, I want the imports that currently sit inside functions moved to module level wherever the cycle they avoided no longer exists, so that the real dependencies are visible.
15. As a contributor, I want any remaining cycle to be visible rather than worked around silently, so that it can be recorded and fixed deliberately.
16. As a maintainer, I want an architecture tool to be able to load the package, so that import boundaries can be enforced by a check later.
17. As a maintainer, I want the application's behaviour to be unchanged by this work, so that I can review it as a move, not as a rewrite.
18. As a maintainer, I want the smoke test to pass from the repository root after the change, so that I have one procedure that proves the application still runs.
19. As a maintainer, I want the documented start command updated in the README and the smoke test, so that the instructions match the code.
20. As a maintainer, I want file moves committed as renames, so that `git log --follow` still finds each file's history.
21. As a maintainer, I want the dead example modules left alone, so that this change stays reviewable and their removal is decided separately.
22. As a contributor deploying the application, I want the start command to work inside a container without a working-directory trick, so that deployment configuration stays simple.
23. As a contributor, I want the scheduled cleanup job to keep running as it does today, so that packaging does not quietly change runtime behaviour.
24. As a contributor, I want the dev sign-in and the Entra sign-in to behave exactly as they do today, so that packaging changes nothing about who can sign in.

## Implementation Decisions

- **One root package, named `mathutrice`.** The existing source directory becomes that package. The name matches the project, and it is the name an architecture tool will be configured against.
- **Sub-packages keep their current names and contents.** The generator modules, the question-type modules and the evaluation module stay where they are relative to each other. This work moves the root, not the internals.
- **Every import becomes absolute**, rooted at `mathutrice`. The two competing styles are unified on that one form.
- **Every `sys.path` mutation is deleted**, not replaced. If a module cannot reach what it needs after the move, its import is wrong and is fixed at the import.
- **Function-local imports are hoisted to module level where the cycle they avoided no longer exists.** Where a genuine cycle remains, it stays local and is recorded in the pull request so it can be tracked separately. Breaking cycles is not part of this work.
- **`pyproject.toml` declares the project, its dependencies and its Python version.** Dependencies come from the pinned list already in the repository; nothing is upgraded, added or removed as part of this change. `uv` is the dependency manager, and its lockfile is committed.
- **Templates and static assets are declared as package data**, so an installed copy finds them. They are already resolved relative to the module that loads them, so no code change is needed for this.
- **The application entry point becomes `mathutrice.app:app`.** The README, the smoke test and any deployment instructions are updated to match.
- **Behaviour is unchanged.** No module gains or loses a public name, no function changes signature, no configuration variable is renamed, and no default changes. A reviewer should be able to read the diff as renames plus import rewrites.
- **The dead example modules and the unused LLM SDK stay.** Removing them is separate work and is already tracked.
- **On this fork, do not re-do the packaging move.** Lock the criteria with tests. Leave the README and smoke test as they are (already describe `uvicorn mathutrice.app:app`).

## Testing Decisions

Two seams. Do not start the server, open a browser, or call the LLM endpoint.

- **Seam 1 — static packaging proofs.** Under `mathutrice/`, no `sys.path` mutation and no relative-to-nothing import (`from database import …`, `from main import …`, `from base_generator import …`). `pyproject.toml`, the committed lockfile, and `.python-version` are present; dependencies and the required Python version are declared to the installer.
- **Seam 2 — importability.** `import mathutrice` succeeds from a working directory outside the repository. `import mathutrice.app` succeeds with a minimal environment (settings required at import). Templates and static assets are reachable from the installed package path (same resolution the app uses).

Prior art: document checks in `tests/test_readme.py` / `tests/test_smoke_test.py`; importable package use in `tests/test_catalogue_seed.py`.

## Out of Scope

- **Breaking import cycles.** Any cycle that survives is recorded, not fixed.
- **Reducing the size of the application module.** It stays as it is.
- **CI.** Wiring packaging or boundary checks into CI is separate (later roadmap).
- **Removing dead modules or the unused LLM SDK.** Tracked separately.
- **Any change to interfaces, behaviour, configuration or defaults.**
- **Deployment configuration and Dockerfile.** US 22 is the start command without a cwd trick, not a container image. Deployment config stays out of scope.
- **Rewriting the README or smoke test.** Already updated; leave them.
- **Package-boundary check (`tach`) and fixing its violations.** That is B4.

## Further Notes

- This version is the dev-roadmap entry B3. It follows « Package the project… » (#28) and does not replace it.
- Packaging already landed upstream on `course-2026`; B3 adds the automated lock.
- Course work targets `course-2026` (ADR-0001).
