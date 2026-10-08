import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tp1.partie_d import demander_mot, jouer


class PenduTests(unittest.TestCase):
    def test_victoire_python(self):
        with patch("builtins.input", side_effect=list("python")):
            self.assertTrue(jouer("Python"))

    def test_sept_erreurs(self):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=list("abcdefg")) as saisie, redirect_stdout(sortie):
            self.assertFalse(jouer("PYTHON"))
            self.assertEqual(saisie.call_count, 7)
        self.assertIn("Perdu, le mot était PYTHON", sortie.getvalue())

    def test_repetitions_et_invalides_sans_penalite(self):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=["", "12", "ab", "a", "A", "p", "P", "y", "t", "h", "o", "n"]), redirect_stdout(sortie):
            self.assertTrue(jouer("PYTHON"))
        self.assertIn("Erreurs : 1/7", sortie.getvalue())
        self.assertNotIn("Erreurs : 2/7", sortie.getvalue())

    def test_accent_et_occurrences(self):
        with patch("builtins.input", side_effect=["e\u0301", "l", "p", "h", "a", "n", "t"]):
            self.assertTrue(jouer("ÉLÉPHANT"))
        with patch("builtins.input", return_value="a") as saisie:
            self.assertTrue(jouer("AAA"))
            self.assertEqual(saisie.call_count, 1)

    def test_mot_deux_joueurs_et_mot_invalide(self):
        with patch("tp1.partie_d.getpass", side_effect=["123", "éléphant"]):
            self.assertEqual(demander_mot(), "ÉLÉPHANT")
        with self.assertRaises(ValueError):
            jouer("")
