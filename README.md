# R3.08 — Lorraine Thibault

Monorepo des travaux pratiques de R3.08, BUT Réseaux et Télécommunications.
Le TP1 contient la gestion de notes et les mini-jeux en console, avec les bonus.

## Démarrer

Prérequis : **Python 3.10 ou plus**. Aucune bibliothèque externe à installer.
Depuis la racine de ce dépôt :

```console
python -m tp1
```

Sous Windows, `py -m tp1` convient également si Python est installé via le lanceur.
Le menu permet de gérer les notes, deviner un nombre, manipuler les mots, jouer
au Pendu seul ou à deux et consulter le classement.

## Organisation

```text
tp1/
  __main__.py       Menu interactif
  partie_a.py       Dictionnaire de notes et fichiers texte
  partie_b.py       Devine le nombre, dix essais maximum
  partie_c.py       Chargement des mots et masque
  partie_d.py       Pendu, sept erreurs maximum
  bonus.py          Rejouabilité et scores persistants
  data/mots.txt     Liste de mots modifiable
tests/             Tests automatisés de toutes les parties
tp2/               Emplacement réservé au prochain TP
tp3/               Emplacement réservé au prochain TP
```

## Fonctionnement et choix

| Partie | Comportement |
| --- | --- |
| A | Ajout et modification d'une note, moyenne arrondie, meilleur étudiant, lecture/écriture UTF-8. |
| B | Secret aléatoire, indices « Trop petit » et « Trop grand », dix propositions valides maximum, bornes personnalisables. |
| C | Mot choisi en majuscules et masque sous forme de liste de `_`. Liste intégrée utilisée si le fichier est inutilisable. |
| D | Révélation de toutes les occurrences, affichage des lettres proposées, dessin ASCII, victoire ou défaite à la septième erreur. |
| Bonus | Rejouer après chaque manche, classement partagé, mode à deux avec saisie du mot masquée. |

- Un dictionnaire vide donne une moyenne de `0.0` et aucun meilleur étudiant (`None`).
- Une note doit être un nombre fini ; aucune plage de notation n'est imposée par l'énoncé.
- Les lignes mal formées sont signalées et ignorées. Un fichier absent donne un dictionnaire vide.
- Une saisie invalide ne consomme pas de tentative. Au Pendu, une lettre répétée ne consomme pas d'erreur.
- Les accents sont conservés : `É` et `E` sont distincts. Les minuscules et les accents Unicode décomposés sont normalisés.
- Les notes et scores sont stockés dans `tp1/data/notes.txt` et `tp1/data/scores.txt`, au format `nom:valeur`, et exclus de Git.
- Une victoire vaut un point, une défaite zéro. Les scores sont relus au début de chaque session et écrits après chaque manche. Deux victoires d'Ana donnent `Ana:2.0`.
- En mode deux joueurs, le nom demandé est celui du joueur qui devine. L'autre choisit un nouveau mot à chaque manche.
- Utiliser un vrai terminal pour masquer le mot secret : certains environnements de développement ne prennent pas en charge la saisie cachée.
- `Ctrl+C` ou une fin d'entrée quitte proprement. Les manches terminées restent sauvegardées si l'écriture a réussi ; les notes non sauvegardées sont perdues.

## Vérifier

```console
python -m unittest discover -s tests -v -b
```

Les tests couvrent les exemples Alice/Bob/Claire, les fichiers absents ou invalides,
les erreurs d'écriture, le dixième essai, les sept lettres fausses, les répétitions,
`PYTHON`, `ÉLÉPHANT`, la persistance des scores et le menu complet.

## Historique

Les parties sont séparées en commits `TP1 partie A`, `TP1 partie B`,
`TP1 partie C` et `TP1 partie D`. Les bonus et la documentation ont leurs propres commits.
Les dossiers TP2 et TP3 sont uniquement réservés : leurs énoncés ne sont pas inclus dans ce travail.
