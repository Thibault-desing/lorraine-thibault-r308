"""Partie B : deviner un nombre en dix propositions valides au maximum."""

import random


def jouer(minimum: int = 1, maximum: int = 100) -> bool:
    """Joue une manche et renvoie True en cas de victoire."""
    if minimum > maximum:
        raise ValueError("La borne minimale doit être inférieure ou égale à la maximale.")
    secret = random.randint(minimum, maximum)
    print(f"Devine le nombre entre {minimum} et {maximum} : 10 essais.")
    essais = 0
    while essais < 10:
        try:
            proposition = int(input(f"Essai {essais + 1}/10 : "))
        except ValueError:
            print("Entre un nombre entier.")
            continue
        # Une erreur de saisie ne consomme pas une tentative.
        if not minimum <= proposition <= maximum:
            print(f"Entre un nombre de {minimum} à {maximum}.")
            continue
        essais += 1
        if proposition == secret:
            print("Gagné !")
            return True
        print("Trop petit" if proposition < secret else "Trop grand")
    print(f"Perdu, le nombre était {secret}.")
    return False


def demander_bornes() -> tuple[int, int]:
    """Permet de garder les bornes par défaut en appuyant sur Entrée."""
    while True:
        try:
            minimum = int(input("Minimum [1] : ").strip() or "1")
            maximum = int(input("Maximum [100] : ").strip() or "100")
        except ValueError:
            print("Les bornes doivent être des entiers.")
            continue
        if minimum <= maximum:
            return minimum, maximum
        print("Le minimum ne doit pas dépasser le maximum.")
