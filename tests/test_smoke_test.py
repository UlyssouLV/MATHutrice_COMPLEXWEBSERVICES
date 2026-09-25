from pathlib import Path

SMOKE = Path(__file__).resolve().parents[1] / "docs" / "smoke-test.md"


def test_smoke_test_says_first_startup_provides_the_modules():
    """Reads the smoke test only. Does not start the application."""
    text = SMOKE.read_text(encoding="utf-8")
    lower = text.lower()

    assert "fresh database does not have yet" not in lower
    assert "does not have notions yet" not in lower
    assert "a first startup on an empty database provides the modules" in lower
