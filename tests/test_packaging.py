"""Lock the packaging criteria. Does not start the server or call the LLM."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "mathutrice"

BARE_MODULE_IMPORT = re.compile(
    r"^\s*(?:from|import)\s+(database|main|base_generator)\b",
    re.MULTILINE,
)

SYS_PATH_MUTATION = re.compile(
    r"sys\.path\s*(?:[=+]|=)|"
    r"sys\.path\.(?:append|insert|extend|remove|pop|clear)\s*\("
)

MINIMAL_APP_ENV = {
    "SESSION_SECRET": "packaging-test-session-secret",
    "AUTH_MODE": "dev",
    "DATABASE_URL": "sqlite:///:memory:",
    "LLM_BASE_URL": "https://example.invalid/v1",
    "LLM_API_KEY": "packaging-test-key",
    "LLM_MODEL": "packaging-test-model",
}


def _python_sources() -> list[Path]:
    return sorted(path for path in PACKAGE.rglob("*.py") if path.is_file())


def _strip_hash_comments(source: str) -> str:
    """Drop `# …` comments so commented-out dead imports are ignored."""
    out: list[str] = []
    for line in source.splitlines():
        in_string = False
        quote = ""
        escaped = False
        cut = len(line)
        i = 0
        while i < len(line):
            ch = line[i]
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == quote:
                    in_string = False
            else:
                if ch in ("'", '"'):
                    in_string = True
                    quote = ch
                elif ch == "#":
                    cut = i
                    break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


def test_no_sys_path_mutation_under_mathutrice():
    offenders: list[str] = []
    for path in _python_sources():
        text = _strip_hash_comments(path.read_text(encoding="utf-8"))
        if SYS_PATH_MUTATION.search(text):
            offenders.append(str(path.relative_to(REPO)))
    assert offenders == [], f"sys.path mutation still present: {offenders}"


def test_no_bare_relative_to_nothing_imports_under_mathutrice():
    offenders: list[str] = []
    for path in _python_sources():
        text = _strip_hash_comments(path.read_text(encoding="utf-8"))
        for match in BARE_MODULE_IMPORT.finditer(text):
            offenders.append(
                f"{path.relative_to(REPO)}: {match.group(0).strip()}"
            )
    assert offenders == [], (
        "bare relative-to-nothing imports still present: " + "; ".join(offenders)
    )


def test_installer_files_declare_python_and_dependencies():
    pyproject = REPO / "pyproject.toml"
    lockfile = REPO / "uv.lock"
    python_version = REPO / ".python-version"

    assert pyproject.is_file()
    assert lockfile.is_file()
    assert python_version.is_file()

    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = data["project"]
    requires_python = project["requires-python"]
    dependencies = project["dependencies"]

    assert requires_python
    assert dependencies

    declared = python_version.read_text(encoding="utf-8").strip()
    assert declared
    major_minor = ".".join(declared.split(".")[:2])
    assert major_minor in requires_python or declared in requires_python


def test_import_mathutrice_from_outside_the_repository(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import mathutrice; print(mathutrice.__file__)",
        ],
        cwd=outside,
        env={**os.environ, "PYTHONNOUSERSITE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    package_init = Path(result.stdout.strip()).resolve()
    assert package_init == (PACKAGE / "__init__.py").resolve()


def test_import_mathutrice_app_with_minimal_environment(tmp_path):
    outside = tmp_path / "outside-app"
    outside.mkdir()
    env = {
        **os.environ,
        **MINIMAL_APP_ENV,
        "PYTHONNOUSERSITE": "1",
    }
    # Avoid picking up a developer .env from the repo when load_dotenv walks up.
    env.pop("CLIENT_ID", None)
    env.pop("CLIENT_SECRET", None)
    env.pop("TENANT_ID", None)

    script = (
        "import mathutrice.app as app_mod\n"
        "from pathlib import Path\n"
        "base = Path(app_mod.BASE_DIR)\n"
        "assert (base / 'templates').is_dir()\n"
        "assert (base / 'static').is_dir()\n"
        "assert any((base / 'templates').iterdir())\n"
        "assert any((base / 'static').iterdir())\n"
        "print('BASE_DIR=' + str(base))\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=outside,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    marker = next(
        line for line in result.stdout.splitlines() if line.startswith("BASE_DIR=")
    )
    resolved = Path(marker.removeprefix("BASE_DIR=")).resolve()
    assert resolved == PACKAGE.resolve()


def test_templates_and_static_match_app_resolution():
    """Same path formula as mathutrice.app (BASE_DIR next to the module)."""
    app_file = PACKAGE / "app.py"
    base_dir = Path(os.path.dirname(os.path.abspath(app_file)))

    templates = base_dir / "templates"
    static = base_dir / "static"
    assert templates.is_dir()
    assert static.is_dir()
    assert any(templates.iterdir())
    assert any(static.iterdir())
