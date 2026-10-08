"""Bonus : rejouabilité et classement persistant commun aux deux jeux."""

from collections.abc import Callable
from pathlib import Path

from tp1.partie_a import ajouter_etudiant, charger, sauvegarder


def charger_scores(fichier: str | Path) -> dict[str, float]:
    """Ne conserve que les compteurs de victoires entiers et positifs ou nuls."""
    return {nom: score for nom, score in charger(fichier).items()
            if score >= 0 and score.is_integer()}


def demander_nom() -> str:
    """Réutilise la validation du format de fichier de la partie A."""
    while True:
        nom = input("Nom du joueur : ").strip()
        if ajouter_etudiant({}, nom, 0):
            return nom
        print("Entre un nom non vide et sans deux-points.")


def rejouer() -> bool:
    """Redemande une réponse tant qu'elle ne vaut ni o ni n."""
    while True:
        reponse = input("Rejouer ? (o/n) : ").strip().lower()
        if reponse in ("o", "n"):
            return reponse == "o"
        print("Réponds par o ou n.")


def session(jeu: Callable[[], bool], nom: str, fichier: str | Path) -> None:
    """Recharge les scores au lancement et les sauvegarde après chaque manche."""
    scores = charger_scores(fichier)
    scores.setdefault(nom, 0.0)
    while True:
        if jeu():
            scores[nom] += 1.0
        # Écrire avant de demander de rejouer conserve la dernière victoire
        # même si le joueur ferme ensuite le programme avec Ctrl+C.
        if not sauvegarder(scores, fichier):
            print("Attention : le score de cette session n'a pas pu être enregistré.")
        print(f"{nom} : {scores[nom]:g} victoire(s).")
        if not rejouer():
            break
