import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tp1.bonus import charger_scores, demander_nom, rejouer, session


class ScoresTests(unittest.TestCase):
    def test_deux_victoires_et_relance(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "scores.txt"
            with patch("builtins.input", side_effect=["o", "n"]):
                session(Mock(return_value=True), "Ana", fichier)
            self.assertEqual(fichier.read_text(encoding="utf-8"), "Ana:2.0\n")
            with patch("builtins.input", return_value="n"):
                session(Mock(return_value=False), "Ana", fichier)
            self.assertEqual(charger_scores(fichier), {"Ana": 2.0})

    def test_compteurs_invalides(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "scores.txt"
            fichier.write_text("Ana:2.0\nBob:-1\nClaire:1.5\nX:inf\n", encoding="utf-8")
            self.assertEqual(charger_scores(fichier), {"Ana": 2.0})

    def test_sauvegarde_avant_interruption(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "scores.txt"
            with patch("builtins.input", side_effect=EOFError), self.assertRaises(EOFError):
                session(Mock(return_value=True), "Ana", fichier)
            self.assertEqual(charger_scores(fichier), {"Ana": 1.0})

    def test_questions(self):
        with patch("builtins.input", side_effect=["", "A:B", " Ana "]):
            self.assertEqual(demander_nom(), "Ana")
        with patch("builtins.input", side_effect=["peut-être", "O"]):
            self.assertTrue(rejouer())
