import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tp1.partie_b import demander_bornes, jouer


class NombreTests(unittest.TestCase):
    def test_indices_et_victoire(self):
        sortie = io.StringIO()
        with patch("tp1.partie_b.random.randint", return_value=50), \
                patch("builtins.input", side_effect=["10", "90", "50"]), redirect_stdout(sortie):
            self.assertTrue(jouer())
        for texte in ["Trop petit", "Trop grand", "Gagné"]:
            self.assertIn(texte, sortie.getvalue())

    def test_dix_essais_maximum(self):
        with patch("tp1.partie_b.random.randint", return_value=100), \
                patch("builtins.input", side_effect=["1"] * 10) as saisie:
            self.assertFalse(jouer())
            self.assertEqual(saisie.call_count, 10)

    def test_saisies_invalides_et_dixieme_essai_gagnant(self):
        with patch("tp1.partie_b.random.randint", return_value=5), \
                patch("builtins.input", side_effect=["abc", "0", "11"] + ["1"] * 9 + ["5"]):
            self.assertTrue(jouer(1, 10))

    def test_bornes(self):
        with self.assertRaises(ValueError):
            jouer(10, 1)
        with patch("builtins.input", side_effect=["x", "9", "1", "", ""]):
            self.assertEqual(demander_bornes(), (1, 100))
        with patch("builtins.input", return_value="-2"):
            self.assertTrue(jouer(-2, -2))
