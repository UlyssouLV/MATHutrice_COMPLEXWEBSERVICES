# Feuille de route de dev

Versions of this project run B1, B2, B3, B4. Docs are written in English.

## B1 — Make the README true

Delivered. A newcomer can run MATHutrice from the root README: one description, how to start locally, the connexion de développement as shipped, and a link to the smoke test. Parent issue #3.

## B2 — Seed the database

A MATHutrice that runs on an empty database shows nothing to check changes against.

## B3 — Package it

Already done upstream: one root package, and no imports that only work through the working directory or a `sys.path` patch.

## B4 — Fix the one boundary violation

The check is wired upstream. This version fixes its one violation.

## Plus tard — The boundary check runs in CI

B4's last criterion, reserved for Autonomy slot 1.
