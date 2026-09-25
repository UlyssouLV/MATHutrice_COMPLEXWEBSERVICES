"""Copy the in-code catalogue into an empty database, in one transaction."""

import uuid
from datetime import datetime

from sqlmodel import Session, select

from mathutrice import models
from mathutrice.fonctions_python.referentiel import REFERENTIEL

DEMO_ACCOUNTS = (
    ("student.demo@epfedu.fr", "Student"),
    ("teacher.demo@epf.fr", "Teacher"),
    ("admin.demo@epf.fr", "Admin"),
)


def name_from_email(email: str) -> str:
    """Same derivation as the connexion de développement."""
    local_part = email.split("@")[0]
    return local_part.replace(".", " ").replace("_", " ").title()


def seed_catalogue_if_empty(session: Session, auth_mode: str = "entra") -> None:
    """Insert the seven notions and every competence when no notion exists.

    When auth_mode is dev, also create the three demo accounts if that email
    is absent. Catalogue scores are not written as marks. A failure rolls the
    transaction back so the database stays empty and a later startup can try again.
    """
    existing = session.exec(select(models.Notion)).first()
    if existing is not None:
        return

    try:
        for key, data in REFERENTIEL.items():
            notion_id = uuid.uuid4()
            session.add(
                models.Notion(
                    notion_id=notion_id,
                    referentiel_key=key,
                    title=data["notion_nom"],
                    description=data["description"],
                )
            )
            for competence in data["competences"]:
                session.add(
                    models.Competence(
                        competence_id=uuid.uuid4(),
                        referentiel_code=competence["code"],
                        title=competence["nom"],
                        level=competence["niveau"],
                        notion_id=notion_id,
                    )
                )
        if auth_mode == "dev":
            now = datetime.utcnow()
            for email, role in DEMO_ACCOUNTS:
                already = session.exec(
                    select(models.User).where(models.User.email == email)
                ).first()
                if already is not None:
                    continue
                session.add(
                    models.User(
                        sso_id=uuid.uuid4(),
                        email=email,
                        name=name_from_email(email),
                        role=role,
                        created_at=now,
                    )
                )
        session.commit()
    except Exception:
        session.rollback()
        raise
