"""Partie A : dictionnaire d'étudiants et fichiers texte UTF-8."""

import math
from pathlib import Path


def ajouter_etudiant(d: dict[str, float], nom: str, note: object) -> bool:
    """Ajoute ou remplace une note ; renvoie False si la saisie est invalide."""
    if not isinstance(nom, str):
        return False
    nom = nom.strip()
    # Ces caractères rendraient le format « nom:note » ambigu.
    if not nom or any(car in nom for car in ":\n\r"):
        return False
    try:
        valeur = float(note)
    except (TypeError, ValueError, OverflowError):
        return False
    # float accepte NaN et l'infini : on les exclut des calculs de moyenne.
    if not math.isfinite(valeur):
        return False
    d[nom] = valeur
    return True


def moyenne_classe(d: dict[str, float]) -> float:
    """Renvoie la moyenne arrondie à deux décimales, ou 0.0 si vide."""
    return round(sum(d.values()) / len(d), 2) if d else 0.0


def meilleur_etudiant(d: dict[str, float]) -> tuple[str, float] | None:
    """Renvoie (nom, note), ou None si vide ; premier inscrit en cas d'égalité."""
    return max(d.items(), key=lambda element: element[1]) if d else None


def sauvegarder(d: dict[str, float], fichier: str | Path) -> bool:
    """Écrit les données ; signale les erreurs sans faire planter l'application."""
    # Valider avant d'ouvrir évite de tronquer un fichier avec des données invalides.
    donnees: dict[str, float] = {}
    for nom, note in d.items():
        if not ajouter_etudiant(donnees, nom, note):
            print(f"Donnée invalide : {nom!r}. Sauvegarde annulée.")
            return False
    try:
        with Path(fichier).open("w", encoding="utf-8") as flux:
            for nom, note in donnees.items():
                flux.write(f"{nom}:{note}\n")
    except (OSError, UnicodeError) as erreur:
        print(f"Impossible de sauvegarder {fichier} : {erreur}")
        return False
    return True


def charger(fichier: str | Path) -> dict[str, float]:
    """Lit les lignes valides ; un fichier absent correspond à un dictionnaire vide."""
    donnees: dict[str, float] = {}
    try:
        with Path(fichier).open(encoding="utf-8") as flux:
            for numero, ligne in enumerate(flux, start=1):
                if not ligne.strip():
                    continue
                nom, separateur, note = ligne.strip().partition(":")
                if not separateur or not ajouter_etudiant(donnees, nom, note):
                    print(f"Ligne {numero} ignorée : format nom:note attendu.")
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeError) as erreur:
        print(f"Impossible de lire {fichier} : {erreur}")
    return donnees
