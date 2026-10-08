"""Partie C : chargement, normalisation Unicode et masquage des mots."""

import random
import unicodedata
from pathlib import Path

MOTS_PAR_DEFAUT = ["PYTHON", "RÉSEAU", "ÉLÉPHANT", "ORDINATEUR", "CLAVIER"]


def normaliser_mot(mot: str) -> str:
    """Conserve les accents et unifie les différentes écritures Unicode."""
    return unicodedata.normalize("NFC", mot.strip()).upper()


def charger_mots(fichier: str | Path | None = None) -> list[str]:
    """Charge un mot alphabétique par ligne, avec repli sur une liste intégrée."""
    if fichier is None:
        return MOTS_PAR_DEFAUT.copy()
    try:
        lignes = Path(fichier).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as erreur:
        print(f"Liste de mots intégrée utilisée : {erreur}")
        return MOTS_PAR_DEFAUT.copy()
    mots = [normaliser_mot(ligne) for ligne in lignes]
    mots = [mot for mot in mots if mot.isalpha()]
    return mots or MOTS_PAR_DEFAUT.copy()


def choisir_mot(liste: list[str]) -> str:
    """Choisit un mot en majuscules ; accepte aussi une liste vide."""
    mots = [normaliser_mot(mot) for mot in liste if isinstance(mot, str)]
    mots = [mot for mot in mots if mot.isalpha()]
    return random.choice(mots or MOTS_PAR_DEFAUT)


def masque(mot: str) -> list[str]:
    """Crée une case par caractère du mot fourni."""
    return ["_"] * len(mot)
