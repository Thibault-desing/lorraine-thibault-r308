"""Partie D : Pendu à sept erreurs, avec dessin et mode deux joueurs."""

from getpass import getpass

from tp1.partie_c import charger_mots, choisir_mot, masque, normaliser_mot


def dessin(erreurs: int) -> str:
    """Ajoute une partie du pendu à chaque erreur (sept étapes)."""
    tete = "O" if erreurs >= 1 else " "
    corps = "|" if erreurs >= 2 else " "
    gauche = "/" if erreurs >= 3 else " "
    droite = "\\" if erreurs >= 4 else " "
    jambe_gauche = "/" if erreurs >= 5 else " "
    jambe_droite = "\\" if erreurs >= 6 else " "
    sol = "---" if erreurs >= 7 else "   "
    return f" +---+\n |   {tete}\n |  {gauche}{corps}{droite}\n |  {jambe_gauche} {jambe_droite}\n |  {sol}\n=+====="


def demander_mot() -> str:
    """Le premier joueur saisit le mot sans l'afficher dans un vrai terminal."""
    while True:
        mot = normaliser_mot(getpass("Joueur 1, mot secret (saisie masquée) : "))
        if mot.isalpha():
            return mot
        print("Entre un mot contenant uniquement des lettres, accents autorisés.")


def jouer(mot: str | None = None) -> bool:
    """Joue une manche ; sept lettres fausses provoquent la défaite."""
    mot = choisir_mot(charger_mots()) if mot is None else normaliser_mot(mot)
    if not mot.isalpha():
        raise ValueError("Le mot doit être non vide et alphabétique.")
    mot_masque = masque(mot)
    proposees: set[str] = set()
    erreurs = 0
    while erreurs < 7 and "_" in mot_masque:
        print(dessin(erreurs))
        print("Mot :", " ".join(mot_masque))
        print(f"Erreurs : {erreurs}/7 | Lettres proposées : {' '.join(sorted(proposees)) or '-'}")
        lettre = normaliser_mot(input("Une lettre : "))
        if len(lettre) != 1 or not lettre.isalpha():
            print("Entre une seule lettre.")
            continue
        if lettre in proposees:
            print("Lettre déjà proposée : aucune erreur supplémentaire.")
            continue
        proposees.add(lettre)
        if lettre in mot:
            # Révéler toutes les occurrences, pas seulement la première.
            for position, caractere in enumerate(mot):
                if caractere == lettre:
                    mot_masque[position] = lettre
        else:
            erreurs += 1
    print(dessin(erreurs))
    print("Mot :", " ".join(mot_masque))
    print(f"Erreurs : {erreurs}/7 | Lettres proposées : {' '.join(sorted(proposees))}")
    victoire = "_" not in mot_masque
    print(f"Gagné ! Le mot était {mot}." if victoire else f"Perdu, le mot était {mot}.")
    return victoire
