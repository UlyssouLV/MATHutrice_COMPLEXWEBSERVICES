from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def test_readme_has_no_conflict_markers_and_links_the_smoke_test():
    text = README.read_text(encoding="utf-8")
    for marker in CONFLICT_MARKERS:
        assert marker not in text
    assert "docs/smoke-test.md" in text
