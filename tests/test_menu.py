import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tp1.__main__ import main
from tp1.partie_a import charger


class MenuTests(unittest.TestCase):
    def test_notes_et_jeu_avec_scores(self):
        # Parcours utilisateur complet, avec sauvegarde dans un dossier isolé.
        entrees = ["1", "1", "Alice", "12", "1", "Bob", "15", "1", "Claire", "9.5",
                   "2", "0", "2", "Ana", "1", "1", "1", "n", "6", "0"]
        sortie = io.StringIO()
        with tempfile.TemporaryDirectory() as dossier, patch("tp1.__main__.DATA", Path(dossier)), \
                patch("builtins.input", side_effect=entrees), redirect_stdout(sortie):
            main()
            self.assertEqual(charger(Path(dossier) / "scores.txt"), {"Ana": 1.0})
            self.assertEqual(charger(Path(dossier) / "notes.txt"), {"Alice": 12.0, "Bob": 15.0, "Claire": 9.5})
        self.assertIn("Moyenne : 12.17", sortie.getvalue())

    def test_tournoi_et_rejouabilite(self):
        entrees = ["5", "Ana"] + list("python") + ["o"] + list("éléphant") + ["n", "0"]
        # Le second É est déjà proposé : il est accepté sans pénalité.
        with tempfile.TemporaryDirectory() as dossier, patch("tp1.__main__.DATA", Path(dossier)), \
                patch("builtins.input", side_effect=entrees), \
                patch("tp1.partie_d.getpass", side_effect=["Python", "ÉLÉPHANT"]):
            main()
            self.assertEqual(charger(Path(dossier) / "scores.txt"), {"Ana": 2.0})

    def test_interruption_propre(self):
        with tempfile.TemporaryDirectory() as dossier, patch("tp1.__main__.DATA", Path(dossier)), \
                patch("builtins.input", side_effect=EOFError):
            main()
