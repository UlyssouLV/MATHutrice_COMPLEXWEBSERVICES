# MATHutrice

LLM-based tutor that helps EPF first-year students practise mathematical tools through notions, competences and training. Every LLM call goes through an **LLM endpoint**: the OpenAI-compatible API set by `LLM_BASE_URL`, `LLM_API_KEY` and `LLM_MODEL`.

## Run locally

These steps start the application from a clone. To check that the clone actually runs, follow the [smoke test](docs/smoke-test.md).

### Python

The project requires Python `>=3.14,<3.15`. The version pinned for local runs is **3.14.7** (`.python-version`).

### Install dependencies

[uv](https://docs.astral.sh/uv/) installs that Python and the dependency versions in `uv.lock`:

```sh
uv sync
. .venv/bin/activate
```

Without uv, create a virtual environment on Python 3.14.7 and run `pip install -e .` (from `pyproject.toml`, not the lockfile).

### Environment variables

```sh
cp .env.example .env
```

The application reads the variables listed in `.env.example`:

| Variable | Role |
| --- | --- |
| `AUTH_MODE` | Which sign-in is active |
| `DEV_LOGIN_KEY` | Optional shared key for dev sign-in |
| `SESSION_SECRET` | Signs session cookies |
| `DATABASE_URL` | Database URL (SQLite locally) |
| `LLM_BASE_URL` | LLM endpoint base URL |
| `LLM_MODEL` | Model served by that endpoint |
| `LLM_API_KEY` | Key for that endpoint (required to start) |
| `CLIENT_ID` | Entra application id |
| `CLIENT_SECRET` | Entra client secret |
| `TENANT_ID` | Entra tenant |
| `REDIRECT_URL` | Entra redirect after sign-in |
| `POST_LOGOUT_REDIRECT_URL` | Entra redirect after sign-out |

Set `LLM_API_KEY` to the key for your LLM endpoint. Leave the other values as in `.env.example` unless you are changing that endpoint or the database.

### Start

From the repository root, with the virtual environment active:

```sh
uvicorn mathutrice.app:app --port 8000
```

The application listens on <http://localhost:8000/>.
