"""Menu du TP : lancer avec python -m tp1 depuis la racine du dépôt."""

from pathlib import Path

from tp1 import partie_a, partie_b, partie_c, partie_d
from tp1.bonus import charger_scores, demander_nom, session

DATA = Path(__file__).resolve().parent / "data"


def menu_notes() -> None:
    """Gestion des notes ; sauvegarde explicite au retour au menu."""
    fichier = DATA / "notes.txt"
    notes = partie_a.charger(fichier)
    while True:
        print("\nNotes : 1 Ajouter/modifier | 2 Afficher | 0 Sauvegarder et revenir")
        choix = input("Choix : ").strip()
        if choix == "0":
            if partie_a.sauvegarder(notes, fichier):
                return
            print("Les notes restent en mémoire. Tu peux réessayer de sauvegarder.")
        elif choix == "1":
            nom = input("Nom : ")
            note = input("Note : ")
            if not partie_a.ajouter_etudiant(notes, nom, note):
                print("Nom ou note invalide (exemple de note : 9.5).")
        elif choix == "2":
            for nom, note in sorted(notes.items()):
                print(f"{nom} : {note:g}")
            print(f"Moyenne : {partie_a.moyenne_classe(notes):.2f}")
            print("Meilleur étudiant :", partie_a.meilleur_etudiant(notes) or "Aucun étudiant")
        else:
            print("Choix invalide.")


def main() -> None:
    """Distribue les choix du menu et gère une interruption proprement."""
    try:
        DATA.mkdir(exist_ok=True)
        while True:
            print("\nTP1 - Gestion de données et mini-jeux")
            print("1 Notes | 2 Devine le nombre | 3 Mots | 4 Pendu | 5 Pendu à deux | 6 Scores | 0 Quitter")
            choix = input("Choix : ").strip()
            if choix == "0":
                break
            if choix == "1":
                menu_notes()
            elif choix == "2":
                nom = demander_nom()
                minimum, maximum = partie_b.demander_bornes()
                session(lambda: partie_b.jouer(minimum, maximum), nom, DATA / "scores.txt")
            elif choix == "3":
                mot = partie_c.choisir_mot(partie_c.charger_mots(DATA / "mots.txt"))
                print("Mot :", mot)
                print("Masque :", partie_c.masque(mot))
            elif choix in ("4", "5"):
                nom = demander_nom()

                def manche_pendu() -> bool:
                    # En mode deux joueurs, un nouveau mot est demandé à chaque manche.
                    mot = (partie_d.demander_mot() if choix == "5" else
                           partie_c.choisir_mot(partie_c.charger_mots(DATA / "mots.txt")))
                    return partie_d.jouer(mot)

                session(manche_pendu, nom, DATA / "scores.txt")
            elif choix == "6":
                scores = charger_scores(DATA / "scores.txt")
                if not scores:
                    print("Aucun score enregistré.")
                for nom, score in sorted(scores.items(), key=lambda element: (-element[1], element[0])):
                    print(f"{nom} : {score:g} victoire(s)")
            else:
                print("Choix invalide.")
    except (EOFError, KeyboardInterrupt):
        print("\nSession interrompue. Les manches terminées ont déjà été sauvegardées.")
    except OSError as erreur:
        print(f"Impossible d'accéder au dossier de données : {erreur}")


if __name__ == "__main__":
    main()
