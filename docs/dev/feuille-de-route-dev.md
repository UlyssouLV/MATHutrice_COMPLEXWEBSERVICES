# Feuille de route de dev

Versions of this project run B1, B2, B3, B4. Docs are written in English.

## B1 — Make the README true

Delivered. A newcomer can run MATHutrice from the root README: one description, how to start locally, the connexion de développement as shipped, and a link to the smoke test. Parent issue #3.

## B2 — Seed the database

Delivered. A first startup on an empty database provides the catalogue modules and, when `AUTH_MODE=dev`, the three demo accounts. The smoke test matches that first startup. Parent issue #6.

## B3 — Package it

Delivered. One importable `mathutrice` root package; imports no longer depend on the working directory or a `sys.path` patch; automated tests lock those packaging criteria. Parent issue #11.

## B4 — Fix the one boundary violation

The check is wired upstream. This version fixes its one violation.

## Plus tard — The boundary check runs in CI

B4's last criterion, reserved for Autonomy slot 1.
