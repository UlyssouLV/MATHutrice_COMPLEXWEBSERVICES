# B1 — Make the README true

Spec issue: EPF-MDE/MATHutrice#53. Follows #22. Does not replace it.

## Problem Statement

A newcomer who clones MATHutrice on `course-2026` cannot tell what it is or how to run it. The root README is the unresolved merge of several feature-branch READMEs: it still contains merge-conflict markers and mixes descriptions of different branches (home page mockup, front-end branch).

## Solution

One coherent root README that describes MATHutrice in the vocabulary of the glossary, explains how to run it locally, documents the **connexion de développement** as shipped, and points to the smoke test as the check that a clone runs — without restating that check's commands.

A person who has never seen the project can run it from a fresh clone of `course-2026` by following the README alone.

## User Stories

1. As a newcomer, I want the README to contain no merge-conflict markers, so that I can read it as one document.
2. As a newcomer, I want one description of MATHutrice, so that I am not reading several branch write-ups at once.
3. As a newcomer, I want that description to use the glossary terms (**connexion de développement**, **LLM endpoint**), so that I do not confuse the dev sign-in with impersonation.
4. As a newcomer, I want the README to state the Python version the project requires, so that I install an interpreter that can run it.
5. As a newcomer, I want the README to explain how to install dependencies, so that a fresh clone has what it needs to start.
6. As a newcomer, I want the README to list the environment variables the application reads, so that I can fill in a local environment file.
7. As a newcomer, I want the README to say how to start the application with `uvicorn`, so that I can open it locally.
8. As a newcomer, I want `AUTH_MODE` documented (`entra` by default, `dev` for the **connexion de développement**), so that I know which sign-in I am using.
9. As a newcomer, I want `DEV_LOGIN_KEY` documented, so that I know when the dev sign-in page asks for a shared key.
10. As a newcomer, I want `REDIRECT_URL` and `POST_LOGOUT_REDIRECT_URL` documented, so that I know they belong to Entra sign-in and not to the **connexion de développement**.
11. As a newcomer, I want the `SESSION_SECRET` caveat, so that I know a placeholder value lets anyone forge a session cookie and skip `DEV_LOGIN_KEY`.
12. As a newcomer, I want a `curl` example of scripted sign-in (`POST /dev/login`) that keeps the session cookie between requests, so that I can call the app without a browser.
13. As someone deploying MATHutrice, I want the deployment checklist to say `AUTH_MODE` unset or `entra`, so that the **connexion de développement** never reaches production.
14. As a newcomer, I want a link to the smoke test, so that I know how to check that a clone runs.
15. As a newcomer, I want that link to stand in for the smoke test's steps, so that the README does not restate the browser check or the chat `curl`.
16. As a reviewer, I want the dev sign-in section to match the behaviour already shipped for `AUTH_MODE=dev`, so that the README is not ahead of or behind the application.

## Implementation Decisions

- The only document this version rewrites is the root README. The package-boundary document is left as it is.
- Remove every merge-conflict marker and keep a single description of MATHutrice.
- The running instructions cover the Python version, installing dependencies, environment variables, and starting with `uvicorn`.
- The **connexion de développement** section matches the shipped behaviour: `AUTH_MODE` (`entra` by default, `dev`), `DEV_LOGIN_KEY`, `REDIRECT_URL`, `POST_LOGOUT_REDIRECT_URL`, the `SESSION_SECRET` caveat, a `curl` example of `POST /dev/login` that keeps the session cookie, and a deployment checklist line that `AUTH_MODE` is unset or `entra`.
- The README links to the smoke test as the check that a clone runs and does not copy that document's commands (browser steps, chat completion request).
- Docs for this version are in English. The agent skills pack is not rewritten.
- Vocabulary follows the glossary: **connexion de développement** is not impersonation; the **LLM endpoint** is the OpenAI-compatible API, not "Mistral" as a synonym for every endpoint.

## Testing Decisions

- One seam: the root README, read as a document. Do not start the application in the test.
- A good test checks external content, not wording style: no merge-conflict markers, a link to the smoke test, and the shipped **connexion de développement** facts (`AUTH_MODE`, `DEV_LOGIN_KEY`, the `SESSION_SECRET` caveat, `POST /dev/login`).
- The criterion "a newcomer can run it from the README alone" stays the manual smoke test, not a second automated seam.
- There is no existing README test in the suite. The new test is the prior art for later document checks.

## Out of Scope

- Seeding the database.
- The package-boundary document and its check.
- Running the boundary check in CI.
- Changing the **connexion de développement** behaviour.
- Rewriting the agent skills pack.
- Restating the smoke test's verification steps in the README.

## Further Notes

- This version is the dev-roadmap entry B1 and follows the already-open issue "Clean up the README after branch merges" (#22). It does not replace that issue.
- The dev sign-in issue (#18) is closed; the README documents that behaviour rather than waiting for it.
- Course work targets `course-2026` (ADR-0001), which is the branch whose README still contains the conflict markers.
