# Feuille de route de dev

Versions of this project run B1, B2, B3, B4. Docs are written in English.

## B1 — Make the README true

Nothing else can be followed until the instructions for running MATHutrice are right. This version is issue #22: clean up the README after branch merges.

## B2 — Seed the database

A MATHutrice that runs on an empty database shows nothing to check changes against.

## B3 — Package it

Already done upstream: one root package, and no imports that only work through the working directory or a `sys.path` patch.

## B4 — Fix the one boundary violation

The check is wired upstream. This version fixes its one violation.

## Plus tard — The boundary check runs in CI

B4's last criterion, reserved for Autonomy slot 1.
