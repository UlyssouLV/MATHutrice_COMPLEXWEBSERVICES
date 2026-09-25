"""Copy the in-code catalogue into an empty database, in one transaction."""

import uuid

from sqlmodel import Session, select

from mathutrice import models
from mathutrice.fonctions_python.referentiel import REFERENTIEL


def seed_catalogue_if_empty(session: Session) -> None:
    """Insert the seven notions and every competence when no notion exists.

    Catalogue scores are not written as marks. A failure rolls the transaction
    back so the database stays empty and a later startup can try again.
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
        session.commit()
    except Exception:
        session.rollback()
        raise
