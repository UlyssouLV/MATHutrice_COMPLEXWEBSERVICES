from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def test_readme_has_no_conflict_markers_and_links_the_smoke_test():
    text = README.read_text(encoding="utf-8")
    for marker in CONFLICT_MARKERS:
        assert marker not in text
    assert "docs/smoke-test.md" in text


def test_readme_documents_the_connexion_de_developpement():
    """Reads the README only. Does not start the application."""
    text = README.read_text(encoding="utf-8")
    lower = text.lower()

    assert "connexion de développement" in lower

    default_at = lower.find("default")
    assert default_at != -1
    assert "entra" in lower[default_at : default_at + 80]
    assert "auth_mode" in lower
    assert "`dev`" in text

    assert "dev_login_key" in lower
    assert "redirect_url" in lower
    assert "post_logout_redirect_url" in lower
    redirect_at = lower.find("redirect_url")
    redirect_window = lower[max(0, redirect_at - 120) : redirect_at + 280]
    assert "entra" in redirect_window

    forge_at = lower.find("forge")
    assert forge_at != -1
    caveat = lower[max(0, forge_at - 160) : forge_at + 160]
    assert "session cookie" in caveat
    assert "placeholder" in caveat
    assert "session_secret" in caveat
    assert "dev_login_key" in caveat

    assert "curl" in lower
    assert "/dev/login" in lower
    assert "-c " in text
    assert "-b " in text

    checklist_at = lower.find("checklist")
    assert checklist_at != -1
    checklist = lower[checklist_at : checklist_at + 400]
    assert "auth_mode" in checklist
    assert "unset" in checklist
    assert "entra" in checklist
