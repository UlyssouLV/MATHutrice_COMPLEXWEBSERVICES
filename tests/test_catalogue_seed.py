"""Startup catalogue fill on a temporary database. Does not start the server."""

import uuid
from datetime import datetime
from pathlib import Path

import pytest
from sqlmodel import SQLModel, Session, create_engine, select

from mathutrice import models
from mathutrice.fonctions_python.catalogue_seed import seed_catalogue_if_empty

EXPECTED = {
    'analyse_dimensionnelle': {
        'title': 'Analyse dimensionnelle',
        'description': 'Dimensions, unités et homogénéité des formules physiques.',
        'competences': [
            ('ad01', 'Distinguer dimension et unité', 'basique'),
            ('ad02', 'Connaître les 7 grandeurs fondamentales du SI', 'basique'),
            ('ad03', 'Règles de calcul sur les dimensions', 'solide'),
            ('ad04', 'Règles de calcul sur les puissances en contexte dimensionnel', 'basique'),
            ('ad05', "Établir la dimension d'une grandeur dérivée", 'solide'),
            ('ad06', 'Convertir unité dérivée en unités de base', 'solide'),
            ('ad07', "Vérifier l'homogénéité d'une formule", 'solide'),
            ('ad08', "Déduire la dimension d'une grandeur inconnue", 'expert'),
            ('ad09', 'Identifier les paramètres pertinents en modélisation', 'expert'),
            ('ad10', "Résoudre une équation aux dimensions par identification d'exposants", 'expert'),
            ('ad11', 'Interpréter physiquement le résultat', 'expert'),
            ('ad12', 'Connaître et utiliser les constantes fondamentales', 'solide'),
        ],
    },
    'fractions_puissances_radicaux': {
        'title': 'Fractions – Puissances – Radicaux',
        'description': 'Manipulation des fractions, puissances et radicaux.',
        'competences': [
            ('fp01', 'Opérations élémentaires sur les fractions', 'basique'),
            ('fp02', 'Choisir un dénominateur commun pertinent', 'basique'),
            ('fp03', 'Simplifier une fraction numérique et littérale', 'solide'),
            ('fp04', 'Manipuler les fractions composées', 'solide'),
            ('fp05', 'Respecter les priorités opératoires', 'basique'),
            ('fp06', 'Connaître les définitions et conventions des puissances', 'basique'),
            ('fp07', 'Appliquer les règles de calcul sur les puissances', 'basique'),
            ('fp08', 'Manipuler les puissances avec exposants littéraux', 'solide'),
            ('fp09', 'Factoriser une expression contenant des puissances', 'solide'),
            ('fp10', 'Décomposer une base en facteurs premiers', 'solide'),
            ('fp11', 'Gérer les signes dans les puissances', 'solide'),
            ('fp12', 'Connaître les propriétés fondamentales de la racine carrée', 'basique'),
            ('fp13', 'Simplifier une expression contenant des racines', 'solide'),
            ('fp14', 'Rationaliser un dénominateur', 'solide'),
            ('fp15', 'Articuler racines, puissances et identités remarquables', 'expert'),
        ],
    },
    'logarithme_exponentielle': {
        'title': 'Logarithme et exponentielle',
        'description': 'Étude des fonctions logarithme et exponentielle.',
        'competences': [
            ('le01', "Définition et propriétés caractéristiques de l'exponentielle", 'basique'),
            ('le02', "Règles algébriques sur l'exponentielle", 'basique'),
            ('le03', 'Dériver une expression contenant une exponentielle', 'solide'),
            ('le04', 'Résoudre une équation avec exponentielles', 'solide'),
            ('le05', 'Résoudre une inéquation avec exponentielles', 'solide'),
            ('le06', 'Définition et propriétés caractéristiques du logarithme népérien', 'basique'),
            ('le07', 'Règles algébriques sur le logarithme népérien', 'basique'),
            ('le08', 'Dériver une expression contenant un logarithme', 'solide'),
            ('le09', "Identifier le domaine de définition d'un logarithme", 'solide'),
            ('le10', 'Résoudre une équation avec logarithmes', 'solide'),
            ('le11', 'Résoudre une inéquation avec logarithmes', 'solide'),
            ('le12', 'Utiliser les identités fondamentales entre exponentielle et logarithme', 'basique'),
            ('le13', 'Convertir entre forme exponentielle et logarithmique', 'solide'),
            ('le14', 'Manipuler la fonction exponentielle de base a', 'expert'),
            ('le15', 'Manipuler le logarithme décimal', 'solide'),
        ],
    },
    'manipulation_expressions_litterales': {
        'title': "Manipulation d'expressions littérales",
        'description': 'Isolement et manipulation de variables dans des expressions algébriques.',
        'competences': [
            ('el01', 'Distinguer expression littérale et application numérique', 'basique'),
            ('el02', 'Identifier la variable à isoler et anticiper la stratégie', 'solide'),
            ('el03', "Appliquer le principe d'équivalence des opérations", 'basique'),
            ('el04', "Suivre l'ordre inverse des priorités opératoires", 'solide'),
            ('el05', "Isoler une variable au numérateur d'une fraction", 'basique'),
            ('el06', 'Isoler une variable au dénominateur', 'solide'),
            ('el07', 'Faire passer un terme additif', 'basique'),
            ('el08', 'Faire passer un facteur multiplicatif', 'basique'),
            ('el09', "Factoriser pour simplifier lors d'un isolement", 'solide'),
            ('el10', 'Distribuer pour développer', 'basique'),
            ('el11', 'Éliminer un carré par passage à la racine', 'solide'),
            ('el12', 'Éliminer une racine par élévation au carré', 'solide'),
            ('el13', 'Éliminer une exponentielle ou un logarithme', 'solide'),
            ('el14', 'Manipuler les sommes et produits remarquables', 'solide'),
            ('el15', 'Isoler dans une expression de la forme (ax+b)/(cx+d)=k', 'solide'),
            ('el16', 'Isoler une variable apparaissant à plusieurs endroits', 'expert'),
            ('el17', 'Manipuler une fraction étagée', 'expert'),
            ('el18', 'Substituer une expression dans une autre', 'solide'),
            ('el19', 'Combiner plusieurs relations', 'expert'),
            ('el20', 'Transposer une structure par analogie', 'expert'),
            ('el21', "Gérer les conditions d'existence et de validité", 'solide'),
            ('el22', 'Vérifier la cohérence dimensionnelle ou un cas particulier', 'expert'),
            ('el23', 'Maintenir une notation rigoureuse', 'solide'),
        ],
    },
    'equations_inequations': {
        'title': 'Équations – Inéquations',
        'description': "Résolution d'équations et d'inéquations du premier et second degré.",
        'competences': [
            ('ei01', 'Comprendre le vocabulaire des équations', 'basique'),
            ('ei02', 'Tester si un nombre est solution', 'basique'),
            ('ei03', 'Traduire un problème simple en équation', 'basique'),
            ('ei04', 'Résoudre une équation du premier degré simple', 'basique'),
            ('ei05', 'Résoudre une équation du premier degré avec inconnue des deux côtés', 'basique'),
            ('ei06', 'Développer et réduire avant de résoudre', 'solide'),
            ('ei07', 'Résoudre une équation-produit', 'solide'),
            ('ei08', 'Résoudre une équation de la forme x² = a', 'solide'),
            ('ei09', 'Résoudre une équation-quotient avec valeurs interdites', 'solide'),
            ('ei10', 'Résoudre une inéquation du premier degré', 'solide'),
            ('ei11', "Représenter les solutions d'une inéquation", 'basique'),
            ('ei12', "Étudier le signe d'une expression affine", 'solide'),
            ('ei13', 'Résoudre une inéquation-produit ou quotient avec tableau de signes', 'solide'),
            ('ei14', 'Résoudre une équation du second degré avec le discriminant', 'solide'),
            ('ei15', 'Résoudre une inéquation du second degré', 'expert'),
        ],
    },
    'polynomes_factorisation': {
        'title': 'Polynômes – Factorisation',
        'description': 'Étude des polynômes, factorisation et identités remarquables.',
        'competences': [
            ('pf01', 'Reconnaître un polynôme et ses éléments', 'basique'),
            ('pf02', "Déterminer le degré d'un polynôme", 'basique'),
            ('pf03', 'Réduire et ordonner un polynôme', 'basique'),
            ('pf04', 'Développer une expression polynomiale', 'basique'),
            ('pf05', 'Utiliser les identités remarquables', 'basique'),
            ('pf06', 'Factoriser par facteur commun simple ou composé', 'solide'),
            ('pf07', 'Factoriser par regroupement', 'expert'),
            ('pf08', 'Factoriser un trinôme du second degré', 'solide'),
            ('pf09', 'Calculer le discriminant', 'basique'),
            ('pf10', "Déterminer les racines d'un trinôme", 'solide'),
            ('pf11', 'Relier racines et factorisation', 'solide'),
            ('pf12', "Vérifier qu'un nombre est racine", 'basique'),
            ('pf13', 'Factoriser un polynôme de degré 3 avec racine évidente', 'expert'),
            ('pf14', 'Utiliser les identités de degré 3', 'expert'),
            ('pf15', 'Développer avec le binôme de Newton', 'expert'),
        ],
    },
    'trigonometrie': {
        'title': 'Trigonométrie',
        'description': 'Étude des fonctions trigonométriques, des angles et du cercle trigonométrique.',
        'competences': [
            ('tr01', "Comprendre la notion d'angle en radian", 'basique'),
            ('tr02', 'Convertir degrés et radians', 'basique'),
            ('tr03', 'Connaître les valeurs remarquables de sinus et cosinus', 'basique'),
            ('tr04', 'Lire un angle sur le cercle trigonométrique', 'solide'),
            ('tr05', "Déterminer une mesure principale d'un angle", 'solide'),
            ('tr06', 'Reconnaître deux angles équivalents modulo 2π', 'solide'),
            ('tr07', 'Comprendre les fonctions sinus, cosinus et tangente', 'solide'),
            ('tr08', 'Utiliser les relations fondamentales entre sinus, cosinus et tangente', 'solide'),
            ('tr09', 'Étudier la parité de sinus, cosinus et tangente', 'solide'),
            ('tr10', 'Utiliser les angles associés', 'solide'),
            ('tr11', 'Calculer des valeurs exactes avec angles remarquables', 'solide'),
            ('tr12', 'Calculer des valeurs non immédiates par décomposition', 'solide'),
            ('tr13', "Manipuler correctement la tangente et ses conditions d'existence", 'solide'),
            ('tr14', "Connaître et appliquer les formules d'addition", 'solide'),
            ('tr15', 'Connaître et appliquer les formules de duplication', 'solide'),
            ('tr16', 'Résoudre des équations trigonométriques simples', 'solide'),
            ('tr17', 'Résoudre des équations avec angle composé', 'solide'),
            ('tr18', 'Résoudre des équations nécessitant une transformation', 'expert'),
            ('tr19', 'Résoudre des inéquations trigonométriques', 'expert'),
            ('tr20', 'Linéariser des puissances trigonométriques simples', 'expert'),
            ('tr21', 'Transformer des produits en sommes', 'expert'),
            ('tr22', 'Transformer des sommes en produits', 'expert'),
        ],
    },
}


def _session(tmp_path: Path):
    engine = create_engine(f"sqlite:///{tmp_path / 'catalogue.db'}")
    SQLModel.metadata.create_all(engine)
    return engine


DEMO_ACCOUNTS = (
    ("student.demo@epfedu.fr", "Student", "Student Demo"),
    ("teacher.demo@epf.fr", "Teacher", "Teacher Demo"),
    ("admin.demo@epf.fr", "Admin", "Admin Demo"),
)


def _rows(engine):
    with Session(engine) as session:
        notions = session.exec(select(models.Notion)).all()
        competences = session.exec(select(models.Competence)).all()
        marks = session.exec(select(models.Progression)).all()
        users = session.exec(select(models.User)).all()
    return notions, competences, marks, users


def test_empty_database_receives_the_catalogue(tmp_path):
    engine = _session(tmp_path)
    with Session(engine) as session:
        seed_catalogue_if_empty(session)

    notions, competences, marks, _users = _rows(engine)
    by_key = {notion.referentiel_key: notion for notion in notions}
    assert set(by_key) == set(EXPECTED)

    seen_ids = set()
    for key, expected in EXPECTED.items():
        notion = by_key[key]
        assert notion.title == expected["title"]
        assert notion.description == expected["description"]
        notion_uuid = uuid.UUID(str(notion.notion_id))
        assert str(notion_uuid) != key
        assert notion_uuid not in seen_ids
        seen_ids.add(notion_uuid)

        stored = sorted(
            (row.referentiel_code, row.title, row.level)
            for row in competences
            if row.notion_id == notion.notion_id
        )
        assert stored == sorted(expected["competences"])

    assert len(competences) == sum(len(item["competences"]) for item in EXPECTED.values())
    assert marks == []


def test_existing_notion_is_left_unchanged(tmp_path):
    engine = _session(tmp_path)
    kept_id = uuid.uuid4()
    with Session(engine) as session:
        session.add(
            models.Notion(
                notion_id=kept_id,
                referentiel_key="deja_la",
                title="Déjà là",
                description="Une notion déjà présente.",
            )
        )
        session.commit()
        seed_catalogue_if_empty(session, auth_mode="dev")

    notions, competences, marks, users = _rows(engine)
    assert len(notions) == 1
    assert notions[0].notion_id == kept_id
    assert notions[0].referentiel_key == "deja_la"
    assert notions[0].title == "Déjà là"
    assert competences == []
    assert marks == []
    assert users == []


def test_failure_in_the_middle_leaves_the_database_unchanged(tmp_path):
    engine = _session(tmp_path)
    with engine.begin() as conn:
        conn.exec_driver_sql(
            """
            CREATE TRIGGER fail_mid_catalogue
            AFTER INSERT ON notion
            WHEN (SELECT COUNT(*) FROM notion) > 3
            BEGIN
                SELECT RAISE(ABORT, 'mid-seed failure');
            END
            """
        )

    with Session(engine) as session:
        with pytest.raises(Exception, match="mid-seed failure"):
            seed_catalogue_if_empty(session)

    notions, competences, marks, _users = _rows(engine)
    assert notions == []
    assert competences == []
    assert marks == []

    with engine.begin() as conn:
        conn.exec_driver_sql("DROP TRIGGER fail_mid_catalogue")

    with Session(engine) as session:
        seed_catalogue_if_empty(session)

    notions, competences, _marks, _users = _rows(engine)
    assert {notion.referentiel_key for notion in notions} == set(EXPECTED)
    assert len(competences) == sum(len(item["competences"]) for item in EXPECTED.values())


def test_dev_mode_creates_the_three_demo_accounts(tmp_path):
    engine = _session(tmp_path)
    with Session(engine) as session:
        seed_catalogue_if_empty(session, auth_mode="dev")

    notions, _competences, marks, users = _rows(engine)
    assert {notion.referentiel_key for notion in notions} == set(EXPECTED)
    assert marks == []
    stored = {(user.email, user.role, user.name) for user in users}
    assert stored == set(DEMO_ACCOUNTS)


def test_entra_mode_does_not_create_demo_accounts(tmp_path):
    engine = _session(tmp_path)
    with Session(engine) as session:
        seed_catalogue_if_empty(session, auth_mode="entra")

    notions, _competences, _marks, users = _rows(engine)
    assert {notion.referentiel_key for notion in notions} == set(EXPECTED)
    assert users == []


def test_existing_email_is_left_as_it_is(tmp_path):
    engine = _session(tmp_path)
    kept_id = uuid.uuid4()
    with Session(engine) as session:
        session.add(
            models.User(
                sso_id=kept_id,
                email="student.demo@epfedu.fr",
                name="Déjà là",
                role="Teacher",
                created_at=datetime(2020, 1, 1),
            )
        )
        session.commit()
        seed_catalogue_if_empty(session, auth_mode="dev")

    _notions, _competences, marks, users = _rows(engine)
    by_email = {user.email: user for user in users}
    kept = by_email["student.demo@epfedu.fr"]
    assert kept.sso_id == kept_id
    assert kept.name == "Déjà là"
    assert kept.role == "Teacher"
    assert by_email["teacher.demo@epf.fr"].role == "Teacher"
    assert by_email["teacher.demo@epf.fr"].name == "Teacher Demo"
    assert by_email["admin.demo@epf.fr"].role == "Admin"
    assert by_email["admin.demo@epf.fr"].name == "Admin Demo"
    assert len(users) == 3
    assert marks == []
